%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python3-iniparse
Version:        0.5
Release:        1%{?dist}
Summary:        Python Module for Accessing and Modifying Configuration Data in INI files
Group:          Development/Libraries
License:        MIT
URL:            http://code.google.com/p/iniparse/
Source0:        http://iniparse.googlecode.com/files/iniparse-%{version}.tar.gz
%define sha1 iniparse=eecb8fc113c4fc5930fea7eebf0eb796229c0ebc
Vendor:         VMware, Inc.
Distribution:   Photon

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-test
BuildRequires:  python3-devel
BuildRequires:  python3-six
BuildRequires:  python3-setuptools
Requires:       python3
Requires:       python3-libs
Requires:       python3-pycparser
Requires:       python3-six

%description
iniparse is an INI parser for Python which is API compatible
with the standard library's ConfigParser, preserves structure of INI
files (order of sections & options, indentation, comments, and blank
lines are preserved when data is updated), and is more convenient to
use.


%prep
%setup -q -n iniparse-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
# fixes
chmod 644 %{buildroot}/usr/share/doc/iniparse-%{version}/index.html
mv %{buildroot}/usr/share/doc/iniparse-%{version} %{buildroot}/usr/share/doc/python-iniparse-%{version}


%check
python3 runtests.py


%files
%defattr(-,root,root,-)
%doc  %{_docdir}/python-iniparse-%{version}/*
%{python3_sitelib}/*


%changelog
*   Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 0.5-1
-   Automatic Version Bump
*   Sat Jun 20 2020 Tapas Kundu <tkundu@vmware.com> 0.4-7
-   Mass removal python2
*   Tue Jul 11 2017 Xiaolin Li <xiaolinl@vmware.com> 0.4-6
-   Fix python3 and make check issues.
*   Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 0.4-5
-   Use python2 explicitly to build
*   Mon May 22 2017 Xiaolin Li <xiaolinl@vmware.com> 0.4-4
-   Added python3 subpackage.
*   Mon Oct 03 2016 ChangLee <changLee@vmware.com> 0.4-3
-   Modified %check
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.4-2
-   GA - Bump release of all rpms
*   Sat Jun 12 2010 Paramjit Oberoi <param@cs.wisc.edu> - 0.4-1
-   Release 0.4
*   Sat Apr 17 2010 Paramjit Oberoi <param@cs.wisc.edu> - 0.3.2-1
-   Release 0.3.2
*   Mon Mar 2 2009 Paramjit Oberoi <param@cs.wisc.edu> - 0.3.1-1
-   Release 0.3.1
*   Fri Feb 27 2009 Paramjit Oberoi <param@cs.wisc.edu> - 0.3.0-1
-   Release 0.3.0
*   Sat Dec 6 2008 Paramjit Oberoi <param@cs.wisc.edu> - 0.2.4-1
-   Release 0.2.4
-   added egg-info file to %%files
*   Tue Dec 11 2007 Paramjit Oberoi <param@cs.wisc.edu> - 0.2.3-1
-   Release 0.2.3
*   Mon Sep 24 2007 Paramjit Oberoi <param@cs.wisc.edu> - 0.2.2-1
-   Release 0.2.2
*   Tue Aug 7 2007 Paramjit Oberoi <param@cs.wisc.edu> - 0.2.1-1
-   Release 0.2.1
*   Fri Jul 27 2007 Tim Lauridsen <timlau@fedoraproject.org> - 0.2-3
-   relocated doc to %{_docdir}/python-iniparse-%{version}
*   Thu Jul 26 2007 Tim Lauridsen <timlau@fedoraproject.org> - 0.2-2
-   changed name from iniparse to python-iniparse
*   Tue Jul 17 2007 Tim Lauridsen <timlau@fedoraproject.org> - 0.2-1
-   Release 0.2
-   Added html/* to %%doc
*   Fri Jul 13 2007 Tim Lauridsen <timlau@fedoraproject.org> - 0.1-1
-   Initial build.
