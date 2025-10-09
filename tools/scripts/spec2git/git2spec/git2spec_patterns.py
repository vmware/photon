"""
Regex patterns and constants for git2spec conversion

This module centralizes all regex patterns and magic numbers used
throughout the git2spec conversion process.
"""

import re

# ============================================================================
# REGEX PATTERNS
# ============================================================================

# Spec file field patterns
NAME_PATTERN = re.compile(r'^Name:\s*(.+)$', re.MULTILINE)
VERSION_PATTERN = re.compile(r'^Version:\s*(.+)$', re.MULTILINE)
RELEASE_PATTERN = re.compile(r'^Release:\s*(.+)$', re.MULTILINE)
PATCH_PATTERN = re.compile(r'^Patch(\d+):\s*(.+)$', re.MULTILINE)
SOURCE0_PATTERN = re.compile(r'^Source0?:\s*(.+)$', re.MULTILINE)

# Line-based patterns (for line-by-line processing)
PATCH_LINE_PATTERN = re.compile(r'^(Patch\d+:)(\s*)(.*)$')
RELEASE_LINE_PATTERN = re.compile(r'^(Release:)(\s*)(\d+)(.*)$')
AUTOPATCH_PATTERN = re.compile(r'^(%autopatch\s+(?:-p\d+\s*)?(?:-m\d+\s*)?)-M(\d+)(.*)$')

# Patch content patterns
PATCH_SUBJECT_PATTERN = re.compile(r'^Subject: \[?PATCH[^\]]*\]?\s*(.+)$', re.MULTILINE)

# Macro and filename patterns
MACRO_PATTERN = re.compile(r'%\{([^}]+)\}')
SAFE_FILENAME_PATTERN = re.compile(r'[^\w\s-]')
WHITESPACE_PATTERN = re.compile(r'[-\s]+')

# Source reference pattern (for %include directives)
SOURCE_REF_PATTERN = re.compile(r'%\{SOURCE(\d+)\}', re.IGNORECASE)

# Include directive pattern
INCLUDE_PATTERN = re.compile(r'^%include\s+(.+)$', re.MULTILINE)

# Patch filename normalization pattern
NUMERIC_PREFIX_PATTERN = re.compile(r'^\d+-')

# ============================================================================
# CONSTANTS
# ============================================================================

# Git format-patch filename length limits
# Git uses a 52-character limit for the slug part of patch filenames
GIT_PATCH_FILENAME_SLUG_LENGTH = 52

# Maximum patch filename length (used when generating new patches)
# This is retrieved from config but we define a default here
DEFAULT_MAX_PATCH_FILENAME_LENGTH = 64

# Default whitespace between "Patch###:" and filename in spec files
DEFAULT_PATCH_WHITESPACE = "            "

# Diff similarity threshold for fuzzy matching
# This is retrieved from config but we define a default here
DEFAULT_DIFF_SIMILARITY_THRESHOLD = 0.85

# Number of context lines to show when logging diff differences
DEFAULT_DIFF_CONTEXT_LINES = 3

# Subprocess timeout defaults (in seconds)
DEFAULT_SUBPROCESS_TIMEOUT = 30
DEFAULT_GIT_FORMAT_PATCH_TIMEOUT = 60

# Changelog formatting
CHANGELOG_DATE_FORMAT = '%a %b %d %Y'  # e.g., "Mon Oct 17 2025"

# File encodings
DEFAULT_FILE_ENCODING = 'utf-8'
FALLBACK_FILE_ENCODING = 'latin-1'

# Temporary directory prefix for patch generation
TEMP_DIR_PREFIX = 'git2spec_'

# Default author information
DEFAULT_AUTHOR_NAME = "Spec2Git Converter"
DEFAULT_AUTHOR_EMAIL = "spec2git@photon.local"

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_numeric_from_patch_name(patch_name: str) -> int:
    """
    Extract patch number from patch name (e.g., "Patch512" -> 512)

    Args:
        patch_name: Patch name string (e.g., "Patch512", "512")

    Returns:
        Patch number as integer

    Raises:
        ValueError: If no numeric part found
    """
    # Try to extract number from "PatchXXX" format
    match = re.search(r'Patch(\d+)', patch_name)
    if match:
        return int(match.group(1))

    # Try direct conversion if it's just a number
    try:
        return int(patch_name)
    except ValueError:
        raise ValueError(f"Cannot extract patch number from: {patch_name}")


def normalize_patch_filename(filename: str) -> str:
    """
    Normalize a patch filename for comparison by removing numeric prefixes and extension.

    Args:
        filename: Patch filename

    Returns:
        Normalized filename (lowercase, no prefix, no extension, hyphens for underscores)
    """
    import os

    # Remove directory path
    filename = os.path.basename(filename)

    # Remove .patch extension
    if filename.endswith('.patch'):
        filename = filename[:-6]

    # Remove leading numeric prefixes like "0001-"
    filename = NUMERIC_PREFIX_PATTERN.sub('', filename)

    # Normalize to lowercase
    filename = filename.lower()

    # Normalize underscores to hyphens for comparison
    # (git format-patch uses hyphens, but patch files may use underscores)
    filename = filename.replace('_', '-')

    return filename


def sanitize_filename(text: str, max_length: int = DEFAULT_MAX_PATCH_FILENAME_LENGTH) -> str:
    """
    Sanitize text for use as a filename

    Args:
        text: Text to sanitize
        max_length: Maximum length of resulting filename

    Returns:
        Safe filename string
    """
    # Remove unsafe characters
    safe_text = SAFE_FILENAME_PATTERN.sub('', text)

    # Replace whitespace with hyphens
    safe_text = WHITESPACE_PATTERN.sub('-', safe_text).strip('-')

    # Truncate if too long
    if len(safe_text) > max_length:
        safe_text = safe_text[:max_length].rstrip('-')

    return safe_text


def extract_subject_from_patch(patch_content: str) -> str:
    """
    Extract subject line from patch content

    Args:
        patch_content: Full patch content

    Returns:
        Subject line (without [PATCH] prefix)
    """
    match = PATCH_SUBJECT_PATTERN.search(patch_content)
    if match:
        return match.group(1).strip()
    return ""

