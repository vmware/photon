%global security_hardening nonow
%define glibc_target_cpu %{_build}

Summary:        Main C library
Name:           glibc
Version:        2.32
Release:        20%{?dist}
License:        LGPLv2+
URL:            http://www.gnu.org/software/libc
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://ftp.gnu.org/gnu/glibc/%{name}-%{version}.tar.xz
%define sha512 %{name}=8460c155b7003e04f18dabece4ed9ad77445fa2288a7dc08e80a8fc4c418828af29e0649951bd71a54ea2ad2d4da7570aafd9bdfe4a37e9951b772b442afe50b

Source1:        locale-gen.sh
Source2:        locale-gen.conf
Source3:        nsswitch.conf
Source4:        v2.32.patches

# Patch0 taken from:
# http://www.linuxfromscratch.org/patches/downloads/glibc/glibc-2.31-fhs-1.patch
Patch0:       glibc-2.31-fhs-1.patch
Patch1:       0002-malloc-arena-fix.patch
Patch9:       0001-elf-Refactor-_dl_update_slotinfo-to-avoid-use-after-.patch
Patch10:      0002-elf-Fix-data-races-in-pthread_create-and-TLS-access-.patch
Patch11:      0003-elf-Use-relaxed-atomics-for-racy-accesses-BZ-19329.patch
Patch12:      0004-elf-Fix-DTV-gap-reuse-logic-BZ-27135.patch
Patch13:      0005-elf-Add-test-case-for-BZ-19329.patch

#release branch patches
#generate using ./tools/scripts/generate-glibc-release-patches.sh %{version}
%include %{SOURCE4}

#Additional patches
Patch300:     CVE-2023-4806_CVE-2023-5156.patch
Patch301:     CVE-2023-4813.patch

#fix: CVE-2023-0687
Patch302:     0001_gmon_Fix_allocated_buffer_overflow.patch

Patch303:     CVE-2023-4911.patch

Provides:       rtld(GNU_HASH)
Requires:       filesystem

Conflicts:      %{name}-i18n < 2.32-19

%define ExtraBuildRequires bison, python3, python3-libs

%description
This library provides the basic routines for allocating memory,
searching directories, opening and closing files, reading and
writing files, string handling, pattern matching, arithmetic,
and so on.

%package devel
Summary: Header files for glibc
Group: Applications/System
Requires: %{name} = %{version}-%{release}
%description devel
These are the header files of glibc.

%package lang
Summary: Additional language files for glibc
Group: Applications/System
Requires: %{name} = %{version}-%{release}
%description lang
These are the additional language files of glibc.

%package i18n
Summary: Additional internationalization files for glibc
Group: Applications/System
Requires: %{name} = %{version}-%{release}
%description i18n
These are the additional internationalization files of glibc.

%package iconv
Summary: gconv modules for glibc
Group: Applications/System
Requires: %{name} = %{version}-%{release}
%description iconv
These is gconv modules for iconv() and iconv tools.

%package tools
Summary: tools for glibc
Group: Applications/System
Requires: %{name} = %{version}-%{release}
%description tools
Extra tools for glibc.

%package nscd
Summary: Name Service Cache Daemon
Group: Applications/System
Requires: %{name} = %{version}-%{release}
%description nscd
Name Service Cache Daemon

%prep
# Using autosetup is not feasible
%setup -q
sed -i 's/\\$$(pwd)/`pwd`/' timezone/Makefile
%autopatch -p1 -m0 -M19
# Release branch patches
%autopatch -p1 -m101 -M247

# Additional patches
%autopatch -p1 -m300 -M304

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
%{_libdir}/rpm/find-requires %{buildroot} %{glibc_target_cpu} | grep -v GLIBC_PRIVATE
fi
_EOF
chmod +x find_requires.sh

%build

cd %{_builddir}/%{name}-build
../%{name}-%{version}/configure \
        --prefix=%{_prefix} \
        --build=%{_build} \
        --host=%{_host} \
        --disable-profile \
        --disable-werror \
        --enable-kernel=3.2 \
        --enable-bind-now \
        --enable-stack-protector=strong \
        --disable-experimental-malloc \
        --disable-silent-rules \
        libc_cv_slibdir=/lib

# Sometimes we have false "out of memory" make error
# just rerun/continue make to workaround it.
%make_build || %make_build || %make_build

%install
#       Do not remove static libs
pushd %{_builddir}/glibc-build
#       Create directories
%make_install install_root=%{buildroot}
install -vdm 755 %{buildroot}%{_sysconfdir}/ld.so.conf.d
install -vdm 755 %{buildroot}%{_var}/cache/nscd
install -vdm 755 %{buildroot}%{_libdir}/locale
cp -v ../%{name}-%{version}/nscd/nscd.conf %{buildroot}%{_sysconfdir}/nscd.conf
#       Install locale generation script and config file
cp -v %{SOURCE2} %{buildroot}%{_sysconfdir}
cp -v %{SOURCE1} %{buildroot}/sbin
#       Remove unwanted cruft
rm -rf %{buildroot}%{_infodir}
#       Install configuration files

cp -pv %{SOURCE3} %{buildroot}%{_sysconfdir}

cat > %{buildroot}%{_sysconfdir}/ld.so.conf <<- "EOF"
#       Begin /etc/ld.so.conf
    %{_usr}/local/lib
    /opt/lib
    include /etc/ld.so.conf.d/*.conf
EOF
# Create empty ld.so.cache
:> %{buildroot}%{_sysconfdir}/ld.so.cache
popd

%find_lang %{name} --all-name
pushd localedata
# Generate out of locale-archive an (en_US.) UTF-8 locale
mkdir -p %{buildroot}%{_libdir}/locale
if [ %{_host} != %{_build} ]; then
LOCALEDEF=localedef
else
LOCALEDEF=../../glibc-build/locale/localedef
fi
I18NPATH=. GCONV_PATH=../../glibc-build/iconvdata LC_ALL=C $LOCALEDEF --no-archive --prefix=%{buildroot} -A ../intl/locale.alias -i locales/en_US -c -f charmaps/UTF-8 en_US.UTF-8
mv %{buildroot}%{_libdir}/locale/en_US.utf8 %{buildroot}%{_libdir}/locale/en_US.UTF-8
popd
# to do not depend on /bin/bash
sed -i 's@#! /bin/bash@#! /bin/sh@' %{buildroot}%{_bindir}/ldd
sed -i 's@#!/bin/bash@#!/bin/sh@' %{buildroot}%{_bindir}/tzselect

%check
cd %{_builddir}/glibc-build
%make_build check ||:
# These 2 persistant false positives are OK
# XPASS for: elf/tst-protected1a and elf/tst-protected1b
[ `grep ^XPASS tests.sum | wc -l` -ne 2 -a `grep "^XPASS: elf/tst-protected1[ab]" tests.sum | wc -l` -ne 2 ] && exit 1 ||:

# FAIL (intermittent) in chroot but PASS in container:
# posix/tst-spawn3 and stdio-common/test-vfprintf
n=0

grep "^FAIL: c++-types-check" tests.sum >/dev/null && n=$((n+1)) ||:
# can fail in chroot
grep "^FAIL: io/tst-fchownat" tests.sum >/dev/null && n=$((n+1)) ||:
grep "^FAIL: malloc/tst-tcfree2" tests.sum >/dev/null && n=$((n+1)) ||:
# can timeout
grep "^FAIL: nptl/tst-mutex10" tests.sum >/dev/null && n=$((n+1)) ||:
# can fail in chroot
grep "^FAIL: nptl/tst-setuid3" tests.sum >/dev/null && n=$((n+1)) ||:
grep "^FAIL: stdlib/tst-secure-getenv" tests.sum >/dev/null && n=$((n+1)) ||:
grep "^FAIL: support/tst-support_descriptors" tests.sum >/dev/null && n=$((n+1)) ||:
#https://sourceware.org/glibc/wiki/Testing/Testsuite
grep "^FAIL: nptl/tst-eintr1" tests.sum >/dev/null && n=$((n+1)) ||:
#This happens because the kernel fails to reap exiting threads fast enough,
#eventually resulting an EAGAIN when pthread_create is called within the test.

# check for exact 'n' failures
[ `grep ^FAIL tests.sum | wc -l` -ne $n ] && exit 1 ||:

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%posttrans iconv
%{_sbindir}/iconvconfig

%postun iconv
if [ -e %{_lib64dir}/gconv/gconv-modules.cache ]; then
  rm %{_lib64dir}/gconv/gconv-modules.cache
fi

%files
%defattr(-,root,root)
%{_libdir}/locale/*
%dir %{_sysconfdir}/ld.so.conf.d
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/nsswitch.conf
%config(noreplace) %{_sysconfdir}/ld.so.conf
%config(noreplace) %{_sysconfdir}/rpc
%attr(0644,root,root) %config(missingok,noreplace) %{_sysconfdir}/ld.so.cache
%config %{_sysconfdir}/locale-gen.conf
/lib/*
%exclude /lib/libpcprofile.so
%{_libdir}/*.so
/sbin/ldconfig
/sbin/locale-gen.sh
%{_bindir}/*
%{_libexecdir}/*
%{_datadir}/i18n/charmaps/UTF-8.gz
%{_datadir}/i18n/charmaps/ISO-8859-1.gz
%{_datadir}/i18n/locales/en_US
%{_datadir}/i18n/locales/en_GB
%{_datadir}/i18n/locales/i18n*
%{_datadir}/i18n/locales/iso14651_t1
%{_datadir}/i18n/locales/iso14651_t1_common
%{_datadir}/i18n/locales/translit_*
%{_datadir}/locale/locale.alias
%exclude %{_sharedstatedir}/nss_db/Makefile
%exclude %{_bindir}/catchsegv
%exclude %{_bindir}/iconv
%exclude %{_bindir}/mtrace
%exclude %{_bindir}/pcprofiledump
%exclude %{_bindir}/pldd
%exclude %{_bindir}/sotruss
%exclude %{_bindir}/sprof
%exclude %{_bindir}/xtrace

%files iconv
%defattr(-,root,root)
%{_libdir}/gconv/*
%{_bindir}/iconv
%{_sbindir}/iconvconfig

%files tools
%defattr(-,root,root)
%{_bindir}/catchsegv
%{_bindir}/mtrace
%{_bindir}/pcprofiledump
%{_bindir}/pldd
%{_bindir}/sotruss
%{_bindir}/sprof
%{_bindir}/xtrace
%{_sbindir}/zdump
%{_sbindir}/zic
/sbin/sln
%{_libdir}/audit/*
/lib/libpcprofile.so

%files nscd
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/nscd.conf
%{_sbindir}/nscd
%dir %{_localstatedir}/cache/nscd

%files i18n
%defattr(-,root,root)
%{_datadir}/i18n/charmaps/*.gz
%{_datadir}/i18n/locales/*
%exclude %{_datadir}/i18n/charmaps/UTF-8.gz
%exclude %{_datadir}/i18n/charmaps/ISO-8859-1.gz
%exclude %{_datadir}/i18n/locales/en_US
%exclude %{_datadir}/i18n/locales/en_GB
%exclude %{_datadir}/i18n/locales/i18n*
%exclude %{_datadir}/i18n/locales/iso14651_t1
%exclude %{_datadir}/i18n/locales/iso14651_t1_common
%exclude %{_datadir}/i18n/locales/translit_*

%files devel
%defattr(-,root,root)
# TODO: Excluding for now to remove dependency on PERL
# %%{_bindir}/mtrace
%{_libdir}/*.a
%{_libdir}/*.o
%{_includedir}/*

%files -f %{name}.lang lang
%defattr(-,root,root)

%changelog
* Wed Nov 27 2024 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 2.32-20
- Adjust nsswitch.conf formatting
* Sun Jun 30 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.32-19
- Fix locale generation issue by packaging files properly
* Tue May 28 2024 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 2.32-18
- Fix CVEs reported on nscd
- Sync branch patches
* Tue Apr 16 2024 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 2.32-17
- Fix CVE-2024-2961
* Fri Mar 22 2024 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 2.32-16
- Fix CVE-2023-4911
- Sync with branch
* Fri Jan 12 2024 Ajay Kaher <akaher@vmware.com> 2.32-15
- Fix CVE-2023-0687
* Fri Dec 22 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 2.32-14
- Update patches from release branch
- Fix CVE-2023-4806, CVE-2023-5156
* Thu Dec 21 2023 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.32-13
- Fix nsswitch.conf permissions
* Fri Oct 13 2023 Ajay Kaher <akaher@vmware.com> 2.32-12
- Fix CVE-2023-4813
* Mon Jan 24 2022 Ajay Kaher <akaher@vmware.com> 2.32-11
- Fix CVE-2022-23218, CVE-2022-23219
* Fri Aug 27 2021 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 2.32-10
- Fix LTP Testcase (semctl) failure issue
* Wed Aug 25 2021 Keerthana K <keerthanak@vmware.com> 2.32-9
- Fix CVE-2021-38604
* Wed Aug 04 2021 Keerthana K <keerthanak@vmware.com> 2.32-8
- Fix CVE-2021-35942
* Wed Jun 30 2021 Srinidhi Rao <srinidhir@vmware.com> 2.32-7
- Fix racy access issues in dl-open & dl-tls.
* Wed Jun 02 2021 Ajay Kaher <akaher@vmware.com> 2.32-6
- Fix CVE-2021-33574
* Thu Apr 01 2021 Ajay Kaher <akaher@vmware.com> 2.32-5
- Fix CVE-2020-27618
* Thu Mar 11 2021 Ajay Kaher <akaher@vmware.com> 2.32-4
- Fix CVE-2019-25013, CVE-2021-3326, CVE-2020-29562
* Wed Mar 03 2021 Tapas Kundu <tkundu@vmware.com> 2.32-3
- Fix FMA4 detection in ifunc
* Mon Nov 30 2020 Ajay Kaher <akaher@vmware.com> 2.32-2
- Added post for glibc-iconv, to have:
- fast-loading gconv module configuration cache file
* Mon Aug 24 2020 Keerthana K <keerthanak@vmware.com> 2.32-1
- Update to version 2.32
* Thu Mar 12 2020 Alexey Makhalov <amakhalov@vmware.com> 2.31-1
- Version update. Use /lib
* Tue Sep 24 2019 Alexey Makhalov <amakhalov@vmware.com> 2.28-5
- Cross compilling support
- Create empty ld.so.cache file for all builds (native and cross)
- Use /lib64 for aarch64
* Fri Jul 12 2019 Ankit Jain <ankitja@vmware.com> 2.28-4
- Replaced spaces with tab in nsswitch.conf file
* Fri Mar 08 2019 Alexey Makhalov <amakhalov@vmware.com> 2.28-3
- Fix CVE-2019-9169
* Tue Jan 22 2019 Anish Swaminathan <anishs@vmware.com> 2.28-2
- Fix CVE-2018-19591
* Tue Aug 28 2018 Alexey Makhalov <amakhalov@vmware.com> 2.28-1
- Version update. Disable obsolete rpc (use libtirpc) and nsl.
* Tue Jan 23 2018 Xiaolin Li <xiaolinl@vmware.com> 2.26-10
- Fix CVE-2018-1000001 and CVE-2018-6485
* Mon Jan 08 2018 Xiaolin Li <xiaolinl@vmware.com> 2.26-9
- Fix CVE-2017-16997
* Thu Dec 21 2017 Xiaolin Li <xiaolinl@vmware.com> 2.26-8
- Fix CVE-2017-17426
* Tue Nov 14 2017 Alexey Makhalov <amakhalov@vmware.com> 2.26-7
- Aarch64 support
* Wed Oct 25 2017 Xiaolin Li <xiaolinl@vmware.com> 2.26-6
- Fix CVE-2017-15670 and CVE-2017-15804
* Tue Oct 10 2017 Alexey Makhalov <amakhalov@vmware.com> 2.26-5
- Compile out tcache.
* Fri Sep 15 2017 Bo Gan <ganb@vmware.com> 2.26-4
- exclude tst-eintr1 per official wiki recommendation.
* Tue Sep 12 2017 Alexey Makhalov <amakhalov@vmware.com> 2.26-3
- Fix makecheck for run in docker.
* Tue Aug 29 2017 Alexey Makhalov <amakhalov@vmware.com> 2.26-2
- Fix tunables setter.
- Add malloc arena fix.
- Fix makecheck.
* Tue Aug 15 2017 Alexey Makhalov <amakhalov@vmware.com> 2.26-1
- Version update
* Tue Aug 08 2017 Anish Swaminathan <anishs@vmware.com> 2.25-4
- Apply fix for CVE-2017-1000366
* Thu May 4  2017 Bo Gan <ganb@vmware.com> 2.25-3
- Remove bash dependency in post/postun script
* Fri Apr 21 2017 Alexey Makhalov <amakhalov@vmware.com> 2.25-2
- Added -iconv -tools and -nscd subpackages
* Wed Mar 22 2017 Alexey Makhalov <amakhalov@vmware.com> 2.25-1
- Version update
* Wed Dec 14 2016 Alexey Makhalov <amakhalov@vmware.com> 2.24-1
- Version update
* Wed Nov 23 2016 Alexey Makhalov <amakhalov@vmware.com> 2.22-13
- Install en_US.UTF-8 locale by default
* Wed Nov 16 2016 Alexey Makhalov <amakhalov@vmware.com> 2.22-12
- Added i18n subpackage
* Tue Oct 25 2016 Alexey Makhalov <amakhalov@vmware.com> 2.22-11
- Workaround for build failure with "out of memory" message
* Wed Sep 28 2016 Alexey Makhalov <amakhalov@vmware.com> 2.22-10
- Added pthread_create-fix-use-after-free.patch
* Tue Jun 14 2016 Divya Thaluru <dthaluru@vmware.com> 2.22-9
- Enabling rpm debug package and stripping the libraries
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.22-8
- GA - Bump release of all rpms
* Mon May 23 2016 Divya Thaluru <dthaluru@vmware.com> 2.22-7
- Added patch for CVE-2014-9761
* Mon Mar 21 2016 Alexey Makhalov <amakhalov@vmware.com>  2.22-6
- Security hardening: nonow
* Fri Mar 18 2016 Anish Swaminathan <anishs@vmware.com>  2.22-5
- Change conf file qualifiers
* Fri Mar 11 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com>  2.22-4
- Added patch for res_qeury assertion with bad dns config
- Details: https://sourceware.org/bugzilla/show_bug.cgi?id=19791
* Tue Feb 16 2016 Anish Swaminathan <anishs@vmware.com>  2.22-3
- Added patch for CVE-2015-7547
* Mon Feb 08 2016 Anish Swaminathan <anishs@vmware.com>  2.22-2
- Added patch for bindresvport blacklist
* Tue Jan 12 2016 Xiaolin Li <xiaolinl@vmware.com> 2.22-1
- Updated to version 2.22
* Tue Dec 1 2015 Divya Thaluru <dthaluru@vmware.com> 2.19-8
- Disabling rpm debug package and stripping the libraries
* Wed Nov 18 2015 Divya Thaluru <dthaluru@vmware.com> 2.19-7
- Adding patch to close nss files database
* Tue Nov 10 2015 Xiaolin Li <xiaolinl@vmware.com> 2.19-6
- Handled locale files with macro find_lang
* Wed Aug 05 2015 Kumar Kaushik <kaushikk@vmware.com> 2.19-5
- Adding postun section for ldconfig.
* Tue Jul 28 2015 Alexey Makhalov <amakhalov@vmware.com> 2.19-4
- Support glibc building against current rpm version.
* Thu Jul 23 2015 Divya Thaluru <dthaluru@vmware.com> 2.19-3
- Packing locale-gen scripts
* Mon May 18 2015 Touseef Liaqat <tliaqat@vmware.com> 2.19-2
- Update according to UsrMove.
* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 2.19-1
- Initial build. First version
