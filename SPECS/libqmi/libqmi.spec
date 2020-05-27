Summary:        Library for talking to WWAN modems and devices
Name:           libqmi
Version:        1.20.2
Release:        1%{?dist}
URL:            https://www.freedesktop.org
License:        GPLv2
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://www.freedesktop.org/software/libqmi/libqmi-1.20.2.tar.xz
%define sha1    libqmi=1299e8b6e5a5e867dbc2d17dffbedcf1eb808b07
BuildRequires:  libmbim-devel
Requires:       libmbim
%description
The libqmi package contains a GLib-based library for talking to WWAN modems
and devices which speak the Qualcomm MSM Interface (QMI) protocol.

%package    devel
Summary:    Header and development files for libqmi
Requires:   %{name} = %{version}
Requires:   libmbim-devel
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
*   Mon Dec 10 2018 Alexey Makhalov <amakhalov@vmware.com> 1.20.2-1
-   Initial build. First version
