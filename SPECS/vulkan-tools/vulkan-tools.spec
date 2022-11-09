Name:           vulkan-tools
Version:        1.3.231.1
Release:        1%{?dist}
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
mkdir build
cd build
python ../scripts/update_deps.py
cmake .. -C helper.cmake -DBUILD_CUBE=OFF -DBUILD_ICD=OFF -DINSTALL_ICD=OFF
cmake --build .

%install
cd build
%make_install

mv %{buildroot}/usr/local/* %{buildroot}/usr/

%ldconfig_scriptlets

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/*

%changelog
* Mon Nov 7 2022 Shivani Agarwal <shivania2@vmware.com> 1.3.231.1-1
- Initial version
