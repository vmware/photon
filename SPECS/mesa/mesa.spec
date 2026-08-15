%global build_if %{photon_subrelease} >= 91

Summary:        Mesa is an OpenGL compatible 3D graphics library.
Name:           mesa
Version:        26.2.0
Release:        4%{?dist}
URL:            http://www.mesa3d.org
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://archive.mesa3d.org/%{name}-%{version}.tar.xz

Source1: license.txt
%include %{SOURCE1}

Patch0:         0001-Remove-Nouveau-from-vulkan-drivers-and-gallium-drive.patch
Patch1:         0002-jay-Fix-build-with-GCC-12-lacking-C23-fixed-underly.patch
%ifarch aarch64
Patch2:         0003-Disable-tegra-in-aarch64.patch
%endif

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
BuildRequires:  libunwind-devel
BuildRequires:  libclc-devel
BuildRequires:  libclc-spirv
BuildRequires:  python3-PyYAML
BuildRequires:  spirv-tools-devel
BuildRequires:  spirv-llvm-translator-devel
BuildRequires:  clang-devel
BuildRequires:  libunwind-devel
BuildRequires:  lm-sensors-devel
BuildRequires:  libdisplay-info-devel
%ifarch aarch64
BuildRequires:  python3-pycparser
%endif

Requires:       libllvm
Requires:       expat-libs
Requires:       libdrm
Requires:       libwayland-client

Provides:       pkg-config(dri)

%description
Mesa is an OpenGL compatible 3D graphics library.

%package        vulkan-drivers
Summary:        Mesa Vulkan drivers
Requires:       elfutils-libelf
Requires:       expat-libs
Requires:       libdisplay-info
Requires:       libdrm
Requires:       libllvm
Requires:       libwayland-client
Requires:       spirv-tools-libs

%description    vulkan-drivers
The drivers with support for the Vulkan API.

%package        libgbm
Summary:        Mesa gbm runtime library
Requires:       %{name}-libgallium = %{version}-%{release}
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

%package libEGL
Summary: Mesa EGL runtime library
Group: System/Libraries
Requires: %{name}-libgbm = %{version}-%{release}
Requires: %{name}-libgallium = %{version}-%{release}
Requires: expat-libs
Requires: libdrm
Requires: libwayland-client

%description libEGL
This package contains the Mesa implementation of the EGL library.

%package libEGL-devel
Summary: EGL development headers for Mesa
Group: Development/C
Requires: %{name}-libEGL = %{version}-%{release}

%description libEGL-devel
Development files (headers and pkg-config) for Mesa EGL.

%package dri-devel
Summary: Development files for Mesa DRI
Group: Development/Libraries

%description dri-devel
This package contains development files for the Mesa Direct Rendering Infrastructure (DRI).

%package libgallium
Summary: Gallium shared library from Mesa
Group: System/Libraries
Requires: elfutils-libelf
Requires: expat-libs
Requires: libdrm
Requires: libllvm
Requires: spirv-tools-libs

%description libgallium
This package contains the Gallium shared library from Mesa.

%prep
%autosetup -n %{name}-%{version} -p1

%build
%{meson} \
    -Dgallium-va=disabled \
    -Dplatforms=wayland \
    -Dvulkan-layers=device-select \
    -Dgles1=disabled \
    -Dopengl=false \
    -Dgbm=enabled \
    -Dglx=disabled \
    -Dgallium-mediafoundation=disabled \
    -Dxlib-lease=disabled \
    -Dandroid-libbacktrace=disabled \
    -Dlmsensors=disabled \
    -Degl=enabled \
    -Dglvnd=disabled \
    -Dllvm=enabled \
    -Dshared-llvm=enabled \
    -Dvalgrind=disabled \
    -Dbuild-tests=false \
    -Dvulkan-drivers=auto \
    -Dgles2=disabled \
    -Dmicrosoft-clc=disabled \
    -Dbuild-aco-tests=false \
    -Dgallium-rusticl=false \
    -Dandroid-libbacktrace=disabled \
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
%{_datadir}/drirc.d/00-anv-defaults.conf
%{_datadir}/drirc.d/00-lavapipe-defaults.conf
%ifarch x86_64
%{_libdir}/libvulkan_radeon.so
%{_libdir}/libvulkan_intel.so
%{_libdir}/libvulkan_intel_hasvk.so
%{_datadir}/drirc.d/00-radv-defaults.conf
%{_datadir}/drirc.d/00-hasvk-defaults.conf
%{_datadir}/vulkan/icd.d/intel_icd.x86_64.json
%{_datadir}/vulkan/icd.d/intel_hasvk_icd.x86_64.json
%{_datadir}/vulkan/icd.d/radeon_icd.x86_64.json
%endif
%ifarch aarch64
%{_libdir}/libvulkan_freedreno.so
%{_libdir}/libvulkan_intel.so
%{_libdir}/libvulkan_panfrost.so
%{_libdir}/libvulkan_asahi.so
%{_datadir}/drirc.d/00-turnip-defaults.conf
%{_datadir}/drirc.d/00-panvk-defaults.conf
%{_datadir}/drirc.d/00-hk-defaults.conf
%{_datadir}/vulkan/icd.d/freedreno_icd.aarch64.json
%{_datadir}/vulkan/icd.d/intel_icd.aarch64.json
%{_datadir}/vulkan/icd.d/panfrost_icd.aarch64.json
%{_datadir}/vulkan/icd.d/asahi_icd.aarch64.json
%endif

%files libgbm
%defattr(-,root,root)
%{_libdir}/libgbm.so.1
%{_libdir}/libgbm.so.1.*
%{_libdir}/gbm/dri_gbm.so

%files libgbm-devel
%defattr(-,root,root)
%{_libdir}/libgbm.so
%{_includedir}/gbm.h
%{_libdir}/pkgconfig/gbm.pc
%{_includedir}/gbm_backend_abi.h

%files libEGL
%defattr(-,root,root)
%{_libdir}/libEGL.so.1*
%{_libdir}/libEGL.so

%files libEGL-devel
%defattr(-,root,root)
%{_includedir}/EGL/egl.h
%{_includedir}/EGL/eglext.h
%{_includedir}/EGL/eglext_angle.h
%{_includedir}/EGL/eglmesaext.h
%{_includedir}/EGL/eglplatform.h
%{_includedir}/KHR/khrplatform.h
%{_libdir}/pkgconfig/egl.pc

%files dri-devel
%defattr(-,root,root)
%{_includedir}/GL/internal/dri_interface.h
%{_libdir}/pkgconfig/dri.pc

%files libgallium
%defattr(-,root,root)
%{_libdir}/libgallium-*.so
%{_datadir}/drirc.d/00-iris-defaults.conf
%{_datadir}/drirc.d/00-virtio_gpu-defaults.conf
%{_datadir}/drirc.d/00-vmwgfx-defaults.conf
%{_datadir}/drirc.d/00-zink-defaults.conf
%ifarch x86_64
%{_datadir}/drirc.d/00-crocus-defaults.conf
%{_datadir}/drirc.d/00-r300-defaults.conf
%{_datadir}/drirc.d/00-r600-defaults.conf
%{_datadir}/drirc.d/00-radeonsi-defaults.conf
%endif
%ifarch aarch64
%{_datadir}/drirc.d/00-v3d-defaults.conf
%{_datadir}/drirc.d/00-panfrost-defaults.conf
%{_datadir}/drirc.d/00-asahi-defaults.conf
%{_datadir}/drirc.d/00-msm-defaults.conf
%endif

%changelog
* Sat Aug 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 26.2.0-4
- Extend to build for 91 and above
* Tue Aug 11 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 26.2.0-3
- Fix patch applicability issue during aarch64 build, mishap from last fix
* Mon Aug 10 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 26.2.0-2
- Fix aarch64 build
* Thu Aug 06 2026 Shivani Agarwal <shivani.agarwal@broadcom.com> 26.2.0-1
- Upgrade mesa to 26.2.0
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 25.3.6-2
- Extended to build for subrelease 91 and above
* Sat Mar 28 2026 Ankit Jain <ankit-aj.jain@broadcom.com> 25.3.6-1
- Bump to build with updated llvm
- Fixed requires for whole spec
* Wed Mar 18 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 25.1.4-3
- Bump version as a part of python3.14 upgrade
* Thu Oct 30 2025 Shivani Agarwal <shivani.agarwal@broadcom.com> 25.1.4-2
- Remove Tegra driver from Gallium driver auto list as it depends on Nouveau
- which is already disabled due to Rust and Bindgen dependencies.
* Fri Oct 24 2025 Shivani Agarwal <shivani.agarwal@broadcom.com> 25.1.4-1
- Upgrade mesa to 25.1.4 version to support the VK_KHR_sampler_ycbcr_conversion extension
* Thu Oct 23 2025 Ankit Jain <ankit-aj.jain@broadcom.com> 23.3.6-1
- Bump to build with updated llvm
* Tue Sep 02 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 23.0.0-5
- Rebuild with llvm shared libs
* Wed Apr 09 2025 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 23.0.0-4
- Version bump for expat upgrade
* Wed Jan 22 2025 Tapas Kundu <tapas.kundu@broadcom.com> 23.0.0-3
- Bump version as a part of meson upgrade
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
