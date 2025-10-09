"""
Git repository analysis for git2spec conversion

This module handles analyzing git repositories to extract commits
that will be converted to patches.
"""

import logging
import tempfile
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from difflib import SequenceMatcher

from common.exceptions import SpecParseError
from common.config import get_config
from git2spec.git2spec_utils import safe_run_command
from git2spec.git2spec_patterns import normalize_patch_filename


class Git2SpecAnalyzer:
    """
    Analyzer for git repositories in git2spec context

    Maps commits to existing patches and detects new/modified commits.
    Uses filename matching and diff content comparison to identify changes.
    """

    def __init__(self, git_repo_dir: Path, patches_dir: Path,
                 verbose: bool = False):
        """
        Initialize git analyzer

        Args:
            git_repo_dir: Path to git repository
            patches_dir: Directory containing patch files
            verbose: Enable verbose logging
        """
        self.git_repo_dir = git_repo_dir
        self.patches_dir = patches_dir
        self.verbose = verbose

        self.logger = logging.getLogger(f'{__name__}.Git2SpecAnalyzer')
        if verbose:
            self.logger.setLevel(logging.DEBUG)

        # Analysis results
        self.base_commit: Optional[str] = None
        self.current_commits: List[str] = []
        self.new_commits: List[str] = []
        self.modified_commits: List[Tuple[str, int]] = []  # (commit_hash, patch_num)

    def analyze(self, spec_info: Dict, original_patches: Dict[int, str]) -> Dict:
        """
        Analyze git repository and detect changes

        Args:
            spec_info: Dictionary from spec parser containing name, version, etc.
            original_patches: Dict mapping patch numbers to filenames

        Returns:
            Dictionary containing:
                - base_commit: Base commit hash
                - current_commits: List of all commits after base
                - new_commits: List of new/modified commit hashes
                - modified_commits: List of (commit_hash, patch_num) tuples
                - has_changes: Boolean indicating if changes detected

        Raises:
            SpecParseError: If analysis fails
        """
        self.logger.info("Analyzing git repository...")

        # Validate git repository
        self._validate_git_repo()

        # Find base commit
        self.base_commit = self._find_base_commit(
            spec_info.get('base_commit_id'),
            spec_info.get('version')
        )
        self.logger.info(f"Base commit: {self.base_commit[:12]}")

        # Get all commits after base
        self._get_commits_after_base()
        self.logger.info(
            f"Found {len(self.current_commits)} commits after base (Photon patches)"
        )

        # Detect changes (map commits to patches)
        if self.current_commits and original_patches:
            self._detect_changes(original_patches)
        else:
            # No existing patches or no commits - treat all as new
            self.new_commits = self.current_commits
            self.modified_commits = []

        has_changes = len(self.new_commits) > 0

        return {
            'base_commit': self.base_commit,
            'current_commits': self.current_commits,
            'new_commits': self.new_commits,
            'modified_commits': self.modified_commits,
            'has_changes': has_changes,
        }

    def _validate_git_repo(self) -> None:
        """
        Validate that git repository exists and is valid

        Raises:
            SpecParseError: If repository is invalid
        """
        if not self.git_repo_dir.exists():
            raise SpecParseError(
                f"Git repository directory not found: {self.git_repo_dir}"
            )

        if not (self.git_repo_dir / '.git').exists():
            raise SpecParseError(f"Not a git repository: {self.git_repo_dir}")

    def _find_base_commit(self, base_commit_id: Optional[str],
                         version: str) -> str:
        """
        Find the base commit that corresponds to the spec version

        Args:
            base_commit_id: Commit ID from config.yaml (if available)
            version: Package version

        Returns:
            Commit hash of the base

        Raises:
            SpecParseError: If base commit cannot be determined
        """
        # First priority: use commit_id from config.yaml
        if base_commit_id:
            try:
                # Verify the commit exists
                result = safe_run_command(
                    ['git', 'cat-file', '-e', base_commit_id],
                    cwd=self.git_repo_dir,
                    check=False
                )
                if result.returncode == 0:
                    result = safe_run_command(
                        ['git', 'rev-parse', base_commit_id],
                        cwd=self.git_repo_dir
                    )
                    commit = result.stdout.strip()
                    self.logger.info(
                        f"Using base commit from config.yaml: {commit[:12]}..."
                    )
                    return commit
                else:
                    self.logger.warning(
                        f"commit_id from config.yaml not found in repo: {base_commit_id}"
                    )
            except SpecParseError as e:
                self.logger.warning(f"Error checking commit_id from config.yaml: {e}")

        # Second priority: use the first commit (tarball-based repo)
        try:
            result = safe_run_command(
                ['git', 'rev-list', '--max-parents=0', 'HEAD'],
                cwd=self.git_repo_dir,
                check=False
            )
            if result.returncode == 0 and result.stdout.strip():
                first_commit = result.stdout.strip().split('\n')[0]
                self.logger.info(
                    f"Using first commit as base (tarball-based repo): {first_commit[:12]}"
                )
                return first_commit
        except SpecParseError as e:
            self.logger.warning(f"Error finding first commit: {e}")

        # Last resort: use HEAD
        self.logger.warning("Could not determine base version commit, using HEAD")
        result = safe_run_command(
            ['git', 'rev-parse', 'HEAD'],
            cwd=self.git_repo_dir
        )
        return result.stdout.strip()

    def _get_commits_after_base(self) -> None:
        """Get all commits after the base commit"""
        result = safe_run_command(
            ['git', 'rev-list', '--reverse', f'{self.base_commit}..HEAD'],
            cwd=self.git_repo_dir
        )
        self.current_commits = (
            result.stdout.strip().split('\n') if result.stdout.strip() else []
        )

    def _detect_changes(self, original_patches: Dict[int, str]) -> None:
        """
        Detect which commits are modified or new compared to original patches

        Args:
            original_patches: Dict mapping patch numbers to filenames
        """
        num_original_patches = len(original_patches)
        num_current_commits = len(self.current_commits)

        self.logger.debug(
            f"Detecting changes: {num_current_commits} commits vs "
            f"{num_original_patches} patches"
        )

        if num_current_commits == 0 or num_original_patches == 0:
            return

        self.logger.info("Building commit-to-patch mapping by comparing patch content...")

        # Build mapping from commit to patch number
        commit_to_patch_map = self._build_commit_to_patch_mapping(original_patches)

        self.logger.info(f"Mapped {len(commit_to_patch_map)} commits to patches")

        # Check which mapped commits have been modified
        for commit_hash, patch_num in commit_to_patch_map.items():
            if self._is_commit_modified(commit_hash, patch_num, original_patches):
                self.modified_commits.append((commit_hash, patch_num))
                self.logger.info(
                    f"Commit {commit_hash[:12]} (Patch{patch_num}) has been modified"
                )

        # Build list of commits to regenerate
        if self.modified_commits:
            self.logger.info(
                f"Found {len(self.modified_commits)} modified patches - "
                "will regenerate only those"
            )
            self.new_commits = [commit for commit, _ in self.modified_commits]

        # Find new commits that don't map to any existing patch
        mapped_commits = set(commit_to_patch_map.keys())
        new_commit_list = [c for c in self.current_commits if c not in mapped_commits]
        if new_commit_list:
            self.logger.info(
                f"Found {len(new_commit_list)} new commits to add as patches"
            )
            self.new_commits.extend(new_commit_list)

    def _build_commit_to_patch_mapping(self,
                                      original_patches: Dict[int, str]) -> Dict[str, int]:
        """
        Build mapping from commit hash to patch number

        Args:
            original_patches: Dict mapping patch numbers to filenames

        Returns:
            Dictionary mapping commit hash to patch number
        """
        commit_to_patch = {}

        # Generate patch filenames for each commit
        commit_filenames = self._generate_commit_filenames()

        # Match patches by filename
        for patch_num, patch_filename in original_patches.items():
            base_filename = normalize_patch_filename(patch_filename)

            # Try exact filename match
            for commit_hash, git_filename in commit_filenames.items():
                if commit_hash in commit_to_patch:
                    continue

                git_base = normalize_patch_filename(git_filename)

                if base_filename == git_base:
                    commit_to_patch[commit_hash] = patch_num
                    if self.verbose:
                        self.logger.debug(
                            f"Mapped commit {commit_hash[:12]} → Patch{patch_num} "
                            f"(filename: {patch_filename})"
                        )
                    break

        # Second pass: Try diff content comparison for unmapped patches
        unmapped_patches = [
            (num, name) for num, name in original_patches.items()
            if num not in commit_to_patch.values()
        ]
        unmapped_commits = [
            c for c in self.current_commits if c not in commit_to_patch
        ]

        if unmapped_patches and unmapped_commits:
            self._match_by_diff_content(
                unmapped_patches,
                unmapped_commits,
                commit_to_patch
            )

        return commit_to_patch

    def _generate_commit_filenames(self) -> Dict[str, str]:
        """
        Generate patch filenames for all commits

        Returns:
            Dictionary mapping commit hash to generated filename
        """
        commit_filenames = {}

        with tempfile.TemporaryDirectory(prefix='git2spec_') as tmpdir:
            tmpdir_path = Path(tmpdir)

            for commit_hash in self.current_commits:
                try:
                    result = safe_run_command(
                        ['git', 'format-patch', '-1', '--no-numbered',
                         '-o', str(tmpdir_path), commit_hash],
                        cwd=self.git_repo_dir
                    )
                    created_file = result.stdout.strip()
                    if created_file and Path(created_file).exists():
                        filename = Path(created_file).name
                        commit_filenames[commit_hash] = filename
                        Path(created_file).unlink()
                except SpecParseError as e:
                    self.logger.warning(
                        f"Failed to generate patch for commit {commit_hash[:12]}: {e}"
                    )
                    continue

        return commit_filenames

    def _match_by_diff_content(self, unmapped_patches: List[Tuple[int, str]],
                               unmapped_commits: List[str],
                               commit_to_patch: Dict[str, int]) -> None:
        """
        Match unmapped patches to commits by comparing diff content

        Args:
            unmapped_patches: List of (patch_num, patch_filename) tuples
            unmapped_commits: List of commit hashes
            commit_to_patch: Dictionary to update with mappings
        """
        self.logger.info(
            f"Attempting diff-based matching for {len(unmapped_patches)} unmapped patches..."
        )

        # Generate patches for unmapped commits
        commit_patches = {}
        for commit_hash in unmapped_commits:
            try:
                result = safe_run_command(
                    ['git', 'format-patch', '-1', '--stdout', '--no-numbered',
                     '--no-signature', commit_hash],
                    cwd=self.git_repo_dir
                )
                commit_patches[commit_hash] = self._extract_diff_content(result.stdout)
            except SpecParseError as e:
                self.logger.warning(
                    f"Failed to generate patch for commit {commit_hash[:12]}: {e}"
                )
                continue

        # Try to match by diff content
        diff_similarity_threshold = get_config().diff_similarity_threshold

        for patch_num, patch_filename in unmapped_patches:
            patch_path = self._find_patch_file(patch_filename)
            if not patch_path:
                if self.verbose:
                    self.logger.debug(f"Patch{patch_num} file not found: {patch_filename}")
                continue

            try:
                with open(patch_path, 'r', encoding='utf-8', errors='replace') as f:
                    patch_content = f.read()
                patch_diff = self._extract_diff_content(patch_content)

                # Find best matching commit
                best_match = None
                best_similarity = 0.0

                for commit_hash, commit_diff in commit_patches.items():
                    if commit_hash in commit_to_patch:
                        continue

                    # Try exact match first
                    if commit_diff == patch_diff:
                        best_match = commit_hash
                        best_similarity = 1.0
                        break

                    # Calculate fuzzy similarity
                    similarity = SequenceMatcher(None, commit_diff, patch_diff).ratio()
                    if similarity > best_similarity:
                        best_similarity = similarity
                        best_match = commit_hash

                # Map if similarity exceeds threshold
                if best_match and best_similarity >= diff_similarity_threshold:
                    commit_to_patch[best_match] = patch_num
                    if self.verbose:
                        match_type = (
                            "exact" if best_similarity == 1.0
                            else f"fuzzy ({best_similarity:.1%})"
                        )
                        self.logger.debug(
                            f"Mapped commit {best_match[:12]} → Patch{patch_num} "
                            f"({match_type} diff match)"
                        )
                else:
                    if self.verbose and best_match:
                        self.logger.debug(
                            f"No commit found for Patch{patch_num}: {patch_filename} "
                            f"(best: {best_similarity:.1%})"
                        )

            except (IOError, OSError, UnicodeDecodeError) as e:
                self.logger.warning(f"Failed to read patch {patch_filename}: {e}")
                continue

    def _extract_diff_content(self, patch_content: str) -> str:
        """
        Extract and normalize just the diff content from a patch

        Args:
            patch_content: Full patch file content

        Returns:
            Normalized diff content (hunks only, no file metadata)
        """
        lines = patch_content.split('\n')
        result_lines = []
        in_hunk = False

        for line in lines:
            # Stop at git signature marker
            if line == '-- ' or line == '--':
                break
            # Skip metadata lines
            elif line.startswith(('index ', 'new file mode', 'deleted file mode',
                                'similarity index', 'rename from', 'rename to',
                                '---', '+++')):
                continue
            # Hunk headers - normalize
            elif line.startswith('@@'):
                in_hunk = True
                parts = line.split('@@')
                if len(parts) >= 3:
                    context = parts[2].rstrip() if parts[2] else ''
                    normalized = '@@' + context
                else:
                    normalized = '@@'
                result_lines.append(normalized)
            # Actual diff content
            elif in_hunk:
                if line.startswith(('+', '-', ' ')) or line == '':
                    if line.startswith(('+', '-', ' ')):
                        prefix = line[0]
                        content = line[1:].rstrip()
                        if not content:
                            result_lines.append('')
                        else:
                            result_lines.append(prefix + content)
                    else:
                        result_lines.append('')
                elif line.startswith('diff --git'):
                    in_hunk = False
                    result_lines.append(line)
            # Start of diff sections
            elif line.startswith('diff --git'):
                result_lines.append(line)

        return '\n'.join(result_lines).rstrip('\n')

    def _find_patch_file(self, patch_filename: str) -> Optional[Path]:
        """
        Find a patch file with flexible matching

        Args:
            patch_filename: Patch filename from spec

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

    def _is_commit_modified(self, commit_hash: str, patch_num: int,
                           original_patches: Dict[int, str]) -> bool:
        """
        Check if a commit's content differs from the original patch

        Args:
            commit_hash: Git commit hash
            patch_num: Patch number in spec file
            original_patches: Dict mapping patch numbers to filenames

        Returns:
            True if the commit differs from the original patch
        """
        try:
            patch_filename = original_patches.get(patch_num)
            if not patch_filename:
                return False

            patch_path = self._find_patch_file(patch_filename)
            if not patch_path:
                self.logger.warning(f"Original patch file not found: {patch_filename}")
                return True

            # Read original patch
            with open(patch_path, 'r', encoding='utf-8', errors='replace') as f:
                original_patch = f.read()

            # Generate current patch from commit
            result = safe_run_command(
                ['git', 'format-patch', '-1', '--stdout', '--no-numbered',
                 '--no-signature', commit_hash],
                cwd=self.git_repo_dir
            )
            current_patch = result.stdout

            # Compare diff content
            original_diff = self._extract_diff_content(original_patch)
            current_diff = self._extract_diff_content(current_patch)

            return original_diff != current_diff

        except (IOError, OSError, SpecParseError, UnicodeDecodeError) as e:
            self.logger.debug(f"Error comparing patch {patch_num}: {e}")
            return True

