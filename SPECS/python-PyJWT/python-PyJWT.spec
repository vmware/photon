%global build_if %{photon_subrelease} >= 91

Name:           python3-PyJWT
Version:        2.8.0
Release:        5%{?dist}
Summary:        JSON Web Token implementation in Python
Group:          Development/Languages/Python
URL:            https://github.com/jpadilla/pyjwt
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/jpadilla/pyjwt/archive/refs/tags/PyJWT-2.8.0.tar.gz

Source1: license.txt
%include %{SOURCE1}

Patch0: CVE-2026-48523-1.patch
Patch1: CVE-2026-32597.patch
Patch2: pyjwt-cve-fixes.patch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
Requires:       python3
BuildArch:      noarch

%description
A Python implementation of JSON Web Token draft 01. This library provides a means of representing signed content using JSON data structures, including claims to be transferred between two parties encoded as digitally signed and encrypted JSON objects.

%prep
%autosetup -p1 -n pyjwt-%{version}

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
* Tue Aug 25 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 2.8.0-5
- Fix CVE-2026-32597, CVE-2026-48522, 48523, 48524, 48525, 48526
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 2.8.0-4
- Extended to build for subrelease 91 and above
* Wed Mar 18 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 2.8.0-3
- Bump version as a part of python3.14 upgrade
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 2.8.0-2
- Release bump for SRP compliance
* Mon Sep 11 2023 Felippe Burkf <burkf@vmware.com> 2.8.0-1
- update to 2.8.0
* Mon Nov 28 2022 Anmol Jain <anmolja@vmware.com> 2.6.0-1
- Initial Build
