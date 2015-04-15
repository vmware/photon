Summary:	A simplified, portable interface to several low-level networking routines
Name:		libdnet
Version:	1.11
Release:	1
License:	BSD
URL:		http://prdownloads.sourceforge.net/libdnet/libdnet-1.11.tar.gz
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://prdownloads.sourceforge.net/libdnet/%{name}-%{version}.tar.gz
%description
libdnet provides a simplified, portable interface to several low-level networking routines.
%prep
%setup -q
%build
./configure --prefix=/usr "CFLAGS=-fPIC"
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
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
*	Thu Nov 06 2014 Sharath George <sharathg@vmware.com> 1.11-1
	Initial version
