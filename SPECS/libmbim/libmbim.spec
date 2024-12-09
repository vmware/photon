Summary:        Library for talking to WWAN modems and devices
Name:           libmbim
Version:        1.26.2
Release:        6%{?dist}
URL:            https://www.freedesktop.org
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://www.freedesktop.org/software/libmbim/libmbim-%{version}.tar.xz
%define sha512  %{name}=7cce1fa6ff5630a1cc565a2198544de9f4a1db20b30304fac96de6c698eaf56b17fe6ccb089151623d4484d88fda6abe980bced19dfbf0d3ef425fc954fb5844

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  libgudev-devel
BuildRequires:  libgudev
BuildRequires:  systemd-devel
BuildRequires:  systemd-libs
BuildRequires:  python3
BuildRequires:  gcc
BuildRequires:  glib-devel
BuildRequires:  pkg-config
BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  libtool

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

%post   -p /sbin/ldconfig
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
* Wed Dec 11 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.26.2-6
- Release bump for SRP compliance
* Tue Jan 03 2023 Guruswamy Basavaiah <bguruswamy@vmware.com> 1.26.2-5
- Bump release as a part of libgudev upgrade to 237-1
* Tue Dec 06 2022 Prashant S Chauhan <psinghchauha@vmware.com> 1.26.2-4
- Update release to compile with python 3.11
* Sun Aug 07 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.26.2-3
- Remove .la files
* Sun May 29 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.26.2-2
- Fix binary path
* Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 1.26.2-1
- Automatic Version Bump
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 1.24.6-1
- Automatic Version Bump
* Mon Dec 14 2020 Susant Sahani<ssahani@vmware.com> 1.24.2-2
- Add build requires
* Wed Jul 08 2020 Gerrit Photon <photon-checkins@vmware.com> 1.24.2-1
- Automatic Version Bump
* Mon Dec 10 2018 Alexey Makhalov <amakhalov@vmware.com> 1.16.2-1
- Initial build. First version
