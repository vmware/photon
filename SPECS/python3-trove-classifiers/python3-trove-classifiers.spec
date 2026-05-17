%global build_if %{photon_subrelease} >= 91

%define srcname trove-classifiers

Name:           python3-trove-classifiers
Version:        2026.1.14.14
Release:        2%{?dist}
Summary:        Canonical source for classifiers on PyPI (pypi.org)
URL:            https://github.com/pypa/trove-classifiers
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon

BuildArch:      noarch

Source0: https://github.com/pypa/trove-classifiers/archive/refs/tags/%{srcname}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

# Drop dependency on calver which is not packaged in Fedora.
# This patch is rebased version of upstream PR:
# https://github.com/pypa/trove-classifiers/pull/126/commits/809156bb35852bcaa1c753e0165f1814f2bcedf6
Patch0: Move-to-PEP-621-declarative-metadata.patch

BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-packaging
BuildRequires: python3-build
BuildRequires: python3-installer
%if 0%{?with_check}
%define ExtraBuildRequires python3-pytest
%endif

Requires: python3

%description
Canonical source for classifiers on PyPI.
Classifiers categorize projects per PEP 301. Use this package to validate
classifiers in packages for PyPI upload or download.

%prep
%autosetup -p1 -n %{srcname}-%{version}
sed -i 's/@@VERSION@@/%{version}/g' pyproject.toml

%build
%py3_build_wheel

%install
%py3_install_wheel

%{py_byte_compile_and_ghost}

%if 0%{?with_check}
%check
sed -i 's@{BINDIR}/@@' tests/test_cli.py
%pytest
%endif

%files -f %{py_ghost_filelist}
%defattr(-,root,root)
%{_bindir}/trove-classifiers
%{python3_sitelib}/*

%changelog
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 2026.1.14.14-2
- Extended to build for subrelease 91 and above
* Fri Apr 10 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2026.1.14.14-1
- Initial version, needed by hatchling
