%define rpmhome %{_libdir}/rpm

Summary:        Package manager
Name:           rpm
Version:        4.17.1
Release:        2%{?dist}
License:        GPLv2+
URL:            http://rpm.org
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/rpm-software-management/rpm/archive/%{name}-%{version}.tar.bz2
%define sha512  %{name}=d0429510140f25a25b6c9441abe2027d27c485bbd4969752f69e1c843435c9508b9f85e5bb68085dd64b7da533801aa5c04d8c9d962e08d2ddd3199d0265cc85

Source1:        brp-strip-debug-symbols
Source2:        brp-strip-unneeded
Source3:        macros
Source4:        macros.php
Source5:        macros.perl
Source6:        macros.vpath
Source7:        macros.ldconfig
Source8:        rpmdb-rebuild.sh
Source9:        rpmdb-migrate.sh
Source10:       rpmdb-rebuild.service
Source11:       rpmdb-migrate.service
Source12:       rpm.conf
Source13:       lock.c

Patch0:         rpmdb-rename-dir.patch
Patch1:         silence-warning.patch
Patch2:         sync-buf-cache.patch
Patch3:         wait-for-lock.patch
Patch4:         migrate-rpmdb.patch

Requires:       bash
Requires:       zstd-libs
Requires:       lua
Requires:       openssl >= 1.1.1
Requires:       %{name}-libs = %{version}-%{release}

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
BuildRequires:  python3-devel
BuildRequires:  openssl-devel >= 1.1.1
BuildRequires:  zstd-devel
BuildRequires:  sqlite-devel
BuildRequires:  debugedit
BuildRequires:  dwz
BuildRequires:  python3-setuptools

%description
RPM package manager

%package devel
Summary:        Libraries and header files for rpm
Provides:       pkgconfig(rpm)
Requires:       %{name} = %{version}-%{release}
Requires:       zstd-devel

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
Requires:   (toybox or coreutils-selinux)
Requires:   (toybox or findutils)
Requires:   (toybox or sed)
Conflicts:  libsolv < 0.7.19

%description    libs
Shared libraries librpm and librpmio

%package build
Requires:   perl
Requires:   lua
Requires:   %{name}-devel = %{version}-%{release}
Requires:   elfutils-libelf
Requires:   cpio
Requires:   systemd-rpm-macros
Requires:   python3-macros
Requires:   dwz
Requires:   debugedit
Summary:    Binaries, scripts and libraries needed to build rpms.

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

%description -n python3-rpm
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
%autosetup -p1 -n %{name}-%{version}

%build
# pass -L opts to gcc as well to prioritize it over standard libs
sed -i 's/-Wl,-L//g' python/setup.py.in
sed -i '/library_dirs/d' python/setup.py.in
sed -i 's/extra_link_args/library_dirs/g' python/setup.py.in

sh autogen.sh --noconfigure
%configure \
    CPPFLAGS='-I/usr/include/nspr -I/usr/include/nss -DLUA_COMPAT_APIINTCASTS' \
        --disable-dependency-tracking \
        --disable-static \
        --enable-python \
        --with-cap \
        --with-vendor=vmware \
        --disable-silent-rules \
        --enable-zstd \
        --without-archive \
        --enable-sqlite \
        --enable-bdb-ro \
        --enable-plugins \
        --with-crypto=openssl \
        --with-lua \
        --enable-nls

%make_build %{?_smp_mflags}

gcc -Wall -o lock %{SOURCE13}
chmod 700 lock

pushd python
%py3_build
popd

%check
%if 0%{?with_check}
make check TESTSUITEFLAGS=%{?_smp_mflags} || (cat tests/rpmtests.log; exit 1)
make clean %{?_smp_mflags}
%endif

%install
%make_install %{?_smp_mflags}
find %{buildroot} -name '*.la' -delete

ln -sfv %{_bindir}/find-debuginfo %{buildroot}%{rpmhome}/find-debuginfo.sh

%find_lang %{name}

# System macros and prefix
install -dm644 %{buildroot}%{_sysconfdir}/rpm
install -vm755 %{SOURCE1} %{buildroot}%{_libdir}/rpm
install -vm755 %{SOURCE2} %{buildroot}%{_libdir}/rpm
install -vm644 %{SOURCE3} %{buildroot}%{_sysconfdir}/rpm
install -vm644 %{SOURCE4} %{buildroot}%{rpmhome}/macros.d
install -vm644 %{SOURCE5} %{buildroot}%{rpmhome}/macros.d
install -vm644 %{SOURCE6} %{buildroot}%{rpmhome}/macros.d
install -vm644 %{SOURCE7} %{buildroot}%{rpmhome}/macros.d
install -vm755 %{SOURCE8} %{buildroot}%{_libdir}/rpm
install -vm755 %{SOURCE9} %{buildroot}%{_libdir}/rpm

mkdir -p %{buildroot}%{_unitdir}
install -vm644 %{SOURCE10} %{buildroot}/%{_unitdir}
install -vm644 %{SOURCE11} %{buildroot}/%{_unitdir}

mkdir -p %{buildroot}%{_sysconfdir}/tdnf/minversions.d
install -vm644 %{SOURCE12} %{buildroot}%{_sysconfdir}/tdnf/minversions.d
mv lock %{buildroot}%{_libdir}/rpm

pushd python
%py3_install
popd

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%pre
# Symlink all rpmdb files to the new location if we're still using /var/lib/rpm
if [ -d %{_sharedstatedir}/rpm ]; then
  mkdir -p %{_libdir}/sysimage/rpm
  rpmdb_files=$(find %{_sharedstatedir}/rpm -maxdepth 1 -type f | sed 's|^/var/lib/rpm/||g' | sort)
  for fn in ${rpmdb_files[@]}; do
    ln -sfr %{_sharedstatedir}/rpm/${fn} %{_libdir}/sysimage/rpm/${fn}
  done
fi

%posttrans libs
if [ -f %{_sharedstatedir}/rpm/Packages ]; then
  if [ -x %{_bindir}/systemctl ]; then
    systemctl --no-reload preset rpmdb-rebuild || :
  fi
  nohup bash %{rpmhome}/rpmdb-rebuild.sh &>/dev/null &
fi

if [ -d %{_sharedstatedir}/rpm ] && [ -x %{_bindir}/systemctl ]; then
  touch %{_sharedstatedir}/rpm/.migratedb
  systemctl --no-reload preset rpmdb-migrate || :
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
%{_libdir}/rpm-plugins/fsverity.so
%exclude %{_libdir}/rpm-plugins/dbus_announce.so

%{_sysconfdir}/dbus-1/system.d/org.rpm.conf

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
%{_mandir}/man8/rpm-plugin-dbus-announce.8.gz
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
%{rpmhome}/rpmdb-migrate.sh
%{rpmhome}/lock
%{_bindir}/rpmdb
%{_unitdir}/rpmdb-rebuild.service
%{_unitdir}/rpmdb-migrate.service
%config(noreplace) %{_sysconfdir}/tdnf/minversions.d/%{name}.conf

%files build
%{_bindir}/rpmbuild
%{_bindir}/rpmsign
%{_bindir}/rpmspec
%{_libdir}/librpmbuild.so
%{_libdir}/librpmbuild.so.*
%{rpmhome}/macros.d/*
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
%{rpmhome}/mkinstalldirs
%{rpmhome}/pkgconfigdeps.sh
%{rpmhome}/ocamldeps.sh
%{rpmhome}/*.prov
%{rpmhome}/rpmdeps
%{rpmhome}/find-debuginfo.sh

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
%{_libdir}/librpmsign.so.*

%files lang -f %{name}.lang
%defattr(-,root,root)

%files -n python3-rpm
%defattr(-,root,root,-)
%{python3_sitelib}/*

%files plugin-systemd-inhibit
%{_libdir}/rpm-plugins/systemd_inhibit.so
%{_mandir}/man8/rpm-plugin-systemd-inhibit.8*

%changelog
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
