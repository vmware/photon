Summary:	Basic and advanced IPV4-based networking
Name:		iproute2
Version:	3.12.0
Release:	1%{?dist}
License:	GPLv2+
URL:		http://www.kernel.org/pub/linux/utils/net/iproute2
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0:	http://www.kernel.org/pub/linux/utils/net/iproute2/%{name}-%{version}.tar.xz
%define sha1 iproute2=9397376e5d4dcbb1182745cd58625895fcdb868d
%description
The IPRoute2 package contains programs for basic and advanced
IPV4-based networking.
%prep
%setup -q
sed -i '/^TARGETS/s@arpd@@g' misc/Makefile
sed -i /ARPD/d Makefile
sed -i 's/arpd.8//' man/man8/Makefile
%build
make VERBOSE=1 %{?_smp_mflags} DESTDIR= LIBDIR=%{_libdir}
%install
make	DESTDIR=%{buildroot} \
	MANDIR=%{_mandir} \
	LIBDIR=%{_libdir} \
	DOCDIR=%{_defaultdocdir}/%{name}-%{version} install
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%files
%defattr(-,root,root)
%{_sysconfdir}/%{name}/*
/sbin/*
%{_libdir}/tc/*
%{_defaultdocdir}/%{name}-%{version}/*
%{_mandir}/*/*
%changelog
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 3.12.0-1
-	Initial build. First version
