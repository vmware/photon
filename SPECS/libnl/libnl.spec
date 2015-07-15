Summary:	Netlink Protocol Library Suite
Name:		libnl
Version:	3.2.25
Release:	1%{?dist}
License: 	LGPLv2+
Group: 		System Environment/Libraries
URL:		http://www.infradead.org/~tgr/libnl/
Source0:	http://www.infradead.org/~tgr/libnl/files/%{name}-%{version}.tar.gz
%define sha1 libnl=b7a4981f7edf7398256d35fd3c0b87bc84ae27d1
Vendor:		VMware, Inc.
Distribution:	Photon
BuildRequires:	glib-devel
BuildRequires:	dbus
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
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%files 
%defattr(-,root,root)
%{_sysconfdir}/*
%{_sbindir}/*
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
*	Tue Jun 23 2015 Divya Thaluru <dthaluru@vmware.com> 3.2.25-1
-	Initial build.
