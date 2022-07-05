Summary:        Library for talking to WWAN modems and devices
Name:           libmbim
Version:        1.26.2
Release:        1%{?dist}
URL:            https://www.freedesktop.org
License:        GPLv2
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://www.freedesktop.org/software/libmbim/libmbim-%{version}.tar.xz
%define sha512  libmbim=7cce1fa6ff5630a1cc565a2198544de9f4a1db20b30304fac96de6c698eaf56b17fe6ccb089151623d4484d88fda6abe980bced19dfbf0d3ef425fc954fb5844
BuildRequires:  libgudev-devel
BuildRequires:  libgudev
BuildRequires:  systemd-devel
BuildRequires:  systemd-libs
BuildRequires:  python3
BuildRequires:  gcc
BuildRequires:  glib-devel
BuildRequires:  pkg-config
BuildRequires:  automake autoconf libtool
Requires:       libgudev

%description
The libmbim package contains a GLib-based library for talking to WWAN modems
and devices which speak the Mobile Interface Broadband Model (MBIM) protocol.

%package        devel
Summary:        Header and development files for libmbim
Requires:       %{name} = %{version}
Requires:       libgudev-devel

%description    devel
It contains the libraries and header files for libmbim

%prep
%autosetup

%build
%configure --disable-static
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} %{?_smp_mflags} install

%check
make %{?_smp_mflags} check

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libexecdir}/mbim-proxy
%{_bindir}/mbimcli
%{_bindir}/mbim-network
%{_libdir}/libmbim-glib.so*
%exclude %{_libdir}/debug
%{_mandir}/man1/*
%{_datadir}/bash-completion/*

%files devel
%{_includedir}/libmbim-glib/*
%{_libdir}/pkgconfig/mbim-glib.pc
%{_libdir}/libmbim-glib.la
%{_datadir}/gtk-doc/*

%changelog
*   Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 1.26.2-1
-   Automatic Version Bump
*   Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 1.24.6-1
-   Automatic Version Bump
*   Mon Dec 14 2020 Susant Sahani<ssahani@vmware.com> 1.24.2-2
-   Add build requires
*   Wed Jul 08 2020 Gerrit Photon <photon-checkins@vmware.com> 1.24.2-1
-   Automatic Version Bump
*   Mon Dec 10 2018 Alexey Makhalov <amakhalov@vmware.com> 1.16.2-1
-   Initial build. First version.
