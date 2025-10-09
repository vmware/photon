"""
Unit tests for input validation

Tests the validation logic to ensure bad inputs are caught early.
"""

import pytest
from common.exceptions import ValidationError
from spec2git_lib.spec2git_main import Spec2Git
from git2spec.git2spec_core import Git2Spec
from common.validation import validate_spec2git_inputs, validate_git2spec_inputs


class TestSpec2GitValidation:
    """Test Spec2Git input validation"""

    def test_empty_spec_file_rejected(self):
        """Empty spec file should be rejected"""
        with pytest.raises(ValidationError, match="must be a non-empty string"):
            validate_spec2git_inputs("", None, None, None, None)

    def test_non_spec_file_rejected(self):
        """Non-.spec files should be rejected"""
        with pytest.raises(ValidationError, match="must end with .spec"):
            validate_spec2git_inputs("foo.txt", None, None, None, None)

    def test_relative_paths_allowed(self):
        """Relative paths with .. should be allowed for legitimate use cases"""
        # This should NOT raise an exception - relative paths are valid
        try:
            validate_spec2git_inputs("../photon-5.0/SPECS/kpatch/kpatch.spec", None, None, None, None)
            validate_spec2git_inputs("../../other-repo/test.spec", None, None, None, None)
        except ValidationError:
            pytest.fail("Relative paths with .. should be allowed")

    def test_dev_path_rejected(self):
        """/dev paths should be rejected"""
        with pytest.raises(ValidationError, match="Suspicious spec_file path"):
            validate_spec2git_inputs("/dev/null.spec", None, None, None, None)

    def test_valid_spec_file_accepted(self):
        """Valid spec file path should be accepted"""
        # Should not raise
        validate_spec2git_inputs("/tmp/foo.spec", None, None, None, None)

    def test_invalid_macros_rejected(self):
        """Non-dict macros should be rejected"""
        with pytest.raises(ValidationError, match="must be a dictionary"):
            validate_spec2git_inputs("/tmp/foo.spec", None, "not a dict", None, None)

    def test_invalid_macro_values_rejected(self):
        """Non-string macro values should be rejected"""
        with pytest.raises(ValidationError, match="must be strings"):
            validate_spec2git_inputs("/tmp/foo.spec", None, {"foo": 123}, None, None)

    def test_dangerous_macro_names_rejected(self):
        """Dangerous macro names should be rejected"""
        with pytest.raises(ValidationError, match="not allowed for security"):
            validate_spec2git_inputs("/tmp/foo.spec", None, {"__import__": "os"}, None, None)

    def test_invalid_patch_number_format_rejected(self):
        """Invalid patch number formats should be rejected"""
        with pytest.raises(ValidationError, match="must be in format"):
            validate_spec2git_inputs("/tmp/foo.spec", None, None, "invalid", None)

    def test_negative_patch_number_rejected(self):
        """Negative patch numbers should be rejected"""
        # This will fail the isdigit() check
        with pytest.raises(ValidationError):
            validate_spec2git_inputs("/tmp/foo.spec", None, None, "-1", None)

    def test_huge_patch_number_rejected(self):
        """Excessively large patch numbers should be rejected"""
        with pytest.raises(ValidationError, match="must be between"):
            validate_spec2git_inputs("/tmp/foo.spec", None, None, "999999", None)

    def test_valid_patch_numbers_accepted(self):
        """Valid patch numbers should be accepted"""
        # Should not raise
        validate_spec2git_inputs("/tmp/foo.spec", None, None, "123", "456")
        validate_spec2git_inputs("/tmp/foo.spec", None, None, "Patch123", "Patch456")


class TestGit2SpecValidation:
    """Test Git2Spec input validation"""

    def test_empty_spec_file_rejected(self):
        """Empty spec file should be rejected"""
        with pytest.raises(ValidationError, match="must be a non-empty string"):
            validate_git2spec_inputs("", "/tmp/repo", None)

    def test_empty_repo_dir_rejected(self):
        """Empty repo dir should be rejected"""
        with pytest.raises(ValidationError, match="must be a non-empty string"):
            validate_git2spec_inputs("/tmp/foo.spec", "", None)

    def test_non_string_changelog_rejected(self):
        """Non-string changelog should be rejected"""
        with pytest.raises(ValidationError, match="must be a string"):
            validate_git2spec_inputs("/tmp/foo.spec", "/tmp/repo", 123)

    def test_excessive_changelog_length_rejected(self):
        """Excessively long changelog should be rejected"""
        long_msg = "x" * 1001
        with pytest.raises(ValidationError, match="too long"):
            validate_git2spec_inputs("/tmp/foo.spec", "/tmp/repo", long_msg)

    def test_valid_inputs_accepted(self):
        """Valid inputs should be accepted"""
        # Should not raise
        validate_git2spec_inputs("/tmp/foo.spec", "/tmp/repo", "Fixed CVE")

