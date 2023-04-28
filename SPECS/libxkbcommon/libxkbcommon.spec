Summary:        X.Org X11 XKB parsing library
Name:           libxkbcommon
Version:        1.4.1
Release:        2%{?dist}
License:        MIT
URL:            https://xkbcommon.org
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://xkbcommon.org/download/%{name}-%{version}.tar.xz
%define sha512 %{name}=757b340aeab6d187917807a88015b5113475ab2172aaaa8e530b40ea60619b3fbdfa668fd62707d66ed8fb763e68fee19394fcbd519af7c01d8975c59fdf0d89

BuildRequires:  cmake
BuildRequires:  meson >= 0.50
BuildRequires:  libX11-devel
BuildRequires:  libxml2-devel
BuildRequires:  bison

Requires:       libX11
Requires:       libxml2

%description
%{name} is the X.Org library for compiling XKB maps into formats usable by
the X Server or other display servers.

%package        devel
Summary:        X.Org X11 XKB parsing development package
Requires:       %{name} = %{version}-%{release}

%description    devel
X.Org X11 XKB parsing development package

%package        x11
Summary:        X.Org X11 XKB keymap creation library
Requires:       %{name} = %{version}-%{release}

%description    x11
%{name}-x11 is the X.Org library for creating keymaps by querying the X
server.

%package        x11-devel
Summary:        X.Org x11 XKB keymap creation library
Requires:       %{name}-x11 = %{version}-%{release}

%description    x11-devel
X.Org X11 XKB keymap creation library development package

%package        utils
Summary:        X.Org X11 XKB parsing utilities
Requires:       %{name} = %{version}-%{release}

%description utils
%{name}-utils is a set of utilities to analyze and test XKB parsing.

%prep
%autosetup -p1

%build
%meson \
      -Denable-docs=false \
      -Denable-x11=true \
      -Denable-wayland=false \
      %{nil}

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
%{_libdir}/libxkbcommon.so.0.0.0
%{_libdir}/libxkbcommon.so.0
%{_libdir}/libxkbregistry.so.0.0.0
%{_libdir}/libxkbregistry.so.0

%files devel
%defattr(-,root,root)
%{_libdir}/libxkbcommon.so
%{_libdir}/libxkbregistry.so
%dir %{_includedir}/xkbcommon/
%{_includedir}/xkbcommon/xkbcommon.h
%{_includedir}/xkbcommon/xkbcommon-compat.h
%{_includedir}/xkbcommon/xkbcommon-compose.h
%{_includedir}/xkbcommon/xkbcommon-keysyms.h
%{_includedir}/xkbcommon/xkbcommon-names.h
%{_includedir}/xkbcommon/xkbregistry.h
%{_libdir}/pkgconfig/xkbcommon.pc
%{_libdir}/pkgconfig/xkbregistry.pc
%{_bindir}/xkbcli
%{_libexecdir}/*
%{_mandir}/man1/*

%ldconfig_scriptlets x11

%files x11
%defattr(-,root,root)
%{_libdir}/libxkbcommon-x11.so.0.0.0
%{_libdir}/libxkbcommon-x11.so.0

%files x11-devel
%defattr(-,root,root)
%{_libdir}/libxkbcommon-x11.so
%{_includedir}/xkbcommon/xkbcommon-x11.h
%{_libdir}/pkgconfig/xkbcommon-x11.pc

%changelog
* Wed Apr 19 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 1.4.1-2
- Bump version as a part of libxml2 upgrade
* Sun Sep 4 2022 Shivani Agarwal <shivania2@vmware.com> 1.4.1-1
- Initial version
