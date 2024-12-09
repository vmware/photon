Summary:        Fast javascript parser (based on esprima.js).
Name:           python3-pyjsparser
Version:        2.7.1
Release:        4%{?dist}
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/pyjsparser/2.5.2

Source0:        https://files.pythonhosted.org/packages/source/p/pyjsparser/pyjsparser-%{version}.tar.gz
%define         sha512 pyjsparser=811faf1d1fcae363417931e095bf108b27ec8762a12048b658215ecdecc1fd1bbb183f2ec35199ce67e7837aeda6ccf27b6f4bbd62b19fe6a5c9ba6fa7615031

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-six

Requires:       python3
Requires:       python3-libs

BuildArch:      noarch

%description
Fast javascript parser (based on esprima.js).

%prep
%autosetup -p1 -n pyjsparser-%{version}

%build
%py3_build

%install
%py3_install

#%%check
#This package does not come with a test suite.

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 2.7.1-4
- Release bump for SRP compliance
* Fri Dec 02 2022 Prashant S Chauhan <psinghchauha@vmware.com> 2.7.1-3
- Update release to compile with python 3.11
* Fri Jun 19 2020 Tapas Kundu <tkundu@vmware.com> 2.7.1-2
- Mass removal python2
* Sun Nov 10 2019 Tapas Kundu <tkundu@vmware.com> 2.7.1-1
- Update to 2.7.1
* Mon Sep 11 2017 Xiaolin Li <xiaolinl@vmware.com> 2.5.2-1
- Initial packaging for Photon
