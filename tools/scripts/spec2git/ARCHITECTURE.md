# spec2git Architecture Documentation

## Table of Contents
1. [Overview](#overview)
2. [Design Philosophy](#design-philosophy)
3. [System Architecture](#system-architecture)
4. [Module Reference](#module-reference)
5. [Data Flow](#data-flow)
6. [Workflow Patterns](#workflow-patterns)
7. [State Management](#state-management)
8. [Extension Points](#extension-points)

---

## Overview

**spec2git** is a bidirectional converter between RPM spec files and git repositories. It consists of 22 Python modules organized into 3 main subsystems plus a unified entry point.

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      spec2git.py (Entry Point)              │
│                    Command-line argument parsing            │
└────────────┬───────────────────────────────┬────────────────┘
             │                               │
             ▼                               ▼
┌────────────────────────┐      ┌──────────────────────────────┐
│   Spec2Git (Forward)   │      │   Git2Spec (Reverse)         │
│   12 modules           │      │   7 modules                  │
│   Workflow-based       │      │   Pipeline-based             │
└────────────┬───────────┘      └──────────────┬───────────────┘
             │                                 │
             └─────────────┬───────────────────┘
                           ▼
                ┌──────────────────────┐
                │  Common (Shared)     │
                │  3 modules           │
                │  Config, Exceptions, │
                │  Validation          │
                └──────────────────────┘
```

### Module Count by Subsystem

- **Entry Point**: 1 module (`spec2git.py`)
- **Common**: 3 modules (config, exceptions, validation)
- **Git2Spec**: 7 modules (reverse conversion)
- **Spec2Git_lib**: 12 modules (forward conversion)
- **Total**: 23 modules

---

## Design Philosophy

### Core Principles

1. **Modularity Over Monoliths**
   - Each module has a single, clear responsibility
   - Average module size: 200-400 lines
   - No module exceeds 600 lines

2. **Scripts Over Packages**
   - No `__init__.py` files
   - Direct imports using `sys.path` manipulation
   - Simpler for one-off scripts and CLI tools

3. **Immutable State**
   - State updates create new instances (copy-on-write)
   - Prevents accidental state mutations
   - Easier debugging and testing

4. **Workflow Pattern**
   - Complex operations decomposed into phases
   - Each phase can succeed/fail independently
   - Clear error boundaries

5. **Lazy Initialization**
   - Services loaded only when needed
   - Reduces startup time
   - Minimizes memory footprint

6. **Absolute Imports**
   - All imports use absolute paths
   - No relative imports (`.` or `..`)
   - Clear dependency graph

### Why No Packages?

Traditional Python packages use `__init__.py` files and support relative imports. spec2git deliberately avoids this pattern because:

- **Simplicity**: Scripts don't need package installation
- **Clarity**: Absolute imports make dependencies explicit
- **Portability**: Easy to copy/move without breaking imports
- **Debugging**: No import path confusion

### Architecture Evolution

**v1.0 (Monolithic)**
- Single file: `spec2git.py` (1000+ lines)
- Single file: `git2spec.py` (1745 lines)
- Hard to maintain and test

**v2.0 (Modularized)**
- Split into multiple modules
- Organized into directories
- Still somewhat coupled

**v3.0 (Current - Workflow-based)**
- Workflow pattern for spec2git_lib
- Context-based dependency injection
- Immutable state management
- Production-ready architecture

---

## System Architecture

### Directory Structure (Detailed)

```
spec2git/
├── spec2git.py                 # Entry point (160 lines)
│
├── common/                     # Shared utilities (3 modules, ~360 lines total)
│   ├── config.py              # Configuration (113 lines)
│   ├── exceptions.py          # Exception hierarchy (49 lines)
│   └── validation.py          # Input validation (130 lines)
│
├── git2spec/                   # Git → Spec conversion (7 modules, ~2300 lines total)
│   ├── git2spec_core.py       # Orchestration (323 lines)
│   ├── git2spec_patterns.py   # Regex patterns (180 lines)
│   ├── git2spec_utils.py      # Utilities (250 lines)
│   ├── git2spec_spec_parser.py     # Spec parsing (350 lines)
│   ├── git2spec_git_analyzer.py    # Git analysis (420 lines)
│   ├── git2spec_patch_generator.py # Patch generation (380 lines)
│   └── git2spec_spec_updater.py    # Spec updating (400 lines)
│
├── spec2git_lib/               # Spec → Git conversion (12 modules, ~3800 lines total)
│   ├── spec2git_main.py       # CLI wrapper (153 lines)
│   ├── spec2git_workflow.py   # Workflow (335 lines)
│   ├── base_workflow.py       # Base class (73 lines)
│   ├── workflow_context.py    # Context manager (160 lines)
│   ├── conversion_state.py    # State tracking (280 lines)
│   ├── spec_parser.py         # Spec parsing (520 lines)
│   ├── git_operations.py      # Git commands (310 lines)
│   ├── source_handler.py      # Source handling (450 lines)
│   ├── patch_handler.py       # Patch application (380 lines)
│   ├── prep_executor.py       # %prep execution (580 lines)
│   ├── result_types.py        # Result types (70 lines)
│   └── shell_executor_template.sh  # Shell template
│
└── tests/                      # Test suite (6 modules, ~1500 lines total)
    ├── test_config.py
    ├── test_end_to_end.py
    ├── test_git_operations.py
    ├── test_patch_handler.py
    ├── test_spec_parser.py
    └── test_validation.py
```

### Subsystem Breakdown

#### 1. Entry Point (`spec2git.py`)

**Responsibilities:**
- Command-line argument parsing
- Mode selection (spec2git vs git2spec)
- Logging configuration
- Top-level error handling

**Key Functions:**
- `main()`: Entry point, parses args and routes to appropriate converter
- `setup_logging()`: Configures logging based on verbosity

**Exit Codes:**
- `0`: Success
- `1`: Failure (validation, execution, or unexpected error)

#### 2. Common Subsystem

Shared utilities used by both conversion directions.

**config.py**
- `Spec2GitConfig`: Dataclass with configurable constants
- `get_config()`: Global config singleton
- `from_environment()`: Load config from env vars
- Configuration includes: timeouts, file size limits, security settings

**exceptions.py**
- `SpecParseError`: Spec file parsing errors
- `PatchApplicationError`: Patch application errors
- `ValidationError`: Input validation errors
- `PrepExecutionError`: %prep execution errors (base class)
- `PrepCommandFailure`: Specific command failures
- `PrepTimeoutError`: Timeout errors
- `PrepSecurityError`: Security violations

**validation.py**
- `validate_spec2git_inputs()`: Validates spec2git parameters
- `validate_git2spec_inputs()`: Validates git2spec parameters
- Checks: file types, path safety, macro safety, numeric ranges

#### 3. Git2Spec Subsystem (Reverse Conversion)

Converts git repositories back to spec files with updated patches.

**Architecture Pattern:** Pipeline-based processing

```
Parse Spec → Analyze Git → Generate Patches → Update Spec
```

**git2spec_core.py** (Main Orchestrator)
- `Git2Spec`: Main class coordinating the conversion
- `run()`: Execute 4-phase pipeline
- Phase 1: Parse spec file
- Phase 2: Analyze git repository
- Phase 3: Extract patches from commits
- Phase 4: Update spec file

**git2spec_spec_parser.py** (Spec Parsing)
- `Git2SpecParser`: Parse spec files for git2spec
- Extracts: name, version, release, patches, base_commit_id
- Uses regex patterns from `git2spec_patterns.py`

**git2spec_git_analyzer.py** (Git Analysis)
- `Git2SpecAnalyzer`: Analyze git repository
- Find base commit (from spec or first commit)
- Identify new commits (added since spec)
- Identify modified commits (changed content)
- Compare with existing patches

**git2spec_patch_generator.py** (Patch Generation)
- `Git2SpecPatchGenerator`: Generate patch files
- Extract patches from commits using `git format-patch`
- Handle patch numbering and naming
- Support fuzzy matching for modified patches

**git2spec_spec_updater.py** (Spec Updating)
- `Git2SpecUpdater`: Update spec file
- Insert new patch definitions
- Update %prep section
- Increment release number
- Add changelog entry

**git2spec_patterns.py** (Patterns & Constants)
- Regex patterns for spec file parsing
- Constants for patch numbering
- Helper functions for pattern matching

**git2spec_utils.py** (Utilities)
- File I/O helpers
- String manipulation
- Path handling
- Diff utilities

#### 4. Spec2Git_lib Subsystem (Forward Conversion)

Converts spec files to git repositories with patches as commits.

**Architecture Pattern:** Workflow-based with context and state

```
Context → Workflow → Phases → Services → Result
```

**spec2git_main.py** (CLI Entry Point)
- `Spec2Git`: CLI wrapper class
- Validates inputs
- Creates workflow context
- Executes workflow
- Reports results

**spec2git_workflow.py** (Workflow Orchestration)
- `Spec2GitWorkflow`: Main workflow implementation
- Extends `BaseWorkflow`
- Phases:
  1. Parse spec file
  2. Setup output directory
  3. Download sources
  4. Execute %prep section (extraction + patches)

**base_workflow.py** (Base Workflow)
- `BaseWorkflow`: Abstract base class for workflows
- Provides: context updates, logging helpers
- Enforces: `execute()` method implementation

**workflow_context.py** (Context Management)
- `WorkflowContext`: Bundles state with services
- Lazy-loaded services: spec_parser, source_handler, patch_handler, etc.
- Factory method: `create()` for initialization
- Immutable updates: `update_state()` creates new context

**conversion_state.py** (State Tracking)
- `ConversionState`: Immutable state dataclass
- Tracks: paths, sources, patches, macros, configuration
- Copy-on-write updates: `with_updates()` method
- Factory method: `create()` for initialization

**spec_parser.py** (Spec Parsing)
- `SpecFileParser`: Parse spec files using rpmspec
- Extracts: name, version, release, sources, patches, macros, %prep
- Supports: conditional macros, architecture-specific builds
- Creates temporary build environment for rpmspec

**source_handler.py** (Source Handling)
- `SourceHandler`: Download and manage sources
- Find sources: local files, URLs, git repositories
- Download: HTTP/HTTPS/FTP sources
- Git clone: Support for git-based Source0
- Config.yaml integration: Read source metadata

**patch_handler.py** (Patch Application)
- `PatchHandler`: Apply patches to source code
- Supports: patch command, git apply command
- Strip levels: Automatic detection
- Rollback: On failure, rollback to previous state
- Git commit: Each patch becomes a git commit

**prep_executor.py** (Prep Execution)
- `PrepExecutor`: Execute %prep section
- Parse %prep macros: %setup, %patch, %autopatch, etc.
- Execute in phases: setup, patches, post-setup
- Shell execution: Uses template for safety
- Security: Validates commands, prevents dangerous operations

**git_operations.py** (Git Operations)
- `GitOperations`: Git command wrapper
- Operations: init, add, commit, log, diff, etc.
- Error handling: Proper exception propagation
- Output parsing: Parse git command output

**result_types.py** (Result Types)
- `ConversionResult`: Result of conversion
- Fields: success, error, patches_applied, sources_downloaded, etc.
- Immutable dataclass

---

## Data Flow

### Spec → Git Flow

```
1. User Input
   ├── spec_file: path/to/package.spec
   ├── output_dir: /tmp/package-git (optional)
   ├── macros: {name: value} (optional)
   └── options: stop_before_patch, use_tarball, etc.

2. Validation (common/validation.py)
   ├── Validate spec file extension
   ├── Check path security
   ├── Validate macro names
   └── Validate patch numbers

3. Context Creation (workflow_context.py)
   ├── Create ConversionState
   ├── Initialize logger
   └── Return WorkflowContext

4. Workflow Execution (spec2git_workflow.py)
   │
   ├── Phase 1: Parse Spec
   │   ├── Run rpmspec to extract metadata
   │   ├── Parse %prep section
   │   ├── Load config.yaml
   │   └── Update context with results
   │
   ├── Phase 2: Setup Output
   │   ├── Create/clean output directory
   │   └── Set as BUILD directory
   │
   ├── Phase 3: Download Sources
   │   ├── Find Source0, Source1, etc.
   │   ├── Check for git repository info
   │   └── Download/copy to BUILD directory
   │
   └── Phase 4: Execute %prep
       ├── Parse %prep macros
       ├── Extract source archives
       ├── Initialize git repository
       ├── Apply patches sequentially
       └── Create git commits

5. Result
   ├── success: True/False
   ├── git_repo_path: path/to/output
   ├── patches_applied: count
   └── error: error message (if failed)
```

### Git → Spec Flow

```
1. User Input
   ├── spec_file: path/to/package.spec
   ├── git_repo_dir: /tmp/package-git
   ├── output_spec: path/to/new.spec (optional)
   └── changelog_msg: "Fixed CVE-XXXX" (optional)

2. Validation (common/validation.py)
   ├── Validate spec file
   ├── Validate git repo directory
   └── Validate changelog message

3. Git2Spec Execution (git2spec_core.py)
   │
   ├── Phase 1: Parse Spec
   │   ├── Extract name, version, release
   │   ├── Extract existing patches
   │   └── Extract base_commit_id
   │
   ├── Phase 2: Analyze Git
   │   ├── Find base commit
   │   ├── List all commits after base
   │   ├── Identify new commits
   │   └── Identify modified commits
   │
   ├── Phase 3: Generate Patches
   │   ├── Run git format-patch for each commit
   │   ├── Number patches sequentially
   │   ├── Write patch files to spec directory
   │   └── Return patch metadata
   │
   └── Phase 4: Update Spec
       ├── Insert new Patch definitions
       ├── Update %prep section with %patch macros
       ├── Increment release number
       ├── Add changelog entry
       └── Write updated spec file

4. Result
   ├── success: True/False
   ├── backup_path: path/to/backup.spec.bak
   ├── patches_added: count
   └── updated_spec: path/to/spec
```

---

## Workflow Patterns

### BaseWorkflow Pattern

All workflows extend `BaseWorkflow` and implement `execute()`:

```python
class BaseWorkflow(ABC):
    def __init__(self, context: WorkflowContext):
        self.context = context
        self.logger = context.logger

    @abstractmethod
    def execute(self) -> ConversionResult:
        pass

    def _update_context(self, **kwargs) -> WorkflowContext:
        self.context = self.context.update_state(**kwargs)
        return self.context
```

**Benefits:**
- Consistent interface for all workflows
- Context management handled by base class
- Logging helpers available to all workflows
- Easy to add new workflows

### Context Pattern

Context bundles state with service instances:

```python
@dataclass
class WorkflowContext:
    state: ConversionState
    logger: logging.Logger

    # Lazy-loaded services
    _spec_parser: Optional[object] = None
    _source_handler: Optional[object] = None

    @property
    def spec_parser(self):
        if self._spec_parser is None:
            self._spec_parser = SpecFileParser(...)
        return self._spec_parser
```

**Benefits:**
- Services loaded only when needed
- Immutable state updates
- Clear dependency injection
- Easy testing (mock services)

### State Pattern

State is immutable and uses copy-on-write:

```python
@dataclass(frozen=True)
class ConversionState:
    spec_file: Path
    output_dir: Optional[Path] = None
    # ... more fields ...

    def with_updates(self, **kwargs) -> 'ConversionState':
        return replace(self, **kwargs)
```

**Benefits:**
- No accidental mutations
- Easy to track state changes
- Safer concurrent operations
- Simpler debugging

---

## State Management

### ConversionState Fields

**Path Information:**
- `spec_file`: Path to spec file
- `spec_dir`: Directory containing spec
- `output_dir`: Output directory for git repo
- `build_dir`: BUILD directory (usually == output_dir)
- `git_repo_path`: Path to git repository

**Metadata:**
- `name`: Package name
- `version`: Package version
- `release`: Package release number

**Sources & Patches:**
- `sources`: Dict[int, str] - Source0, Source1, etc.
- `patches`: Dict[int, PatchInfo] - Patch definitions
- `downloaded_sources`: Dict[int, Path] - Downloaded source paths

**Configuration:**
- `macros`: Dict[str, str] - RPM macros
- `config`: Spec2GitConfig - Global config
- `config_yaml_data`: Dict - config.yaml data
- `shared_sources_data`: Dict - Shared sources metadata

**Options:**
- `verbose`: Enable debug logging
- `force`: Force overwrite existing output
- `use_tarball`: Force tarball (ignore git info)
- `use_git_apply`: Use git apply instead of patch
- `target_arch`: Target architecture

**Control Flow:**
- `stop_before_patch`: Stop before this patch

**Prep Section:**
- `prep_section`: String - %prep section content

**Git Info:**
- `source0_git_info`: Dict - Git clone info for Source0

### State Transitions

```
1. Initial State (from user input)
   ConversionState(spec_file, output_dir, macros, ...)

2. After Parsing
   + name, version, release, sources, patches, prep_section

3. After Source Download
   + downloaded_sources

4. After Git Init
   + git_repo_path

5. After Prep Execution
   (final state)
```

---

## Advanced Features

### Patch Control

The patch control feature allows fine-grained control over which patches are applied during spec2git conversion. This is useful for:
- **Debugging**: Apply patches incrementally to find problematic patches
- **Partial Conversion**: Convert only a subset of patches
- **Resume Failed Runs**: Skip already-applied patches and continue
- **Range Processing**: Apply only patches in a specific range

#### Stop Before Patch

Stop conversion before applying a specific patch:

```bash
# Stop before Patch512 (applies 0-511)
./spec2git.py linux.spec --stop-before-patch 512
./spec2git.py linux.spec --stop-before-patch Patch512

# Debug: Apply only first 10 patches
./spec2git.py package.spec --stop-before-patch 10
```

**Behavior:**
- Patches with numbers < stop_before are applied
- Patches with numbers >= stop_before are NOT applied
- Conversion stops gracefully after executing pending shell commands
- Logs: "Stopping before patch X (PatchY) as requested"

#### Resume Execution

Resume execution from a saved state (e.g., after conflict resolution or `--stop-before-patch`):

```bash
# Resume from where it stopped
./spec2git.py package.spec --resume --output-dir /tmp/package-git
```

**Behavior:**
- Loads state from `.spec2git_state.json` in the output directory
- Restores directory stack (`pushd`/`popd` state)
- Skips initialization (source download, git init) if resuming
- Continues execution from the next line in `%prep` section

#### Implementation Details

**PrepExecutor Integration:**
```python
class PrepExecutor:
    def __init__(self, ...,
                 stop_before_patch: Optional[str] = None,
                 resume: bool = False):
        self.stop_before_patch = stop_before_patch
        self.resume = resume

    def execute_prep_section(self, ...):
        # If resuming, load state and skip to saved line index
        if self.resume:
            state = PrepState.load(...)
            current_line_index = state.next_line_index
            # Restore directory stack...

        for line in lines[current_line_index:]:
            # ... process line ...

            if is_patch(line):
                # Check stop_before
                if self.stop_before_patch and patch_num >= stop_num:
                    log("Stopping before...")
                    # Save state
                    state.save(...)
                    return

                # Apply patch
                apply_patch(patch)
                # Save state
                state.save(...)
```

**Patch Number Formats:**
- Numeric: `"512"` → Patch512
- With Prefix: `"Patch512"` → Patch512
- Both formats normalized to `"Patch512"` internally
- Extraction uses: `int(patch_str.replace('Patch', ''))`

**Edge Cases:**
- Empty patch list: No error, conversion succeeds
- stop_before = 0: No patches applied (success)
- Invalid formats validated by `validation.py`

#### Testing

The test suite covers:
1. **test_stop_before_patch**: Basic stop functionality
2. **test_patch_handler**: Patch application and conflict handling

All tests verify:
- Correct patches applied/skipped
- Git commit history matches expectations
- File content reflects applied patches
- Proper logging messages

---

## Module Reference

### Common Modules

#### config.py

**Purpose:** Centralized configuration management

**Key Classes:**
- `Spec2GitConfig`: Configuration dataclass

**Key Functions:**
- `get_config()`: Get global config instance
- `set_config()`: Set global config
- `reset_config()`: Reset to defaults

**Configuration Fields:**
- `default_subprocess_timeout`: 60 seconds
- `max_patch_filename_length`: 1024 characters
- `chunk_size`: 8192 bytes
- `default_strip_level`: 1
- `enable_path_traversal_checks`: True
- `diff_similarity_threshold`: 0.70 (70%)

**Environment Variables:**
- `SPEC2GIT_SUBPROCESS_TIMEOUT`
- `SPEC2GIT_GIT_CLONE_TIMEOUT`
- `SPEC2GIT_CHUNK_SIZE`

#### exceptions.py

**Purpose:** Custom exception hierarchy

**Exception Tree:**
```
Exception
├── SpecParseError
│   └── PrepExecutionError
│       ├── PrepCommandFailure
│       ├── PrepTimeoutError
│       └── PrepSecurityError
├── PatchApplicationError
└── ValidationError
```

**Usage:**
- `SpecParseError`: Spec file parsing issues
- `PatchApplicationError`: Patch application failures
- `ValidationError`: Input validation failures
- `PrepExecutionError`: %prep execution base class
- `PrepCommandFailure`: Specific command failed (includes command, exit code, stderr)
- `PrepTimeoutError`: Command exceeded timeout
- `PrepSecurityError`: Dangerous command detected

#### validation.py

**Purpose:** Input validation functions

**Key Functions:**
- `validate_spec2git_inputs()`: Validates all spec2git inputs
- `validate_git2spec_inputs()`: Validates all git2spec inputs

**Validation Checks:**
- File extension (.spec)
- Path security (no /dev/, /proc/)
- Macro safety (no __import__, etc.)
- String length limits
- Numeric ranges (patch numbers 0-99999)
- Non-empty strings

### Git2Spec Modules

#### git2spec_core.py

**Purpose:** Main orchestration for git → spec

**Key Classes:**
- `Git2Spec`: Main class

**Key Methods:**
- `run()`: Execute 4-phase pipeline
- `parse_spec_file()`: Phase 1
- `analyze_git_repo()`: Phase 2
- `extract_patches_from_commits()`: Phase 3
- `update_spec_file()`: Phase 4

**Returns:**
- `True` on success, `False` on failure

#### git2spec_spec_parser.py

**Purpose:** Parse spec files for git2spec

**Key Classes:**
- `Git2SpecParser`: Spec file parser

**Key Methods:**
- `parse()`: Parse spec file
- `_extract_name()`: Extract package name
- `_extract_version()`: Extract version
- `_extract_release()`: Extract release
- `_extract_patches()`: Extract patch definitions
- `_extract_base_commit_id()`: Extract base commit ID

**Returns:**
- Dict with: name, version, release, patches, base_commit_id

#### git2spec_git_analyzer.py

**Purpose:** Analyze git repository

**Key Classes:**
- `Git2SpecAnalyzer`: Git repository analyzer

**Key Methods:**
- `analyze()`: Main analysis method
- `_find_base_commit()`: Find base commit
- `_list_commits_after_base()`: List commits
- `_identify_new_commits()`: Find new commits
- `_identify_modified_commits()`: Find modified commits

**Returns:**
- Dict with: base_commit, current_commits, new_commits, modified_commits, has_changes

#### git2spec_patch_generator.py

**Purpose:** Generate patch files from commits

**Key Classes:**
- `Git2SpecPatchGenerator`: Patch generator

**Key Methods:**
- `extract_patches()`: Main extraction method
- `_generate_patch_for_commit()`: Generate single patch
- `_determine_patch_number()`: Assign patch number
- `_write_patch_file()`: Write patch to file

**Returns:**
- List of tuples: (patch_number, patch_filename, patch_content)

#### git2spec_spec_updater.py

**Purpose:** Update spec file with new patches

**Key Classes:**
- `Git2SpecUpdater`: Spec file updater

**Key Methods:**
- `update_spec()`: Main update method
- `_insert_patch_definitions()`: Add Patch lines
- `_update_prep_section()`: Add %patch macros
- `_increment_release()`: Bump release number
- `_add_changelog_entry()`: Add %changelog entry

**Side Effects:**
- Writes updated spec file
- Creates backup (if overwriting)

#### git2spec_patterns.py

**Purpose:** Regex patterns and constants

**Key Constants:**
- `PATCH_PATTERN`: Regex for Patch definitions
- `PREP_SECTION_PATTERN`: Regex for %prep section
- `CHANGELOG_PATTERN`: Regex for %changelog section
- `MAX_PATCH_NUMBER`: 99999

**Key Functions:**
- `extract_patch_number()`: Get number from PatchNNN
- `format_patch_line()`: Format Patch definition

#### git2spec_utils.py

**Purpose:** Utility functions

**Key Functions:**
- `read_file()`: Safe file reading
- `write_file()`: Safe file writing
- `run_command()`: Execute subprocess
- `calculate_similarity()`: Diff similarity
- `sanitize_filename()`: Clean filenames

### Spec2Git_lib Modules

#### spec2git_main.py

**Purpose:** CLI entry point for spec2git

**Key Classes:**
- `Spec2Git`: CLI wrapper

**Key Methods:**
- `run()`: Execute conversion
- `_setup_logging()`: Configure logging

**Workflow:**
1. Validate inputs
2. Create WorkflowContext
3. Create Spec2GitWorkflow
4. Execute workflow
5. Report results

#### spec2git_workflow.py

**Purpose:** Main workflow implementation

**Key Classes:**
- `Spec2GitWorkflow`: Extends BaseWorkflow

**Key Methods:**
- `execute()`: Main execution
- `_parse_spec()`: Parse spec file
- `_load_config_yaml()`: Load configuration
- `_prepare_output_directory()`: Setup output
- `_download_sources()`: Download all sources
- `_execute_prep_section()`: Execute %prep

**Phases:**
1. Parse spec file
2. Setup output directory
3. Download sources
4. Execute %prep section

#### base_workflow.py

**Purpose:** Base class for workflows

**Key Classes:**
- `BaseWorkflow`: Abstract base (ABC)

**Key Methods:**
- `execute()`: Abstract method
- `_update_context()`: Update workflow context
- `_log_step()`: Log workflow step
- `_log_error()`: Log error
- `_log_warning()`: Log warning

#### workflow_context.py

**Purpose:** Context management

**Key Classes:**
- `WorkflowContext`: Context dataclass

**Key Properties (Lazy-loaded):**
- `spec_parser`: SpecFileParser instance
- `source_handler`: SourceHandler instance
- `patch_handler`: PatchHandler instance
- `prep_executor`: PrepExecutor instance
- `git_ops`: GitOperations instance

**Key Methods:**
- `create()`: Factory method
- `update_state()`: Immutable state update

#### conversion_state.py

**Purpose:** State tracking

**Key Classes:**
- `ConversionState`: Immutable state dataclass

**Key Methods:**
- `create()`: Factory method
- `with_updates()`: Copy-on-write update

**Fields:** See [State Management](#state-management)

#### spec_parser.py

**Purpose:** Parse spec files using rpmspec

**Key Classes:**
- `SpecFileParser`: Spec parser

**Key Methods:**
- `parse()`: Main parsing method
- `_run_rpmspec()`: Execute rpmspec command
- `_parse_rpmspec_output()`: Parse rpmspec output
- `_extract_prep_section()`: Extract %prep section

**Returns:**
- Sets instance attributes: name, version, release, sources, patches, macros, prep_section

**Implementation Details:**
- Creates temporary build environment
- Runs `rpmspec --parse` to expand macros
- Parses output to extract metadata
- Supports conditional macros via `--define`

#### source_handler.py

**Purpose:** Download and manage sources

**Key Classes:**
- `SourceHandler`: Source manager

**Key Methods:**
- `find_source_file()`: Locate source file
- `_download_http_source()`: Download HTTP source
- `_clone_git_source()`: Clone git repository
- `_find_local_source()`: Find local file

**Search Order:**
1. Spec directory
2. Shared sources (from config.yaml)
3. Download from URL
4. Git clone (if config.yaml has git info)

#### patch_handler.py

**Purpose:** Apply patches

**Key Classes:**
- `PatchHandler`: Patch applicator

**Key Methods:**
- `apply_patch()`: Apply single patch
- `apply_patch_with_git()`: Apply using git apply
- `apply_patch_with_command()`: Apply using patch command
- `_determine_strip_level()`: Auto-detect -p level
- `_rollback()`: Rollback on failure

**Features:**
- Auto-detection of strip level
- Git commit for each patch
- Rollback on failure
- Detailed error messages

#### prep_executor.py

**Purpose:** Execute %prep section

**Key Classes:**
- `PrepExecutor`: %prep executor

**Key Methods:**
- `execute_prep_section()`: Main execution
- `_parse_prep_macros()`: Parse %setup, %patch, etc.
- `_execute_setup_phase()`: Handle %setup
- `_execute_patch_phase()`: Apply patches
- `_execute_shell_commands()`: Execute shell commands

**Supported Macros:**
- `%setup`: Extract source archives
- `%patch`, `%patchN`: Apply specific patch
- `%autopatch`: Apply all patches
- Shell commands (with security checks)

**Patch Control Features:**
- `stop_before_patch`: Stop before applying specified patch
  - Example: `--stop-before-patch 512` or `--stop-before-patch Patch512`
  - Useful for debugging or partial conversions
- `resume`: Resume execution from saved state
  - Example: `--resume`
  - Useful for resuming after conflict resolution or stopping
  - Uses `.spec2git_state.json` to restore context (CWD, directory stack, line number)

**Implementation Details:**
- Patch numbers are extracted from command lines as they're detected
- `stop_before_patch` check occurs second (stops execution completely)
- Proper logging: "Stopping before..." for stop_before
- Pending shell commands are executed before stopping
- State is saved to JSON file on stop or conflict

**Security:**
- Command whitelist
- Timeout enforcement
- Path traversal protection
- No dangerous operations (rm -rf /, etc.)

#### git_operations.py

**Purpose:** Git command wrapper

**Key Classes:**
- `GitOperations`: Git command executor

**Key Methods:**
- `init()`: Initialize repository
- `add()`: Stage files
- `commit()`: Create commit
- `log()`: Get commit log
- `diff()`: Get diff
- `format_patch()`: Generate patches

**Features:**
- Proper error handling
- Output parsing
- Timeout support

#### result_types.py

**Purpose:** Result type definitions

**Key Classes:**
- `ConversionResult`: Result dataclass

**Fields:**
- `success`: True/False
- `error`: Error message (if failed)
- `git_repo_path`: Path to git repo
- `patches_applied`: Number of patches
- `sources_downloaded`: Number of sources
- `warnings`: List of warnings

---

## Extension Points

### Adding New Conversion Features

**1. Add Configuration Option**
```python
# In common/config.py
@dataclass
class Spec2GitConfig:
    new_feature_enabled: bool = False
```

**2. Add State Field**
```python
# In spec2git_lib/conversion_state.py
@dataclass(frozen=True)
class ConversionState:
    new_feature_data: Optional[Dict] = None
```

**3. Add Workflow Phase**
```python
# In spec2git_lib/spec2git_workflow.py
def _new_feature_phase(self):
    # Implementation
    pass

def execute(self) -> ConversionResult:
    # ... existing phases ...
    self._new_feature_phase()
```

### Adding New Validation

```python
# In common/validation.py
def validate_new_input(value: str) -> None:
    if not meets_criteria(value):
        raise ValidationError(f"Invalid: {value}")
```

### Adding New Exception Type

```python
# In common/exceptions.py
class NewFeatureError(SpecParseError):
    """Exception for new feature"""
    pass
```

### Adding New Service

```python
# 1. Create new module in spec2git_lib/
# spec2git_lib/new_service.py
class NewService:
    def __init__(self, context):
        self.context = context

    def do_something(self):
        pass

# 2. Add to WorkflowContext
# In spec2git_lib/workflow_context.py
@dataclass
class WorkflowContext:
    _new_service: Optional[object] = None

    @property
    def new_service(self):
        if self._new_service is None:
            from spec2git_lib.new_service import NewService
            self._new_service = NewService(self)
        return self._new_service
```

### Adding New %prep Macro Support

```python
# In spec2git_lib/prep_executor.py
def _parse_prep_macros(self, prep_section: str):
    # ... existing macros ...

    # Add new macro
    new_macro_pattern = r'%newmacro\s+(.+)'
    matches = re.findall(new_macro_pattern, prep_section)
    for match in matches:
        self._handle_new_macro(match)
```

---

## Performance Considerations

### Optimization Strategies

**1. Lazy Loading**
- Services loaded only when needed
- Reduces startup time
- Minimizes memory usage

**2. Subprocess Optimization**
- Timeouts prevent hanging
- Capture output efficiently
- Reuse git operations

**3. File I/O**
- Read in chunks (8KB default)
- Stream large files
- Minimize temp file writes

**4. State Immutability**
- Copy-on-write for large structures
- Share unchanged data between states
- Minimal copying overhead

### Scalability

**Small Packages** (<10 patches):
- Time: ~5-10 seconds
- Memory: <50 MB
- Disk I/O: Minimal

**Medium Packages** (10-100 patches):
- Time: ~30-60 seconds
- Memory: <100 MB
- Disk I/O: Moderate

**Large Packages** (100+ patches, e.g., Linux kernel):
- Time: ~2-5 minutes
- Memory: <500 MB
- Disk I/O: Significant

**Bottlenecks:**
1. rpmspec parsing (largest single operation)
2. Git operations (format-patch, apply)
3. Source archive extraction
4. Patch application

---

## Testing Strategy

### Test Organization

```
tests/
├── test_config.py          # Configuration tests (6 tests)
├── test_validation.py      # Input validation tests (17 tests)
├── test_spec_parser.py     # Spec parsing tests (11 tests)
├── test_patch_handler.py   # Patch application tests (6 tests)
├── test_patch_control.py   # Patch control features (4 tests)
├── test_git_operations.py  # Git command tests (27 tests)
└── test_end_to_end.py      # Integration tests (8 tests)

Total: 79 tests
```

### Test Types

**1. Unit Tests**
- Test individual functions
- Mock external dependencies
- Fast execution (<1 second each)

**2. Integration Tests**
- Test module interactions
- Use real files and git
- Medium execution (~5-10 seconds each)

**3. End-to-End Tests**
- Test complete workflows
- Real spec files and repos
- Slow execution (~30-60 seconds each)

### Running Tests

```bash
# All tests
python3 -m pytest tests/

# Specific module
python3 -m pytest tests/test_config.py

# With coverage
python3 -m pytest --cov=. tests/

# Verbose
python3 -m pytest -v tests/
```

---

## Security Considerations

### Input Validation

**Path Security:**
- Reject /dev/ and /proc/ paths
- Check for path traversal attempts
- Validate file extensions

**Command Injection:**
- No shell=True in subprocess calls
- Command whitelist in %prep executor
- Escape special characters

**Macro Safety:**
- Reject dangerous macro names (__import__, etc.)
- Validate macro values
- Limit macro expansion depth

### Subprocess Security

**Resource Limits:**
- File size limits
- Patch filename length limits
- Number of patches limit (99999)

**Sandboxing:**
- %prep executed in isolated directory
- No access to parent directories
- Cleaned up after execution

---

## Glossary

**Terms:**
- **spec file**: RPM package specification file (.spec)
- **%prep section**: Section in spec file that prepares source code
- **patch**: Diff file that modifies source code
- **source archive**: Tarball or zip file with source code
- **git repository**: Git version control repository
- **workflow**: Multi-phase conversion process
- **context**: Bundle of state and services
- **state**: Immutable data about conversion progress
- **service**: Reusable component (parser, handler, executor)

**Abbreviations:**
- **RPM**: Red Hat Package Manager
- **CLI**: Command-Line Interface
- **ABC**: Abstract Base Class
- **I/O**: Input/Output
- **CVE**: Common Vulnerabilities and Exposures

---

## References

- [RPM Spec File Format](https://rpm-software-management.github.io/rpm/manual/spec.html)
- [Git Documentation](https://git-scm.com/doc)
- [Python Dataclasses](https://docs.python.org/3/library/dataclasses.html)
- [Python ABC](https://docs.python.org/3/library/abc.html)
- [Photon OS](https://vmware.github.io/photon/)

---

## Changelog

**v3.2 (Current)**
- Implemented robust resume mechanism (`--resume`) with persistent state
- Added handling for directory stack (`pushd`/`popd`) across resumes
- Improved patch conflict handling with `patch --merge` fallback
- Removed `--start-from-patch` in favor of `--resume`

**v3.1**
- Implemented patch control features (`--stop-before-patch`)
- Enhanced PrepExecutor with patch range control

**v3.0**
- Workflow-based architecture
- Context and state management
- Immutable state updates
- Comprehensive documentation

**v2.0**
- Modularized git2spec
- Organized directory structure
- No package complexity

**v1.0**
- Initial monolithic implementation

---

**Last Updated:** 2025-10-20
**Version:** 3.1
**Author:** Generated for Photon OS development

