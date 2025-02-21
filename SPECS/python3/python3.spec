%global VER 3.11
%global with_gdb_hooks 1

Summary:        A high-level scripting language
Name:           python3
Version:        3.11.9
Release:        8%{?dist}
URL:            http://www.python.org
Group:          System Environment/Programming
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://www.python.org/ftp/python/%{version}/Python-%{version}.tar.xz
%define sha512 Python=2b0a1d936b4ef8376f9655797aece8ffdff75031ad7bfa840f330cac2aed189aecc80c163edc12ea772851d7a011f3fc1960470a73d9d4290cf3ab8ad6ed7e6a

Source1: macros.python

# check readme inside the tarball for instructions on
# how to create this tarball
Source2: setuptools-pip-wheels%{?dist}-1.0-2.tar.xz
%define sha512 setuptools-pip-wheels=bb98b9975b611d3bb99644803f9579b8d4ee5216a9d057c5191d214dd4d6a6cc0a8d72b4f33c893c85543a78faf7feec002c53648646c19baa0eeba5f9c0ed7e

Source3: license.txt
%include %{SOURCE3}

Patch0: cgi3.patch
Patch1: use-HMAC-SHA256-in-FIPS-mode.patch
Patch2: ensurepip-upgrade-bundled-pip-and-setuptools.patch
Patch3: CVE-2024-4032.patch
Patch4: CVE-2024-6923.patch
Patch5: CVE-2024-6232.patch
Patch6: CVE-2024-7592.patch
Patch7: CVE-2023-27043.patch
Patch8: CVE-2024-9287.patch

BuildRequires: pkg-config >= 0.28
BuildRequires: bzip2-devel
BuildRequires: ncurses-devel
BuildRequires: openssl-devel
BuildRequires: readline-devel
BuildRequires: xz-devel
BuildRequires: expat-devel >= 2.6.0
BuildRequires: libffi-devel >= 3.0.13
BuildRequires: sqlite-devel
BuildRequires: util-linux-devel
BuildRequires: ca-certificates

# cross compilation requires native python3 installed for ensurepip
%define BuildRequiresNative %{name}-xml

Requires: ncurses
Requires: openssl
Requires: %{name}-libs = %{version}-%{release}
Requires: readline
Requires: xz
Provides: python-sqlite
Provides: python(abi)

Provides: /usr/bin/python
Provides: /bin/python
Provides: /bin/%{name}

%if 0%{?with_check}
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
Requires:       (coreutils or coreutils-selinux)
Requires:       expat >= 2.6.0
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
Requires:       %{name}-libs = %{version}-%{release}
Requires:       %{name} = %{version}-%{release}

%description    xml
The python3-xml package provides the libraries needed for XML manipulation.

%package        curses
Summary:        Python module interface for NCurses Library
Group:          Applications/System
Requires:       %{name}-libs = %{version}-%{release}
Requires:       ncurses

%description    curses
The python3-curses package provides interface for ncurses library.

%package        devel
Summary: The libraries and header files needed for Python development.
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       expat-devel >= 2.6.0
Requires:       %{name}-macros = %{version}-%{release}
# Needed here because of the migration of Makefile from -devel to the main
# package
Conflicts: %{name} < %{version}-%{release}

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
Requires:       %{name} = %{version}-%{release}

%description    tools
The Python package includes several development tools that are used
to build python programs.

%package test
Summary: Regression tests package for Python.
Group: Development/Tools
Requires: %{name} = %{version}-%{release}

%description test
The test package contains all regression tests for Python as well as the
modules test.support and test.regrtest.
test.support is used to enhance your tests while test.regrtest drives the testing suite.

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
%autosetup -p1 -n Python-%{version} -a2

%build
export OPT="${CFLAGS}"
if [ %{_host} != %{_build} ]; then
  ln -sfv %{name} %{_bindir}/python
  export ac_cv_buggy_getaddrinfo=no
  export ac_cv_file__dev_ptmx=yes
  export ac_cv_file__dev_ptc=no
fi

rm -vf Lib/ensurepip/_bundled/pip*.whl \
       Lib/ensurepip/_bundled/setuptools*.whl

pushd setuptools-pip-wheels/%{_arch}
cp pip*.whl \
   setuptools*.whl \
   ../../Lib/ensurepip/_bundled/
popd

%configure \
    --enable-shared \
    --with-system-expat \
    --with-system-ffi \
    --with-lto \
    --enable-optimizations \
    --with-dbmliborder=gdbm:ndbm \
    --with-ssl-default-suites=openssl \
    --with-builtin-hashlib-hashes=blake2

%make_build

%install
%make_install %{?_smp_mflags}
%{_fixperms} %{buildroot}/*

# Remove unused stuff
find %{buildroot}%{_libdir} \( -type f -name '*.pyc' -or \
                               -type f -name '*.pyo' \
                               -type f -name '*.o' \
                               -type f -name '*__pycache__' \) -delete
rm %{buildroot}%{_bindir}/2to3
mkdir -p %{buildroot}%{_rpmmacrodir}
install -m 644 %{SOURCE1} %{buildroot}%{_rpmmacrodir}
cp -p Tools/scripts/pathfix.py %{buildroot}%{_bindir}/pathfix.py

%if 0%{?__debug_package}
%if 0%{?with_gdb_hooks}
  DirHoldingGdbPy=%{_libdir}/debug%{_libdir}
  mkdir -p %{buildroot}$DirHoldingGdbPy
  PathOfGdbPy=$DirHoldingGdbPy/libpython%{VER}.so.1.0-%{version}-%{release}.%{_arch}.debug-gdb.py
  cp Tools/gdb/libpython.py %{buildroot}$PathOfGdbPy
%endif
%endif

%check
%make_build test

%post
ln -sfrv %{_bindir}/%{name} %{_bindir}/python
/sbin/ldconfig

%postun
#we are handling the uninstall rpm
#in case of upgrade/downgrade we dont need any action
#as python will still be linked to python3
if [ $1 -eq 0 ] ; then
  if [ -f "%{_bindir}/python2" ]; then
    ln -sfrv %{_bindir}/python2 %{_bindir}/python
  else
    rm -f %{_bindir}/python
  fi
fi
/sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%defattr(-, root, root)
%{_bindir}/pydoc*
%{_bindir}/%{name}
%{_bindir}/python%{VER}
%{_mandir}/*/*

%dir %{_libdir}/python%{VER}
%{_libdir}/python%{VER}/site-packages/README.txt
%{_libdir}/libpython3.so
%{_libdir}/libpython%{VER}.so.1.0

%exclude %{_bindir}/pip3
%exclude %{_bindir}/pip%{VER}
%exclude %{_libdir}/python%{VER}/ctypes/test
%exclude %{_libdir}/python%{VER}/distutils/tests
%exclude %{_libdir}/python%{VER}/idlelib/idle_test
%exclude %{_libdir}/python%{VER}/test
%exclude %{_libdir}/python%{VER}/lib-dynload/_ctypes_test.*.so

%files libs
%defattr(-, root, root)
%{_libdir}/python%{VER}
%exclude %{_libdir}/python%{VER}/lib2to3
%exclude %{_libdir}/python%{VER}/site-packages/
%exclude %{_libdir}/python%{VER}/ctypes/test
%exclude %{_libdir}/python%{VER}/distutils/tests
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
%{_libdir}/pkgconfig/%{name}.pc
%{_bindir}/pathfix.py
%{_bindir}/%{name}-config
%{_bindir}/python%{VER}-config
%{_libdir}/pkgconfig/python-%{VER}-embed.pc
%{_libdir}/pkgconfig/%{name}-embed.pc

%exclude %{_bindir}/2to3*
%exclude %{_bindir}/idle*

%files tools
%defattr(-, root, root, 755)
%{_libdir}/python%{VER}/lib2to3
%{_bindir}/2to3-%{VER}
%exclude %{_bindir}/idle*

%files test
%defattr(-, root, root, 755)
%{_libdir}/python%{VER}/test/*

%files macros
%defattr(-, root, root, 755)
%{_rpmmacrodir}/macros.python

%changelog
* Wed Jan 22 2025 Prashant S Chauhan <Prashant.singh-chauhan@broadcom.com> 3.11.9-8
- Use updated python3-pip whl file, pyproject_install macro should take argument
* Wed Dec 18 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 3.11.9-7
- Fix CVE-2024-9287
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 3.11.9-6
- Release bump for SRP compliance
* Tue Nov 05 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 3.11.9-5
- Release bump for SRP compliance
* Tue Oct 01 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 3.11.9-4
- Fix CVE-2024-6232, CVE-2024-7592 & CVE-2023-27043
* Mon Aug 19 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 3.11.9-3
- Fix CVE-2024-6923
* Thu Aug 08 2024 Tapas Kundu <tapas.kundu@broadcom.com> 3.11.9-2
- Update expat dependency
* Sat Jul 27 2024 Tapas Kundu <tapas.kundu@broadcom.com> 3.11.9-1
- Update to 3.11.9
- Update pip3 wheel to 24.0
* Tue Jul 23 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 3.11.7-4
- Fix CVE-2024-4032
* Fri Mar 01 2024 Nitesh Kumar <nitesh-nk.kumar@broadcom.com> 3.11.7-3
- Bump version as a part of sqlite upgrade to v3.43.2
* Wed Feb 28 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 3.11.7-2
- Seperate pip & setuptools
- Use pip & setuptools whl from system
* Mon Dec 11 2023 Prashant S Chauhan <psinghchauha@vmware.com> 3.11.7-1
- Update to 3.11.7
* Fri Nov 03 2023 Prashant S Chauhan <psinghchauha@vmware.com> 3.11.0-10
- Fix CVE-2007-4559
* Mon Sep 11 2023 Prashant S Chauhan <psingchauha@vmware.com> 3.11.0-9
- Fix CVE-2023-24329, CVE-2022-45061, CVE-2023-41105, CVE-2023-40217
* Fri Sep 08 2023 Prashant S Chauhan <psinghchauha@vmware.com> 3.11.0-8
- Add patch for multiprocessing library to use sha256  in FIPS mode
* Thu Jun 01 2023 Nitesh Kumar <kunitesh@vmware.com> 3.11.0-7
- Bump version as a part of ncurses upgrade to v6.4
* Wed Jan 25 2023 Shreenidhi Shedi <sshedi@vmware.com> 3.11.0-6
- Fix requires
* Thu Jan 12 2023 Shreenidhi Shedi <sshedi@vmware.com> 3.11.0-5
- Disable builtin hashes and use openssl backend for the same
* Wed Jan 11 2023 Oliver Kurth <okurth@vmware.com> 3.11.0-4
- bump release as part of sqlite update
* Fri Jan 06 2023 Oliver Kurth <okurth@vmware.com> 3.11.0-3
- bump version as a part of xz upgrade
* Tue Dec 20 2022 Guruswamy Basavaiah <bguruswamy@vmware.com> 3.11.0-2
- Bump release as a part of readline upgrade
* Mon Sep 19 2022 Prashant S Chauhan <psinghchauha@vmware.com> 3.11.0-1
- Update to 3.11
* Fri Aug 12 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.9.1-9
- Bump version as a part of sqlite upgrade
* Wed Aug 10 2022 Piyush Gupta <gpiyush@vmware.com> 3.9.1-8
- Handle EPERM error in crypt.py
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
