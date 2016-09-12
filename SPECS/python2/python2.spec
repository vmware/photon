Summary:	A high-level scripting language
Name:		python2
Version:	2.7.11
Release:	6%{?dist}
License:	PSF
URL:		http://www.python.org/
Group:		System Environment/Programming
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://www.python.org/ftp/python/2.7.11/Python-%{version}.tar.xz
%define sha1 Python=c3b8bbe3f084c4d4ea13ffb03d75a5e22f9756ff
Patch0: cgi.patch
Patch1: added-compiler-flags-for-curses-module.patch
Patch2: added-pyopenssl-ipaddress-certificate-validation.patch
BuildRequires:	pkg-config >= 0.28
BuildRequires:	bzip2-devel
BuildRequires:  openssl-devel
BuildRequires:	expat >= 2.1.0
BuildRequires:	libffi >= 3.0.13
BuildRequires:	sqlite-autoconf
BuildRequires:	ncurses-devel
BuildRequires:	readline-devel
Requires:	bzip2
Requires:  	openssl
Requires:	python2-libs = %{version}-%{release}
Provides: 	python-sqlite
Provides: 	python(abi)
Provides: 	/bin/python

%description
The Python 2 package contains the Python development environment. It 
is useful for object-oriented programming, writing scripts, 
prototyping large programs or developing entire applications. This 
version is for backward compatibility with other dependent packages.

%package libs
Summary: The libraries for python runtime
Group: Applications/System
Requires:	sqlite-autoconf
Requires:	expat >= 2.1.0
Requires:	libffi >= 3.0.13
Requires:	ncurses
Requires:	coreutils

# Needed for ctypes, to load libraries, worked around for Live CDs size
# Requires: binutils

%description libs
The python interpreter can be embedded into applications wanting to 
use python as an embedded scripting language.  The python-libs package 
provides the libraries needed for this.

%package -n python-xml
Summary: XML libraries for python runtime
Group: Applications/System
Requires: python2-libs = %{version}-%{release}

%description -n python-xml
The python-xml package provides the libraries needed for XML manipulation.

%package -n python-curses
Summary: Python module interface for NCurses Library 
Group: Applications/System
Requires: python2-libs = %{version}-%{release}
Requires: ncurses

%description -n python-curses
The python-curses package provides interface for ncurses library.

%package devel
Summary: The libraries and header files needed for Python development.
Group: Development/Libraries
Requires: python2 = %{version}-%{release}
# Needed here because of the migration of Makefile from -devel to the main
# package
Conflicts: python2 < %{version}-%{release}

%description devel
The Python programming language's interpreter can be extended with
dynamically loaded extensions and can be embedded in other programs.
This package contains the header files and libraries needed to do
these types of tasks.

Install python-devel if you want to develop Python extensions.  The
python package will also need to be installed.  You'll probably also
want to install the python-docs package, which contains Python
documentation.

%package tools
Summary: A collection of development tools included with Python.
Group: Development/Tools
Requires: python2 = %{version}-%{release}

%description tools
The Python package includes several development tools that are used
to build python programs.


%prep
%setup -q -n Python-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%build
export OPT="${CFLAGS}"
./configure \
	CFLAGS="%{optflags}" \
	CXXFLAGS="%{optflags}" \
	--prefix=%{_prefix} \
	--bindir=%{_bindir} \
	--libdir=%{_libdir} \
	--enable-shared \
	--with-ssl \
	--with-system-expat \
	--with-system-ffi \
	--enable-unicode=ucs4 \
	--with-dbmliborder=gdbm:ndbm
make %{?_smp_mflags}
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install
chmod -v 755 %{buildroot}%{_libdir}/libpython2.7.so.1.0
%{_fixperms} %{buildroot}/* 

# Remove unused stuff
find $RPM_BUILD_ROOT/ -name "*~"|xargs rm -f
find $RPM_BUILD_ROOT/ -name ".cvsignore"|xargs rm -f
find . -name "*~"|xargs rm -f
find . -name ".cvsignore"|xargs rm -f
#zero length
rm -f $RPM_BUILD_ROOT%{_libdir}/python2.7/site-packages/modulator/Templates/copyright
rm -f $RPM_BUILD_ROOT%{_libdir}/python2.7/LICENSE.txt

find %{buildroot}%{_libdir} -name '*.pyc' -delete
find %{buildroot}%{_libdir} -name '*.pyo' -delete

%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%clean
rm -rf %{buildroot}/*

%files 
%defattr(-, root, root)
%doc LICENSE README
%{_bindir}/pydoc*
%{_bindir}/python*
%{_mandir}/*/*

%dir %{_libdir}/python2.7
%dir %{_libdir}/python2.7/site-packages

%{_libdir}/libpython2.7.so.*
/usr/lib/pkgconfig/python-2.7.pc
/usr/lib/pkgconfig/python.pc
/usr/lib/pkgconfig/python2.pc

%exclude %{_libdir}/python2.7/bsddb/test
%exclude %{_libdir}/python2.7/ctypes/test
%exclude %{_libdir}/python2.7/distutils/tests
%exclude %{_libdir}/python2.7/email/test
%exclude %{_libdir}/python2.7/json/tests
%exclude %{_libdir}/python2.7/sqlite3/test
%exclude %{_libdir}/python2.7/idlelib/idle_test
%exclude %{_libdir}/python2.7/test
#%exclude %{_libdir}/python2.7/unittest
%exclude %{_libdir}/python2.7/lib-dynload/_ctypes_test.so


%files libs
%defattr(-,root,root)
%doc LICENSE README
/usr/lib/python2.7
%exclude %{_libdir}/python2.7/bsddb/test
%exclude %{_libdir}/python2.7/ctypes/test
%exclude %{_libdir}/python2.7/distutils/tests
%exclude %{_libdir}/python2.7/email/test
%exclude %{_libdir}/python2.7/json/tests
%exclude %{_libdir}/python2.7/sqlite3/test
%exclude %{_libdir}/python2.7/idlelib/idle_test
%exclude %{_libdir}/python2.7/test
%exclude %{_libdir}/python2.7/lib-dynload/_ctypes_test.so
%exclude %{_libdir}/python2.7/config
%exclude %{_libdir}/python2.7/config/*
%exclude %{_libdir}/libpython2.7.so
%exclude %{_libdir}/python2.7/xml
%exclude %{_libdir}/python2.7/lib-dynload/pyexpat.so

%files -n python-xml
%{_libdir}/python2.7/xml
%{_libdir}/python2.7/lib-dynload/pyexpat.so

%files -n python-curses
%{_libdir}/python2.7/curses
%{_libdir}/python2.7/lib-dynload/_curses*.so

%files devel
%defattr(-,root,root)
/usr/include/*
%doc Misc/README.valgrind Misc/valgrind-python.supp Misc/gdbinit
%dir %{_libdir}/python2.7/config
%{_libdir}/python2.7/config/*
%exclude %{_libdir}/python2.7/config/python.o
%{_libdir}/libpython2.7.so
%exclude %{_bindir}/smtpd*.py*
%exclude %{_bindir}/2to3*
%exclude %{_bindir}/idle*

%files tools
%defattr(-,root,root,755)
#%doc Tools/modulator/README.modulator
#%{_libdir}/python2.7/lib2to3
#%{_libdir}/python2.7/site-packages/modulator
%{_bindir}/smtpd*.py*
%{_bindir}/2to3*
%{_bindir}/idle*

%changelog
*   Wed Sep 7 2016 Divya Thaluru <dthaluru@vmware.com> 2.7.11-6
-   Added patch to python openssl to validate certificates by ipaddress 
*   Mon Jun 20 2016 Divya Thaluru <dthaluru@vmware.com> 2.7.11-5
-   Added stack-protector flag for ncurses module
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.7.11-4
-   GA - Bump release of all rpms
*   Tue Apr 26 2016 Nick Shi <nshi@vmware.com> 2.7.11-3
-   Adding readline module into python2-libs

*   Wed Apr 13 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.7.11-2
-   update python to require python-libs

*   Thu Jan 28 2016 Anish Swaminathan <anishs@vmware.com> 2.7.11-1
-   Upgrade version

*   Fri Jan 22 2016 Divya Thaluru <dthaluru@vmware.com> 2.7.9-5
-   Seperate python-curses package from python-libs package

*   Thu Oct 29 2015 Mahmoud Bassiouny <mbassiouny@vmware.com> 2.7.9-4
-   Seperate python-xml package from python-libs package

*   Fri Jun 19 2015 Alexey Makhalov <amakhalov@vmware.com> 2.7.9-3
-   Provide /bin/python

*   Wed Jun 3 2015 Divya Thaluru <dthaluru@vmware.com> 2.7.9-2
-   Adding coreutils package to run time required package

*   Mon Apr 6 2015 Divya Thaluru <dthaluru@vmware.com> 2.7.9-1
-   Initial build.	First version
