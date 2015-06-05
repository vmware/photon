Summary:	Compression and decompression routines
Name:		zlib
Version:	1.2.8
Release:	2%{?dist}
URL:		http://www.zlib.net/
License:	zlib
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0:	http://www.zlib.net/%{name}-%{version}.tar.xz
%description
Compression and decompression routines
%package	devel
Summary:	Header and development files for zlib
Requires:	%{name} = %{version}
%description	devel
It contains the libraries and header files to create applications 
for handling compiled objects.
%prep
%setup -q
%build
./configure \
	--prefix=%{_prefix}
make V=1 %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
install -vdm 755 %{buildroot}/%{_lib}
ln -sfv ../../lib/$(readlink %{buildroot}%{_libdir}/libz.so) %{buildroot}%{_libdir}/libz.so
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%files
%defattr(-,root,root)
%{_mandir}/man3/zlib.3.gz
%{_lib}/libz.so.1
%{_lib}/libz.so.1.2.8
%files devel
%{_includedir}/zconf.h
%{_includedir}/zlib.h
%{_libdir}/pkgconfig/zlib.pc
%{_libdir}/libz.a
%{_libdir}/libz.so
%changelog
*   Mon May 18 2015 Touseef Liaqat <tliaqat@vmware.com> 1.2.8-2
-   Update according to UsrMove.
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 1.2.8-1
-	Initial build. First version
