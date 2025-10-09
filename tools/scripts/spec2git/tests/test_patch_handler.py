"""
Tests for patch handler functionality

Tests patch file location and metadata extraction.
Note: Patch detection tests have been removed as that functionality
is now handled internally by PrepExecutor which parses %prep sections.
"""

import pytest
from pathlib import Path
import tempfile
import os

# Add parent directory to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from spec2git_lib.patch_handler import PatchHandler


class TestPatchFileLocation:
    """Test patch file location functionality"""

    def test_find_patch_file_in_spec_dir(self, tmp_path):
        """Test finding patch file directly in spec directory"""
        spec_dir = tmp_path / "spec"
        spec_dir.mkdir()

        # Create a patch file
        patch_file = spec_dir / "test.patch"
        patch_file.write_text("patch content")

        handler = PatchHandler(spec_dir)
        result = handler.find_patch_file("test.patch")

        assert result == patch_file
        assert result.exists()

    def test_find_patch_file_in_subdirectory(self, tmp_path):
        """Test finding patch file in subdirectory"""
        spec_dir = tmp_path / "spec"
        spec_dir.mkdir()
        patches_subdir = spec_dir / "patches"
        patches_subdir.mkdir()

        # Create a patch file in subdirectory
        patch_file = patches_subdir / "test.patch"
        patch_file.write_text("patch content")

        handler = PatchHandler(spec_dir)
        result = handler.find_patch_file("test.patch")

        assert result == patch_file
        assert result.exists()

    def test_find_patch_file_not_found(self, tmp_path):
        """Test error when patch file not found"""
        spec_dir = tmp_path / "spec"
        spec_dir.mkdir()

        handler = PatchHandler(spec_dir)

        with pytest.raises(FileNotFoundError, match="Patch file not found"):
            handler.find_patch_file("nonexistent.patch")


class TestPatchMetadataExtraction:
    """Test patch metadata extraction"""

    def test_extract_metadata_with_all_fields(self, tmp_path):
        """Test extracting all metadata fields from patch"""
        spec_dir = tmp_path / "spec"
        spec_dir.mkdir()

        patch_content = """From: John Doe <john@example.com>
Date: Mon, 1 Jan 2024 12:00:00 +0000
Subject: [PATCH] Fix SSL handling

Detailed description of the fix.

---
 file.c | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
"""

        patch_file = spec_dir / "test.patch"
        patch_file.write_text(patch_content)

        handler = PatchHandler(spec_dir)
        subject, author, date = handler.extract_patch_metadata(patch_file, 1)

        # Note: extract_patch_metadata now returns full description in subject
        assert "Fix SSL handling" in subject
        assert author == "John Doe <john@example.com>"
        assert date == "Mon, 1 Jan 2024 12:00:00 +0000"

    def test_extract_metadata_with_patch_prefix(self, tmp_path):
        """Test removing [PATCH] prefix from subject"""
        spec_dir = tmp_path / "spec"
        spec_dir.mkdir()

        patch_content = """Subject: [PATCH v2 1/3] Add new feature

Description.
---
"""

        patch_file = spec_dir / "test.patch"
        patch_file.write_text(patch_content)

        handler = PatchHandler(spec_dir)
        subject, author, date = handler.extract_patch_metadata(patch_file, 1)

        # Subject now includes description
        assert "Add new feature" in subject
        assert author is None
        assert date is None

    def test_extract_metadata_fallback_subject(self, tmp_path):
        """Test fallback subject when no Subject header found"""
        spec_dir = tmp_path / "spec"
        spec_dir.mkdir()

        patch_content = """---
 file.c | 1 +
 1 file changed, 1 insertion(+)
"""

        patch_file = spec_dir / "my-patch.patch"
        patch_file.write_text(patch_content)

        handler = PatchHandler(spec_dir)
        subject, author, date = handler.extract_patch_metadata(patch_file, 5)

        assert subject == "Apply patch 5: my-patch.patch"
        assert author is None
        assert date is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
