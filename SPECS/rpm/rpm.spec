%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Package manager
Name:           rpm
Version:        4.13.0.2
Release:        1%{?dist}
License:        GPLv2+
URL:            http://rpm.org
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://ftp.rpm.org/releases/rpm-4.13.x/%{name}-%{version}.tar.bz2
%define sha1    rpm=9d6da0750184d8d077b4c28bb0ce171aef4da70b
Source1:        http://download.oracle.com/berkeley-db/db-5.3.28.tar.gz
%define sha1    db=fa3f8a41ad5101f43d08bc0efb6241c9b6fc1ae9
Source2:        rpm-system-configuring-scripts-2.2.tar.gz
%define sha1 rpm-system-configuring-scripts=9461cdc0b65f7ecc244bfa09886b4123e55ab5a8
Patch1:         find-debuginfo-do-not-generate-non-existing-build-id.patch
Patch2:         find-debuginfo-do-not-generate-dir-entries.patch
#Requires:      nspr
Requires:       nss 
Requires:       popt
Requires:       libgcc
Requires:       lua
Requires:       zlib
Requires:       file
Requires:       bash
Requires:       elfutils-libelf
Requires:       libcap
BuildRequires:  lua-devel
BuildRequires:  popt-devel
BuildRequires:  nss-devel
BuildRequires:  elfutils-devel
BuildRequires:  libcap-devel
%description
RPM package manager

%package devel
Summary:        Libraries and header files for rpm
Provides:       pkgconfig(rpm)
%description    devel
Static libraries and header files for the support library for rpm

%package build
Requires:       perl
Requires:       rpm-devel
Requires:       rpm
Requires:       elfutils-libelf
Requires:       lua
Summary:        Binaries, scripts and libraries needed to build rpms.
%description build
Binaries, libraries and scripts to build rpms.


%package -n     python-rpm
Summary:        Python 2 bindings for rpm.
Group:          Development/Libraries
BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
Requires:       python2
%description -n python-rpm

%package -n     python3-rpm
Summary:        Python 3 bindings for rpm.
Group:          Development/Libraries
BuildRequires:  python3-devel
Requires:       python3

%description -n python3-rpm
Python3 rpm.

%prep
%setup -n %{name}-%{version}
%setup -n %{name}-%{version} -T -D -a 1
%setup -n %{name}-%{version} -T -D -a 2
mv db-5.3.28 db
%patch1 -p1
%patch2 -p1

%build
sed -i '/define _GNU_SOURCE/a #include "../config.h"' tools/sepdebugcrcfix.c
# pass -L opts to gcc as well to prioritize it over standard libs
sed -i 's/-Wl,-L//g' python/setup.py.in
sed -i 's/extra_link_args/library_dirs/g' python/setup.py.in

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
	--without-archive \
        --disable-dependency-tracking \
        --disable-static \
        --enable-python \
        --with-cap \
        --with-lua \
        --disable-silent-rules
make %{?_smp_mflags}

pushd python
python2 setup.py build
python3 setup.py build
popd

%install
make DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -delete
%find_lang %{name}
# System macros and prefix
install -dm 755 %{buildroot}%{_sysconfdir}/rpm
pushd rpm-system-configuring-scripts
install -vm644 macros %{buildroot}%{_sysconfdir}/rpm/
install -vm755 brp-strip-debug-symbols %{buildroot}%{_libdir}/rpm/
install -vm755 brp-strip-unneeded %{buildroot}%{_libdir}/rpm/
popd

pushd python
python2 setup.py install --skip-build --prefix=%{_prefix} --root=%{buildroot}
python3 setup.py install --skip-build --prefix=%{_prefix} --root=%{buildroot}
popd

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig
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
%{_libdir}/rpm/elfdeps
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
%{_libdir}/rpm/rpmpopt*
%{_libdir}/rpm/rpmrc
%{_libdir}/rpm/tgpg
%{_libdir}/librpmbuild.so
%{_libdir}/librpmbuild.so.*

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
%{_libdir}/rpm/macros.*
%{_libdir}/rpm/perl.req
%{_libdir}/rpm/find-debuginfo.sh
%{_libdir}/rpm/find-lang.sh
%{_libdir}/rpm/find-provides
%{_libdir}/rpm/find-requires
%{_libdir}/rpm/brp-*
%{_libdir}/rpm/*.prov
%{_libdir}/rpm/mono-find-provides
%{_libdir}/rpm/mono-find-requires
%{_libdir}/rpm/ocaml-find-provides.sh
%{_libdir}/rpm/ocaml-find-requires.sh
%{_libdir}/rpm/macros.*
%{_libdir}/rpm/fileattrs/*
%{_libdir}/rpm/script.req
%{_libdir}/rpm/sepdebugcrcfix

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

%files -n python-rpm
%defattr(-,root,root)
%{python2_sitelib}/*

%files -n python3-rpm
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
*   Sat Nov 03 2018 Tapas Kundu <tkundu@vmware.com> 4.13.0.2-1
-   Updated to 4.13.0.2
-   Fix CVE-2017-7501 and CVE-2017-7500
*   Thu Dec 21 2017 Xiaolin Li <xiaolinl@vmware.com> 4.13.0.1-4
-   Fix CVE-2017-7501
*    Mon Dec 04 2017 Kumar Kaushik <kaushikk@vmware.com> 4.13.0.1-3
-    Release bump to use python 3.5.4.
*    Tue Oct 03 2017 Alexey Makhalov <amakhalov@vmware.com> 4.13.0.1-2
-    make python{,3}-rpm depend on current version of librpm
*    Fri Sep 29 2017 Alexey Makhalov <amakhalov@vmware.com> 4.13.0.1-1
-    rpm version update
*    Mon Jul 10 2017 Divya Thaluru <dthaluru@vmware.com> 4.11.2-14
-    Do not allow -debuginfo to own directories to avoid conflicts with
-    find-debuginfo...patch: exclude non existing .build-id from packaging
*    Fri May 26 2017 Xiaolin Li <xiaolinl@vmware.com> 4.11.2-13
-    Remove python2 from requires of rpm-devel subpackages.
*    Tue Mar 28 2017 Xiaolin Li <xiaolinl@vmware.com> 4.11.2-12
-    Added python3 packages and moved python2 site packages from devel to python-rpm.
*    Thu Oct 20 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.11.2-11
-    Apply patch for CVE-2014-8118
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
