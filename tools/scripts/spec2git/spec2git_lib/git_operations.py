"""
Git operations helper

Encapsulates all git-related operations for better separation of concerns.
"""

import subprocess
import logging
from pathlib import Path
from typing import List, Optional, Tuple
import re

from common.exceptions import SpecParseError

# Constants
DEFAULT_GIT_TIMEOUT = 60
GIT_CLONE_TIMEOUT = 600
EMAIL_PATTERN = re.compile(r'<([^>]+)>')
PATCH_SUBJECT_PATTERN = re.compile(r'^\[PATCH[^\]]*\]\s*')


class GitOperations:
    """Helper class for git operations"""

    def __init__(self, repo_path: Path, logger: Optional[logging.Logger] = None,
                 default_timeout: int = DEFAULT_GIT_TIMEOUT):
        """
        Initialize git operations helper

        Args:
            repo_path: Path to git repository
            logger: Optional logger instance
            default_timeout: Default timeout for git operations
        """
        self.repo_path = repo_path
        self.logger = logger or logging.getLogger(__name__)
        self.default_timeout = default_timeout

    def run_command(self, cmd: List[str], timeout: Optional[int] = None,
                   check: bool = True) -> subprocess.CompletedProcess:
        """
        Run a git command safely with timeout and error handling

        Args:
            cmd: Command and arguments
            timeout: Timeout in seconds (uses default if not specified)
            check: If True, raise on non-zero exit

        Returns:
            CompletedProcess instance

        Raises:
            SpecParseError: If command fails or times out
        """
        timeout = timeout or self.default_timeout

        try:
            result = subprocess.run(
                cmd,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False
            )

            if check and result.returncode != 0:
                raise SpecParseError(
                    f"Git command failed: {' '.join(cmd)}\n"
                    f"Exit code: {result.returncode}\n"
                    f"Stdout: {result.stdout}\n"
                    f"Stderr: {result.stderr}"
                )

            return result

        except subprocess.TimeoutExpired:
            raise SpecParseError(
                f"Git command timed out after {timeout}s: {' '.join(cmd)}\n"
                f"Repository: {self.repo_path}"
            )

    def init_repository(self) -> None:
        """Initialize a new git repository"""
        self.run_command(['git', 'init'])
        self.logger.debug(f"Initialized git repository at {self.repo_path}")

    def add_all(self) -> None:
        """Stage all changes"""
        self.run_command(['git', 'add', '.'])

    def commit(self, message: str, author_name: Optional[str] = None,
              author_email: Optional[str] = None, allow_empty: bool = False) -> None:
        """
        Create a commit

        Args:
            message: Commit message
            author_name: Author name (optional)
            author_email: Author email (optional)
            allow_empty: Allow empty commits
        """
        cmd = [
            'git',
            '-c', 'user.name=Spec2Git Converter',
            '-c', 'user.email=spec2git@photon.local',
            'commit', '-m', message
        ]

        if allow_empty:
            cmd.append('--allow-empty')

        if author_name and author_email:
            cmd.extend(['--author', f'{author_name} <{author_email}>'])
        elif author_email:
            cmd.extend(['--author', f'{author_email} <{author_email}>'])
        elif author_name:
            cmd.extend(['--author', f'{author_name} <spec2git@photon.local>'])

        self.run_command(cmd)

    def get_commits_after(self, base_commit: str) -> List[str]:
        """
        Get list of commits after a base commit

        Args:
            base_commit: Base commit hash

        Returns:
            List of commit hashes in chronological order
        """
        result = self.run_command(
            ['git', 'rev-list', '--reverse', f'{base_commit}..HEAD']
        )
        commits = result.stdout.strip().split('\n') if result.stdout.strip() else []
        return commits

    def get_commit_hash(self, ref: str) -> str:
        """
        Resolve a reference to a commit hash

        Args:
            ref: Git reference (branch, tag, commit)

        Returns:
            Full commit hash
        """
        result = self.run_command(['git', 'rev-parse', ref])
        return result.stdout.strip()

    def format_patch(self, commit_hash: str) -> str:
        """
        Generate patch content for a commit

        Args:
            commit_hash: Commit to generate patch for

        Returns:
            Patch content as string
        """
        result = self.run_command([
            'git', 'format-patch', '-1', '--stdout',
            '--no-numbered', '--no-signature', commit_hash
        ])
        return result.stdout

    def get_commit_subject(self, commit_hash: str) -> str:
        """
        Get commit subject line

        Args:
            commit_hash: Commit hash

        Returns:
            Subject line
        """
        result = self.run_command(
            ['git', 'log', '-1', '--format=%s', commit_hash]
        )
        return result.stdout.strip()

    def get_commit_author(self, commit_hash: str) -> Tuple[str, str]:
        """
        Get commit author name and email

        Args:
            commit_hash: Commit hash

        Returns:
            Tuple of (author_name, author_email)
        """
        name_result = self.run_command(
            ['git', 'log', '-1', '--format=%an', commit_hash]
        )
        email_result = self.run_command(
            ['git', 'log', '-1', '--format=%ae', commit_hash]
        )
        return name_result.stdout.strip(), email_result.stdout.strip()

    def get_config(self, key: str) -> Optional[str]:
        """
        Get git config value

        Args:
            key: Config key (e.g., 'user.name')

        Returns:
            Config value or None if not set
        """
        try:
            result = self.run_command(['git', 'config', key], check=False)
            if result.returncode == 0:
                return result.stdout.strip()
        except SpecParseError:
            pass
        return None

    def search_log(self, grep_pattern: str, format_str: str = '%H') -> Optional[str]:
        """
        Search git log for a pattern

        Args:
            grep_pattern: Pattern to search for
            format_str: Output format

        Returns:
            First matching result or None
        """
        try:
            result = self.run_command([
                'git', 'log', '--all', f'--grep={grep_pattern}',
                f'--format={format_str}', '-n', '1'
            ], check=False)
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()
        except SpecParseError:
            pass
        return None

    def get_status(self) -> str:
        """
        Get git status porcelain output

        Returns:
            Status output
        """
        result = self.run_command(['git', 'status', '--porcelain'])
        return result.stdout

    def reset_hard(self) -> None:
        """Reset repository to HEAD (hard reset)"""
        self.run_command(['git', 'reset', '--hard', 'HEAD'], check=False)

    def clean(self) -> None:
        """Clean untracked files"""
        self.run_command(['git', 'clean', '-fd'], check=False)

    def clone(self, url: str, destination: Path, timeout: int = None) -> None:
        """
        Clone a repository

        Args:
            url: Repository URL
            destination: Destination path
            timeout: Clone timeout in seconds (None for no timeout)
        """
        cmd = ['git', 'clone', url, str(destination)]
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False
        )

        if result.returncode != 0:
            raise SpecParseError(
                f"Git clone failed for {url}\n"
                f"Stdout: {result.stdout}\n"
                f"Stderr: {result.stderr}"
            )

    def checkout(self, ref: str) -> None:
        """
        Checkout a specific reference

        Args:
            ref: Branch, tag, or commit to checkout
        """
        self.run_command(['git', 'checkout', ref])

    def repository_exists(self) -> bool:
        """Check if .git directory exists"""
        return (self.repo_path / '.git').exists()


def extract_patch_metadata(patch_content: str) -> Tuple[str, Optional[str], Optional[str]]:
    """
    Extract commit message and author from patch content

    Args:
        patch_content: Full patch file content

    Returns:
        Tuple of (commit_message, author_name, author_email)
    """
    lines = patch_content.split('\n')
    subject = ""
    description = []
    author_name = None
    author_email = None

    # Extract author
    for line in lines:
        if line.startswith('From:') or line.startswith('Author:'):
            author_line = line.split(':', 1)[1].strip() if ':' in line else ""
            email_match = EMAIL_PATTERN.search(author_line)
            if email_match:
                author_email = email_match.group(1)
                name_part = author_line[:email_match.start()].strip()
                if name_part:
                    author_name = name_part
            elif '@' in author_line:
                author_email = author_line
            break

    # Extract subject
    for line in lines:
        if line.startswith('Subject:'):
            subject = line[8:].strip()
            subject = PATCH_SUBJECT_PATTERN.sub('', subject)
            break

    # Extract description
    in_description = False
    for line in lines:
        if line.startswith('---') or line.startswith('diff '):
            break
        if line.startswith('Subject:'):
            in_description = True
            continue
        elif in_description:
            line_stripped = line.strip()
            if not line_stripped.startswith(('From:', 'Date:')):
                description.append(line.rstrip())

    # Build commit message
    commit_msg = subject if subject else "Imported patch"
    if description:
        # Remove leading empty lines
        while description and not description[0].strip():
            description.pop(0)
        if description:
            commit_msg += "\n\n" + "\n".join(description)

    return commit_msg, author_name, author_email



