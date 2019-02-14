Summary:        A high-level scripting language
Name:           python3
Version:        3.5.6
Release:        3%{?dist}
License:        PSF
URL:            http://www.python.org/
Group:          System Environment/Programming
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://www.python.org/ftp/python/%{version}/Python-%{version}.tar.xz
%define         sha1 Python=05548da58ec75a7af316c4a4cb8fc667ac6ac8f9
Patch0:         cgi3.patch
Patch1:         sockWarning.patch
Patch3:         python3-CVE-2018-1000117.patch
Patch4:         python3-CVE-2017-18207.patch
Patch5:         python3-CVE-2018-1061.patch
Patch6:         python3-CVE-2018-14647.patch
Patch7:         python3-CVE-2018-20406.patch
BuildRequires:  pkg-config >= 0.28
BuildRequires:  bzip2-devel
BuildRequires:  ncurses-devel >= 6.0-3
BuildRequires:  openssl-devel
BuildRequires:  readline-devel
BuildRequires:  xz-devel
Requires:       bzip2
Requires:       ncurses >= 6.0-3
Requires:       openssl
Requires:       python3-libs = %{version}-%{release}
Requires:       readline
Requires:       xz
Provides:       python-sqlite
Provides:       python(abi)
Provides:       /usr/bin/python
Provides:       /bin/python
Provides:       /bin/python3
#Conflicts with pyconfig.h file from earlier devel package
Conflicts: python3-devel < %{version}-%{release}

%description
The Python 3 package contains a new version of Python development environment.
Python 3 brings more efficient ways of handling dictionaries, better unicode
strings support, easier and more intuitive syntax, and removes the deprecated
code. It is incompatible with Python 2.x releases.

%package libs
Summary:        The libraries for python runtime
Group:          Applications/System
BuildRequires:  expat >= 2.2.4
BuildRequires:  libffi >= 3.0.13
BuildRequires:  ncurses-devel >= 6.0-3
BuildRequires:  sqlite-autoconf
Requires:       coreutils
Requires:       expat >= 2.2.4
Requires:       libffi >= 3.0.13
Requires:       ncurses >= 6.0-3
Requires:       sqlite-autoconf


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
%patch0 -p1
%patch1 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

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
chmod -v 755 %{buildroot}%{_libdir}/libpython3.5m.so.1.0
%{_fixperms} %{buildroot}/*

# Remove unused stuff
find %{buildroot}%{_libdir} -name '*.pyc' -delete
find %{buildroot}%{_libdir} -name '*.pyo' -delete
find %{buildroot}%{_libdir} -name '*.o' -delete
rm %{buildroot}%{_bindir}/2to3

%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%post
/sbin/ldconfig
ln -sf %{_libdir}/libpython3.5m.so %{_libdir}/libpython3.5.so

%post libs
export PYTHONHOME=/usr
export PYTHONPATH=/usr/lib/python3.5

%postun
if [ $1 -eq 0 ] ; then
    rm %{_libdir}/libpython3.5.so
fi
/sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%defattr(-, root, root)
%doc LICENSE README
%{_bindir}/pydoc*
%{_bindir}/pyvenv*
%{_bindir}/python*
%{_bindir}/pip*
%{_bindir}/easy_install-3.5
%{_mandir}/*/*

%dir %{_libdir}/python3.5
%dir %{_libdir}/python3.5/site-packages

%{_libdir}/libpython3.so
%{_libdir}/libpython3.5m.so
%{_libdir}/libpython3.5m.so.1.0
%{_libdir}/pkgconfig/python-3.5.pc
%{_libdir}/pkgconfig/python-3.5m.pc
%{_libdir}/pkgconfig/python3.pc
%{_includedir}/python3.5m/pyconfig.h

%exclude %{_libdir}/python3.5/ctypes/test
%exclude %{_libdir}/python3.5/distutils/tests
%exclude %{_libdir}/python3.5/sqlite3/test
%exclude %{_libdir}/python3.5/idlelib/idle_test
%exclude %{_libdir}/python3.5/test
%exclude %{_libdir}/python3.5/lib-dynload/_ctypes_test.*.so

%files libs
%defattr(-,root,root)
%doc LICENSE README
%{_libdir}/python3.5
%exclude %{_libdir}/python3.5/ctypes/test
%exclude %{_libdir}/python3.5/distutils/tests
%exclude %{_libdir}/python3.5/sqlite3/test
%exclude %{_libdir}/python3.5/idlelib/idle_test
%exclude %{_libdir}/python3.5/test
%exclude %{_libdir}/python3.5/lib-dynload/_ctypes_test.*.so

%files devel
%defattr(-,root,root)
%{_includedir}/*
%exclude %{_includedir}/python3.5m/pyconfig.h

%doc Misc/README.valgrind Misc/valgrind-python.supp Misc/gdbinit
%{_libdir}/libpython3.so
%exclude %{_bindir}/2to3*
%exclude %{_bindir}/idle*

%files tools
%defattr(-,root,root,755)
%doc Tools/README
%{_libdir}/python3.5/lib2to3
%{_bindir}/2to3-3.5
%{_bindir}/idle*

%changelog
*   Mon Feb 11 2019 Tapas Kundu <tkundu@vmware.com> 3.5.6-3
-   Fix for CVE-2018-20406
*   Mon Dec 31 2018 Tapas Kundu <tkundu@vmware.com> 3.5.6-2
-   Fix for CVE-2018-14647
*   Thu Dec 06 2018 Sujay G <gsujay@vmware.com> 3.5.6-1
-   Upgrade to version 3.5.6
*   Fri Aug 17 2018 Dweep Advani <dadvani@vmware.com> 3.5.5-2
-   Fix CVE-2018-1060 and CVE-2018-1061
*   Fri May 11 2018 Xiaolin Li <xiaolinl@vmware.com> 3.5.5-1
-   Upgrading to 3.5.5
*   Wed Apr 18 2018 Xiaolin Li <xiaolinl@vmware.com> 3.5.4-2
-   Fix CVE-2018-1000117 and CVE-2017-18207
*   Mon Dec 04 2017 Kumar Kaushik <kaushikk@vmware.com> 3.5.4-1
-   Upgrading to 3.5.4
*   Tue Sep 26 2017 Anish Swaminathan <anishs@vmware.com> 3.5.3-7
-   Release bump for expat version update
*   Thu Sep 14 2017 Kumar Kaushik <kaushikk@vmware.com> 3.5.3-6
-   Adding patch for socket cleanup issue, Bug # 1956257.
*   Fri Jul 28 2017 Divya Thaluru <dthaluru@vmware.com> 3.5.3-5
-   Fixed dependencies for easy_install-3.5
*   Thu Jun 29 2017 Divya Thaluru <dthaluru@vmware.com> 3.5.3-4
-   Bump release to built with latest toolchain
*   Mon Apr 3 2017 Alexey Makhalov <amakhalov@vmware.com> 3.5.3-3
-   Use specified version of ncurses wich has long chtype and mmask_t
    (see ncurses changelog)
*   Fri Mar 10 2017 Xiaolin Li <xiaolinl@vmware.com> 3.5.3-2
-   Provides /bin/python3.
*   Tue Feb 28 2017 Xiaolin Li <xiaolinl@vmware.com> 3.5.3-1
-   Updated to version 3.5.3
*   Thu Oct 27 2016 Anish Swaminathan <anishs@vmware.com> 3.5.1-6
-   Patch for CVE-2016-5636
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
