Summary:        Vulkan Header files and API registry
Name:           vulkan-headers
Version:        1.3.230
Release:        1%{?dist}
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        ASL 2.0

URL:            https://github.com/KhronosGroup/Vulkan-Headers
Source0:        https://github.com/KhronosGroup/Vulkan-Headers/archive/refs/tags/Vulkan-Headers-%{version}.tar.gz
%define sha512  Vulkan-Headers-%{version}.tar.gz=1d94c220e6e0a274c57ffac09885d7154ed5b79aebd6018a20117d0f7907a5af875e697908b4cd4acdb9c4f6b0ff96f4c70b8d68dd2c1c2add90f41d85feaa2e

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
*   Thu Oct 06 2022 Gerrit Photon <photon-checkins@vmware.com> 1.3.230-1
-   Automatic Version Bump
*   Mon Jun 13 2022 Shivani Agarwal <shivania2@vmware.com> 1.3.216-1
-   Initial version
