"""
Workflow context management

Bundles state with service instances for workflow execution.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional
import logging

from spec2git_lib.conversion_state import ConversionState
from common.config import Spec2GitConfig


@dataclass
class WorkflowContext:
    """
    Context for workflow execution

    Bundles conversion state with service instances. This is passed
    to workflow steps and services.
    """

    # Core state
    state: ConversionState
    logger: logging.Logger

    # Service instances (lazy-loaded)
    _spec_parser: Optional[object] = None
    _source_handler: Optional[object] = None
    _patch_handler: Optional[object] = None
    _prep_executor: Optional[object] = None
    _git_ops: Optional[object] = None

    @property
    def spec_parser(self):
        """Lazy-load spec parser"""
        if self._spec_parser is None:
            from spec2git_lib.spec_parser import SpecFileParser
            self._spec_parser = SpecFileParser(
                self.state.spec_file,
                logger=self.logger,
                target_arch=self.state.target_arch
            )
        return self._spec_parser

    @property
    def source_handler(self):
        """Lazy-load source handler"""
        if self._source_handler is None:
            from spec2git_lib.source_handler import SourceHandler
            self._source_handler = SourceHandler(
                spec_dir=self.state.spec_dir,
                config_yaml_data=self.state.config_yaml_data,
                shared_sources_data=self.state.shared_sources_data,
                logger=self.logger,
                verbose=self.state.verbose
            )
        return self._source_handler

    @property
    def patch_handler(self):
        """Lazy-load patch handler"""
        if self._patch_handler is None:
            from spec2git_lib.patch_handler import PatchHandler
            self._patch_handler = PatchHandler(
                spec_dir=self.state.spec_dir,
                patches=self.state.patches,
                logger=self.logger,
                verbose=self.state.verbose,
                state=self.state
            )
        return self._patch_handler

    @property
    def prep_executor(self):
        """Lazy-load prep executor"""
        if self._prep_executor is None and self.state.output_dir:
            from spec2git_lib.prep_executor import PrepExecutor
            self._prep_executor = PrepExecutor(
                output_dir=self.state.output_dir,
                patches=self.state.patches,
                sources=self.state.sources,
                name=self.state.name,
                version=self.state.version,
                patch_handler=self.patch_handler,
                source_handler=self.source_handler,
                logger=self.logger,
                verbose=self.state.verbose,
                stop_before_patch=self.state.stop_before_patch,
                resume=self.state.resume,
            )
        return self._prep_executor

    @property
    def git_ops(self):
        """Lazy-load git operations"""
        if self._git_ops is None and self.state.git_repo_path:
            from spec2git_lib.git_operations import GitOperations
            self._git_ops = GitOperations(
                repo_path=self.state.git_repo_path,
                logger=self.logger
            )
        return self._git_ops

    @classmethod
    def create(cls, spec_file: Path, output_dir: Optional[Path] = None,
               config: Optional[Spec2GitConfig] = None,
               verbose: bool = False,
               **kwargs) -> 'WorkflowContext':
        """
        Factory method to create workflow context

        Args:
            spec_file: Path to spec file
            output_dir: Optional output directory
            config: Optional configuration
            verbose: Enable verbose logging
            **kwargs: Additional state fields

        Returns:
            New WorkflowContext instance
        """
        # Setup logging
        logger = logging.getLogger('spec2git_lib.workflow')
        logger.setLevel(logging.DEBUG if verbose else logging.INFO)

        # Create initial state
        state = ConversionState.create(
            spec_file=spec_file,
            output_dir=output_dir,
            build_dir=output_dir,
            config=config,
            verbose=verbose,
            **kwargs
        )

        return cls(state=state, logger=logger)

    def update_state(self, **kwargs) -> 'WorkflowContext':
        """
        Create new context with updated state

        Args:
            **kwargs: State fields to update

        Returns:
            New WorkflowContext with updated state
        """
        new_state = self.state.with_updates(**kwargs)
        return WorkflowContext(
            state=new_state,
            logger=self.logger,
            # Service instances stay the same (they'll re-init if needed)
            _spec_parser=self._spec_parser,
            _source_handler=self._source_handler,
            _patch_handler=None if 'git_repo_path' in kwargs else self._patch_handler,
            _prep_executor=None if 'git_repo_path' in kwargs else self._prep_executor,
            _git_ops=None if 'git_repo_path' in kwargs else self._git_ops,
        )

