%define srcname sphinxcontrib-htmlhelp

Name:           python3-sphinxcontrib-htmlhelp
Version:        2.0.0
Release:        3%{?dist}
Summary:        Sphinx extension for HTML help files
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
URL:            https://pypi.org/project/sphinxcontrib-htmlhelp
Distribution:   Photon

Source0: https://files.pythonhosted.org/packages/c9/2e/a7a5fef38327b7f643ed13646321d19903a2f54b0a05868e4bc34d729e1f/%{srcname}-%{version}.tar.gz
%define sha512 %{srcname}=6ed673966615f3e818e00de4b7e59c27f0a0d7b494294f804540777c580480870c36002c08d8ad626b7b41a676fe40edc0b0b5ffc6ad8080f38f59c24e157636

BuildArch: noarch

BuildRequires: python3-devel
BuildRequires: python3-setuptools

Requires: python3

Provides: python%{python3_version}dist(%{srcname})

%description
sphinxcontrib-htmlhelp is a sphinx extension which renders HTML help files.

%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
%{py3_build}

%install
%{py3_install}

%files
%defattr(-,root,root,-)
%license LICENSE
%doc README.rst
%{python3_sitelib}/*

%changelog
* Sun Aug 20 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.0.0-3
- Fix summary & description
* Mon Oct 31 2022 Prashant S Chauhan <psinghchauha@vmware.com> 2.0.0-2
- Update release to compile with python 3.11
* Mon Sep 05 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.0.0-1
- Upgrade to v2.0.0
* Mon Dec 14 2020 Shreenidhi Shedi <sshedi@vmware.com> 1.0.3-1
- initial version
