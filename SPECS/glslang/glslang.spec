Name:           glslang
Version:        11.13.0
Release:        3%{?dist}
Summary:        OpenGL and OpenGL ES shader front end and validator
URL:            https://github.com/KhronosGroup/glslang
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/KhronosGroup/glslang/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512  %{name}=20c2a6543b002648f459f26bd36b5c445afd6d8eae175e400dbe45632f11ca8de1f9e6f6e98fd6f910aa75d90063e174c095e7df26d9d4982192b84d08b0dc8b

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  ninja-build
BuildRequires:  python3-devel

%description
%{name} is the official reference compiler front end for the OpenGL
ES and OpenGL shading languages. It implements a strict
interpretation of the specifications for these languages.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description    devel
%{name} is the official reference compiler front end for the OpenGL
ES and OpenGL shading languages. It implements a strict
interpretation of the specifications for these languages.

%prep
%autosetup -p1

%build
%cmake \
    -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
    -DCMAKE_BUILD_TYPE=Debug

%cmake_build

%install
%cmake_install

%ldconfig_scriptlets

%files
%defattr(-,root,root)
%doc README.md README-spirv-remap.txt
%{_bindir}/%{name}Validator
%{_bindir}/spirv-remap
%{_libdir}/libglslang.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/%{name}/
%{_libdir}/libHLSL.so
%{_libdir}/libSPIRV.so
%{_libdir}/libSPVRemapper.so
%{_libdir}/libglslang.so
%{_libdir}/libglslang-default-resource-limits.so
%{_libdir}/cmake/*

%changelog
*   Wed Dec 11 2024 Tapas Kundu <tapas.kundu@broadcom.com> 11.13.0-3
-   Release bump for SRP compliance
*   Thu Dec 15 2022 Shivani Agarwal <shivania2@vmware.com> 11.13.0-2
-   Add support for shared libraries
*   Thu Dec 15 2022 Gerrit Photon <photon-checkins@vmware.com> 11.13.0-1
-   Automatic Version Bump
*   Tue Nov 1 2022 Gerrit Photon <photon-checkins@vmware.com> 11.12.0-1
-   Automatic Version Bump
*   Tue Sep 27 2022 Shreenidhi Shedi <sshedi@vmware.com> 11.11.0-1
-   First build, needed for mesa-22.2.0
