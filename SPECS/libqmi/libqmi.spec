Summary:        Library for talking to WWAN modems and devices
Name:           libqmi
Version:        1.26.4
Release:        3%{?dist}
URL:            https://www.freedesktop.org
License:        GPLv2
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://www.freedesktop.org/software/libqmi/libqmi-%{version}.tar.xz
%define sha512 %{name}=6545de5d82dfbfb139ecbf5fefb0b8e34032863f36d573ca3785aa37c12881e88a0903ea7f5eb665f29406189baa2901e751338589da8310f737abaa2df04d89

BuildRequires:  libmbim-devel
BuildRequires:  libgudev-devel
BuildRequires:  systemd-devel
BuildRequires:  systemd-libs
BuildRequires:  gcc
BuildRequires:  pkg-config
BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  libtool

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
%autosetup -p1

%build
%configure --disable-static
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}

%check
%if 0%{?with_check}
make %{?_smp_mflags} check
%endif

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libexecdir}/qmi-proxy
%{_bindir}/qmicli
%{_bindir}/qmi-network
%{_bindir}/qmi-firmware-update
%{_libdir}/libqmi-glib.so*
%exclude %dir %{_libdir}/debug
%{_mandir}/man1/*
%{_datadir}/bash-completion/*

%files devel
%defattr(-,root,root)
%{_includedir}/libqmi-glib/*
%{_libdir}/pkgconfig/qmi-glib.pc
%{_datadir}/gtk-doc/*

%changelog
* Tue Mar 01 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.26.4-3
- Exclude debug symbols properly
* Mon Dec 14 2020 Susant Sahani <ssahani@vmware.com> 1.26.4-2
- Add build requires
* Wed Sep 09 2020 Gerrit Photon <photon-checkins@vmware.com> 1.26.4-1
- Automatic Version Bump
* Wed Jul 08 2020 Gerrit Photon <photon-checkins@vmware.com> 1.26.2-1
- Automatic Version Bump
* Mon Dec 10 2018 Alexey Makhalov <amakhalov@vmware.com> 1.20.2-1
- Initial build. First version
