Summary:        Library for talking to WWAN modems and devices
Name:           libqmi
Version:        1.30.4
Release:        5%{?dist}
URL:            https://www.freedesktop.org
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://www.freedesktop.org/software/libqmi/libqmi-%{version}.tar.xz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  libmbim-devel
BuildRequires:  libgudev-devel
BuildRequires:  systemd-devel
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
Requires:       %{name} = %{version}-%{release}
Requires:       libmbim-devel

%description    devel
It contains the libraries and header files for libqmi

%prep
%autosetup -p1

%build
%configure --disable-static
%make_build

%install
%make_install %{?_smp_mflags}

%if 0%{?with_check}
%check
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
%{_libdir}/libqmi-glib.so.*
%{_mandir}/man1/*
%{_datadir}/bash-completion/*
%exclude %dir %{_libdir}/debug

%files devel
%{_libdir}/*.so
%{_includedir}/libqmi-glib/*
%{_libdir}/pkgconfig/qmi-glib.pc
%{_datadir}/gtk-doc/*

%changelog
* Wed Dec 11 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.30.4-5
- Release bump for SRP compliance
* Tue Jan 03 2023 Guruswamy Basavaiah <bguruswamy@vmware.com> 1.30.4-4
- Bump release as a part of libgudev upgrade to 237-1
* Sun Aug 07 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.30.4-3
- Remove .la files
* Sun May 29 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.30.4-2
- Fix binary path
* Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 1.30.4-1
- Automatic Version Bump
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 1.28.2-1
- Automatic Version Bump
* Mon Dec 14 2020 Susant Sahani <ssahani@vmware.com> 1.26.4-2
- Add build requires
* Wed Sep 09 2020 Gerrit Photon <photon-checkins@vmware.com> 1.26.4-1
- Automatic Version Bump
* Wed Jul 08 2020 Gerrit Photon <photon-checkins@vmware.com> 1.26.2-1
- Automatic Version Bump
* Mon Dec 10 2018 Alexey Makhalov <amakhalov@vmware.com> 1.20.2-1
- Initial build. First version
