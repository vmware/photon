# Tests for spec2git

## Quick Start

To run all tests:
```bash
cd /root/gerrit/photon-common2/tools/scripts/spec2git
python3 -m pytest tests/ -v
```

Or from the project root:
```bash
cd /root/gerrit/photon-common2
python3 -m pytest tools/scripts/spec2git/tests/ -v
```

## Running Specific Tests

Run specific test files:
```bash
python3 -m pytest tests/test_validation.py -v
python3 -m pytest tests/test_config.py -v
python3 -m pytest tests/test_spec_parser.py -v
python3 -m pytest tests/test_git_operations.py -v
python3 -m pytest tests/test_patch_handler.py -v
python3 -m pytest tests/test_end_to_end.py -v
```

Run specific test class:
```bash
python3 -m pytest tests/test_validation.py::TestSpec2GitValidation -v
```

Run specific test:
```bash
python3 -m pytest tests/test_validation.py::TestSpec2GitValidation::test_empty_spec_file_rejected -v
```

## Coverage Reports (Optional)

First, install pytest-cov:
```bash
pip3 install pytest-cov
```

Then run with coverage:
```bash
cd /root/gerrit/photon-common2/tools/scripts/spec2git
python3 -m pytest tests/ --cov=. --cov-report=html
```

Or from project root:
```bash
cd /root/gerrit/photon-common2
python3 -m pytest tools/scripts/spec2git/tests/ --cov=tools/scripts/spec2git --cov-report=html
```

View coverage report:
```bash
firefox htmlcov/index.html  # or your preferred browser
```

## Test Structure

Current test files:
- `test_validation.py` (17 tests) - Input validation and security ✅
- `test_config.py` (6 tests) - Configuration management ✅
- `test_git_operations.py` (27 tests) - Git operations ✅
- `test_patch_handler.py` (6 tests) - Patch file handling and metadata ✅
- `test_spec_parser.py` (11 tests) - Spec file parsing ✅
- `test_end_to_end.py` (8 tests) - End-to-end integration tests ✅
- `test_patch_control.py` (4 tests) - Patch control features ✅

**Total: 79 tests passing, 0 skipped** 🎉

### All Tests Fixed!

**test_spec_parser.py** - Now uses `photon_build_env` fixture:
- ✅ All 11 tests passing!
- Uses proper SPECS directory structure to prevent hang
- Tests correctly validate current parser implementation

**test_end_to_end.py** - Now uses `photon_e2e_env` fixture:
- ✅ All 8 tests passing!
- Tests conditional patches, macro expansion, file operations, and complex workflows
- Uses SPECS/SOURCES/ directory structure for proper file discovery
- Includes helper function to create test tarballs dynamically

### photon_build_env Fixture

Tests now use a fixture that creates proper Photon OS structure:
```python
build_root/
├── SPECS/          # Spec files go here
├── SOURCES/        # Source files (optional)
└── build-config.json  # Mock Photon config
```

This prevents the hang issue by ensuring `_get_dist_tag()` finds the SPECS directory.

## Test Requirements

### Minimal (for running tests)
```bash
pip3 install pytest
```

### Full (for coverage reports)
```bash
pip3 install pytest pytest-cov
```

### Already Installed?
Check if pytest is installed:
```bash
python3 -m pytest --version
```

If you see an error, install it:
```bash
pip3 install pytest
```

