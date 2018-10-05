%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Awesome Python HTTP Library That's Actually Usable
Name:           python-requests
Version:        2.19.1
Release:        2%{?dist}
License:        Apache2
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            http://python-requests.org
Source0:        http://pypi.python.org/packages/source/r/requests/requests-%{version}.tar.gz
%define sha1    requests=b6e6ed992c86835aa1a7d7a81fec2aee0d385416

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python-setuptools
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

#%check
#Commented out %check due to no test existence

%files
%defattr(-,root,root)
%doc README.rst HISTORY.rst LICENSE
%{python2_sitelib}/*

%files -n python3-requests
%defattr(-,root,root)
%doc README.rst HISTORY.rst LICENSE
%{python3_sitelib}/*

%changelog
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
