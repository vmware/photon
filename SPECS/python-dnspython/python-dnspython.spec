%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        A DNS toolkit for Python
Name:           python-dnspython
Version:        1.15.0
Release:        3%{?dist}
URL:            https://pypi.python.org/pypi/dnspython
License:        BSD
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://files.pythonhosted.org/packages/source/d/dnspython/dnspython-%{version}.zip
%define sha1    dnspython=2a3ffd70c0dbcac5ab60b582b5c53d202a938570
Patch0:         dnspython-test_zone-testToFileFilename.patch
BuildArch:      noarch

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  unzip
Requires:       python2
Requires:       python2-libs

%description
dnspython is a DNS toolkit for Python. It supports almost all record types. It can be used for queries, zone transfers, and dynamic updates. It supports TSIG authenticated messages and EDNS0.

dnspython provides both high and low level access to DNS. The high level classes perform queries for data of a given name, type, and class, and return an answer set. The low level classes allow direct manipulation of DNS zones, messages, names, and records.

dnspython originated at Nominum where it was developed to facilitate the testing of DNS software. Nominum has generously allowed it to be open sourced under a BSD-style license.

%package -n     python3-dnspython
Summary:        python3-dnspython
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3
Requires:       python3-libs

%description -n python3-dnspython
Python 3 version.

%prep
%setup -q -n dnspython-%{version}
%patch0 -p1
rm -rf ../p3dir
cp -a . ../p3dir

%build
python2 setup.py build
pushd ../p3dir
python3 setup.py build
popd

%install
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}
pushd ../p3dir
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
popd

%check
python2 setup.py test
pushd ../p3dir
python3 setup.py test
popd

%files
%defattr(-,root,root)
%{python2_sitelib}/*

%files -n python3-dnspython
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Wed Jul 12 2017 Xiaolin Li <xiaolinl@vmware.com> 1.15.0-3
-   Fix make check issues.
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 1.15.0-2
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Tue Apr 11 2017 Xiaolin Li <xiaolinl@vmware.com> 1.15.0-1
-   Initial packaging for Photon
