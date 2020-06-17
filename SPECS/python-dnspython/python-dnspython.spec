%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        A DNS toolkit for Python
Name:           python3-dnspython
Version:        1.15.0
Release:        4%{?dist}
Url:            https://pypi.python.org/pypi/dnspython
License:        BSD
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://files.pythonhosted.org/packages/source/d/dnspython/dnspython-%{version}.zip
%define sha1    dnspython=2a3ffd70c0dbcac5ab60b582b5c53d202a938570
Patch0:         dnspython-test_zone-testToFileFilename.patch
BuildArch:      noarch

BuildRequires:  python3
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
%setup -q -n dnspython-%{version}
%patch0 -p1

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
*   Sat Jun 20 2020 Tapas Kundu <tkundu@vmware.com> 1.15.0-4
-   Mass removal python2
*   Wed Jul 12 2017 Xiaolin Li <xiaolinl@vmware.com> 1.15.0-3
-   Fix make check issues.
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 1.15.0-2
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Tue Apr 11 2017 Xiaolin Li <xiaolinl@vmware.com> 1.15.0-1
-   Initial packaging for Photon
