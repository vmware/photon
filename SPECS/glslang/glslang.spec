%global build_if %{photon_subrelease} >= 91

Name:           glslang
Version:        16.2.0
Release:        2%{?dist}
Summary:        OpenGL and OpenGL ES shader front end and validator
URL:            https://github.com/KhronosGroup/glslang
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/KhronosGroup/glslang/archive/refs/tags/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  ninja-build
BuildRequires:  python3-devel
BuildRequires:  spirv-tools-devel

Requires: %{name}-libs = %{version}-%{release}

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

%package        libs
Summary:        %{name} shared library

%description    libs
The %{name}-libs package contains shared libraries for %{name}

%prep
%autosetup -p1

%build
%cmake \
    -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
    -DCMAKE_BUILD_TYPE=Release \
    -DBUILD_SHARED_LIBS=ON \
    -DENABLE_OPT=ON \
    -DGLSLANG_TESTS=OFF \
    -DALLOW_EXTERNAL_SPIRV_TOOLS=ON

%cmake_build

%install
%cmake_install

%ldconfig_scriptlets libs

%files
%defattr(-,root,root)
%doc README.md
%{_bindir}/%{name}
%{_bindir}/%{name}Validator

%files devel
%defattr(-,root,root)
%{_includedir}/%{name}/
%{_libdir}/libSPIRV.so
%{_libdir}/libglslang.so
%{_libdir}/libglslang-default-resource-limits.so
%{_libdir}/cmake/*

%files libs
%defattr(-,root,root)
%{_libdir}/libSPIRV.so.*
%{_libdir}/libglslang.so.*
%{_libdir}/libglslang-default-resource-limits.so.*

%changelog
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 16.2.0-2
- Extended to build for subrelease 91 and above
* Sat Mar 28 2026 Ankit Jain <ankit-aj.jain@broadcom.com> 16.2.0-1
- Bump to build with updated mesa
* Wed Mar 18 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 11.13.0-4
- Bump version as a part of python3.14 upgrade
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
