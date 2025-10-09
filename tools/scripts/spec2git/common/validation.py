"""
Input validation for CLI

Provides validation functions for user inputs.
"""

from pathlib import Path
from typing import Dict, Optional

from .exceptions import ValidationError


def validate_spec2git_inputs(spec_file: str, output_dir: Optional[str],
                             macros: Optional[Dict[str, str]],
                             stop_before_patch: Optional[str],
                             start_from_patch: Optional[str]) -> None:
    """
    Validate input parameters for Spec2Git

    Args:
        spec_file: Path to spec file
        output_dir: Output directory path
        macros: Macro definitions
        stop_before_patch: Patch to stop before
        start_from_patch: Patch to start from

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

    # Validate output_dir if provided
    if output_dir is not None:
        if not isinstance(output_dir, str):
            raise ValidationError("output_dir must be a string if provided")

        if not output_dir.strip():
            raise ValidationError("output_dir cannot be whitespace only")

    # Validate macros if provided
    if macros is not None:
        if not isinstance(macros, dict):
            raise ValidationError("macros must be a dictionary if provided")

        for key, value in macros.items():
            if not isinstance(key, str) or not isinstance(value, str):
                raise ValidationError(f"All macro keys and values must be strings, got: {key}={value}")

            # Check for potentially dangerous macro names
            if key in ['__file__', '__line__', '__import__']:
                raise ValidationError(f"Macro name '{key}' is not allowed for security reasons")

    # Validate patch numbers if provided
    for param_name, param_value in [
        ('stop_before_patch', stop_before_patch),
        ('start_from_patch', start_from_patch)
    ]:
        if param_value is not None:
            if not isinstance(param_value, str):
                raise ValidationError(f"{param_name} must be a string if provided")

            # Try to extract and validate patch number
            patch_str = param_value.replace('Patch', '')
            if not patch_str.isdigit():
                raise ValidationError(
                    f"{param_name} must be in format 'PatchNNN' or 'NNN', got: {param_value}"
                )

            patch_num = int(patch_str)
            if patch_num < 0 or patch_num > 99999:
                raise ValidationError(
                    f"{param_name} number must be between 0 and 99999, got: {patch_num}"
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

