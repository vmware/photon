Summary:	A simplified, portable interface to several low-level networking routines
Name:		libdnet
Version:	1.11
Release:	2%{?dist}
License:	BSD
URL:		http://prdownloads.sourceforge.net/libdnet/libdnet-1.11.tar.gz
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://prdownloads.sourceforge.net/libdnet/%{name}-%{version}.tar.gz
%define sha1 libdnet=e2ae8c7f0ca95655ae9f77fd4a0e2235dc4716bf
%description
libdnet provides a simplified, portable interface to several low-level networking routines.

%package        devel
Summary:        Development files for libdnet
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The libdnet-devel package contains libraries, header files and documentation
for developing applications that use libdnet.

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
%{_libdir}/libdnet
%{_libdir}/libdnet.1
%{_libdir}/libdnet.1.0.1
%{_sbindir}/*
%{_prefix}/man/*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/libdnet.a
%{_libdir}/libdnet.la

%changelog
*   Tue Oct 6 2015 Xiaolin Li <xiaolinl@vmware.com> 1.11-2
-   Move header files, and static lib files to devel package.
*	Thu Nov 06 2014 Sharath George <sharathg@vmware.com> 1.11-1
	Initial version
