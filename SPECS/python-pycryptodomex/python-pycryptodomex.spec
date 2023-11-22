Summary:        Cryptographic library for Python
Name:           python3-pycryptodomex
Version:        3.9.9
Release:        2%{?dist}
License:        BSD and Public Domain
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.org/project/pycryptodomex
Source0:        pycryptodomex-%{version}.tar.gz
%define sha512 pycryptodomex=68a59cd537c1745db0082979716f0ba0508bb9d82d7129d42931056b5927f27ada1b92f88cc7c4d3954a02cd724a88c0e60fa38a5d8d7c73baa6541d332ff8a9

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:  python3-sphinx

Requires:  python3-sphinx
Requires:  python3-libs
Requires:  python3
Requires:  python3-setuptools

%description
Cryptographic library for Python

%prep
%autosetup -p1 -n pycryptodomex-%{version}

%build
%{py3_build}

%install
%{py3_install}

%check
python3 setup.py test

%files
%defattr(-,root,root,-)
%{python3_sitelib}/Cryptodome
%{python3_sitelib}/pycryptodomex-%{version}-py3.7.egg-info
%exclude %{python3_sitearch}/Cryptodome/SelfTest

%changelog
* Tue Nov 21 2023 Prashant S Chauhan <psingchauha@vmware.com> 3.9.9-2
- package SelfTest as separate package
* Tue Jan 19 2021 Tapas Kundu <tkundu@vmware.com> 3.9.9-1
- Initial packaging for Photon
