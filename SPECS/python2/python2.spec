Summary:	A high-level scripting language
Name:		python2
Version:	2.7.9
Release:	3%{?dist}
License:	PSF
URL:		http://www.python.org/
Group:		System Environment/Programming
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://www.python.org/ftp/python/2.7.9/Python-%{version}.tar.xz
%define sha1 Python=3172f6e957713c2d9fca462cc16068222fd1b9d3
Patch: cgi.patch
BuildRequires:	pkg-config >= 0.28
BuildRequires:	bzip2-devel
BuildRequires:  openssl-devel
Requires:	bzip2
Requires:  	openssl
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
Requires: python2 = %{version}-%{release}
Requires:	sqlite-autoconf
Requires:	expat >= 2.1.0
Requires:	libffi >= 3.0.13
Requires:	ncurses
Requires:	coreutils
BuildRequires:	expat >= 2.1.0
BuildRequires:	libffi >= 3.0.13
BuildRequires:	sqlite-autoconf
BuildRequires:	ncurses-devel

# Needed for ctypes, to load libraries, worked around for Live CDs size
# Requires: binutils

%description libs
The python interpreter can be embedded into applications wanting to 
use python as an embedded scripting language.  The python-libs package 
provides the libraries needed for this.

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
%patch -p1
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
#%exclude %{_libdir}/python2.7/unittest
%exclude %{_libdir}/python2.7/lib-dynload/_ctypes_test.so
%exclude %{_libdir}/python2.7/config
%exclude %{_libdir}/python2.7/config/*
%exclude %{_libdir}/libpython2.7.so

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
*	Fri Jun 19 2015 Alexey Makhalov <amakhalov@vmware.com> 2.7.9-3
-	Provide /bin/python
*	Wed Jun 3 2015 Divya Thaluru <dthaluru@vmware.com> 2.7.9-2
-	Adding coreutils package to run time required package
*	Mon Apr 6 2015 Divya Thaluru <dthaluru@vmware.com> 2.7.9-1
-	Initial build.	First version
