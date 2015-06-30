Summary:	Library for Neighbor Discovery Protocol
Name:		libndp
Version:	1.5
Release:	1%{?dist}
License:	LGPLv2+
URL:		http://www.libndp.org/
Source:		http://www.libndp.org/files/%{name}-%{version}.tar.gz
Group:		System Environment/Libraries

%description
This package contains a library which provides a wrapper
for IPv6 Neighbor Discovery Protocol.  It also provides a tool
named ndptool for sending and receiving NDP messages.

%package devel
Summary:	Libraries and header files for libndp
Requires:	libndp

%description devel
Headers and libraries for the libndp.

%prep
%setup -q

%build
%configure --disable-static
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install INSTALL="install -p"
find %{buildroot}%{_libdir} -name \*.la -delete

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%{_bindir}/*
%{_libdir}/*so.*
%{_mandir}/man8/ndptool.8*

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
*	Tue Jun 23 2015 Divya Thaluru <dthaluru@vmware.com> 1.5-1
-	Initial build.
