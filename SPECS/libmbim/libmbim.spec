Summary:        Library for talking to WWAN modems and devices
Name:           libmbim
Version:        1.24.2
Release:        6%{?dist}
URL:            https://www.freedesktop.org
License:        GPLv2
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://www.freedesktop.org/software/libmbim/libmbim-%{version}.tar.xz
%define sha512  %{name}=1005ca982b9f705deb64ae6e9ed0af7803a7802cf653b1dc83c7c90a073ac9e776100f6b2bda2be8c72fefd18ae7adb5c5509d9368398271b3b364a0ae977a1f

BuildRequires:  libgudev-devel
BuildRequires:  libgudev
BuildRequires:  systemd-devel
BuildRequires:  python3-devel
BuildRequires:  gcc
BuildRequires:  glib-devel >= 2.68.4
BuildRequires:  pkg-config
BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  libtool

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
%autosetup -p1

%build
%configure --disable-static
make %{?_smp_mflags}

%install
make %{?_smp_mflags} DESTDIR=%{buildroot} install

%if 0%{?with_check}
%check
make %{?_smp_mflags} check
%endif

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libexecdir}/mbim-proxy
%{_bindir}/mbimcli
%{_bindir}/mbim-network
%{_libdir}/libmbim-glib.so*
%exclude %dir %{_libdir}/debug
%{_mandir}/man1/*
%{_datadir}/bash-completion/*

%files devel
%{_includedir}/libmbim-glib/*
%{_libdir}/pkgconfig/mbim-glib.pc
%{_datadir}/gtk-doc/*

%changelog
* Sat Oct 07 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 1.24.2-6
- Bump version as part of glib upgrade
* Sun Oct 02 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.24.2-5
- Remove .la files
* Tue Mar 01 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.24.2-4
- Exclude debug symbols properly
* Thu Dec 09 2021 Prashant S Chauhan <psinghchauha@vmware.com> 1.24.2-3
- Bump up to compile with python 3.10
* Mon Dec 14 2020 Susant Sahani<ssahani@vmware.com> 1.24.2-2
- Add build requires
* Wed Jul 08 2020 Gerrit Photon <photon-checkins@vmware.com> 1.24.2-1
- Automatic Version Bump
* Mon Dec 10 2018 Alexey Makhalov <amakhalov@vmware.com> 1.16.2-1
- Initial build. First version
