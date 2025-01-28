Summary:        Internationalized Domain Names in Applications (IDNA).
Name:           python3-idna
Version:        2.10
Release:        3%{?dist}
Url:            https://pypi.python.org/pypi/idna
License:        BSD-like
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        idna-%{version}.tar.gz
%define sha512  idna=83b412de2f79a4bc86fb4bdac7252521b9d84f0be54f4fb1bde1ee13a210bbfa4b1a98247affbc7921046fb117a591316c12694c1be72865767646554c5207ac
Patch0:         CVE-2024-3651.patch

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
%autosetup -p1 -n idna-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
python3 setup.py test

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Tue Jan 28 2025 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 2.10-3
- Fix CVE-2024-3651
* Thu Dec 09 2021 Prashant S Chauhan <psinghchauha@vmware.com> 2.10-2
- Bump up to compile with python 3.10
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
