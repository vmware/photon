Summary:       Netlink Protocol Library Suite
Name:          libnl
Version:       3.7.0
Release:       1%{?dist}
License:       LGPLv2+
Group:         System Environment/Libraries
URL:           https://github.com/thom311/libnl
Source0:       https://github.com/thom311/libnl/releases/download/libnl3_5_0/%{name}-%{version}.tar.gz
%define sha512 libnl=80fbbc079299c90afd2a5eda62e4d4f98bf4ef23958c3ce5101f4ed4d81d783af733213bb3bab15f218555d8460bc2394898f909f4ac024fc27281faec86a041
Vendor:        VMware, Inc.
Distribution:  Photon

BuildRequires: glib-devel
BuildRequires: dbus-devel

Requires:      glib
Requires:      dbus

%description
The libnl suite is a collection of libraries providing APIs to netlink protocol
based Linux kernel interfaces. Netlink is a IPC mechanism primarly between the
kernel and user space processes. It was designed to be a more flexible successor
to ioctl to provide mainly networking related kernel configuration and monitoring
interfaces.

%package       devel
Summary:       Libraries and headers for the libnl
Requires:      libnl

%description   devel
Headers and static libraries for the libnl

%prep
%autosetup

%build
%configure
%make_build %{?_smp_mflags}

%install
%make_install %{?_smp_mflags}

%check
make %{?_smp_mflags} check

%ldconfig_scriptlets

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
%{_libdir}/*.la
%{_libdir}/*.a
%{_libdir}/pkgconfig/*.pc

%changelog
* Tue Aug 30 2022 Susant Sahani <ssahani@vmware.com> 3.7.0-1
- Version update
* Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 3.6.0-1
- Automatic Version Bump
* Mon Aug 02 2021 Susant Sahani <ssahani@vmware.com> 3.5.0-2
- Use autosetup and ldconfig scriptlets
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
