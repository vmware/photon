Summary:        Contains a linker, an assembler, and other tools
Name:           binutils
Version:        2.35
Release:        2%{?dist}
License:        GPLv2+
URL:            http://www.gnu.org/software/binutils
Group:          System Environment/Base
Vendor:         VMware, Inc.
Distribution:   Photon
Requires:       %{name}-libs = %{version}-%{release}
%if %{with_check}
BuildRequires:  dejagnu
BuildRequires:  bc
%endif
Source0:        http://ftp.gnu.org/gnu/binutils/%{name}-%{version}.tar.xz
%define sha1 binutils=6bdd090ce268b6d6c3442516021c4e4b5019e303
Patch1:         binutils-sync-libiberty-add-no-recurse-limit-make-check-fix.patch
Patch2:         binutils-CVE-2019-1010204.patch
Patch3:         binutils-CVE-2021-3487.patch

%description
The Binutils package contains a linker, an assembler,
and other tools for handling object files.

%package    libs
Summary:    Shared library files for binutils
Obsoletes:  binutils <= 2.32-1

%description    libs
It contains the binutils shared libraries that applications can link
to at runtime.

%package    devel
Summary:    Header and development files for binutils
Requires:   %{name} = %{version}

%description    devel
It contains the libraries and header files to create applications
for handling compiled objects.

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
sed -i '/@\tincremental_copy/d' gold/testsuite/Makefile.in
%configure \
            --enable-gold       \
            --enable-ld=default \
            --enable-plugins    \
            --enable-shared     \
            --enable-targets=x86_64-unknown-linux-gnu,aarch64-unknown-linux-gnu \
            --disable-werror    \
            --with-system-zlib  \
	    --enable-install-libiberty \
            --disable-silent-rules
make %{?_smp_mflags} tooldir=%{_prefix}
%install
make %{?_smp_mflags} DESTDIR=%{buildroot} tooldir=%{_prefix} install
find %{buildroot} -name '*.la' -delete
# Don't remove libiberity.a
rm -rf %{buildroot}/%{_infodir}
%find_lang %{name} --all-name

%check
# Disable gcc hardening as it will affect some tests.
rm `dirname $(gcc --print-libgcc-file-name)`/../specs
make %{?_smp_mflags} -k check > tests.sum 2>&1


%files -f %{name}.lang
%defattr(-,root,root)
%{_bindir}/dwp
%{_bindir}/gprof
%{_bindir}/ld.bfd
%{_bindir}/ld.gold
%{_bindir}/c++filt
%{_bindir}/objdump
%{_bindir}/as
%{_bindir}/ar
%{_bindir}/objcopy
%{_bindir}/strings
%{_bindir}/addr2line
%{_bindir}/nm
%{_bindir}/size
%{_bindir}/ld
%{_bindir}/elfedit
%{_bindir}/ranlib
%{_bindir}/readelf
%{_bindir}/strip
%{_libdir}/ldscripts/*
%{_mandir}/man1/readelf.1.gz
%{_mandir}/man1/windmc.1.gz
%{_mandir}/man1/ranlib.1.gz
%{_mandir}/man1/gprof.1.gz
%{_mandir}/man1/strip.1.gz
%{_mandir}/man1/c++filt.1.gz
%{_mandir}/man1/as.1.gz
%{_mandir}/man1/objcopy.1.gz
%{_mandir}/man1/elfedit.1.gz
%{_mandir}/man1/strings.1.gz
%{_mandir}/man1/nm.1.gz
%{_mandir}/man1/ar.1.gz
%{_mandir}/man1/ld.1.gz
%{_mandir}/man1/dlltool.1.gz
%{_mandir}/man1/addr2line.1.gz
%{_mandir}/man1/windres.1.gz
%{_mandir}/man1/size.1.gz
%{_mandir}/man1/objdump.1.gz

%post   libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files libs
%{_libdir}/libbfd-%{version}.so
%{_libdir}/libctf.so*
%{_libdir}/libctf-nobfd.so*
%{_libdir}/libopcodes-%{version}.so

%files devel
%{_includedir}/bfd_stdint.h
%{_includedir}/ctf.h
%{_includedir}/ctf-api.h
%{_includedir}/plugin-api.h
%{_includedir}/symcat.h
%{_includedir}/bfd.h
%{_includedir}/ansidecl.h
%{_includedir}/bfdlink.h
%{_includedir}/dis-asm.h
%{_includedir}/libiberty/*
%{_includedir}/diagnostics.h
%{_libdir}/libbfd.a
%{_libdir}/libbfd.so
%{_libdir}/libctf.a
%{_libdir}/libctf-nobfd.a
%{_libdir}/libopcodes.a
%{_libdir}/libopcodes.so
%{_lib64dir}/libiberty.a

%changelog
*   Wed Apr 28 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 2.35-2
-   Fix CVE-2021-3487
*   Tue Sep 08 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 2.35-1
-   Update binutils to 2.35
*   Fri Mar 13 2020 Alexey Makhalov <amakhalov@vmware.com> 2.34-1
-   Version update.
*   Tue Nov 26 2019 Alexey Makhalov <amakhalov@vmware.com> 2.32-4
-   Support for aarch64 target to be able to strip aarch64 libraries
    during cross-aarch64-gcc build
*   Wed Nov 13 2019 Satya Naga Vasamsetty <svasamsetty@vmware.com> 2.32-3
-   Fix CVE-2019-17450 and CVE-2019-17451
*   Sun Sep 29 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 2.32-2
-   Separate out libbfd and libopcodes shared libraries into
-   binutils-libs sub-package.
*   Mon Aug 26 2019 Satya Naga Vasamsetty <svasamsetty@vmware.com> 2.32-1
-   Update version to 2.32, fix CVE-2019-1010204, fix a make check failure
*   Mon Aug 12 2019 Satya Naga Vasamsetty <svasamsetty@vmware.com> 2.31.1-6
-   Fix CVE-2019-14444, CVE-2019-12972, CVE-2019-14250
*   Thu Jun 20 2019 Vikash Bansal <bvikas@vmware.com> 2.31.1-5
-   Fix CVE-2018-20623, CVE-2018-20671, CVE-2018-20651,
-   CVE-2018-17794-18700-18701-18484, CVE-2019-9071, CVE-2019-9073 and CVE-2019-9074
*   Thu Mar 14 2019 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.31.1-4
-   Fix CVE-2019-9075 and CVE-2019-9077
*   Tue Jan 22 2019 Anish Swaminathan <anishs@vmware.com> 2.31.1-3
-   fix CVE-2018-1000876
*   Tue Jan 08 2019 Alexey Makhalov <amakhalov@vmware.com> 2.31.1-2
-   Fix CVE-2018-17358, CVE-2018-17359 and CVE-2018-17360
*   Fri Sep 21 2018 Keerthana K <keerthanak@vmware.com> 2.31.1-1
-   Update to version 2.31.1
*   Wed Aug 1 2018 Keerthana K <keerthanak@vmware.com> 2.31-1
-   Update to version 2.31.
*   Thu Jun 7 2018 Keerthana K <keerthanak@vmware.com> 2.30-4
-   Fix CVE-2018-10373
*   Mon Mar 19 2018 Alexey Makhalov <amakhalov@vmware.com> 2.30-3
-   Add libiberty to the -devel package
*   Wed Feb 28 2018 Xiaolin Li <xiaolinl@vmware.com> 2.30-2
-   Fix CVE-2018-6543.
*   Mon Jan 29 2018 Xiaolin Li <xiaolinl@vmware.com> 2.30-1
-   Update to version 2.30
*   Mon Dec 18 2017 Anish Swaminathan <anishs@vmware.com> 2.29.1-5
-   Fix CVEs CVE-2017-17121, CVE-2017-17122, CVE-2017-17123,
-   CVE-2017-17124, CVE-2017-17125
*   Mon Dec 4 2017 Anish Swaminathan <anishs@vmware.com> 2.29.1-4
-   Fix CVEs CVE-2017-16826, CVE-2017-16827, CVE-2017-16828, CVE-2017-16829,
-   CVE-2017-16830, CVE-2017-16831, CVE-2017-16832
*   Tue Nov 14 2017 Alexey Makhalov <amakhalov@vmware.com> 2.29.1-3
-   Aarch64 support
-   Parallel build
*   Thu Oct 12 2017 Anish Swaminathan <anishs@vmware.com> 2.29.1-2
-   Add patch to fix CVE-2017-15020
*   Mon Oct 2 2017 Anish Swaminathan <anishs@vmware.com> 2.29.1-1
-   Version update to 2.29.1, fix CVEs CVE-2017-12799, CVE-2017-14729,CVE-2017-14745
*   Fri Aug 11 2017 Anish Swaminathan <anishs@vmware.com> 2.29-3
-   Apply patches for CVE-2017-12448,CVE-2017-12449,CVE-2017-12450,CVE-2017-12451,
-   CVE-2017-12452,CVE-2017-12453,CVE-2017-12454,CVE-2017-12455,CVE-2017-12456,
-   CVE-2017-12457,CVE-2017-12458,CVE-2017-12459
*   Tue Aug 8 2017 Rongrong Qiu <rqiu@vmware.com> 2.29-2
-   fix for make check for bug 1900247
*   Wed Aug 2 2017 Alexey Makhalov <amakhalov@vmware.com> 2.29-1
-   Version update
*   Tue May 16 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.28-2
-   Patch for CVE-2017-8421
*   Thu Apr 06 2017 Anish Swaminathan <anishs@vmware.com> 2.28-1
-   Upgraded to version 2.28
-   Apply patch for CVE-2017-6969
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.25.1-2
-   GA - Bump release of all rpms
*   Tue Jan 12 2016 Xiaolin Li <xiaolinl@vmware.com> 2.25.1-1
-   Updated to version 2.25.1
*   Tue Nov 10 2015 Xiaolin Li <xiaolinl@vmware.com> 2.25-2
-   Handled locale files with macro find_lang
*   Mon Apr 6 2015 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.25-1
-   Updated to 2.25
*   Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 2.24-1
-   Initial build. First version
