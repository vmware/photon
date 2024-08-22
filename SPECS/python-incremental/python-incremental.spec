Summary:        Incremental is a small library that versions your Python projects.
Name:           python3-incremental
Version:        21.3.0
Release:        1%{?dist}
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/incremental
Source0:        incremental-%{version}.tar.gz
%define sha512  incremental=b8b50151cd2467e552d9268decadbb839b047cf58a450b72e0437ffc5f9af7d78c20a24193c0668cf48dd6264b852d9cee68e59529018e0ca07825e0c185d1e8

BuildRequires:  python3-libs
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3
Requires:       python3-libs

BuildArch:      noarch

%description
Incremental is a small library that versions your Python projects.

%prep
%autosetup -n incremental-%{version}

%build
%py3_build

%install
%py3_install

%check
python3 setup.py test

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Mon Aug 26 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 21.3.0-1
- Update to 21.3.0 as part of python3-Twisted update
* Thu Dec 09 2021 Prashant S Chauhan <psinghchauha@vmware.com> 17.5.0-3
- Bump up to compile with python 3.10
* Fri Jun 19 2020 Tapas Kundu <tkundu@vmware.com> 17.5.0-2
- Mass removal python2
* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 17.5.0-1
- Update to version 17.5.0
* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 16.10.1-2
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
* Mon Mar 06 2017 Xiaolin Li <xiaolinl@vmware.com> 16.10.1-1
- Initial packaging for Photon.
