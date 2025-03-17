%global security_hardening nonow
%define glibc_target_cpu %{_build}
%global __brp_elfperms  /bin/true

Summary:        Main C library
Name:           glibc
Version:        2.36
Release:        16%{?dist}
URL:            http://www.gnu.org/software/libc
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://ftp.gnu.org/gnu/glibc/%{name}-%{version}.tar.xz

Source1:        locale-gen.sh
Source2:        locale-gen.conf
Source3:        v2.36.patches
Source4:        license.txt
%include        %{SOURCE4}

#Patch taken from http://www.linuxfromscratch.org/patches/downloads/glibc/glibc-2.31-fhs-1.patch
Patch0:         glibc-2.31-fhs-1.patch
Patch1:         0002-malloc-arena-fix.patch

#release branch patches
#generate using ./tools/scripts/generate-glibc-release-patches.sh %{version}
%include %{SOURCE3}

Provides:       rtld(GNU_HASH)
Provides:       /sbin/ldconfig

Requires:       filesystem
Requires:       %{name}-libs = %{version}-%{release}

Conflicts:      %{name}-i18n < 2.36-4

%define ExtraBuildRequires bison, python3, python3-libs

%description
This library provides the basic routines for allocating memory,
searching directories, opening and closing files, reading and
writing files, string handling, pattern matching, arithmetic,
and so on.

%package libs
Summary:    glibc shared library
Group:      System/Libraries
Conflicts:  %{name} < 2.36-5

%description libs
This subpackage contains the implementation as a shared library.

%package    devel
Summary:    Header files for glibc
Group:      Applications/System
Requires:   %{name} = %{version}-%{release}

%description devel
These are the header files of glibc.

%package    lang
Summary:    Additional language files for glibc
Group:      Applications/System
Requires:   %{name} = %{version}-%{release}

%description lang
These are the additional language files of glibc.

%package    i18n
Summary:    Additional internationalization files for glibc
Group:      Applications/System
Requires:   %{name} = %{version}-%{release}

%description i18n
These are the additional internationalization files of glibc.

%package    iconv
Summary:    gconv modules for glibc
Group:      Applications/System
Requires:   %{name} = %{version}-%{release}

%description iconv
These is gconv modules for iconv() and iconv tools.

%package    tools
Summary:    tools for glibc
Group:      Applications/System
Requires:   %{name} = %{version}-%{release}

%description tools
Extra tools for glibc.

%package    nscd
Summary:    Name Service Cache Daemon
Group:      Applications/System
Requires:   %{name} = %{version}-%{release}

%description nscd
Name Service Cache Daemon

%prep
%autosetup -p1
sed -i 's/\\$$(pwd)/`pwd`/' timezone/Makefile
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
  %{_libdir}/rpm/find-provides | grep -v GLIBC_PRIVATE
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
        --host=%{_host} --build=%{_build} \
        CFLAGS="%{optflags}" \
        CXXFLAGS="%{optflags}" \
        --program-prefix=%{?_program_prefix} \
        --disable-dependency-tracking \
        --prefix=%{_prefix} \
        --exec-prefix=%{_prefix} \
        --bindir=%{_bindir} \
        --sbindir=%{_sbindir} \
        --sysconfdir=%{_sysconfdir} \
        --datadir=%{_datadir} \
        --includedir=%{_includedir} \
        --libdir=%{_libdir} \
        --libexecdir=%{_libexecdir} \
        --localstatedir=%{_localstatedir} \
        --sharedstatedir=%{_sharedstatedir} \
        --mandir=%{_mandir} \
        --infodir=%{_infodir} \
        --disable-profile \
        --disable-werror \
        --enable-static-pie \
        --enable-kernel=3.2 \
        --enable-bind-now \
        --enable-stack-protector=strong \
        --disable-experimental-malloc \
        --disable-silent-rules \
        --disable-crypt \
        libc_cv_slibdir=%{_libdir}

# Sometimes we have false "out of memory" make error
# just rerun/continue make to workaroung it.
%make_build || %make_build || %make_build

%install
#       Do not remove static libs
pushd %{_builddir}/glibc-build
#       Create directories
make install_root=%{buildroot} install %{?_smp_mflags}
install -vdm 755 %{buildroot}%{_sysconfdir}/ld.so.conf.d
install -vdm 755 %{buildroot}%{_sharedstatedir}/cache/nscd
install -vdm 755 %{buildroot}%{_libdir}/locale
cp -v ../%{name}-%{version}/nscd/nscd.conf %{buildroot}%{_sysconfdir}/nscd.conf
#       Install locale generation script and config file
cp -v %{SOURCE2} %{buildroot}%{_sysconfdir}
cp -v %{SOURCE1} %{buildroot}%{_sbindir}
#       Remove unwanted cruft
rm -rf %{buildroot}%{_infodir}
#       Install configuration files

cat > %{buildroot}%{_sysconfdir}/nsswitch.conf <<- "EOF"
#       Begin /etc/nsswitch.conf

passwd: files
group: files
shadow: files

hosts: files dns
networks: files

protocols: files
services: files
ethers: files
rpc: files
#       End /etc/nsswitch.conf
EOF
cat > %{buildroot}%{_sysconfdir}/ld.so.conf <<- "EOF"
#       Begin /etc/ld.so.conf
    /usr/local/lib
    /opt/lib
    include %{_sysconfdir}/ld.so.conf.d/*.conf
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

I18NPATH=. GCONV_PATH=../../glibc-build/iconvdata LC_ALL=C ../../glibc-build/elf/ld.so --library-path ../../glibc-build $LOCALEDEF --no-archive --prefix=%{buildroot} -A ../intl/locale.alias -i locales/en_US -c -f charmaps/UTF-8 en_US.UTF-8

mv %{buildroot}%{_libdir}/locale/en_US.utf8 %{buildroot}%{_libdir}/locale/en_US.UTF-8

popd

mv %{buildroot}/sbin/* %{buildroot}/%{_sbindir}
rmdir %{buildroot}/sbin

%if 0%{?with_check}
%check
cd %{_builddir}/glibc-build
make %{?_smp_mflags} check ||:
# These 2 persistant false positives are OK
# XPASS for: elf/tst-protected1a and elf/tst-protected1b
[ $(grep ^XPASS tests.sum | wc -l) -ne 2 -a $(grep "^XPASS: elf/tst-protected1[ab]" tests.sum | wc -l) -ne 2 ] && exit 1 ||:

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
[ $(grep ^FAIL tests.sum | wc -l) -ne $n ] && exit 1 ||:
%endif

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

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
%config(noreplace) %{_sysconfdir}/nsswitch.conf
%config(noreplace) %{_sysconfdir}/ld.so.conf
%config(noreplace) %{_sysconfdir}/rpc
%attr(0644,root,root) %config(missingok,noreplace) %{_sysconfdir}/ld.so.cache
%config %{_sysconfdir}/locale-gen.conf
%{_sbindir}/ldconfig
%{_sbindir}/locale-gen.sh
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
%exclude %{_bindir}/iconv
%exclude %{_bindir}/mtrace
%exclude %{_bindir}/pcprofiledump
%exclude %{_bindir}/pldd
%exclude %{_bindir}/sotruss
%exclude %{_bindir}/sprof
%exclude %{_bindir}/xtrace

%files libs
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/*.so.*
%exclude %{_libdir}/libpcprofile.so

%files iconv
%defattr(-,root,root)
%{_libdir}/gconv/*
%{_bindir}/iconv
%{_sbindir}/iconvconfig

%files tools
%defattr(-,root,root)
%{_bindir}/mtrace
%{_bindir}/pcprofiledump
%{_bindir}/pldd
%{_bindir}/sotruss
%{_bindir}/sprof
%{_bindir}/xtrace
%{_bindir}/zdump
%{_sbindir}/zic
%{_sbindir}/sln
%{_libdir}/audit/*
%{_libdir}/libpcprofile.so

%files nscd
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/nscd.conf
%{_sbindir}/nscd
%dir %{_sharedstatedir}/cache/nscd

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
%{_libdir}/*.a
%{_libdir}/*.o
%{_includedir}/*

%files -f %{name}.lang lang
%defattr(-,root,root)

%changelog
* Wed Dec 11 2024 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 2.36-16
- Release bump for SRP compliance
* Thu Nov 14 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.36-15
- Disable libcrypt as a part of yescrypt addition
* Fri Nov 08 2024 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 2.36-14
- Remove standalone license exceptions
* Tue Sep 24 2024 Mukul Sikka <mukul.sikka@broadcom.com> 2.36-13
- Bump version to generate SRP provenance file
* Wed Jul 17 2024 Harinadh D <Harinadh.Dommaraju@broadcom.com> 2.36-12
- Enable static-pie support
* Tue May 28 2024 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 2.36-11
- Fix CVEs on nscd
- Sync release branch patches
* Tue Apr 16 2024 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 2.36-10
- Fix for CVE-2024-2961.patch
* Tue Jan 23 2024 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 2.36-9
- Fix for CVE-2023-6246, CVE-2023-6779, CVE-2023-6780
* Thu Oct 05 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 2.36-8
- Update patches from release branch
- Fix for CVE-2023-4527
* Tue Oct 03 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 2.36-7
- Fix for CVE-2023-4806/2023-5156
* Tue Jun 27 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 2.36-6
- Fix for CVE-2022-39046
* Thu May 11 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.36-5
- Add libs sub package
* Fri Apr 07 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.36-4
- Fix locale generation issue by packaging files properly
* Fri Jan 20 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.36-3
- Don't change elf permissions in glibc
* Tue Jan 17 2023 Piyush Gupta <gpiyush@vmware.com> 2.36-2
- Remove spaces from /etc/nsswitch.conf to avoid failure while adding altfiles.
* Wed Aug 17 2022 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 2.36-1
- Upgrade to 2.36
- catchsegv is removed, zdump is moved to /usr/bin from /usr/sbin
* Fri Sep 17 2021 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 2.32-8
- Fix LTP Testcase (semctl) failure issue
* Tue Sep 07 2021 Keerthana K <keerthanak@vmware.com> 2.32-7
- Fix CVE-2021-38604
* Wed Aug 04 2021 Keerthana K <keerthanak@vmware.com> 2.32-6
- Fix CVE-2021-35942
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
