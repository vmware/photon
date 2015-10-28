Name:           python-Twisted
Version:        15.4.0
Release:        1%{?dist}
Url:            https://twistedmatrix.com
Summary:        An asynchronous networking framework written in Python
License:        MIT
Group:          Development/Languages/Python
Source0:        https://pypi.python.org/packages/source/T/Twisted/Twisted-%{version}.tar.bz2
%define sha1 Twisted=eb3607f58ac3d046fa38f513e15a68544f038c58

BuildRequires: python2
BuildRequires: python2-libs
BuildRequires: python2-devel
BuildRequires: python-setuptools

Requires:       python2
Requires:		python2-libs
requires:       python-zope.interface

BuildArch:      x86_64

%description
Twisted is an event-driven networking engine written in Python and licensed under the open source ​MIT license. Twisted runs on Python 2 and an ever growing subset also works with Python 3. 

Twisted also supports many common network protocols, including SMTP, POP3, IMAP, SSHv2, and DNS.

%prep
%setup -q -n Twisted-%{version}

%build
python setup.py build

%install
python setup.py install --prefix=%{_prefix} --root=%{buildroot}

%files
%defattr(-,root,root)
%{python_sitelib}/*
%{_bindir}/*

%changelog
* Tue Oct 27 2015 Mahmoud Bassiouny <mbassiouny@vmware.com>
- Initial packaging for Photon
