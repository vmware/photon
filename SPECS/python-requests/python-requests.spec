Name:           python-requests
Version:        2.9.1
Release:        2%{?dist}
Url:            http://python-requests.org
Summary:        Awesome Python HTTP Library That's Actually Usable
License:        Apache2
Group:          Development/Languages/Python
Source0:        http://pypi.python.org/packages/source/r/requests/requests-%{version}.tar.gz
%define sha1 requests=17f01c47a0d7c676f6291608ef2f43db3fa74095

BuildRequires: python2
BuildRequires: python2-libs
BuildRequires: python-setuptools

Requires:       python2
Requires:		python2-libs

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

%build
python setup.py build

%install
python setup.py install --prefix=%{_prefix} --root=%{buildroot}

%files
%defattr(-,root,root)
%doc README.rst HISTORY.rst LICENSE NOTICE
%{python_sitelib}/*

%changelog
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com>         2.9.1-2
-	GA - Bump release of all rpms
* Tue Feb 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 2.9.1-1
- Updated to version 2.9.1
* Wed Mar 04 2015 Mahmoud Bassiouny <mbassiouny@vmware.com>
- Initial packaging for Photon
