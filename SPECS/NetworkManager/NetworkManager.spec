Summary:    NetworkManager
Name:       NetworkManager
Version:    1.0.10
Release:    3%{?dist}
License:    LGPLv2+
URL:        https://wiki.gnome.org/Projects/NetworkManager
Source0:    https://download.gnome.org/sources/NetworkManager/1.0/%{name}-%{version}.tar.xz
%define sha1 NetworkManager=1c199fdfb9fff9e7f540d51952699ce815a12369
Group:      System Environment/Base
Vendor:     VMware, Inc.
Distribution:   Photon
BuildRequires:  intltool
BuildRequires:  iptables
BuildRequires:  dbus-devel
BuildRequires:  dbus-glib-devel
BuildRequires:  libnl-devel
BuildRequires:  readline-devel
BuildRequires:  ncurses-devel
BuildRequires:  nss-devel
BuildRequires:  libndp-devel
BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python-xml
BuildRequires:  dhcp-client
BuildRequires:  libsoup-devel
BuildRequires:  autogen
BuildRequires:  libgudev-devel
BuildRequires:  systemd-devel
Requires:       libnl
Requires:       dbus-glib
Requires:       glib
Requires:       libndp
Requires:       libsoup
Requires:       nss
Requires:       ncurses
Requires:       readline
Requires:       dbus
%package devel
Summary:    Libraries and header files for NetworkManager
Requires:   NetworkManager

%description devel
Headers and libraries for the NetworkManager.

%description
NetworkManager is a set of co-operative tools that make networking simple and straightforward. Whether Wi-Fi, wired, bond, bridge, 3G, or Bluetooth, NetworkManager allows you to quickly move from one network to another: once a network has been configured and joined, it can be detected and re-joined automatically the next time its available.

%prep
%setup -q
%build
./configure \
    --prefix=%{_prefix} \
    --disable-ppp \
    --disable-gtk-doc \
    --sysconfdir=%{_sysconfdir} \
        --with-dhclient=yes \
    --enable-ifcfg-rh=yes \
    --with-setting-plugins-default='ifcfg-rh,ibft'

 
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
cat >> %{buildroot}/etc/NetworkManager/NetworkManager.conf << "EOF"
[main]
plugins=ifcfg-rh,ibft
EOF

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig
%files 
%defattr(-,root,root)
%{_sysconfdir}/NetworkManager/NetworkManager.conf
%{_bindir}/*
%{_sbindir}/*
%{_libdir}/*.so.*
%{_libdir}/*.la
%{_libdir}/NetworkManager/*
%{_libexecdir}/*
%{_libdir}/systemd/system/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*
%{_sysconfdir}/dbus-1/system.d/*
%{_datadir}/gtk-doc/*
%{_datadir}/bash-completion/*  
%{_datadir}/dbus-1/*  
%{_datadir}/doc/*  
%{_datadir}/locale/*
%{_datadir}/polkit-1/*
/lib/udev/rules.d/*.rules
%files devel
%defattr(-,root,root)
%{_includedir}/NetworkManager/*.h
%{_includedir}/libnm/*.h
%{_includedir}/libnm-glib/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
*   Fri Nov 18 2016 Anish Swaminathan <anishs@vmware.com>  1.0.10-3
-   Change systemd dependency
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.10-2
-   GA - Bump release of all rpms
*   Tue Feb 23 2016 Anish Swaminathan <anishs@vmware.com>  1.0.10-1
-   Upgrade to 1.0.10
*   Mon Dec 14 2015 Anish Swaminathan<anishs@vmware.com> 1.0.2-4
-   Adding the missing BuildRequires 
*   Tue Sep 22 2015 Harish Udaiya Kumar<hudaiyakumar@vmware.com> 1.0.2-3
-   Adding the missing Requires list 
*   Thu Jul 23 2015 Divya Thaluru <dthaluru@vmware.com> 1.0.2-2
-   Building with dhclient.
*   Tue Jun 23 2015 Divya Thaluru <dthaluru@vmware.com> 1.0.2-1
-   Initial build.
