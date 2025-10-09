"""
Patch handling - detection, application, and metadata extraction

Handles all operations related to patches including finding, applying, and extracting metadata.
"""

import os
import re
import subprocess
from pathlib import Path
from typing import Optional, Tuple, List
import logging

from common.exceptions import PatchApplicationError, SpecParseError

# Constants
DEFAULT_STRIP_LEVEL = 1
EMAIL_PATTERN = re.compile(r'<([^>]+)>')
PATCH_SUBJECT_PATTERN = re.compile(r'^\[PATCH[^\]]*\]\s*')


class PatchHandler:
    """Handles patch operations including finding, applying, and metadata extraction"""

    def __init__(self, spec_dir: Path,
                 patches: Optional[dict] = None,
                 logger: Optional[logging.Logger] = None, verbose: bool = False):
        """
        Initialize patch handler

        Args:
            spec_dir: Directory containing the spec file
            patches: Dictionary mapping patch basenames to patch numbers {basename: patch_num}
            logger: Optional logger instance
            verbose: Enable verbose output
        """
        self.spec_dir = spec_dir
        self.patches = patches or {}
        self.logger = logger or logging.getLogger(__name__)
        self.verbose = verbose

    def find_patch_file(self, patch_name: str) -> Path:
        """Find the patch file in the spec directory or subdirectories"""
        # First try the spec directory directly
        patch_path = self.spec_dir / patch_name
        if patch_path.exists():
            return patch_path

        # Search in subdirectories, excluding hidden directories
        for root, dirs, files in os.walk(self.spec_dir):
            # Exclude hidden directories in-place
            dirs[:] = [d for d in dirs if not d.startswith('.')]

            if patch_name in files:
                return Path(root) / patch_name

        raise FileNotFoundError(f"Patch file not found: {patch_name}")

    def apply_patch(self, patch_path: Path, strip_level: int, patch_num: int,
                   working_dir: Optional[Path] = None) -> None:
        """
        Apply a single patch and create a git commit

        Args:
            patch_path: Path to the patch file
            strip_level: Number of path components to strip (patch -p option)
            patch_num: Patch number for identification
            working_dir: Git repository directory to apply patch in (required)

        Raises:
            PatchApplicationError: If patch application fails
        """
        if not working_dir:
            raise ValueError("working_dir is required for patch application")

        self.logger.info(f"Applying Patch{patch_num}: {patch_path.name}")
        patch_cwd = working_dir

        # Read patch file
        try:
            with open(patch_path, 'r', encoding='utf-8', errors='replace') as f:
                patch_content = f.read()
        except Exception as e:
            raise PatchApplicationError(f"Failed to read patch file {patch_path}: {e}")

        # Apply patch using git apply for better handling
        try:
            # Try git apply first (handles binary patches, renames, etc.)
            result = subprocess.run(
                ['git', 'apply', f'-p{strip_level}', '--verbose', '--whitespace=nowarn'],
                input=patch_content,
                capture_output=True,
                text=True,
                cwd=patch_cwd,
                timeout=60
            )

            if result.returncode != 0:
                # Fallback to patch command
                self.logger.debug(f"git apply failed, trying patch command: {result.stderr}")
                result = subprocess.run(
                    ['patch', f'-p{strip_level}', '-f', '--no-backup-if-mismatch'],
                    input=patch_content,
                    capture_output=True,
                    text=True,
                    cwd=patch_cwd,
                    timeout=60
                )

                if result.returncode != 0:
                    raise PatchApplicationError(
                        f"Failed to apply patch {patch_path.name}\n"
                        f"Stdout: {result.stdout}\n"
                        f"Stderr: {result.stderr}"
                    )

        except subprocess.TimeoutExpired:
            raise PatchApplicationError(f"Patch application timed out for {patch_path.name}")
        except Exception as e:
            raise PatchApplicationError(f"Error applying patch {patch_path.name}: {e}")

        # Stage all changes including new files
        # Patches can add new files, so we need 'git add -A' not just 'git add -u'
        self._run_git_command(['git', 'add', '-A'], cwd=patch_cwd)

        # Check if there are changes to commit
        try:
            status_result = subprocess.run(
                ['git', 'status', '--porcelain'],
                cwd=patch_cwd,
                capture_output=True,
                text=True,
                timeout=30,
                check=True
            )

            if not status_result.stdout.strip():
                self.logger.warning(f"Patch {patch_path.name} applied but no changes to commit (may be empty or already applied)")
                return

        except Exception as e:
            self.logger.warning(f"Could not check git status: {e}")

        # Extract patch metadata for commit message
        commit_message, author, date = self.extract_patch_metadata(patch_path, patch_num)

        # Prepare git commit command with metadata
        commit_cmd = [
            'git',
            '-c', 'user.name=Photon Patcher',
            '-c', 'user.email=photon-patcher@vmware.com',
            'commit',
            '-F', '-'  # Read message from stdin
        ]

        # Add author if found in patch
        if author:
            commit_cmd.extend(['--author', author])

        # Add date if found in patch
        if date:
            commit_cmd.extend(['--date', date])

        # Commit changes with full message via stdin
        try:
            result = subprocess.run(
                commit_cmd,
                input=commit_message,
                text=True,
                cwd=patch_cwd,
                stdout=subprocess.DEVNULL if not self.verbose else None,
                stderr=subprocess.DEVNULL if not self.verbose else None,
                timeout=60,
                check=False
            )
            if result.returncode != 0:
                raise SpecParseError(f"Git commit failed with exit code {result.returncode}")
        except subprocess.TimeoutExpired:
            raise SpecParseError("Git commit timed out")

    def extract_patch_metadata(self, patch_path: Path, patch_num: int) -> Tuple[str, Optional[str], Optional[str]]:
        """
        Extract metadata from patch file for git commit

        Args:
            patch_path: Path to patch file
            patch_num: Patch number for fallback subject

        Returns:
            Tuple of (full_commit_message, author, date)
        """
        subject = None
        author = None
        date = None
        body_lines = []

        try:
            with open(patch_path, 'r', encoding='utf-8', errors='replace') as f:
                in_header = True
                in_body = False

                for line in f:
                    line = line.rstrip()

                    # Check for diff start (end of commit message)
                    if line.startswith('---') or line.startswith('diff '):
                        break

                    if in_header:
                        # Extract Subject
                        if line.startswith('Subject:'):
                            subject = line[8:].strip()
                            # Remove [PATCH] prefix
                            subject = PATCH_SUBJECT_PATTERN.sub('', subject)
                        # Extract From
                        elif line.startswith('From:'):
                            from_line = line[5:].strip()
                            # Try to extract name and email
                            email_match = EMAIL_PATTERN.search(from_line)
                            if email_match:
                                email = email_match.group(1)
                                # Extract name (everything before <email>)
                                name = from_line[:from_line.index('<')].strip()
                                # Remove quotes if present
                                name = name.strip('"\'')
                                author = f"{name} <{email}>" if name else f"<{email}>"
                            else:
                                author = from_line
                        # Extract Date
                        elif line.startswith('Date:'):
                            date = line[5:].strip()
                        # Check for end of header (empty line after headers)
                        elif not line and subject:
                            in_header = False
                            in_body = True
                    elif in_body:
                        # Collect body lines (everything between headers and diff)
                        body_lines.append(line)

        except Exception as e:
            self.logger.debug(f"Could not extract metadata from {patch_path.name}: {e}")

        # Fallback subject if not found
        if not subject:
            subject = f"Apply patch {patch_num}: {patch_path.name}"

        # Build full commit message: subject + empty line + body
        commit_message = subject
        if body_lines:
            # Remove leading/trailing empty lines from body
            while body_lines and not body_lines[0]:
                body_lines.pop(0)
            while body_lines and not body_lines[-1]:
                body_lines.pop()

            if body_lines:
                commit_message += '\n\n' + '\n'.join(body_lines)

        return commit_message, author, date

    def detect_patch_command(self, line: str, all_lines: List[str], current_idx: int,
                           command_block: List[str]) -> Optional[Tuple[int, str, int]]:
        """
        Detect if current line (and possibly following lines) represent a patch command.

        Returns:
            Tuple of (patch_num, patch_name, lines_consumed) if patch detected, None otherwise
        """
        stripped = line.strip()

        # Pattern 1: rpmuncompress ... /path/to/patch.patch |
        # followed by: /bin/patch ...
        if '|' in line and line.rstrip().endswith('|'):
            # Check if this is piping to patch
            if current_idx + 1 < len(all_lines):
                next_line = all_lines[current_idx + 1].strip()
                if 'patch' in next_line and ('patch ' in next_line or '/patch' in next_line):
                    # Extract patch filename from current line
                    patch_basename = self._extract_patch_filename_from_line(line)
                    if patch_basename and patch_basename in self.patches:
                        patch_num = self.patches[patch_basename]
                        return (patch_num, patch_basename, 2)  # Consumed 2 lines (pipe + patch)

        # Pattern 2: patch ... < "/path/to/patch.patch"
        # or: patch -i "/path/to/patch.patch"
        if 'patch' in stripped and ('patch ' in stripped or '/patch' in stripped):
            # Look for redirect or -i flag
            if ' < ' in line:
                # Extract filename after '<'
                parts = line.split(' < ')
                if len(parts) >= 2:
                    patch_basename = self._extract_patch_filename_from_line(parts[1])
                    if patch_basename and patch_basename in self.patches:
                        patch_num = self.patches[patch_basename]
                        return (patch_num, patch_basename, 1)
            elif ' -i ' in line or ' --input' in line:
                # Extract filename after -i or --input
                patch_basename = self._extract_patch_filename_from_line(line)
                if patch_basename and patch_basename in self.patches:
                    patch_num = self.patches[patch_basename]
                    return (patch_num, patch_basename, 1)

        # Pattern 3: cat /path/to/patch.patch | patch
        # Need to check if previous command block ends with cat/rpmuncompress piping
        if command_block and ('patch' in stripped and ('patch ' in stripped or '/patch' in stripped)):
            # Check last line of command block for piped patch file
            if command_block[-1].rstrip().endswith('|'):
                patch_basename = self._extract_patch_filename_from_line(command_block[-1])
                if patch_basename and patch_basename in self.patches:
                    patch_num = self.patches[patch_basename]
                    # Note: The pipe command is in the command_block, this line is the patch command
                    return (patch_num, patch_basename, 1)

        return None

    def _extract_patch_filename_from_line(self, line: str) -> Optional[str]:
        """
        Extract patch basename from a command line

        Returns just the basename (e.g., 'my-patch.patch') to use as key in patches dict
        """
        import re

        # Try single quotes first
        single_quote_match = re.search(r"'([^']+\.patch)'", line)
        if single_quote_match:
            filename = single_quote_match.group(1)
            # Extract just the basename
            return Path(filename).name

        # Try double quotes
        double_quote_match = re.search(r'"([^"]+\.patch)"', line)
        if double_quote_match:
            filename = double_quote_match.group(1)
            return Path(filename).name

        # Try without quotes (look for .patch extension)
        patch_match = re.search(r'(\S+\.patch)', line)
        if patch_match:
            filename = patch_match.group(1)
            return Path(filename).name

        return None

    def _run_git_command(self, cmd: List[str], cwd: Path,
                        timeout: int = 60) -> subprocess.CompletedProcess:
        """Run a git command with error handling"""
        if not cwd:
            raise ValueError("cwd is required for git commands")

        try:
            result = subprocess.run(
                cmd,
                cwd=cwd,
                stdout=subprocess.DEVNULL if not self.verbose else None,
                stderr=subprocess.DEVNULL if not self.verbose else None,
                timeout=timeout,
                check=False
            )
            if result.returncode != 0:
                # Re-run with limited stderr capture for error reporting
                error_result = subprocess.run(
                    cmd,
                    cwd=cwd,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.PIPE,
                    text=True,
                    timeout=30,
                    check=False
                )
                raise SpecParseError(
                    f"Git command failed: {' '.join(cmd)}\n"
                    f"Exit code: {error_result.returncode}\n"
                    f"Stderr: {error_result.stderr}"
                )
            return result
        except subprocess.TimeoutExpired:
            raise SpecParseError(
                f"Git command timed out after {timeout}s: {' '.join(cmd)}\n"
                f"Working directory: {cwd}"
            )



