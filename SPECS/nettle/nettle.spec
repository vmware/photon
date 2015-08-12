Summary:	Low level cryptographic libraries
Name:		nettle
Version:	3.1.1
Release:	1%{?dist}
License:	LGPLv3+ or GPLv2+
URL:            http://www.lysator.liu.se/~nisse/nettle/
Source0: 	https://ftp.gnu.org/gnu/nettle/%{name}-%{version}.tar.gz
%define sha1 nettle=1836601393522124787e029466935408e22dd204
Group: 		Development/Libraries
Vendor:		VMware, Inc.
Distribution:	Photon
Provides:	libhogweed.so.4()(64bit)
Provides:	libhogweed.so.4(HOGWEED_4)(64bit)
Provides:	libnettle.so.6()(64bit)
Provides:	libnettle.so.6(NETTLE_6)(64bit)
Requires:	gmp

%description
GNettle is a cryptographic library that is designed to fit easily in more
or less any context: In crypto toolkits for object-oriented languages
(C++, Python, Pike, ...), in applications like LSH or GNUPG, or even in
kernel space.

%package devel
Summary:	Development libraries and header files for nettle
Requires:	nettle
Provides:	pkgconfig(hogweed)
Provides:	pkgconfig(nettle)

%description devel
The package contains libraries and header files for
developing applications that use nettle.

%prep
%setup -q
%build
./configure \
	--prefix=%{_prefix} \
	--enable-shared
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
rm %{buildroot}%{_infodir}/*
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%files
%defattr(-,root,root)
%{_libdir}/*.so.*
%{_bindir}/*
%{_libdir}/*.a
%files devel
%defattr(-,root,root)
%{_includedir}/nettle/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%changelog
*	Thu Jun 18 2015 Divya Thaluru <dthaluru@vmware.com> 3.1.1-1
-	Initial build. First version

