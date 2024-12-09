Summary:        Mesa is an OpenGL compatible 3D graphics library.
Name:           mesa
Version:        23.0.0
Release:        2%{?dist}
URL:            http://www.mesa3d.org
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://ftp.freedesktop.org/pub/%{name}/%{version}/%{name}-%{version}.tar.gz
%define sha512  %{name}=79e115c2e21198b61353d98f2eb44093ff7247e2793163b17bb00b6f30125253dc64761c3290bfb456df6de7b5dba9b7b7e9cc503aa0ff28516483f2f26f00ba

Source1: license.txt
%include %{SOURCE1}

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
BuildRequires:  glslang-devel
BuildRequires:  bison

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
%{meson} \
    -Dgallium-vdpau=disabled \
    -Dgallium-omx=disabled \
    -Dgallium-va=disabled \
    -Dgallium-xa=disabled \
    -Dgallium-nine=false \
    -Dgallium-opencl=disabled \
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
    -Dvulkan-drivers=auto \
    -Dintel-clc=disabled \
    -Dgles2=disabled \
    -Ddri3=disabled \
    -Dmicrosoft-clc=disabled \
    -Dbuild-aco-tests=false \
    %{nil}

%{meson_build}

%install
%{meson_install}

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
%{_datadir}/vulkan/icd.d/intel_icd.x86_64.json
%{_datadir}/vulkan/icd.d/intel_hasvk_icd.x86_64.json
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
* Thu Dec 12 2024 Ajay Kaher <ajay.kaher@broadcom.com> 23.0.0-2
- Release bump for SRP compliance
* Fri Feb 24 2023 Shivani Agarwal <shivania2@vmware.com> 23.0.0-1
- Upgrade Version
* Tue Jan 10 2023 Shivani Agarwal <shivania2@vmware.com> 22.3.0-1
- Upgrade mesa to 22.3.0 and enabled intel and Nvidia driver support
* Fri Jan 06 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 22.2.2-3
- Bump up due to change in elfutils
* Wed Nov 30 2022 Shivani Agarwal <shivania2@vmware.com> 22.2.2-2
- Enable libgbm
* Tue Oct 25 2022 Gerrit Photon <photon-checkins@vmware.com> 22.2.2-1
- Automatic Version Bump
* Tue Sep 27 2022 Shreenidhi Shedi <sshedi@vmware.com> 22.2.0-1
- Upgrade to v22.2.0
* Fri Jun 10 2022 Shivani Agarwal <shivania2@vmware.com> 22.1.1-1
- Initial Version
