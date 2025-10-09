"""
Core orchestration for git2spec conversion

This module provides the main Git2Spec class that orchestrates
the conversion of git commits to spec file patches. It maps all
commits after the base to patches without conditional filtering.
"""

import shutil
import logging
from pathlib import Path
from typing import Optional, Dict

from common.exceptions import SpecParseError, ValidationError
from common.config import get_config
from common.validation import validate_git2spec_inputs
from git2spec.git2spec_spec_parser import Git2SpecParser
from git2spec.git2spec_git_analyzer import Git2SpecAnalyzer
from git2spec.git2spec_patch_generator import Git2SpecPatchGenerator
from git2spec.git2spec_spec_updater import Git2SpecUpdater


class Git2Spec:
    """
    Main class for converting git repositories back to spec files

    Maps all commits after the base commit to patches and updates the
    spec file accordingly. No conditional filtering is performed - all
    commits are converted to patches.
    """

    def __init__(self, spec_file: str, git_repo_dir: str,
                 output_spec: Optional[str] = None,
                 changelog_msg: Optional[str] = None,
                 use_commit_msgs: bool = False,
                 verbose: bool = False):
        """
        Initialize the Git2Spec converter

        Args:
            spec_file: Path to the original .spec file
            git_repo_dir: Path to the git repository with changes
            output_spec: Output spec file path (default: overwrite original)
            changelog_msg: Custom changelog message (default: placeholder)
            use_commit_msgs: Use commit messages for changelog (default: False)
            verbose: Enable verbose logging

        Raises:
            ValidationError: If inputs are invalid
            SpecParseError: If spec file doesn't exist or can't create backup
        """
        # Validate inputs
        validate_git2spec_inputs(spec_file, git_repo_dir, changelog_msg)

        # Setup paths
        self.spec_file = Path(spec_file).resolve()
        self.spec_dir = self.spec_file.parent
        self.git_repo_dir = Path(git_repo_dir).resolve()

        if not self.spec_file.exists():
            raise SpecParseError(f"Spec file not found: {self.spec_file}")

        # Handle output spec file with backup if overwriting original
        if output_spec:
            self.output_spec = Path(output_spec).resolve()
            self._backup_created: Optional[Path] = None
        else:
            # Default: overwrite original, create backup first
            self.output_spec = self.spec_file
            backup_path = self.spec_file.with_suffix('.spec.bak')
            try:
                if self.spec_file.exists():
                    shutil.copy2(self.spec_file, backup_path)
                    self._backup_created = backup_path
                else:
                    self._backup_created = None
            except (OSError, IOError, shutil.Error) as e:
                raise SpecParseError(f"Failed to create backup of spec file: {e}")

        # Store configuration
        self.changelog_msg = changelog_msg
        self.use_commit_msgs = use_commit_msgs
        self.verbose = verbose

        # Setup logging
        self.logger = logging.getLogger(f'{__name__}.Git2Spec')
        log_level = logging.DEBUG if verbose else logging.INFO
        self.logger.setLevel(log_level)

        # Log backup creation if it happened
        if self._backup_created:
            self.logger.info(f"Created backup of original spec file: {self._backup_created}")

        # Initialize components
        self.spec_parser = Git2SpecParser(
            self.spec_file,
            verbose=verbose
        )

        self.git_analyzer = Git2SpecAnalyzer(
            self.git_repo_dir,
            self.spec_dir,
            verbose=verbose
        )

        self.patch_generator = Git2SpecPatchGenerator(
            self.git_repo_dir,
            self.spec_dir,
            verbose=verbose
        )

        self.spec_updater = Git2SpecUpdater(
            self.spec_file,
            output_spec=self.output_spec,
            git_repo_dir=self.git_repo_dir,
            changelog_msg=changelog_msg,
            use_commit_msgs=use_commit_msgs,
            verbose=verbose
        )

    def run(self) -> bool:
        """
        Run the git2spec conversion process

        This is the main entry point that orchestrates the entire conversion.

        Returns:
            True if conversion succeeded, False if it failed

        Note:
            This method catches exceptions and returns False for failures,
            allowing the CLI to set appropriate exit codes.
        """
        try:
            # Parse spec file
            self.logger.info("Step 1/4: Parsing spec file...")
            spec_info = self.spec_parser.parse()
            original_patches = spec_info['patches']

            # Analyze git repository
            self.logger.info("Step 2/4: Analyzing git repository...")
            analysis_result = self.git_analyzer.analyze(spec_info, original_patches)

            if not analysis_result['has_changes']:
                self.logger.info("No changes detected in git repository")
                self.logger.info("Spec file unchanged")
                return True

            # Extract patches from commits
            self.logger.info("Step 3/4: Extracting patches from commits...")
            new_patches = self.patch_generator.extract_patches(
                analysis_result,
                original_patches
            )

            if not new_patches:
                self.logger.info("No new patches to add")
                return True

            # Update spec file
            self.logger.info("Step 4/4: Updating spec file...")
            self.spec_updater.update_spec(
                spec_info,
                new_patches,
                analysis_result['modified_commits']
            )

            # Success summary
            self.logger.info("=" * 60)
            self.logger.info("✓ Git to spec conversion completed successfully!")
            self.logger.info(f"  Added/updated patches: {len(new_patches)}")
            self.logger.info(f"  Updated spec file: {self.output_spec}")
            if self._backup_created:
                self.logger.info(f"  Backup saved: {self._backup_created}")
            self.logger.info("=" * 60)

            return True

        except (SpecParseError, ValidationError) as e:
            self.logger.error(f"Conversion failed: {e}")
            if self.verbose:
                import traceback
                traceback.print_exc()
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error during conversion: {e}")
            if self.verbose:
                import traceback
                traceback.print_exc()
            return False

    # Backward compatibility methods - these delegate to the new components

    def parse_spec_file(self) -> None:
        """
        Parse the spec file (backward compatibility method)

        Note: In the new architecture, this is called internally by run().
              This method is provided for backward compatibility with code
              that calls the methods individually.
        """
        spec_info = self.spec_parser.parse()
        # Store results for backward compatibility
        self.name = spec_info['name']
        self.version = spec_info['version']
        self.release = spec_info['release']
        self.original_patches = spec_info['patches']
        self.base_commit_id = spec_info.get('base_commit_id')

    def analyze_git_repo(self) -> bool:
        """
        Analyze git repository (backward compatibility method)

        Returns:
            True if changes detected, False otherwise
        """
        if not hasattr(self, 'original_patches'):
            self.parse_spec_file()

        spec_info = {
            'name': self.name,
            'version': self.version,
            'release': self.release,
            'base_commit_id': self.base_commit_id,
        }

        analysis_result = self.git_analyzer.analyze(spec_info, self.original_patches)

        # Store results for backward compatibility
        self.base_commit = analysis_result['base_commit']
        self.current_commits = analysis_result['current_commits']
        self.new_commits = analysis_result['new_commits']
        self.modified_commits = analysis_result['modified_commits']

        return analysis_result['has_changes']

    def extract_patches_from_commits(self, output_dir: Optional[Path] = None):
        """
        Extract patches from commits (backward compatibility method)

        Args:
            output_dir: Directory to write patch files

        Returns:
            List of tuples: (patch_number, patch_filename, patch_content)
        """
        if not hasattr(self, 'new_commits'):
            raise SpecParseError("Must call analyze_git_repo() first")

        analysis_result = {
            'new_commits': self.new_commits,
            'modified_commits': self.modified_commits,
        }

        return self.patch_generator.extract_patches(
            analysis_result,
            self.original_patches,
            output_dir
        )

    def update_spec_file(self, new_patches) -> None:
        """
        Update spec file (backward compatibility method)

        Args:
            new_patches: List of tuples (patch_number, patch_filename, patch_content)
        """
        spec_info = {
            'name': self.name,
            'version': self.version,
            'release': self.release,
        }

        self.spec_updater.update_spec(
            spec_info,
            new_patches,
            self.modified_commits
        )


def validate_git2spec_inputs(spec_file: str, git_repo_dir: str,
                             changelog_msg: Optional[str]) -> None:
    """
    Validate input parameters for Git2Spec

    Args:
        spec_file: Path to spec file
        git_repo_dir: Path to git repository
        changelog_msg: Changelog message

    Raises:
        ValidationError: If any input is invalid
    """
    # Validate spec_file
    if not spec_file or not isinstance(spec_file, str):
        raise ValidationError("spec_file must be a non-empty string")

    if not spec_file.strip():
        raise ValidationError("spec_file cannot be whitespace only")

    if not spec_file.endswith('.spec'):
        raise ValidationError(f"spec_file must end with .spec, got: {spec_file}")

    # Check for dangerous special device paths
    if spec_file.startswith('/dev/') or spec_file.startswith('/proc/'):
        raise ValidationError(f"Suspicious spec_file path detected: {spec_file}")

    # Validate git_repo_dir
    if not git_repo_dir or not isinstance(git_repo_dir, str):
        raise ValidationError("git_repo_dir must be a non-empty string")

    if not git_repo_dir.strip():
        raise ValidationError("git_repo_dir cannot be whitespace only")

    # Validate changelog_msg if provided
    if changelog_msg is not None:
        if not isinstance(changelog_msg, str):
            raise ValidationError("changelog_msg must be a string if provided")

        if len(changelog_msg) > 1000:
            raise ValidationError("changelog_msg is too long (max 1000 characters)")

