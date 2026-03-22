%global build_if %{photon_subrelease} >= 92

%define srcname sphinxcontrib_htmlhelp

Name:           python3-sphinxcontrib-htmlhelp
Version:        2.1.0
Release:        1%{?dist}
Summary:        Sphinx extension for HTML help files
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
URL:            https://pypi.org/project/sphinxcontrib-htmlhelp
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
sphinxcontrib-htmlhelp is a sphinx extension which renders HTML help files.

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
* Sun Mar 22 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.1.0-1
- Version upgrade
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 2.0.0-4
- Release bump for SRP compliance
* Sun Aug 20 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.0.0-3
- Fix summary & description
* Mon Oct 31 2022 Prashant S Chauhan <psinghchauha@vmware.com> 2.0.0-2
- Update release to compile with python 3.11
* Mon Sep 05 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.0.0-1
- Upgrade to v2.0.0
* Mon Dec 14 2020 Shreenidhi Shedi <sshedi@vmware.com> 1.0.3-1
- initial version
