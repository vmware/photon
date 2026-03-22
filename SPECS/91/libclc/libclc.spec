%global build_if %{photon_subrelease} <= 91

%define debug_package %{nil}

Summary:        OpenCL C language library implementation
Name:           libclc
Version:        18.1.8
Release:        1.1%{?dist}
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://libclc.llvm.org

Source0:        https://github.com/llvm/llvm-project/releases/download/llvmorg-%{version}/%{name}-%{version}.tar.xz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  cmake
BuildRequires:  llvm-devel >= 18.1.8
BuildRequires:  clang-devel >= 18.1.8
BuildRequires:  spirv-llvm-translator-tools
BuildRequires:  python3

Requires:       spirv-llvm-translator

%description
libclc is an open source implementation of the OpenCL C programming language
library requirements, as specified by the OpenCL 1.1 Specification.

%package devel
Summary:        Development files for libclc
Requires:       %{name} = %{version}-%{release}
Requires:       clang-devel >= 18.1.8
Requires:       spirv-llvm-translator-tools

%description devel
Development files for libclc, including headers and pkg-config files.

%package spirv
Summary:        SPIR-V subset of libclc
Requires:       %{name} = %{version}-%{release}

%description spirv
The libclc-spirv package contains only the spirv*-mesa3d-.spv files,
which are needed for Mesa OpenCL support with RustiCL.

%prep
%autosetup -n %{name}-%{version}.src

%build
%{cmake} \
    -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DCMAKE_INSTALL_DATADIR:PATH=%{_lib} \
    -DCMAKE_BUILD_TYPE=Release

%{cmake_build}

%install
%{cmake_install}

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%dir %{_libdir}/clc
%{_libdir}/clc/*.bc

%files spirv
%defattr(-,root,root)
%dir %{_libdir}/clc
%{_libdir}/clc/spirv-mesa3d-.spv
%{_libdir}/clc/spirv64-mesa3d-.spv

%files devel
%defattr(-,root,root)
%{_libdir}/pkgconfig/libclc.pc
%{_includedir}/clc

%changelog
* Wed Mar 18 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 18.1.8-1.1
- Bump after moving to SPECS/91
* Tue Jun 24 2025 Shivani Agarwal <shivania2@vmware.com> 18.1.8-1
- Initial libclc version, required for mesa
