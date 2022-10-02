Summary:        Library for talking to WWAN modems and devices
Name:           libmbim
Version:        1.16.2
Release:        3%{?dist}
URL:            https://www.freedesktop.org
License:        GPLv2
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://www.freedesktop.org/software/libmbim/libmbim-1.16.2.tar.xz
%define sha512 %{name}=6081a5b40b7fc5cd21adf1948c16c57919c452bc2eccdccb561412ecada5aca7ff1fcac79568eb3dda83d49c780b0dab95a0b15bda0c4f2712b735cbe95402be

BuildRequires:  libgudev-devel

Requires:       libgudev

%description
The libmbim package contains a GLib-based library for talking to WWAN modems
and devices which speak the Mobile Interface Broadband Model (MBIM) protocol.

%package    devel
Summary:    Header and development files for libmbim
Requires:   %{name} = %{version}-%{release}
Requires:   libgudev-devel
%description    devel
It contains the libraries and header files for libmbim

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
* Mon Oct 03 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.16.2-3
- Remove .la files
* Fri Mar 25 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.16.2-2
- Exclude debug symbols properly
* Mon Dec 10 2018 Alexey Makhalov <amakhalov@vmware.com> 1.16.2-1
- Initial build. First version
