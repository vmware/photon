Summary:	A library that provides compression and decompression of file formats used by Microsoft
Name:		libmspack
Version:	0.4alpha
Release:	1%{?dist}
License:	LGPLv2+
URL:		http://www.cabextract.org.uk/libmspack/libmspack-0.4alpha.tar.gz
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://www.cabextract.org.uk/libmspack/%{name}-%{version}.tar.gz
%define sha1 libmspack=b10249bde64ca387b211fd0bd125fc360377593c
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
*	Thu Nov 06 2014 Sharath George <sharathg@vmware.com> 0.4-1
	Initial version
