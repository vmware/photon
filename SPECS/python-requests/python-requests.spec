%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Awesome Python HTTP Library That's Actually Usable
Name:           python-requests
Version:        2.19.1
Release:        3%{?dist}
License:        Apache2
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            http://python-requests.org
Source0:        http://pypi.python.org/packages/source/r/requests/requests-%{version}.tar.gz
Patch0:         make_check_add_pipfile.patch
%define sha1    requests=b6e6ed992c86835aa1a7d7a81fec2aee0d385416

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python-setuptools
%if %{with_check}
BuildRequires:  openssl-devel
BuildRequires:  curl-devel
BuildRequires:  python-atomicwrites
BuildRequires:  python-pytest
BuildRequires:  python-attrs
BuildRequires:  python-urllib3
BuildRequires:  python-chardet
BuildRequires:  python-certifi
BuildRequires:  python-idna
%endif
Requires:       python2
Requires:       python2-libs
Requires:       python-urllib3
Requires:       python-chardet
Requires:       python-pyOpenSSL
Requires:       python-certifi
Requires:       python-idna

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

%package -n     python3-requests
Summary:        python-requests
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

%description -n python3-requests
Python 3 version.

%prep
%setup -q -n requests-%{version}
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
easy_install_2=$(ls /usr/bin |grep easy_install |grep 2)
$easy_install_2 pathlib2 funcsigs pluggy more_itertools pysocks
$easy_install_2 pytest-mock pytest-httpbin
LANG=en_US.UTF-8  PYTHONPATH=%{buildroot}%{python2_sitelib} \
py.test2

easy_install_3=$(ls /usr/bin |grep easy_install |grep 3)
$easy_install_3 pathlib2 funcsigs pluggy more_itertools pysocks
$easy_install_3 pytest-mock pytest-httpbin
LANG=en_US.UTF-8  PYTHONPATH=%{buildroot}%{python3_sitelib} \
py.test3

%files
%defattr(-,root,root)
%doc README.rst HISTORY.rst LICENSE
%{python2_sitelib}/*

%files -n python3-requests
%defattr(-,root,root)
%doc README.rst HISTORY.rst LICENSE
%{python3_sitelib}/*

%changelog
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
*   Mon Oct 04 2016 ChangLee <changlee@vmware.com> 2.9.1-3
-   Modified %check
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.9.1-2
-   GA - Bump release of all rpms
*   Tue Feb 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 2.9.1-1
-   Updated to version 2.9.1
*   Wed Mar 04 2015 Mahmoud Bassiouny <mbassiouny@vmware.com>
-   Initial packaging for Photon
