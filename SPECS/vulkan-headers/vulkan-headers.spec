Summary:        Vulkan Header files and API registry
Name:           vulkan-headers
Version:        1.3.232
Release:        1%{?dist}
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        ASL 2.0

URL:            https://github.com/KhronosGroup/Vulkan-Headers
Source0:        https://github.com/KhronosGroup/Vulkan-Headers/archive/refs/tags/Vulkan-Headers-%{version}.tar.gz
%define sha512  Vulkan-Headers-%{version}.tar.gz=78d7a2bc85c4a483cf9a6a9c34e9da81fa348175d24ce2fa9b7d0e40bf66c2b60abc6edc051db19086e35fa7c06f68e2fae5d5e280a355a47c75d73a2a46eaca

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

%changelog
*   Fri Oct 28 2022 Gerrit Photon <photon-checkins@vmware.com> 1.3.232-1
-   Automatic Version Bump
*   Thu Oct 06 2022 Gerrit Photon <photon-checkins@vmware.com> 1.3.230-1
-   Automatic Version Bump
*   Mon Jun 13 2022 Shivani Agarwal <shivania2@vmware.com> 1.3.216-1
-   Initial version
