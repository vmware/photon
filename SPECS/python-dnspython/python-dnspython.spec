Summary:        A DNS toolkit for Python
Name:           python3-dnspython
Version:        2.0.0
Release:        3%{?dist}
Url:            https://pypi.python.org/pypi/dnspython
License:        BSD
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://files.pythonhosted.org/packages/source/d/dnspython/dnspython-%{version}.zip
%define sha512 dnspython=5dd135c9e550c9b50128c6eec31de63fd993efb24097394f29f93d1f99ca509c514c7a46eefd6336503727f43a6358f775046f442ea60cc9647c1451490bcd87
Patch0:         CVE-2023-29483.patch
BuildArch:      noarch

BuildRequires:  python3-libs
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  unzip
Requires:       python3
Requires:       python3-libs

%description
dnspython is a DNS toolkit for Python. It supports almost all record types. It can be used for queries, zone transfers, and dynamic updates. It supports TSIG authenticated messages and EDNS0.

dnspython provides both high and low level access to DNS. The high level classes perform queries for data of a given name, type, and class, and return an answer set. The low level classes allow direct manipulation of DNS zones, messages, names, and records.

dnspython originated at Nominum where it was developed to facilitate the testing of DNS software. Nominum has generously allowed it to be open sourced under a BSD-style license.

%prep
%autosetup -p1 -n dnspython-%{version}

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
* Fri May 17 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 2.0.0-3
- Fix CVE-2023-29483
* Thu Dec 09 2021 Prashant S Chauhan <psinghchauha@vmware.com> 2.0.0-2
- Bump up to compile with python 3.10
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
