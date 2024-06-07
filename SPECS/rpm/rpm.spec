%define rpmhome %{_libdir}/rpm

Summary:        Package manager
Name:           rpm
Version:        4.16.1.3
Release:        19%{?dist}
License:        GPLv2+
URL:            http://rpm.org
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/rpm-software-management/rpm/archive/%{name}-%{version}.tar.gz
%define sha512 %{name}=dc1be96d433223e764f20fc7807f46baf44d2ec23a54edcf570251f0fec4b5040a311f62521e6fb4cd96723a4b791c51fa1f5fb5bc86b478e89b587ea36b46a4

Source1: macros
Source2: macros.php
Source3: macros.perl
Source4: macros.vpath
Source5: macros.ldconfig
Source6: rpmdb-rebuild.sh
Source7: rpmdb-rebuild.service
Source8: rpm.conf
Source9: lock.c

Patch0: 0001-find-debuginfo-do-not-generate-dir-entries.patch
Patch1: 0002-Header-signatures-alone-are-not-sufficient.patch
Patch2: 0003-Fix-regression-reading-rpm-v3-and-other-rare-package.patch
Patch3: 0004-lib-rpmdb.c-use-a-fallback-method-for-renaming-direc.patch
Patch4: 0005-This-patch-fixes-a-warning-that-is-shown-upon-every-.patch
Patch5: 0006-commit-buffer-cache-to-disk-after-ending-rpm-transac.patch
Patch6: 0007-If-rpm-is-not-triggered-from-tty-rpm-transactions-wo.patch
Patch7: 0008-CVE-2021-3521-1.patch
Patch8: 0009-CVE-2021-3521-2.patch
Patch9: 0010-os-install-post-improvements.patch
Patch10: 0011-Fix-setup-and-patch-not-getting-expanded-in-rpmspec-.patch
Patch11: 0012-Move-patch-uncompress-logic-from-spec-parse-to-build.patch
Patch12: 0013-Unbreak-checking-of-installed-rich-dependencies.patch

Requires: bash
Requires: zstd-libs
Requires: lua
Requires: openssl >= 1.1.1
Requires: %{name}-libs = %{version}-%{release}

BuildRequires: systemd-devel
BuildRequires: dbus-devel >= 1.3
BuildRequires: systemd-rpm-macros
BuildRequires: lua-devel
BuildRequires: popt-devel
BuildRequires: nss-devel
BuildRequires: elfutils-devel
BuildRequires: libcap-devel
BuildRequires: xz-devel
BuildRequires: file-devel
BuildRequires: python3-devel
BuildRequires: openssl >= 1.1.1
BuildRequires: zstd-devel
BuildRequires: sqlite-devel
BuildRequires: python3-setuptools
BuildRequires: libtool
BuildRequires: libltdl-devel
BuildRequires: openssl-devel

%description
RPM package manager

%package devel
Summary:        Libraries and header files for rpm
Provides:       pkgconfig(rpm)
Requires:       zstd-devel
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-sign-libs = %{version}-%{release}
Requires:       %{name}-build-libs = %{version}-%{release}

Conflicts: %{name}-build < 4.16.1.3-18%{?dist}

%description devel
Static libraries and header files for the support library for rpm

%package libs
Summary:    Libraries for rpm
Requires:   nss-libs
Requires:   popt
Requires:   libgcc
Requires:   libcap
Requires:   zlib
Requires:   bzip2-libs
Requires:   elfutils-libelf
Requires:   xz-libs
Requires:   zstd-libs
Requires:   openssl
Requires:   (toybox or coreutils or coreutils-selinux)

Conflicts:  libsolv < 0.7.19

%description    libs
Shared libraries librpm and librpmio

%package build-libs
Summary:  Libraries for building RPM packages
Requires: %{name}-libs = %{version}-%{release}
Conflicts: %{name}-build < 4.16.1.3-18%{?dist}

%description build-libs
This package contains the RPM shared libraries for building packages.

%package sign-libs
Summary:  Libraries for signing RPM packages
Requires: %{name}-libs = %{version}-%{release}

Conflicts: %{name}-devel < 4.16.1.3-18%{?dist}

%description sign-libs
This package contains the RPM shared libraries for signing packages.

%package build
Summary:    Binaries, scripts and libraries needed to build rpms.
Requires:   perl
Requires:   lua
Requires:   elfutils-libelf
Requires:   cpio
Requires:   systemd-rpm-macros
Requires:   python3-macros
Requires:   %{name}-devel = %{version}-%{release}
Requires:   %{name}-build-libs = %{version}-%{release}

%description build
Binaries, libraries and scripts to build rpms.

%package lang
Summary:    Additional language files for rpm
Group:      Applications/System
Requires:   %{name} = %{version}-%{release}

%description lang
These are the additional language files of rpm.

%package -n python3-rpm
Summary:    Python 3 bindings for rpm.
Group:      Development/Libraries
Requires:   python3
Requires:   python3-setuptools
Requires:   %{name}-build-libs = %{version}-%{release}
Requires:   %{name}-sign-libs = %{version}-%{release}

%description -n python3-%{name}
Python3 rpm.

%package plugin-systemd-inhibit
Summary:    Rpm plugin for systemd inhibit functionality
Requires:   rpm-libs = %{version}-%{release}
Requires:   dbus
Requires:   systemd

%description plugin-systemd-inhibit
This plugin blocks systemd from entering idle, sleep or shutdown while an rpm
transaction is running using the systemd-inhibit mechanism.

%prep
%autosetup -p1 -n rpm-%{name}-%{version}

%build
sed -i '/define _GNU_SOURCE/a #include "../config.h"' tools/sepdebugcrcfix.c
# pass -L opts to gcc as well to prioritize it over standard libs
sed -i 's/-Wl,-L//g' python/setup.py.in
sed -i '/library_dirs/d' python/setup.py.in
sed -i 's/extra_link_args/library_dirs/g' python/setup.py.in

# set default db to sqlite
sed -i -e "/_db_backend/ s/ bdb/ sqlite/g" macros.in

sh autogen.sh --noconfigure
export CPPFLAGS="-I/usr/include/nspr -I/usr/include/nss -DLUA_COMPAT_APIINTCASTS"
%configure \
        --program-prefix= \
        --disable-dependency-tracking \
        --disable-static \
        --enable-python \
        --with-cap \
        --with-lua \
        --with-vendor=vmware \
        --disable-silent-rules \
        --enable-zstd \
        --without-archive \
        --enable-sqlite \
        --enable-bdb-ro \
        --enable-systemd-inhibit \
        --with-crypto=openssl \
        --enable-plugins \
        --enable-bdb=no

%make_build

gcc -Wall -o lock %{SOURCE9}
chmod 700 lock

pushd python
%py3_build
popd

%check
%make_build check

%install
%make_install %{?_smp_mflags}
find %{buildroot} -name '*.la' -delete
%find_lang %{name}
# System macros and prefix
install -dm644 %{buildroot}%{_sysconfdir}/rpm
install -vm644 %{SOURCE1} %{buildroot}%{_sysconfdir}/rpm
install -vm644 %{SOURCE2} %{buildroot}%{_rpmmacrodir}
install -vm644 %{SOURCE3} %{buildroot}%{_rpmmacrodir}
install -vm644 %{SOURCE4} %{buildroot}%{_rpmmacrodir}
install -vm644 %{SOURCE5} %{buildroot}%{_rpmmacrodir}
install -vm755 %{SOURCE6} %{buildroot}%{rpmhome}

mkdir -p %{buildroot}%{_unitdir}
install -vm644 %{SOURCE7} %{buildroot}%{_unitdir}

mkdir -p %{buildroot}%{_sysconfdir}/tdnf/minversions.d
install -vm644 %{SOURCE8} %{buildroot}%{_sysconfdir}/tdnf/minversions.d
mv lock %{buildroot}%{rpmhome}

pushd python
%py3_install
popd

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%posttrans libs
if [ -f %{_sharedstatedir}/rpm/Packages ]; then
  if [ -x %{_bindir}/systemctl ]; then
    systemctl --no-reload preset rpmdb-rebuild || :
  fi
  nohup bash %{rpmhome}/rpmdb-rebuild.sh &>/dev/null &
fi

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/rpm
%{_bindir}/gendiff
%{_bindir}/rpm2cpio
%{_bindir}/rpmgraph
%{_bindir}/rpmkeys
%{_bindir}/rpmquery
%{_bindir}/rpmverify
%{rpmhome}/rpmpopt-*
%{rpmhome}/rpm.daily
%{rpmhome}/rpm.log
%{rpmhome}/rpm.supp
%{rpmhome}/rpm2cpio.sh
%{rpmhome}/tgpg
%{rpmhome}/platform
%{_libdir}/rpm-plugins/ima.so
%{_libdir}/rpm-plugins/syslog.so
%{_libdir}/rpm-plugins/prioreset.so
%{_mandir}/man8/rpm2cpio.8.gz
%{_mandir}/man8/rpmdb.8.gz
%{_mandir}/man8/rpmgraph.8.gz
%{_mandir}/man8/rpmkeys.8.gz
%{_mandir}/man8/rpm-misc.8.gz
%{_mandir}/man8/rpm-plugin-ima.8.gz
%{_mandir}/man8/rpm-plugin-prioreset.8.gz
%{_mandir}/man8/rpm-plugin-syslog.8.gz
%{_mandir}/man8/rpm-plugins.8.gz
%{_mandir}/man8/rpm.8.gz
%exclude %{_mandir}/fr/man8/*.gz
%exclude %{_mandir}/ja/man8/*.gz
%exclude %{_mandir}/ko/man8/*.gz
%exclude %{_mandir}/pl/man1/*.gz
%exclude %{_mandir}/pl/man8/*.gz
%exclude %{_mandir}/ru/man8/*.gz
%exclude %{_mandir}/sk/man8/*.gz

%files libs
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/rpm/macros
%{_libdir}/librpmio.so.*
%{_libdir}/librpm.so.*
%{rpmhome}/macros
%{rpmhome}/rpmrc
%{rpmhome}/rpmdb_*
%{rpmhome}/rpmdb-rebuild.sh
%{rpmhome}/lock
%{_bindir}/rpmdb
%{_unitdir}/rpmdb-rebuild.service
%config(noreplace) %{_sysconfdir}/tdnf/minversions.d/%{name}.conf

%files build-libs
%defattr(-,root,root)
%{_libdir}/librpmbuild.so.*

%files sign-libs
%defattr(-,root,root)
%{_libdir}/librpmsign.so.*

%files build
%{_bindir}/rpmbuild
%{_bindir}/rpmsign
%{_bindir}/rpmspec
%{_rpmmacrodir}/*
%{rpmhome}/perl.req
%{rpmhome}/find-debuginfo.sh
%{rpmhome}/find-lang.sh
%{rpmhome}/find-provides
%{rpmhome}/find-requires
%{rpmhome}/brp-*
%{rpmhome}/fileattrs/*
%{rpmhome}/script.req
%{rpmhome}/check-buildroot
%{rpmhome}/check-files
%{rpmhome}/check-prereqs
%{rpmhome}/check-rpaths
%{rpmhome}/check-rpaths-worker
%{rpmhome}/debugedit
%{rpmhome}/elfdeps
%{rpmhome}/libtooldeps.sh
%{rpmhome}/mkinstalldirs
%{rpmhome}/pkgconfigdeps.sh
%{rpmhome}/ocamldeps.sh
%{rpmhome}/*.prov
%{rpmhome}/sepdebugcrcfix
%{rpmhome}/rpmdeps
%{rpmhome}/pythondistdeps.py
%{_mandir}/man1/gendiff.1*
%{_mandir}/man8/rpmbuild.8*
%{_mandir}/man8/rpmdeps.8*
%{_mandir}/man8/rpmspec.8*
%{_mandir}/man8/rpmsign.8.gz

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/pkgconfig/rpm.pc
%{_libdir}/librpmio.so
%{_libdir}/librpm.so
%{_libdir}/librpmsign.so
%{_libdir}/librpmbuild.so

%files lang -f %{name}.lang
%defattr(-,root,root)

%files -n python3-rpm
%defattr(-,root,root,-)
%{python3_sitelib}/*

%files plugin-systemd-inhibit
%defattr(-,root,root,-)
%{_libdir}/rpm-plugins/systemd_inhibit.so
%{_mandir}/man8/rpm-plugin-systemd-inhibit.8*

%changelog
* Fri Jun 07 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 4.16.1.3-19
- Fix rich dependency issue
* Mon Aug 21 2023 Shreenidhi Shedi <sshedi@vmware.com> 4.16.1.3-18
- Add build-libs, sign-libs sub packages
* Sat Apr 29 2023 Harinadh D <hdommaraju@vmware.com> 4.16.1.3-17
- Fix for requires
* Fri Mar 10 2023 Shreenidhi Shedi <sshedi@vmware.com> 4.16.1.3-16
- Fix patch parsing logic
* Sun Feb 26 2023 Shreenidhi Shedi <sshedi@vmware.com> 4.16.1.3-15
- Fix setup macro parsing in rpmspec
* Sun Oct 02 2022 Shreenidhi Shedi <sshedi@vmware.com> 4.16.1.3-14
- Cleanup macros file
- Remove redundant brp-strip-debug-symbols script
* Wed Sep 14 2022 Shreenidhi Shedi <sshedi@vmware.com> 4.16.1.3-13
- Further fixes to CVE-2021-3521
- Remove pgp related fixes, it's not used by other distros
* Tue Aug 30 2022 Shreenidhi Shedi <sshedi@vmware.com> 4.16.1.3-12
- Fix CVE-2021-3521
* Wed Jun 22 2022 Harinadh D <hdommaraju@vmware.com> 4.16.1.3-11
- version bump with zstd
* Tue Jun 21 2022 Shreenidhi Shedi <sshedi@vmware.com> 4.16.1.3-10
- Bump version as a part of sqlite upgrade
- Add latest perl rpm macros
* Fri Apr 29 2022 Michelle Wang <michellew@vmware.com> 4.16.1.3-9
- Update sha1 to sha512
* Tue Apr 26 2022 Shreenidhi Shedi <sshedi@vmware.com> 4.16.1.3-8
- Fix Requires & BuildRequires
* Tue Feb 08 2022 Shreenidhi Shedi <sshedi@vmware.com> 4.16.1.3-7
- Fix posttrans logic
- Drop libdb support
* Mon Feb 07 2022 Dweep Advani <dadvani@vmware.com> 4.16.1.3-6
- RPM %pre script order fix
* Tue Dec 21 2021 Shreenidhi Shedi <sshedi@vmware.com> 4.16.1.3-5
- Further fix to rpm-rebuilddb.sh
- Introduced a new locking method to handle contention while rebuilding db
* Fri Dec 03 2021 Shreenidhi Shedi <sshedi@vmware.com> 4.16.1.3-4
- Conflict with libsolv < 0.7.19 to support sqlite
- Improve rpm-rebuilddb.sh script
* Mon Nov 29 2021 Prashant S Chauhan <psinghchauha@vmware.com> 4.16.1.3-3
- Update release to compile with python 3.10
* Mon Nov 22 2021 Shreenidhi Shedi <sshedi@vmware.com> 4.16.1.3-2
- Add procps-ng to Requires
* Wed Aug 18 2021 Shreenidhi Shedi <sshedi@vmware.com> 4.16.1.3-1
- Bump to version 4.16.1.3
* Mon Aug 16 2021 Shreenidhi Shedi <sshedi@vmware.com> 4.16.1.2-8
- Add python3-macros to rpm-build
* Wed Jul 28 2021 Shreenidhi Shedi <sshedi@vmware.com> 4.16.1.2-7
- Remove python dependency from rpm main package
- Build without archive support
- Add zstd-libs to Requires
* Wed Jul 21 2021 Susant Sahani <ssahani@vmware.com> 4.16.1.2-6
- Add systemd-rpm-macros to build requires and requires
* Wed May 26 2021 Shreenidhi Shedi <sshedi@vmware.com> 4.16.1.2-5
- Fix CVE-2021-20271, CVE-2021-20266
- Fix regression introduced in CVE-2021-20271 fix
- Keep all macros in /usr/lib/rpm/macros.d
* Tue May 18 2021 Shreenidhi Shedi <sshedi@vmware.com> 4.16.1.2-4
- Fix CVE-2021-20266
- Temporarily disabling few fixes as a workaround to regression
* Tue Apr 27 2021 Shreenidhi Shedi <sshedi@vmware.com> 4.16.1.2-3
- Fix PGP parsing & signature validation issues
* Tue Mar 23 2021 Piyush Gupta <gpiyush@vmware.com> 4.16.1.2-2
- Internal version bump up in order to compile with new lua.
* Thu Feb 04 2021 Shreenidhi Shedi <sshedi@vmware.com> 4.16.1.2-1
- Version upgrade to 4.16.1.2
* Tue Oct 13 2020 Anisha Kumari <kanisha@vmware.com> 4.14.2-11
- Add build conditional and enable zstd support
* Tue Sep 08 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 4.14.2-10
- Openssl 1.1.1 compatibility
* Sat Jun 20 2020 Tapas Kundu <tkundu@vmware.com> 4.14.2-9
- Mass removal python2
* Wed Apr 29 2020 Keerthana K <keerthanak@vmware.com> 4.14.2-8
- Added %config(noreplace) for /etc/rpm/macros file.
* Sat Jan 04 2020 Neal Gompa <ngompa13@gmail.com> 4.14.2-7
- Configure RPMCANONVENDOR to vmware
* Thu Oct 31 2019 Alexey Makhalov <amakhalov@vmware.com> 4.14.2-6
- rpm-build depends on cpio
* Thu Oct 10 2019 Tapas Kundu <tkundu@vmware.com> 4.14.2-5
- Enabled lua support
* Wed Oct 03 2018 Alexey Makhalov <amakhalov@vmware.com> 4.14.2-4
- Clean up the file in accordance to spec file checker
* Mon Oct 01 2018 Alexey Makhalov <amakhalov@vmware.com> 4.14.2-3
- Fix python libs dependencies to use current libs version (regression)
* Fri Sep 28 2018 Alexey Makhalov <amakhalov@vmware.com> 4.14.2-2
- macros: set _build_id_links to alldebug
* Fri Sep 14 2018 Keerthana K <keerthanak@vmware.com> 4.14.2-1
- Update to version 4.14.2
* Thu Dec 21 2017 Xiaolin Li <xiaolinl@vmware.com> 4.13.0.1-7
- Fix CVE-2017-7501
* Wed Oct 04 2017 Alexey Makhalov <amakhalov@vmware.com> 4.13.0.1-6
- make python{,3}-rpm depend on current version of librpm
* Wed Jun 28 2017 Xiaolin Li <xiaolinl@vmware.com> 4.13.0.1-5
- Add file-devel to BuildRequires
* Mon Jun 26 2017 Chang Lee <changlee@vmware.com> 4.13.0.1-4
- Updated %check
* Mon Jun 05 2017 Bo Gan <ganb@vmware.com> 4.13.0.1-3
- Fix Dependency
* Thu May 18 2017 Xiaolin Li <xiaolinl@vmware.com> 4.13.0.1-2
- Mass removal python2 from requires of rpm-devel subpackages.
* Wed May 10 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.13.0.1-1
- Update to 4.13.0.1
* Fri Apr 21 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.13.0-1
- Update to 4.13.0
* Wed Apr 19 2017 Alexey Makhalov <amakhalov@vmware.com> 4.11.2-22
- Do not allow -debuginfo to own directories to avoid conflicts with
  filesystem package and between each other. Patch applied
* Fri Apr 14 2017 Alexey Makhalov <amakhalov@vmware.com> 4.11.2-21
- rpm-libs requires nss-libs, xz-libs and bzip2-libs.
* Tue Mar 21 2017 Xiaolin Li <xiaolinl@vmware.com> 4.11.2-20
- Added python3 packages and moved python2 site packages from devel to python-rpm.
* Tue Jan 10 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.11.2-19
- added buildrequires for xz-devel for PayloadIsLzma cap
* Thu Dec 15 2016 Xiaolin Li <xiaolinl@vmware.com> 4.11.2-18
- Moved some files from rpm to rpm-build.
* Tue Dec 06 2016 Xiaolin Li <xiaolinl@vmware.com> 4.11.2-17
- Added -lang subpackage.
* Wed Nov 23 2016 Alexey Makhalov <amakhalov@vmware.com> 4.11.2-16
- Move rpmrc and macros into -libs subpackage
- Move zlib and elfutils-libelf dependency from rpm to rpm-libs
- Add bzip2 dependency to rpm-libs
* Thu Nov 17 2016 Alexey Makhalov <amakhalov@vmware.com> 4.11.2-15
- Added -libs subpackage
* Tue Nov 15 2016 Alexey Makhalov <amakhalov@vmware.com> 4.11.2-14
- Disable lua support
* Tue Oct 18 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.11.2-13
- Apply patch for CVE-2014-8118
* Wed Oct 05 2016 ChangLee <changlee@vmware.com> 4.11.2-12
- Modified %check
* Fri Aug 26 2016 Alexey Makhalov <amakhalov@vmware.com> 4.11.2-11
- find-debuginfo...patch: exclude non existing .build-id from packaging
- Move all files from rpm-system-configuring-scripts tarball to here
* Wed May 25 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.11.2-10
- Exclude .build-id/.1 and .build-id/.1.debug from debuginfo pkg
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.11.2-9
- GA - Bump release of all rpms
* Thu May 05 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.11.2-8
- Update rpm version in lock-step with lua update to 5.3.2
* Fri Apr 08 2016 Mahmoud Bassiouny <mbassiouny@vmware.com> 4.11.2-7
- Build rpm with capabilities.
* Wed Aug 05 2015 Sharath George <sharathg@vmware.com> 4.11.2-6
- Moving build utils to a different package.
* Sat Jun 27 2015 Alexey Makhalov <amakhalov@vmware.com> 4.11.2-5
- Update rpm-system-configuring-scripts. Use tar --no-same-owner for rpmbuild.
* Thu Jun 18 2015 Anish Swaminathan <anishs@vmware.com> 4.11.2-4
- Add pkgconfig Provides directive
* Thu Jun 18 2015 Alexey Makhalov <amakhalov@vmware.com> 4.11.2-3
- Do no strip debug info from .debug files
* Wed Jun 3 2015 Divya Thaluru <dthaluru@vmware.com> 4.11.2-2
- Removing perl-module-scandeps package from run time required packages
* Tue Jan 13 2015 Divya Thaluru <dthaluru@vmware.com> 4.11.2-1
- Initial build. First version
