"""
Spec2Git workflow implementation

Orchestrates the conversion from RPM spec file to git repository.
"""

import os
import shutil
import subprocess
import yaml
from pathlib import Path
from typing import Optional, Dict

from spec2git_lib.base_workflow import BaseWorkflow
from spec2git_lib.result_types import ConversionResult
from spec2git_lib.conversion_state import ConversionState
from common.exceptions import SpecParseError, ValidationError, PatchConflictError
from spec2git_lib.prep_executor import PrepExecutor


class Spec2GitWorkflow(BaseWorkflow):
    """
    Workflow for converting spec file to git repository

    This class orchestrates the entire conversion process:
    1. Parse spec file
    2. Download sources
    3. Extract sources
    4. Initialize git repository
    5. Execute prep section (includes patches)
    6. Apply remaining patches
    7. Finalize repository
    """

    def execute(self) -> ConversionResult:
        """
        Execute the complete spec to git conversion workflow

        Returns:
            ConversionResult with success status and details
        """
        temp_dir_to_cleanup = None

        try:
            # Phase 1: Parse spec file
            self._log_step("Phase 1", f"Parse spec file: {self.context.state.spec_file.name}")
            self._parse_spec()

            # Store temp directory path for cleanup
            temp_dir_to_cleanup = self.context.spec_parser.prep_section_temp_dir

            # These parts should already be set up
            if not self.context.state.resume:
                # Phase 2: Prepare output directory (handles multi-source BUILD dir)
                self._log_step("Phase 2", f"Setting up {self.context.state.output_dir}")
                self._prepare_output_directory()

                # Phase 3: Locate/download sources and patches (but don't extract yet)
                self._log_step("Phase 3", f"Locate {len(self.context.state.sources)} sources")
                self._download_sources()
            else:
                # When resuming, output_dir IS the build dir, but state might not be updated yet
                # because we skipped _prepare_output_directory
                if self.context.state.output_dir:
                    self.context.state = self.context.state.with_updates(build_dir=self.context.state.output_dir)

            # Phase 4: Execute prep section
            # This will handle extraction, git initialization, and patch application inline
            self._log_step("Phase 4", "Execute %prep section (extraction, git init, patches)")
            patches_applied, git_roots = self._execute_prep_section()

            return ConversionResult(
                success=True,
                git_roots=git_roots,
                output_dir=self.context.state.output_dir,
                patches_applied=patches_applied,
                sources_downloaded=len(self.context.state.downloaded_sources),
            )

        except PatchConflictError:
            return ConversionResult(
                success=False,
                error="Patch conflict detected - stopped for manual resolution",
            )

        except Exception as e:
            self._log_error(f"Conversion failed: {e}")
            return ConversionResult(
                success=False,
                error=str(e),
            )

        finally:
            # Cleanup temporary directories
            self._cleanup_temp_directories(temp_dir_to_cleanup)

    def _validate_environment(self):
        """Validate that required tools are available"""
        # Check for git
        try:
            result = subprocess.run(
                ['git', '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode != 0:
                raise ValidationError("git command not available")
        except (FileNotFoundError, subprocess.TimeoutExpired):
            raise ValidationError("git command not found - please install git")

    def _parse_spec(self):
        """Parse the spec file to extract metadata"""
        parser = self.context.spec_parser

        # Determine output directory if not specified (need this before parsing for rpmspec)
        output_dir = self.context.state.output_dir

        # Need to do initial parse to get name and version for default output_dir
        parser.parse(additional_macros=self.context.state.macros, build_dir=None)
        if not output_dir:
            output_dir = Path.cwd() / f"{parser.name}-{parser.version}-git"
        else:
            output_dir = output_dir / f"{parser.name}-{parser.version}-git"

        # Now re-parse with the correct build_dir
        parser.parse(additional_macros=self.context.state.macros, build_dir=output_dir)

        # Update context with parsed data
        self._update_context(
            name=parser.name,
            version=parser.version,
            release=parser.release,
            sources=parser.sources,
            patches=parser.patches,
            macros=parser.macros,
            output_dir=output_dir,
            prep_section=parser.prep_section,
        )

        # Load config.yaml if it exists
        self._load_config_yaml()

    def _load_config_yaml(self):
        """Load config.yaml from spec directory"""
        config_yaml_path = self.context.state.spec_dir / "config.yaml"

        if not config_yaml_path.exists():
            self.logger.debug("No config.yaml found")
            return

        try:
            with open(config_yaml_path, 'r', encoding='utf-8') as f:
                config_data = yaml.safe_load(f) or {}

            self._update_context(config_yaml_data=config_data)

            # Load shared sources
            shared_sources_data = {}
            for shared_config in config_data.get('shared_sources', []):
                shared_path = self.context.state.spec_dir.parent / shared_config
                if shared_path.exists():
                    try:
                        with open(shared_path, 'r', encoding='utf-8') as f:
                            shared_data = yaml.safe_load(f) or {}
                            for source in shared_data.get('sources', []):
                                archive_name = source.get('archive', '')
                                if archive_name:
                                    shared_sources_data[archive_name] = source
                    except Exception as e:
                        self.logger.warning(f"Failed to load shared config {shared_config}: {e}")

            if shared_sources_data:
                self._update_context(shared_sources_data=shared_sources_data)

        except Exception as e:
            self.logger.warning(f"Failed to parse config.yaml: {e}")

    def _prepare_output_directory(self):
        """
        Prepare the output directory.
        The output_dir serves as the BUILD directory where extraction happens.
        """
        output_dir = self.context.state.output_dir

        if output_dir.exists():
            # If resuming, do not wipe directory
            if self.context.state.resume:
                self.logger.info(f"Resuming build in existing directory: {output_dir}")
            else:
                if not self.context.state.force:
                    raise ValidationError(
                        f"Output directory already exists: {output_dir}\n"
                        f"Use --force to overwrite"
                    )
                self.logger.warning(
                    f"Overwriting existing directory: {output_dir}\n"
                    "There may be conflicts, please manually cleanup if you want to start from a clean state."
                )
        else:
            if self.context.state.resume:
                raise Exception("Resuming is not supported when output directory does not exist")

            output_dir.mkdir(parents=True, exist_ok=True)

        # Output dir IS the build dir - no separate BUILD subdirectory
        self.context.state = self.context.state.with_updates(build_dir=output_dir)

    def _download_sources(self):
        """Download all sources"""
        downloaded = {}

        for source_num, source_name in self.context.state.sources.items():
            # A CLI-provided --repo-url/--repo-commit pair for Source0 means
            # the caller already knows how to get the source and doesn't
            # need (or may not even have) a downloadable tarball -- skip the
            # tarball lookup entirely rather than risk it hanging/failing on
            # an unreachable or nonexistent URL.
            if source_num == 0 and self.context.state.cli_repo_url and self.context.state.cli_repo_commit:
                self._check_source0_git_info(source_name)
                continue

            try:
                source_path = self.context.source_handler.find_source_file(source_name)
                downloaded[source_num] = source_path

                # Check for Source0 git info
                if source_num == 0:
                    self._check_source0_git_info(source_name)

            except FileNotFoundError as e:
                self.logger.warning(f"Could not locate Source{source_num} ({source_name}): {e}")
                self.logger.debug("This may be a conditional source that is not needed")

        self._update_context(downloaded_sources=downloaded)

    def _check_source0_git_info(self, source_name: str):
        """Check if Source0 should use git clone"""
        # Extract filename from URL if source_name is a URL
        if source_name.startswith(('http://', 'https://', 'ftp://')):
            filename = os.path.basename(source_name)
        else:
            filename = source_name

        # CLI-provided repo info always wins, and applies even under
        # --use-tarball (which only disables the config.yaml-derived
        # autodetection below).
        if self.context.state.cli_repo_url and self.context.state.cli_repo_commit:
            self.logger.info(
                f"Using CLI-provided git repository for Source0: "
                f"{self.context.state.cli_repo_url}@{self.context.state.cli_repo_commit}"
            )
            self._update_context(
                source0_git_info={
                    'repo_url': self.context.state.cli_repo_url,
                    'commit_id': self.context.state.cli_repo_commit,
                    'filename': filename,
                }
            )
            return

        if self.context.state.use_tarball:
            return

        # Look for git info in config.yaml
        for source in self.context.state.config_yaml_data.get('sources', []):
            if source.get('archive') == filename:
                repo_url = source.get('repo_url')
                commit_id = source.get('commit_id')
                if repo_url and commit_id:
                    self.logger.info(f"Found git repository for Source0: {repo_url}@{commit_id}")
                    self._update_context(
                        source0_git_info={
                            'repo_url': repo_url,
                            'commit_id': commit_id,
                            'filename': filename,
                        }
                    )
                break


    def _execute_prep_section(self) -> int:
        """Execute the %prep section"""
        prep_section = self.context.state.prep_section
        if not prep_section:
            self.logger.warning("No %prep section found in spec file")
            return 0

        # Create prep executor with build_dir
        state = self.context.state
        from spec2git_lib.prep_executor import PrepExecutor
        from spec2git_lib.patch_handler import PatchHandler

        # Create patch handler
        patch_handler = PatchHandler(
            spec_dir=state.spec_dir,
            patches=state.patches,
            logger=self.logger,
            verbose=state.verbose,
            state=state
        )

        prep_executor = PrepExecutor(
            output_dir=state.build_dir,  # Use build_dir as the working directory
            patches=state.patches,
            sources=state.sources,
            name=state.name,
            version=state.version,
            patch_handler=patch_handler,
            source_handler=self.context.source_handler,
            logger=self.logger,
            verbose=state.verbose,
            stop_before_patch=state.stop_before_patch,
            resume=state.resume,
        )

        # Get path information from spec parser if available
        parser = self.context.spec_parser
        prep_temp_dir = getattr(parser, 'prep_section_temp_dir', None)
        prep_build_dir = getattr(parser, 'prep_section_build_dir', None)
        prep_sources_dir = getattr(parser, 'prep_section_sources_dir', None)

        # Execute prep section - this will handle extraction, git init, and patches
        patches_applied, git_roots = prep_executor.execute_prep_section(
            prep_section,
            self.context.state.source0_git_info,
            rpmspec_build_dir=prep_build_dir,
            rpmspec_sources_dir=prep_sources_dir,
            rpmspec_temp_dir=prep_temp_dir
        )

        return patches_applied, git_roots

    def _finalize_repository(self):
        """Finalize the git repository"""
        # Clean up any temporary files
        if self.context.state.tmp_sources_dir:
            try:
                if self.context.state.tmp_sources_dir.exists():
                    shutil.rmtree(self.context.state.tmp_sources_dir)
            except Exception as e:
                self.logger.debug(f"Failed to clean up temp sources: {e}")

        # Clean up rpmspec temp directory if it exists
        parser = self.context.spec_parser
        prep_temp_dir = getattr(parser, 'prep_section_temp_dir', None)
        if prep_temp_dir:
            try:
                temp_path = Path(prep_temp_dir)
                if temp_path.exists():
                    shutil.rmtree(temp_path)
                    self.logger.debug(f"Cleaned up rpmspec temp directory")
            except Exception as e:
                self.logger.debug(f"Failed to clean up rpmspec temp dir: {e}")

        self.logger.info(f"Conversion complete! See build directory: {self.context.state.build_dir}")

    def _cleanup_temp_directories(self, temp_dir_path: Optional[str] = None):
        """
        Clean up temporary directories created during conversion

        Args:
            temp_dir_path: Path to the temp directory to clean up
        """
        if temp_dir_path:
            try:
                temp_path = Path(temp_dir_path)
                if temp_path.exists():
                    shutil.rmtree(temp_path)
                    self.logger.debug(f"Cleaned up temporary directory: {temp_path}")
            except Exception as e:
                self.logger.debug(f"Failed to clean up temp directory {temp_dir_path}: {e}")

        # Also clean up old rpm-* directories if they exist
        try:
            spec2git_root = Path.home() / '.spec2git'
            if spec2git_root.exists():
                # Find all rpm-* directories
                for rpm_dir in spec2git_root.glob('rpm-*'):
                    if rpm_dir.is_dir():
                        try:
                            shutil.rmtree(rpm_dir)
                            self.logger.debug(f"Cleaned up old temp directory: {rpm_dir.name}")
                        except Exception as e:
                            self.logger.debug(f"Failed to clean up {rpm_dir.name}: {e}")
        except Exception as e:
            self.logger.debug(f"Failed to clean up old temp directories: {e}")

