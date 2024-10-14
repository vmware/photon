%define rpmhome %{_libdir}/%{name}

Summary:    Package manager
Name:       rpm
Version:    4.19.1.1
Release:    3%{?dist}
License:    GPLv2+
URL:        http://rpm.org
Group:      Applications/System
Vendor:     VMware, Inc.
Distribution: Photon

Source0: https://github.com/rpm-software-management/rpm/archive/%{name}-%{version}.tar.bz2
%define sha512 %{name}=3364c453c29903c144a3680ceca7a17426eb085c288b6313fb7e857a42a5e0a965f623882e0f58e633f8b8770e839d9df9f7653d99c73759af5c89d0a981908d

Source1:    macros
Source2:    macros.php
Source3:    macros.perl
Source4:    macros.vpath
Source5:    macros.ldconfig

Patch0:     0001-silence-warning.patch
Patch1:     0002-sync-buf-cache.patch
Patch2:     0003-wait-for-lock.patch
Patch3:     0004-migrate-rpmdb.patch
Patch4:     0005-dilute-user-group-requires.patch
Patch5:     0006-disable-sysusers.patch
Patch6:     0007-remove-brp-elfperms-script.patch

Requires:   bash
Requires:   zstd-libs
Requires:   %{name}-libs = %{version}-%{release}

BuildRequires:  cmake
BuildRequires:  photon-release
BuildRequires:  pandoc-bin
BuildRequires:  systemd-devel
BuildRequires:  dbus-devel >= 1.3
BuildRequires:  systemd-rpm-macros
BuildRequires:  lua-devel
BuildRequires:  popt-devel
BuildRequires:  nss-devel
BuildRequires:  elfutils-devel
BuildRequires:  libcap-devel
BuildRequires:  xz-devel
BuildRequires:  file-devel
BuildRequires:  openssl-devel
BuildRequires:  zstd-devel
BuildRequires:  sqlite-devel
BuildRequires:  debugedit
BuildRequires:  dwz
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

%description
RPM package manager

%package devel
Summary:    Libraries and header files for rpm
Provides:   pkgconfig(%{name})
Requires:   zstd-devel
Requires:   %{name} = %{version}-%{release}
Requires:   %{name}-sign-libs = %{version}-%{release}
Requires:   %{name}-build-libs = %{version}-%{release}

Conflicts: %{name}-build < 4.18.0-14%{?dist}

%description devel
Static libraries and header files for the support library for rpm

%package libs
Summary:  Libraries for rpm
Requires: nss-libs
Requires: popt
Requires: libgcc
Requires: libcap
Requires: zlib
Requires: bzip2-libs
Requires: elfutils-libelf
Requires: xz-libs
Requires: zstd-libs
Requires: openssl-libs
Requires: lua-libs

Conflicts:  libsolv < 0.7.19

%description  libs
Shared libraries librpm and librpmio

%package build-libs
Summary:  Libraries for building RPM packages
Requires: %{name}-libs = %{version}-%{release}

Conflicts: %{name}-build < 4.18.0-14%{?dist}

%description build-libs
This package contains the RPM shared libraries for building packages.

%package sign-libs
Summary:  Libraries for signing RPM packages
Requires: %{name}-libs = %{version}-%{release}

Conflicts: %{name}-devel < 4.18.0-14%{?dist}

%description sign-libs
This package contains the RPM shared libraries for signing packages.

%package build
Summary:  Binaries, scripts and libraries needed to build rpms.
Requires: perl
Requires: lua
Requires: elfutils-libelf
Requires: cpio
Requires: systemd-rpm-macros
Requires: python3-macros
Requires: dwz
Requires: debugedit
# toybox versions of find and xargs are not sufficient
Requires: findutils
Requires: patch
Requires: bzip2
Requires: tar
Requires: gzip
Requires: file
Requires: %{name}-devel = %{version}-%{release}
Requires: %{name}-build-libs = %{version}-%{release}

Conflicts: systemd < 254.1-6%{?dist}

%description build
Binaries, libraries and scripts to build rpms.

%package lang
Summary:  Additional language files for rpm
Group:    Applications/System
Requires: %{name} = %{version}-%{release}

%description lang
These are the additional language files of rpm.

%package -n python3-%{name}
Summary:  Python 3 bindings for rpm.
Group:    Development/Libraries
Requires: python3
Requires: python3-setuptools
Requires: %{name}-sign-libs = %{version}-%{release}
Requires: %{name}-build-libs = %{version}-%{release}

%description -n python3-%{name}
Python3 rpm.

%package plugin-systemd-inhibit
Summary:  Rpm plugin for systemd inhibit functionality
Requires: %{name}-libs = %{version}-%{release}
Requires: dbus
Requires: systemd

%description plugin-systemd-inhibit
This plugin blocks systemd from entering idle, sleep or shutdown while an rpm
transaction is running using the systemd-inhibit mechanism.

%package plugin-selinux
Summary: Rpm plugin for SELinux functionality
Requires: %{name}-libs = %{version}-%{release}
Requires: libselinux

%description plugin-selinux
%{summary}.

%package plugin-dbus-announce
Summary: Rpm plugin for announcing transactions on the DBUS
Requires: %{name}-libs = %{version}-%{release}

%description plugin-dbus-announce
The plugin announces basic information about rpm transactions to the
system DBUS - like packages installed or removed.  Other programs can
subscribe to the signals to get notified when packages on the system
change.

%package apidocs
Summary:    API documentation for RPM libraries
BuildArch:  noarch
Requires:   %{name} = %{version}-%{release}

%description apidocs
This package contains API documentation for developing applications
that will manipulate RPM packages and databases.

%prep
%autosetup -p1

%build
%{cmake} \
    -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
    -DENABLE_BDB_RO=ON \
    -DENABLE_SQLITE=ON \
    -DRPM_VENDOR="unknown" \
    -DWITH_OPENSSL=ON \
    -DWITH_SELINUX=ON \
    -DENABLE_PYTHON=ON \
    -DWITH_INTERNAL_OPENPGP=ON \
    -DENABLE_PLUGINS=ON \
    -DWITH_CAP=ON \
    -DWITH_ACL=OFF \
    -DWITH_ARCHIVE=OFF \
    -DWITH_AUDIT=OFF \
    -DENABLE_NDB=OFF \
    -DENABLE_OPENMP=OFF \
    -DENABLE_TESTSUITE=OFF

pushd %{__cmake_builddir}
%make_build
popd

%install
pushd %{__cmake_builddir}

%make_install %{?_smp_mflags}

ln -sfrv %{_bindir}/find-debuginfo %{buildroot}%{rpmhome}/find-debuginfo.sh
%find_lang %{name}
popd

# System macros and prefix
install -dm644 %{buildroot}%{_sysconfdir}/%{name}
install -vm644 %{SOURCE1} %{buildroot}%{_sysconfdir}/%{name}
install -vm644 %{SOURCE2} %{buildroot}%{_rpmmacrodir}
install -vm644 %{SOURCE3} %{buildroot}%{_rpmmacrodir}
install -vm644 %{SOURCE4} %{buildroot}%{_rpmmacrodir}
install -vm644 %{SOURCE5} %{buildroot}%{_rpmmacrodir}

%check
# tests run in container env, so use a VM and do make check

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%license COPYING
%doc %{_docdir}/%{name}/CONTRIBUTING.md
%doc %{_docdir}/%{name}/COPYING
%doc %{_docdir}/%{name}/INSTALL
%doc %{_docdir}/%{name}/README
%doc %{_docdir}/%{name}/CREDITS
%{_bindir}/%{name}
%{_bindir}/gendiff
%{_bindir}/rpm2cpio
%{_bindir}/rpmgraph
%{_bindir}/rpmkeys
%{_bindir}/rpmquery
%{_bindir}/rpmverify
%{_bindir}/rpmsort
%{rpmhome}/rpmpopt-*
%{rpmhome}/%{name}.daily
%{rpmhome}/%{name}.log
%{rpmhome}/%{name}.supp
%{rpmhome}/rpm2cpio.sh
%{rpmhome}/tgpg
%{rpmhome}/platform
%{rpmhome}/sysusers.sh
%exclude %{_libdir}/%{name}-plugins/syslog.so
%exclude %{_libdir}/%{name}-plugins/prioreset.so
%exclude %{_libdir}/%{name}-plugins/fapolicyd.so

%{_mandir}/man8/rpm2cpio.8.gz
%{_mandir}/man8/rpmdb.8.gz
%{_mandir}/man8/rpmgraph.8.gz
%{_mandir}/man8/rpmkeys.8.gz
%{_mandir}/man8/rpmsort.8.gz
%{_mandir}/man8/%{name}-misc.8.gz
%{_mandir}/man8/%{name}-plugin-prioreset.8.gz
%{_mandir}/man8/%{name}-plugin-syslog.8.gz
%{_mandir}/man8/%{name}-plugins.8.gz
%{_mandir}/man8/%{name}.8.gz
%{_mandir}/man8/rpm-plugin-fapolicyd.8.gz

%files libs
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/%{name}/macros
%{_libdir}/librpmio.so.*
%{_libdir}/librpm.so.*
%{rpmhome}/macros
%{rpmhome}/rpmrc
%{rpmhome}/rpmdb_*
%{_bindir}/rpmdb

%files build-libs
%defattr(-,root,root)
%{_libdir}/librpmbuild.so.*

%files sign-libs
%defattr(-,root,root)
%{_libdir}/librpmsign.so.*

%files build
%defattr(-,root,root)
%{_bindir}/rpmbuild
%{_bindir}/rpmsign
%{_bindir}/rpmspec
%{_bindir}/rpmlua
%{_rpmmacrodir}/*
%{rpmhome}/perl.req
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
%{rpmhome}/elfdeps
%{rpmhome}/pkgconfigdeps.sh
%{rpmhome}/ocamldeps.sh
%{rpmhome}/*.prov
%{rpmhome}/rpmdeps
%{rpmhome}/find-debuginfo.sh
%{rpmhome}/rpm_macros_provides.sh
%{rpmhome}/rpmuncompress
%{_mandir}/man1/gendiff.1*
%{_mandir}/man8/rpmbuild.8*
%{_mandir}/man8/rpmdeps.8*
%{_mandir}/man8/rpmspec.8*
%{_mandir}/man8/rpmsign.8.gz
%{_mandir}/man8/rpmlua.8.gz

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/librpmio.so
%{_libdir}/librpm.so
%{_libdir}/librpmsign.so
%{_libdir}/librpmbuild.so
%{_libdir}/cmake/%{name}/*

%files lang -f %{__cmake_builddir}/%{name}.lang
%defattr(-,root,root)

%files -n python3-%{name}
%defattr(-,root,root,-)
%{python3_sitelib}/*
%{_docdir}/%{name}/examples/*.py

%files plugin-systemd-inhibit
%defattr(-,root,root)
%{_libdir}/%{name}-plugins/systemd_inhibit.so
%{_mandir}/man8/%{name}-plugin-systemd-inhibit.8*

%files plugin-dbus-announce
%defattr(-,root,root)
%{_libdir}/%{name}-plugins/dbus_announce.so
%{_mandir}/man8/%{name}-plugin-dbus-announce.8*
%{_datadir}/dbus-1/system.d/org.%{name}.conf

%files plugin-selinux
%{_libdir}/%{name}-plugins/selinux.so
%{_mandir}/man8/%{name}-plugin-selinux.8*

%files apidocs
%defattr(-,root,root)
%doc %{_docdir}/%{name}/API/
%{_docdir}/%{name}/*.md

%changelog
* Mon Oct 14 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 4.19.1.1-3
- Remove brp-elfperms script
* Tue Aug 06 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 4.19.1.1-2
- Bump version as a part of nss upgrade
* Sun Jun 16 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 4.19.1.1-1
- Upgrade to v4.19.1.1
* Fri Mar 22 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 4.19.0-6
- Bump version as a part of dbus upgrade
* Thu Mar 14 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 4.19.0-5
- Bump version as a part of nss upgrade
* Mon Mar 04 2024 Nitesh Kumar <nitesh-nk.kumar@broadcom.com> 4.19.0-4
- Bump version as a part of sqlite upgrade to v3.43.2
* Sun Nov 19 2023 Shreenidhi Shedi <sshedi@vmware.com> 4.19.0-3
- Bump version as a part of openssl upgrade
* Sat Nov 18 2023 Shreenidhi Shedi <sshedi@vmware.com> 4.19.0-2
- Move sysusers.sh out of rpm-build to rpm
* Sun Sep 24 2023 Shreenidhi Shedi <sshedi@vmware.com> 4.19.0-1
- Upgrade to v4.19.0
* Fri Aug 25 2023 Shreenidhi Shedi <sshedi@vmware.com> 4.18.0-16
- Add build-libs, sign-libs sub packages
* Tue Jul 11 2023 Shreenidhi Shedi <sshedi@vmware.com> 4.18.0-15
- Bump version as a part of elfutils upgrade
* Tue Jun 20 2023 Shreenidhi Shedi <sshedi@vmware.com> 4.18.0-14
- Bump version as a part of lua upgrade
* Tue May 09 2023 Shreenidhi Shedi <sshedi@vmware.com> 4.18.0-13
- Bump version as a part of nss upgrade
* Fri Apr 14 2023 Shreenidhi Shedi <sshedi@vmware.com> 4.18.0-12
- Bump version as a part of zstd upgrade
* Fri Apr 14 2023 Shreenidhi Shedi <sshedi@vmware.com> 4.18.0-11
- Bump version as a part of zlib upgrade
* Thu Mar 09 2023 Shreenidhi Shedi <sshedi@vmware.com> 4.18.0-10
- Require lua-libs
* Wed Mar 08 2023 Shreenidhi Shedi <sshedi@vmware.com> 4.18.0-9
- Require openssl-libs
* Wed Feb 08 2023 Shreenidhi Shedi <sshedi@vmware.com> 4.18.0-8
- Fix requires
* Tue Jan 24 2023 Shreenidhi Shedi <sshedi@vmware.com> 4.18.0-7
- Remove DB migration & DB rebuild logix & related files
* Fri Jan 13 2023 Oliver Kurth <okurth@vmware.com> 4.18.0-6
- add tools needed to rpm-build requires
* Wed Jan 11 2023 Oliver Kurth <okurth@vmware.com> 4.18.0-5
- bump release as part of sqlite update
* Tue Jan 10 2023 Shreenidhi Shedi <sshedi@vmware.com> 4.18.0-4
- Bump version as part of xz upgrade
* Fri Jan 06 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 4.18.0-3
- Bump up due to change in elfutils
* Fri Jan 06 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 4.18.0-2
- Version bump for dwz upgrade
* Tue Jan 03 2023 Shreenidhi Shedi <sshedi@vmware.com> 4.18.0-1
- Upgrade to v4.18.0
* Mon Oct 10 2022 Prashant S Chauhan <psinghchauha@vmware.com> 4.17.1-5
- Bump up to compile with python 3.11
* Tue Oct 04 2022 Shreenidhi Shedi <sshedi@vmware.com> 4.17.1-4
- Bump version as a part of zstd upgrade
* Tue Sep 13 2022 Shreenidhi Shedi <sshedi@vmware.com> 4.17.1-3
- Cleanup macros file
- Remove redundant brp-strip-debug-symbols script
* Sat Jul 30 2022 Shreenidhi Shedi <sshedi@vmware.com> 4.17.1-2
- Bump version as a part of sqlite upgrade
* Tue Feb 08 2022 Shreenidhi Shedi <sshedi@vmware.com> 4.17.1-1
- Upgrade to v4.17.0
- Migrate rpmdb location to /usr/lib/sysimage/rpm
- More details at: https://fedoraproject.org/wiki/Changes/RelocateRPMToUsr
* Tue Dec 21 2021 Shreenidhi Shedi <sshedi@vmware.com> 4.16.1.3-4
- Further fix to rpm-rebuilddb.sh
- Introduced a new locking method to handle contention while rebuilding db
* Fri Dec 03 2021 Shreenidhi Shedi <sshedi@vmware.com> 4.16.1.3-3
- Conflict with libsolv < 0.7.19 to support sqlite
- Improve rpm-rebuilddb.sh script
* Mon Nov 22 2021 Shreenidhi Shedi <sshedi@vmware.com> 4.16.1.3-2
- Add procps-ng to Requires
* Wed Aug 18 2021 Shreenidhi Shedi <sshedi@vmware.com> 4.16.1.3-1
- Bump to version 4.16.1.3
* Mon Aug 16 2021 Shreenidhi Shedi <sshedi@vmware.com> 4.16.1.2-7
- Add python3-macros to rpm-build
* Wed Jul 28 2021 Shreenidhi Shedi <sshedi@vmware.com> 4.16.1.2-6
- Remove python dependency from rpm main package
* Wed Jul 14 2021 Susant Sahani <ssahani@vmware.com> 4.16.1.2-5
- Add systemd-rpm-macros to build requires and requires
* Fri May 21 2021 Shreenidhi Shedi <sshedi@vmware.com> 4.16.1.2-4
- Fix CVE-2021-20266 & CVE-2021-20271
- Fix regression introduced in CVE-2021-20271 fix
- Keep all macros in /usr/lib/rpm/macros.d
* Wed May 05 2021 Susant Sahani <ssahani@vmware.com> 4.16.1.2-3
- Add vpath and python3 macros and move macros to macro.d
* Fri Apr 30 2021 Shreenidhi Shedi <sshedi@vmware.com> 4.16.1.2-2
- Fix PGP parsing & signature validation issues
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
