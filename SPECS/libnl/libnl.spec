Summary:    Netlink Protocol Library Suite
Name:       libnl
Version:    3.5.0
Release:    3%{?dist}
License:    LGPLv2+
Group:      System Environment/Libraries
URL:        https://github.com/thom311/libnl
Vendor:     VMware, Inc.
Distribution:   Photon

Source0:    https://github.com/thom311/libnl/releases/download/libnl3_5_0/%{name}-%{version}.tar.gz
%define   sha512  libnl=9c94c09bac34297493b3ea482713d7c0865d2839b5042e5c7d1ed008e2402ab63df35a18e272f40b2cce27d0c31dc733fe7e4b2d376e7ca847a2b0d5e90de50c

BuildRequires:  glib-devel >= 2.68.4
BuildRequires:  dbus-devel
BuildRequires:  bison

Requires:   glib >= 2.68.4
Requires:   dbus

%description
The libnl suite is a collection of libraries providing APIs to netlink protocol
based Linux kernel interfaces. Netlink is a IPC mechanism primarly between the
kernel and user space processes. It was designed to be a more flexible successor
to ioctl to provide mainly networking related kernel configuration and monitoring
interfaces.

%package devel
Summary:    Libraries and headers for the libnl
Requires:   %{name} = %{version}-%{release}

%description devel
Headers and static libraries for the libnl

%prep
%autosetup -p1

%build
%configure
make %{?_smp_mflags}

%install
%make_install %{?_smp_mflags}

%check
make %{?_smp_mflags} check

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_sysconfdir}/*
%{_bindir}/*
%{_libdir}/*.so.*
%{_mandir}/man8/*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/libnl/*
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/pkgconfig/*.pc

%changelog
* Sat Oct 07 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 3.5.0-3
- Bump version as part of glib upgrade
* Sun Oct 02 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.5.0-2
- Remove .la files
* Wed May 06 2020 Susant Sahani <ssahani@vmware.com> 3.5.0-1
- Updated to version 3.5.0
* Wed Sep 19 2018 Bo Gan <ganb@vmware.com> 3.4.0-1
- Updated to version 3.4.0
* Tue Apr 11 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.2.29-1
- Updated to version 3.2.29.
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.2.27-2
- GA - Bump release of all rpms
* Fri Jan 15 2016 Xiaolin Li <xiaolinl@vmware.com> 3.2.27-1
- Updated to version 3.2.27
* Tue Sep 22 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.2.25-2
- Updated build-requires after creating devel package for dbus.
* Tue Jun 23 2015 Divya Thaluru <dthaluru@vmware.com> 3.2.25-1
- Initial build.
