%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           python-iniparse
Version:        0.4
Release:        2%{?dist}
Summary:        Python Module for Accessing and Modifying Configuration Data in INI files
Group:          Development/Libraries
License:        MIT
URL:            http://code.google.com/p/iniparse/
Source0:        http://iniparse.googlecode.com/files/iniparse-%{version}.tar.gz
%define sha1 iniparse=2b2af8a19f3e5c212c27d7c524cd748fa0b38650
Vendor:		VMware, Inc.
Distribution:	Photon
BuildRequires:	python2-devel
BuildRequires:	python2-libs
BuildArch:	noarch
Requires:	python2

%description
iniparse is an INI parser for Python which is API compatible
with the standard library's ConfigParser, preserves structure of INI
files (order of sections & options, indentation, comments, and blank
lines are preserved when data is updated), and is more convenient to
use.

%prep
%setup -q -n iniparse-%{version}


%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
# fixes
chmod 644 $RPM_BUILD_ROOT//usr/share/doc/iniparse-%{version}/index.html
mv $RPM_BUILD_ROOT/usr/share/doc/iniparse-%{version} $RPM_BUILD_ROOT/usr/share/doc/python-iniparse-%{version}

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc  %{_docdir}/python-iniparse-%{version}/*
%{python_sitelib}/iniparse
%{python_sitelib}/iniparse-%{version}-py*.egg-info



%changelog
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.4-2
-	GA - Bump release of all rpms
* Sat Jun 12 2010 Paramjit Oberoi <param@cs.wisc.edu> - 0.4-1
- Release 0.4
* Sat Apr 17 2010 Paramjit Oberoi <param@cs.wisc.edu> - 0.3.2-1
- Release 0.3.2
* Mon Mar 2 2009 Paramjit Oberoi <param@cs.wisc.edu> - 0.3.1-1
- Release 0.3.1
* Fri Feb 27 2009 Paramjit Oberoi <param@cs.wisc.edu> - 0.3.0-1
- Release 0.3.0
* Sat Dec 6 2008 Paramjit Oberoi <param@cs.wisc.edu> - 0.2.4-1
- Release 0.2.4
- added egg-info file to %%files
* Tue Dec 11 2007 Paramjit Oberoi <param@cs.wisc.edu> - 0.2.3-1
- Release 0.2.3
* Mon Sep 24 2007 Paramjit Oberoi <param@cs.wisc.edu> - 0.2.2-1
- Release 0.2.2
* Tue Aug 7 2007 Paramjit Oberoi <param@cs.wisc.edu> - 0.2.1-1
- Release 0.2.1
* Fri Jul 27 2007 Tim Lauridsen <timlau@fedoraproject.org> - 0.2-3
- relocated doc to %{_docdir}/python-iniparse-%{version}
* Thu Jul 26 2007 Tim Lauridsen <timlau@fedoraproject.org> - 0.2-2
- changed name from iniparse to python-iniparse
* Tue Jul 17 2007 Tim Lauridsen <timlau@fedoraproject.org> - 0.2-1
- Release 0.2
- Added html/* to %%doc
* Fri Jul 13 2007 Tim Lauridsen <timlau@fedoraproject.org> - 0.1-1
- Initial build.
