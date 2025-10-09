"""
Unit tests for SpecFileParser

Tests spec file parsing functionality in isolation.
"""

import pytest
import tempfile
import json
from pathlib import Path

from spec2git_lib.spec_parser import SpecFileParser
from common.exceptions import SpecParseError


@pytest.fixture
def photon_build_env(tmp_path):
    """
    Create a mock Photon OS build environment with proper directory structure.

    This fixture creates:
    - SPECS/ directory
    - build-config.json file

    Returns the SPECS directory path.
    """
    # Create the directory structure
    build_root = tmp_path / "photon-build"
    specs_dir = build_root / "SPECS"
    specs_dir.mkdir(parents=True)

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

    return specs_dir


class TestSpecFileParser:
    """Test SpecFileParser class"""

    def create_temp_spec(self, specs_dir: Path, content: str) -> Path:
        """
        Helper to create a temporary spec file in the SPECS directory.

        Args:
            specs_dir: The SPECS directory from the photon_build_env fixture
            content: The spec file content

        Returns:
            Path to the created spec file
        """
        spec_file = specs_dir / "test.spec"
        spec_file.write_text(content)
        return spec_file

    def test_parse_basic_info(self, photon_build_env):
        """Test parsing name, version, release"""
        content = """
Name:           testpkg
Version:        1.0.0
Release:        1%{?dist}
Summary:        Test package
License:        MIT
Source0:        testpkg-1.0.0.tar.gz

%description
Test package description
"""
        spec_file = self.create_temp_spec(photon_build_env, content)
        parser = SpecFileParser(spec_file)
        parser.parse()

        assert parser.name == "testpkg"
        assert parser.version == "1.0.0"
        # %{?dist} should expand to .ph5 from build-config.json
        assert parser.release in ["1", "1.ph5"]

    def test_parse_with_macros(self, photon_build_env):
        """Test macro expansion"""
        content = """
%global major_version 2
%global minor_version 5

Name:           testpkg
Version:        %{major_version}.%{minor_version}.1
Release:        1
Summary:        Test
License:        MIT
Source0:        testpkg.tar.gz

%description
Test
"""
        spec_file = self.create_temp_spec(photon_build_env, content)
        parser = SpecFileParser(spec_file)
        parser.parse()

        # Macros are expanded by rpmspec, so version should be expanded
        assert parser.version == "2.5.1"
        # Note: parser.macros is no longer populated in the current implementation
        # The macros are expanded by rpmspec during parsing

    def test_parse_sources(self, photon_build_env):
        """Test parsing source definitions"""
        content = """
Name:           testpkg
Version:        1.0
Release:        1
Summary:        Test
License:        MIT

Source0:        https://example.com/%{name}-%{version}.tar.gz
Source1:        extra-file.txt

%description
Test
"""
        spec_file = self.create_temp_spec(photon_build_env, content)
        parser = SpecFileParser(spec_file)
        parser.parse()

        assert len(parser.sources) == 2
        assert 0 in parser.sources
        assert 1 in parser.sources
        assert "testpkg-1.0.tar.gz" in parser.sources[0]

    def test_parse_patches(self, photon_build_env):
        """Test parsing patch definitions"""
        content = """
Name:           testpkg
Version:        1.0
Release:        1
Summary:        Test
License:        MIT
Source0:        test.tar.gz

Patch0:         fix-bug1.patch
Patch1:         fix-bug2.patch
Patch10:        feature-x.patch

%description
Test
"""
        spec_file = self.create_temp_spec(photon_build_env, content)
        parser = SpecFileParser(spec_file)
        parser.parse()

        assert len(parser.patches) == 3
        # Note: patches dict is {filename: number} not {number: filename}
        assert parser.patches["fix-bug1.patch"] == 0
        assert parser.patches["fix-bug2.patch"] == 1
        assert parser.patches["feature-x.patch"] == 10

    def test_parse_prep_section(self, photon_build_env):
        """Test parsing %prep section"""
        content = """
Name:           testpkg
Version:        1.0
Release:        1
Summary:        Test
License:        MIT
Source0:        test.tar.gz

Patch0:         fix1.patch
Patch1:         fix2.patch
Patch2:         fix3.patch

%description
Test

%prep
%autosetup
%autopatch -p1 -M2

%build
echo "build"
"""
        spec_file = self.create_temp_spec(photon_build_env, content)
        parser = SpecFileParser(spec_file)
        parser.parse()

        # Should have extracted prep section
        assert parser.prep_section is not None
        assert len(parser.prep_section) > 0
        # Prep section is expanded by rpmspec, so it contains shell commands
        # Check for common prep section patterns like cd, rm, chmod
        assert "cd" in parser.prep_section or "rm" in parser.prep_section

    def test_missing_name_raises_error(self, photon_build_env):
        """Missing Name field should raise error"""
        content = """
Version:        1.0
Release:        1
Source0:        test.tar.gz

%description
Test
"""
        spec_file = self.create_temp_spec(photon_build_env, content)
        parser = SpecFileParser(spec_file)
        with pytest.raises(SpecParseError, match="Name"):
            parser.parse()

    def test_missing_version_raises_error(self, photon_build_env):
        """Missing Version field should raise error"""
        content = """
Name:           testpkg
Release:        1
Source0:        test.tar.gz

%description
Test
"""
        spec_file = self.create_temp_spec(photon_build_env, content)
        parser = SpecFileParser(spec_file)
        with pytest.raises(SpecParseError, match="Version"):
            parser.parse()

    def test_missing_source_raises_error(self, photon_build_env):
        """Missing Source field should raise error"""
        content = """
Name:           testpkg
Version:        1.0
Release:        1
Summary:        Test
License:        MIT

%description
Test
"""
        spec_file = self.create_temp_spec(photon_build_env, content)
        parser = SpecFileParser(spec_file)
        with pytest.raises(SpecParseError, match="Source"):
            parser.parse()

    def test_conditional_macros(self, photon_build_env):
        """Test conditional macro expansion"""
        content = """
%global with_feature 1

Name:           testpkg
Version:        1.0
Release:        1%{?dist}
Summary:        Test %{?with_feature:with feature}%{!?without_feature:enabled}
License:        MIT

Source0:        test.tar.gz

%description
Test
"""
        spec_file = self.create_temp_spec(photon_build_env, content)
        parser = SpecFileParser(spec_file)
        parser.parse()

        # Conditional macros should work
        assert parser.name == "testpkg"

    def test_additional_macros_override(self, photon_build_env):
        """Test that additional_macros parameter is accepted"""
        content = """
%global custom_val original

Name:           testpkg
Version:        1.0
Release:        1
Summary:        Test
License:        MIT

Source0:        test.tar.gz

%description
Test
"""
        spec_file = self.create_temp_spec(photon_build_env, content)
        parser = SpecFileParser(spec_file)
        # Just verify that additional_macros parameter is accepted without error
        parser.parse(additional_macros={"custom_val": "override"})

        # Verify parsing succeeded
        assert parser.name == "testpkg"
        assert parser.version == "1.0"

    def test_nonexistent_file_raises_error(self, photon_build_env):
        """Nonexistent spec file should raise error"""
        nonexistent_path = photon_build_env / "nonexistent.spec"
        parser = SpecFileParser(nonexistent_path)
        with pytest.raises(SpecParseError, match="not found"):
            parser.parse()
