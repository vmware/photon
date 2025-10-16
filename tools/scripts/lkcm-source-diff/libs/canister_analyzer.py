#!/usr/bin/env python3

# Copyright (c) 2025 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.

"""
Canister Analyzer Library

This library provides functionality to analyze Linux kernel crypto/Makefile
to extract source files that are linked into crypto/canister.o
"""

import os
import re
import sys


def parse_canister_rule_dependencies(rule_line):
    """
    Parse the canister.o build rule line to extract variable dependencies.

    Example input: "$(obj)/canister.o: $(addprefix crypto/x86-,$(aesni-intel-y)) ..."

    Returns:
        list of tuples: [(prefix, variable_name), ...]
    """
    dependencies = []

    # Find all $(addprefix ...) patterns
    addprefix_pattern = r'\$\(addprefix\s+([^,]+),\s*\$\(([^)]+)\)\)'
    for match in re.finditer(addprefix_pattern, rule_line):
        prefix = match.group(1).strip()
        var_name = match.group(2).strip()

        # Remove $(obj)/ from prefix if present
        prefix = prefix.replace('$(obj)/', '')
        prefix = prefix.replace('crypto/', '')

        dependencies.append((prefix, var_name))

    # Also look for direct variable references without addprefix
    # Pattern: $(variable_name) but not inside addprefix
    # First, remove all addprefix patterns
    temp_line = re.sub(addprefix_pattern, '', rule_line)
    direct_var_pattern = r'\$\(([a-zA-Z_][a-zA-Z0-9_-]*)\)'
    for match in re.finditer(direct_var_pattern, temp_line):
        var_name = match.group(1)
        # Skip special variables like 'obj'
        if var_name not in ['obj', 'LD', 'foreach']:
            dependencies.append(('', var_name))

    return dependencies


def parse_makefile_for_canister(makefile_path):
    """
    Parse crypto/Makefile and extract all object files that are linked into canister.o

    This function:
    1. Finds the canister.o build rule
    2. Parses its dependencies to extract variable names and prefixes
    3. Collects all variable assignments from the Makefile
    4. Resolves the variables to get the final list of object files

    Args:
        makefile_path: Path to crypto/Makefile

    Returns:
        list of tuples: [(object_file, source_variable), ...]
    """
    # Dictionary to store variable assignments
    variables = {}
    canister_rule = None

    try:
        with open(makefile_path, 'r') as f:
            lines = f.readlines()

        # First pass: handle line continuations
        processed_lines = []
        i = 0
        while i < len(lines):
            line = lines[i].rstrip('\n')
            # Check if line ends with backslash (line continuation)
            while line.endswith('\\') and i + 1 < len(lines):
                line = line[:-1].strip() + ' ' + lines[i + 1].strip()
                i += 1
            processed_lines.append(line)
            i += 1

        # Second pass: parse variables and rules
        for line in processed_lines:
            line = line.strip()

            # Skip empty lines and comments
            if not line or line.startswith('#'):
                continue

            # Look for the canister.o build rule
            if re.match(r'\$\(obj\)/canister\.o:', line) or re.match(r'canister\.o:', line):
                canister_rule = line
                continue

            # Match variable assignments like "rsa_generic-y := file.o" or "rsa_generic-y += file.o"
            # Also handle conditional assignments like "aesni-intel-$(CONFIG_64BIT) += file.o"
            var_assign_match = re.match(r'([a-zA-Z_][a-zA-Z0-9_-]*(?:-\$\([^)]+\))?)\s*([+:]?=)\s*(.+)', line)
            if var_assign_match:
                var_name = var_assign_match.group(1)
                operator = var_assign_match.group(2)
                value = var_assign_match.group(3).strip()

                # Handle conditional variable names like "aesni-intel-$(CONFIG_64BIT)"
                # Assume CONFIG_64BIT=y and other CONFIG options are 'y' if they appear
                var_name = re.sub(r'\$\(CONFIG_[^)]+\)', 'y', var_name)

                # Check if value contains $(addprefix ...) expressions
                # If so, store it as a single string for later parsing
                if 'addprefix' in value or '$(' in value:
                    # Store the entire value as one item for complex expressions
                    files = [value]
                else:
                    # Split value by whitespace in case there are multiple files
                    files = value.split()

                if '+=' in operator:
                    # Append to existing variable
                    if var_name not in variables:
                        variables[var_name] = []
                    variables[var_name].extend(files)
                else:
                    # Assignment (overwrite)
                    variables[var_name] = files

    except FileNotFoundError:
        raise FileNotFoundError(f"Makefile not found: {makefile_path}")
    except Exception as e:
        raise Exception(f"Error reading Makefile: {e}")

    if not canister_rule:
        raise Exception("Could not find canister.o build rule in Makefile")

    # Parse the canister.o rule to get dependencies
    dependencies = parse_canister_rule_dependencies(canister_rule)

    # For any dependencies that are direct variable references (no prefix),
    # check if the variable contains addprefix expressions and expand them
    expanded_dependencies = []
    for prefix, var_name in dependencies:
        if prefix == '' and var_name in variables:
            # Check if the variable value contains addprefix
            var_value = ' '.join(variables[var_name])
            if 'addprefix' in var_value:
                # Parse the variable value for addprefix expressions
                sub_deps = parse_canister_rule_dependencies(var_value)
                if sub_deps:
                    expanded_dependencies.extend(sub_deps)
                else:
                    expanded_dependencies.append((prefix, var_name))
            else:
                expanded_dependencies.append((prefix, var_name))
        else:
            expanded_dependencies.append((prefix, var_name))

    dependencies = expanded_dependencies

    # Helper function to recursively resolve variable references
    def resolve_variable(var_name, prefix='', original_var=None):
        """Recursively resolve a variable to get actual .o files"""
        if original_var is None:
            original_var = var_name

        results = []
        if var_name not in variables:
            return results

        for item in variables[var_name]:
            # Check if item is a variable reference like $(foo)
            var_ref_match = re.match(r'^\$\(([^)]+)\)$', item.strip())
            if var_ref_match:
                ref_var_name = var_ref_match.group(1)
                # Recursively resolve with the same prefix
                results.extend(resolve_variable(ref_var_name, prefix, original_var))
            # Check if item contains multiple variable references (like "$(var1) $(var2)")
            elif '$(' in item:
                # Find all variable references
                var_refs = re.findall(r'\$\(([^)]+)\)', item)
                for ref_var_name in var_refs:
                    # Recursively resolve with the same prefix
                    results.extend(resolve_variable(ref_var_name, prefix, original_var))
            # Check if it's a regular .o file
            elif item.endswith('.o'):
                results.append((prefix + item, original_var))
            # Skip non-.o files (like backslash continuations)

        return results

    # Collect all object files with their source variables
    result = []

    for prefix, var_name in dependencies:
        result.extend(resolve_variable(var_name, prefix, var_name))

    return result


def parse_pattern_rules(makefile_path):
    """
    Parse pattern rules from the Makefile to map object file patterns to source paths.

    Returns:
        List of tuples: [(obj_pattern, src_pattern, extension), ...]
        For example: [('x86-%.o', 'arch/x86/crypto/%', '.c'), ...]
    """
    rules = []

    try:
        with open(makefile_path, 'r') as f:
            lines = f.readlines()

        # Handle line continuations
        processed_lines = []
        i = 0
        while i < len(lines):
            line = lines[i].rstrip('\n')
            while line.endswith('\\') and i + 1 < len(lines):
                line = line[:-1].strip() + ' ' + lines[i + 1].strip()
                i += 1
            processed_lines.append(line)
            i += 1

        # Parse pattern rules
        for line in processed_lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            # Match pattern rules like:
            # $(obj)/x86-%.o: $(srctree)/arch/x86/crypto/%.c FORCE
            # crypto/x86-%.o: arch/x86/crypto/%.c ...
            pattern_match = re.match(r'(?:\$\(obj\)/|crypto/)?([^:]+%.o):\s*(?:\$\(srctree\)/)?([^%]+)%\.([cS])', line)
            if pattern_match:
                obj_pattern = pattern_match.group(1)
                src_dir = pattern_match.group(2).strip()
                src_ext = '.' + pattern_match.group(3)

                # Remove prefixed such as $(obj)/ or crypto/ from obj_pattern and keep only the object filename pattern
                obj_pattern = os.path.basename(obj_pattern)

                rules.append((obj_pattern, src_dir, src_ext))

    except Exception as e:
        raise Exception(f"Error parsing pattern rules: {e}")

    return rules


def find_source_file(source_tree_path, obj_file, pattern_rules):
    """
    Convert an object file name to its source file path using pattern rules.

    Args:
        source_tree_path: Root of the Linux source tree
        obj_file: Object file name (may include prefix like x86-, lib-crypto-, etc.)
        pattern_rules: List of pattern rules from parse_pattern_rules()

    Returns:
        Full path to the source file, or None if not found
    """
    # Remove .o extension
    if obj_file.endswith('.o'):
        base_name = obj_file[:-2]
    else:
        base_name = obj_file

    # Special case: if the file is already .asn1 (like rsapubkey.asn1.o -> rsapubkey.asn1)
    # then it's already the source file name in crypto/
    if base_name.endswith('.asn1'):
        source_path = os.path.join(source_tree_path, 'crypto', base_name)
        if os.path.exists(source_path):
            return os.path.join('crypto', base_name)

    # Try to match against pattern rules
    for obj_pattern, src_dir, src_ext in pattern_rules:
        # Convert pattern to regex
        # x86-%.o becomes ^x86-(.+)\.o$
        pattern_regex = obj_pattern.replace('.', r'\.').replace('%', '(.+)')
        pattern_regex = '^' + pattern_regex + '$'

        match = re.match(pattern_regex, obj_file)
        if match:
            # Extract the wildcard part
            wildcard = match.group(1)

            # Construct source path
            source_file = src_dir + wildcard + src_ext
            source_path = os.path.join(source_tree_path, source_file)

            if os.path.exists(source_path):
                return source_file

    # Fallback: try default crypto/ directory with .c, .S, or .asn1
    for ext in ['.c', '.S', '.asn1']:
        source_path = os.path.join(source_tree_path, 'crypto', base_name + ext)
        if os.path.exists(source_path):
            return os.path.join('crypto', base_name + ext)

    # If not found, return None
    return None


def get_canister_source_files(linux_source_tree_path):
    """
    Main library function to get list of source files for crypto/canister.o

    Args:
        linux_source_tree_path: Path to the Linux source tree root directory

    Returns:
        list: List of source file paths relative to the source tree root

    Raises:
        FileNotFoundError: If the source tree or Makefile doesn't exist
        Exception: If there's an error parsing the Makefile
    """
    # Validate input path
    if not os.path.exists(linux_source_tree_path):
        raise FileNotFoundError(f"Linux source tree not found: {linux_source_tree_path}")

    # Construct path to crypto/Makefile
    makefile_path = os.path.join(linux_source_tree_path, 'crypto', 'Makefile')

    if not os.path.exists(makefile_path):
        raise FileNotFoundError(f"crypto/Makefile not found: {makefile_path}")

    # Parse pattern rules from Makefile
    pattern_rules = parse_pattern_rules(makefile_path)

    # Parse the Makefile for object files
    object_files = parse_makefile_for_canister(makefile_path)

    # Convert object files to source files using pattern rules
    source_files = []
    not_found = []

    for obj_file, var_name in object_files:
        source_file = find_source_file(linux_source_tree_path, obj_file, pattern_rules)
        if source_file:
            source_files.append(source_file)
        else:
            not_found.append(obj_file)

    if not_found:
        raise Exception(f"Could not find source files for: {', '.join(not_found)}")

    return source_files


