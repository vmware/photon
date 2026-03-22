%global build_if %{photon_subrelease} >= 92

%define srcname sphinxcontrib_qthelp

Name:           python3-sphinxcontrib-qthelp
Version:        2.0.0
Release:        1%{?dist}
Summary:        Sphinx extension for QtHelp documents
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
URL:            https://pypi.org/project/sphinxcontrib-qthelp
Distribution:   Photon

BuildArch: noarch

Source0: %{srcname}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-pip
BuildRequires: python3-flit-core

Requires: python3

Provides: python%{python3_version}dist(%{srcname})

%description
sphinxcontrib-qthelp is a sphinx extension which outputs QtHelp document.

%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Sun Mar 22 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.0.0-1
- Version upgrade
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.0.3-4
- Release bump for SRP compliance
* Sun Aug 20 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.0.3-3
- Fix summary & description
* Fri Dec 02 2022 Prashant S Chauhan <psinghchauha@vmware.com> 1.0.3-2
- Update release to compile with python 3.11
* Mon Dec 14 2020 Shreenidhi Shedi <sshedi@vmware.com> 1.0.3-1
- initial version
