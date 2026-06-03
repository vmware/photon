"""
Prep section execution

Handles execution of RPM %prep section commands including source extraction and patch application.
"""

import subprocess
import tempfile
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import logging

from common.exceptions import PrepExecutionError, PatchApplicationError, SpecParseError, PatchConflictError
from common.config import get_config

# Constants
DEFAULT_STRIP_LEVEL = 1

import json
from dataclasses import dataclass, asdict, field
import os

@dataclass
class PrepState:
    """State of prep execution for resumption"""
    next_line_index: int
    directory_stack: List[str] = field(default_factory=list)
    git_roots: List[str] = field(default_factory=list)

    @property
    def current_cwd(self) -> Optional[str]:
        """Get current working directory from top of stack"""
        if self.directory_stack:
            return self.directory_stack[0] # dirs -p puts current dir at top
        return None

    def save(self, path: Path):
        # Don't serialize the property
        data = asdict(self)
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)

    @classmethod
    def load(cls, path: Path) -> Optional['PrepState']:
        if not path.exists():
            return None
        try:
            with open(path, 'r') as f:
                data = json.load(f)
            return cls(**data)
        except Exception:
            return None



class PrepExecutor:
    """Handles execution of %prep section commands"""

    def __init__(self, output_dir: Path,
                 patches: Dict[int, str], sources: Dict[int, str],
                 name: str, version: str,
                 patch_handler, source_handler,
                 logger: Optional[logging.Logger] = None, verbose: bool = False,
                 stop_before_patch: Optional[str] = None,
                 resume: bool = False):
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
            resume: Resume from saved state file
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
        self.resume = resume
        self.persistent_state_file = output_dir / ".spec2git_state.json"
        self.git_roots = set()

    def ensure_build_dir(self, prep_section_lines: []):
        first_line = prep_section_lines[0]
        if first_line.startswith('cd'):
            build_dir = first_line.split()[1]
            if not build_dir:
                raise PrepExecutionError("cd cmd found but no directory passed!")

            build_dir = build_dir.strip("'\"")

            # As far as I can tell RPM will always inject an absolute path here...
            # So this is pointless unless RPM behavior changes, which is possible
            if not build_dir.startswith("/"):
                raise PrepExecutionError(
                        f"Found local path {build_dir} in first line of %prep section" +
                         "- need absolute path"
                    )

            if not os.path.exists(build_dir):
                os.makedirs(build_dir)

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

        total_patches_applied = 0
        current_command_block = []

        try:
            # Check for resumption state
            resuming_state = None
            if self.resume:
                resuming_state = PrepState.load(self.persistent_state_file)
                if resuming_state:
                    self.logger.info(f"Resuming from saved state (Line {resuming_state.next_line_index})")
                    if resuming_state.git_roots:
                        self.git_roots.update(resuming_state.git_roots)
                else:
                    raise PrepExecutionError("Resume requested but no state file found.")

            lines = prep_section.split('\n')
            i = 0

            # If resuming from state, restore context
            if resuming_state:
                i = resuming_state.next_line_index

                # Restore working directory
                if resuming_state.current_cwd:
                    cwd_path = Path(resuming_state.current_cwd)
                    if not cwd_path.exists():
                        raise PrepExecutionError(f"Working directory not found: {cwd_path}")
            else:
                # RPM v6 injects only a CD to the build dir into the %prep script, so
                # it will fail unless we create the build directory ourselves first
                self.ensure_build_dir(lines)

            while i < len(lines):
                line = lines[i]
                stripped = line.strip()

                # Skip empty lines and comments
                if not stripped or stripped.startswith('#'):
                    i += 1
                    continue

                # Check if we should replace Source0 extraction with git clone
                if source0_git_info and 0 in self.sources and not resuming_state:
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
                            source_dir_name = f"{self.name}-{self.version}"
                            
                            # When using git sources, we need to match RPM's expected directory structure
                            # RPM creates a build directory like "linux-6.12.92-build" and extracts sources inside it
                            # We need to do the same for git clone to maintain compatibility
                            build_subdir = f"{self.name}-{self.version}-build"
                            build_path = self.output_dir / build_subdir
                            
                            git_clone_commands = [
                                f"cd '{self.output_dir}'",
                                f"mkdir -p '{build_subdir}'",
                                f"cd '{build_subdir}'",
                                f"rm -rf '{source_dir_name}'",
                                f"git clone '{repo_url}' '{source_dir_name}'",
                                f"cd '{source_dir_name}'",
                                f"git checkout '{commit_id}'",
                                f"cd .."
                            ]

                            self._execute_shell_block(git_clone_commands)

                            # Clear the command block since we replaced it
                            current_command_block = []

                            # Mark that we've replaced Source0 - don't detect it again
                            source0_git_info = None

                            self.git_roots.add(f"{build_path}/{source_dir_name}")

                            i += 1
                            continue

                # Check if this is a patch command
                patch_info = self.patch_handler.detect_patch_command(line, lines, i, current_command_block)

                if patch_info:
                    patch_num, patch_name, lines_consumed = patch_info

                    # Check if we should stop before this patch
                    if self.stop_before_patch:
                        # Extract patch number from stop_before_patch (e.g., "Patch512" -> 512)
                        stop_num = int(self.stop_before_patch.replace('Patch', ''))
                        if patch_num >= stop_num:
                            self.logger.info(f"Stopping before {patch_name} (Patch{patch_num}) as requested")

                            # Execute pending commands before stopping
                            if current_command_block:
                                self._execute_shell_block(current_command_block)

                            # Save state before stopping
                            working_dir = self._get_current_working_directory_from_state()
                            # Ensure we have a valid stack if it's empty
                            stack = self._get_directory_stack_from_state()
                            if not stack and working_dir:
                                stack = [str(working_dir)]

                            state = PrepState(
                                next_line_index=i, # Stop at current line so we resume processing it
                                directory_stack=stack,
                                git_roots=list(self.git_roots)
                            )
                            state.save(self.persistent_state_file)
                            self.logger.info(f"State saved to {self.persistent_state_file}")

                            return total_patches_applied

                    # Execute any pending commands first
                    if current_command_block:
                        self._execute_shell_block(current_command_block)
                        current_command_block = []

                    # Always get the current working directory from state before applying patch
                    # This ensures we apply patches in the correct directory after cd/pushd/popd
                    working_dir = self._get_current_working_directory_from_state()

                    # Ensure we have a valid stack if it's empty
                    stack = self._get_directory_stack_from_state()
                    if not stack and working_dir:
                        stack = [str(working_dir)]

                    # Save state after each patch application
                    # If it fails in a shell block, we need to start from scratch, so don't bother
                    # saving the state
                    state = PrepState(
                        next_line_index=i + lines_consumed, # Resume AFTER this patch
                        directory_stack=stack,
                        git_roots=list(self.git_roots)
                    )
                    state.save(self.persistent_state_file)

                    if working_dir and working_dir.exists() and working_dir.is_dir():
                        #TODO: Only initialize git for SOURCE0... It's ok for now
                        if not (working_dir / '.git').exists():
                            self._initialize_git_repo(working_dir)
                    else:
                        raise PrepExecutionError(f"Invalid working directory before applying patch: {working_dir}")

                    # Find patch file
                    patch_path = self.patch_handler.find_patch_file(patch_name)

                    # Apply the patch (logs patch application internally)
                    self.patch_handler.apply_patch(patch_path, DEFAULT_STRIP_LEVEL, patch_num, working_dir)
                    total_patches_applied += 1

                    # Skip the lines that were part of the patch command
                    i += lines_consumed
                else:
                    # Regular command - add to current block
                    current_command_block.append(line)
                    i += 1

            # Execute any remaining commands
            if current_command_block:
                self._execute_shell_block(current_command_block)

            # Create final commit for any remaining changes in git repos
            self._create_final_commits()

            # Cleanup state file on successful completion
            if self.persistent_state_file.exists():
                self.persistent_state_file.unlink()

            return total_patches_applied, self.git_roots

        finally:
            pass

    def _execute_shell_block(self, commands: List[str]) -> None:
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
                {self._get_current_working_directory_from_state()}"
            )
            self.logger.debug(f"Full command list:")
            for cmd in commands:
                self.logger.debug(f"  {cmd}")


        # Load the shell script template
        template_path = Path(__file__).parent / 'shell_executor_template.sh'
        with open(template_path, 'r') as f:
            script_content = f.read()

        # Restore directory stack if available, otherwise just use current_cwd
        current_stack = self._get_directory_stack_from_state()
        current_cwd = self._get_current_working_directory_from_state()

        if current_stack:
            # Reconstruct stack
            # Stack from dirs -p is: top (current), next, ..., bottom
            # To restore: cd bottom, pushd next-to-bottom, ..., pushd top
            bottom = current_stack[-1]
            setup_cmds = [f"pushd '{bottom}' > /dev/null"]

            # Iterate from second-to-last up to first (stack[0])
            if len(current_stack) > 1:
                for path in reversed(current_stack[:-1]):
                    setup_cmds.append(f"pushd '{path}' > /dev/null")

            # Prepend setup commands
            commands[0:0] = setup_cmds
        elif current_cwd:
            commands.insert(0, f"cd '{current_cwd}'")

        # Capture stack at end of execution
        tmp_stack_f = "/tmp/spec2git_stack.txt"
        commands.append(f'dirs -p -l &> {tmp_stack_f}')
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
                cwd=self.output_dir,
                text=True,
            )

            if result.returncode != 0:
                # Need to start from scratch, resumption is not valid in this case
                if os.path.exists(self.persistent_state_file):
                    os.remove(self.persistent_state_file)
                    self.logger.info(f"State file removed, resume is no longer valid after shell block execution failure")
                raise PrepExecutionError(
                    f"Prep shell block execution failed (exit code {result.returncode}):\n"
                    f"First command: {commands[0][:100]}...\n"
                    f"STDERR:\n{result.stderr}\n"
                    f"STDOUT:\n{result.stdout}\n"
                )

            with open(tmp_stack_f, 'r') as f:
                    # dirs -p output one per line
                    new_stack = [l.strip() for l in f.readlines() if l.strip()]

            self._update_persistent_state(new_stack)

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
                if tmp_stack_f and Path(tmp_stack_f).exists():
                    Path(tmp_stack_f).unlink()
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

    def _get_current_working_directory_from_state(self) -> Optional[Path]:
        """Extract current directory from persistent state file"""
        state = PrepState.load(self.persistent_state_file)
        if state and state.current_cwd:
            return Path(state.current_cwd)
        return None

    def _get_directory_stack_from_state(self) -> List[str]:
        """Extract directory stack from persistent state file"""
        state = PrepState.load(self.persistent_state_file)
        if state and state.directory_stack:
            return state.directory_stack
        return []


    def _update_persistent_state(self, new_stack: List[str] = None):
        """Update CWD and stack in the persistent state"""
        state = PrepState.load(self.persistent_state_file)
        if not state:
            # If no state exists yet, create one with default values
            state = PrepState(next_line_index=0)

        if new_stack:
            state.directory_stack = new_stack

        # Ensure git_roots are preserved/updated
        if hasattr(self, 'git_roots') and self.git_roots:
             state = PrepState(
                 next_line_index=state.next_line_index,
                 directory_stack=state.directory_stack,
                 git_roots=list(self.git_roots)
             )

        state.save(self.persistent_state_file)

    def _is_child_of_git_repo(self, dirpath: Path, max_top_dir: Path) -> bool:
        paths = dirpath.parents
        for path in paths:
            if path == max_top_dir:
                return False

            if os.path.exists(os.path.join(path, '.git')):
                return True
        return False

    def _init_all_git_repos(self):
        # We only initialize the directories underneath the output_dir
        # Don't recurse any further down.
        for path in os.listdir(self.output_dir):
            path = f"{self.output_dir}/{path}"
            if not os.path.isdir(path):
                continue
            if os.path.exists(os.path.join(path, '.git')):
                continue
            if self._is_child_of_git_repo(Path(path), Path(self.output_dir)):
                continue
            self._initialize_git_repo(Path(path))

    def _create_final_commits(self):
        """Check known git repositories for uncommitted changes and commit them"""
        if not self.git_roots:
            self.logger.info("No git repositories found after prep section execution - no patches applied?")
        self._init_all_git_repos()

        self.logger.info("Checking for uncommitted changes in git repositories...")

        for repo_path_str in self.git_roots:
            repo_path = Path(repo_path_str)
            if not repo_path.exists():
                continue

            try:
                # Check for changes
                status = subprocess.run(
                    ['git', 'status', '--porcelain'],
                    cwd=repo_path,
                    capture_output=True,
                    text=True,
                    check=False
                )

                if status.stdout.strip():
                    self.logger.info(f"Creating final commit in {repo_path}")
                    # Add all changes
                    subprocess.run(
                        ['git', 'add', '-A'],
                        cwd=repo_path,
                        check=True,
                        capture_output=True
                    )

                    # Commit
                    subprocess.run([
                        'git',
                        '-c', 'user.name=Photon Patcher',
                        '-c', 'user.email=spec2git@photon.local',
                        'commit', '-m', 'Final prep section changes'
                    ], cwd=repo_path, check=True, capture_output=True)
            except Exception as e:
                self.logger.warning(f"Failed to create final commit in {repo_path}: {e}")

    def _initialize_git_repo(self, git_repo_path: Path) -> None:
        """Initialize git repository in the extracted source directory"""
        if not git_repo_path:
            return

        self.logger.info("Initializing git repository...")
        self.git_roots.add(str(git_repo_path.absolute()))

        # Check if we already have a git repository (from cloning a git source)
        if (git_repo_path / '.git').exists():
            self.logger.info("Git repository already exists")
            self.logger.info("Preserving original git history, do nothing")
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



