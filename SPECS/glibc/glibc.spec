%define debug_package %{nil}
%define __os_install_post %{nil}
%global security_hardening nonow
%define glibc_target_cpu %{_build}

Summary:        Main C library
Name:           glibc
Version:        2.22
Release:        23%{?dist}
License:        LGPLv2+
URL:            http://www.gnu.org/software/libc
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://ftp.gnu.org/gnu/glibc/%{name}-%{version}.tar.xz
%define sha1    glibc=5be95334f197121d8b351059a1c6518305d88e2a
Source1:        locale-gen.sh
Source2:        locale-gen.conf
Patch0:         http://www.linuxfromscratch.org/patches/downloads/glibc/glibc-2.22-upstream_i386_fix-1.patch
Patch1:         http://www.linuxfromscratch.org/patches/downloads/glibc/glibc-2.22-largefile-1.patch
Patch2:         http://www.linuxfromscratch.org/patches/downloads/glibc/glibc-2.22-fhs-1.patch
Patch3:     glibc-2.22-bindrsvport-blacklist.patch
Patch4:         http://www.linuxfromscratch.org/patches/downloads/glibc/glibc-2.22-upstream_fixes-1.patch
Patch5:         glibc-fix-CVE-2014-9761-1.patch
Patch6:         glibc-fix-CVE-2014-9761-2.patch
Patch7:         glibc-fix-CVE-2014-9761-3.patch
Patch8:         glibc-fix-CVE-2014-9761-4.patch
Patch9:         pthread_create-fix-use-after-free.patch
# Fixes CVE-2016-3075
Patch10:        CVE-2016-3075-Stack-overflow-in-_nss_dns_getnetbynam.patch
# Fixes CVE-2016-3706
Patch11:        CVE-2016-3706-getaddrinfo-stack-overflow-in-hostent-.patch
# It allows to apply CVE-2016-1234 patch
Patch12:        glob-Simplify-the-interface-for-the-GLOB_ALTDIRFUNC-.patch
# Fixes CVE-2016-1234
Patch13:        CVE-2016-1234-glob-Do-not-copy-d_name-field-of-struc.patch
# Fixed CVE-2016-4429
Patch14:        CVE-2016-4429-sunrpc-Do-not-use-alloca-in-clntudp_ca.patch
Patch15:        glibc-fix-CVE-2017-1000366.patch
#https://sourceware.org/git/gitweb.cgi?p=glibc.git;h=d42eed4a044e5e10dfb885cf9891c2518a72a491
Patch16:        glibc-fix-CVE-2017-12133.patch
Patch17:        glibc-fix-CVE-2017-15670.patch
Patch18:        glibc-fix-CVE-2017-15804.patch
#https://sourceware.org/git/gitweb.cgi?p=glibc.git;a=patch;h=20f534e0abd81149c71cef082c8c058bb9d953af
Patch19:        glibc-fix-CVE-2015-5180.patch
#https://sourceware.org/git/gitweb.cgi?p=glibc.git;a=patch;h=5e7fdabd7df1fc6c56d104e61390bf5a6b526c38
Patch20:        glibc-2.22-CVE-2016-5417.patch
Patch21:        glibc-fix-CVE-2017-16997.patch
Patch22:        glibc-fix-CVE-2018-1000001.patch
Patch23:        glibc-fix-CVE-2018-6485.patch
Patch24:        glibc-fix-CVE-2017-18269.patch
Patch25:        glibc-fix-CVE-2018-11236.patch
Patch26:        glibc-fix-CVE-2017-15671.patch
Patch27:        glibc-fix-CVE-2017-12132.patch
Provides:       rtld(GNU_HASH)
Requires:       filesystem
%description
This library provides the basic routines for allocating memory,
searching directories, opening and closing files, reading and
writing files, string handling, pattern matching, arithmetic,
and so on.

%package devel
Summary: Header files for glibc
Group: Applications/System
Requires: glibc >= 2.22
%description devel
These are the header files of glibc.

%package lang
Summary: Additional language files for glibc
Group: Applications/System
Requires: glibc >= 2.22
%description lang
These are the additional language files of glibc.

%prep
%setup -q
sed -i 's/\\$$(pwd)/`pwd`/' timezone/Makefile
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1
%patch24 -p1
%patch25 -p1
%patch26 -p1
%patch27 -p1

install -vdm 755 %{_builddir}/%{name}-build
# do not try to explicitly provide GLIBC_PRIVATE versioned libraries
%define __find_provides %{_builddir}/%{name}-%{version}/find_provides.sh
%define __find_requires %{_builddir}/%{name}-%{version}/find_requires.sh

# create find-provides and find-requires script in order to ignore GLIBC_PRIVATE errors
cat > find_provides.sh << _EOF
#! /bin/sh
if [ -d /tools ]; then
/tools/lib/rpm/find-provides | grep -v GLIBC_PRIVATE
else
%{_prefix}/lib/rpm/find-provides | grep -v GLIBC_PRIVATE
fi
exit 0
_EOF
chmod +x find_provides.sh

cat > find_requires.sh << _EOF
#! /bin/sh
if [ -d /tools ]; then
/tools/lib/rpm/find-requires %{buildroot} %{glibc_target_cpu} | grep -v GLIBC_PRIVATE
else
%{_prefix}/lib/rpm/find-requires %{buildroot} %{glibc_target_cpu} | grep -v GLIBC_PRIVATE
fi
_EOF
chmod +x find_requires.sh
#___EOF

%build
cd %{_builddir}/%{name}-build
../%{name}-%{version}/configure \
    --prefix=%{_prefix} \
    --disable-profile \
    --enable-kernel=2.6.32 \
    --enable-obsolete-rpc \
    --disable-silent-rules
make %{?_smp_mflags}
%check
cd %{_builddir}/glibc-build
make -k check > %{_topdir}/LOGS/%{name}-check.log 2>&1 || true
%install
#   Do not remove static libs
pushd %{_builddir}/glibc-build
#   Create directories
make install_root=%{buildroot} install
install -vdm 755 %{buildroot}%{_sysconfdir}/ld.so.conf.d
install -vdm 755 %{buildroot}/var/cache/nscd
install -vdm 755 %{buildroot}%{_libdir}/locale
cp -v ../%{name}-%{version}/nscd/nscd.conf %{buildroot}%{_sysconfdir}/nscd.conf
#   Install locale generation script and config file
cp -v %{SOURCE2} %{buildroot}%{_sysconfdir}
cp -v %{SOURCE1} %{buildroot}/sbin
#   Remove unwanted cruft
rm -rf %{buildroot}%{_infodir}
#   Install configuration files
cat > %{buildroot}%{_sysconfdir}/nsswitch.conf <<- "EOF"
#   Begin /etc/nsswitch.conf

    passwd: files
    group: files
    shadow: files

    hosts: files dns
    networks: files

    protocols: files
    services: files
    ethers: files
    rpc: files
#   End /etc/nsswitch.conf
EOF
cat > %{buildroot}%{_sysconfdir}/ld.so.conf <<- "EOF"
#   Begin /etc/ld.so.conf
    /usr/local/lib
    /opt/lib
    include /etc/ld.so.conf.d/*.conf
EOF
popd
%find_lang %{name} --all-name

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%dir %{_localstatedir}/cache/nscd
%dir %{_libdir}/locale
%dir %{_sysconfdir}/ld.so.conf.d
%config(noreplace) %{_sysconfdir}/nsswitch.conf
%config(noreplace) %{_sysconfdir}/ld.so.conf
%config(noreplace) %{_sysconfdir}/rpc
%config(missingok,noreplace) %{_sysconfdir}/ld.so.cache
%config %{_sysconfdir}/locale-gen.conf
%config(noreplace) %{_sysconfdir}/nscd.conf
%ifarch x86_64
/lib64/*
%{_lib64dir}/gconv/*
%{_lib64dir}/audit/*
%{_lib64dir}/*.so
%else
%{_lib}/*
%endif
/sbin/*
%{_bindir}/*
%{_libexecdir}/*
%{_sbindir}/*
%{_datadir}/i18n/charmaps/*.gz
%{_datadir}/i18n/locales/*
%{_localstatedir}/lib/nss_db/Makefile
%exclude /usr/bin/mtrace

%files devel
%defattr(-,root,root)
# TODO: Excluding for now to remove dependency on PERL
# /usr/bin/mtrace
%ifarch x86_64
%{_lib64dir}/*.a
%{_lib64dir}/*.o
%endif
%{_includedir}/*

%files -f %{name}.lang lang
%defattr(-,root,root)
%{_datarootdir}/locale/locale.alias

%changelog
*   Tue Jan 29 2019 Keerthana K <keerthanak@vmware.com> 2.22-23
-   Fix for CVE-2017-12132.
*   Thu Aug 09 2018 Keerthana K <keerthanak@vmware.com> 2.22-22
-   Fix for CVE-2017-15761.
*   Tue Jun 26 2018 Keerthana K <keerthnanak@vmware.com> 2.22-21
-   Fix for CVE-2018-11236.
*   Mon Jun 25 2018 Keerthana K <keerthanak@vmware.com> 2.22-20
-   Fix for CVE-2017-18269.
*   Tue Jan 20 2018 Xiaolin Li <xiaolinl@vmware.com> 2.22-19
-   Fix CVE-2018-1000001 and CVE-2018-6485
*   Mon Jan 08 2018 Xiaolin Li <xiaolinl@vmware.com> 2.22-18
-   Fix CVE-2017-16997
*   Tue Dec 5 2017 Anish Swaminathan <anishs@vmware.com> 2.22-17
-   Fix CVE-2016-5417
*   Tue Nov 14 2017 Xiaolin Li <xiaolinl@vmware.com> 2.22-16
-   Fix CVE-2015-5180
*   Wed Oct 25 2017 Xiaolin Li <xiaolinl@vmware.com> 2.22-15
-   Fix CVE-2017-15670, CVE-2017-15804
*   Thu Oct 19 2017 Xiaolin Li <xiaolinl@vmware.com> 2.22-14
-   Fix CVE-2017-12133
*   Thu Jun 29 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.22-13
-   Apply related patches for CVE-2017-1000366
*   Thu Jun 29 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.22-12
-   Fix CVE-2017-1000366
*   Wed Jun 07 2017 Bo Gan <ganb@vmware.com> 2.22-11
-   Fix post/postun
*   Tue Apr 18 2017 Alexey Makhalov <amakhalov@vmware.com> 2.22-10
-   Fix CVE-2016-3075, CVE-2016-3706, CVE-2016-1234 and CVE-2016-4429
*   Wed Sep 28 2016 Alexey Makhalov <amakhalov@vmware.com> 2.22-9
-   Added pthread_create-fix-use-after-free.patch
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.22-8
-   GA - Bump release of all rpms
*   Mon May 23 2016 Divya Thaluru <dthaluru@vmware.com> 2.22-7
-   Added patch for CVE-2014-9761
*   Mon Mar 21 2016 Alexey Makhalov <amakhalov@vmware.com>  2.22-6
-   Security hardening: nonow
*   Fri Mar 18 2016 Anish Swaminathan <anishs@vmware.com>  2.22-5
-   Change conf file qualifiers
*   Fri Mar 11 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com>  2.22-4
-   Added patch for res_qeury assertion with bad dns config
-   Details: https://sourceware.org/bugzilla/show_bug.cgi?id=19791
*   Tue Feb 16 2016 Anish Swaminathan <anishs@vmware.com>  2.22-3
-   Added patch for CVE-2015-7547
*   Mon Feb 08 2016 Anish Swaminathan <anishs@vmware.com>  2.22-2
-   Added patch for bindresvport blacklist
*   Tue Jan 12 2016 Xiaolin Li <xiaolinl@vmware.com> 2.22-1
-   Updated to version 2.22
*   Tue Dec 1 2015 Divya Thaluru <dthaluru@vmware.com> 2.19-8
-   Disabling rpm debug package and stripping the libraries
*   Wed Nov 18 2015 Divya Thaluru <dthaluru@vmware.com> 2.19-7
-   Adding patch to close nss files database
*   Tue Nov 10 2015 Xiaolin Li <xiaolinl@vmware.com> 2.19-6
-   Handled locale files with macro find_lang
*   Wed Aug 05 2015 Kumar Kaushik <kaushikk@vmware.com> 2.19-5
-   Adding postun section for ldconfig.
*   Tue Jul 28 2015 Alexey Makhalov <amakhalov@vmware.com> 2.19-4
-   Support glibc building against current rpm version.
*   Thu Jul 23 2015 Divya Thaluru <dthaluru@vmware.com> 2.19-3
-   Packing locale-gen scripts
*   Mon May 18 2015 Touseef Liaqat <tliaqat@vmware.com> 2.19-2
-   Update according to UsrMove.
*   Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 2.19-1
-   Initial build. First version
