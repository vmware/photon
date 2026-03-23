%global build_if %{photon_subrelease} <= 91

%global debug_package %{nil}
%define srcname scramp

Name:           python3-scramp
Version:        1.4.6
Release:        1.2%{?dist}
Summary:        Python implementation of the SCRAM protocol
URL:            https://pypi.org/project/scramp
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
BuildArch:      noarch

Source0: https://files.pythonhosted.org/packages/58/77/6db18bab446c12cfbee22ca8f65d5b187966bd8f900aeb65db9e60d4be3d/%{srcname}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  python3-devel
BuildRequires:  python3-wheel
BuildRequires:  python3-pip
BuildRequires:  python3-hatchling
BuildRequires:  python3-pathspec
BuildRequires:  python3-pluggy
BuildRequires:  python3-versioningit
BuildRequires:  python3-packaging

Requires: python3
Requires: python3-asn1crypto

%description
A Python implementation of the SCRAM authentication protocol.

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
%{python3_sitelib}/*

%changelog
* Mon Mar 23 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.4.6-1.2
- Fix config.yaml
* Wed Mar 18 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.4.6-1.1
- Bump after moving to SPECS/91
* Fri Aug 29 2025 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.4.6-1
- Initial build
