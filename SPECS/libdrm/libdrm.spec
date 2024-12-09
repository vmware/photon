Summary:        user space library for accessing the DRM.
Name:           libdrm
Version:        2.4.113
Release:        3%{?dist}
URL:            http://dri.freedesktop.org/
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://dri.freedesktop.org/libdrm/%{name}-%{version}.tar.xz
%define sha512  libdrm=fca9834ce090f63ce6dc6d04491a2c5e86162fdddfc8ea70d55a6cdeb401be656388aae1577e58f463a78d8dc502be0a641908784819874e20bbec9a39a057e0

Source1: license.txt
%include %{SOURCE1}

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
        -Dintel=enabled
        -Dradeon=disabled
        -Damdgpu=enabled
        -Dnouveau=enabled
        -Dvmwgfx=disabled
        -Dvalgrind=disabled
        -Dtests=false
        -Dman-pages=disabled
        -Dcairo-tests=disabled
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
* Wed Dec 11 2024 Mukul Sikka <mukul.sikka@broadcom.com> 2.4.113-3
- Release bump for SRP compliance
* Sun Nov 6 2022 Shivani Agarwal <shivania2@vmware.com> 2.4.113-2
- Enable support for intel and nvidia driver
* Tue Oct 25 2022 Gerrit Photon <photon-checkins@vmware.com> 2.4.113-1
- Automatic Version Bump
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
