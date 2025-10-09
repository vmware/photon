"""
Spec file parsing for git2spec conversion

This module handles parsing RPM spec files to extract package information,
patches, sources, and configuration data.
"""

import logging
import yaml
from pathlib import Path
from typing import Dict, Optional

from common.exceptions import SpecParseError
from git2spec.git2spec_patterns import (
    NAME_PATTERN,
    VERSION_PATTERN,
    RELEASE_PATTERN,
    PATCH_PATTERN,
    SOURCE0_PATTERN,
    INCLUDE_PATTERN,
    SOURCE_REF_PATTERN,
)
from git2spec.git2spec_utils import read_file_safe, expand_macros_simple, expand_source_macros


class Git2SpecParser:
    """
    Parser for RPM spec files in git2spec context

    Extracts package information, patches, and configuration needed
    for converting git repositories back to spec files.
    """

    def __init__(self, spec_file: Path, verbose: bool = False):
        """
        Initialize spec file parser

        Args:
            spec_file: Path to spec file
            verbose: Enable verbose logging
        """
        self.spec_file = spec_file
        self.spec_dir = spec_file.parent
        self.verbose = verbose

        self.logger = logging.getLogger(f'{__name__}.Git2SpecParser')
        if verbose:
            self.logger.setLevel(logging.DEBUG)

        # Parsed data
        self.name = ""
        self.version = ""
        self.release = ""
        self.patches: Dict[int, str] = {}
        self.config_yaml_data: Dict = {}
        self.shared_sources_data: Dict = {}
        self.base_commit_id: Optional[str] = None

    def parse(self) -> Dict:
        """
        Parse spec file and extract all relevant information

        Returns:
            Dictionary containing:
                - name: Package name
                - version: Package version
                - release: Package release
                - patches: Dict mapping patch numbers to filenames
                - base_commit_id: Base commit ID from config.yaml (if present)

        Raises:
            SpecParseError: If parsing fails or required fields missing
        """
        self.logger.info(f"Parsing spec file: {self.spec_file}")

        # Read spec file
        spec_content = read_file_safe(self.spec_file)

        # Parse basic fields
        self._parse_basic_fields(spec_content)

        # Parse patches
        self._parse_patches(spec_content)

        # Parse config.yaml for base commit
        self._parse_config_yaml(spec_content)

        self.logger.info(
            f"Parsed package: {self.name}-{self.version}-{self.release} "
            f"with {len(self.patches)} patches"
        )

        return {
            'name': self.name,
            'version': self.version,
            'release': self.release,
            'patches': self.patches,
            'base_commit_id': self.base_commit_id,
        }

    def _parse_basic_fields(self, spec_content: str) -> None:
        """
        Parse basic package fields (Name, Version, Release)

        Args:
            spec_content: Full spec file content

        Raises:
            SpecParseError: If required fields are missing
        """
        # Parse Name
        name_match = NAME_PATTERN.search(spec_content)
        if name_match:
            self.name = name_match.group(1).strip()

        # Parse Version
        version_match = VERSION_PATTERN.search(spec_content)
        if version_match:
            self.version = version_match.group(1).strip()

        # Parse Release
        release_match = RELEASE_PATTERN.search(spec_content)
        if release_match:
            self.release = release_match.group(1).strip()

        # Validate required fields
        if not self.name:
            raise SpecParseError("Could not find 'Name:' field in spec file")
        if not self.version:
            raise SpecParseError("Could not find 'Version:' field in spec file")

        self.logger.debug(f"Package: {self.name}-{self.version}-{self.release}")

    def _parse_patches(self, spec_content: str) -> None:
        """
        Parse patch definitions from spec file

        Args:
            spec_content: Full spec file content
        """
        # Parse all Patch definitions directly
        for match in PATCH_PATTERN.finditer(spec_content):
            patch_num = int(match.group(1))
            patch_file = match.group(2).strip()
            self.patches[patch_num] = patch_file
            if self.verbose:
                self.logger.debug(f"Parsed Patch{patch_num}: {patch_file}")

        # Parse patches from %include files
        self._parse_include_patches(spec_content)

        # Sort patches by number
        self.patches = dict(sorted(self.patches.items()))

        self.logger.debug(f"Found {len(self.patches)} patches in spec file")

    def _parse_include_patches(self, spec_content: str) -> None:
        """
        Parse patch definitions from %include files

        Args:
            spec_content: Full spec file content
        """
        for match in INCLUDE_PATTERN.finditer(spec_content):
            include_ref = match.group(1).strip()

            # Expand macros in the include reference
            expanded_ref = expand_macros_simple(include_ref, {
                'name': self.name,
                'version': self.version,
                'NAME': self.name.upper() if self.name else '',
            })

            # Check if it's a Source reference pattern like %{SOURCE6}
            source_match = SOURCE_REF_PATTERN.match(include_ref)

            if source_match:
                source_num = int(source_match.group(1))
                # Find this source in the spec
                source_pattern = PATCH_PATTERN  # Reuse for Source pattern
                source_pattern_str = rf'^Source{source_num}:\s*(.+)$'
                import re
                source_find = re.search(source_pattern_str, spec_content, re.MULTILINE | re.IGNORECASE)
                if source_find:
                    include_file = source_find.group(1).strip()
                    self._parse_patches_from_include_file(include_file)
                else:
                    self.logger.warning(
                        f"Source{source_num} referenced in %include but not defined"
                    )
            elif expanded_ref != include_ref:
                # Macro was expanded
                self._parse_patches_from_include_file(expanded_ref)
            else:
                # Direct file reference
                self._parse_patches_from_include_file(expanded_ref)

    def _parse_patches_from_include_file(self, filename: str) -> None:
        """
        Parse Patch definitions from an included file

        Args:
            filename: Name of file to parse
        """
        # Try to find the file
        include_paths = [
            self.spec_dir / filename,
            self.spec_dir / 'SOURCES' / filename,
        ]

        include_file = None
        for path in include_paths:
            if path.exists():
                include_file = path
                break

        if not include_file:
            self.logger.debug(
                f"Include file not found: {filename} "
                f"(searched: {[str(p) for p in include_paths]})"
            )
            return

        try:
            self.logger.debug(f"Parsing patches from include file: {include_file}")
            include_content = read_file_safe(include_file)

            # Parse Patch definitions
            patches_found = 0
            for match in PATCH_PATTERN.finditer(include_content):
                patch_num = int(match.group(1))
                patch_file = match.group(2).strip()
                self.patches[patch_num] = patch_file
                patches_found += 1

            if patches_found > 0:
                self.logger.info(
                    f"Found {patches_found} patches in included file: {filename}"
                )

        except SpecParseError as e:
            self.logger.warning(f"Failed to read include file {include_file}: {e}")

    def _parse_config_yaml(self, spec_content: str) -> None:
        """
        Parse config.yaml file to get base commit_id for git sources

        Args:
            spec_content: Full spec file content (used to find Source0)
        """
        config_yaml_path = self.spec_dir / "config.yaml"

        if not config_yaml_path.exists():
            self.logger.debug("No config.yaml found")
            return

        try:
            with open(config_yaml_path, 'r', encoding='utf-8') as f:
                self.config_yaml_data = yaml.safe_load(f) or {}
        except (IOError, OSError, yaml.YAMLError) as e:
            self.logger.warning(f"Failed to parse config.yaml: {e}")
            return

        # Load shared sources if specified
        self._load_shared_sources()

        # Try to find the commit_id for Source0
        source0_match = SOURCE0_PATTERN.search(spec_content)
        if source0_match:
            source0_value = source0_match.group(1).strip()
            filename = expand_source_macros(
                source0_value,
                self.name,
                self.version,
                self.release
            )

            self.logger.debug(f"Looking for source in config.yaml: {filename}")

            # Look in config.yaml sources
            for source in self.config_yaml_data.get('sources', []):
                archive = source.get('archive', '')
                if archive == filename:
                    self.base_commit_id = source.get('commit_id')
                    if self.base_commit_id:
                        self.logger.info(
                            f"Found base commit_id from config.yaml: "
                            f"{self.base_commit_id[:12]}..."
                        )
                    break

            # Also check shared sources
            if not self.base_commit_id and filename in self.shared_sources_data:
                self.base_commit_id = self.shared_sources_data[filename].get('commit_id')
                if self.base_commit_id:
                    self.logger.info(
                        f"Found base commit_id from shared sources: "
                        f"{self.base_commit_id[:12]}..."
                    )

        if not self.base_commit_id:
            self.logger.debug("No git commit_id found in config.yaml (tarball source)")

    def _load_shared_sources(self) -> None:
        """Load shared source configurations"""
        shared_sources = self.config_yaml_data.get('shared_sources', [])
        for shared_config in shared_sources:
            shared_path = self.spec_dir.parent / shared_config
            if shared_path.exists():
                try:
                    with open(shared_path, 'r', encoding='utf-8') as f:
                        shared_data = yaml.safe_load(f) or {}
                        for source in shared_data.get('sources', []):
                            archive_name = source.get('archive', '')
                            if archive_name:
                                self.shared_sources_data[archive_name] = source
                    self.logger.debug(f"Loaded shared config: {shared_config}")
                except (IOError, OSError, yaml.YAMLError) as e:
                    self.logger.warning(
                        f"Failed to load shared config {shared_config}: {e}"
                    )

