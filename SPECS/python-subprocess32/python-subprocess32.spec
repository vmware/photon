%define python2_ver %(python2 -c "import sys;print sys.version[0:3]")

Name:           python-subprocess32
Version:        3.5.2
Release:        2%{?dist}
Summary:        A backport of the subprocess module from Python 3.2/3.3 for use on 2.x
License:        PSF
Group:          Development/Languages/Python
Url:            https://pypi.python.org/pypi/subprocess32
Source0:        subprocess32-%{version}.tar.gz
%define sha1    subprocess32=d01a5a57c94a655992b6fc0172a6ab19f813bf70
Vendor:         VMware, Inc.
Distribution:   Photon

BuildRequires:  python2-devel
BuildRequires:  python2-libs
BuildRequires:  python-setuptools
BuildRequires:  python-pytest
%if %{with_check}
BuildRequires:  python2-test
%endif

Requires:       python2
Requires:       python2-libs
Requires:       python-setuptools

%description
A backport of the subprocess module from Python 3.2/3.3 for use on 2.x

%prep
%setup -n subprocess32-%{version}

%build
python2 setup.py build

%install
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
PYTHONPATH=build/lib.linux-%{_arch}-%{python2_ver}/ python2 test_subprocess32.py

%files
%defattr(-,root,root,-)
%{python_sitelib}/*

%changelog
*   Tue Jan 08 2019 Alexey Makhalov <amakhalov@vmware.com> 3.5.2-2
-   Added BuildRequires python2-devel
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 3.5.2-1
-   Update to version 3.5.2
*   Mon Sep 25 2017 Rui Gu <ruig@vmware.com> 3.2.7-2
-   Fix make check failure.
*   Fri Aug 25 2017 Vinay Kulkarni <kulkarniv@vmware.com> 3.2.7-1
-   Initial version of python-subprocess32 package for Photon.
