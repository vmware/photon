#!/usr/bin/env python3

# Copyright (c) 2025 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.

"""
File Comparator Library

This library provides functionality to compare files between two source trees
and calculate line-level statistics (added, removed, changed lines).
"""

import os
import difflib
import re

def is_preprocessor_directive(line):
    """
    Check if a line is a preprocessor directive.

    Args:
        line: The line content to check

    Returns:
        bool: True if the line is a preprocessor directive, False otherwise
    """
    return (line.startswith('#include') or line.startswith('#define') or
            line.startswith('#ifdef') or line.startswith('#ifndef') or
            line.startswith('#if') or line.startswith('#elif') or
            line.startswith('#else') or line.startswith('#endif') or
            line.startswith('#undef'))

def is_comment_line(line, file_extension):
    """
    Check if a line is a comment based on file extension.

    Args:
        line: The line content to check (stripped of leading/trailing whitespace)
        file_extension: File extension (e.g., '.c', '.py', '.S')

    Returns:
        bool: True if the line is a comment, False otherwise
    """
    line = line.strip()

    # Empty lines are not considered comments
    if not line:
        return False

    # C/C++/Java style comments (.c, .h, .cpp, .S, .java)
    if file_extension in ['.c', '.h', '.cpp', '.cc', '.cxx', '.hpp', '.S', '.s', '.java']:
        # Single-line comment
        if line.startswith('//'):
            return True
        # Multi-line comment (/* ... */)
        elif line.startswith('/*') or line.startswith('*') or line.endswith('*/'):
            return True

    # Python/Shell/Makefile style comments (.py, .sh, Makefile, .mk)
    if file_extension in ['.py', '.sh', '.mk', ''] or 'Makefile' in file_extension:
        if line.startswith('#'):
            return True

    # Assembly comments
    # .s (lowercase) and .asm files use # or ; for comments
    if file_extension in ['.s', '.asm']:
        # GNU assembler uses # for comments (but not in .S files!)
        # Some assemblers use ;
        if line.startswith('#') or line.startswith(';'):
            return True

    # .S files (uppercase) are preprocessed by gcc.
    # Some lines starting with # are preprocessor directives
    if file_extension == '.S':
        if line.startswith('#') and not is_preprocessor_directive(line):
            return True

    # ASN.1 and SQL style comments (.asn1, .asn, .sql)
    if file_extension in ['.asn1', '.asn', '.sql']:
        if line.startswith('--'):
            return True

    return False


def strip_inline_comments(line, file_extension):
    """
    Remove inline comments from a line while preserving code.

    Args:
        line: The line content
        file_extension: File extension to determine comment style

    Returns:
        str: Line with inline comments removed
    """
    # C/C++/Java style inline comments
    if file_extension in ['.c', '.h', '.cpp', '.cc', '.cxx', '.hpp', '.S', '.s', '.java']:
        # Remove // comments
        if '//' in line:
            line = line.split('//', 1)[0]
        # Note: We don't handle /* */ inline comments as they're complex to parse correctly

    # Python/Shell style inline comments
    if file_extension in ['.py', '.sh', '.mk', ''] or 'Makefile' in file_extension:
        # Remove # comments (but be careful with strings)
        # Simple approach: remove everything after #
        # (This is imperfect but good enough for most cases)
        if '#' in line:
            line = line.split('#', 1)[0]

    # Assembly inline comments
    # For .s (lowercase) and .asm files, # is a comment
    if file_extension in ['.s', '.asm']:
        if '#' in line:
            line = line.split('#', 1)[0]
        if ';' in line:
            line = line.split(';', 1)[0]

    # .S files (uppercase) are preprocessed by gcc.
    # Some lines starting with # are preprocessor directives
    if file_extension == '.S':
        if line.startswith('#') and not is_preprocessor_directive(line):
            line = line.split('#', 1)[0]

    return line.rstrip()

def normalize_lines(lines, file_extension):
    """Normalize lines by removing comments and empty lines."""
    normalized = []
    for line in lines:
        stripped = line.strip()
        if stripped and not is_comment_line(line, file_extension):
            stripped = strip_inline_comments(stripped, file_extension).strip()
            if stripped:
                normalized.append(stripped + '\n')
    return normalized

def compare_file(source_tree_1, source_tree_2, file_path, ignore_comments=False):
    """
    Compare a file between two source trees and calculate line statistics.

    Args:
        source_tree_1: Path to the first source tree
        source_tree_2: Path to the second source tree
        file_path: Relative path to the file within the source trees
        ignore_comments: If True, exclude comment-only lines from statistics

    Returns:
        dict: Dictionary with keys:
            - 'lines_before': Number of lines in tree 1 (0 if file doesn't exist)
            - 'lines_removed': Number of lines removed
            - 'lines_added': Number of lines added
            - 'lines_after': Number of lines in tree 2 (0 if file doesn't exist)

    """
    result = {
        'lines_before': 0,
        'lines_removed': 0,
        'lines_added': 0,
        'lines_after': 0
    }

    file_1_path = os.path.join(source_tree_1, file_path)
    file_2_path = os.path.join(source_tree_2, file_path)

    # Get file extension for comment detection
    _, file_extension = os.path.splitext(file_path)

    # Check if files exist
    exists_in_1 = os.path.exists(file_1_path)
    exists_in_2 = os.path.exists(file_2_path)

    # Read file contents if they exist
    lines_1 = []
    lines_2 = []

    if exists_in_1:
        try:
            with open(file_1_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines_1 = f.readlines()
            result['lines_before'] = len(lines_1)
        except Exception:
            # If we can't read the file, throw an error
            raise Exception(f"Error reading file {file_1_path}")

    if exists_in_2:
        try:
            with open(file_2_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines_2 = f.readlines()
            result['lines_after'] = len(lines_2)
        except Exception:
            # If we can't read the file, throw an error
            raise Exception(f"Error reading file {file_2_path}")

    # If file exists in both trees, calculate diff
    if exists_in_1 and exists_in_2:
        if ignore_comments:
            lines_1 = normalize_lines(lines_1, file_extension)
            lines_2 = normalize_lines(lines_2, file_extension)

        diff = list(difflib.unified_diff(lines_1, lines_2, lineterm=''))

        for line in diff:
            if line.startswith('-') and not line.startswith('---'):
                result['lines_removed'] += 1
            elif line.startswith('+') and not line.startswith('+++'):
                result['lines_added'] += 1

    # If file only exists in tree 1, all lines are "removed"
    elif exists_in_1 and not exists_in_2:
        result['lines_removed'] = result['lines_before']

    # If file only exists in tree 2, all lines are "added"
    elif not exists_in_1 and exists_in_2:
        result['lines_added'] = result['lines_after']

    return result


def compare_files_batch(source_tree_1, source_tree_2, file_list, ignore_comments=False):
    """
    Compare multiple files between two source trees.

    Args:
        source_tree_1: Path to the first source tree
        source_tree_2: Path to the second source tree
        file_list: List of file paths to compare
        ignore_comments: If True, exclude comment-only lines from statistics

    Returns:
        dict: Dictionary mapping file paths to comparison results
    """
    results = {}

    for file_path in file_list:
        results[file_path] = compare_file(source_tree_1, source_tree_2, file_path, ignore_comments)

    return results


def generate_diff(source_tree_1, source_tree_2, file_path, ignore_comments=False):
    """
    Generate a unified diff for a file between two source trees.

    Args:
        source_tree_1: Path to the first source tree
        source_tree_2: Path to the second source tree
        file_path: Relative path to the file within the source trees
        ignore_comments: If True, generate diff from normalized files (comments/whitespace stripped)

    Returns:
        str: Unified diff output, or empty string if files are identical or don't exist
    """
    file_1_path = os.path.join(source_tree_1, file_path)
    file_2_path = os.path.join(source_tree_2, file_path)

    # Get file extension for comment detection
    _, file_extension = os.path.splitext(file_path)

    # Check if files exist
    exists_in_1 = os.path.exists(file_1_path)
    exists_in_2 = os.path.exists(file_2_path)

    if not (exists_in_1 and exists_in_2):
        return ""

    # Read file contents
    try:
        with open(file_1_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines_1 = f.readlines()
    except Exception:
        return ""

    try:
        with open(file_2_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines_2 = f.readlines()
    except Exception:
        return ""

    # If ignore_comments is enabled, normalize the files before diffing
    if ignore_comments:
        lines_1 = normalize_lines(lines_1, file_extension)
        lines_2 = normalize_lines(lines_2, file_extension)

    # Generate unified diff
    diff_lines = list(difflib.unified_diff(
        lines_1,
        lines_2,
        fromfile=f'a/{file_path}',
        tofile=f'b/{file_path}'
    ))

    # Remove the trailing newline from the last line if present
    if diff_lines and diff_lines[-1].endswith('\n'):
        diff_lines[-1] = diff_lines[-1].rstrip('\n')

    return ''.join(diff_lines)

