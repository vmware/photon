%global VER 3.9
%global with_gdb_hooks 1

Summary:        A high-level scripting language
Name:           python3
Version:        3.9.1
Release:        7%{?dist}
License:        PSF
URL:            http://www.python.org/
Group:          System Environment/Programming
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://www.python.org/ftp/python/%{version}/Python-%{version}.tar.xz
%define sha512  Python=b90029d6825751685983e9dcf0e0ec9e46f18e6c7d37b0dd7a245a94316f8c0090308ad7c2b2b49ed2514b0b909177231dd5bcad03031bf4624e37136fcf8019
Source1:        macros.python

Patch0:         cgi3.patch

BuildRequires:  pkg-config >= 0.28
BuildRequires:  bzip2-devel
BuildRequires:  ncurses-devel
BuildRequires:  openssl-devel
BuildRequires:  readline-devel
BuildRequires:  xz-devel
BuildRequires:  expat-devel >= 2.1.0
BuildRequires:  libffi-devel >= 3.0.13
BuildRequires:  sqlite-devel
BuildRequires:  util-linux-devel
# cross compilation requires native python3 installed for ensurepip
%define BuildRequiresNative python3-xml

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

%if 0%{with_check:1}
BuildRequires:  iana-etc
BuildRequires:  tzdata
BuildRequires:  curl-devel
%endif

%description
The Python 3 package contains a new version of Python development environment.
Python 3 brings more efficient ways of handling dictionaries, better unicode
strings support, easier and more intuitive syntax, and removes the deprecated
code. It is incompatible with Python 2.x releases.

%package libs
Summary: The libraries for python runtime
Group: Applications/System
Requires:       (coreutils or toybox)
Requires:       expat >= 2.1.0
Requires:       libffi >= 3.0.13
Requires:       ncurses
Requires:       sqlite-libs
Requires:       bzip2-libs
Requires:       util-linux-libs

%description    libs
The python interpreter can be embedded into applications wanting to
use python as an embedded scripting language.  The python-libs package
provides the libraries needed for python 3 applications.

%package        xml
Summary:        XML libraries for python3 runtime
Group:          Applications/System
Requires:       python3-libs = %{version}-%{release}
Requires:       python3 = %{version}-%{release}

%description    xml
The python3-xml package provides the libraries needed for XML manipulation.

%package        curses
Summary:        Python module interface for NCurses Library
Group:          Applications/System
Requires:       python3-libs = %{version}-%{release}
Requires:       ncurses

%description    curses
The python3-curses package provides interface for ncurses library.

%package        devel
Summary: The libraries and header files needed for Python development.
Group:          Development/Libraries
Requires:       python3 = %{version}-%{release}
Requires:       expat-devel >= 2.1.0
Requires:       python3-macros = %{version}-%{release}
# Needed here because of the migration of Makefile from -devel to the main
# package
Conflicts: python3 < %{version}-%{release}

%description    devel
The Python programming language's interpreter can be extended with
dynamically loaded extensions and can be embedded in other programs.
This package contains the header files and libraries needed to do
these types of tasks.

Install python-devel if you want to develop Python extensions.  The
python package will also need to be installed.  You'll probably also
want to install the python-docs package, which contains Python
documentation.

%package        tools
Summary:        A collection of development tools included with Python.
Group:          Development/Tools
Requires:       python3 = %{version}-%{release}

%description    tools
The Python package includes several development tools that are used
to build python programs.

%package        pip
Summary:        The PyPA recommended tool for installing Python packages.
Group:          Development/Tools
BuildArch:      noarch
Requires:       python3 = %{version}-%{release}
Requires:       python3-xml = %{version}-%{release}

%description    pip
The PyPA recommended tool for installing Python packages.

%package        setuptools
Summary:        Download, build, install, upgrade, and uninstall Python packages.
Group:          Development/Tools
BuildArch:      noarch
Requires:       python3 = %{version}-%{release}
Requires:       python3-xml = %{version}-%{release}

Provides:       python%{VER}dist(setuptools)

%description    setuptools
setuptools is a collection of enhancements to the Python distutils that allow you to more easily build and distribute Python packages, especially ones that have dependencies on other packages.

%package test
Summary: Regression tests package for Python.
Group: Development/Tools
Requires: python3 = %{version}-%{release}

%description test
The test package contains all regression tests for Python as well as the modules test.support and test.regrtest. test.support is used to enhance your tests while test.regrtest drives the testing suite.

%package        macros
Summary:        Macros for Python packages.
Group:          Development/Tools
BuildArch:      noarch

%description    macros
This package contains the unversioned Python RPM macros, that most
implementations should rely on.
You should not need to install this package manually as the various
python-devel packages require it. So install a python-devel package instead.

%prep
%autosetup -p1 -n Python-%{version}

%build
export OPT="${CFLAGS}"
if [ %{_host} != %{_build} ]; then
  ln -sfv python3 /bin/python
  export ac_cv_buggy_getaddrinfo=no
  export ac_cv_file__dev_ptmx=yes
  export ac_cv_file__dev_ptc=no
fi

%configure \
    --enable-shared \
    --with-system-expat \
    --with-system-ffi \
    --enable-optimizations \
    --with-dbmliborder=gdbm:ndbm

make %{?_smp_mflags}

%install
[ %{buildroot} != "/" ] && rm -rf %{buildroot}/*

make DESTDIR=%{buildroot} install %{?_smp_mflags}
%{_fixperms} %{buildroot}/*

# Remove unused stuff
find %{buildroot}%{_libdir} -name '*.pyc' -delete
find %{buildroot}%{_libdir} -name '*.pyo' -delete
find %{buildroot}%{_libdir} -name '*.o' -delete
find %{buildroot}%{_libdir} -name '*__pycache__' -delete
rm %{buildroot}%{_bindir}/2to3
mkdir -p %{buildroot}%{_libdir}/rpm/macros.d
install -m 644 %{SOURCE1} %{buildroot}%{_libdir}/rpm/macros.d

%if 0%{?with_gdb_hooks:1}
  DirHoldingGdbPy=%{_libdir}/debug%{_libdir}
  mkdir -p %{buildroot}$DirHoldingGdbPy
  PathOfGdbPy=$DirHoldingGdbPy/libpython%{VER}.so.1.0-%{version}-%{release}.%{_arch}.debug-gdb.py
  cp Tools/gdb/libpython.py %{buildroot}$PathOfGdbPy
%endif # with gdb_hooks

%check
%if 0%{?with_check:1}
make %{?_smp_mflags} test
%endif

%post
ln -sfv %{_bindir}/python3 %{_bindir}/python
/sbin/ldconfig

%postun
#we are handling the uninstall rpm
#in case of upgrade/downgrade we dont need any action
#as python will still be linked to python3
if [ $1 -eq 0 ] ; then
  if [ -f "%{_bindir}/python2" ]; then
    ln -sfv %{_bindir}/python2 %{_bindir}/python
  else
    rm -f %{_bindir}/python
  fi
fi
/sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%defattr(-, root, root)
%doc LICENSE README.rst
%{_bindir}/pydoc*
%{_bindir}/python3
%{_bindir}/python%{VER}
%{_mandir}/*/*

%dir %{_libdir}/python%{VER}
%{_libdir}/python%{VER}/site-packages/README.txt

%{_libdir}/libpython3.so
%{_libdir}/libpython%{VER}.so.1.0

%exclude %{_libdir}/python%{VER}/ctypes/test
%exclude %{_libdir}/python%{VER}/distutils/tests
%exclude %{_libdir}/python%{VER}/sqlite3/test
%exclude %{_libdir}/python%{VER}/idlelib/idle_test
%exclude %{_libdir}/python%{VER}/test
%exclude %{_libdir}/python%{VER}/lib-dynload/_ctypes_test.*.so

%files libs
%defattr(-, root, root)
%doc LICENSE README.rst
%{_libdir}/python%{VER}
%exclude %{_libdir}/python%{VER}/lib2to3
%exclude %{_libdir}/python%{VER}/site-packages/
%exclude %{_libdir}/python%{VER}/ctypes/test
%exclude %{_libdir}/python%{VER}/distutils/tests
%exclude %{_libdir}/python%{VER}/sqlite3/test
%exclude %{_libdir}/python%{VER}/idlelib/idle_test
%exclude %{_libdir}/python%{VER}/test
%exclude %{_libdir}/python%{VER}/lib-dynload/_ctypes_test.*.so
%exclude %{_libdir}/python%{VER}/xml
%exclude %{_libdir}/python%{VER}/lib-dynload/pyexpat*.so
%exclude %{_libdir}/python%{VER}/curses
%exclude %{_libdir}/python%{VER}/lib-dynload/_curses*.so

%files  xml
%defattr(-, root, root, 755)
%{_libdir}/python%{VER}/xml/*
%{_libdir}/python%{VER}/lib-dynload/pyexpat*.so

%files  curses
%defattr(-, root, root, 755)
%{_libdir}/python%{VER}/curses/*
%{_libdir}/python%{VER}/lib-dynload/_curses*.so

%files devel
%defattr(-, root, root)
%{_includedir}/*
%{_libdir}/libpython%{VER}.so
%{_libdir}/pkgconfig/python-%{VER}.pc
%{_libdir}/pkgconfig/python3.pc
%{_bindir}/python3-config
%{_bindir}/python%{VER}-config
%{_libdir}/pkgconfig/python-%{VER}-embed.pc
%{_libdir}/pkgconfig/python3-embed.pc

%doc Misc/README.valgrind Misc/valgrind-python.supp Misc/gdbinit
%exclude %{_bindir}/2to3*
%exclude %{_bindir}/idle*

%files tools
%defattr(-, root, root, 755)
%doc Tools/README
%{_libdir}/python%{VER}/lib2to3
%{_bindir}/2to3-%{VER}
%exclude %{_bindir}/idle*

%files pip
%defattr(-, root, root, 755)
%{_libdir}/python%{VER}/site-packages/pip/*
%{_bindir}/pip*
%exclude %{_libdir}/python%{VER}/site-packages/pip/_vendor/distlib/*.exe

%files setuptools
%defattr(-, root, root, 755)
%{_libdir}/python%{VER}/site-packages/pkg_resources/*
%{_libdir}/python%{VER}/site-packages/setuptools/*
%{_libdir}/python%{VER}/site-packages/setuptools-49.2.1.dist-info/*
%{_bindir}/easy_install-%{VER}
%exclude %{_libdir}/python%{VER}/site-packages/setuptools/*.exe

%files test
%defattr(-, root, root, 755)
%{_libdir}/python%{VER}/test/*

%files macros
%defattr(-, root, root, 755)
%{_libdir}/rpm/macros.d/macros.python

%changelog
* Tue May 10 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.9.1-7
- Bump version as a part of libffi upgrade
* Wed Feb 02 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.9.1-6
- Package python gdb hooks script
* Sat Aug 21 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 3.9.1-5
- Bump up release for openssl
* Mon Aug 16 2021 Shreenidhi Shedi <sshedi@vmware.com> 3.9.1-4
- Fix python rpm macros
* Sat Mar 27 2021 Tapas Kundu <tkundu@vmware.com> 3.9.1-3
- Remove packaging exe files in python3-pip
* Sat Jan 16 2021 Shreenidhi Shedi <sshedi@vmware.com> 3.9.1-2
- Fix build with new rpm
* Fri Jan 08 2021 Tapas Kundu <tkundu@vmware.com> 3.9.1-1
- Update to 3.9.1
* Tue Oct 13 2020 Tapas Kundu <tkundu@vmware.com> 3.9.0-1
- Update to 3.9.0
* Wed Sep 30 2020 Gerrit Photon <photon-checkins@vmware.com> 3.8.6-1
- Automatic Version Bump
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 3.8.5-4
- openssl 1.1.1
* Sun Aug 16 2020 Tapas Kundu <tkundu@vmware.com> 3.8.5-3
- Package %{_libdir}/python3.8/lib2to3 in tools
* Thu Aug 13 2020 Tapas Kundu <tkundu@vmware.com> 3.8.5-2
- Add macros subpackage
* Sun Jul 26 2020 Tapas Kundu <tkundu@vmware.com> 3.8.5-1
- Updated to 3.8.5 release
* Fri Jul 17 2020 Tapas Kundu <tkundu@vmware.com> 3.7.5-3
- symlink python to python3
* Fri May 01 2020 Alexey Makhalov <amakhalov@vmware.com> 3.7.5-2
- -setuptools requires -xml.
* Sat Dec 07 2019 Tapas Kundu <tkundu@vmware.com> 3.7.5-1
- Updated to 3.7.5 release
- Linked /usr/bin/python to python3.
- While uninstalling link to python2 if available.
* Tue Nov 26 2019 Alexey Makhalov <amakhalov@vmware.com> 3.7.4-5
- Cross compilation support
* Tue Nov 05 2019 Tapas Kundu <tkundu@vmware.com> 3.7.4-4
- Fix for CVE-2019-17514
* Thu Oct 24 2019 Shreyas B. <shreyasb@vmware.com> 3.7.4-3
- Fixed makecheck errors.
* Wed Oct 23 2019 Tapas Kundu <tkundu@vmware.com> 3.7.4-2
- Fix conflict of libpython3.so
* Thu Oct 17 2019 Tapas Kundu <tkundu@vmware.com> 3.7.4-1
- Updated to patch release 3.7.4
- Fix CVE-2019-16935
* Wed Sep 11 2019 Tapas Kundu <tkundu@vmware.com> 3.7.3-3
- Fix CVE-2019-16056
* Mon Jun 17 2019 Tapas Kundu <tkundu@vmware.com> 3.7.3-2
- Fix for CVE-2019-10160
* Mon Jun 10 2019 Tapas Kundu <tkundu@vmware.com> 3.7.3-1
- Update to Python 3.7.3 release
* Thu May 23 2019 Tapas Kundu <tkundu@vmware.com> 3.7.0-6
- Fix for CVE-2019-5010
- Fix for CVE-2019-9740
* Tue Mar 12 2019 Tapas Kundu <tkundu@vmware.com> 3.7.0-5
- Fix for CVE-2019-9636
* Mon Feb 11 2019 Taps Kundu <tkundu@vmware.com> 3.7.0-4
- Fix for CVE-2018-20406
* Fri Dec 21 2018 Tapas Kundu <tkundu@vmware.com> 3.7.0-3
- Fix for CVE-2018-14647
* Tue Dec 04 2018 Tapas Kundu <tkundu@vmware.com> 3.7.0-2
- Excluded windows installer from python3 libs packaging.
* Wed Sep 26 2018 Tapas Kundu <tkundu@vmware.com> 3.7.0-1
- Updated to version 3.7.0
* Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 3.6.1-9
- Requires coreutils or toybox
- Requires bzip2-libs
* Fri Sep 15 2017 Bo Gan <ganb@vmware.com> 3.6.1-8
- Remove devpts mount in check
* Mon Aug 28 2017 Dheeraj Shetty <dheerajs@vmware.com> 3.6.1-7
- Add pty for tests to pass
* Wed Jul 12 2017 Xiaolin Li <xiaolinl@vmware.com> 3.6.1-6
- Add python3-test package.
* Fri Jun 30 2017 Dheeraj Shetty <dheerajs@vmware.com> 3.6.1-5
- Remove the imaplib tests.
* Mon Jun 05 2017 Xiaolin Li <xiaolinl@vmware.com> 3.6.1-4
- Added pip, setuptools, xml, and curses sub packages.
* Sun Jun 04 2017 Bo Gan <ganb@vmware.com> 3.6.1-3
- Fix symlink and script
* Wed May 10 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.6.1-2
- Exclude idle3.
* Wed Apr 26 2017 Siju Maliakkal <smaliakkal@vmware.com> 3.6.1-1
- Updating to latest
* Fri Apr 14 2017 Alexey Makhalov <amakhalov@vmware.com> 3.5.3-3
- Python3-devel requires expat-devel.
* Thu Mar 23 2017 Xiaolin Li <xiaolinl@vmware.com> 3.5.3-2
- Provides /bin/python3.
* Tue Feb 28 2017 Xiaolin Li <xiaolinl@vmware.com> 3.5.3-1
- Updated to version 3.5.3.
* Fri Jan 20 2017 Dheeraj Shetty <dheerajs@vmware.com> 3.5.1-10
- Added patch to support Photon OS
* Tue Dec 20 2016 Xiaolin Li <xiaolinl@vmware.com> 3.5.1-9
- Move easy_install-3.5 to devel subpackage.
* Wed Nov 16 2016 Alexey Makhalov <ppadmavilasom@vmware.com> 3.5.1-8
- Use sqlite-{devel,libs}
* Thu Oct 27 2016 Anish Swaminathan <anishs@vmware.com> 3.5.1-7
- Patch for CVE-2016-5636
* Mon Oct 10 2016 ChangLee <changlee@vmware.com> 3.5.1-6
- Modified %check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.5.1-5
- GA - Bump release of all rpms
* Wed May 04 2016 Anish Swaminathan <anishs@vmware.com> 3.5.1-4
- Edit scriptlets.
* Wed Apr 13 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.5.1-3
- update python to require python-libs
* Thu Apr 07 2016 Mahmoud Bassiouny <mbassiouny@vmware.com> 3.5.1-2
- Providing python3 binaries instead of the minor versions.
* Tue Feb 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.5.1-1
- Updated to version 3.5.1
* Wed Dec 09 2015 Anish Swaminathan <anishs@vmware.com> 3.4.3-3
- Edit post script.
* Mon Aug 17 2015 Vinay Kulkarni <kulkarniv@vmware.com> 3.4.3-2
- Remove python.o file, and minor cleanups.
* Wed Jul 1 2015 Vinay Kulkarni <kulkarniv@vmware.com> 3.4.3
- Add Python3 package to Photon.
