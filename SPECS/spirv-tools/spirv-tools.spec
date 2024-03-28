Summary:        API and commands for processing SPIR-V modules
Name:           spirv-tools
Version:        1.3.231.1
Release:        5%{?dist}
License:        ASL 2.0
URL:            https://github.com/KhronosGroup/SPIRV-Tools/
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/KhronosGroup/SPIRV-Tools/archive/refs/tags/SPIRV-Tools-%{version}.tar.gz
%define sha512  SPIRV-Tools-%{version}.tar.gz=e999bcd7002fd821b2aa5e53de37d501113735059ca61cb7df4c6383fb2566a5371adbe82faff52461c8791f76cd30b13e22e2b39954f7ec1942d80dd8f50636

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  ninja-build
BuildRequires:  python3-devel
BuildRequires:  python3-xml
BuildRequires:  libxml2-devel
BuildRequires:  spirv-headers-devel

Requires:       libxml2
Requires:       %{name}-libs = %{version}-%{release}

%description
The package includes an assembler, binary module parser,
disassembler, and validator for SPIR-V..

%package        libs
Summary:        Library files for spirv-tools

%description    libs
library files for spirv-tools

%package        devel
Summary:        Development files for spirv-tools
Requires:       %{name} = %{version}-%{release}
Requires:       libxml2-devel

%description    devel
Development files for spirv-tools

%prep
%autosetup -p1 -n SPIRV-Tools-sdk-%{version}

%build
%cmake  \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_LIBDIR=%{_lib} \
    -DSPIRV-Headers_SOURCE_DIR=%{_prefix} \
    -DPYTHON_EXECUTABLE=%{__python3} \
    -DSPIRV_TOOLS_BUILD_STATIC=OFF \
    -GNinja

%cmake_build

%install
%cmake_install

%ldconfig_scriptlets libs

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/spirv-as
%{_bindir}/spirv-cfg
%{_bindir}/spirv-dis
%{_bindir}/spirv-lesspipe.sh
%{_bindir}/spirv-link
%{_bindir}/spirv-lint
%{_bindir}/spirv-opt
%{_bindir}/spirv-reduce
%{_bindir}/spirv-val

%files devel
%defattr(-,root,root)
%{_includedir}/spirv-tools/
%{_libdir}/cmake/*
%{_libdir}/pkgconfig/SPIRV-Tools-shared.pc
%{_libdir}/pkgconfig/SPIRV-Tools.pc

%files libs
%defattr(-,root,root)
%{_libdir}/libSPIRV-Tools-diff.so
%{_libdir}/libSPIRV-Tools-link.so
%{_libdir}/libSPIRV-Tools-lint.so
%{_libdir}/libSPIRV-Tools-opt.so
%{_libdir}/libSPIRV-Tools.so
%{_libdir}/libSPIRV-Tools-reduce.so
%{_libdir}/libSPIRV-Tools-shared.so

%changelog
*   Thu Mar 28 2024 Ashwin Dayanand Kamat <ashwin.kamat@broadcom.com> 1.3.231.1-5
-   Bump version as a part of libxml2 upgrade
*   Tue Feb 20 2024 Ashwin Dayanand Kamat <ashwin.kamat@broadcom.com> 1.3.231.1-4
-   Bump version as a part of libxml2 upgrade
*   Wed Apr 19 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 1.3.231.1-3
-   Bump version as a part of libxml2 upgrade
*   Mon Jan 30 2023 Shivani Agarwal <shivania2@vmware.com> 1.3.231.1-2
-   Minor changes in spec file
*   Tue Nov 15 2022 Shivani Agarwal <shivania2@vmware.com> 1.3.231.1-1
-   initial version
