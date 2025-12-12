"""
Conversion state management

Provides immutable state object for spec2git conversion workflow.
"""

from dataclasses import dataclass, replace, field
from pathlib import Path
from typing import Dict, Optional
import logging

from common.config import Spec2GitConfig, get_config


@dataclass(frozen=True)
class ConversionState:
    """
    Immutable state object for spec2git conversion

    This class holds all the state needed during a conversion workflow.
    It's immutable by default (frozen=True), so updates create new instances.
    """

    # Spec file information
    spec_file: Path
    spec_dir: Path

    # Package metadata
    name: str = ""
    version: str = ""
    release: str = ""

    # Parsed data from spec
    sources: Dict[int, str] = field(default_factory=dict)
    patches: Dict[int, str] = field(default_factory=dict)
    macros: Dict[str, str] = field(default_factory=dict)

    # File locations
    output_dir: Optional[Path] = None
    build_dir: Optional[Path] = None
    downloaded_sources: Dict[int, Path] = field(default_factory=dict)
    tmp_sources_dir: Optional[Path] = None

    # Configuration
    config: Spec2GitConfig = field(default_factory=get_config)

    # Options
    use_tarball: bool = False
    target_arch: Optional[str] = None
    force: bool = False
    verbose: bool = False
    use_git_apply: bool = False
    cmd_str: str = ""

    # Patch control
    stop_before_patch: Optional[str] = None
    resume: bool = False

    # Special handling
    source0_git_info: Optional[Dict[str, str]] = None
    prep_section: Optional[str] = None
    parsed_spec_content: Optional[str] = None

    # Additional data
    config_yaml_data: Dict = field(default_factory=dict)
    shared_sources_data: Dict = field(default_factory=dict)

    def with_updates(self, **kwargs) -> 'ConversionState':
        """
        Create a new ConversionState with updated fields

        This is the primary way to "modify" state - create a new instance
        with some fields changed.

        Args:
            **kwargs: Fields to update

        Returns:
            New ConversionState instance with updates

        Example:
            new_state = old_state.with_updates(
                name="linux",
                version="6.12",
            )
        """
        return replace(self, **kwargs)

    @classmethod
    def create(cls, spec_file: Path, output_dir: Optional[Path] = None,
               macros: Optional[Dict[str, str]] = None,
               config: Optional[Spec2GitConfig] = None,
               **kwargs) -> 'ConversionState':
        """
        Factory method to create initial conversion state

        Args:
            spec_file: Path to spec file
            output_dir: Optional output directory
            macros: Optional macro definitions
            config: Optional configuration
            **kwargs: Additional state fields

        Returns:
            New ConversionState instance
        """
        spec_path = Path(spec_file).resolve()
        spec_dir = spec_path.parent

        return cls(
            spec_file=spec_path,
            spec_dir=spec_dir,
            output_dir=output_dir.resolve() if output_dir else None,
            macros=macros or {},
            config=config or get_config(),
            **kwargs
        )

    def __repr__(self) -> str:
        """String representation for debugging"""
        return (
            f"ConversionState("
            f"name={self.name!r}, "
            f"version={self.version!r}, "
            f"sources={len(self.sources)}, "
            f"patches={len(self.patches)}, "
            f"output_dir={self.output_dir}"
            f")"
        )

