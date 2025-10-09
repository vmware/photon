"""
Spec file parsing functionality

Extracted from monolithic classes for better separation of concerns.
"""

import re
import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import logging
import os
import json

from common.exceptions import SpecParseError


# Pre-compiled regex patterns
NAME_PATTERN = re.compile(r'^Name:\s*(.+)$', re.MULTILINE)
VERSION_PATTERN = re.compile(r'^Version:\s*(.+)$', re.MULTILINE)
RELEASE_PATTERN = re.compile(r'^Release:\s*(.+)$', re.MULTILINE)
SOURCE_PATTERN = re.compile(r'^Source(\d*?):\s*(.+)$', re.MULTILINE)
PATCH_PATTERN = re.compile(r'^Patch(\d+):\s*(.+)$', re.MULTILINE)
MACRO_DEFINE_PATTERN = re.compile(r'^%(?:global|define)\s+(\w+)\s+(.+)$', re.MULTILINE)
MACRO_DEFINE_NO_VALUE_PATTERN = re.compile(r'^%(?:global|define)\s+(\w+)$', re.MULTILINE)
MACRO_PATTERN = re.compile(r'%\{([^}]+)\}')
AUTOPATCH_PATTERN = re.compile(r'%autopatch\s+(?:-p(\d+)\s*)?(?:-m(\d+)\s*)?(?:-M(\d+))?')
AUTOSETUP_PATTERN = re.compile(r'%autosetup\s+(?:.*-p(\d+))?')


class SpecFileParser:
    """Parse RPM spec files and extract relevant information"""

    def __init__(self, spec_file_path: Path, logger: Optional[logging.Logger] = None,
                 target_arch: Optional[str] = None):
        """
        Initialize the spec file parser

        Args:
            spec_file_path: Path to the .spec file
            logger: Optional logger instance
            target_arch: Optional target architecture for rpmspec
        """
        self.spec_file = spec_file_path
        self.logger = logger or logging.getLogger(__name__)
        self.target_arch = target_arch

        # Parsed data
        self.name: str = ""
        self.version: str = ""
        self.release: str = ""
        self.sources: Dict[int, str] = {}
        self.patches: Dict[int, str] = {}
        self.macros: Dict[str, str] = {}
        self.patch_ranges: List[Tuple[int, int, int]] = []  # (min, max, strip_level)
        self.prep_section: str = ""  # Full %prep section content

        # Attributes for rpmspec-expanded prep section
        self.prep_section_build_dir: Optional[str] = None
        self.prep_section_sources_dir: Optional[str] = None
        self.prep_section_spec_dir: Optional[str] = None
        self.prep_section_temp_dir: Optional[str] = None

    def parse(self, additional_macros: Optional[Dict[str, str]] = None,
              build_dir: Optional[Path] = None) -> None:
        """
        Parse the spec file and extract all relevant information

        Args:
            additional_macros: Additional macro definitions to merge
            build_dir: Optional build directory to use for rpmspec _builddir macro

        Raises:
            SpecParseError: If spec file cannot be parsed
        """
        # Store build_dir for use in prep section expansion
        self._build_dir = build_dir
        if not self.spec_file.exists():
            raise SpecParseError(f"Spec file not found: {self.spec_file}")

        # Get dist tag
        self.dist_tag = self._get_dist_tag(self.spec_file)

        # Step 1: Create RPM directory structure
        rpm_root, sources_dir, build_dir = self._setup_rpm_directory_structure(build_dir)

        # Step 2: Copy/symlink ALL files from spec dir to sources dir (flattened)
        self._copy_all_spec_files_to_sources(sources_dir)

        # Step 3: First rpmspec call - expand full spec to get conditional sources/patches
        expanded_spec = self._expand_full_spec(rpm_root, sources_dir)
        self._parse_basic_info(expanded_spec)
        self._parse_sources(expanded_spec)
        self._parse_patches(expanded_spec)

        # Step 4: Parse expanded sources and download/copy them to sources dir
        self._ensure_sources_in_sourcedir(sources_dir)

        # Step 5: Second rpmspec call - get prep section with all files available
        self._generate_prep_section_with_rpmspec(rpm_root, sources_dir, build_dir)

        self.logger.debug(f"Parsed spec: {self.name}-{self.version}-{self.release}")
        self.logger.debug(f"Found {len(self.sources)} sources, {len(self.patches)} patches")


    def _get_dist_tag(self, spec_path):
        # find build-config.json
        ph_root = os.path.abspath(spec_path)
        while os.path.basename(ph_root) != "SPECS" and ph_root:
            ph_root = os.path.dirname(ph_root)

        if not ph_root:
            raise SpecParseError(f"Failed to find the ./SPECS path for {spec_path}! \
                                    Can't locate build-config.json.")

        ph_root = os.path.dirname(ph_root)

        with open(f"{ph_root}/build-config.json") as build_conf:
            build_config_json = json.load(build_conf)
            return build_config_json["photon-build-param"][
                "photon-dist-tag"
            ]

    def _setup_rpm_directory_structure(self, build_dir: Optional[Path] = None) -> Tuple[Path, Path, Path]:
        """
        Step 1: Create RPM directory structure.

        Args:
            build_dir: Optional build directory to use for _builddir macro

        Returns:
            Tuple of (rpm_root, sources_dir, build_dir)
        """
        # Create RPM directory structure under ~/.spec2git
        home = Path.home()
        rpm_root = home / '.spec2git' / f'rpm-{os.getpid()}'
        sources_dir = rpm_root / 'SOURCES'
        specs_dir = rpm_root / 'SPECS'

        # Use provided build_dir or rpm_root as the _builddir
        if build_dir is None:
            build_dir = rpm_root

        # Clean up old directory if it exists
        if rpm_root.exists():
            shutil.rmtree(rpm_root)

        # Create directory structure
        sources_dir.mkdir(parents=True)
        specs_dir.mkdir(parents=True)

        self.logger.debug(f"Created RPM directory structure at {rpm_root}")

        return rpm_root, sources_dir, build_dir

    def _copy_all_spec_files_to_sources(self, sources_dir: Path) -> None:
        """
        Step 2: Symlink ALL files from spec directory to sources dir (flattened, no subdirectories).
        This ensures rpmspec can find any file it might reference.

        Args:
            sources_dir: Path to SOURCES directory
        """
        spec_dir = self.spec_file.parent
        linked_count = 0

        # Iterate through all files in spec_dir (recursively)
        for file_path in spec_dir.rglob('*'):
            if file_path.is_file():
                # Flatten: use only the filename, no subdirectories
                dest_path = sources_dir / file_path.name

                # Skip if already exists (in case of duplicate filenames in subdirs)
                if dest_path.exists():
                    continue

                try:
                    # Create symlink instead of copying
                    dest_path.symlink_to(file_path)
                    linked_count += 1
                except (OSError, IOError) as e:
                    self.logger.warning(f"Could not symlink {file_path.name}: {e}")

        self.logger.debug(f"Symlinked {linked_count} files from spec directory to SOURCES/")

    def _expand_full_spec(self, rpm_root: Path, sources_dir: Path) -> str:
        """
        Step 3: First rpmspec call - expand the full spec file to resolve conditionals and get sources/patches.
        All spec files are already in SOURCES/, so rpmspec can reference them.

        Args:
            rpm_root: Root directory for RPM structure
            sources_dir: Directory containing sources (for _sourcedir macro)

        Returns:
            Fully expanded spec file content
        """
        try:
            cmd = ['rpmspec', '-P']

            # Set RPM directory macros so rpmspec knows where to find files
            cmd.extend(['-D', f'_topdir {rpm_root}'])
            cmd.extend(['-D', f'_sourcedir {sources_dir}'])

            # Add user macro definitions
            for macro_name, macro_value in self.macros.items():
                if macro_name not in ['name', 'version', '_arch']:
                    cmd.extend(['-D', f'{macro_name} {macro_value}'])

            # Add dist tag
            cmd.extend(['-D', f'dist {self.dist_tag}'])

            # Add target arch if specified
            if self.target_arch:
                cmd.extend(['--target', self.target_arch])

            cmd.append(str(self.spec_file))

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

            if result.returncode == 0:
                self.logger.debug("Expanded spec file with rpmspec (first pass)")
                return result.stdout
            else:
                raise SpecParseError(f"rpmspec failed: {result.stderr}")

        except SpecParseError:
            raise
        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            raise SpecParseError(f"Failed to run rpmspec: {e}")
        except Exception as e:
            raise SpecParseError(f"Error during spec expansion: {e}")

    def _ensure_sources_in_sourcedir(self, sources_dir: Path) -> None:
        """
        Step 4: Parse expanded sources and ensure they are in the sources directory.
        For remote sources (URLs), download them. For local sources, ensure they're symlinked.

        Args:
            sources_dir: Path to SOURCES directory
        """
        spec_dir = self.spec_file.parent
        from spec2git_lib.source_handler import SourceHandler
        source_handler = SourceHandler(spec_dir, {}, {}, logger=self.logger)

        for source_num, source_file in self.sources.items():
            # Check if it's a URL
            if source_file.startswith(('http://', 'https://', 'ftp://')):
                # Extract filename from URL
                from urllib.parse import urlparse
                parsed = urlparse(source_file)
                filename = Path(parsed.path).name
                dest_path = sources_dir / filename

                if not dest_path.exists():
                    self.logger.debug(f"Source{source_num} is a URL, needs downloading: {source_file}")
                    # Note: SourceHandler will handle the actual download
                    try:
                        source_path = source_handler.find_source_file(source_file)
                        if source_path and source_path.exists():
                            # For downloaded files, we need to copy not symlink
                            shutil.copy2(source_path, dest_path)
                            self.logger.debug(f"Downloaded/copied {filename} to SOURCES/")
                    except Exception as e:
                        self.logger.warning(f"Could not download/find source {source_file}: {e}")
            else:
                # Local file - should already be symlinked from step 2
                dest_path = sources_dir / Path(source_file).name
                if not dest_path.exists():
                    # Try to find and symlink it
                    try:
                        source_path = source_handler.find_source_file(source_file)
                        if source_path:
                            dest_path.symlink_to(source_path)
                            self.logger.debug(f"Symlinked missing source {source_file} to SOURCES/")
                    except Exception as e:
                        self.logger.warning(f"Could not find source {source_file}: {e}")

    def _generate_prep_section_with_rpmspec(self, rpm_root: Path, sources_dir: Path,
                                            build_dir: Path) -> None:
        """
        Step 5: Second rpmspec call - generate prep shell script with all files available.

        Args:
            rpm_root: Root directory for RPM structure
            sources_dir: Directory containing sources
            build_dir: Build directory for _builddir macro
        """
        try:
            # Create truncated spec and run rpmspec
            rpmspec_output = self._create_truncated_spec_and_run_rpmspec(rpm_root, sources_dir, build_dir)

            # Extract and store the prep section
            self.prep_section_sources_dir = str(sources_dir)
            self.prep_section_temp_dir = str(rpm_root)

            expanded_prep = self._extract_prep_from_rpmspec_output(rpmspec_output, build_dir, sources_dir)
            if expanded_prep:
                self.prep_section = expanded_prep
                self.logger.debug(f"Generated prep shell script ({len(expanded_prep.split(chr(10)))} lines)")

        except SpecParseError:
            # Re-raise SpecParseError (e.g., missing sources/patches) - don't catch these
            raise
        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            self.logger.warning(f"Could not use rpmspec for spec expansion: {e}")
            raise SpecParseError(f"Failed to run rpmspec: {e}")
        except Exception as e:
            self.logger.warning(f"Error during rpmspec expansion: {e}")
            raise SpecParseError(f"Error during spec expansion: {e}")

    def _create_truncated_spec_and_run_rpmspec(self, rpm_root: Path, sources_dir: Path,
                                                build_dir: Path) -> str:
        """
        Create a truncated spec file and run rpmspec to expand it.

        Args:
            rpm_root: Root directory for RPM structure
            sources_dir: Directory containing sources
            build_dir: Build directory for _builddir macro

        Returns:
            Output from rpmspec -P command

        Raises:
            SpecParseError: If rpmspec fails
        """
        # Create truncated spec file (cut off at %build to only process up to %prep)
        truncated_spec = rpm_root / 'SPECS' / 'truncated.spec'
        truncated_spec.parent.mkdir(exist_ok=True)

        with open(self.spec_file, 'r', encoding='utf-8', errors='replace') as f:
            spec_content = f.read()

        lines = spec_content.split('\n')
        truncated_lines = []
        for line in lines:
            stripped = line.strip()
            if stripped in ['%build', '%install', '%check']:
                break
            truncated_lines.append(line)

        with open(truncated_spec, 'w', encoding='utf-8') as f:
            f.write('\n'.join(truncated_lines))

        # Run rpmspec with RPM directory structure on truncated spec
        cmd = ['rpmspec', '-P']
        cmd.extend(['-D', f'_topdir {rpm_root}'])
        cmd.extend(['-D', f'_sourcedir {sources_dir}'])
        cmd.extend(['-D', f'_builddir {build_dir}'])
        cmd.extend(['-D', f'dist {self.dist_tag}'])

        # Add user macro definitions
        for macro_name, macro_value in self.macros.items():
            if macro_name not in ['name', 'version', '_arch']:
                cmd.extend(['-D', f'{macro_name} {macro_value}'])

        # Add target arch if specified
        if self.target_arch:
            cmd.extend(['--target', self.target_arch])

        cmd.append(str(truncated_spec))

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            self.logger.debug("Expanded spec file with rpmspec (second pass for prep)")
            return result.stdout
        else:
            raise SpecParseError(f"rpmspec failed: {result.stderr}")

    def _extract_prep_from_rpmspec_output(self, rpmspec_output: str,
                                          build_dir: Path, sources_dir: Path) -> str:
        """
        Extract the %prep section shell commands from rpmspec -P output.

        Args:
            rpmspec_output: Output from rpmspec -P
            build_dir: Path to BUILD directory used in rpmspec
            sources_dir: Path to SOURCES directory used in rpmspec

        Returns:
            Extracted prep section with shell commands
        """
        lines = rpmspec_output.split('\n')
        in_prep = False
        prep_lines = []

        # Section markers in rpmspec output
        section_markers = ['%build', '%install', '%check', '%files', '%changelog']

        for line in lines:
            stripped = line.strip()

            # Start of prep section
            if stripped == '%prep':
                in_prep = True
                continue

            # End of prep section
            if in_prep:
                # Check if we hit another section
                if any(stripped.startswith(marker) for marker in section_markers):
                    break

                # The paths in the output reference our temp directories, which is correct
                # since we keep the temp directory around with all sources
                prep_lines.append(line)

        return '\n'.join(prep_lines).strip()

    def _parse_basic_info(self, content: str) -> None:
        """Extract name, version, release from spec content"""
        name_match = NAME_PATTERN.search(content)
        version_match = VERSION_PATTERN.search(content)
        release_match = RELEASE_PATTERN.search(content)

        # Extract raw values first
        if name_match:
            self.name = name_match.group(1).strip()
        if version_match:
            self.version = version_match.group(1).strip()
        if release_match:
            self.release = release_match.group(1).strip()

        if not self.name:
            raise SpecParseError("Could not find 'Name:' field in spec file")
        if not self.version:
            raise SpecParseError("Could not find 'Version:' field in spec file")

    def _parse_sources(self, content: str) -> None:
        """Parse Source definitions"""
        for match in SOURCE_PATTERN.finditer(content):
            source_num = match.group(1) or "0"
            source_file = match.group(2).strip()
            self.sources[int(source_num)] = source_file

        if not self.sources:
            raise SpecParseError("No Source definitions found in spec file")

    def _parse_patches(self, content: str) -> None:
        """
        Parse Patch definitions

        Stores patches as: {basename: patch_num}
        This allows fast lookup by filename during patch detection
        """
        for match in PATCH_PATTERN.finditer(content):
            patch_num = int(match.group(1))
            patch_file = match.group(2).strip()
            # Use basename as key for fast lookup
            basename = Path(patch_file).name
            self.patches[basename] = patch_num
