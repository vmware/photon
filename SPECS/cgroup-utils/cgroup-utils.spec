%{!?python3_sitelib: %global python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
Summary:        Utility tools for control groups of Linux
Name:           cgroup-utils
Version:        0.8
Release:        2%{?dist}
License:        GPLv2
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://pypi.python.org/pypi/cgroup-utils/0.6
Source0:        https://github.com/peo3/cgroup-utils/archive/%{name}-%{version}.tar.gz
%define sha1    cgroup-utils=33c50a033dbcc8f490850a368a41d6348def9114

Patch0:         cgutil-support-space-in-procname.patch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3
Requires:       python3-curses

%description
cgroup-utils provides utility tools and libraries for control groups of Linux. For example,
cgutil top is a top-like tool which shows activities of running processes in control groups.

%prep
%setup -q
%patch0 -p1

%build
python3 setup.py build

%install
python3 setup.py install --single-version-externally-managed -O1 --root=%{buildroot}

%check
python3 test_all.py

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}/cgutil
%{python3_sitelib}/*

%changelog
*   Tue Jul 14 2020 Tapas Kundu <tkundu@vmware.com> 0.8-2
-   Mass removal python2
*   Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 0.8-1
-   Automatic Version Bump
*   Fri Aug 11 2017 Rongrong Qiu <rqiu@vmware.com> 0.6-6
-   fix make check for bug 1900249
*   Tue Jun 13 2017 Xiaolin Li <xiaolinl@vmware.com> 0.6-5
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Fri Jun 09 2017 Xiaolin Li <xiaolinl@vmware.com> 0.6-4
-   Support space in proc name.
*   Tue May 23 2017 Xiaolin Li <xiaolinl@vmware.com> 0.6-3
-   Added python3 subpackage.
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.6-2
-   GA - Bump release of all rpms
*   Wed Jan 6 2016 Xiaolin Li <xiaolinl@vmware.com> 0.6-1
-   Initial build.  First version
