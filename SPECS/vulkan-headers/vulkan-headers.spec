Summary:        Vulkan Header files and API registry
Name:           vulkan-headers
Version:        1.3.234
Release:        1%{?dist}
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        ASL 2.0
URL:            https://github.com/KhronosGroup/Vulkan-Headers

Source0:        https://github.com/KhronosGroup/Vulkan-Headers/archive/refs/tags/Vulkan-Headers-%{version}.tar.gz
%define sha512  Vulkan-Headers=e2b157af033aae8b5a0f0a48e43887a72d7c5b9b8b8e65fc8eec6368822e5905918e3850e85aa9eeaed2ad7f28e12d3c815024a08f85c295c26ce6b536bd6ec9

BuildRequires:  cmake

BuildArch:      noarch

%description
Vulkan Header files and API registry

%prep
%autosetup -n Vulkan-Headers-%{version} -p1

%build
%{cmake} \
    -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
    -DCMAKE_C_FLAGS_RELEASE:STRING="-DNDEBUG" \
    -DCMAKE_CXX_FLAGS_RELEASE:STRING="-DNDEBUG" \
    -DCMAKE_Fortran_FLAGS_RELEASE:STRING="-DNDEBUG" \
    -DCMAKE_INSTALL_DO_STRIP:BOOL=OFF \
    -DINCLUDE_INSTALL_DIR:PATH=%{_includedir} \
    -DLIB_INSTALL_DIR:PATH=%{_libdir} \
    -DSYSCONF_INSTALL_DIR:PATH=%{_sysconfdir} \
    -DSHARE_INSTALL_PREFIX:PATH=%{_datadir}

%{cmake_build}

%install
%{cmake_install}

%if 0%{?with_check}
%check
%{cmake_check}
%endif

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%license LICENSE.txt
%doc README.md
%{_includedir}/vulkan/
%{_includedir}/vk_video/
%dir %{_datadir}/vulkan/
%{_datadir}/vulkan/registry/
%{_datadir}/cmake/*

%changelog
* Fri Nov 11 2022 Michelle Wang <michellew@vmware.com> 1.3.234-1
- Bump up version since mesa version bump up
* Fri Oct 28 2022 Gerrit Photon <photon-checkins@vmware.com> 1.3.232-1
- Automatic Version Bump
* Thu Oct 06 2022 Gerrit Photon <photon-checkins@vmware.com> 1.3.230-1
- Automatic Version Bump
* Mon Jun 13 2022 Shivani Agarwal <shivania2@vmware.com> 1.3.216-1
- Initial version
