Summary:          Package manager
Name:             rpm
Version:          4.11.2
Release:          17%{?dist}
License:          GPLv2+
URL:              http://rpm.org
Group:            Applications/System
Vendor:           VMware, Inc.
Distribution:     Photon
Source0:          http://rpm.org/releases/rpm-4.11.x/%{name}-%{version}.tar.bz2
%define sha1      rpm-4.11.2=ceef44bd180d48d4004c437bc31a3ea038f54e3e
Source1:          http://download.oracle.com/berkeley-db/db-5.3.28.tar.gz
%define sha1      db=fa3f8a41ad5101f43d08bc0efb6241c9b6fc1ae9
Source2:          macros
Source3:          brp-strip-debug-symbols
Source4:          brp-strip-unneeded
Patch0:           find-debuginfo-do-not-generate-non-existing-build-id.patch
Patch1:           rpm-4.11.2-cve-2014-8118.patch
Requires:         bash
Requires:         rpm-libs = %{version}-%{release}
BuildRequires:    python2
BuildRequires:    python2-libs
BuildRequires:    python2-devel
BuildRequires:    popt-devel
BuildRequires:    nss-devel
BuildRequires:    elfutils-devel
BuildRequires:    libcap-devel
%description
RPM package manager

%package devel
Requires:   python2
Summary:    Libraries and header files for rpm
Provides:   pkgconfig(rpm)
Requires:   %{name} = %{version}-%{release}
%description devel
Static libraries and header files for the support library for rpm

%package libs
Summary:    Libraries for rpm
Requires:   nss 
Requires:   popt
Requires:   libgcc
Requires:   libcap
Requires:   zlib
Requires:   bzip2
Requires:   elfutils-libelf
%description libs
Shared libraries librpm and librpmio

%package build
Requires:   perl
Requires:   %{name}-devel = %{version}-%{release}
Requires:   elfutils-libelf
Summary: Binaries, scripts and libraries needed to build rpms.
%description build
Binaries, libraries and scripts to build rpms.

%package lang
Summary:    Additional language files for rpm
Group:      Applications/System
Requires:   %{name} = %{version}-%{release}
%description lang
These are the additional language files of rpm.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%setup -q -T -D -a 1
mv db-5.3.28 db
%build
./autogen.sh --noconfigure
./configure \
    CPPFLAGS='-I/usr/include/nspr -I/usr/include/nss -DLUA_COMPAT_APIINTCASTS' \
        --program-prefix= \
        --prefix=%{_prefix} \
        --exec-prefix=%{_prefix} \
        --bindir=%{_bindir} \
        --sbindir=%{_sbindir} \
        --sysconfdir=%{_sysconfdir} \
        --datadir=%{_datadir} \
        --includedir=%{_includedir} \
        --libdir=%{_libdir} \
        --libexecdir=%{_libexecdir} \
        --localstatedir=%{_var} \
        --sharedstatedir=%{_sharedstatedir} \
        --mandir=%{_mandir} \
        --infodir=%{_infodir} \
        --disable-dependency-tracking \
        --disable-static \
        --enable-python \
        --with-cap \
        --without-lua \
        --disable-silent-rules
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -delete
%find_lang %{name}
# System macros and prefix
install -dm 755 %{buildroot}%{_sysconfdir}/rpm
install -vm644 %{SOURCE2} %{buildroot}%{_sysconfdir}/rpm/
install -vm755 %{SOURCE3} %{buildroot}%{_libdir}/rpm/
install -vm755 %{SOURCE4} %{buildroot}%{_libdir}/rpm/

%check
make %{?_smp_mflags} check

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig
%clean
rm -rf %{buildroot}
%files
%defattr(-,root,root)
/bin/rpm
%{_bindir}/gendiff
%{_bindir}/rpm2cpio
%{_bindir}/rpmdb
%{_bindir}/rpmgraph
%{_bindir}/rpmkeys
%{_bindir}/rpmquery
%{_bindir}/rpmverify

%{_libdir}/rpm/check-buildroot
%{_libdir}/rpm/check-files
%{_libdir}/rpm/check-prereqs
%{_libdir}/rpm/check-rpaths
%{_libdir}/rpm/check-rpaths-worker
%{_libdir}/rpm/config.guess
%{_libdir}/rpm/config.sub
%{_libdir}/rpm/debugedit
%{_libdir}/rpm/desktop-file.prov
%{_libdir}/rpm/elfdeps
%{_libdir}/rpm/fontconfig.prov
%{_libdir}/rpm/libtooldeps.sh
%{_libdir}/rpm/mkinstalldirs
%{_libdir}/rpm/pkgconfigdeps.sh
%{_libdir}/rpm/platform
%{_libdir}/rpm/pythondeps.sh
%{_libdir}/rpm/rpm.daily
%{_libdir}/rpm/rpm.log
%{_libdir}/rpm/rpm.supp
%{_libdir}/rpm/rpm2cpio.sh
%{_libdir}/rpm/rpmdb_*
%{_libdir}/rpm/rpmdeps
%{_libdir}/rpm/rpmpopt-4.11.2
%{_libdir}/rpm/tgpg
%{_libdir}/rpm-plugins/*
%{_mandir}/man8/rpm.8.gz
%{_mandir}/man8/rpm2cpio.8.gz
%{_mandir}/man8/rpmdb.8.gz
%{_mandir}/man8/rpmgraph.8.gz
%{_mandir}/man8/rpmkeys.8.gz
%exclude %{_mandir}/fr/man8/*.gz
%exclude %{_mandir}/ja/man8/*.gz
%exclude %{_mandir}/ko/man8/*.gz
%exclude %{_mandir}/pl/man1/*.gz
%exclude %{_mandir}/pl/man8/*.gz
%exclude %{_mandir}/ru/man8/*.gz
%exclude %{_mandir}/sk/man8/*.gz

%files libs
%defattr(-,root,root)
%{_sysconfdir}/rpm/macros
%{_libdir}/librpmio.so.*
%{_libdir}/librpm.so.*
%{_libdir}/rpm/macros
%{_libdir}/rpm/rpmrc
%{_libdir}/rpm/platform/*

%files build
%{_bindir}/rpmbuild
%{_bindir}/rpmsign
%{_bindir}/rpmspec
%{_libdir}/librpmbuild.so
%{_libdir}/librpmbuild.so.*
%{_libdir}/rpm/osgideps.pl
%{_libdir}/rpm/perldeps.pl
%{_libdir}/rpm/macros.perl
%{_libdir}/rpm/perl.prov
%{_libdir}/rpm/perl.req
%{_libdir}/rpm/perldeps.pl
%{_libdir}/rpm/find-debuginfo.sh
%{_libdir}/rpm/find-lang.sh
%{_libdir}/rpm/find-provides
%{_libdir}/rpm/find-requires
%{_libdir}/rpm/brp-*
%{_libdir}/rpm/mono-find-provides
%{_libdir}/rpm/mono-find-requires
%{_libdir}/rpm/ocaml-find-provides.sh
%{_libdir}/rpm/ocaml-find-requires.sh
%{_libdir}/rpm/macros.perl
%{_libdir}/rpm/macros.php
%{_libdir}/rpm/macros.python
%{_libdir}/rpm/fileattrs/*
%{_libdir}/rpm/script.req
%{_libdir}/rpm/tcl.req

%{_mandir}/man1/gendiff.1*
%{_mandir}/man8/rpmbuild.8*
%{_mandir}/man8/rpmdeps.8*
%{_mandir}/man8/rpmspec.8*
%{_mandir}/man8/rpmsign.8.gz

%files devel
%defattr(-,root,root)
%{_libdir}/python*
%{_includedir}/*
%{_libdir}/pkgconfig/rpm.pc
%{_libdir}/librpmio.so
%{_libdir}/librpm.so
%{_libdir}/librpmsign.so
%{_libdir}/librpmsign.so.*

%files lang -f %{name}.lang
%defattr(-,root,root)

%changelog
*    Tue Dec 06 2016 Xiaolin Li <xiaolinl@vmware.com> 4.11.2-17
-    Added -lang subpackage.
*    Wed Nov 23 2016 Alexey Makhalov <amakhalov@vmware.com> 4.11.2-16
-    Move rpmrc and macros into -libs subpackage
-    Move zlib and elfutils-libelf dependency from rpm to rpm-libs
-    Add bzip2 dependency to rpm-libs
*    Thu Nov 17 2016 Alexey Makhalov <amakhalov@vmware.com> 4.11.2-15
-    Added -libs subpackage
*    Tue Nov 15 2016 Alexey Makhalov <amakhalov@vmware.com> 4.11.2-14
-    Disable lua support
*    Tue Oct 18 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.11.2-13
-    Apply patch for CVE-2014-8118
*    Wed Oct 05 2016 ChangLee <changlee@vmware.com> 4.11.2-12
-    Modified %check
*    Fri Aug 26 2016 Alexey Makhalov <amakhalov@vmware.com> 4.11.2-11
-    find-debuginfo...patch: exclude non existing .build-id from packaging
-    Move all files from rpm-system-configuring-scripts tarball to here 
*    Wed May 25 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.11.2-10
-    Exclude .build-id/.1 and .build-id/.1.debug from debuginfo pkg
*    Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.11.2-9
-    GA - Bump release of all rpms
*    Thu May 05 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.11.2-8
-    Update rpm version in lock-step with lua update to 5.3.2
*    Fri Apr 08 2016 Mahmoud Bassiouny <mbassiouny@vmware.com> 4.11.2-7
-    Build rpm with capabilities.
*    Thu Aug 05 2015 Sharath George <sharathg@vmware.com> 4.11.2-6
-    Moving build utils to a different package.
*    Sat Jun 27 2015 Alexey Makhalov <amakhalov@vmware.com> 4.11.2-5
-    Update rpm-system-configuring-scripts. Use tar --no-same-owner for rpmbuild.
*    Thu Jun 18 2015 Anish Swaminathan <anishs@vmware.com> 4.11.2-4
-    Add pkgconfig Provides directive
*    Thu Jun 18 2015 Alexey Makhalov <amakhalov@vmware.com> 4.11.2-3
-    Do no strip debug info from .debug files
*    Wed Jun 3 2015 Divya Thaluru <dthaluru@vmware.com> 4.11.2-2
-    Removing perl-module-scandeps package from run time required packages
*    Tue Jan 13 2015 Divya Thaluru <dthaluru@vmware.com> 4.11.2-1
-    Initial build. First version
