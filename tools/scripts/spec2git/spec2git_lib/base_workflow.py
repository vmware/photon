"""
Base workflow class

Provides common functionality for all workflows.
"""

from abc import ABC, abstractmethod
from typing import Optional
import logging

from spec2git_lib.conversion_state import ConversionState
from spec2git_lib.workflow_context import WorkflowContext
from spec2git_lib.result_types import ConversionResult
from common.exceptions import SpecParseError


class BaseWorkflow(ABC):
    """
    Base class for conversion workflows

    Subclasses implement the actual conversion logic by overriding
    the execute() method and any workflow steps.
    """

    def __init__(self, context: WorkflowContext):
        """
        Initialize workflow

        Args:
            context: Workflow context containing state and services
        """
        self.context = context
        self.logger = context.logger

    @abstractmethod
    def execute(self) -> ConversionResult:
        """
        Execute the workflow

        Returns:
            ConversionResult indicating success/failure
        """
        pass

    def _update_context(self, **kwargs) -> WorkflowContext:
        """
        Update workflow context with new state

        Args:
            **kwargs: State fields to update

        Returns:
            New context with updated state
        """
        self.context = self.context.update_state(**kwargs)
        return self.context

    def _log_step(self, step_name: str, details: str = ""):
        """Log a workflow step"""
        if details:
            self.logger.info(f"Step: {step_name} - {details}")
        else:
            self.logger.info(f"Step: {step_name}")

    def _log_error(self, error: str):
        """Log an error"""
        self.logger.error(error)

    def _log_warning(self, warning: str):
        """Log a warning"""
        self.logger.warning(warning)

