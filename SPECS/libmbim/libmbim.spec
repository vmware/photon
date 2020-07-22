Summary:        Library for talking to WWAN modems and devices
Name:           libmbim
Version:        1.24.2
Release:        1%{?dist}
URL:            https://www.freedesktop.org
License:        GPLv2
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://www.freedesktop.org/software/libmbim/libmbim-%{version}.tar.xz
%define sha1    libmbim=1162a4302be250ca3334f3bfd1e7d04770e4b4ff
BuildRequires:  libgudev-devel
Requires:       libgudev
%description
The libmbim package contains a GLib-based library for talking to WWAN modems
and devices which speak the Mobile Interface Broadband Model (MBIM) protocol.

%package       devel
Summary:       Header and development files for libmbim
Requires:      %{name} = %{version}
Requires:      libgudev-devel
%description   devel
It contains the libraries and header files for libmbim

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
*   Wed Jul 08 2020 Gerrit Photon <photon-checkins@vmware.com> 1.24.2-1
-   Automatic Version Bump
*   Mon Dec 10 2018 Alexey Makhalov <amakhalov@vmware.com> 1.16.2-1
-   Initial build. First version
