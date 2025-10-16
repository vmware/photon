#!/usr/bin/env python3

# Copyright (c) 2025 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.

"""
Canister Source File Analyzer


Command-line tool to analyze Linux kernel crypto/Makefile and compare
source files between two Linux source trees for crypto/canister.o
"""

import sys
import os
import argparse
from libs.canister_analyzer import get_canister_source_files
from libs.file_comparator import compare_files_batch, generate_diff


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description='Compare crypto/canister.o source files between two Linux kernel trees'
    )
    parser.add_argument('source_tree_1', help='Path to first Linux source tree')
    parser.add_argument('source_tree_2', help='Path to second Linux source tree')
    parser.add_argument('--new-files', action='store_true',
                        help='Include removed and added files in the output (default: only show files in both trees)')
    parser.add_argument('--ignore-comments', action='store_true',
                        help='Ignore comment-only changes in statistics')
    parser.add_argument('--generate-diffs', action='store_true',
                        help='Generate .diff files for common files in diffs/ directory')

    args = parser.parse_args()

    source_tree_1 = args.source_tree_1
    source_tree_2 = args.source_tree_2
    show_new_files = args.new_files
    ignore_comments = args.ignore_comments
    generate_diffs_flag = args.generate_diffs

    try:
        # Get source files from both trees
        files_1 = get_canister_source_files(source_tree_1)
        files_2 = get_canister_source_files(source_tree_2)

        # Convert to sets for comparison
        set_1 = set(files_1)
        set_2 = set(files_2)

        # Find files in both, only in tree 1, only in tree 2
        files_in_both = sorted(set_1 & set_2)
        files_only_in_1 = sorted(set_1 - set_2)
        files_only_in_2 = sorted(set_2 - set_1)

        # Determine which files to display based on --new-files flag
        if show_new_files:
            # Show all files: common, removed, and added
            all_files = files_in_both + files_only_in_1 + files_only_in_2
            sections = [
                (files_in_both, ''),
                (files_only_in_1, 'Removed'),
                (files_only_in_2, 'Added')
            ]
        else:
            # Show only files in both trees
            all_files = files_in_both
            sections = [(files_in_both, '')]

        # Compare all files between the two trees
        comparisons = compare_files_batch(source_tree_1, source_tree_2, all_files, ignore_comments)

        # Adjust table formatting based on whether Status column is shown
        if show_new_files:
            # With Status column
            table_width = 162
            print("=" * table_width)
            print(f"{'#':<5} {'File':<50} {'Status':<10} {'Before':>10} {'Removed':>10} {'Added':>10} {'After':>10}    {'% Changed':<18}")
            print("=" * table_width)
        else:
            # Without Status column
            table_width = 152
            print("=" * table_width)
            print(f"{'#':<5} {'File':<50} {'Before':>10} {'Removed':>10} {'Added':>10} {'After':>10}    {'% Changed':<18}")
            print("=" * table_width)

        counter = 1

        # Totals
        total_before = 0
        total_removed = 0
        total_added = 0
        total_after = 0

        # Print files by section and accumulate totals
        for file_list, status in sections:
            for file in file_list:
                comp = comparisons[file]

                # Adjust display values based on file status
                if status == 'Removed':
                    # For removed files: show Before, but zero out Removed/Added/After
                    display_before = comp['lines_before']
                    display_removed = comp['lines_before']
                    display_added = 0
                    display_after = 0
                    pct_str = "N/A"
                elif status == 'Added':
                    # For added files: show After, but zero out Before/Removed/Added
                    display_before = 0
                    display_removed = 0
                    display_added = comp['lines_after']
                    display_after = comp['lines_after']
                    pct_str = "N/A"
                else:
                    # For common files: show all values and calculate percentages
                    display_before = comp['lines_before']
                    display_removed = comp['lines_removed']
                    display_added = comp['lines_added']
                    display_after = comp['lines_after']

                    if comp['lines_before'] > 0:
                        # Method 1: max(Removed, Added) / Before
                        pct_max = (max(comp['lines_removed'], comp['lines_added']) / comp['lines_before']) * 100
                        # Method 2: (Removed + Added) / Before
                        pct_sum = ((comp['lines_removed'] + comp['lines_added']) / comp['lines_before']) * 100
                        pct_str = f"{pct_max:>5.1f}% ... {pct_sum:>5.1f}%"
                    else:
                        pct_str = "N/A"

                # Format row based on whether Status column is shown
                if show_new_files:
                    # With Status column
                    print(f"{counter:<5} {file:<50} {status:<10} {display_before:>10} {display_removed:>10} {display_added:>10} {display_after:>10}    {pct_str:<18}")
                else:
                    # Without Status column
                    print(f"{counter:<5} {file:<50} {display_before:>10} {display_removed:>10} {display_added:>10} {display_after:>10}    {pct_str:<18}")
                counter += 1

                # Accumulate totals
                total_before += display_before
                total_removed += display_removed
                total_added += display_added
                total_after += display_after

        # Calculate total percentages
        if total_before > 0:
            total_pct_max = (max(total_removed, total_added) / total_before) * 100
            total_pct_sum = ((total_removed + total_added) / total_before) * 100
            total_pct_str = f"{total_pct_max:>5.1f}% ... {total_pct_sum:>5.1f}%"
        else:
            total_pct_str = "N/A"

        # Print separator and total row
        print("=" * table_width)
        if show_new_files:
            # With Status column
            print(f"{'':5} {'Total':<50} {'':10} {total_before:>10} {total_removed:>10} {total_added:>10} {total_after:>10}    {total_pct_str:<18}")
        else:
            # Without Status column
            print(f"{'':5} {'Total':<50} {total_before:>10} {total_removed:>10} {total_added:>10} {total_after:>10}    {total_pct_str:<18}")
        print("=" * table_width)

        # Generate diff files if requested
        if generate_diffs_flag:
            print("\nGenerating diff files...")
            diffs_dir = "diffs"

            # Create diffs directory if it doesn't exist
            if os.path.exists(diffs_dir):
                # Clean up existing diffs directory
                import shutil
                shutil.rmtree(diffs_dir)
            os.makedirs(diffs_dir)

            # Generate diffs only for files in both trees (first section)
            diff_count = 0
            for file_path in files_in_both:
                # Generate diff
                diff_content = generate_diff(source_tree_1, source_tree_2, file_path, ignore_comments)

                # Only create file if there's actual diff content
                if diff_content:
                    # Create full path for diff file
                    diff_file_path = os.path.join(diffs_dir, file_path + ".diff")

                    # Create parent directories if needed
                    diff_dir = os.path.dirname(diff_file_path)
                    if diff_dir:
                        os.makedirs(diff_dir, exist_ok=True)

                    # Write diff to file
                    with open(diff_file_path, 'w', encoding='utf-8') as f:
                        f.write(diff_content)
                        f.write('\n')

                    diff_count += 1

            print(f"Generated {diff_count} diff file(s) in '{diffs_dir}/' directory")
            if ignore_comments:
                print("Note: Diffs generated with --ignore-comments filtering applied")

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
