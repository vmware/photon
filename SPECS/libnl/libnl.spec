Summary:	Netlink Protocol Library Suite
Name:		libnl
Version:	3.2.29
Release:	1%{?dist}
License: 	LGPLv2+
Group: 		System Environment/Libraries
URL:		http://www.infradead.org/~tgr/libnl/
Source0:	http://www.infradead.org/~tgr/libnl/files/%{name}-%{version}.tar.gz
%define sha1 libnl=0129a2428b6437558c260324e6ace60eec558053
Vendor:		VMware, Inc.
Distribution:	Photon
BuildRequires:	glib-devel
BuildRequires:	dbus-devel
Requires:	glib
Requires:	dbus

%description
The libnl suite is a collection of libraries providing APIs to netlink protocol based Linux kernel interfaces.
Netlink is a IPC mechanism primarly between the kernel and user space processes. It was designed to be a more flexible successor to ioctl to provide mainly networking related kernel configuration and monitoring interfaces.

%package devel
Summary:	Libraries and headers for the libnl
Requires:	libnl

%description devel
Headers and static libraries for the libnl

%prep
%setup -q
%build
./configure \
	--prefix=%{_prefix} \
	--sysconfdir=%{_sysconfdir} \
 
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install

%check
make %{?_smp_mflags} check

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%files 
%defattr(-,root,root)
%{_sysconfdir}/*
%{_bindir}/*
%{_libdir}/*.so.*
%{_libdir}/*.la
%{_libdir}/*.a
%{_libdir}//libnl/*
%{_mandir}/man8/*

%files devel
%defattr(-,root,root)
%{_includedir}/libnl3/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
*	Tue Apr 11 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.2.29-1
-	Updated to version 3.2.29.
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.2.27-2
-	GA - Bump release of all rpms
* 	Fri Jan 15 2016 Xiaolin Li <xiaolinl@vmware.com> 3.2.27-1
- 	Updated to version 3.2.27
*	Tue Sep 22 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.2.25-2
-	Updated build-requires after creating devel package for dbus. 
*	Tue Jun 23 2015 Divya Thaluru <dthaluru@vmware.com> 3.2.25-1
-	Initial build.
