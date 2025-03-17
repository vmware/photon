Name:           lzo
Version:        2.10
Release:        3%{?dist}
Summary:        Data compression library with very fast (de)compression
Group:          System Environment/Libraries
URL:            http://www.oberhumer.com/opensource/lzo/
Vendor:     VMware, Inc.
Distribution:   Photon

Source0: http://www.oberhumer.com/opensource/lzo/download/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  zlib-devel

%description
LZO is a portable lossless data compression library written in ANSI C.
It offers pretty fast compression and very fast decompression.
Decompression requires no memory. In addition there are slower
compression levels achieving a quite competitive compression ratio
while still decompressing at this very high speed.

%package    minilzo
Summary:        Mini version of lzo for apps which don't need the full version
Group:          System Environment/Libraries

%description    minilzo
A small (mini) version of lzo for embedding into applications which don't need
full blown lzo compression support.

%package devel
Summary:        Development files for the lzo library
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-minilzo = %{version}-%{release}

%description devel
LZO is a portable lossless data compression library written in ANSI C.
It offers pretty fast compression and very fast decompression.
This package contains development files needed for lzo.

%prep
%autosetup -p1
# mark asm files as NOT needing execstack
for i in asm/i386/src_gas/*.S; do
  echo '.section .note.GNU-stack,"",@progbits' >> $i
done

%build
%configure --disable-dependency-tracking --disable-static --enable-shared
%make_build
gcc %{optflags} -fpic -Iinclude/lzo -o minilzo/minilzo.o -c minilzo/minilzo.c
gcc -g -shared -o libminilzo.so.0 -Wl,-soname,libminilzo.so.0 minilzo/minilzo.o

%install
%make_install %{?_smp_mflags}
install -m 755 libminilzo.so.0 %{buildroot}%{_libdir}
ln -s libminilzo.so.0 %{buildroot}%{_libdir}/libminilzo.so
install -p -m 644 minilzo/minilzo.h %{buildroot}%{_includedir}/lzo

%check
make check test %{?_smp_mflags}

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post minilzo -p /sbin/ldconfig
%postun minilzo -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/liblzo2.so.*

%files minilzo
%defattr(-,root,root,-)
%doc minilzo/README.LZO
%{_libdir}/libminilzo.so.0

%files devel
%defattr(-,root,root,-)
%doc doc/LZOAPI.TXT doc/LZO.FAQ doc/LZO.TXT
%{_datadir}/doc/lzo
%{_includedir}/lzo
%{_libdir}/lib*lzo*.so
%{_libdir}/pkgconfig/lzo2.pc

%changelog
* Thu Dec 12 2024 Ajay Kaher <ajay.kaher@broadcom.com> 2.10-3
- Release bump for SRP compliance
* Fri Apr 14 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.10-2
- Bump version as a part of zlib upgrade
* Tue Apr 4 2017 Michelle Wang <michellew@vmware.com> 2.10-1
- Update package version
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.09-2
- GA - Bump release of all rpms
* Thu Feb 26 2015 Divya Thaluru <dthaluru@vmware.com> 2.09-1
- Initial version
