Name:           python3-PyJWT
Version:        2.8.0
Release:        2%{?dist}
Summary:        JSON Web Token implementation in Python
Group:          Development/Languages/Python
URL:            https://github.com/jpadilla/pyjwt
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/jpadilla/pyjwt/archive/refs/tags/PyJWT-2.8.0.tar.gz

Source1: license.txt
%include %{SOURCE1}

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
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 2.8.0-2
- Release bump for SRP compliance
* Mon Sep 11 2023 Felippe Burkf <burkf@vmware.com> 2.8.0-1
- update to 2.8.0
* Mon Nov 28 2022 Anmol Jain <anmolja@vmware.com> 2.6.0-1
- Initial Build
