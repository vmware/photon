Summary:        Contains a linker, an assembler, and other tools
Name:           binutils
Version:        2.30
Release:        2%{?dist}
License:        GPLv2+
URL:            http://www.gnu.org/software/binutils
Group:          System Environment/Base
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://ftp.gnu.org/gnu/binutils/%{name}-%{version}.tar.xz
%define sha1    binutils=574d3b5650413d6ee65195a4f5ecbddc3a38f718
Patch0:         binutils-2.30-CVE-2018-6543.patch
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
%{_mandir}/man1/nlmconv.1.gz
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
%{_libdir}/libbfd.a
%{_libdir}/libopcodes.a
%{_libdir}/libbfd.so
%{_libdir}/libopcodes.so

%changelog
*   Wed Feb 28 2018 Xiaolin Li <xiaolinl@vmware.com> 2.30-2
-   Fix CVE-2018-6543.
*   Mon Jan 29 2018 Xiaolin Li <xiaolinl@vmware.com> 2.30-1
-   Update to version 2.30
*   Mon Dec 18 2017 Anish Swaminathan <anishs@vmware.com> 2.29.1-3
-   Fix CVEs CVE-2017-17121, CVE-2017-17122, CVE-2017-17123,
-   CVE-2017-17124, CVE-2017-17125
*   Mon Dec 4 2017 Anish Swaminathan <anishs@vmware.com> 2.29.1-2
-   Fix CVEs CVE-2017-16826, CVE-2017-16827, CVE-2017-16828, CVE-2017-16829,
-   CVE-2017-16830, CVE-2017-16831, CVE-2017-16832
*   Mon Oct 2 2017 Anish Swaminathan <anishs@vmware.com> 2.29.1-1
-   Version update to 2.29.1, fix CVEs CVE-2017-12799, CVE-2017-14729,CVE-2017-14745,
-   CVE-2017-15020
*   Fri Aug 11 2017 Anish Swaminathan <anishs@vmware.com> 2.29-1
-   Version update
-   Apply patches for CVE-2017-12448,CVE-2017-12449,CVE-2017-12450,CVE-2017-12451,
-   CVE-2017-12452,CVE-2017-12453,CVE-2017-12454,CVE-2017-12455,CVE-2017-12456,
-   CVE-2017-12457,CVE-2017-12458,CVE-2017-12459
*   Thu Jun 29 2017 Divya Thaluru <dthaluru@vmware.com> 2.25.1-5
-   Bump release to built with latest toolchain
*   Tue Apr 04 2017 Anish Swaminathan <anishs@vmware.com> 2.25.1-4
-   Apply patch for CVE-2017-6969
*   Tue Apr 04 2017 Anish Swaminathan <anishs@vmware.com> 2.25.1-3
-   Apply patch for CVE-2014-9939
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
