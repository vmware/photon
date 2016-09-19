Summary:	Contains a linker, an assembler, and other tools
Name:		binutils
Version:	2.25.1
Release:	2%{?dist}
License:	GPLv2+
URL:		http://www.gnu.org/software/binutils
Group:		System Environment/Base
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0:	http://ftp.gnu.org/gnu/binutils/%{name}-%{version}.tar.bz2
%define sha1 binutils=1d597ae063e3947a5f61e23ceda8aebf78405fcd
Patch0:		http://www.linuxfromscratch.org/patches/downloads/binutils/binutils-2.25.1-gold_export_symbols-1.patch
%description
The Binutils package contains a linker, an assembler,
and other tools for handling object files.
%package	devel
Summary:	Header and development files for binutils
Requires:	%{name} = %{version}
%description	devel
It contains the libraries and header files to create applications 
for handling compiled objects.
%prep
%setup -q
%patch0 -p1
rm -fv etc/standards.info
sed -i.bak '/^INFO/s/standards.info //' etc/Makefile.in
%build
install -vdm 755 ../binutils-build
cd ../binutils-build
../%{name}-%{version}/configure \
	--prefix=%{_prefix} \
	--enable-shared \
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
make %{?_smp_mflags} check


%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%files -f %{name}.lang
%defattr(-,root,root)
%{_bindir}/gprof
%{_bindir}/ld.bfd
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
%{_libdir}/ldscripts/elf32_x86_64.xu
%{_libdir}/ldscripts/elf32_x86_64.xr
%{_libdir}/ldscripts/i386linux.xr
%{_libdir}/ldscripts/elf_l1om.xw
%{_libdir}/ldscripts/elf_l1om.xdc
%{_libdir}/ldscripts/elf_x86_64.xdw
%{_libdir}/ldscripts/elf_k1om.xn
%{_libdir}/ldscripts/elf_x86_64.xr
%{_libdir}/ldscripts/i386linux.x
%{_libdir}/ldscripts/elf_l1om.xd
%{_libdir}/ldscripts/elf_k1om.xw
%{_libdir}/ldscripts/elf_l1om.xs
%{_libdir}/ldscripts/elf_i386.xc
%{_libdir}/ldscripts/elf_i386.xdc
%{_libdir}/ldscripts/elf_k1om.xd
%{_libdir}/ldscripts/elf_i386.xw
%{_libdir}/ldscripts/elf32_x86_64.x
%{_libdir}/ldscripts/elf_i386.xsc
%{_libdir}/ldscripts/elf_x86_64.xw
%{_libdir}/ldscripts/i386linux.xn
%{_libdir}/ldscripts/elf_k1om.xdw
%{_libdir}/ldscripts/elf_k1om.x
%{_libdir}/ldscripts/elf_i386.xr
%{_libdir}/ldscripts/elf32_x86_64.xc
%{_libdir}/ldscripts/elf_x86_64.xsw
%{_libdir}/ldscripts/elf_x86_64.xd
%{_libdir}/ldscripts/elf_i386.x
%{_libdir}/ldscripts/elf_i386.xu
%{_libdir}/ldscripts/elf_k1om.xdc
%{_libdir}/ldscripts/elf32_x86_64.xn
%{_libdir}/ldscripts/elf32_x86_64.xs
%{_libdir}/ldscripts/elf_x86_64.x
%{_libdir}/ldscripts/elf32_x86_64.xdc
%{_libdir}/ldscripts/elf_l1om.xsc
%{_libdir}/ldscripts/elf_l1om.x
%{_libdir}/ldscripts/elf_x86_64.xsc
%{_libdir}/ldscripts/elf_k1om.xu
%{_libdir}/ldscripts/elf32_x86_64.xbn
%{_libdir}/ldscripts/elf_x86_64.xu
%{_libdir}/ldscripts/elf32_x86_64.xw
%{_libdir}/ldscripts/elf_k1om.xs
%{_libdir}/ldscripts/elf_x86_64.xn
%{_libdir}/ldscripts/elf_l1om.xu
%{_libdir}/ldscripts/elf32_x86_64.xdw
%{_libdir}/ldscripts/elf_l1om.xsw
%{_libdir}/ldscripts/elf_l1om.xc
%{_libdir}/ldscripts/elf_l1om.xr
%{_libdir}/ldscripts/i386linux.xbn
%{_libdir}/ldscripts/elf_l1om.xn
%{_libdir}/ldscripts/elf_i386.xsw
%{_libdir}/ldscripts/elf32_x86_64.xd
%{_libdir}/ldscripts/elf_k1om.xbn
%{_libdir}/ldscripts/elf_i386.xn
%{_libdir}/ldscripts/elf_i386.xbn
%{_libdir}/ldscripts/i386linux.xu
%{_libdir}/ldscripts/elf_k1om.xc
%{_libdir}/ldscripts/elf32_x86_64.xsw
%{_libdir}/ldscripts/elf_k1om.xr
%{_libdir}/ldscripts/elf32_x86_64.xsc
%{_libdir}/ldscripts/elf_k1om.xsw
%{_libdir}/ldscripts/elf_i386.xdw
%{_libdir}/ldscripts/elf_i386.xd
%{_libdir}/ldscripts/elf_x86_64.xdc
%{_libdir}/ldscripts/elf_i386.xs
%{_libdir}/ldscripts/elf_x86_64.xs
%{_libdir}/ldscripts/elf_x86_64.xc
%{_libdir}/ldscripts/elf_k1om.xsc
%{_libdir}/ldscripts/elf_l1om.xbn
%{_libdir}/ldscripts/elf_x86_64.xbn
%{_libdir}/ldscripts/elf_l1om.xdw
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
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.25.1-2
-	GA - Bump release of all rpms
*   Tue Jan 12 2016 Xiaolin Li <xiaolinl@vmware.com> 2.25.1-1
-   Updated to version 2.25.1
*	Tue Nov 10 2015 Xiaolin Li <xiaolinl@vmware.com> 2.25-2
-	Handled locale files with macro find_lang
*	Mon Apr 6 2015 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.25-1
-	Updated to 2.25
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 2.24-1
-	Initial build. First version
