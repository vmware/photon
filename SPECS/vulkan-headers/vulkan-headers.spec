Summary:        Vulkan Header files and API registry
Name:           vulkan-headers
Version:        1.3.216
Release:        1%{?dist}
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        ASL 2.0

URL:            https://github.com/KhronosGroup/Vulkan-Headers
Source0:        https://github.com/KhronosGroup/Vulkan-Headers/archive/refs/tags/Vulkan-Headers-%{version}.tar.gz
%define sha512  Vulkan-Headers-%{version}.tar.gz=25bd561227145e144866749c6a8b83eab9f67a03d62b5277758d93125b2283facff74ad1876280d357a4ae67f20b5b17a2a6168514c4b7fad3d9c3ff8a2ba51f

BuildRequires:  cmake

BuildArch:      noarch

%description
Vulkan Header files and API registry

%prep
%autosetup -n Vulkan-Headers-%{version} -p1

%build
%cmake -DCMAKE_INSTALL_LIBDIR=%{_libdir}
%make_build

%install
%make_install

%check
make %{?_smp_mflags} check

%clean
rm -rf %{buildroot}/*

%files
%license LICENSE.txt
%doc README.md
%{_includedir}/vulkan/
%{_includedir}/vk_video/
%dir %{_datadir}/vulkan/
%{_datadir}/vulkan/registry/

%changelog
*   Mon Jun 13 2022 Shivani Agarwal <shivania2@vmware.com> 1.3.216-1
-   Initial version
