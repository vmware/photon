Summary:    Glib interfaces to D-Bus API
Name:       dbus-glib
Version:    0.110
Release:    3%{?dist}
License:    AFL and GPLv2+
Group:      System Environment/Libraries
Url:        https://dbus.freedesktop.org/doc/dbus-glib
Source0:    http://dbus.freedesktop.org/releases/dbus-glib/%{name}-%{version}.tar.gz
%define sha512 dbus-glib=c40ccf7118d4951f0e09082216ccd26f21ee906bdf96d912611d3cd29badd7ef446bea74e19f26c28ebceb9e19bb659d11c643c3e712dac499df12907be88a54
Vendor:     VMware, Inc.
Distribution:   Photon
BuildRequires:  glib-devel >= 2.58.3
BuildRequires:  dbus-devel
Requires:   glib >= 2.58.3
Requires:   dbus
Provides:   pkgconfig(dbus-glib-1)

%description
The D-Bus GLib package contains GLib interfaces to the D-Bus API.

%package devel
Summary:    Libraries and headers for the D-Bus GLib bindings
Requires:   glib-devel >= 2.58.3
Requires:   dbus-devel
Requires:   %{name} = %{version}

%description devel
Headers and static libraries for the D-Bus GLib bindings

%prep
%autosetup -p1

%build
%configure \
    --disable-static \
    --disable-gtk-doc

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}

%check
make %{?_smp_mflags} check

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig
%files
%defattr(-,root,root)
%{_sysconfdir}/bash_completion.d/*
%{_bindir}/*
%{_libdir}/*.so.*
%{_libexecdir}/*
%{_mandir}/man1/*
%{_datadir}/gtk-doc/*

%files devel
%defattr(-,root,root)
%{_includedir}/dbus-1.0/dbus/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Wed Nov 15 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 0.110-3
- Version bump due to glib change
* Mon Oct 03 2022 Shreenidhi Shedi <sshedi@vmware.com> 0.110-2
- Remove .la files
* Mon Sep 10 2018 Ajay Kaher <akaher@vmware.com> 0.110-1
- Upgraded to 0.110
* Wed May 03 2017 Bo Gan <ganb@vmware.com> 0.108-1
- Update to 0.108
* Wed Oct 05 2016 ChangLee <changlee@vmware.com> 0.106-5
- Modified %check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.106-4
- GA - Bump release of all rpms
* Mon Feb 22 2016 XIaolin Li <xiaolinl@vmware.com> 0.106-1
- Updated to version 0.106
* Thu Jan 28 2016 Anish Swaminathan <anishs@vmware.com> 0.104-3
- Add requires to dbus-glib-devel
* Tue Sep 22 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 0.104-2
- Updated build requires after creating devel package for dbus
* Tue Jun 23 2015 Divya Thaluru <dthaluru@vmware.com> 0.104-1
- Initial build.
