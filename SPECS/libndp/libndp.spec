Summary:	Library for Neighbor Discovery Protocol
Name:		libndp
Version:	1.6
Release:	1%{?dist}
License:	LGPLv2+
URL:		http://www.libndp.org/
Source:		http://www.libndp.org/files/%{name}-%{version}.tar.gz
%define sha1 libndp=300e63fcf69f6239dc6c5f82770437d5ffbc2dd4
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
*   Thu Oct 24 2019 Shreyas B. <shreyasb@vmware.com> 1.6-1
-   Update to 1.6 to fix CVE-2016-3698.
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.5-2
-	GA - Bump release of all rpms
*	Tue Jun 23 2015 Divya Thaluru <dthaluru@vmware.com> 1.5-1
-	Initial build.
