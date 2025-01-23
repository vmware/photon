%define srcname idna

Summary:        Internationalized Domain Names in Applications (IDNA).
Name:           python3-idna
Version:        3.3
Release:        4%{?dist}
Url:            https://pypi.python.org/pypi/idna
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        %{srcname}-%{version}.tar.gz
Patch0:         CVE-2024-3651.patch
%define sha512  %{srcname}=70b7cc8718e7d7899c75cfe476f044eae5a2fa03801fc9c12e3a092627ca943ffc4a578f9b8a55e181a11564835e125cfaaa577c02a6461dbb97366e620e53ad

Source1: license.txt
%include %{SOURCE1}

BuildArch:      noarch

BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3
Requires:       python3-libs

%description
Support for the Internationalised Domain Names in Applications (IDNA) protocol as specified in RFC 5891. This is the latest version of the protocol and is sometimes referred to as “IDNA 2008”.

This library also provides support for Unicode Technical Standard 46, Unicode IDNA Compatibility Processing.

This acts as a suitable replacement for the “encodings.idna” module that comes with the Python standard library, but only supports the old, deprecated IDNA specification (RFC 3490).

%prep
%autosetup -p1 -n %{srcname}-%{version}

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
* Thu Jan 23 2025 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 3.3-4
- Fix CVE-2024-3651
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 3.3-3
- Release bump for SRP compliance
* Fri Dec 02 2022 Prashant S Chauhan <psinghchauha@vmware.com> 3.3-2
- Update release to compile with python 3.11
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 3.3-1
- Automatic Version Bump
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 2.10-1
- Automatic Version Bump
* Fri Jun 19 2020 Tapas Kundu <tkundu@vmware.com> 2.7-2
- Mass removal python2
* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 2.7-1
- Update to version 2.7
* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 2.5-2
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
* Mon Mar 13 2017 Xiaolin Li <xiaolinl@vmware.com> 2.5-1
- Initial packaging for Photon
