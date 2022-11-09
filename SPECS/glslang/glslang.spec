Summary:        OpenGL and OpenGL ES shader front end and validator
Name:           glslang
Version:        1.3.231.1
Release:        1%{?dist}
License:        BSD and GPLv3+ and ASL 2.0
URL:            https://github.com/KhronosGroup/glslang
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/KhronosGroup/glslang/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512  glslang=91379a0077ae8c1cec07f63397e29552e3e77e51109495907dc3163a5e597e7345888f70c072c409a014aaf4bb1e76aee8311002119d036a842589f83ba0ef5e

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  ninja-build
BuildRequires:  spirv-tools-devel
BuildRequires:  spirv-tools-libs
BuildRequires:  python3-devel

%description
glslang is the official reference compiler front end for the OpenGL
ES and OpenGL shading languages. It implements a strict
interpretation of the specifications for these languages.

%package        devel
Summary:        Development files for glslang
Requires:       %{name} = %{version}-%{release}

%description    devel
glslang is the official reference compiler front end for the OpenGL
ES and OpenGL shading languages. It implements a strict
interpretation of the specifications for these languages.

%prep
%autosetup -p1 -n %{name}-sdk-%{version}

%build
%cmake -DCMAKE_INSTALL_LIBDIR=%{_lib}
%cmake_build

%install
%cmake_install

# we don't want them in here
rm -rf %{buildroot}%{_includedir}/SPIRV

%clean
rm -rf %{buildroot}/*

%ldconfig_scriptlets

%files
%defattr(-,root,root)
%doc README.md README-spirv-remap.txt
%{_bindir}/glslangValidator
%{_bindir}/spirv-remap
%{_libdir}/libglslang.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/glslang/
%{_libdir}/libHLSL.so
%{_libdir}/libSPIRV.so
%{_libdir}/libSPVRemapper.so
%{_libdir}/libglslang.so
%{_libdir}/libglslang-default-resource-limits.so
%{_libdir}/cmake/*

%changelog
*   Thu Nov 17 2022 Shivani Agarwal <shivanai2@vmware.com> 1.3.231.1-1
-   initial version
