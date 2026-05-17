%global build_if %{photon_subrelease} >= 91

%global debug_package %{nil}
%define srcname versioningit

Name:           python3-versioningit
Version:        3.1.0
Release:        3%{?dist}
Summary:        Versioning It with your Version In Git
URL:            https://pypi.org/project/versioningit
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://files.pythonhosted.org/packages/bd/cd/7a5ee8bb5a8c51632e51170bb125e439ae9d823239e88bffec08144418d4/%{srcname}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-hatchling
BuildRequires:  python3-pathspec
BuildRequires:  python3-pluggy
BuildRequires:  python3-packaging

Requires: python3

%description
Versioningit is yet another Python packaging plugin for automatically determining
your package’s version based on your version control repository’s tags.
Unlike others, it allows easy customization of the version format and
even lets you easily override the separate functions used for version extraction & calculation.

%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
%{pyproject_wheel}

%install
%{pyproject_install}

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/versioningit
%{python3_sitelib}/*

%changelog
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 3.1.0-3
- Extended to build for subrelease 91 and above
* Wed Mar 18 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 3.1.0-2
- Bump version as a part of python3.14 upgrade
* Fri Aug 29 2025 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 3.1.0-1
- Initial build
