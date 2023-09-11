Name:           python3-PyJWT
Version:        2.8.0
Release:        1%{?dist}
Summary:        JSON Web Token implementation in Python
License:        MIT
Group:          Development/Languages/Python
URL:            https://github.com/jpadilla/pyjwt
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/jpadilla/pyjwt/archive/refs/tags/PyJWT-2.8.0.tar.gz
%define sha512  PyJWT=9d631c20c5207d5ab3137c9d56825f9e197688181abae4f3d6aac766530a35e07a2dfd5e3ba6e530dd5a29a27f54e961cb01075f3bc831b73816aa7c357eb0d4

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
* Mon Sep 11 2023 Felippe Burkf <burkf@vmware.com> 2.8.0-1
- initial 3.0 package
