Name:           vulkan-tools
Version:        1.3.231.1
Release:        5%{?dist}
Summary:        Vulkan tools
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/KhronosGroup/Vulkan-Tools

Source0:        https://github.com/KhronosGroup/Vulkan-Tools/archive/refs/tags/Vulkan-Tools-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

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
* Wed Dec 11 2024 Keerthana K <keerthana.kalyanasundaram@broadcom.com> 1.3.231.1-5
- Release bump for SRP compliance
* Wed Jun 14 2023 Shivani Agarwal <shivania2@vmware.com> 1.3.231.1-4
- Bump version as a part of libX11 upgrade
* Thu May 25 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 1.3.231.1-3
- Bump version as a part of libxml2 upgrade
* Mon Jan 30 2023 Shivani Agarwal <shivania2@vmware.com> 1.3.231.1-2
- Minor changes in spec file
* Mon Nov 7 2022 Shivani Agarwal <shivania2@vmware.com> 1.3.231.1-1
- Initial version
