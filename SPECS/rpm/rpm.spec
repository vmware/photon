Summary:        Package manager
Name:           rpm
Version:        4.14.3
Release:        8%{?dist}
License:        GPLv2+
URL:            http://rpm.org
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/rpm-software-management/rpm/archive/%{name}-%{version}-release.tar.gz
%define sha512 %{name}=726c72e2b920a43572d5ccc872411e1d89352ae49f0a9a2bea80a15cede65f55942224f373923bf0615c19328599191f617bb86a63c9075a8a9b1d4a038e7f0d

Source1: macros
Source2: macros.python2
Source3: macros.python3

Patch0: find-debuginfo-do-not-generate-dir-entries.patch
Patch1: CVE-2021-20271.patch
Patch2: Header-signatures-alone-are-not-sufficient.patch
Patch3: CVE-2021-20266.patch
Patch4: Fix-regression-reading-rpm-v3.patch
Patch5: CVE-2021-3521.patch
Patch6: os-install-post-improvements.patch
Patch7: 0001-When-doing-the-same-thing-more-than-once-use-a-loop.patch
Patch8: 0001-Introduce-patch_nums-and-source_nums-Lua-variables-i.patch
Patch9: 0001-Add-limits-to-autopatch-macro.patch
Patch10: setup-macro-fix.patch

Requires: bash
Requires: libdb
Requires: %{name}-libs = %{version}-%{release}
Requires: lua
Requires: zstd-libs

BuildRequires: lua-devel
BuildRequires: libdb-devel
BuildRequires: popt-devel
BuildRequires: nss-devel
BuildRequires: elfutils-devel
BuildRequires: libcap-devel
BuildRequires: xz-devel
BuildRequires: file-devel
BuildRequires: python3-devel
BuildRequires: zstd-devel

%description
RPM package manager

%package devel
Summary:        Libraries and header files for rpm
Provides:       pkgconfig(%{name})
Requires:       %{name} = %{version}-%{release}
Requires:       zstd-devel
%description devel
Static libraries and header files for the support library for rpm

%package libs
Summary:        Libraries for rpm
Requires:       nss-libs
Requires:       popt
Requires:       libgcc
Requires:       libcap
Requires:       zlib
Requires:       bzip2-libs
Requires:       elfutils-libelf
Requires:       xz-libs
Requires:       zstd-libs
%description    libs
Shared libraries librpm and librpmio

%package build
Requires:       perl
Requires:       lua
Requires:       %{name}-devel = %{version}-%{release}
Requires:       elfutils-libelf
Summary: Binaries, scripts and libraries needed to build rpms.
%description build
Binaries, libraries and scripts to build rpms.

%package lang
Summary:        Additional language files for rpm
Group:          Applications/System
Requires:       %{name} = %{version}-%{release}
%description lang
These are the additional language files of rpm.

%package -n     python3-%{name}
Summary:        Python 3 bindings for rpm.
Group:          Development/Libraries
Requires:       python3

%description -n python3-%{name}
Python3 rpm.

%prep
%autosetup -p1 -n %{name}-%{name}-%{version}-release

%build
sed -i '/define _GNU_SOURCE/a #include "../config.h"' tools/sepdebugcrcfix.c
# pass -L opts to gcc as well to prioritize it over standard libs
sed -i 's/-Wl,-L//g' python/setup.py.in
sed -i '/library_dirs/d' python/setup.py.in
sed -i 's/extra_link_args/library_dirs/g' python/setup.py.in

sh ./autogen.sh --noconfigure
export CPPFLAGS='-I%{_includedir}/nspr -I%{_includedir}/nss -DLUA_COMPAT_APIINTCASTS'
%configure \
    --program-prefix= \
    --disable-dependency-tracking \
    --disable-static \
    --enable-python \
    --with-cap \
    --with-lua \
    --with-vendor=vmware \
    --disable-silent-rules \
    --with-external-db \
    --enable-zstd \
    --without-archive \
    PYTHON=%{python3}

%make_build

pushd python
%py3_build
popd

%install
%make_install %{?_smp_mflags}

# All these are unused
rm -v %{buildroot}%{_rpmconfigdir}/macros.python \
      %{buildroot}%{_rpmconfigdir}/macros.php \
      %{buildroot}%{_rpmconfigdir}/macros.perl

find %{buildroot} -name '*.la' -delete

%find_lang %{name}

# System macros and prefix
install -dm 755 %{buildroot}%{_sysconfdir}/%{name}
install -vm644 %{SOURCE1} %{buildroot}%{_sysconfdir}/%{name}
install -vm644 %{SOURCE2} %{buildroot}%{_rpmmacrodir}
install -vm644 %{SOURCE3} %{buildroot}%{_rpmmacrodir}

pushd python
%py3_install
popd

%if 0%{?with_check}
%check
make check %{?_smp_mflags}
%endif

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/%{name}
%{_bindir}/gendiff
%{_bindir}/rpm2cpio
%{_bindir}/rpmdb
%{_bindir}/rpmgraph
%{_bindir}/rpmkeys
%{_bindir}/rpmquery
%{_bindir}/rpmverify

%{_rpmconfigdir}/rpmpopt-*
%{_rpmconfigdir}/rpmdb_*
%{_rpmconfigdir}/%{name}.daily
%{_rpmconfigdir}/%{name}.log
%{_rpmconfigdir}/%{name}.supp
%{_rpmconfigdir}/rpm2cpio.sh
%{_rpmconfigdir}/tgpg
%{_rpmconfigdir}/platform
%{_libdir}/%{name}-plugins/*
%{_mandir}/man8/%{name}.8.gz
%{_mandir}/man8/rpm2cpio.8.gz
%{_mandir}/man8/rpmdb.8.gz
%{_mandir}/man8/rpmgraph.8.gz
%{_mandir}/man8/rpmkeys.8.gz
%{_mandir}/man8/%{name}-misc.8.gz
%{_mandir}/man8/%{name}-plugin-systemd-inhibit.8.gz
%exclude %{_mandir}/fr/man8/*.gz
%exclude %{_mandir}/ja/man8/*.gz
%exclude %{_mandir}/ko/man8/*.gz
%exclude %{_mandir}/pl/man1/*.gz
%exclude %{_mandir}/pl/man8/*.gz
%exclude %{_mandir}/ru/man8/*.gz
%exclude %{_mandir}/sk/man8/*.gz

%files libs
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/%{name}/macros
%{_libdir}/librpmio.so.*
%{_libdir}/librpm.so.*
%{_rpmconfigdir}/macros
%{_rpmconfigdir}/rpmrc
%{_rpmconfigdir}/platform/*

%files build
%{_bindir}/rpmbuild
%{_bindir}/rpmsign
%{_bindir}/rpmspec
%{_libdir}/librpmbuild.so
%{_libdir}/librpmbuild.so.*
%{_rpmmacrodir}/*
%{_rpmconfigdir}/perl.req
%{_rpmconfigdir}/find-debuginfo.sh
%{_rpmconfigdir}/find-lang.sh
%{_rpmconfigdir}/find-provides
%{_rpmconfigdir}/find-requires
%{_rpmconfigdir}/brp-*
%{_rpmconfigdir}/mono-find-provides
%{_rpmconfigdir}/mono-find-requires
%{_rpmconfigdir}/ocaml-find-provides.sh
%{_rpmconfigdir}/ocaml-find-requires.sh
%{_rpmconfigdir}/fileattrs/*
%{_rpmconfigdir}/script.req
%{_rpmconfigdir}/check-buildroot
%{_rpmconfigdir}/check-files
%{_rpmconfigdir}/check-prereqs
%{_rpmconfigdir}/check-rpaths
%{_rpmconfigdir}/check-rpaths-worker
%{_rpmconfigdir}/config.guess
%{_rpmconfigdir}/config.sub
%{_rpmconfigdir}/debugedit
%{_rpmconfigdir}/elfdeps
%{_rpmconfigdir}/libtooldeps.sh
%{_rpmconfigdir}/mkinstalldirs
%{_rpmconfigdir}/pkgconfigdeps.sh
%{_rpmconfigdir}/*.prov
%{_rpmconfigdir}/sepdebugcrcfix

%{_rpmconfigdir}/python-macro-helper
%{_rpmconfigdir}/pythondistdeps.py

%{_rpmconfigdir}/pythondeps.sh
%{_rpmconfigdir}/rpmdeps

%{_mandir}/man1/gendiff.1*
%{_mandir}/man8/rpmbuild.8*
%{_mandir}/man8/rpmdeps.8*
%{_mandir}/man8/rpmspec.8*
%{_mandir}/man8/rpmsign.8.gz

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/librpmio.so
%{_libdir}/librpm.so
%{_libdir}/librpmsign.so
%{_libdir}/librpmsign.so.*

%files lang -f %{name}.lang
%defattr(-,root,root)

%files -n python3-%{name}
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
* Sun Feb 26 2023 Shreenidhi Shedi <sshedi@vmware.com> 4.14.3-8
- Fix setup macro parsing issue in rpmspec
* Fri Feb 10 2023 Shreenidhi Shedi <sshedi@vmware.com> 4.14.3-7
- Remove python2 things
- Add limits to autopatch macro
* Thu Oct 06 2022 Shreenidhi Shedi <sshedi@vmware.com> 4.14.3-6
- Cleanup macros file
- Remove redundant brp-strip-debug-symbols script
* Wed Sep 14 2022 Shreenidhi Shedi <sshedi@vmware.com> 4.14.3-5
- Further fixes to CVE-2021-3521
- Remove pgp related fixes, it's not used by other distros
* Tue Aug 30 2022 Shreenidhi Shedi <sshedi@vmware.com> 4.14.3-4
- Fix CVE-2021-3521
* Fri Jul 08 2022 Harinadh D <hdommaraju@vmware.com> 4.14.3-3
- version bump to build with zstd
* Mon Jul 04 2022 Shreenidhi Shedi <sshedi@vmware.com> 4.14.3-2
- Remove unused macro files from /usr/lib/rpm
* Mon Aug 16 2021 Shreenidhi Shedi <sshedi@vmware.com> 4.14.3-1
- Version bump to 4.14.3
- Add macros for py2 & py3
* Tue Jul 27 2021 Piyush Gupta <gpiyush@vmware.com> 4.14.2-14
- Added zstd-libs in Requires
- Remove python dependency from rpm
- Build without archive support
* Tue Jun 01 2021 Shreenidhi Shedi <sshedi@vmware.com> 4.14.2-13
- Invalid signature tag Archivesize (1046) issue fix
* Tue May 18 2021 Shreenidhi Shedi <sshedi@vmware.com> 4.14.2-12
- Fix CVE-2021-20266
- Temporarily disabling few fixes as a workaround to regression
* Tue Apr 27 2021 Shreenidhi Shedi <sshedi@vmware.com> 4.14.2-11
- Fix PGP parsing & signature validation issues
* Wed Apr 07 2021 Shreenidhi Shedi <sshedi@vmware.com> 4.14.2-10
- Fix for CVE-2021-20271
* Wed Sep 09 2020 Anisha Kumari <kanisha@vmware.com> 4.14.2-9
- Add build conditional and enable zstd support
* Mon Jun 01 2020 Siju Maliakkal <smaliakkal@vmware.com> 4.14.2-8
- Use latest sqlite
* Wed Apr 29 2020 Keerthana K <keerthanak@vmware.com> 4.14.2-7
- Added %config(noreplace) for /etc/rpm/macros file.
* Sat Jan 04 2020 Neal Gompa <ngompa13@gmail.com> 4.14.2-6
- Configure RPMCANONVENDOR to vmware
* Thu Oct 10 2019 Tapas Kundu <tkundu@vmware.com> 4.14.2-5
- Enabled lua support.
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
- Remove python2 from requires of rpm-devel subpackages.
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
