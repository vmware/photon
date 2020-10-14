%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Python NTP library
Name:           python3-ntplib
Version:        0.3.4
Release:        1%{?dist}
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/ntplib/
Source0:        ntplib-%{version}.tar.gz
%define         sha1 ntplib=08c3591bf257d893f455b833064e8be1889ec8bf

BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-incremental

Requires:       python3
Requires:       python3-libs

BuildArch:      noarch

%description
This module offers a simple interface to query NTP servers from Python.

It also provides utility functions to translate NTP fields values to text (mode, leap indicator…). Since it’s pure Python, and only depends on core modules, it should work on any platform with a Python implementation.


%prep
%setup -q -n ntplib-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

#%check
#Commented out %check due to no test existence

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Wed Oct 14 2020 Tapas Kundu <tkundu@vmware.com> 0.3.4-1
-   Update to 0.3.4
*   Fri Jun 19 2020 Tapas Kundu <tkundu@vmware.com> 0.3.3-3
-   Mass removal python2
*   Wed Jul 05 2017 Chang Lee <changlee@vmware.com> 0.3.3-2
-   Removed %check due to no test existence.
*   Mon Mar 06 2017 Xiaolin Li <xiaolinl@vmware.com> 0.3.3-1
-   Initial packaging for Photon.
