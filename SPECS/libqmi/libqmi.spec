Summary:        Library for talking to WWAN modems and devices
Name:           libqmi
Version:        1.20.2
Release:        3%{?dist}
URL:            https://www.freedesktop.org
License:        GPLv2
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://www.freedesktop.org/software/libqmi/libqmi-1.20.2.tar.xz
%define sha512 %{name}=2d1ceda25ad995b27dc20d9b5d85ee23a841c43f33aa68b3543df10cc1da72062e648c1136a2706740659ae2cf8c17373d7c6c6f5f8d075864f47e4fb89d7b50

BuildRequires:  libmbim-devel

Requires:       libmbim

%description
The libqmi package contains a GLib-based library for talking to WWAN modems
and devices which speak the Qualcomm MSM Interface (QMI) protocol.

%package    devel
Summary:    Header and development files for libqmi
Requires:   %{name} = %{version}-%{release}
Requires:   libmbim-devel
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
%{_mandir}/man1/*
%{_datadir}/bash-completion/*
%exclude %dir %{_libdir}/debug

%files devel
%{_includedir}/libqmi-glib/*
%{_libdir}/pkgconfig/qmi-glib.pc
%{_datadir}/gtk-doc/*

%changelog
* Mon Oct 03 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.20.2-3
- Remove .la files
* Sat Mar 26 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.20.2-2
- Exclude debug symbols properly
* Mon Dec 10 2018 Alexey Makhalov <amakhalov@vmware.com> 1.20.2-1
- Initial build. First version
