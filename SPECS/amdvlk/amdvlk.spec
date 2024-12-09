Summary:        AMD Open Source Driver for Vulkan
Name:           amdvlk
Version:        2023.Q1.3
Release:        4%{?dist}
URL:            https://github.com/GPUOpen-Drivers/AMDVLK
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/GPUOpen-Drivers/AMDVLK/archive/refs/tags/%{name}-%{version}.tar.xz
%define sha512  %{name}=118c960c1a737f48095667283278d901284bdd5d6e9853759026781600decb59a81436683545063316661a11300dbc1be2b6e71cecf9968be91a31d83d09ae34

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  cmake
BuildRequires:  ninja-build
BuildRequires:  proto
BuildRequires:  libxcb-devel
BuildRequires:  libX11-devel
BuildRequires:  wayland-devel
BuildRequires:  libwayland-client
BuildRequires:  libxml2-devel
BuildRequires:  libffi-devel
BuildRequires:  libXrandr-devel
BuildRequires:  libXrender-devel
BuildRequires:  libxshmfence-devel

%description
AMD Open Source Driver for Vulkan

%prep
%autosetup -p1

%build
cmake -B %{_target_platform} \
      -DCMAKE_INSTALL_DO_STRIP:BOOL=OFF \
      -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} \
      -DINCLUDE_INSTALL_DIR:PATH=%{_includedir} \
      -DLIB_INSTALL_DIR:PATH=%{_libdir} \
      -DCMAKE_INSTALL_LIBDIR=lib \
      -DSYSCONF_INSTALL_DIR:PATH=%{_sysconfdir} \
      -DSHARE_INSTALL_PREFIX:PATH=%{_datadir} \
      -GNinja -DCMAKE_BUILD_TYPE=RelWithDebInfo \
      -S xgl -DLLVM_PARALLEL_LINK_JOBS=1 \
      -DVKI_RAY_TRACING=OFF -Wno-dev
cmake --build %{_target_platform} %{?_smp_mflags} --verbose

%install
DESTDIR=%{buildroot} cmake --install %{_target_platform} --component icd
chmod +x %{buildroot}%{_libdir}/amdvlk64.so

%clean
rm -rf %{buildroot}/*

%ldconfig_scriptlets

%files
%defattr(-,root,root)
%{_sysconfdir}/vulkan/icd.d/amd_icd64.json
%{_sysconfdir}/vulkan/implicit_layer.d/amd_icd64.json
%{_libdir}/amdvlk64.so
%license %{_datadir}/doc/%{name}/LICENSE.txt

%changelog
* Wed Dec 11 2024 HarinadhD <harinadh.dommaraju@broadcom.com> 2023.Q1.3-4
- Release bump for SRP compliance
* Wed Jun 14 2023 Shivani Agarwal <shivania2@vmware.com> 2023.Q1.3-3
- Bump version as a part of libX11 upgrade
* Thu May 25 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 2023.Q1.3-2
- Bump version as a part of libxml2 upgrade
* Thu Feb 23 2023 Shivani Agarwal <shivania2@vmware.com> - 2023.Q1.3-1
- Initial version
