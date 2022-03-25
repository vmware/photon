Summary:        Library for talking to WWAN modems and devices
Name:           libmbim
Version:        1.16.2
Release:        2%{?dist}
URL:            https://www.freedesktop.org
License:        GPLv2
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://www.freedesktop.org/software/libmbim/libmbim-1.16.2.tar.xz
%define sha1    %{name}=acb71b3afa3cabd39f2c7e0f70d188b9bbc4b6ea

BuildRequires:  libgudev-devel

Requires:       libgudev

%description
The libmbim package contains a GLib-based library for talking to WWAN modems
and devices which speak the Mobile Interface Broadband Model (MBIM) protocol.

%package    devel
Summary:    Header and development files for libmbim
Requires:   %{name} = %{version}
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
%{_libdir}/libmbim-glib.la
%{_datadir}/gtk-doc/*

%changelog
* Fri Mar 25 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.16.2-2
- Exclude debug symbols properly
* Mon Dec 10 2018 Alexey Makhalov <amakhalov@vmware.com> 1.16.2-1
- Initial build. First version
