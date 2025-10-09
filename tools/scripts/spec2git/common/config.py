"""
Configuration management for spec2git_lib

This module provides configurable constants and settings.
"""

from dataclasses import dataclass
from typing import Optional
import os


@dataclass
class Spec2GitConfig:
    """Configuration for spec2git operations"""

    # Subprocess timeouts
    default_subprocess_timeout: int = 60  # seconds

    # File size limits
    max_patch_filename_length: int = 1024  # characters
    chunk_size: int = 8192  # bytes for file reading

    # Default values
    default_strip_level: int = 1  # for patch application
    default_patch_min: int = 0

    # Display settings
    diff_context_lines: int = 4  # lines of context in diff display

    # Security settings
    enable_path_traversal_checks: bool = True
    allow_dev_proc_paths: bool = False

    # Git settings
    default_patch_whitespace: str = ' '

    # Git2Spec settings
    diff_similarity_threshold: float = 0.70  # 70% similarity required for fuzzy patch matching

    @classmethod
    def from_environment(cls) -> 'Spec2GitConfig':
        """
        Create configuration from environment variables

        Environment variables:
            SPEC2GIT_SUBPROCESS_TIMEOUT: Default subprocess timeout
            SPEC2GIT_GIT_CLONE_TIMEOUT: Git clone timeout
            SPEC2GIT_CHUNK_SIZE: Chunk size for file operations

        Returns:
            Spec2GitConfig instance with values from environment
        """
        config = cls()

        # Read from environment if available
        if timeout := os.getenv('SPEC2GIT_SUBPROCESS_TIMEOUT'):
            try:
                config.default_subprocess_timeout = int(timeout)
            except ValueError:
                pass  # Use default

        if clone_timeout := os.getenv('SPEC2GIT_GIT_CLONE_TIMEOUT'):
            try:
                config.git_clone_timeout = int(clone_timeout)
            except ValueError:
                pass  # Use default

        if chunk_size := os.getenv('SPEC2GIT_CHUNK_SIZE'):
            try:
                config.chunk_size = int(chunk_size)
            except ValueError:
                pass  # Use default

        return config


# Global default configuration
_default_config: Optional[Spec2GitConfig] = None


def get_config() -> Spec2GitConfig:
    """
    Get the current global configuration

    Returns:
        Current Spec2GitConfig instance
    """
    global _default_config
    if _default_config is None:
        _default_config = Spec2GitConfig.from_environment()
    return _default_config


def set_config(config: Spec2GitConfig) -> None:
    """
    Set the global configuration

    Args:
        config: New Spec2GitConfig instance
    """
    global _default_config
    _default_config = config


def reset_config() -> None:
    """Reset configuration to defaults from environment"""
    global _default_config
    _default_config = Spec2GitConfig.from_environment()




