Name:           vulkan-tools
Version:        1.3.231.1
Release:        6%{?dist}
Summary:        Vulkan tools
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
License:        ASL 2.0
URL:            https://github.com/KhronosGroup/Vulkan-Tools

Source0:        https://github.com/KhronosGroup/Vulkan-Tools/archive/refs/tags/Vulkan-Tools-%{version}.tar.gz
%define sha512  Vulkan-Tools-%{version}.tar.gz=48b87ac2d45496d031eff492ed562df08ec34b40fc94bc6eaf122c4203949b0db5fceccf2718eef1d90b891ef0681db1c9d945f1dd710fb0c99020e4e3efa025

BuildRequires:  cmake
BuildRequires:  ninja-build
BuildRequires:  python3-devel
BuildRequires:  vulkan-loader-devel
BuildRequires:  vulkan-headers
BuildRequires:  libxml2-devel
BuildRequires:  wayland-devel
BuildRequires:  libwayland-client
BuildRequires:  libwayland-cursor
BuildRequires:  libwayland-server
BuildRequires:  libwayland-egl
BuildRequires:  wayland-protocols-devel
BuildRequires:  libxcb-devel
BuildRequires:  libX11-devel
BuildRequires:  libXrandr-devel
BuildRequires:  libdrm-devel
BuildRequires:  llvm-devel
BuildRequires:  git

Requires:       vulkan-loader
Requires:       vulkan-headers
Requires:       mesa-vulkan-drivers
Requires:       libdrm
Requires:       libX11

%description
Vulkan tools

%prep
%autosetup -p1 -n Vulkan-Tools-sdk-%{version}

%build
%{cmake} \
    -GNinja \
    -DCMAKE_BUILD_TYPE=Debug \
    -DBUILD_CUBE=OFF \
    -DBUILD_ICD=OFF \
    -DINSTALL_ICD=OFF

%{cmake_build}

%install
%{cmake_install}

%{ldconfig_scriptlets}

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/*

%changelog
* Thu Mar 28 2024 Ashwin Dayanand Kamat <ashwin.kamat@broadcom.com> 1.3.231.1-6
- Bump version as a part of libxml2 upgrade
* Tue Feb 20 2024 Ashwin Dayanand Kamat <ashwin.kamat@broadcom.com> 1.3.231.1-5
- Bump version as a part of libxml2 upgrade
* Wed Jun 14 2023 Shivani Agarwal <shivania2@vmware.com> 1.3.231.1-4
- Bump version as a part of libX11 upgrade
* Wed Apr 19 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 1.3.231.1-3
- Bump version as a part of libxml2 upgrade
* Mon Jan 30 2023 Shivani Agarwal <shivania2@vmware.com> 1.3.231.1-2
- Minor changes in spec file
* Mon Nov 7 2022 Shivani Agarwal <shivania2@vmware.com> 1.3.231.1-1
- Initial version
