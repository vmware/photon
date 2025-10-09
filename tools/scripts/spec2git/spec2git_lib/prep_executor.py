"""
Prep section execution

Handles execution of RPM %prep section commands including source extraction and patch application.
"""

import subprocess
import tempfile
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import logging

from common.exceptions import PrepExecutionError, PatchApplicationError, SpecParseError
from common.config import get_config

DEFAULT_STRIP_LEVEL = 1


class PrepExecutor:
    """Handles execution of %prep section commands"""

    def __init__(self, output_dir: Path,
                 patches: Dict[int, str], sources: Dict[int, str],
                 name: str, version: str,
                 patch_handler, source_handler,
                 logger: Optional[logging.Logger] = None, verbose: bool = False,
                 stop_before_patch: Optional[str] = None,
                 start_from_patch: Optional[str] = None):
        """
        Initialize prep executor

        Args:
            output_dir: BUILD directory path
            patches: Dictionary of patch numbers to patch names
            sources: Dictionary of source numbers to source names/URLs
            name: Package name
            version: Package version
            patch_handler: PatchHandler instance
            source_handler: SourceHandler instance
            logger: Optional logger instance
            verbose: Enable verbose output
            stop_before_patch: Stop before applying this patch (e.g., "Patch512")
            start_from_patch: Start from this patch (e.g., "Patch56")
        """
        self.output_dir = output_dir
        self.patches = patches
        self.sources = sources
        self.name = name
        self.version = version
        self.patch_handler = patch_handler
        self.source_handler = source_handler
        self.logger = logger or logging.getLogger(__name__)
        self.verbose = verbose
        self.stop_before_patch = stop_before_patch
        self.start_from_patch = start_from_patch

    def execute_prep_section(self, prep_section: str, source0_git_info: Optional[Dict] = None,
                            rpmspec_build_dir: Optional[str] = None,
                            rpmspec_sources_dir: Optional[str] = None,
                            rpmspec_temp_dir: Optional[str] = None) -> int:
        """
        Execute %prep section line by line, applying patches inline.

        Simple approach:
        - If line has patch filename → apply patch as git commit
        - Otherwise → execute command and track state

        Args:
            prep_section: The prep section content
            source0_git_info: Optional git info for Source0 (for git clone replacement)
            rpmspec_build_dir: BUILD directory used by rpmspec
            rpmspec_sources_dir: SOURCES directory used by rpmspec (with symlinked files)
            rpmspec_temp_dir: Temp directory created for rpmspec

        Returns:
            Number of patches applied

        Raises:
            PrepExecutionError: If prep execution fails
            PatchApplicationError: If patch application fails
        """
        if not prep_section:
            self.logger.debug("No %prep section found")
            return 0

        self.logger.info("Executing %prep section")

        # Create temporary file for shell state persistence
        state_file = Path(tempfile.mktemp(suffix='.sh', prefix='spec2git_state_'))
        total_patches_applied = 0
        current_command_block = []
        source0_extracted = False

        try:
            # Walk through prep section line by line, buffering lines to detect patch commands
            lines = prep_section.split('\n')
            i = 0

            while i < len(lines):
                line = lines[i]
                stripped = line.strip()

                # Skip empty lines and comments
                if not stripped or stripped.startswith('#'):
                    i += 1
                    continue

                # Check if we should replace Source0 extraction with git clone
                if source0_git_info and 0 in self.sources:
                    source0_name = source0_git_info.get('filename', '')
                    # Only check if current line or recent block mentions the source
                    if source0_name and (source0_name in line or (current_command_block and source0_name in '\n'.join(current_command_block[-5:]))):
                        # Check the full command block
                        block_text = '\n'.join(current_command_block) if current_command_block else ''
                        if source0_name in block_text or source0_name in line:
                            self.logger.info(f"Replacing Source0 extraction with git clone")

                            # Create git clone command
                            repo_url = source0_git_info['repo_url']
                            commit_id = source0_git_info['commit_id']
                            clone_dir_name = f"{self.name}-{self.version}"

                            git_clone_commands = [
                                f"cd '{self.output_dir}'",
                                f"rm -rf '{clone_dir_name}'",
                                f"git clone '{repo_url}' '{clone_dir_name}'",
                                f"cd '{clone_dir_name}'",
                                f"git checkout '{commit_id}'",
                                f"cd ../"
                            ]

                            self._execute_shell_block(git_clone_commands, state_file)

                            # Clear the command block since we replaced it
                            current_command_block = []

                            # Mark that we've replaced Source0 - don't detect it again
                            source0_git_info = None

                            i += 1
                            continue

                # Check if this is a patch command
                patch_info = self.patch_handler.detect_patch_command(line, lines, i, current_command_block)

                if patch_info:
                    patch_num, patch_name, lines_consumed = patch_info

                    # Check if we should skip this patch due to start_from_patch
                    if self.start_from_patch:
                        # Extract patch number from start_from_patch (e.g., "Patch56" -> 56)
                        start_num = int(self.start_from_patch.replace('Patch', ''))
                        if patch_num < start_num:
                            self.logger.info(f"Skipping {patch_name} (Patch{patch_num}) - before start_from_patch (Patch{start_num})")
                            i += lines_consumed
                            continue

                    # Check if we should stop before this patch
                    if self.stop_before_patch:
                        # Extract patch number from stop_before_patch (e.g., "Patch512" -> 512)
                        stop_num = int(self.stop_before_patch.replace('Patch', ''))
                        if patch_num >= stop_num:
                            self.logger.info(f"Stopping before {patch_name} (Patch{patch_num}) as requested")
                            # Execute any pending commands before stopping
                            if current_command_block:
                                self._execute_shell_block(current_command_block, state_file)
                            return total_patches_applied

                    # Execute any pending commands first
                    if current_command_block:
                        self._execute_shell_block(current_command_block, state_file)
                        current_command_block = []

                    # Always get the current working directory from state before applying patch
                    # This ensures we apply patches in the correct directory after cd/pushd/popd
                    working_dir = self._get_current_working_directory_from_state(state_file)

                    if working_dir and working_dir.exists() and working_dir.is_dir():
                        #TODO: Only initialize git for SOURCE0... It's ok for now
                        if not (working_dir / '.git').exists():
                            self._initialize_git_repo(working_dir)
                    else:
                        raise PrepExecutionError(f"Invalid working directory before applying patch: {working_dir}")

                    # Find patch file
                    patch_path = self.patch_handler.find_patch_file(patch_name)

                    # Apply the patch (logs patch application internally)
                    try:
                        self.patch_handler.apply_patch(patch_path, DEFAULT_STRIP_LEVEL, patch_num, working_dir)
                        total_patches_applied += 1
                    except PatchApplicationError as e:
                        self.logger.error(f"Failed to apply patch {patch_name}: {e}")
                        raise

                    # Skip the lines that were part of the patch command
                    i += lines_consumed
                else:
                    # Regular command - add to current block
                    current_command_block.append(line)
                    i += 1

            # Execute any remaining commands
            if current_command_block:
                self._execute_shell_block(current_command_block, state_file)

            return total_patches_applied

        finally:
            # Clean up state file
            try:
                if state_file.exists():
                    state_file.unlink()
            except Exception as e:
                self.logger.debug(f"Could not remove state file: {e}")

    def _execute_shell_block(self, commands: List[str], state_file: Optional[Path] = None) -> None:
        """
        Execute a block of shell commands

        Args:
            commands: List of shell command strings
            state_file: Optional state file for persistent shell state

        Raises:
            PrepExecutionError: If command execution fails
        """
        if not commands:
            return

        self.logger.info(f"Executing {len(commands)} commands (first: {commands[0][:60]}...)")

        if self.verbose:
            self.logger.debug(
                f"Current working directory: \
                {self._get_current_working_directory_from_state(state_file)}"
            )
            self.logger.debug(f"Full command list:")
            for cmd in commands:
                self.logger.debug(f"  {cmd}")


        # Load the shell script template
        template_path = Path(__file__).parent / 'shell_executor_template.sh'
        with open(template_path, 'r') as f:
            script_content = f.read()

        # Replace placeholders
        state_file_str = str(state_file) if state_file else ""
        script_content = script_content.replace('__STATE_FILE_PLACEHOLDER__', state_file_str)

        # Add RPM environment variables that rpmspec expects
        rpm_env_vars = self._get_rpm_environment_variables()
        script_content = script_content.replace('__RPM_ENV_VARS_PLACEHOLDER__', rpm_env_vars)

        # Replace commands placeholder with actual commands
        commands_str = '\n'.join(commands)
        script_content = script_content.replace('__COMMANDS_PLACEHOLDER__', commands_str)

        try:
            # Execute script - don't capture output to avoid OOM with large extractions
            with tempfile.NamedTemporaryFile(mode='w', suffix='.sh', delete=False) as script:
                script.write(script_content)
                script.flush()
                script_path = Path(script.name)

            # Make script executable
            script_path.chmod(0o755)

            # Execute
            result = subprocess.run(
                ['/bin/bash', str(script_path)],
                capture_output=True,
                text=True,
            )

            if result.returncode != 0:
                raise PrepExecutionError(
                    f"Prep shell block execution failed (exit code {result.returncode}):\n"
                    f"First command: {commands[0][:100]}...\n"
                    f"STDERR:\n{result.stderr}\n"
                    f"STDOUT:\n{result.stdout}\n"
                )

        except subprocess.TimeoutExpired:
            raise PrepExecutionError(f"Command execution timed out")
        except Exception as e:
            if isinstance(e, PrepExecutionError):
                raise
            raise PrepExecutionError(f"Command execution error: {e}")
        finally:
            # Clean up script
            try:
                if script_path and script_path.exists():
                    script_path.unlink()
            except:
                pass

    def _get_rpm_environment_variables(self) -> str:
        """
        Generate RPM environment variables that rpmspec injects into the prep section.

        Returns:
            String containing export statements for RPM variables
        """
        import os
        import multiprocessing

        # Get number of CPUs
        ncpus = multiprocessing.cpu_count()

        # Build the export statements
        rpm_vars = [
            f"export RPM_BUILD_NCPUS={ncpus}",
            f"export RPM_BUILD_ROOT=",  # Empty by default
            f"export RPM_OPT_FLAGS=\"\"",  # Empty by default
            f"export RPM_ARCH=\"{os.uname().machine}\"",
            f"export RPM_OS=\"linux\"",
            f"export RPM_PACKAGE_NAME=\"{self.name}\"",
            f"export RPM_PACKAGE_VERSION=\"{self.version}\"",
        ]

        return '\n'.join(rpm_vars)

    def _get_current_working_directory_from_state(self, state_file: Path) -> Optional[Path]:
        """Extract current directory from state file"""
        if not state_file or not state_file.exists():
            return None

        try:
            with open(state_file, 'r') as f:
                content = f.read()
                # Look for cd command at end of file
                for line in content.split('\n'):
                    if line.startswith('cd '):
                        # Extract directory from cd command
                        dir_str = line[3:].strip().strip('"\'')
                        return Path(dir_str)
        except Exception as e:
            self.logger.debug(f"Could not get working directory from state: {e}")

        return None

    def _initialize_git_repo(self, git_repo_path: Path) -> None:
        """Initialize git repository in the extracted source directory"""
        if not git_repo_path:
            return

        self.logger.info("Initializing git repository...")

        # Check if we already have a git repository (from cloning a git source)
        if (git_repo_path / '.git').exists():
            self.logger.info("Git repository already exists (cloned from source)")
            self.logger.info("Preserving original git history")
            return

        # Initialize git repo
        subprocess.run(['git', 'init'], cwd=git_repo_path, check=True,
                      capture_output=True)
        self.logger.info("Git init completed")

        # Check if there are any files to commit
        files = list(git_repo_path.glob('*'))
        if not files:
            self.logger.debug("Git repository initialized but no files to commit yet")
            return

        # Add all base files
        self.logger.info("Adding files to git (this may take a while for large repositories)...")
        subprocess.run(['git', 'add', '.'], cwd=git_repo_path, check=True,
                      capture_output=True)
        self.logger.info("Git add completed")

        # Commit base source
        commit_msg = f"Initial source from {self.name}-{self.version}"
        subprocess.run([
            'git',
            '-c', 'user.name=Photon Patcher',
            '-c', 'user.email=spec2git@photon.local',
            'commit', '-m', commit_msg
        ], cwd=git_repo_path, check=True, capture_output=True)

        self.logger.info("Git repository initialized with base source")



