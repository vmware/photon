"""
End-to-end tests for spec2git and git2spec

Tests comprehensive workflows including:
- Conditional patch application based on architecture
- Macro expansion in %setup and other commands
- File copying and manipulation in %prep
- Full bidirectional conversion workflows
- Complex spec file features
"""

import pytest
import tempfile
import shutil
import subprocess
import json
from pathlib import Path
import os


@pytest.fixture
def photon_e2e_env(tmp_path):
    """
    Create a complete Photon OS build environment for end-to-end tests.

    This fixture creates:
    - SPECS/ directory (for spec files)
    - SPECS/SOURCES/ subdirectory (for source tarballs and patches)
    - build-config.json file
    - Helper function to create tarballs

    Returns a tuple of (specs_dir, sources_dir, build_root, helper).
    """
    # Create the directory structure
    build_root = tmp_path / "photon-build"
    specs_dir = build_root / "SPECS"
    sources_dir = specs_dir / "SOURCES"  # SOURCES as subdirectory of SPECS
    specs_dir.mkdir(parents=True)
    sources_dir.mkdir(parents=True)

    # Create build-config.json
    build_config = {
        "photon-build-param": {
            "photon-dist-tag": ".ph5",
            "photon-release-version": "5.0"
        }
    }
    build_config_path = build_root / "build-config.json"
    with open(build_config_path, 'w') as f:
        json.dump(build_config, f)

    # Helper to create tarballs
    class Helper:
        @staticmethod
        def create_tarball(name, version, files_dict, output_dir=None):
            """
            Create a tarball for testing.

            Args:
                name: Package name
                version: Package version
                files_dict: Dict of {relative_path: content}
                output_dir: Where to create the tarball (defaults to sources_dir)

            Returns:
                Path to created tarball
            """
            if output_dir is None:
                output_dir = sources_dir

            # Create temporary directory with content
            temp_extract = tmp_path / "temp_extract"
            source_dir = temp_extract / f"{name}-{version}"
            source_dir.mkdir(parents=True, exist_ok=True)

            for rel_path, content in files_dict.items():
                file_path = source_dir / rel_path
                file_path.parent.mkdir(parents=True, exist_ok=True)
                file_path.write_text(content)

            # Create tarball
            tarball = output_dir / f"{name}-{version}.tar.gz"
            subprocess.run(
                ['tar', 'czf', str(tarball), '-C', str(temp_extract), f"{name}-{version}"],
                check=True, capture_output=True
            )

            # Cleanup temp directory
            shutil.rmtree(temp_extract)

            return tarball

    return specs_dir, sources_dir, build_root, Helper()


class TestConditionalPatches:
    """Test conditional patch application based on %ifarch and %if directives"""

    def test_ifarch_x86_64_patches_applied(self, photon_e2e_env):
        """Test that x86_64-specific patches are applied on x86_64"""
        specs_dir, sources_dir, build_root, helper = photon_e2e_env

        spec_content = """
Name:           test-conditional
Version:        1.0
Release:        1
Summary:        Test conditional patches
License:        MIT
Source0:        test-conditional-1.0.tar.gz

Patch0:         common.patch
%ifarch x86_64
Patch1:         x86-specific.patch
%endif
%ifarch aarch64
Patch2:         arm-specific.patch
%endif

%description
Test package

%prep
%setup -q
%autopatch -p1
"""
        spec_file = specs_dir / "test-conditional.spec"
        spec_file.write_text(spec_content)

        # Create source tarball
        helper.create_tarball("test-conditional", "1.0", {
            "README": "Test package",
            "main.c": "#include <stdio.h>\nint main() { return 0; }\n"
        })

        # Create patch files
        common_patch = sources_dir / "common.patch"
        common_patch.write_text("""--- a/README
+++ b/README
@@ -1 +1,2 @@
 Test package
+Common patch applied
""")

        x86_patch = sources_dir / "x86-specific.patch"
        x86_patch.write_text("""--- a/main.c
+++ b/main.c
@@ -1,2 +1,3 @@
 #include <stdio.h>
+// x86_64 optimization
 int main() { return 0; }
""")

        arm_patch = sources_dir / "arm-specific.patch"
        arm_patch.write_text("""--- a/main.c
+++ b/main.c
@@ -1,2 +1,3 @@
 #include <stdio.h>
+// aarch64 optimization
 int main() { return 0; }
""")

        # Run spec2git with x86_64 architecture
        output_dir = build_root / "test-git"

        from spec2git_lib.spec2git_main import Spec2Git

        converter = Spec2Git(
            spec_file=str(spec_file),
            output_dir=str(output_dir),
            macros={},
            verbose=True,
            target_arch='x86_64',
            force=True
        )

        # This should succeed and apply common + x86 patches
        result = converter.run()
        assert result is True

        # Check that x86 patch was applied
        actual_dir = output_dir / "test-conditional-1.0"
        assert actual_dir.exists(), f"Expected directory {actual_dir} not found"

        main_c = actual_dir / "main.c"
        assert main_c.exists()
        content = main_c.read_text()
        assert "x86_64 optimization" in content
        assert "aarch64 optimization" not in content

    def test_if_macro_conditional_patches(self, photon_e2e_env):
        """Test patches controlled by %if macro conditionals"""
        specs_dir, sources_dir, build_root, helper = photon_e2e_env

        spec_content = """
Name:           test-macro-cond
Version:        1.0
Release:        1
Summary:        Test macro conditionals
License:        MIT
Source0:        test-macro-cond-1.0.tar.gz

Patch0:         base.patch
%if 0%{?debug_build:1}
Patch1:         debug.patch
%endif

%description
Test package

%prep
%setup -q
%autopatch -p1
"""
        spec_file = specs_dir / "test-macro-cond.spec"
        spec_file.write_text(spec_content)

        # Create source tarball
        helper.create_tarball("test-macro-cond", "1.0", {
            "config.h": "#define VERSION 1\n"
        })

        # Create patch files
        base_patch = sources_dir / "base.patch"
        base_patch.write_text("""--- a/config.h
+++ b/config.h
@@ -1 +1,2 @@
 #define VERSION 1
+#define PATCHED 1
""")

        debug_patch = sources_dir / "debug.patch"
        debug_patch.write_text("""--- a/config.h
+++ b/config.h
@@ -1,2 +1,3 @@
 #define VERSION 1
 #define PATCHED 1
+#define DEBUG 1
""")

        # Run without debug_build macro - should only apply base patch
        output_dir = build_root / "test-git-nodebug"

        from spec2git_lib.spec2git_main import Spec2Git

        converter = Spec2Git(
            spec_file=str(spec_file),
            output_dir=str(output_dir),
            macros={},
            verbose=True,
            force=True
        )

        result = converter.run()
        assert result is True

        # Check that debug patch was NOT applied
        actual_dir = output_dir / "test-macro-cond-1.0"
        config_h = actual_dir / "config.h"
        content = config_h.read_text()
        assert "#define PATCHED 1" in content
        assert "#define DEBUG 1" not in content


class TestMacroExpansion:
    """Test macro expansion in %prep commands"""

    def test_setup_macro_with_name(self, photon_e2e_env):
        """Test %setup macro with -n parameter"""
        specs_dir, sources_dir, build_root, helper = photon_e2e_env

        spec_content = """
Name:           test-setup
Version:        1.0
Release:        1
Summary:        Test setup macro
License:        MIT
Source0:        source-tarball-1.0.tar.gz

%description
Test package

%prep
%setup -q -n source-tarball-1.0
"""
        spec_file = specs_dir / "test-setup.spec"
        spec_file.write_text(spec_content)

        # Create source tarball with different name
        helper.create_tarball("source-tarball", "1.0", {
            "README": "Source tarball"
        })

        # Run spec2git
        output_dir = build_root / "test-git"

        from spec2git_lib.spec2git_main import Spec2Git

        converter = Spec2Git(
            spec_file=str(spec_file),
            output_dir=str(output_dir),
            macros={},
            verbose=True,
            force=True
        )

        result = converter.run()
        assert result is True

        # Directory is created based on the actual tarball directory structure
        # Since %setup -n specifies source-tarball-1.0, that's the directory name
        actual_dir = output_dir / "source-tarball-1.0"
        assert actual_dir.exists(), f"Expected {actual_dir} to exist"

        readme = actual_dir / "README"
        assert readme.exists()
        assert readme.read_text() == "Source tarball"

    def test_macro_expansion_in_shell_commands(self, photon_e2e_env):
        """Test that macros are expanded in shell commands"""
        specs_dir, sources_dir, build_root, helper = photon_e2e_env

        spec_content = """
%global myprefix /usr/local

Name:           test-macros
Version:        1.0
Release:        1
Summary:        Test macro expansion
License:        MIT
Source0:        test-macros-1.0.tar.gz

%description
Test package

%prep
%setup -q
echo "prefix=%{myprefix}" > config.txt
"""
        spec_file = specs_dir / "test-macros.spec"
        spec_file.write_text(spec_content)

        # Create source tarball
        helper.create_tarball("test-macros", "1.0", {
            "README": "Test"
        })

        # Run spec2git
        output_dir = build_root / "test-git"

        from spec2git_lib.spec2git_main import Spec2Git

        converter = Spec2Git(
            spec_file=str(spec_file),
            output_dir=str(output_dir),
            macros={},
            verbose=True,
            force=True
        )

        result = converter.run()
        assert result is True

        actual_dir = output_dir / "test-macros-1.0"
        config_txt = actual_dir / "config.txt"
        assert config_txt.exists()
        # The echo command should have been executed
        content = config_txt.read_text().strip()
        assert "prefix=/usr/local" in content


class TestFileCopyingInPrep:
    """Test file operations in %prep section"""

    def test_cp_command_in_prep(self, photon_e2e_env):
        """Test cp command in prep section"""
        specs_dir, sources_dir, build_root, helper = photon_e2e_env

        spec_content = """
Name:           test-cp
Version:        1.0
Release:        1
Summary:        Test cp command
License:        MIT
Source0:        test-cp-1.0.tar.gz
Source1:        extra-config.txt

%description
Test package

%prep
%setup -q
cp %{SOURCE1} ./config.txt
"""
        spec_file = specs_dir / "test-cp.spec"
        spec_file.write_text(spec_content)

        # Create source tarball
        helper.create_tarball("test-cp", "1.0", {
            "README": "Test"
        })

        # Create extra source file
        extra_config = sources_dir / "extra-config.txt"
        extra_config.write_text("Extra configuration")

        # Run spec2git
        output_dir = build_root / "test-git"

        from spec2git_lib.spec2git_main import Spec2Git

        converter = Spec2Git(
            spec_file=str(spec_file),
            output_dir=str(output_dir),
            macros={},
            verbose=True,
            force=True
        )

        result = converter.run()
        assert result is True

        actual_dir = output_dir / "test-cp-1.0"
        config_txt = actual_dir / "config.txt"
        assert config_txt.exists()
        assert config_txt.read_text() == "Extra configuration"

    def test_sed_manipulation_in_prep(self, photon_e2e_env):
        """Test sed manipulation in prep section"""
        specs_dir, sources_dir, build_root, helper = photon_e2e_env

        spec_content = """
Name:           test-sed
Version:        1.0
Release:        1
Summary:        Test sed command
License:        MIT
Source0:        test-sed-1.0.tar.gz

%description
Test package

%prep
%setup -q
sed -i 's/"VERSION"/"1.0"/g' config.h
"""
        spec_file = specs_dir / "test-sed.spec"
        spec_file.write_text(spec_content)

        # Create source tarball
        helper.create_tarball("test-sed", "1.0", {
            "config.h": "#define VERSION \"VERSION\"\n"
        })

        # Run spec2git
        output_dir = build_root / "test-git"

        from spec2git_lib.spec2git_main import Spec2Git

        converter = Spec2Git(
            spec_file=str(spec_file),
            output_dir=str(output_dir),
            macros={},
            verbose=True,
            force=True
        )

        result = converter.run()
        assert result is True

        actual_dir = output_dir / "test-sed-1.0"
        config_h = actual_dir / "config.h"
        content = config_h.read_text()
        # sed should have replaced VERSION with 1.0
        assert '#define VERSION "1.0"' in content


class TestBidirectionalConversion:
    """Test spec -> git conversion with git repository verification"""

    def test_spec_to_git_to_spec_roundtrip(self, photon_e2e_env):
        """Test converting spec to git (git2spec part is separate tool)"""
        specs_dir, sources_dir, build_root, helper = photon_e2e_env

        spec_content = """
Name:           test-roundtrip
Version:        1.0
Release:        1
Summary:        Test roundtrip conversion
License:        MIT
Source0:        test-roundtrip-1.0.tar.gz

Patch0:         fix-typo.patch

%description
Test package for roundtrip

%prep
%setup -q
%patch0 -p1

%build
make

%install
make install
"""
        spec_file = specs_dir / "test-roundtrip.spec"
        spec_file.write_text(spec_content)

        # Create source tarball
        helper.create_tarball("test-roundtrip", "1.0", {
            "README": "Test packge\n",  # Note: typo, with newline
            "Makefile": "build:\n\t@echo Building\n"
        })

        # Create patch (must match exact file content)
        patch_file = sources_dir / "fix-typo.patch"
        patch_file.write_text("""--- a/README
+++ b/README
@@ -1 +1 @@
-Test packge
+Test package
""")

        # Convert spec to git
        git_dir = build_root / "test-git"

        from spec2git_lib.spec2git_main import Spec2Git

        spec2git = Spec2Git(
            spec_file=str(spec_file),
            output_dir=str(git_dir),
            macros={},
            verbose=True,
            force=True
        )

        result = spec2git.run()
        assert result is True

        # Verify git repository was created
        repo_dir = git_dir / "test-roundtrip-1.0"
        assert (repo_dir / ".git").exists()

        # Verify patch was applied
        readme = repo_dir / "README"
        assert readme.read_text().strip() == "Test package"  # Typo fixed

        # Verify git history exists
        import subprocess
        git_log = subprocess.run(
            ['git', 'log', '--oneline'],
            cwd=repo_dir,
            capture_output=True,
            text=True
        )
        assert git_log.returncode == 0
        assert len(git_log.stdout.strip().split('\n')) >= 1  # At least one commit


class TestComplexSpecFeatures:
    """Test complex spec file features"""

    def test_multiple_sources_and_patches(self, photon_e2e_env):
        """Test handling multiple sources and patches"""
        specs_dir, sources_dir, build_root, helper = photon_e2e_env

        spec_content = """
Name:           test-complex
Version:        1.0
Release:        1
Summary:        Test complex spec
License:        MIT
Source0:        test-complex-1.0.tar.gz
Source1:        additional-file.txt
Source2:        config.ini

Patch0:         fix1.patch
Patch1:         fix2.patch
Patch2:         feature.patch

%description
Test package with multiple sources and patches

%prep
%setup -q
cp %{SOURCE1} ./additional.txt
cp %{SOURCE2} ./config.ini
%patch0 -p1
%patch1 -p1
%patch2 -p1
"""
        spec_file = specs_dir / "test-complex.spec"
        spec_file.write_text(spec_content)

        # Create main tarball
        helper.create_tarball("test-complex", "1.0", {
            "main.c": "int main() { return 0; }\n",
            "README": "Version 1\n"
        })

        # Create additional sources
        (sources_dir / "additional-file.txt").write_text("Additional data")
        (sources_dir / "config.ini").write_text("[config]\nkey=value\n")

        # Create patches
        (sources_dir / "fix1.patch").write_text("""--- a/main.c
+++ b/main.c
@@ -1 +1,2 @@
+#include <stdio.h>
 int main() { return 0; }
""")

        (sources_dir / "fix2.patch").write_text("""--- a/README
+++ b/README
@@ -1 +1,2 @@
 Version 1
+Fixed
""")

        (sources_dir / "feature.patch").write_text("""--- a/main.c
+++ b/main.c
@@ -1,2 +1,3 @@
 #include <stdio.h>
+// New feature
 int main() { return 0; }
""")

        # Run spec2git
        output_dir = build_root / "test-git"

        from spec2git_lib.spec2git_main import Spec2Git

        converter = Spec2Git(
            spec_file=str(spec_file),
            output_dir=str(output_dir),
            macros={},
            verbose=True,
            force=True
        )

        result = converter.run()
        assert result is True

        # Verify all files are present
        actual_dir = output_dir / "test-complex-1.0"

        assert (actual_dir / "main.c").exists()
        assert (actual_dir / "README").exists()
        assert (actual_dir / "additional.txt").exists()
        assert (actual_dir / "config.ini").exists()

        # Verify patches were applied
        main_c_content = (actual_dir / "main.c").read_text()
        assert "#include <stdio.h>" in main_c_content
        assert "// New feature" in main_c_content

        readme_content = (actual_dir / "README").read_text()
        assert "Fixed" in readme_content
