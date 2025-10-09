"""
Tests for patch control features (--stop-before-patch and --start-from-patch)

Tests the ability to control which patches are applied during conversion.
"""

import pytest
import subprocess
import json
from pathlib import Path


@pytest.fixture
def photon_patch_control_env(tmp_path):
    """
    Create environment for testing patch control features.
    """
    build_root = tmp_path / "photon-build"
    specs_dir = build_root / "SPECS"
    sources_dir = specs_dir / "SOURCES"
    specs_dir.mkdir(parents=True)
    sources_dir.mkdir(parents=True)

    # Create build-config.json
    config = {
        "photon-build-param": {
            "photon-dist-tag": ".ph5",
            "photon-release-version": "5.0"
        }
    }
    (build_root / "build-config.json").write_text(json.dumps(config))

    # Helper to create tarball
    def create_tarball(name, version, files_dict):
        temp_extract = tmp_path / "temp_extract"
        source_dir = temp_extract / f"{name}-{version}"
        source_dir.mkdir(parents=True, exist_ok=True)

        for rel_path, content in files_dict.items():
            file_path = source_dir / rel_path
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content)

        tarball = sources_dir / f"{name}-{version}.tar.gz"
        subprocess.run(
            ['tar', 'czf', str(tarball), '-C', str(temp_extract), f"{name}-{version}"],
            check=True, capture_output=True
        )

        import shutil
        shutil.rmtree(temp_extract)
        return tarball

    return specs_dir, sources_dir, build_root, create_tarball


class TestStopBeforePatch:
    """Test --stop-before-patch functionality"""

    def test_stop_before_patch_by_number(self, photon_patch_control_env):
        """Test stopping before a specific patch number"""
        specs_dir, sources_dir, build_root, create_tarball = photon_patch_control_env

        # Create spec with 3 patches
        spec_content = """
Name:           testpkg
Version:        1.0
Release:        1
Summary:        Test patch control
License:        MIT
Source0:        testpkg-1.0.tar.gz

Patch0:         patch0.patch
Patch1:         patch1.patch
Patch2:         patch2.patch

%description
Test

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
"""
        spec_file = specs_dir / "testpkg.spec"
        spec_file.write_text(spec_content)

        # Create tarball with multiple files
        create_tarball("testpkg", "1.0", {
            "file0.txt": "content0\n",
            "file1.txt": "content1\n",
            "file2.txt": "content2\n"
        })

        # Create non-overlapping patches
        (sources_dir / "patch0.patch").write_text("""--- a/file0.txt
+++ b/file0.txt
@@ -1 +1,2 @@
 content0
+patch0 applied
""")

        (sources_dir / "patch1.patch").write_text("""--- a/file1.txt
+++ b/file1.txt
@@ -1 +1,2 @@
 content1
+patch1 applied
""")

        (sources_dir / "patch2.patch").write_text("""--- a/file2.txt
+++ b/file2.txt
@@ -1 +1,2 @@
 content2
+patch2 applied
""")

        # Run spec2git with --stop-before-patch 2
        output_dir = build_root / "test-stop"

        from spec2git_lib.spec2git_main import Spec2Git

        converter = Spec2Git(
            spec_file=str(spec_file),
            output_dir=str(output_dir),
            stop_before_patch="2",
            verbose=True,
            force=True
        )

        result = converter.run()
        assert result is True

        # Verify git history
        repo_dir = output_dir / "testpkg-1.0"
        assert repo_dir.exists()

        log_result = subprocess.run(
            ['git', 'log', '--oneline'],
            cwd=repo_dir,
            capture_output=True,
            text=True
        )

        commits = [l for l in log_result.stdout.strip().split('\n') if l]

        # Should have: base commit + patch0 + patch1 = 3 commits
        assert len(commits) == 3, f"Expected 3 commits, got {len(commits)}"

        # Verify patch2 was not applied
        file2_content = (repo_dir / "file2.txt").read_text()
        assert "patch2 applied" not in file2_content

        # Verify patch0 and patch1 were applied
        file0_content = (repo_dir / "file0.txt").read_text()
        assert "patch0 applied" in file0_content

        file1_content = (repo_dir / "file1.txt").read_text()
        assert "patch1 applied" in file1_content

    def test_stop_before_patch_with_patch_prefix(self, photon_patch_control_env):
        """Test stopping with Patch prefix (e.g., Patch512)"""
        specs_dir, sources_dir, build_root, create_tarball = photon_patch_control_env

        spec_content = """
Name:           testpkg2
Version:        1.0
Release:        1
Summary:        Test
License:        MIT
Source0:        testpkg2-1.0.tar.gz
Patch0:         p0.patch
Patch1:         p1.patch
%description
Test
%prep
%setup -q
%patch0 -p1
%patch1 -p1
"""
        spec_file = specs_dir / "testpkg2.spec"
        spec_file.write_text(spec_content)

        create_tarball("testpkg2", "1.0", {
            "a.txt": "a\n",
            "b.txt": "b\n"
        })

        (sources_dir / "p0.patch").write_text("""--- a/a.txt
+++ b/a.txt
@@ -1 +1,2 @@
 a
+p0
""")

        (sources_dir / "p1.patch").write_text("""--- a/b.txt
+++ b/b.txt
@@ -1 +1,2 @@
 b
+p1
""")

        output_dir = build_root / "test-stop2"

        from spec2git_lib.spec2git_main import Spec2Git

        converter = Spec2Git(
            spec_file=str(spec_file),
            output_dir=str(output_dir),
            stop_before_patch="Patch1",  # Using Patch prefix
            verbose=True,
            force=True
        )

        result = converter.run()
        assert result is True

        repo_dir = output_dir / "testpkg2-1.0"
        log_result = subprocess.run(
            ['git', 'log', '--oneline'],
            cwd=repo_dir,
            capture_output=True,
            text=True
        )

        commits = [l for l in log_result.stdout.strip().split('\n') if l]
        assert len(commits) == 2  # base + patch0


class TestStartFromPatch:
    """Test --start-from-patch functionality"""

    def test_start_from_patch_skips_earlier(self, photon_patch_control_env):
        """Test starting from a specific patch skips earlier ones"""
        specs_dir, sources_dir, build_root, create_tarball = photon_patch_control_env

        spec_content = """
Name:           testpkg3
Version:        1.0
Release:        1
Summary:        Test
License:        MIT
Source0:        testpkg3-1.0.tar.gz
Patch0:         p0.patch
Patch1:         p1.patch
Patch2:         p2.patch
%description
Test
%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
"""
        spec_file = specs_dir / "testpkg3.spec"
        spec_file.write_text(spec_content)

        create_tarball("testpkg3", "1.0", {
            "f0.txt": "f0\n",
            "f1.txt": "f1\n",
            "f2.txt": "f2\n"
        })

        for i in range(3):
            patch_content = f"""--- a/f{i}.txt
+++ b/f{i}.txt
@@ -1 +1,2 @@
 f{i}
+p{i}
"""
            (sources_dir / f"p{i}.patch").write_text(patch_content)

        output_dir = build_root / "test-start"

        from spec2git_lib.spec2git_main import Spec2Git

        converter = Spec2Git(
            spec_file=str(spec_file),
            output_dir=str(output_dir),
            start_from_patch="1",
            verbose=True,
            force=True
        )

        result = converter.run()
        assert result is True

        repo_dir = output_dir / "testpkg3-1.0"

        # Verify patch0 was NOT applied
        f0_content = (repo_dir / "f0.txt").read_text()
        assert "p0" not in f0_content

        # Verify patch1 and patch2 WERE applied
        f1_content = (repo_dir / "f1.txt").read_text()
        assert "p1" in f1_content

        f2_content = (repo_dir / "f2.txt").read_text()
        assert "p2" in f2_content

        # Verify commit count (base + patch1 + patch2 = 3)
        log_result = subprocess.run(
            ['git', 'log', '--oneline'],
            cwd=repo_dir,
            capture_output=True,
            text=True
        )
        commits = [l for l in log_result.stdout.strip().split('\n') if l]
        assert len(commits) == 3


class TestCombinedPatchControl:
    """Test combining --start-from-patch and --stop-before-patch"""

    def test_start_and_stop_combined(self, photon_patch_control_env):
        """Test using both start and stop together"""
        specs_dir, sources_dir, build_root, create_tarball = photon_patch_control_env

        spec_content = """
Name:           testpkg4
Version:        1.0
Release:        1
Summary:        Test
License:        MIT
Source0:        testpkg4-1.0.tar.gz
Patch0:         p0.patch
Patch1:         p1.patch
Patch2:         p2.patch
Patch3:         p3.patch
%description
Test
%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
"""
        spec_file = specs_dir / "testpkg4.spec"
        spec_file.write_text(spec_content)

        create_tarball("testpkg4", "1.0", {
            f"f{i}.txt": f"f{i}\n" for i in range(4)
        })

        for i in range(4):
            (sources_dir / f"p{i}.patch").write_text(f"""--- a/f{i}.txt
+++ b/f{i}.txt
@@ -1 +1,2 @@
 f{i}
+p{i}
""")

        output_dir = build_root / "test-combined"

        from spec2git_lib.spec2git_main import Spec2Git

        converter = Spec2Git(
            spec_file=str(spec_file),
            output_dir=str(output_dir),
            start_from_patch="1",
            stop_before_patch="3",
            verbose=True,
            force=True
        )

        result = converter.run()
        assert result is True

        repo_dir = output_dir / "testpkg4-1.0"

        # Only patch1 and patch2 should be applied
        # patch0 skipped by start_from, patch3 stopped before

        f0_content = (repo_dir / "f0.txt").read_text()
        assert "p0" not in f0_content

        f1_content = (repo_dir / "f1.txt").read_text()
        assert "p1" in f1_content

        f2_content = (repo_dir / "f2.txt").read_text()
        assert "p2" in f2_content

        f3_content = (repo_dir / "f3.txt").read_text()
        assert "p3" not in f3_content

        # Verify commit count (base + patch1 + patch2 = 3)
        log_result = subprocess.run(
            ['git', 'log', '--oneline'],
            cwd=repo_dir,
            capture_output=True,
            text=True
        )
        commits = [l for l in log_result.stdout.strip().split('\n') if l]
        assert len(commits) == 3

