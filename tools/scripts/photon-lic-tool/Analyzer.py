#!/usr/bin/env python3

"""
Analyzer module for photon-lic-tool
Provides license detection analysis and comparison functionality
"""

import os
import sys
import yaml
import shutil
import functools
from difflib import SequenceMatcher, unified_diff
from urllib.request import urlopen
from urllib.error import URLError

from Scanner import Scanner
from DockerUtil import DockerUtil
import common
from common import err_exit, pr_err, ph_scan_tool_dir


class Analyzer:
    """Analyzer for license detections in source code"""

    # ANSI color codes
    BOLD = '1'
    RED = '31'
    GREEN = '32'
    YELLOW = '33'

    def __init__(self):
        """Initialize the Analyzer with a Scanner instance"""
        self.scanner = Scanner()
        self.divider_length = common.wrap_output if common.wrap_output else 80
        if self.divider_length > 80:
            self.divider_length = 80

    @staticmethod
    def _color_print(msg, color=None, **kwargs):
        """Print with optional ANSI color, only when stdout is a TTY"""
        if color and sys.stdout.isatty():
            print(f"\033[{color}m{msg}\033[0m", **kwargs)
        else:
            print(msg, **kwargs)

    def analyze(self, yaml_path=None, license_filter=None, source_path=None,
                context_lines=5, no_diff=False):
        """
        Analyze license detections from a scan

        Args:
            yaml_path: Path to existing scan YAML (optional)
            license_filter: License expression filter to apply to the analysis
            source_path: Path to source (spec file, archive, or directory)
            context_lines: Number of context lines to show
            no_diff: Skip comparison with matched rule
        """
        source_dir = None
        cleanup_src = True
        cleanup_yaml = not bool(yaml_path)

        if not source_path:
            err_exit("Can't analyze without a source path...")
        elif not os.path.exists(source_path):
            err_exit(f"Source path {source_path} does not exist")

        docker_util = DockerUtil() if DockerUtil.detect() else None
        if docker_util:
            mnt_list, cmd = docker_util.build_analyze_docker_cmd(
                yaml_path=yaml_path,
                license_filter=license_filter,
                source_path=source_path,
                context_lines=context_lines,
                no_diff=no_diff,
            )
            docker_util.run_docker_cmd(cmd=cmd, mount_list=mnt_list)
            return

        build_spec = True if source_path.endswith('.spec') else False
        try:
            # Step 1: Build/extract source tree if needed
            if os.path.isdir(source_path):
                source_dir = source_path
                cleanup_src = False
                print(f"Using existing source directory: {source_dir}")
            else:
                print(f"Building source tree from: {source_path}")
                source_dir = self._extract_source(
                    source_path,
                    build_spec=build_spec,
                )

            source_dir = os.path.abspath(source_dir)

            # Step 2: Load or generate scan results
            if yaml_path:
                print(f"Loading previous scan results from: {yaml_path}")
                scan_data = self._load_scan_yaml(yaml_path)
            else:
                print(f"Running scan on: {source_dir}")
                yaml_path = f"{ph_scan_tool_dir}/analyze-scan-results.yaml"
                self.scanner._scan(scan_dir=source_dir, path=source_dir, yaml_out=yaml_path)
                scan_data = self._load_scan_yaml(yaml_path)

            print(f"\nAnalyzing licenses which match filter: {license_filter}")
            print(f"Source directory: {source_dir}")
            print("=" * self.divider_length)

            # Step 4: Generate analysis report
            self._generate_report(
                scan_data,
                source_dir,
                license_filter=license_filter,
                context_lines=context_lines,
                enable_diff=not no_diff
            )

        finally:
            # Step 5: Cleanup
            if cleanup_src and source_dir and os.path.exists(source_dir):
                print("\nCleaning up extracted source...")
                shutil.rmtree(source_dir)

            if cleanup_yaml and yaml_path and os.path.exists(yaml_path):
                os.remove(yaml_path)

    def _load_scan_yaml(self, yaml_path):
        """Load scan results from YAML file"""
        try:
            with open(yaml_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            err_exit(f"Failed to load scan YAML: {e}")

    def _extract_source(self, source_path, build_spec=False):
        """Extract/build source tree from spec file or archive"""

        try:
            # Use Scanner's _setup_scan_dir to handle extraction
            source_dir = self.scanner._setup_scan_dir(
                source_path,
                build_spec=build_spec,
            )

            print(f"Source tree built at: {source_dir}")
            return source_dir

        except Exception as e:
            err_exit(f"Failed to extract source: {e}")

    def _generate_report(self, scan_data, source_dir, license_filter=None,
                         context_lines=5, enable_diff=True):
        """Generate analysis report for license detections"""

        if not scan_data or 'license_detections' not in scan_data:
            print("No scan data available")
            return

        print("\n" + "=" * self.divider_length)
        print(f"LICENSE ANALYSIS REPORT: {license_filter or 'ALL'}")
        print("=" * self.divider_length)

        match_count = 0
        detections = scan_data.get('license_detections', [])

        for detection in detections:
            license_key = detection.get('license_expression', '')
            spdx_id = detection.get('license_expression_spdx', license_key)

            if not spdx_id:
                continue

            # Filter by license if specified
            if license_filter and license_filter.lower() not in spdx_id.lower():
                continue

            # Process each reference match in this detection
            matches = detection.get('reference_matches', [])

            for match in matches:
                # Extract match details
                file_path = match.get('from_file', '')
                start_line = match.get('start_line', 0)
                end_line = match.get('end_line', 0)
                score = float(match.get('score', 0))
                rule_id = match.get('rule_identifier', 'N/A')
                rule_url = match.get('rule_url', 'N/A')
                match_license = match.get('license_expression', license_key)
                match_spdx = match.get('license_expression_spdx', spdx_id)

                if not license_filter.lower() in match_spdx.lower():
                    continue

                match_count += 1

                # Print match header
                print("\n" + "-" * self.divider_length)
                print(f"Match #{match_count}")
                print(f"License: {match_license}")
                print(f"SPDX:    {match_spdx}")
                print(f"File:    {file_path}")
                print(f"Lines:   {start_line}-{end_line}")
                print(f"Score:   {score:.2f}")
                print(f"Rule ID: {rule_id}")
                print(f"Rule URL: {rule_url}")
                print("-" * self.divider_length)

                # Show file context
                # Try multiple path combinations
                full_path = None

                # This is added when we use docker, strip it out to match the actual path
                file_path = file_path.replace("scan-mnt/", "")

                # If scanning a directory, both the file path and the source dir will
                # have the same directory in the path
                if os.path.basename(source_dir) in file_path:
                    file_path = file_path.replace(f"{os.path.basename(source_dir)}/", "")

                # First, try direct join
                candidate = os.path.join(source_dir, file_path)
                if os.path.exists(candidate):
                    full_path = candidate

                # If file_path starts with BUILD/ and source_dir ends with BUILD, remove BUILD/
                # prefix from the file path
                if not full_path and file_path.startswith('BUILD/'):
                    if source_dir.endswith('/BUILD') or source_dir.endswith('/BUILD/'):
                        candidate = os.path.join(source_dir, file_path[6:])
                        if os.path.exists(candidate):
                            full_path = candidate

                # Try absolute path
                if not full_path and os.path.exists(file_path):
                    full_path = file_path

                print(f"\nActual path: {full_path or file_path}")

                if full_path and os.path.exists(full_path):
                    context = self._get_file_context(
                        full_path, start_line, end_line, context_lines
                    )
                    print("\nContext:")
                    print(context)

                    # Show diff with rule text if enabled
                    if enable_diff and rule_url and rule_url != 'N/A':
                        detected_text = self._get_license_text_from_file(
                            full_path, start_line, end_line
                        )
                        rule_text = self._fetch_rule_text(rule_id, rule_url)

                        if detected_text and rule_text:
                            self._show_diff(detected_text, rule_text, match_license)
                        elif not rule_text:
                            print(f"\n[!] Rule text not found for {rule_id} at {rule_url}")
                        elif not detected_text:
                            print(
                                    f"\n[!] Detected text not found for {file_path} at " +
                                    f"{start_line}-{end_line}"
                                  )
                    elif enable_diff:
                        print("\n[!] Rule URL not provided, skipping diff")
                else:
                    print(f"File not found: {file_path}")
                    print(f"   Tried: {source_dir}")

        print("\n" + "=" * self.divider_length)
        print(f"Total references matching '{license_filter or 'ALL'}': {match_count}")
        print("=" * self.divider_length)

    def _get_file_context(self, file_path, start_line, end_line, context_lines=5):
        """Get file context around detected lines"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()

            context_start = max(1, start_line - context_lines)
            context_end = min(len(lines), end_line + context_lines)

            result = []
            for i in range(context_start - 1, context_end):
                line_num = i + 1
                line = lines[i].rstrip()

                if start_line <= line_num <= end_line:
                    result.append(f">>>  {line_num:6d} | {line}")
                else:
                    result.append(f"     {line_num:6d} | {line}")

            return '\n'.join(result)

        except Exception as e:
            return f"Error reading file: {e}"

    def _get_license_text_from_file(self, file_path, start_line, end_line):
        """Extract detected license text from file"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()

            license_lines = lines[start_line - 1:end_line]
            return ''.join(license_lines)

        except Exception as e:
            pr_err(f"Error extracting license text: {e}")
            return None

    @functools.lru_cache(maxsize=128)
    def _fetch_rule_text(self, rule_identifier, rule_url):
        """Fetch rule text from GitHub URL (cached)"""
        try:
            # Convert GitHub tree URL to raw URL
            if 'github.com' in rule_url and '/tree/' in rule_url:
                rule_url = rule_url.replace('github.com', 'raw.githubusercontent.com')
                rule_url = rule_url.replace('/tree/', '/')

            print(f"Fetching rule text from: {rule_url}")

            with urlopen(rule_url, timeout=10) as response:
                content = response.read().decode('utf-8')

            # Strip YAML front matter if present
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    content = parts[2].strip()

            return content

        except URLError as e:
            return f"Error fetching rule: {e}"
        except Exception as e:
            return f"Error: {e}"

    def _strip_comment_markers(self, text):
        """Strip common comment markers from text"""
        lines = []
        for line in text.splitlines():
            # Remove common comment prefixes
            stripped = line.strip()
            for prefix in ['//', '/*', '*/', '* ', '*', '#', ';', '--']:
                if stripped.startswith(prefix):
                    stripped = stripped[len(prefix):].strip()
            lines.append(stripped)
        return '\n'.join(lines)

    def _normalize_text_for_comparison(self, text):
        """
        Normalize text for comparison by extracting words and creating
        a consistent representation

        Returns: list of words (not rewrapped into lines)
        """
        # Convert to lowercase
        text = text.lower()

        # Extract all alphanumeric words
        words = []
        current_word = []

        for char in text:
            if char.isalnum():
                current_word.append(char)
            else:
                if current_word:
                    words.append(''.join(current_word))
                    current_word = []

        if current_word:
            words.append(''.join(current_word))

        return words

    def _show_diff(self, detected_text, official_text, license_key):
        """Show comparison between detected and official license text"""
        if not official_text or official_text.startswith("Error"):
            return

        # Strip comment markers for better comparison
        detected_stripped = self._strip_comment_markers(detected_text)
        official_stripped = self._strip_comment_markers(official_text)

        # Count non-blank lines to determine if we should normalize
        official_line_count = len([line for line in official_stripped.splitlines() if line.strip()])
        detected_line_count = len([line for line in detected_stripped.splitlines() if line.strip()])

        # If rule text is > 3 lines, normalize both sides for better comparison
        should_normalize = official_line_count > 3 or detected_line_count > 3

        print("\n" + "=" * self.divider_length)
        print("COMPARISON WITH MATCHED RULE")
        print("=" * self.divider_length)

        if should_normalize:
            # Normalize to word lists
            detected_words = self._normalize_text_for_comparison(detected_stripped)
            official_words = self._normalize_text_for_comparison(official_stripped)

            # Use word-level SequenceMatcher
            self._print_matching_blocks(detected_words, official_words)

        else:
            # For short texts, use simple unified diff
            detected_lines = [line + "\n" for line in detected_stripped.splitlines()]
            official_lines = [line + "\n" for line in official_stripped.splitlines()]

            diff = unified_diff(
                official_lines,
                detected_lines,
                fromfile="Rule (comments stripped)",
                tofile="Detected (comments stripped)",
                lineterm=''
            )

            has_diff = False
            for line in diff:
                has_diff = True
                line = line.strip()
                if line.startswith('---') or line.startswith('+++') or line.startswith('@@'):
                    self._color_print(line, self.BOLD)
                elif line.startswith('-'):
                    self._color_print(line, self.RED)
                elif line.startswith('+'):
                    self._color_print(line, self.GREEN)
                else:
                    print(line)

            if not has_diff:
                self._color_print(
                    "[OK] Texts match exactly (after stripping comments)", self.GREEN
                )

    def _print_matching_blocks(self, detected_words, official_words):
        """
        Print word-level diff using SequenceMatcher

        Args:
            detected_words: List of words from detected text
            official_words: List of words from official/rule text
        """
        # Use SequenceMatcher on word lists
        matcher = SequenceMatcher(None, official_words, detected_words)

        # Check for exact match
        if matcher.ratio() == 1.0:
            self._color_print(
                "[OK] Texts match exactly (normalized: lowercase, words only)",
                self.GREEN,
            )
            return

        # Get matching blocks
        matching_blocks = matcher.get_matching_blocks()

        # Track positions in both sequences
        official_pos = 0
        detected_pos = 0

        print("--- Rule text (normalized: lowercase, words only)")
        print("+++ Detected in source code (normalized: lowercase, words only)")
        print()

        for block in matching_blocks:
            official_start, detected_start, size = block.a, block.b, block.size

            # Print deletions (words in official but not in detected)
            if official_start > official_pos:
                deleted_words = official_words[official_pos:official_start]
                self._print_word_block(deleted_words, '-', self.RED)

            # Print additions (words in detected but not in official)
            if detected_start > detected_pos:
                added_words = detected_words[detected_pos:detected_start]
                self._print_word_block(added_words, '+', self.GREEN)

            # Print common words (matching block)
            if size > 0:
                common_words = official_words[official_start:official_start + size]
                self._print_word_block(common_words, ' ')

            # Update positions
            official_pos = official_start + size
            detected_pos = detected_start + size

        print()
        self._color_print(
            "[!] Differences found between detected and rule text", self.YELLOW
        )

    def _print_word_block(self, words, prefix, color=None, line_width=78):
        """
        Print a block of words with optional color, wrapped to line_width

        Args:
            words: List of words to print
            prefix: Prefix character ('-', '+', or ' ')
            color: ANSI color code
            line_width: Maximum line width (default 78, accounting for prefix)
        """
        if not words:
            return

        # Build lines by wrapping words
        lines = []
        current_line = []
        current_length = 0

        for word in words:
            word_len = len(word) + 1  # +1 for space

            if current_length + word_len > line_width and current_line:
                lines.append(' '.join(current_line))
                current_line = [word]
                current_length = word_len
            else:
                current_line.append(word)
                current_length += word_len

        if current_line:
            lines.append(' '.join(current_line))

        # Print lines with prefix and color
        for line in lines:
            self._color_print(f"{prefix}{line}", color)
