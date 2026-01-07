"""
Source file handling - location, download, and extraction

Handles all operations related to finding, downloading, and extracting source files.
"""

import os
import hashlib
import tarfile
import zipfile
import gzip
import shutil
import urllib.request
import urllib.error
from pathlib import Path
from typing import Dict, Optional
import logging

from common.exceptions import SpecParseError


class SourceHandler:
    """Handles source file operations including finding, downloading, and extracting"""

    def __init__(self, spec_dir: Path, config_yaml_data: Optional[Dict] = None,
                 shared_sources_data: Optional[Dict] = None,
                 logger: Optional[logging.Logger] = None, verbose: bool = False):
        """
        Initialize source handler

        Args:
            spec_dir: Directory containing the spec file
            config_yaml_data: Optional config.yaml data for source information
            shared_sources_data: Optional shared sources data
            logger: Optional logger instance
            verbose: Enable verbose output
        """
        self.spec_dir = spec_dir
        self.config_yaml_data = config_yaml_data
        self.shared_sources_data = shared_sources_data or {}
        self.logger = logger or logging.getLogger(__name__)
        self.verbose = verbose

    def find_source_file(self, source_name: str) -> Path:
        """Find the source file, handling URLs, local paths, and config.yaml sources"""
        # If it's a URL, extract the filename
        source_url = None
        if source_name.startswith(('http://', 'https://', 'ftp://')):
            source_url = source_name
            filename = os.path.basename(source_name)
        else:
            filename = source_name

        # Look for the file locally
        try:
            return self._find_local_source_file(filename)
        except FileNotFoundError:
            # First check if we have this source in config.yaml
            config_source = self._find_source_in_config(filename)
            if config_source:
                expected_checksum = config_source.get("archive_sha512sum")
            else:
                expected_checksum = ""

            # Try to download from Broadcom Photon sources repository
            self.logger.info(f"Source {filename} not found locally, trying Broadcom Photon sources \
                                repository...")
            photon_sources_url = f"https://packages.broadcom.com/photon/photon_sources/1.0/{filename}"
            try:
                return self._download_from_url(photon_sources_url, filename,
                                               expected_checksum=expected_checksum)
            except (FileNotFoundError, SpecParseError, Exception) as e:
                self.logger.warning(f"Could not download from Photon sources: {e}")

            if config_source:
                return self._get_source_from_config(config_source, filename)

            # If local search fails, we can't get it from broadcom, then try to download from the
            # external URL
            if source_url:
                self.logger.info(f"Source not found  or within Broadcom Photon sources repository, \
                                    downloading from URL: {source_url}")
                return self._download_from_url(source_url, filename,
                                                    expected_checksum=expected_checksum)

            # Re-raise the original error if all attempts failed
            raise FileNotFoundError(f"Source file not found: {filename}")

    def _find_source_in_config(self, filename: str) -> Optional[Dict]:
        """Find source configuration in config.yaml or shared sources"""
        # Check config.yaml
        if self.config_yaml_data:
            for source in self.config_yaml_data.get('sources', []):
                if source.get('archive') == filename:
                    return source

        # Check shared sources
        if filename in self.shared_sources_data:
            return self.shared_sources_data[filename]

        return None

    def _find_local_source_file(self, filename: str) -> Path:
        """Find source file in local directories, searching recursively under spec's parent directory"""
        # 1. Look for the file directly in the spec directory
        source_path = self.spec_dir / filename
        if source_path.exists():
            self.logger.debug(f"Found {filename} in spec directory")
            return source_path

        # 2. Look in common source directories (exact match)
        search_paths = [
            self.spec_dir / 'SOURCES' / filename,
            self._find_photon_root() / 'stage' / 'SOURCES' / filename,
        ]

        for potential_path in search_paths:
            if potential_path.exists():
                self.logger.debug(f"Found {filename} at {potential_path}")
                return potential_path

        # 3. Search recursively under the spec file's parent directory
        self.logger.debug(f"Searching recursively for {filename} under {self.spec_dir}")

        # Get the parent directory that contains the spec file
        search_root = self.spec_dir

        # Search recursively in the spec directory and its subdirectories
        found_files = list(search_root.rglob(filename))
        if len(found_files) > 1:
            raise SpecParseError(f"Multiple files found for {filename}: {found_files}")
        elif len(found_files) == 1:
            return found_files[0]

        raise FileNotFoundError(f"Source file not found: {filename}")

    def _get_source_from_config(self, config_source: Dict, filename: str) -> Path:
        """Get source file based on config.yaml information"""
        # Check if we have git repository information
        repo_url = config_source.get('repo_url')
        commit_id = config_source.get('commit_id')

        # For git sources, return special marker that will be handled by prep execution
        if repo_url and commit_id:
            # Return just the filename - git clone will be handled during prep
            return Path(filename)

        # Otherwise, download or find the archive
        return self._download_source_archive(config_source, filename)

    def _download_source_archive(self, config_source: Dict, filename: str) -> Path:
        """Download source archive from URL with checksum verification"""
        source_url = config_source.get('url', '')
        checksum = config_source.get('archive_sha512sum', '')

        # Check if we already have the file locally with correct checksum
        local_path = self._find_local_archive(filename, checksum)
        if local_path:
            return local_path

        # If no URL in config, try to find it locally without checksum validation
        if not source_url:
            self.logger.debug(f"No URL in config for {filename}, searching locally without checksum validation")
            try:
                return self._find_local_source_file(filename)
            except FileNotFoundError:
                raise SpecParseError(f"No URL specified for source {filename} in config.yaml and file not found locally")

        # Download from URL
        return self._download_from_url(source_url, filename, checksum)

    def _find_local_archive(self, filename: str, expected_checksum: str) -> Optional[Path]:
        """Search for archive in common locations and verify checksum"""
        search_paths = [
            self.spec_dir / filename,
            self._find_photon_root() / 'stage' / 'SOURCES' / filename,
        ]

        for path in search_paths:
            if path.exists() and path.is_file():
                if not expected_checksum or self._verify_checksum(path, expected_checksum):
                    self.logger.info(f"Found {filename} locally at {path}")
                    return path
                else:
                    self.logger.warning(f"Found {filename} at {path} but checksum mismatch")

        return None

    def _download_from_url(self, source_url: str, filename: str, expected_checksum: str) -> Path:
        """Download source from URL and verify checksum"""
        # Create cache directory
        photon_root = self._find_photon_root()
        cache_dir = photon_root / 'stage' / 'SOURCES'
        cache_dir.mkdir(parents=True, exist_ok=True)

        dest_path = cache_dir / filename

        # Check if already downloaded with correct checksum
        if dest_path.exists() and (not expected_checksum or self._verify_checksum(dest_path, expected_checksum)):
            self.logger.info(f"Using cached {filename} from {dest_path}")
            return dest_path

        self.logger.info(f"Downloading {filename} from {source_url}...")

        try:
            # Create request with User-Agent header to avoid 403 errors from some servers
            request = urllib.request.Request(
                source_url,
                headers={'User-Agent': 'spec2git/1.0 (Photon OS package conversion tool)'}
            )

            # Download with progress indication for large files
            with urllib.request.urlopen(request, timeout=300) as response:
                content_length = response.headers.get('Content-Length')

                with open(dest_path, 'wb') as out_file:
                    if content_length:
                        # Download with progress
                        total_size = int(content_length)
                        downloaded = 0
                        chunk_size = 8192

                        while True:
                            chunk = response.read(chunk_size)
                            if not chunk:
                                break
                            out_file.write(chunk)
                            downloaded += len(chunk)

                            if self.verbose:
                                progress = (downloaded / total_size) * 100
                                print(f"\rDownloading: {progress:.1f}%", end='', flush=True)

                        if self.verbose:
                            print()  # New line after progress
                    else:
                        # Download without progress
                        out_file.write(response.read())

        except urllib.error.URLError as e:
            raise SpecParseError(f"Failed to download {filename} from {source_url}: {e}")
        except Exception as e:
            # Clean up partial download
            if dest_path.exists():
                dest_path.unlink()
            raise SpecParseError(f"Error downloading {filename}: {e}")

        # Verify checksum if provided
        if expected_checksum and not self._verify_checksum(dest_path, expected_checksum):
            dest_path.unlink()
            raise SpecParseError(
                f"Checksum verification failed for {filename}\n"
                f"Downloaded file does not match expected SHA512 checksum"
            )

        self.logger.info(f"Downloaded {filename} to {dest_path}")
        return dest_path

    def _find_photon_root(self) -> Path:
        """Find the Photon repository root directory"""
        # Start from spec directory and search upwards for common markers
        current = self.spec_dir.resolve()

        while current != current.parent:
            # Check for common Photon root markers
            if (current / 'SPECS').exists() or (current / 'stage').exists():
                return current
            current = current.parent

        # Fallback to spec_dir parent
        return self.spec_dir.parent

    def _verify_checksum(self, file_path: Path, expected_checksum: str) -> bool:
        """Verify file SHA512 checksum"""
        if not expected_checksum:
            return True

        sha512_hash = hashlib.sha512()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(65536), b""):
                sha512_hash.update(byte_block)

        actual_checksum = sha512_hash.hexdigest()
        return actual_checksum == expected_checksum
