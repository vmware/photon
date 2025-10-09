# spec2git - Bidirectional RPM Spec and Git Repository Converter

A tool for converting between RPM .spec files and git repositories, with full support for patches and bidirectional conversion.

## Overview

**spec2git** is a sophisticated Python-based tool that provides:
- **Spec → Git**: Convert RPM spec files to git repositories with all patches applied as commits
- **Git → Spec**: Convert modified git repositories back to spec files with updated patches
- **Workflow Architecture**: Modular, maintainable design with clear separation of concerns
- **%prep Execution**: Full support for RPM %prep macros (%setup, %patch, %autopatch, etc.)
- **Production Ready**: Comprehensive error handling, validation, and rollback capabilities

## Quick Start

```bash
# Navigate to the spec2git directory
cd /root/gerrit/photon-common2/tools/scripts/spec2git

# Convert spec to git (default mode)
./spec2git.py package.spec

# Convert git back to spec
./spec2git.py package.spec --git2spec --git-repo /path/to/repo
```

**Dependencies:** Python 3.6+, git, rpm-build (for rpmspec command)

## Directory Structure

```
spec2git/
├── spec2git.py              # Main entry point (executable script)
│
├── common/                  # Shared utilities (3 modules)
│   ├── config.py           # Configuration management
│   ├── exceptions.py       # Custom exception hierarchy
│   └── validation.py       # Input validation
│
├── git2spec/               # Git to Spec conversion (7 modules)
│   ├── git2spec_core.py           # Main orchestration
│   ├── git2spec_patterns.py       # Regex patterns & constants
│   ├── git2spec_utils.py          # Utility functions
│   ├── git2spec_spec_parser.py    # Spec file parsing
│   ├── git2spec_git_analyzer.py   # Git commit extraction
│   ├── git2spec_patch_generator.py  # Patch generation
│   └── git2spec_spec_updater.py   # Spec file updating
│
├── spec2git_lib/           # Spec to Git conversion (12 modules)
│   ├── spec2git_main.py         # Main Spec2Git class
│   ├── spec2git_workflow.py     # Workflow orchestration
│   ├── base_workflow.py         # Base workflow class
│   ├── workflow_context.py      # Context management
│   ├── conversion_state.py      # State tracking
│   ├── spec_parser.py           # Spec file parser
│   ├── git_operations.py        # Git operations
│   ├── source_handler.py        # Source archive handling
│   ├── patch_handler.py         # Patch application
│   ├── prep_executor.py         # %prep execution
│   ├── result_types.py          # Result type definitions
│   └── shell_executor_template.sh  # Shell template for %prep
│
└── tests/                   # Test suite
    ├── test_config.py
    ├── test_end_to_end.py
    ├── test_git_operations.py
    ├── test_patch_handler.py
    ├── test_spec_parser.py
    └── test_validation.py
```

## Usage

### Basic Usage

```bash
# Spec to Git (default mode)
./spec2git.py package.spec

# Git to Spec
./spec2git.py package.spec --git2spec --git-repo /path/to/repo
```

### Spec to Git Examples

```bash
# Basic conversion
./spec2git.py linux.spec

# With custom output directory
./spec2git.py linux.spec --output-dir /tmp/linux-git

# With macro definitions
./spec2git.py linux.spec --define canister_build=1 --define acvp_build=1

# Stop before a specific patch
./spec2git.py linux.spec --stop-before-patch Patch512

# Resume from a specific patch
./spec2git.py linux.spec --start-from-patch 56 --output-dir /tmp/linux-git

# Force using tarball source (ignore config.yaml git info)
./spec2git.py linux.spec --use-tarball

# Use git apply instead of patch command
./spec2git.py linux.spec --use-git-apply

# Target specific architecture
./spec2git.py linux.spec --arch aarch64

# Force overwrite existing output directory
./spec2git.py linux.spec --force
```

### Git to Spec Examples

```bash
# Update original spec file (creates backup)
./spec2git.py linux.spec --git2spec --git-repo /tmp/linux-git

# Create new spec file (preserves original)
./spec2git.py linux.spec --git2spec --git-repo /tmp/linux-git --output-spec linux-new.spec

# With custom changelog message
./spec2git.py linux.spec --git2spec --git-repo /tmp/linux-git --changelog "Fixed CVE-2024-XXXXX"

# Use commit messages for changelog
./spec2git.py linux.spec --git2spec --git-repo /tmp/linux-git --use-commit-messages
```

### Command-Line Options

#### Common Options
- `--verbose`, `-v`: Enable verbose logging (DEBUG level)
- `--arch ARCH`: Target architecture (e.g., x86_64, aarch64)

#### Spec to Git Options
- `--output-dir`, `-o`: Output directory for git repository
- `--define`, `-D`: Define macro (format: `name=value` or `name`)
- `--stop-before-patch`: Stop before applying specified patch
- `--start-from-patch`: Resume from specified patch
- `--use-tarball`: Force using tarball instead of git repository
- `--force`, `-f`: Force overwrite existing output directory
- `--use-git-apply`: Use `git apply` instead of `patch` command

#### Git to Spec Options
- `--git2spec`: Enable Git to Spec mode
- `--git-repo`: Path to git repository with changes (required)
- `--output-spec`: Output spec file path (default: overwrite original)
- `--changelog`: Custom changelog message
- `--use-commit-messages`: Use commit messages for changelog entries


### Module Organization

**common/** - Shared utilities used by both converters
- `config.py`: Configuration dataclass with environment variable support
- `exceptions.py`: Custom exception hierarchy
- `validation.py`: Input validation functions

**git2spec/** - Converts git repos back to spec files
- Refactored from 1745-line monolith into 7 focused modules
- Average module size: ~320 lines
- Clean separation: parsing, analysis, generation, updating

**spec2git_lib/** - Converts spec files to git repos
- Workflow-based architecture with clear phases
- Context-based dependency injection
- Handles source extraction, patch application, git operations

See [ARCHITECTURE.md](./ARCHITECTURE.md) for detailed architecture documentation.

## Key Features

### Spec to Git Features

#### Core Functionality
- **Source Handling**: Automatic detection and extraction of source archives
- **Multi-Source Support**: Handles multiple sources (Source0, Source1, etc.)
- **Git Repository Cloning**: Supports git-based Source0 from config.yaml
- **Patch Application**: Sequential patch application with git commits
- **%prep Execution**: Full RPM %prep macro support (%setup, %patch, %autopatch, etc.)
- **Conditional Handling**: Architecture-specific conditional handling

#### Advanced Features
- **Automatic Rollback**: Automatic rollback on patch failure
- **Partial Conversion**: Stop/resume from specific patches
- **Flexible Source**: Support for both tarball and git sources
- **Macro Support**: Custom macro definitions via command line
- **Git Apply Mode**: Option to use `git apply` instead of `patch` command

### Git to Spec Features

#### Core Functionality
- **Commit Detection**: Detects new and modified commits
- **Patch Generation**: Generates patch files from commits
- **Spec Updating**: Updates spec file with new patches
- **Version Management**: Automatic release version increment
- **Changelog Generation**: Automatic or custom changelog entries

#### Advanced Features
- **Fuzzy Matching**: 70% similarity threshold for patch matching
- **Backup Management**: Automatic backup creation when overwriting
- **Commit-to-Patch Mapping**: Clear mapping between commits and patches
- **Flexible Changelog**: Custom messages or commit-based entries

### Error Handling & Validation

- **Input Validation**: Comprehensive validation of all inputs
- **Path Security**: Protection against path traversal attacks
- **Timeout Management**: Configurable timeouts for subprocess operations
- **Graceful Degradation**: Continues on non-critical errors with warnings

## Configuration

### Environment Variables

- `SPEC2GIT_SUBPROCESS_TIMEOUT`: Default subprocess timeout (seconds)
- `SPEC2GIT_GIT_CLONE_TIMEOUT`: Git clone timeout (seconds)
- `SPEC2GIT_CHUNK_SIZE`: Chunk size for file operations (bytes)

### config.yaml Support

spec2git supports `config.yaml` in the spec directory for additional configuration:

```yaml
sources:
  - archive: linux-6.1.10.tar.gz
    repo_url: https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git
    commit_id: abc123def456

shared_sources:
  - ../shared_sources.yaml
```

## Development

### Running Tests

```bash
cd /root/gerrit/photon-common2/tools/scripts/spec2git
python3 -m pytest tests/
```

### Code Organization

- Each module has a single, clear responsibility
- No circular dependencies
- Absolute imports only (no relative imports)
- No `__init__.py` files (simpler for scripts)
- Type hints for better IDE support
- Comprehensive docstrings

### Adding Features

1. Identify the appropriate module (common/git2spec/spec2git_lib)
2. Follow existing patterns (workflow steps, handlers, etc.)
3. Add validation in `common/validation.py`
4. Update tests in `tests/`
5. Document in README.md and ARCHITECTURE.md

## Troubleshooting

### Common Issues

**Issue**: `ValidationError: spec_file must end with .spec`
- **Solution**: Ensure your spec file has the `.spec` extension

**Issue**: `git command not found`
- **Solution**: Install git: `tdnf install git`

**Issue**: `rpmspec command not found`
- **Solution**: Install rpm-build: `tdnf install rpm-build`

**Issue**: `Patch application failed`
- **Solution**: Check patch file format and use `--verbose` for details

**Issue**: `Output directory already exists`
- **Solution**: Use `--force` flag or remove existing directory

### Debug Mode

Enable verbose logging for detailed information:

```bash
./spec2git.py package.spec --verbose
```

## Examples

### Real-World Example: Linux Kernel

```bash
# Convert Linux spec to git
cd /path/to/specs/linux
./spec2git.py linux.spec --output-dir /tmp/linux-git --define canister_build=1

# Make changes in git
cd /tmp/linux-git
# ... make modifications ...
git add .
git commit -m "Fix CVE-2024-XXXXX"

# Convert back to spec
cd /path/to/specs/linux
./spec2git.py linux.spec --git2spec --git-repo /tmp/linux-git --changelog "Fixed CVE-2024-XXXXX"
```

### Multi-Patch Workflow

```bash
# Apply patches 1-10 only
./spec2git.py package.spec --stop-before-patch 11

# Review changes
cd package-version-git/
git log

# Continue with remaining patches
cd ..
./spec2git.py package.spec --start-from-patch 11 --output-dir package-version-git
```

## Performance

- **Small packages** (<10 patches): ~5-10 seconds
- **Medium packages** (10-100 patches): ~30-60 seconds
- **Large packages** (100+ patches, like Linux): ~2-5 minutes

Performance depends on:
- Number and size of patches
- Source archive size
- Disk I/O speed
- Git repository size (if using git clone)

## Version History

**v3.0** - Production Release (Current)
- Workflow-based architecture for spec2git_lib
- Context-based dependency injection
- Immutable state management
- Enhanced %prep execution with full macro support
- Comprehensive error handling and validation
- Production-ready with extensive testing

**v2.0** - Complete Refactoring
- Modularized git2spec from 1745-line monolith
- Organized into common/git2spec/spec2git_lib structure
- Removed package complexity (no `__init__.py` files)
- Single entry point: spec2git.py

**v1.0** - Original Implementation
- Monolithic files
- Basic functionality

## Contributing

This project is part of the Photon OS development infrastructure. For contributions:

1. Follow existing code style and patterns
2. Add tests for new features
3. Update documentation (README.md, ARCHITECTURE.md)
4. Ensure all tests pass: `python3 -m pytest tests/`

## License

Apache 2.0

## Author

Generated for Photon OS development

## See Also

- [ARCHITECTURE.md](./ARCHITECTURE.md) - Detailed architecture documentation
- [tests/README.md](./tests/README.md) - Test suite documentation
- [RPM Spec File Format](https://rpm-software-management.github.io/rpm/manual/spec.html)
- [Git Documentation](https://git-scm.com/doc)
