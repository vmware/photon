Summary:        A high-level scripting language
Name:           python3
Version:        3.6.1
Release:        1%{?dist}
License:        PSF
URL:            http://www.python.org/
Group:          System Environment/Programming
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://www.python.org/ftp/python/%{version}/Python-%{version}.tar.xz
%define sha1    Python=91d880a2a9fcfc6753cbfa132bf47a47e17e7b16
Patch0:         cgi3.patch
Patch2:         python3-support-photon-platform.patch
BuildRequires:  pkg-config >= 0.28
BuildRequires:  bzip2-devel
BuildRequires:  ncurses-devel
BuildRequires:  openssl-devel
BuildRequires:  readline-devel
BuildRequires:  xz-devel
Requires:       bzip2
Requires:       ncurses
Requires:       openssl
Requires:       python3-libs = %{version}-%{release}
Requires:       readline
Requires:       xz
Provides:       python-sqlite
Provides:       python(abi)
Provides:       /usr/bin/python
Provides:       /bin/python
Provides:       /bin/python3

%description
The Python 3 package contains a new version of Python development environment.
Python 3 brings more efficient ways of handling dictionaries, better unicode
strings support, easier and more intuitive syntax, and removes the deprecated
code. It is incompatible with Python 2.x releases.

%package libs
Summary: The libraries for python runtime
Group: Applications/System
BuildRequires:  expat-devel >= 2.1.0
BuildRequires:  libffi-devel >= 3.0.13
BuildRequires:  ncurses-devel
BuildRequires:  sqlite-devel
Requires:       coreutils
Requires:       expat >= 2.1.0
Requires:       libffi >= 3.0.13
Requires:       ncurses
Requires:		%{name} = %{version}
Requires:       sqlite-libs


%description libs
The python interpreter can be embedded into applications wanting to
use python as an embedded scripting language.  The python-libs package
provides the libraries needed for python 3 applications.

%package devel
Summary: The libraries and header files needed for Python development.
Group: Development/Libraries
Requires: python3 = %{version}-%{release}
Requires: expat-devel >= 2.1.0
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
%patch0 -p1
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
    --with-system-expat \
    --with-system-ffi \
    --with-dbmliborder=gdbm:ndbm
make %{?_smp_mflags}

%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install
chmod -v 755 %{buildroot}%{_libdir}/libpython3.6m.so.1.0
%{_fixperms} %{buildroot}/*

# Remove unused stuff
find %{buildroot}%{_libdir} -name '*.pyc' -delete
find %{buildroot}%{_libdir} -name '*.pyo' -delete
find %{buildroot}%{_libdir} -name '*.o' -delete
rm %{buildroot}%{_bindir}/2to3

%check
make  %{?_smp_mflags} test

%post
/sbin/ldconfig
ln -sf %{_libdir}/libpython3.6m.so %{_libdir}/libpython3.6.so

%post libs
export PYTHONHOME=/usr
export PYTHONPATH=/usr/lib/python3.6

%postun
if [ $1 -eq 0 ] ; then
    rm %{_libdir}/libpython3.6.so
fi
/sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%defattr(-, root, root)
%doc LICENSE README.rst
%{_bindir}/pydoc*
%{_bindir}/pyvenv*
%{_bindir}/python*
%{_bindir}/pip*
%{_mandir}/*/*

%dir %{_libdir}/python3.6
%dir %{_libdir}/python3.6/site-packages

%{_libdir}/libpython3.so
%{_libdir}/libpython3.6m.so
%{_libdir}/libpython3.6m.so.1.0
%{_libdir}/pkgconfig/python-3.6.pc
%{_libdir}/pkgconfig/python-3.6m.pc
%{_libdir}/pkgconfig/python3.pc

%exclude %{_libdir}/python3.6/ctypes/test
%exclude %{_libdir}/python3.6/distutils/tests
%exclude %{_libdir}/python3.6/sqlite3/test
%exclude %{_libdir}/python3.6/idlelib/idle_test
%exclude %{_libdir}/python3.6/test
%exclude %{_libdir}/python3.6/lib-dynload/_ctypes_test.*.so

%files libs
%defattr(-,root,root)
%doc LICENSE README.rst
%{_libdir}/python3.6
%exclude %{_libdir}/python3.6/ctypes/test
%exclude %{_libdir}/python3.6/distutils/tests
%exclude %{_libdir}/python3.6/sqlite3/test
%exclude %{_libdir}/python3.6/idlelib/idle_test
%exclude %{_libdir}/python3.6/test
%exclude %{_libdir}/python3.6/lib-dynload/_ctypes_test.*.so

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_bindir}/easy_install-3.6

%doc Misc/README.valgrind Misc/valgrind-python.supp Misc/gdbinit
%{_libdir}/libpython3.so
%exclude %{_bindir}/2to3*
%exclude %{_bindir}/idle*

%files tools
%defattr(-,root,root,755)
%doc Tools/README
%{_libdir}/python3.6/lib2to3
%{_bindir}/2to3-3.6
%exclude %{_bindir}/idle*

%changelog
*	Wed May 10 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.6.1-2
-	Update the Requires & exclude idle3.
*   Wed Apr 26 2017 Siju Maliakkal <smaliakkal@vmware.com> 3.6.1-1
-   Updating to latest
*   Fri Apr 14 2017 Alexey Makhalov <amakhalov@vmware.com> 3.5.3-3
-   Python3-devel requires expat-devel.
*   Thu Mar 23 2017 Xiaolin Li <xiaolinl@vmware.com> 3.5.3-2
-   Provides /bin/python3.
*   Tue Feb 28 2017 Xiaolin Li <xiaolinl@vmware.com> 3.5.3-1
-   Updated to version 3.5.3.
*   Fri Jan 20 2017 Dheeraj Shetty <dheerajs@vmware.com> 3.5.1-10
-   Added patch to support Photon OS
*   Tue Dec 20 2016 Xiaolin Li <xiaolinl@vmware.com> 3.5.1-9
-   Move easy_install-3.5 to devel subpackage.
*   Wed Nov 16 2016 Alexey Makhalov <ppadmavilasom@vmware.com> 3.5.1-8
-   Use sqlite-{devel,libs}
*   Thu Oct 27 2016 Anish Swaminathan <anishs@vmware.com> 3.5.1-7
-   Patch for CVE-2016-5636
*   Mon Oct 10 2016 ChangLee <changlee@vmware.com> 3.5.1-6
-   Modified %check
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.5.1-5
-   GA - Bump release of all rpms
*   Wed May 04 2016 Anish Swaminathan <anishs@vmware.com> 3.5.1-4
-   Edit scriptlets.
*   Wed Apr 13 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.5.1-3
-   update python to require python-libs
*   Thu Apr 07 2016 Mahmoud Bassiouny <mbassiouny@vmware.com> 3.5.1-2
-   Providing python3 binaries instead of the minor versions.
*   Tue Feb 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.5.1-1
-   Updated to version 3.5.1
*   Wed Dec 09 2015 Anish Swaminathan <anishs@vmware.com> 3.4.3-3
-   Edit post script.
*   Mon Aug 17 2015 Vinay Kulkarni <kulkarniv@vmware.com> 3.4.3-2
-   Remove python.o file, and minor cleanups.
*   Wed Jul 1 2015 Vinay Kulkarni <kulkarniv@vmware.com> 3.4.3
-   Add Python3 package to Photon.
