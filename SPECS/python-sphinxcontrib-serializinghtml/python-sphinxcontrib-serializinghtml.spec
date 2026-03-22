%global build_if %{photon_subrelease} >= 92

%define srcname sphinxcontrib_serializinghtml

Name:           python3-sphinxcontrib-serializinghtml
Version:        2.0.0
Release:        1%{?dist}
Summary:        Sphinx extension for serialized HTML
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://pypi.org/project/sphinxcontrib-serializinghtml

Source0: %{srcname}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildArch: noarch

BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-pip
BuildRequires: python3-flit-core

Requires: python3

Provides: python%{python3_version}dist(%{srcname})

%description
sphinxcontrib-serializinghtml is a sphinx extension which outputs "serialized"
HTML files (json and pickle).

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
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.1.5-3
- Release bump for SRP compliance
* Sun Aug 20 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.1.5-2
- Fix summary & description
* Mon Sep 05 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.1.5-1
- Upgrade to v1.1.5
* Mon Dec 14 2020 Shreenidhi Shedi <sshedi@vmware.com> 1.1.4-1
- initial version
