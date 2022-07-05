Summary:       Netlink Protocol Library Suite
Name:          libnl
Version:       3.6.0
Release:       1%{?dist}
License:       LGPLv2+
Group:         System Environment/Libraries
URL:           https://github.com/thom311/libnl
Source0:       https://github.com/thom311/libnl/releases/download/libnl3_5_0/%{name}-%{version}.tar.gz
%define sha512 libnl=7d1190ce94f43f5b18b1f7909221ca034d4ea5c8ed5735dbd27224d03e7f95d3c4e8ccdb611e33b58007729a21bfc0e23adc8758b112c712355664d87a81ce1b
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
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} %{?_smp_mflags} install

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
