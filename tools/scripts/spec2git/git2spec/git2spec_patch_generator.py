"""
Patch generation and extraction for git2spec conversion

This module handles extracting patches from git commits and
generating patch files.
"""

import logging
from pathlib import Path
from typing import List, Tuple, Dict, Optional

from common.exceptions import SpecParseError
from common.config import get_config
from git2spec.git2spec_utils import safe_run_command, ensure_directory_exists
from git2spec.git2spec_patterns import (
    sanitize_filename,
    extract_subject_from_patch,
    DEFAULT_MAX_PATCH_FILENAME_LENGTH,
)


class Git2SpecPatchGenerator:
    """
    Generator for extracting patches from git commits

    Handles patch file generation, naming, and writing to disk.
    """

    def __init__(self, git_repo_dir: Path, patches_dir: Path,
                 verbose: bool = False):
        """
        Initialize patch generator

        Args:
            git_repo_dir: Path to git repository
            patches_dir: Directory to write patch files
            verbose: Enable verbose logging
        """
        self.git_repo_dir = git_repo_dir
        self.patches_dir = patches_dir
        self.verbose = verbose

        self.logger = logging.getLogger(f'{__name__}.Git2SpecPatchGenerator')
        if verbose:
            self.logger.setLevel(logging.DEBUG)

    def extract_patches(self, analysis_result: Dict,
                       original_patches: Dict[int, str],
                       output_dir: Optional[Path] = None) -> List[Tuple[int, str, str]]:
        """
        Extract patches from commits

        Args:
            analysis_result: Result from Git2SpecAnalyzer.analyze()
            original_patches: Dict mapping patch numbers to original filenames
            output_dir: Directory to write patches (default: patches_dir)

        Returns:
            List of tuples: (patch_number, patch_filename, patch_content)

        Raises:
            SpecParseError: If patch extraction fails
        """
        new_commits = analysis_result.get('new_commits', [])
        modified_commits = analysis_result.get('modified_commits', [])

        if not new_commits:
            self.logger.info("No patches to extract")
            return []

        if output_dir is None:
            output_dir = self.patches_dir

        ensure_directory_exists(output_dir)

        patches = []

        # Build commit to patch number mapping
        commit_to_patch = self._build_commit_to_patch_map(
            new_commits,
            modified_commits,
            original_patches
        )

        # Generate patches for all commits
        for commit_hash in new_commits:
            patch_num = commit_to_patch[commit_hash]

            # Determine filename and path
            if patch_num in original_patches:
                # Modified patch - use original location
                patch_filename, patch_path = self._get_modified_patch_path(
                    patch_num,
                    original_patches[patch_num]
                )
            else:
                # New patch - generate filename
                patch_filename = self._generate_patch_filename(commit_hash)
                patch_path = output_dir / patch_filename

            # Ensure parent directory exists
            ensure_directory_exists(patch_path.parent)

            # Generate patch content
            patch_content = self._generate_patch_content(commit_hash)

            # Write patch to file
            try:
                with open(patch_path, 'w', encoding='utf-8') as f:
                    f.write(patch_content)
            except (IOError, OSError) as e:
                raise SpecParseError(f"Failed to write patch file {patch_path}: {e}")

            self.logger.info(f"Extracted Patch{patch_num}: {patch_path.name}")
            patches.append((patch_num, patch_filename, patch_content))

        return patches

    def _build_commit_to_patch_map(self, new_commits: List[str],
                                   modified_commits: List[Tuple[str, int]],
                                   original_patches: Dict[int, str]) -> Dict[str, int]:
        """
        Build mapping from commit hash to patch number

        Args:
            new_commits: List of commit hashes
            modified_commits: List of (commit_hash, patch_num) tuples
            original_patches: Dict mapping patch numbers to filenames

        Returns:
            Dictionary mapping commit hash to patch number
        """
        commit_to_patch = {}

        # For modified commits, use their original patch numbers
        for commit_hash, patch_num in modified_commits:
            commit_to_patch[commit_hash] = patch_num
            self.logger.info(f"Will regenerate Patch{patch_num} from {commit_hash[:12]}")

        # For new commits, assign new patch numbers
        if len(new_commits) > len(modified_commits):
            max_patch_num = max(original_patches.keys()) if original_patches else -1
            start_new_patch_num = max_patch_num + 1

            new_patches_start_idx = len(modified_commits)
            for i, commit_hash in enumerate(new_commits[new_patches_start_idx:]):
                patch_num = start_new_patch_num + i
                commit_to_patch[commit_hash] = patch_num
                self.logger.info(f"Will create new Patch{patch_num} from {commit_hash[:12]}")

        return commit_to_patch

    def _get_modified_patch_path(self, patch_num: int,
                                 original_filename: str) -> Tuple[str, Path]:
        """
        Get path for a modified patch, using original location if found

        Args:
            patch_num: Patch number
            original_filename: Original patch filename from spec

        Returns:
            Tuple of (filename, full_path)
        """
        # Try to find the original file location
        original_path = self._find_patch_file(original_filename)

        if original_path:
            self.logger.debug(
                f"Will overwrite original patch at: "
                f"{original_path.relative_to(self.patches_dir)}"
            )
            return original_filename, original_path
        else:
            # If we can't find the original, write to patches_dir
            self.logger.debug(
                f"Original patch not found, writing to: {original_filename}"
            )
            return original_filename, self.patches_dir / original_filename

    def _find_patch_file(self, patch_filename: str) -> Optional[Path]:
        """
        Find a patch file with flexible matching

        Args:
            patch_filename: Patch filename to find

        Returns:
            Path to patch file if found, None otherwise
        """
        import re

        # Try exact match
        exact_path = self.patches_dir / patch_filename
        if exact_path.exists():
            return exact_path

        # Try subdirectories
        for subdir in self.patches_dir.iterdir():
            if subdir.is_dir():
                subdir_path = subdir / patch_filename
                if subdir_path.exists():
                    return subdir_path

        # Try without numeric prefix
        no_prefix = re.sub(r'^\d+-', '', patch_filename)
        if no_prefix != patch_filename:
            no_prefix_path = self.patches_dir / no_prefix
            if no_prefix_path.exists():
                return no_prefix_path

            for subdir in self.patches_dir.iterdir():
                if subdir.is_dir():
                    subdir_path = subdir / no_prefix
                    if subdir_path.exists():
                        return subdir_path

        # Last resort: fuzzy search
        try:
            for patch_file in self.patches_dir.rglob('*.patch'):
                if (patch_file.name == patch_filename or
                    re.sub(r'^\d+-', '', patch_file.name) == no_prefix):
                    return patch_file
        except Exception as e:
            self.logger.debug(f"Error during fuzzy patch search: {e}")

        return None

    def _generate_patch_content(self, commit_hash: str) -> str:
        """
        Generate patch content from commit using git format-patch

        Args:
            commit_hash: Git commit hash

        Returns:
            Patch content as string

        Raises:
            SpecParseError: If patch generation fails
        """
        result = safe_run_command(
            ['git', 'format-patch', '-1', '--stdout', '--no-numbered',
             '--no-signature', commit_hash],
            cwd=self.git_repo_dir
        )
        return result.stdout

    def _generate_patch_filename(self, commit_hash: str) -> str:
        """
        Generate a safe filename from commit subject

        Args:
            commit_hash: Git commit hash

        Returns:
            Safe filename for the patch
        """
        try:
            result = safe_run_command(
                ['git', 'log', '-1', '--format=%s', commit_hash],
                cwd=self.git_repo_dir
            )
            subject = result.stdout.strip()
        except SpecParseError:
            # Fallback to commit hash if we can't get subject
            return f"{commit_hash[:12]}.patch"

        # Sanitize filename
        max_length = get_config().max_patch_filename_length
        safe_subject = sanitize_filename(subject, max_length)

        # Ensure we have a valid filename
        if not safe_subject or safe_subject.isspace():
            safe_subject = commit_hash[:12]

        return f"{safe_subject}.patch"

