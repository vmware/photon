Summary:	Package manager
Name:		rpm
Version:	4.11.2
Release:	5%{?dist}
License:	GPLv2+
URL:		http://rpm.org
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0:	http://rpm.org/releases/rpm-4.11.x/%{name}-%{version}.tar.bz2
%define sha1 rpm-4.11.2=ceef44bd180d48d4004c437bc31a3ea038f54e3e
Source1:	http://download.oracle.com/berkeley-db/db-5.3.28.tar.gz
%define sha1 db=fa3f8a41ad5101f43d08bc0efb6241c9b6fc1ae9
Source2:	rpm-system-configuring-scripts-2.2.tar.gz
%define sha1 rpm-system-configuring-scripts=9461cdc0b65f7ecc244bfa09886b4123e55ab5a8
#Requires: nspr
Requires: 	nss
Requires: 	popt
Requires:	elfutils-libelf
BuildRequires:	python2
BuildRequires:	python2-libs
BuildRequires:	python2-devel
BuildRequires:	lua-devel
BuildRequires:	popt-devel
BuildRequires:	nss-devel
BuildRequires:	elfutils-devel
%description
RPM package manager

%package devel
Requires:   python2
Summary:    Libraries and header files for rpm
Provides:   pkgconfig(rpm)
%description devel
Static libraries and header files for the support library for rpm

%package build
Requires: perl
Requires: rpm-devel
Requires: rpm
Requires: elfutils-libelf
Requires: lua
Summary: Binaries, scripts and libraries needed to build rpms.
%description build
Binaries, libraries and scripts to build rpms.

%prep
%setup -q
%setup -q -T -D -a 1
%setup -q -T -D -a 2
mv db-5.3.28 db
%build
./autogen.sh --noconfigure
./configure \
	CPPFLAGS='-I/usr/include/nspr -I/usr/include/nss' \
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
	--with-lua \
	--disable-silent-rules
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -delete
%find_lang %{name}
#	System macros and prefix
install -dm 755 %{buildroot}%{_sysconfdir}/rpm
pushd rpm-system-configuring-scripts
install -vm644 macros %{buildroot}%{_sysconfdir}/rpm/
install -vm755 brp-strip-debug-symbols %{buildroot}%{_libdir}/rpm/
install -vm755 brp-strip-unneeded %{buildroot}%{_libdir}/rpm/
popd
%post -p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%clean
rm -rf %{buildroot}
%files -f %{name}.lang
%defattr(-,root,root)
/bin/rpm
%{_sysconfdir}/rpm/macros
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
%{_libdir}/rpm/macros
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
%{_libdir}/rpm/rpmrc
%{_libdir}/rpm/tgpg

%{_libdir}/rpm/platform/*
%{_libdir}/rpm-plugins/*
%{_libdir}/librpmio.so.*
%{_libdir}/librpm.so.*
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

%files build
%{_bindir}/rpmbuild
%{_bindir}/rpmsign
%{_bindir}/rpmspec
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
%{_libdir}/librpmbuild.so
%{_libdir}/librpmsign.so.*
%{_libdir}/librpmbuild.so.*

%changelog
*   Thu Aug 05 2015 Sharath George <sharathg@vmware.com> 4.11.2-6
-   Moving build utils to a different package.
*	Sat Jun 27 2015 Alexey Makhalov <amakhalov@vmware.com> 4.11.2-5
-	Update rpm-system-configuring-scripts. Use tar --no-same-owner for rpmbuild.
*	Thu Jun 18 2015 Anish Swaminathan <anishs@vmware.com> 4.11.2-4
-	Add pkgconfig Provides directive
*	Thu Jun 18 2015 Alexey Makhalov <amakhalov@vmware.com> 4.11.2-3
-	Do no strip debug info from .debug files
*	Wed Jun 3 2015 Divya Thaluru <dthaluru@vmware.com> 4.11.2-2
-	Removing perl-module-scandeps package from run time required packages
*	Tue Jan 13 2015 Divya Thaluru <dthaluru@vmware.com> 4.11.2-1
-	Initial build. First version
