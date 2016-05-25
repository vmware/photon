Summary:	A library that provides compression and decompression of file formats used by Microsoft
Name:		libmspack
Version:	0.5alpha
Release:	2%{?dist}
License:	LGPLv2+
URL:		http://www.cabextract.org.uk/libmspack/libmspack-0.5alpha.tar.gz
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://www.cabextract.org.uk/libmspack/%{name}-%{version}.tar.gz
%define sha1 libmspack=226f19b1fc58e820671a1749983b06896e108cc4
%description
A library that provides compression and decompression of file formats used by Microsoft
%prep
%setup -q
%build
./configure --prefix=/usr
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%files 
%defattr(-,root,root)
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/*.so.*
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*
%changelog
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.5alpha-2
-	GA - Bump release of all rpms
*   Fri Jan 22 2016 Xiaolin Li <xiaolinl@vmware.com> 0.5-1
-   Updated to version 0.5
*	Thu Nov 06 2014 Sharath George <sharathg@vmware.com> 0.4-1
	Initial version
