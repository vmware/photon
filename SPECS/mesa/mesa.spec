Summary:        Mesa is an OpenGL compatible 3D graphics library.
Name:           mesa
Version:        22.2.2
Release:        1%{?dist}
License:        MIT
URL:            http://www.mesa3d.org
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://archive.mesa3d.org/%{name}-%{version}.tar.xz
%define sha512 %{name}=a1eb67e1ae4880c79b1fdc570f4389baba0b8ba796da7e695c9af19a7d92b6c06b95570e6c796548b61355989025fb7efbf9acac74cbd695f7e297dc913b933c

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

Requires:       libllvm
Requires:       expat-libs

Provides:       pkg-config(dri)

%description
Mesa is an OpenGL compatible 3D graphics library.

%package vulkan-drivers
Summary:        Mesa Vulkan drivers

%description vulkan-drivers
The drivers with support for the Vulkan API.

%prep
%autosetup -p1

%build
%{meson} \
    -Dgallium-vdpau=disabled \
    -Dgallium-xvmc=disabled \
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
    -Dgbm=disabled \
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
%{_datadir}/drirc.d/00-radv-defaults.conf
%{_datadir}/vulkan/icd.d/intel_icd.x86_64.json
%{_datadir}/vulkan/icd.d/radeon_icd.x86_64.json
%endif

%changelog
* Tue Oct 25 2022 Gerrit Photon <photon-checkins@vmware.com> 22.2.2-1
- Automatic Version Bump
* Tue Sep 27 2022 Shreenidhi Shedi <sshedi@vmware.com> 22.2.0-1
- Upgrade to v22.2.0
* Fri Jun 10 2022 Shivani Agarwal <shivania2@vmware.com> 22.1.1-1
- Initial Version
