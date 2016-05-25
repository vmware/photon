Summary:	Basic and advanced IPV4-based networking
Name:		iproute2
Version:	4.2.0
Release:	2%{?dist}
License:	GPLv2+
URL:		http://www.kernel.org/pub/linux/utils/net/iproute2
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0:	http://www.kernel.org/pub/linux/utils/net/iproute2/%{name}-%{version}.tar.xz
%define sha1 iproute2=2585177e94fddb59418db149692d0726cde30774
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
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 	4.2.0-2
-	GA - Bump release of all rpms
* 	Tue Jan 12 2016 Xiaolin Li <xiaolinl@vmware.com> 4.2.0-1
- 	Updated to version 4.2.0
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 3.12.0-1
-	Initial build. First version
