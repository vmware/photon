# Linux Kernel Crypto Module Source Diff Tool

A Python library and command-line tool to analyze Linux kernel `crypto/Makefile` and compare source files for `crypto/canister.o` between different kernel versions.

## Features

- **Dynamic Makefile parsing**: Automatically parses pattern rules from the Makefile (no hardcoded mappings)
- **Handles complex builds**: Supports nested variable references, line continuations, and conditional compilation
- **File comparison**: Compares files between two kernel versions with line-level statistics
- **Detailed change tracking**: Shows lines removed, added, and percentage changed for each file
- **Smart filtering**: Option to exclude comments, empty lines, and indentation-only changes from statistics
- **Diff generation**: Creates individual `.diff` files for detailed change review
- **Flexible output**: Option to include/exclude removed and added files
- **Flexible**: Works with different Linux kernel versions with varying Makefile structures
- **Modular design**: Separate libraries for analysis and comparison

## Project Structure

```
lkcm-source-diff/
├── lkcm-source-diff.py      # Command-line interface (main script)
├── libs/
│   ├── canister_analyzer.py # Core library for Makefile analysis
│   └── file_comparator.py   # Library for file comparison
└── README.md
```

## Usage

### As a Library

```python
from libs.canister_analyzer import get_canister_source_files
from libs.file_comparator import compare_files_batch

# Get list of source files
source_files = get_canister_source_files('path/to/linux-source-tree')

# source_files is a list of strings with paths relative to source tree root
for file in source_files:
    print(file)

# Compare files between two trees
comparisons = compare_files_batch('tree1/', 'tree2/', source_files)
```

### As a Command-Line Tool

Compare source files between two Linux kernel versions:

```bash
# Basic comparison (shows only common files)
./lkcm-source-diff.py linux-6.1.75-2 linux-6.12.41-16

# Include removed and added files
./lkcm-source-diff.py linux-6.1.75-2 linux-6.12.41-16 --new-files

# Ignore comment-only changes in statistics
./lkcm-source-diff.py linux-6.1.75-2 linux-6.12.41-16 --ignore-comments

# Generate diff files for common files
./lkcm-source-diff.py linux-6.1.75-2 linux-6.12.41-16 --generate-diffs

# Combine multiple flags
./lkcm-source-diff.py linux-6.1.75-2 linux-6.12.41-16 --new-files --ignore-comments --generate-diffs
```

#### Basic Output (common files only):
```
==================================================================================================================================================================
#     File                                                     Before     Removed       Added       After    % Changed
==================================================================================================================================================================
1     arch/x86/crypto/aesni-intel_asm.S                          1234         45          52        1241      4.2% ...  7.9%
2     crypto/aes_generic.c                                        456         12          18         462      3.9% ...  6.6%
...
==================================================================================================================================================================
      Total                                                     45678       1234        1567       46011      5.2% ...  6.1%
==================================================================================================================================================================
```

#### Output with --new-files flag:
```
====================================================================================================================================================================================================
#     File                                                     Status         Before     Removed       Added       After    % Changed
====================================================================================================================================================================================================
1     arch/x86/crypto/aesni-intel_asm.S                                          1234         45          52        1241      4.2% ...  7.9%
2     crypto/aes_generic.c                                                        456         12          18         462      3.9% ...  6.6%
...
50    arch/x86/crypto/old_cipher.c                             Removed            234        234           0           0    N/A
51    arch/x86/crypto/aes-gcm-aesni-x86_64.S                   Added                0          0         567         567    N/A
...
====================================================================================================================================================================================================
      Total                                                                     46789       2345        2678       47122      5.5% ...  7.2%
====================================================================================================================================================================================================
```

The percentage changed is shown as two values:
- **First value (optimistic)**: `max(Removed, Added) / Before * 100`
- **Second value (worst case)**: `(Removed + Added) / Before * 100`

**Explanation:** For example, in `lib/crypto/aes.c`, upstream replaced one `#include` with another:
```diff
-#include <asm/unaligned.h>
+#include <linux/unaligned.h>
```
The optimistic approach says one line has been changed. The worst case calculation considers it as 1 line removed and 1 line added.

#### Comment and Whitespace Filtering

When using the `--ignore-comments` flag, the tool intelligently filters out non-functional changes from the statistics:

- **Comment-only changes**: Filters out all comment lines (full-line and inline comments)
- **Empty line changes**: Ignores added or removed blank lines
- **Indentation changes**: Detects when lines differ only in whitespace/indentation
- **Inline comments**: Strips comments from code lines before comparison

The following comment styles are supported:

- **C/C++ style** (`.c`, `.h`, `.cpp`, `.java`): `//` and `/* ... */`
- **Python/Shell/Makefile style** (`.py`, `.sh`, `.mk`, `Makefile`): `#`
- **Assembly** (`.s`, `.asm`): `#` and `;`
- **Preprocessed assembly** (`.S`): `#` for comments, but preserves C preprocessor directives (`#include`, `#define`, `#ifdef`, etc.)
- **ASN.1** (`.asn1`, `.asn`): `--`
- **SQL** (`.sql`): `--`

This is useful for focusing on actual code changes and ignoring:
- Documentation or license header updates
- Code reformatting (indentation changes)
- Whitespace-only modifications

#### Diff File Generation

When using the `--generate-diffs` flag, the tool creates individual `.diff` files for each file present in both trees:

- Creates a `diffs/` directory in the current working directory
- Generates unified diff files with the same relative path structure
- Example: `arch/x86/crypto/aesni-intel_asm.S` → `diffs/arch/x86/crypto/aesni-intel_asm.S.diff`
- Only generates diffs for files that have actual changes
- Respects the `--ignore-comments` flag:
  - **Without `--ignore-comments`**: Diffs show all changes including comments and whitespace
  - **With `--ignore-comments`**: Diffs show only functional code changes (normalized)

This is useful for:
- Reviewing changes in detail
- Applying patches selectively
- Archiving change history
- Integrating with other diff tools

## Library API

### `get_canister_source_files(linux_source_tree_path)`

Main library function to get list of source files for crypto/canister.o

**Parameters:**
- `linux_source_tree_path` (str): Path to the Linux source tree root directory

**Returns:**
- `list`: List of source file paths relative to the source tree root

**Raises:**
- `FileNotFoundError`: If the source tree or Makefile doesn't exist
- `Exception`: If there's an error parsing the Makefile

**Example:**
```python
try:
    files = get_canister_source_files('linux-6.12.41-16')
    print(f"Found {len(files)} files")
except FileNotFoundError as e:
    print(f"Error: {e}")
```

### `compare_files_batch(tree1_path, tree2_path, file_list, ignore_comments=False)`

Compares multiple files between two source trees.

**Parameters:**
- `tree1_path` (str): Path to the first source tree
- `tree2_path` (str): Path to the second source tree
- `file_list` (list): List of file paths (relative to tree roots) to compare
- `ignore_comments` (bool): If True, exclude comment-only lines, empty lines, and indentation-only changes from statistics (default: False)

**Returns:**
- `dict`: Dictionary mapping file paths to comparison results with keys:
  - `lines_before`: Number of lines in tree1
  - `lines_after`: Number of lines in tree2
  - `lines_removed`: Number of lines removed
  - `lines_added`: Number of lines added

### `generate_diff(tree1_path, tree2_path, file_path, ignore_comments=False)`

Generates a unified diff for a single file between two source trees.

**Parameters:**
- `tree1_path` (str): Path to the first source tree
- `tree2_path` (str): Path to the second source tree
- `file_path` (str): Relative path to the file to diff
- `ignore_comments` (bool): If True, generate diff from normalized files (default: False)

**Returns:**
- `str`: Unified diff output, or empty string if files are identical or don't exist

**Example:**
```python
from libs.file_comparator import generate_diff

# Generate a standard diff
diff = generate_diff('linux-6.1.75-2', 'linux-6.12.41-16', 'crypto/aes_generic.c')
print(diff)

# Generate a normalized diff (ignoring comments/whitespace)
diff_normalized = generate_diff('linux-6.1.75-2', 'linux-6.12.41-16', 'crypto/aes_generic.c', ignore_comments=True)
print(diff_normalized)
```

## How It Works

1. **Parse Makefile**: Reads `crypto/Makefile` and extracts:
   - The `canister.o` build rule
   - All variable assignments
   - Pattern rules for mapping object files to source files

2. **Resolve Dependencies**:
   - Extracts variables referenced in the `canister.o` rule
   - Recursively resolves nested variable references
   - Handles `$(addprefix ...)` expressions

3. **Map to Source Files**:
   - Uses pattern rules from Makefile (e.g., `x86-%.o` → `arch/x86/crypto/%.c`)
   - Tries both `.c` and `.S` extensions
   - Verifies files exist in the source tree

4. **Compare Files**:
   - Uses Python's `difflib` to compute line-by-line differences
   - Calculates statistics: lines removed, added, and percentage changed
   - Handles missing files gracefully

## Supported Linux Kernel Versions

Tested with:
- linux-6.1.75-2 (40 source files)
- linux-6.12.41-16 (72 source files)

Should work with any Linux kernel version that builds `crypto/canister.o`.

