"""
Spec file updating for git2spec conversion

This module handles updating RPM spec files with new patches,
incrementing release versions, and adding changelog entries.
"""

import logging
import re
from pathlib import Path
from typing import List, Tuple, Dict, Optional

from common.exceptions import SpecParseError
from common.config import get_config
from git2spec.git2spec_utils import (
    read_file_safe,
    write_file_safe,
    format_changelog_entry,
    get_git_author_info,
    get_commit_author,
)
from git2spec.git2spec_patterns import (
    PATCH_LINE_PATTERN,
    RELEASE_LINE_PATTERN,
    DEFAULT_PATCH_WHITESPACE,
    extract_subject_from_patch,
)


class Git2SpecUpdater:
    """
    Updater for RPM spec files in git2spec context

    Handles updating spec files with new patches, incrementing
    release versions, and adding changelog entries.
    """

    def __init__(self, spec_file: Path, output_spec: Optional[Path] = None,
                 git_repo_dir: Optional[Path] = None,
                 changelog_msg: Optional[str] = None,
                 use_commit_msgs: bool = False,
                 verbose: bool = False):
        """
        Initialize spec updater

        Args:
            spec_file: Path to original spec file
            output_spec: Path to output spec file (default: overwrite original)
            git_repo_dir: Path to git repository (for author info)
            changelog_msg: Custom changelog message
            use_commit_msgs: Use commit messages for changelog
            verbose: Enable verbose logging
        """
        self.spec_file = spec_file
        self.output_spec = output_spec or spec_file
        self.git_repo_dir = git_repo_dir
        self.changelog_msg = changelog_msg
        self.use_commit_msgs = use_commit_msgs
        self.verbose = verbose

        self.logger = logging.getLogger(f'{__name__}.Git2SpecUpdater')
        if verbose:
            self.logger.setLevel(logging.DEBUG)

        # State
        self.name = ""
        self.version = ""
        self.release = ""
        self.modified_commits: List[Tuple[str, int]] = []

    def update_spec(self, spec_info: Dict, new_patches: List[Tuple[int, str, str]],
                   modified_commits: List[Tuple[str, int]]) -> None:
        """
        Update spec file with new patches

        Args:
            spec_info: Dictionary from spec parser containing name, version, etc.
            new_patches: List of (patch_num, patch_filename, patch_content) tuples
            modified_commits: List of (commit_hash, patch_num) tuples for modified patches

        Raises:
            SpecParseError: If spec file update fails
        """
        if not new_patches:
            self.logger.warning("update_spec called with no patches")
            return

        self.logger.info("Updating spec file...")

        # Store state
        self.name = spec_info.get('name', '')
        self.version = spec_info.get('version', '')
        self.release = spec_info.get('release', '')
        self.modified_commits = modified_commits

        # Read spec file
        spec_content = read_file_safe(self.spec_file)
        lines = spec_content.split('\n')

        # Update patch definitions
        if modified_commits:
            self._update_modified_patches(lines, new_patches)

        # Add new patches
        self._add_new_patches(lines, new_patches)

        # Increment release
        release_incremented = self._increment_release(lines)

        # Add changelog entry
        if release_incremented:
            self._add_changelog_entry(lines, new_patches)

        # Write updated spec file
        updated_content = '\n'.join(lines)
        write_file_safe(self.output_spec, updated_content)

        self.logger.info(f"Updated spec file written to: {self.output_spec}")

    def _update_modified_patches(self, lines: List[str],
                                new_patches: List[Tuple[int, str, str]]) -> None:
        """
        Update patch definitions for modified patches

        Args:
            lines: Spec file lines (modified in place)
            new_patches: List of new patch tuples
        """
        modified_patch_nums = {patch_num for _, patch_num in self.modified_commits}
        self.logger.info(
            f"Updating patch definitions for modified patches: "
            f"{sorted(modified_patch_nums)}"
        )

        # Build map of new patch filenames
        new_patch_map = {
            patch_num: patch_filename
            for patch_num, patch_filename, _ in new_patches
        }

        # Update existing patch lines
        for i, line in enumerate(lines):
            patch_match = PATCH_LINE_PATTERN.match(line)
            if patch_match:
                patch_prefix = patch_match.group(1)
                original_whitespace = patch_match.group(2)
                patch_num = int(re.search(r'\d+', patch_prefix).group())

                if patch_num in new_patch_map:
                    new_filename = new_patch_map[patch_num]
                    lines[i] = f"{patch_prefix}{original_whitespace}{new_filename}"
                    self.logger.debug(f"Updated: Patch{patch_num} -> {new_filename}")
                    del new_patch_map[patch_num]

    def _add_new_patches(self, lines: List[str],
                        new_patches: List[Tuple[int, str, str]]) -> None:
        """
        Add truly new patches to spec file

        Args:
            lines: Spec file lines (modified in place)
            new_patches: List of new patch tuples
        """
        modified_patch_nums = (
            {patch_num for _, patch_num in self.modified_commits}
            if self.modified_commits else set()
        )
        new_patch_list = [
            (num, name, content) for num, name, content in new_patches
            if num not in modified_patch_nums
        ]

        if not new_patch_list:
            return

        # Find insertion point - simply after the last patch
        last_patch_line = -1
        patch_whitespace = DEFAULT_PATCH_WHITESPACE

        for i, line in enumerate(lines):
            # Find patch definitions
            patch_match = re.match(r'^Patch\d+:(\s*)', line)
            if patch_match:
                last_patch_line = i
                captured_ws = patch_match.group(1)
                if captured_ws is not None:
                    patch_whitespace = captured_ws if captured_ws else DEFAULT_PATCH_WHITESPACE

        if last_patch_line == -1:
            # No patches found, insert after Source lines
            for i, line in enumerate(lines):
                if re.match(r'^Source\d*:', line):
                    last_patch_line = i

        # Determine insertion point - right after last patch
        if last_patch_line >= 0:
            insert_pos = last_patch_line + 1
            self.logger.debug(
                f"Inserting new patches after last patch at line {last_patch_line}"
            )

            # Use configured whitespace if not captured
            if not patch_whitespace:
                patch_whitespace = get_config().default_patch_whitespace

            for patch_num, patch_filename, _ in new_patch_list:
                patch_line = f"Patch{patch_num}:{patch_whitespace}{patch_filename}"
                lines.insert(insert_pos, patch_line)
                insert_pos += 1
                self.logger.debug(f"Added new: {patch_line}")

    def _increment_release(self, lines: List[str]) -> bool:
        """
        Increment the Release field in spec file

        Args:
            lines: Spec file lines (modified in place)

        Returns:
            True if release was incremented, False otherwise
        """
        for i, line in enumerate(lines):
            if line.startswith('Release:'):
                release_match = RELEASE_LINE_PATTERN.match(line)
                if release_match:
                    prefix = release_match.group(1)
                    whitespace = release_match.group(2)
                    current_num = int(release_match.group(3))
                    rest = release_match.group(4)
                    new_num = current_num + 1
                    lines[i] = f"{prefix}{whitespace}{new_num}{rest}"
                    self.release = f"{new_num}{rest}"
                    self.logger.info(f"Incremented release: {current_num} -> {new_num}")
                    return True
                break
        return False

    def _add_changelog_entry(self, lines: List[str],
                            new_patches: List[Tuple[int, str, str]]) -> None:
        """
        Add a new changelog entry to spec file

        Args:
            lines: Spec file lines (modified in place)
            new_patches: List of new patch tuples
        """
        # Find %changelog section
        changelog_start = -1
        for i, line in enumerate(lines):
            if line.strip() == '%changelog':
                changelog_start = i
                break

        if changelog_start == -1:
            self.logger.warning("Could not find %changelog section")
            return

        # Get author info
        author_name, author_email = self._get_changelog_author()

        # Build changelog description
        changelog_desc = self._build_changelog_description(new_patches)

        # Create changelog entry
        changelog_entry = format_changelog_entry(
            self.version,
            self.release,
            author_name,
            author_email,
            changelog_desc
        )

        # Insert after %changelog line
        insert_pos = changelog_start + 1
        for line in reversed(changelog_entry):
            lines.insert(insert_pos, line)

        self.logger.info("Added changelog entry")

    def _get_changelog_author(self) -> Tuple[str, str]:
        """
        Get author name and email for changelog

        Returns:
            Tuple of (author_name, author_email)
        """
        from git2spec.git2spec_patterns import DEFAULT_AUTHOR_NAME, DEFAULT_AUTHOR_EMAIL

        author_name = DEFAULT_AUTHOR_NAME
        author_email = DEFAULT_AUTHOR_EMAIL

        # First priority: Use git config
        if self.git_repo_dir:
            config_author = get_git_author_info(self.git_repo_dir)
            if config_author[0] != DEFAULT_AUTHOR_NAME:
                author_name, author_email = config_author
                self.logger.debug(f"Using author from git config: {author_name} <{author_email}>")
                return author_name, author_email

            # Second priority: Use commit author
            if self.modified_commits or hasattr(self, 'new_commits'):
                # Get latest commit
                commits = (
                    [c for c, _ in self.modified_commits] if self.modified_commits
                    else getattr(self, 'new_commits', [])
                )
                if commits:
                    latest_commit = commits[-1]
                    commit_author = get_commit_author(self.git_repo_dir, latest_commit)
                    if commit_author[0] != DEFAULT_AUTHOR_NAME:
                        author_name, author_email = commit_author
                        self.logger.debug(
                            f"Using author from commit: {author_name} <{author_email}>"
                        )

        return author_name, author_email

    def _build_changelog_description(self,
                                    new_patches: List[Tuple[int, str, str]]) -> str:
        """
        Build changelog description from patches

        Args:
            new_patches: List of patch tuples

        Returns:
            Formatted changelog description
        """
        if self.use_commit_msgs:
            # Use commit messages
            msg_lines = []
            for patch_num, patch_filename, patch_content in new_patches:
                subject = extract_subject_from_patch(patch_content)
                if subject:
                    msg_lines.append(f"- {subject}")
                else:
                    msg_lines.append(f"- {patch_filename}")
            return '\n'.join(msg_lines)
        elif self.changelog_msg:
            return f"- {self.changelog_msg}"
        else:
            # Use placeholder
            return "- <Placeholder>"

