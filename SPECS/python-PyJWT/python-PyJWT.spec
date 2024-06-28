Name:           python3-PyJWT
Version:        2.6.0
Release:        1%{?dist}
Summary:        JSON Web Token implementation in Python
License:        MIT
Group:          Development/Languages/Python
URL:            https://github.com/jpadilla/pyjwt
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/jpadilla/pyjwt/archive/refs/tags/PyJWT-2.6.0.tar.gz
%define sha512  PyJWT=7b3d2aa5a12f51fb6b1137f939cfe6a08519b4d5b83f2c058dc31741e3ec6d7011844c7b426aa44aacf6570f3907a027ca1fe989a0c232e285e158a217f95557

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
Requires:       python3
BuildArch:      noarch

%description
A Python implementation of JSON Web Token draft 01. This library provides a means of representing signed content using JSON data structures, including claims to be transferred between two parties encoded as digitally signed and encrypted JSON objects.

%prep
%autosetup -n pyjwt-%{version}

%build
%py3_build

%install
%py3_install

%check
%pytest

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*
%doc README.rst

%changelog
* Mon Nov 28 2022 Anmol Jain <anmolja@vmware.com> 2.6.0-1
- Initial Build
