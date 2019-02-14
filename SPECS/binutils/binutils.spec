Summary:        Contains a linker, an assembler, and other tools
Name:           binutils
Version:        2.31
Release:        3%{?dist}
License:        GPLv2+
URL:            http://www.gnu.org/software/binutils
Group:          System Environment/Base
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://ftp.gnu.org/gnu/binutils/%{name}-%{version}.tar.xz
%define sha1    binutils=e1a564cd356d2126d2e9a59e8587757634e731aa
Patch0:         binutils-CVE-2018-17794-18700-18701-18484.patch
Patch1:         binutils-CVE-2018-18605.patch
Patch2:         binutils-CVE-2018-18607.patch
Patch3:         binutils-CVE-2018-18606.patch
Patch4:         binutils-CVE-2018-19931.patch
Patch5:         binutils-CVE-2018-1000876.patch

%description
The Binutils package contains a linker, an assembler,
and other tools for handling object files.
%package    devel
Summary:    Header and development files for binutils
Requires:   %{name} = %{version}
%description    devel
It contains the libraries and header files to create applications 
for handling compiled objects.
%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
install -vdm 755 ../binutils-build
cd ../binutils-build
../%{name}-%{version}/configure \
            --prefix=%{_prefix} \
            --enable-gold       \
            --enable-ld=default \
            --enable-plugins    \
            --enable-shared     \
            --disable-werror    \
            --with-system-zlib  \
	    --enable-install-libiberty \
            --disable-silent-rules
make %{?_smp_mflags} tooldir=%{_prefix}
%install
pushd ../binutils-build
make DESTDIR=%{buildroot} tooldir=%{_prefix} install
find %{buildroot} -name '*.la' -delete
# Don't remove libiberity.a
rm -rf %{buildroot}/%{_infodir}
popd
%find_lang %{name} --all-name

%check
cd ../binutils-build
sed -i 's/testsuite/ /g' gold/Makefile
make %{?_smp_mflags} check


%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig
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
%{_libdir}/libbfd-%{version}.so
%{_libdir}/libopcodes-%{version}.so

%files devel
%{_includedir}/plugin-api.h
%{_includedir}/symcat.h
%{_includedir}/bfd.h
%{_includedir}/ansidecl.h
%{_includedir}/bfdlink.h
%{_includedir}/dis-asm.h
%{_includedir}/libiberty/*
%{_includedir}/diagnostics.h
%{_libdir}/libbfd.a
%{_libdir}/libopcodes.a
%{_libdir}/libbfd.so
%{_libdir}/libopcodes.so
%{_lib64dir}/libiberty.a

%changelog
*   Wed Feb 13 2019 Alexey Makhalov <amakhalov@vmware.com> 2.31-3
-   Fix CVE-2018-19931 and CVE-2018-1000876
*   Wed Jan 02 2019 Ankit Jain <ankitja@vmware.com> 2.31-2
-   Fixes for CVE-2018-17794, CVE-2018-18700, CVE-2018-18701
-   CVE-2018-18484, CVE-2018-18605, CVE-2018-18606, CVE-2018-18607
*   Tue Jul 24 2018 Keerthana K <keerthanak@vmware.com> 2.31-1
-   Update to version 2.31.
*   Mon Jun 25 2018 Keerthana K <keerthanak@vmware.com> 2.30-6
-   Fixes for CVE-2018-6759, CVE-2018-6872, CVE-2018-7568, CVE-2018-7569,
-   CVE-2018-7642, CVE-2018-8945, CVE-2018-10372, CVE-2018-10535.
*   Thu Jun 12 2018 Keerthana K <keerthanak@vmware.com> 2.30-5
-   Fix CVE-2018-10373
*   Tue Apr 17 2018 Xiaolin Li <xiaolinl@vmware.com> 2.30-4
-   Fix CVE-2018-7643, CVE-2018-7208
*   Mon Mar 19 2018 Alexey Makhalov <amakhalov@vmware.com> 2.30-3
-   Add libiberty to the -devel package
*   Wed Feb 28 2018 Xiaolin Li <xiaolinl@vmware.com> 2.30-2
-   Fix CVE-2018-6543.
*   Mon Jan 29 2018 Xiaolin Li <xiaolinl@vmware.com> 2.30-1
-   Update to version 2.30
*   Mon Dec 18 2017 Anish Swaminathan <anishs@vmware.com> 2.29.1-4
-   Fix CVEs CVE-2017-17121, CVE-2017-17122, CVE-2017-17123, 
-   CVE-2017-17124, CVE-2017-17125
*   Mon Dec 4 2017 Anish Swaminathan <anishs@vmware.com> 2.29.1-3
-   Fix CVEs CVE-2017-16826, CVE-2017-16827, CVE-2017-16828, CVE-2017-16829,
-   CVE-2017-16830, CVE-2017-16831, CVE-2017-16832
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
