Summary:        user space library for accessing the DRM.
Name:           libdrm
Version:        2.4.110
Release:        1%{?dist}
License:        MIT
URL:            http://dri.freedesktop.org/
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://dri.freedesktop.org/libdrm/%{name}-%{version}.tar.xz

BuildRequires:  meson
BuildRequires:  libpciaccess-devel
Requires:       libpciaccess
Provides:       pkgconfig(libdrm)

%description
libdrm provides a user space library for accessing the DRM, direct rendering manager, on operating systems that support the ioctl interface. libdrm is a low-level library, typically used by graphics drivers such as the Mesa DRI drivers, the X drivers, libva and similar projects.

%package        devel
Summary:        Header and development files
Requires:       %{name} = %{version}-%{release}

%description    devel
libdrm provides a user space library for accessing the DRM, direct rendering manager, on operating systems that support the ioctl interface. libdrm is a low-level library, typically used by graphics drivers such as the Mesa DRI drivers, the X drivers, libva and similar projects.

%prep
%autosetup -p1

%build
CONFIGURE_OPTS=(
        -Dintel=false
        -Dradeon=false
        -Damdgpu=true
        -Dnouveau=false
        -Dvmwgfx=false
        -Dlibkms=false
)

%meson "${CONFIGURE_OPTS[@]}"
meson --prefix=%{_prefix} build

%install
DESTDIR=%{buildroot}/ ninja -C build install

%ldconfig_scriptlets

%if 0%{?with_check}
%check
%meson_test
%endif

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_libdir}/lib*
%{_datadir}/libdrm/*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/pkgconfig*

%changelog
* Thu Oct 27 2022 User <user@example.org> 2.4.110-1
- initial version
