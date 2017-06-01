%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        An asynchronous networking framework written in Python
Name:           python-Twisted
Version:        17.1.0
Release:        6%{?dist}
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://twistedmatrix.com
Source0:        https://files.pythonhosted.org/packages/source/T/Twisted/Twisted-%{version}.tar.bz2
%define         sha1 Twisted=1cd9e3e39323f555a89d882cbbcf001015bd3113

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-incremental
BuildRequires:  python-zope.interface

Requires:       python2
Requires:       python2-libs
Requires:       python-zope.interface
Requires:       python-netaddr
Requires:       python-incremental
Requires:       python-constantly

BuildArch:      x86_64

%description
Twisted is an event-driven networking engine written in Python and licensed under the open source ​MIT license. Twisted runs on Python 2 and an ever growing subset also works with Python 3. 

Twisted also supports many common network protocols, including SMTP, POP3, IMAP, SSHv2, and DNS.

%package -n     python3-Twisted
Summary:        python-Twisted
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-incremental
BuildRequires:  python3-zope.interface

Requires:       python3
Requires:       python3-libs
Requires:       python3-zope.interface
Requires:       python3-netaddr
Requires:       python3-incremental
Requires:       python3-constantly

%description -n python3-Twisted
Python 3 version.

%prep
%setup -q -n Twisted-%{version}
rm -rf ../p3dir
cp -a . ../p3dir

%build
python2 setup.py build
pushd ../p3dir
python3 setup.py build
popd

%install
pushd ../p3dir
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
popd
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%files
%defattr(-,root,root)
%{python2_sitelib}/*
%{_bindir}/*

%files -n python3-Twisted
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
*   Thu Jun 01 2017 Xiaolin Li <rqiu@vmware.com> 17.1.0-6
-   Keep python2 scrips in bin folder.
*   Mon May 22 2017 Rongrong Qiu <rqiu@vmware.com> 17.1.0-5
-   Added python-constantly to the requires.
*   Mon Mar 27 2017 Xiaolin Li <xiaolinl@vmware.com> 17.1.0-4
-   Added python-netaddr and python-incremental to the requires.
*   Mon Mar 20 2017 Xiaolin Li <xiaolinl@vmware.com> 17.1.0-3
-   Upgraded to 17.1.0.
*   Tue Mar 15 2017 Xiaolin Li <xiaolinl@vmware.com> 16.6.0-1
-   Downgraded to 16.6.0
*   Tue Mar 14 2017 Anish Swaminathan <anishs@vmware.com> 17.1.0-2
-   Change requires
*   Wed Mar 01 2017 Xiaolin Li <xiaolinl@vmware.com> 17.1.0-1
-   Added python3 package and updated to version 17.1.0.
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 15.5.0-2
-   GA - Bump release of all rpms
*   Thu Jan 21 2016 Anish Swaminathan <anishs@vmware.com> 15.5.0-1
-   Upgrade version
*   Tue Oct 27 2015 Mahmoud Bassiouny <mbassiouny@vmware.com>
-   Initial packaging for Photon
