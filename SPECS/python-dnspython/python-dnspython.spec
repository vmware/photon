Summary:        A DNS toolkit for Python
Name:           python3-dnspython
Version:        2.6.1
Release:        1%{?dist}
Url:            https://pypi.python.org/pypi/dnspython
License:        BSD
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://files.pythonhosted.org/packages/source/d/dnspython/dnspython-%{version}.tar.gz
%define sha512  dnspython=0a2950b320e3963b0f76a80575b4387b2a92201a3e0a279900f81e353fbc8810f2b8aab8ad680d01e1a7e079c4e37292e103ab8db860ba646451593541067fbb
BuildArch:      noarch

BuildRequires:  python3-libs
BuildRequires:  python3-devel
BuildRequires:  python3-wheel
BuildRequires:  python3-packaging
BuildRequires:  python3-pathspec
BuildRequires:  python3-pluggy
BuildRequires:  python3-hatchling
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  unzip
BuildRequires:  python3-setuptools_scm
Requires:       python3
Requires:       python3-libs

%description
dnspython is a DNS toolkit for Python. It supports almost all record types. It can be used for queries, zone transfers, and dynamic updates. It supports TSIG authenticated messages and EDNS0.

dnspython provides both high and low level access to DNS. The high level classes perform queries for data of a given name, type, and class, and return an answer set. The low level classes allow direct manipulation of DNS zones, messages, names, and records.

dnspython originated at Nominum where it was developed to facilitate the testing of DNS software. Nominum has generously allowed it to be open sourced under a BSD-style license.

%prep
%autosetup -n dnspython-%{version}

%build
%pyproject_wheel

%install
%pyproject_install

%check
python3 setup.py test

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Mon Jun 24 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 2.6.1-1
- Update to 2.6.1, fixes CVE-2023-29483
* Mon Jun 03 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 2.2.1-2
- Use system provided packages to do offline build
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 2.2.1-1
- Automatic Version Bump
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 2.0.0-1
- Automatic Version Bump
* Sat Jun 20 2020 Tapas Kundu <tkundu@vmware.com> 1.15.0-4
- Mass removal python2
* Wed Jul 12 2017 Xiaolin Li <xiaolinl@vmware.com> 1.15.0-3
- Fix make check issues.
* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 1.15.0-2
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
* Tue Apr 11 2017 Xiaolin Li <xiaolinl@vmware.com> 1.15.0-1
- Initial packaging for Photon
