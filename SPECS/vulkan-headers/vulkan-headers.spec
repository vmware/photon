Summary:        Vulkan Header files and API registry
Name:           vulkan-headers
Version:        1.3.237
Release:        1%{?dist}
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        ASL 2.0

URL:            https://github.com/KhronosGroup/Vulkan-Headers
Source0:        https://github.com/KhronosGroup/Vulkan-Headers/archive/refs/tags/Vulkan-Headers-%{version}.tar.gz
%define sha512  Vulkan-Headers-%{version}.tar.gz=6c259fc0ea02a8e2f6b1f5597559f6dfc0f5b5c8553a9c8aa81ac73414a1e672dc45e5e3499bcad70ac27a4802a98cfeb6eada5497a980832fdd7f947da508f8

BuildRequires:  cmake

BuildArch:      noarch

%description
Vulkan Header files and API registry

%prep
%autosetup -n Vulkan-Headers-%{version} -p1

%build
%cmake -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
        -DCMAKE_C_FLAGS_RELEASE:STRING="-DNDEBUG" \
        -DCMAKE_CXX_FLAGS_RELEASE:STRING="-DNDEBUG" \
        -DCMAKE_Fortran_FLAGS_RELEASE:STRING="-DNDEBUG" \
        -DCMAKE_INSTALL_DO_STRIP:BOOL=OFF \
        -DINCLUDE_INSTALL_DIR:PATH=%{_includedir} \
        -DLIB_INSTALL_DIR:PATH=%{_libdir} \
        -DSYSCONF_INSTALL_DIR:PATH=%{_sysconfdir} \
        -DSHARE_INSTALL_PREFIX:PATH=%{_datadir}
%cmake_build

%install
%cmake_install

%check
%cmake_check

%clean
rm -rf %{buildroot}/*

%files
%license LICENSE.txt
%doc README.md
%{_includedir}/vulkan/
%{_includedir}/vk_video/
%dir %{_datadir}/vulkan/
%{_datadir}/vulkan/registry/
%{_datadir}/cmake/VulkanHeaders/

%changelog
* Mon Dec 12 2022 Shivani Agarwal <shivania2@vmware.com> 1.3.237-1
- Upgrade version to 1.3.237
* Mon Jun 13 2022 Shivani Agarwal <shivania2@vmware.com> 1.3.216-1
- Initial version
