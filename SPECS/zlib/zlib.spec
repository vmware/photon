Summary:	Compression and decompression routines
Name:		zlib
Version:	1.2.8
Release:	4%{?dist}
URL:		http://www.zlib.net/
License:	zlib
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0:	http://www.zlib.net/%{name}-%{version}.tar.xz
Patch0:         CVE-2016-9841.patch
Patch1:         CVE-2016-9843.patch
%define sha1 zlib=b598beb7acc96347cbd1020b71aef7871d374677
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
%patch0 -p1
%patch1 -p1
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
%{_libdir}/libz.so.1
%{_libdir}/libz.so.1.2.8
%files devel
%{_includedir}/zconf.h
%{_includedir}/zlib.h
%{_libdir}/pkgconfig/zlib.pc
%{_libdir}/libz.a
%{_libdir}/libz.so
%changelog
*   Wed Jun 14 2017 Kumar Kaushik <kaushikk@vmware.com> 1.2.8-4
-   Fixing CVE-2016-9841 and CVE-2016-9843, bug#1886934
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.2.8-3
-   GA - Bump release of all rpms
*   Mon May 18 2015 Touseef Liaqat <tliaqat@vmware.com> 1.2.8-2
-   Update according to UsrMove.
*   Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 1.2.8-1
-   Initial build. First version
