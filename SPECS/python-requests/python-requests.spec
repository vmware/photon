%{!?python_sitelib: %define python_sitelib %(python -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Awesome Python HTTP Library That's Actually Usable
Name:           python-requests
Version:        2.13.0
Release:        2%{?dist}
License:        Apache2
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            http://python-requests.org
Source0:        http://pypi.python.org/packages/source/r/requests/requests-%{version}.tar.gz
%define sha1    requests=827f7c8abb5a57d980d9870908724613b8b120c1
Patch0:         CVE-2018-18074.patch
BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python-setuptools

Requires:       python2
Requires:       python2-libs

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

Requires:       python3
Requires:       python3-libs
%description -n python3-requests
Python 3 version.

%prep
%setup -q -n requests-%{version}
%patch0 -p1

%build
python setup.py build
python3 setup.py build

%install
python setup.py install --prefix=%{_prefix} --root=%{buildroot}
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%files
%defattr(-,root,root)
%doc README.rst HISTORY.rst LICENSE NOTICE
%{python_sitelib}/*

%files -n python3-requests
%defattr(-,root,root)
%doc README.rst HISTORY.rst LICENSE NOTICE
%{python3_sitelib}/*

%changelog
*   Thu Mar 28 2019 Tapas Kundu <tkundu@vmware.com> 2.13.0-2
-   Fix for CVE-2018-18074
*   Mon Mar 13 2017 Xiaolin Li <xiaolinl@vmware.com> 2.13.0-1
-   Updated to version 2.13.0.
*   Wed Mar 01 2017 Xiaolin Li <xiaolinl@vmware.com> 2.9.1-3
-   Added python3 package.
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.9.1-2
-   GA - Bump release of all rpms
*   Tue Feb 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 2.9.1-1
-   Updated to version 2.9.1
*   Wed Mar 04 2015 Mahmoud Bassiouny <mbassiouny@vmware.com>
-   Initial packaging for Photon
