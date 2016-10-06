Summary:	A simplified, portable interface to several low-level networking routines
Name:		libdnet
Version:	1.11
Release:	3%{?dist}
License:	BSD
URL:		http://prdownloads.sourceforge.net/libdnet/libdnet-1.11.tar.gz
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://prdownloads.sourceforge.net/libdnet/%{name}-%{version}.tar.gz
%define sha1 libdnet=e2ae8c7f0ca95655ae9f77fd4a0e2235dc4716bf
%description
libdnet provides a simplified, portable interface to several low-level networking routines.
%prep
%setup -q
%build
./configure --prefix=/usr "CFLAGS=-fPIC"
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
%check
make  %{?_smp_mflags} check
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%files 
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/libdnet*
%{_includedir}/*
%{_sbindir}/*
%{_prefix}/man/*
%changelog
*       Thu Oct 06 2016 ChangLee <changlee@vmware.com> 1.11-3
-       Modified %check
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.11-2
-	GA - Bump release of all rpms
*	Thu Nov 06 2014 Sharath George <sharathg@vmware.com> 1.11-1
	Initial version
