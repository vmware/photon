"""
Utility functions for git2spec conversion

This module contains reusable utility functions for file operations,
subprocess management, and other common tasks.
"""

import subprocess
import logging
import os
from pathlib import Path
from typing import List, Optional
from datetime import datetime

from common.exceptions import SpecParseError
from common.config import get_config
from git2spec.git2spec_patterns import (
    MACRO_PATTERN,
    CHANGELOG_DATE_FORMAT,
    DEFAULT_FILE_ENCODING,
)


logger = logging.getLogger(__name__)


def safe_run_command(cmd: List[str], cwd: Optional[Path] = None,
                    timeout: Optional[int] = None,
                    check: bool = True, capture_output: bool = True,
                    text: bool = True) -> subprocess.CompletedProcess:
    """
    Safely run a subprocess command with proper timeout and error handling
    
    Args:
        cmd: Command and arguments as list
        cwd: Working directory for the command
        timeout: Timeout in seconds (default: from config)
        check: If True, raise CalledProcessError on non-zero exit
        capture_output: If True, capture stdout and stderr
        text: If True, decode output as text
    
    Returns:
        CompletedProcess instance
    
    Raises:
        SpecParseError: If command times out or fails
    """
    if timeout is None:
        timeout = get_config().default_subprocess_timeout
    
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            timeout=timeout,
            check=check,
            capture_output=capture_output,
            text=text
        )
        return result
    except subprocess.TimeoutExpired as e:
        raise SpecParseError(
            f"Command timed out after {timeout}s: {' '.join(cmd)}\n"
            f"Working directory: {cwd}\n"
            f"Consider increasing timeout if this is a legitimate long-running operation."
        ) from e
    except subprocess.CalledProcessError as e:
        if check:
            raise SpecParseError(
                f"Command failed with exit code {e.returncode}: {' '.join(cmd)}\n"
                f"Working directory: {cwd}\n"
                f"Stdout: {e.stdout}\n"
                f"Stderr: {e.stderr}"
            ) from e
        raise
    except FileNotFoundError as e:
        raise SpecParseError(
            f"Command not found: {cmd[0]}\n"
            f"Make sure the required tool is installed and in PATH."
        ) from e


def expand_macros_simple(text: str, macros: dict) -> str:
    """
    Simple macro expansion for %{name}, %{version}, etc.
    
    Args:
        text: Text containing macros
        macros: Dictionary of macro name -> value
    
    Returns:
        Text with macros expanded
    """
    result = text
    
    # Handle direct macro references
    for macro_name, macro_value in macros.items():
        if macro_value:
            result = result.replace(f'%{{{macro_name}}}', macro_value)
            result = result.replace(f'%{{{macro_name.upper()}}}', macro_value.upper())
    
    return result


def expand_source_macros(source_value: str, name: str, version: str, 
                        release: str = "") -> str:
    """
    Expand macros in source value to get actual filename
    
    Args:
        source_value: Source value from spec file (may contain macros/URLs)
        name: Package name
        version: Package version
        release: Package release (optional)
    
    Returns:
        Expanded filename
    """
    # Extract filename from URL if present
    if source_value.startswith(('http://', 'https://', 'ftp://')):
        source_value = os.path.basename(source_value)
    
    # Expand common macros
    macros = {
        'version': version,
        'name': name,
        'release': release,
    }
    
    def replace_macro(match):
        macro_name = match.group(1)
        # Handle conditional macros
        if macro_name.startswith('?'):
            macro_name = macro_name[1:]
        return macros.get(macro_name, match.group(0))
    
    result = MACRO_PATTERN.sub(replace_macro, source_value)
    return result


def read_file_safe(file_path: Path, encoding: str = DEFAULT_FILE_ENCODING) -> str:
    """
    Safely read a file with fallback encoding
    
    Args:
        file_path: Path to file
        encoding: Primary encoding to try
    
    Returns:
        File content as string
    
    Raises:
        SpecParseError: If file cannot be read
    """
    try:
        with open(file_path, 'r', encoding=encoding) as f:
            return f.read()
    except UnicodeDecodeError:
        # Try with replacement for binary files
        logger.debug(f"Failed to decode {file_path} with {encoding}, using replace mode")
        try:
            with open(file_path, 'r', encoding=encoding, errors='replace') as f:
                return f.read()
        except (IOError, OSError) as e:
            raise SpecParseError(f"Failed to read file {file_path}: {e}")
    except (IOError, OSError) as e:
        raise SpecParseError(f"Failed to read file {file_path}: {e}")


def write_file_safe(file_path: Path, content: str, 
                   encoding: str = DEFAULT_FILE_ENCODING) -> None:
    """
    Safely write content to a file
    
    Args:
        file_path: Path to file
        content: Content to write
        encoding: Encoding to use
    
    Raises:
        SpecParseError: If file cannot be written
    """
    try:
        with open(file_path, 'w', encoding=encoding) as f:
            f.write(content)
    except (IOError, OSError) as e:
        raise SpecParseError(f"Failed to write file {file_path}: {e}")


def find_file_in_paths(filename: str, search_paths: List[Path]) -> Optional[Path]:
    """
    Find a file by searching multiple paths
    
    Args:
        filename: Filename to find
        search_paths: List of paths to search
    
    Returns:
        Path to file if found, None otherwise
    """
    for path in search_paths:
        file_path = path / filename
        if file_path.exists():
            return file_path
    
    return None


def format_changelog_entry(version: str, release: str, author_name: str,
                          author_email: str, description: str) -> List[str]:
    """
    Format a changelog entry for an RPM spec file
    
    Args:
        version: Package version
        release: Package release
        author_name: Author name
        author_email: Author email
        description: Changelog description (can be multi-line)
    
    Returns:
        List of changelog entry lines
    """
    date_str = datetime.now().strftime(CHANGELOG_DATE_FORMAT)
    
    # Remove macro syntax from release for changelog
    release_clean = MACRO_PATTERN.sub('', release).strip()
    
    entry = [
        f"* {date_str} {author_name} <{author_email}> {version}-{release_clean}",
        description
    ]
    
    return entry


def calculate_line_similarity(lines1: List[str], lines2: List[str]) -> float:
    """
    Calculate similarity between two lists of lines
    
    Args:
        lines1: First list of lines
        lines2: Second list of lines
    
    Returns:
        Similarity ratio between 0.0 and 1.0
    """
    if not lines1 and not lines2:
        return 1.0
    if not lines1 or not lines2:
        return 0.0
    
    # Use set intersection for line matching
    set1 = set(lines1)
    set2 = set(lines2)
    
    common = len(set1 & set2)
    total = max(len(set1), len(set2))
    
    return common / total if total > 0 else 0.0


def truncate_string(s: str, max_length: int, suffix: str = "...") -> str:
    """
    Truncate a string to max length with suffix
    
    Args:
        s: String to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
    
    Returns:
        Truncated string
    """
    if len(s) <= max_length:
        return s
    
    return s[:max_length - len(suffix)] + suffix


def ensure_directory_exists(directory: Path) -> None:
    """
    Ensure a directory exists, creating it if necessary
    
    Args:
        directory: Path to directory
    
    Raises:
        SpecParseError: If directory cannot be created
    """
    try:
        directory.mkdir(parents=True, exist_ok=True)
    except (OSError, IOError) as e:
        raise SpecParseError(f"Failed to create directory {directory}: {e}")


def get_git_author_info(git_repo_dir: Path) -> tuple[str, str]:
    """
    Get git author name and email from git config
    
    Args:
        git_repo_dir: Path to git repository
    
    Returns:
        Tuple of (author_name, author_email)
    """
    from git2spec.git2spec_patterns import DEFAULT_AUTHOR_NAME, DEFAULT_AUTHOR_EMAIL
    
    author_name = DEFAULT_AUTHOR_NAME
    author_email = DEFAULT_AUTHOR_EMAIL
    
    try:
        result = safe_run_command(
            ['git', 'config', 'user.name'],
            cwd=git_repo_dir,
            check=False
        )
        config_name = result.stdout.strip()
        if config_name:
            author_name = config_name
        
        result = safe_run_command(
            ['git', 'config', 'user.email'],
            cwd=git_repo_dir,
            check=False
        )
        config_email = result.stdout.strip()
        if config_email:
            author_email = config_email
    
    except SpecParseError:
        pass
    
    return author_name, author_email


def get_commit_author(git_repo_dir: Path, commit_hash: str) -> tuple[str, str]:
    """
    Get author name and email from a specific commit
    
    Args:
        git_repo_dir: Path to git repository
        commit_hash: Commit hash
    
    Returns:
        Tuple of (author_name, author_email)
    """
    from git2spec.git2spec_patterns import DEFAULT_AUTHOR_NAME, DEFAULT_AUTHOR_EMAIL
    
    try:
        result = safe_run_command(
            ['git', 'log', '-1', '--format=%an', commit_hash],
            cwd=git_repo_dir
        )
        author_name = result.stdout.strip() or DEFAULT_AUTHOR_NAME
        
        result = safe_run_command(
            ['git', 'log', '-1', '--format=%ae', commit_hash],
            cwd=git_repo_dir
        )
        author_email = result.stdout.strip() or DEFAULT_AUTHOR_EMAIL
        
        return author_name, author_email
    
    except SpecParseError:
        return DEFAULT_AUTHOR_NAME, DEFAULT_AUTHOR_EMAIL

