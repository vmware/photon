"""
Spec2Git CLI entry point

Streamlined entry point that delegates to workflow.
"""

import logging
from pathlib import Path
from typing import Dict, Optional

from common.validation import validate_spec2git_inputs
from spec2git_lib.workflow_context import WorkflowContext
from spec2git_lib.spec2git_workflow import Spec2GitWorkflow
from common.config import get_config
from common.exceptions import ValidationError, SpecParseError
from spec2git_lib.source_handler import SourceHandler
from spec2git_lib.patch_handler import PatchHandler
from spec2git_lib.prep_executor import PrepExecutor


class Spec2Git:
    """
    Main entry point for spec to git conversion

    This is a thin wrapper around the workflow that provides
    a clean CLI interface.
    """

    def __init__(self, spec_file: str, output_dir: Optional[str] = None,
                 macros: Optional[Dict[str, str]] = None,
                 stop_before_patch: Optional[str] = None,
                 start_from_patch: Optional[str] = None,
                 verbose: bool = False,
                 use_tarball: bool = False,
                 force: bool = False,
                 target_arch: Optional[str] = None,
                 use_git_apply: bool = False):
        """
        Initialize Spec2Git converter

        Args:
            spec_file: Path to the .spec file
            output_dir: Output directory for git repo (default: PACKAGE-VERSION-git/)
            macros: Dictionary of macro definitions to override
            stop_before_patch: Stop before applying this patch (e.g., "Patch512" or "512")
            start_from_patch: Start from this patch (e.g., "Patch512" or "512")
            verbose: Enable verbose logging
            use_tarball: Force using tarball instead of git from config.yaml
            force: Force overwrite existing output directory
            target_arch: Target architecture (e.g., x86_64, aarch64)
            use_git_apply: Use 'git apply' instead of 'patch' command

        Raises:
            ValidationError: If inputs are invalid
        """
        # Validate inputs
        validate_spec2git_inputs(spec_file, output_dir, macros,
                                stop_before_patch, start_from_patch)

        # Setup logging
        self.logger = self._setup_logging(verbose)

        # Store parameters
        self.spec_file = spec_file
        self.output_dir = Path(output_dir) if output_dir else None
        self.macros = macros or {}
        self.stop_before_patch = stop_before_patch
        self.start_from_patch = start_from_patch
        self.verbose = verbose
        self.use_tarball = use_tarball
        self.force = force
        self.target_arch = target_arch
        self.use_git_apply = use_git_apply

        # Normalize patch parameters
        if self.stop_before_patch and not self.stop_before_patch.startswith('Patch'):
            self.stop_before_patch = f"Patch{self.stop_before_patch}"
        if self.start_from_patch and not self.start_from_patch.startswith('Patch'):
            self.start_from_patch = f"Patch{self.start_from_patch}"

    def run(self) -> bool:
        """
        Execute the spec2git conversion

        Returns:
            True if conversion succeeded, False otherwise
        """
        try:
            # Create workflow context
            context = WorkflowContext.create(
                spec_file=Path(self.spec_file),
                output_dir=self.output_dir,
                macros=self.macros,
                stop_before_patch=self.stop_before_patch,
                start_from_patch=self.start_from_patch,
                verbose=self.verbose,
                use_tarball=self.use_tarball,
                force=self.force,
                target_arch=self.target_arch,
                use_git_apply=self.use_git_apply,
            )

            # Create and execute workflow
            workflow = Spec2GitWorkflow(context)
            result = workflow.execute()

            if result.success:
                self.logger.info("✓ Conversion completed successfully!")
                self.logger.info(f"  Git repository: {result.git_repo_path}")
                self.logger.info(f"  Patches applied: {result.patches_applied}")
                self.logger.info(f"  Sources downloaded: {result.sources_downloaded}")
                return True
            else:
                self.logger.error(f"✗ Conversion failed: {result.error}")
                if result.warnings:
                    for warning in result.warnings:
                        self.logger.warning(f"  {warning}")
                return False

        except Exception as e:
            self.logger.error(f"Error during conversion: {e}")
            if self.verbose:
                import traceback
                traceback.print_exc()
            return False

    def _setup_logging(self, verbose: bool) -> logging.Logger:
        """
        Setup logging configuration

        Args:
            verbose: Enable verbose/debug logging

        Returns:
            Configured logger instance
        """
        log_level = logging.DEBUG if verbose else logging.INFO

        # Configure root logger only if not already configured
        root_logger = logging.getLogger()
        if not root_logger.handlers:
            logging.basicConfig(
                level=log_level,
                format='%(asctime)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )

        logger = logging.getLogger('spec2git_lib.cli')
        logger.setLevel(log_level)

        return logger

