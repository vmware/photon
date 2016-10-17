Name:           python-Twisted
Version:        15.5.0
Release:        3%{?dist}
Url:            https://twistedmatrix.com
Summary:        An asynchronous networking framework written in Python
License:        MIT
Group:          Development/Languages/Python
Source0:        https://pypi.python.org/packages/source/T/Twisted/Twisted-%{version}.tar.bz2
%define sha1 Twisted=c7db4b949fc27794ca94677f66082f49be43f283

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

%check
easy_install tox
tox -e py27-tests

%files
%defattr(-,root,root)
%{python_sitelib}/*
%{_bindir}/*

%changelog
*       Mon Oct 10 2016 ChangLee <changlee@vmware.com> 15.5.0-3
-       Modified %check
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 15.5.0-2
-	GA - Bump release of all rpms
*	Thu Jan 21 2016 Anish Swaminathan <anishs@vmware.com> 15.5.0-1
-	Upgrade version
* 	Tue Oct 27 2015 Mahmoud Bassiouny <mbassiouny@vmware.com>
- 	Initial packaging for Photon
