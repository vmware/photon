Summary:        Wayland Compositor Infrastructure
Name:           wayland
Version:        1.20.0
Release:        5%{?dist}
License:        MIT
URL:            http://wayland.freedesktop.org
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://wayland.freedesktop.org/releases/%{name}-%{version}.tar.xz
%define sha512 %{name}=e8a1f410994b947f850799bdd0d95a2429d8467f853e62a0ab3915a4e9fe130f8aa977e03715114ab740c6ec546edea63d275ce7f927d4f3029ea126e6a7d215

Patch0: CVE-2021-3782.patch

BuildRequires: libxml2-devel
BuildRequires: meson
BuildRequires: ninja-build
BuildRequires: libffi-devel
BuildRequires: expat-devel
BuildRequires: libxslt-devel

%description
Wayland is a protocol for a compositor to talk to its clients as well as a C library implementation of that protocol. The compositor can be a standalone display server running on Linux kernel modesetting and evdev input devices, an X application, or a Wayland client itself. The clients can be traditional applications, X servers (rootless or fullscreen) or other display servers.

%package    devel
Summary:    Development files for wayland
Requires:   libwayland-client = %{version}-%{release}
Requires:   libwayland-cursor = %{version}-%{release}
Requires:   libwayland-egl = %{version}-%{release}
Requires:   libwayland-server = %{version}-%{release}

%description devel
It contains the libraries and header files for developing applications that use wayland.

%package    -n libwayland-client
Summary:    wayland client library for wayland
Requires:   libffi

%description -n libwayland-client
It contains the wayland client libraries

%package    -n libwayland-cursor
Summary:    wayland cursor library for wayland
Requires:   libwayland-client = %{version}-%{release}

%description -n libwayland-cursor
It contains the wayland cursor libraries

%package    -n libwayland-egl
Summary:    wayland egl library for wayland

%description -n libwayland-egl
It contains the wayland egl libraries

%package    -n libwayland-server
Summary:    wayland server library for wayland
Requires:   libffi-devel

%description -n libwayland-server
It contains the wayland server libraries

%prep
%autosetup -p1

%build
CONFIGURE_OPTS=(
    -Ddocumentation=false
    )
%meson "${CONFIGURE_OPTS[@]}"
%meson_build

%install
%meson_install

%ldconfig_scriptlets

%check
%meson_test

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%license COPYING

%files devel
%defattr(-,root,root)
%{_bindir}/wayland-scanner
%{_includedir}/wayland-*.h
%{_libdir}/pkgconfig/wayland-*.pc
%{_libdir}/libwayland-*.so
%{_datadir}/aclocal/wayland-scanner.m4
%dir %{_datadir}/wayland
%{_datadir}/wayland/wayland-scanner.mk
%{_datadir}/wayland/wayland.xml
%{_datadir}/wayland/wayland.dtd

%files -n libwayland-client
%defattr(-,root,root)
%{_libdir}/libwayland-client.so.0*

%files -n libwayland-cursor
%defattr(-,root,root)
%{_libdir}/libwayland-cursor.so.0*

%files -n libwayland-egl
%defattr(-,root,root)
%{_libdir}/libwayland-egl.so.1*

%files -n libwayland-server
%defattr(-,root,root)
%{_libdir}/libwayland-server.so.0*

%changelog
* Thu Feb 29 2024 Anmol Jain <anmol.jain@broadcom.com> 1.20.0-5
- Bump version as a part of expat upgrade
* Mon Jul 31 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.20.0-4
- Add libffi-devel to requires of libwayland-server
* Wed Sep 28 2022 Shivani Agarwal <shivania2@vmware.com> 1.20.0-3
- Fix CVE-2021-3782
* Thu Aug 25 2022 Tejaswini Jayaramaiah <jtejaswini@vmware.com> 1.20.0-2
- Bump up release version
* Tue Jun 14 2022 Tejaswini Jayaramaiah <jtejaswini@vmware.com> 1.20.0-1
- Initial build. First version
