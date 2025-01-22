Summary:        user space library for accessing the DRM.
Name:           libdrm
Version:        2.4.110
Release:        3%{?dist}
License:        MIT
URL:            http://dri.freedesktop.org/
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://dri.freedesktop.org/libdrm/%{name}-%{version}.tar.xz
%define sha512  libdrm=52f92ef1fe4c218a1d7dba53ef43334dbfca80e3209afe59f3a32c4bf67473126534e990df07a931a12d46a3b997c21ef17c1c4d8a0c88d44d5c6c040e3b6be3

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
        -Dintel=true
        -Dradeon=false
        -Damdgpu=true
        -Dnouveau=true
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
* Wed Jan 22 2025 Tapas Kundu <tapas.kundu@broadcom.com> 2.4.110-3
- Bump version as a part of meson upgrade
* Sun Nov 6 2022 Shivani Agarwal <shivania2@vmware.com> 2.4.110-2
- Enable support for intel and nvidia driver
* Thu Jun 9 2022 Shivani Agarwal <shivania2@vmware.com> 2.4.110-1
- Upgrade to 2.4.110
* Thu Jun 13 2019 Alexey Makhalov <amakhalov@vmware.com> 2.4.98-1
- Version update
* Thu Nov 30 2017 Alexey Makhalov <amakhalov@vmware.com> 2.4.88-1
- Version update
* Thu Mar 03 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 2.4.67-1
- Updated to version
* Tue May 19 2015 Alexey Makhalov <amakhalov@vmware.com> 2.4.61-1
- initial version
