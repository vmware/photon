%global build_if %{photon_subrelease} >= 92

%global srcname versioneer

Summary:        version-string management for VCS-controlled trees
Name:           python3-versioneer
Version:        0.29
Release:        1%{?dist}
Url:            https://pypi.org/project/versioneer/
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon

BuildArch:      noarch

Source0:        https://files.pythonhosted.org/packages/32/d7/854e45d2b03e1a8ee2aa6429dd396d002ce71e5d88b77551b2fb249cb382/%{srcname}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml

Requires:       python3

%description
This is a tool for managing a recorded version number in setuptools-based python projects.

%prep
%autosetup -n versioneer-%{version}

%build
%py3_build

%install
%py3_install

%check
python3 setup.py test

%files
%defattr(-,root,root,-)
%{_bindir}/versioneer
%{python3_sitelib}/*

%changelog
* Thu Feb 12 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.29-1
- Initial packaging for Photon
