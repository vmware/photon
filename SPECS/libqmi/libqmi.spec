Summary:        Library for talking to WWAN modems and devices
Name:           libqmi
Version:        1.28.2
Release:        1%{?dist}
URL:            https://www.freedesktop.org
License:        GPLv2
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://www.freedesktop.org/software/libqmi/libqmi-%{version}.tar.xz
%define sha1    libqmi=857ace336958c9ee2a43012342b2ef6b2dce5d5f
BuildRequires:  libmbim-devel
BuildRequires:  libgudev-devel
BuildRequires:  systemd-devel
BuildRequires:  systemd-libs
BuildRequires:  gcc
BuildRequires:  pkg-config
BuildRequires:  automake autoconf libtool

Requires:       libmbim
Requires:       libgudev
%description
The libqmi package contains a GLib-based library for talking to WWAN modems
and devices which speak the Qualcomm MSM Interface (QMI) protocol.

%package        devel
Summary:        Header and development files for libqmi
Requires:       %{name} = %{version}
Requires:       libmbim-devel
%description    devel
It contains the libraries and header files for libqmi

%prep
%setup -q

%build
%configure --disable-static
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

%check
make  %{?_smp_mflags} check

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libexecdir}/qmi-proxy
%{_bindir}/qmicli
%{_bindir}/qmi-network
%{_bindir}/qmi-firmware-update
%{_libdir}/libqmi-glib.so*
%exclude %{_libdir}/debug
%{_mandir}/man1/*
%{_datadir}/bash-completion/*

%files devel
%{_includedir}/libqmi-glib/*
%{_libdir}/pkgconfig/qmi-glib.pc
%{_libdir}/libqmi-glib.la
%{_datadir}/gtk-doc/*

%changelog
*   Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 1.28.2-1
-   Automatic Version Bump
*   Mon Dec 14 2020 Susant Sahani <ssahani@vmware.com> 1.26.4-2
-   Add build requires
*   Wed Sep 09 2020 Gerrit Photon <photon-checkins@vmware.com> 1.26.4-1
-   Automatic Version Bump
*   Wed Jul 08 2020 Gerrit Photon <photon-checkins@vmware.com> 1.26.2-1
-   Automatic Version Bump
*   Mon Dec 10 2018 Alexey Makhalov <amakhalov@vmware.com> 1.20.2-1
-   Initial build. First version
