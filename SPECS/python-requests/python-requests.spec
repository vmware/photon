%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Awesome Python HTTP Library That's Actually Usable
Name:           python3-requests
Version:        2.24.0
Release:        1%{?dist}
License:        Apache2
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            http://python-requests.org
Source0:        http://pypi.python.org/packages/source/r/requests/requests-%{version}.tar.gz
%define sha1    requests=9144742bf54db5f2a74a3e724cec3c19431b3539
Patch0:         fix_makecheck.patch
%if %{with_check}
BuildRequires:  curl-devel
%endif
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
%if %{with_check}
BuildRequires:  python3-atomicwrites
BuildRequires:  python3-pytest
BuildRequires:  python3-attrs
BuildRequires:  python3-urllib3
BuildRequires:  python3-chardet
BuildRequires:  python3-certifi
BuildRequires:  python3-idna
%endif
Requires:       python3
Requires:       python3-libs
Requires:       python3-urllib3
Requires:       python3-chardet
Requires:       python3-pyOpenSSL
Requires:       python3-certifi
Requires:       python3-idna
BuildArch:      noarch

%description
Requests is an Apache2 Licensed HTTP library, written in Python, for human
beings.

Most existing Python modules for sending HTTP requests are extremely
verbose and cumbersome. Python's builtin urllib2 module provides most of
the HTTP capabilities you should need, but the api is thoroughly broken.
It requires an enormous amount of work (even method overrides) to
perform the simplest of tasks.

Features:

- Extremely simple GET, HEAD, POST, PUT, DELETE Requests
    + Simple HTTP Header Request Attachment
    + Simple Data/Params Request Attachment
    + Simple Multipart File Uploads
    + CookieJar Support
    + Redirection History
    + Redirection Recursion Urllib Fix
    + Auto Decompression of GZipped Content
    + Unicode URL Support
- Simple Authentication
    + Simple URL + HTTP Auth Registry

%prep
%setup -q -n requests-%{version}
%patch0 -p1

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check

easy_install_3=$(ls /usr/bin |grep easy_install |grep 3)
$easy_install_3 pathlib2 funcsigs pluggy more_itertools pysocks
$easy_install_3 pytest-mock pytest-httpbin
pytest3 -v -k "not test_https_warnings"

%files
%defattr(-,root,root)
%doc LICENSE
%{python3_sitelib}/*

%changelog
*   Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 2.24.0-1
-   Automatic Version Bump
*   Mon Jun 15 2020 Tapas Kundu <tkundu@vmware.com> 2.19.1-5
-   Mass removal python2
*   Thu Mar 28 2019 Tapas Kundu <tkundu@vmware.com> 2.19.1-4
-   Fix for CVE-2018-18074
*   Thu Dec 06 2018 Ashwin H <ashwinh@vmware.com> 2.19.1-3
-   Add %check
*   Thu Sep 27 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 2.19.1-2
-   Add a few missing runtime dependencies (urllib3, chardet,
-   pyOpenSSL, certifi, idna).
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 2.19.1-1
-   Update to version 2.19.1
*   Mon Aug 07 2017 Xiaolin Li <xiaolinl@vmware.com> 2.13.0-3
-   Disabled check section as tests are not available
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 2.13.0-2
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Thu Mar 23 2017 Xiaolin Li <xiaolinl@vmware.com> 2.13.0-1
-   Updated to version 2.13.0.
*   Wed Mar 01 2017 Xiaolin Li <xiaolinl@vmware.com> 2.9.1-4
-   Added python3 package.
*   Tue Oct 04 2016 ChangLee <changlee@vmware.com> 2.9.1-3
-   Modified %check
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.9.1-2
-   GA - Bump release of all rpms
*   Tue Feb 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 2.9.1-1
-   Updated to version 2.9.1
*   Wed Mar 04 2015 Mahmoud Bassiouny <mbassiouny@vmware.com>
-   Initial packaging for Photon
