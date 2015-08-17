Summary:	A high-level scripting language
Name:		python3
Version:	3.4.3
Release:	2%{?dist}
License:	PSF
URL:		http://www.python.org/
Group:		System Environment/Programming
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	https://www.python.org/ftp/python/%{version}/Python-%{version}.tar.xz
%define sha1 Python=7ca5cd664598bea96eec105aa6453223bb6b4456
Patch:          cgi3.patch
BuildRequires:	pkg-config >= 0.28
BuildRequires:	bzip2-devel
BuildRequires:	ncurses-devel
BuildRequires:  openssl-devel
BuildRequires:  readline-devel
BuildRequires:  xz-devel
Requires:	bzip2
Requires:	ncurses
Requires:  	openssl
Requires:  	readline
Requires:  	xz
Provides: 	python-sqlite
Provides: 	python(abi)
Provides: 	/usr/bin/python
Provides: 	/bin/python

%description
The Python 3 package contains a new version of Python development environment.
Python 3 brings more efficient ways of handling dictionaries, better unicode
strings support, easier and more intuitive syntax, and removes the deprecated
code. It is incompatible with Python 2.x releases.

%package libs
Summary: The libraries for python runtime
Group: Applications/System
Requires: python3 = %{version}-%{release}
BuildRequires:	expat >= 2.1.0
BuildRequires:	libffi >= 3.0.13
BuildRequires:	ncurses-devel
BuildRequires:	sqlite-autoconf
Requires:	coreutils
Requires:	expat >= 2.1.0
Requires:	libffi >= 3.0.13
Requires:	ncurses
Requires:	sqlite-autoconf


%description libs
The python interpreter can be embedded into applications wanting to
use python as an embedded scripting language.  The python-libs package
provides the libraries needed for python 3 applications.

%package devel
Summary: The libraries and header files needed for Python development.
Group: Development/Libraries
Requires: python3 = %{version}-%{release}
# Needed here because of the migration of Makefile from -devel to the main
# package
Conflicts: python3 < %{version}-%{release}

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
Requires: python3 = %{version}-%{release}

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
	--with-system-expat \
	--with-system-ffi \
	--with-dbmliborder=gdbm:ndbm
make %{?_smp_mflags}

%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} altinstall
chmod -v 755 %{buildroot}%{_libdir}/libpython3.4m.so.1.0
%{_fixperms} %{buildroot}/*

# Remove unused stuff
find %{buildroot}%{_libdir} -name '*.pyc' -delete
find %{buildroot}%{_libdir} -name '*.pyo' -delete
find %{buildroot}%{_libdir} -name '*.o' -delete

%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%post
-p /sbin/ldconfig
# Enable below if using 'make install' instead of 'make altinstall'
#ln -s %{_bindir}/python3 %{_bindir}/python
#ln -s %{_bindir}/python3-config %{_bindir}/python-config
#ln -s %{_libdir}/libpython3.4m.so %{_libdir}/libpython3.4.so

%postun
-p /sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%defattr(-, root, root)
%doc LICENSE README
%{_bindir}/pydoc*
%{_bindir}/pyvenv*
%{_bindir}/python*
%{_bindir}/pip*
%{_bindir}/easy_install-3.4
%{_mandir}/*/*

%dir %{_libdir}/python3.4
%dir %{_libdir}/python3.4/site-packages

%{_libdir}/libpython3.so
%{_libdir}/libpython3.4m.so
%{_libdir}/libpython3.4m.so.1.0
%{_libdir}/pkgconfig/python-3.4.pc
# Enable below if using 'make install' instead of 'make altinstall'
#%{_libdir}/pkgconfig/python-3.4m.pc
#%{_libdir}/pkgconfig/python3.pc

%exclude %{_libdir}/python3.4/ctypes/test
%exclude %{_libdir}/python3.4/distutils/tests
%exclude %{_libdir}/python3.4/sqlite3/test
%exclude %{_libdir}/python3.4/idlelib/idle_test
%exclude %{_libdir}/python3.4/test
%exclude %{_libdir}/python3.4/lib-dynload/_ctypes_test.*.so

%files libs
%defattr(-,root,root)
%doc LICENSE README
%{_libdir}/python3.4
%exclude %{_libdir}/python3.4/ctypes/test
%exclude %{_libdir}/python3.4/distutils/tests
%exclude %{_libdir}/python3.4/sqlite3/test
%exclude %{_libdir}/python3.4/idlelib/idle_test
%exclude %{_libdir}/python3.4/test
%exclude %{_libdir}/python3.4/lib-dynload/_ctypes_test.*.so

%files devel
%defattr(-,root,root)
%{_includedir}/*

%doc Misc/README.valgrind Misc/valgrind-python.supp Misc/gdbinit
%{_libdir}/libpython3.so
%exclude %{_bindir}/2to3*
%exclude %{_bindir}/idle*

%files tools
%defattr(-,root,root,755)
%doc Tools/README
%{_libdir}/python3.4/lib2to3
%{_bindir}/2to3*
%{_bindir}/idle*

%changelog
*	Wed Aug 17 2015 Vinay Kulkarni <kulkarniv@vmware.com> 3.4.3-2
-	Remove python.o file, and minor cleanups.
*	Wed Jul 1 2015 Vinay Kulkarni <kulkarniv@vmware.com> 3.4.3
-	Add Python3 package to Photon.
