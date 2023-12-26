Summary:        Mesa is an OpenGL compatible 3D graphics library.
Name:           mesa
Version:        23.0.0
Release:        2%{?dist}
License:        MIT
URL:            http://www.mesa3d.org/
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://ftp.freedesktop.org/pub/%{name}/%{version}/%{name}-%{version}.tar.gz
%define sha512  %{name}=79e115c2e21198b61353d98f2eb44093ff7247e2793163b17bb00b6f30125253dc64761c3290bfb456df6de7b5dba9b7b7e9cc503aa0ff28516483f2f26f00ba

BuildRequires:  libdrm-devel >= 2.4.88
BuildRequires:  meson
BuildRequires:  cmake
BuildRequires:  elfutils-libelf-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-markupsafe
BuildRequires:  python3-mako
BuildRequires:  libffi-devel
BuildRequires:  llvm-devel
BuildRequires:  expat-devel
BuildRequires:  wayland-devel
BuildRequires:  wayland-protocols-devel
BuildRequires:  libwayland-client
BuildRequires:  libwayland-server
BuildRequires:  libwayland-egl
BuildRequires:  libpciaccess-devel
BuildRequires:  bison
BuildRequires:  clang-devel
BuildRequires:  glslang-devel

Requires:       libllvm
Requires:       expat-libs
Requires:       libdrm
Requires:       libwayland-client
Provides:       pkg-config(dri)

%description
Mesa is an OpenGL compatible 3D graphics library.

%package        vulkan-drivers
Summary:        Mesa Vulkan drivers

%description     vulkan-drivers
The drivers with support for the Vulkan API.

%package        libgbm
Summary:        Mesa gbm runtime library
Requires:       expat
Requires:       libdrm
Requires:       libwayland-server
Provides:       libgbm

%description    libgbm
Mesa gbm runtime library.

%package        libgbm-devel
Summary:        Mesa libgbm development package
Requires:       %{name}-libgbm = %{version}-%{release}
Provides:       libgbm-devel

%description    libgbm-devel
Mesa libgbm development package.

%prep
%autosetup -n %{name}-%{name}-%{version} -p1

%build
meson --prefix=%{_prefix} build/ \
        -Dgallium-vdpau=disabled \
        -Dgallium-omx=disabled \
        -Dgallium-va=disabled \
        -Dgallium-xa=disabled \
        -Dgallium-nine=false \
        -Dgallium-opencl=disabled \
        -Dvulkan-drivers=auto \
        -Dplatforms=wayland \
        -Dosmesa=false \
        -Dvulkan-layers=device-select \
        -Dshared-glapi=disabled \
        -Dgles1=disabled \
        -Dopengl=false \
        -Dgbm=enabled \
        -Dglx=disabled \
        -Degl=disabled \
        -Dglvnd=false \
        -Dllvm=enabled \
        -Dshared-llvm=enabled \
        -Dvalgrind=disabled \
        -Dbuild-tests=false \
        -Dselinux=false \
        -Dintel-clc=disabled \
        -Dgles2=disabled \
        -Ddri3=disabled \
        -Dmicrosoft-clc=disabled \
        %{nil}

%install
DESTDIR=%{buildroot}/ ninja -C build install

%clean
rm -rf %{buildroot}/*

%ldconfig_scriptlets

%files
%defattr(-,root,root)

%files vulkan-drivers
%defattr(-,root,root)
%{_libdir}/libvulkan_lvp.so
%{_datadir}/vulkan/icd.d/lvp_icd.*.json
%{_datadir}/vulkan/implicit_layer.d/VkLayer_MESA_device_select.json
%{_libdir}/libVkLayer_MESA_device_select.so
%{_datadir}/drirc.d/00-mesa-defaults.conf
%ifarch x86_64
%{_libdir}/libvulkan_radeon.so
%{_libdir}/libvulkan_intel.so
%{_libdir}/libvulkan_intel_hasvk.so
%{_datadir}/drirc.d/00-radv-defaults.conf
%{_datadir}/vulkan/icd.d/intel_hasvk_icd.x86_64.json
%{_datadir}/vulkan/icd.d/intel_icd.x86_64.json
%{_datadir}/vulkan/icd.d/radeon_icd.x86_64.json
%endif

%files libgbm
%defattr(-,root,root)
%{_libdir}/libgbm.so.1
%{_libdir}/libgbm.so.1.*

%files libgbm-devel
%defattr(-,root,root)
%{_libdir}/libgbm.so
%{_includedir}/gbm.h
%{_libdir}/pkgconfig/gbm.pc

%changelog
* Thu Jan 04 2024 Nitesh Kumar <kunitesh@vmware.com> 23.0.0-2
- Bump up as part of python3-markupsafe v2.1.1 upgrade
* Fri Feb 24 2023 Shivani Agarwal <shivania2@vmware.com> 23.0.0-1
- Upgrade Version
* Mon Nov 7 2022 Shivani Agarwal <shivania2@vmware.com> 22.3.0-1
- Upgrade mesa to 22.3.0 and enabled intel and Nvidia driver support
* Mon Sep 19 2022 Shivani Agarwal <shivania2@vmware.com> 22.1.1-2
- Enable libgbm
* Fri Jun 10 2022 Shivani Agarwal <shivania2@vmware.com> 22.1.1-1
- Initial Version
