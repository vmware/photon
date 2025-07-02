Summary:        SPIR-V LLVM Translator
Name:           spirv-llvm-translator
Version:        18.1.13
Release:        1%{?dist}
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/KhronosGroup/SPIRV-LLVM-Translator

Source0:        https://github.com/KhronosGroup/SPIRV-LLVM-Translator/archive/refs/tags/SPIRV-LLVM-Translator-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  cmake
BuildRequires:  ninja-build
BuildRequires:  llvm-devel >= 18.1.0
BuildRequires:  clang-devel >= 18.1.0
BuildRequires:  spirv-headers-devel
BuildRequires:  spirv-tools-devel

Requires:       spirv-tools

BuildArch:      x86_64

%description
SPIRV-LLVM-Translator provides a tool and libraries for translating between LLVM IR and SPIR-V, enabling OpenCL and Vulkan toolchains.

%package devel
Summary:        Development files for SPIRV-LLVM-Translator
Requires:       %{name} = %{version}-%{release}
Requires:       llvm-devel >= 18.1.0

%description devel
CMake and header files for using SPIRV-LLVM-Translator in your own projects.

%package tools
Summary:        SPIRV-LLVM-Translator command-line tools
Requires:       %{name} = %{version}-%{release}

%description tools
This package contains command-line tools for SPIRV-LLVM-Translator, such as llvm-spirv.

%prep
%autosetup -n SPIRV-LLVM-Translator-%{version}

%build
%cmake \
    -G Ninja \
    -DBUILD_SHARED_LIBS=ON \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
    -DLLVM_DIR=%{_libdir}/cmake/llvm \
    -DLLVM_EXTERNAL_PROJECTS="SPIRV-Headers" \
    -DLLVM_EXTERNAL_SPIRV_HEADERS_SOURCE_DIR=%{_includedir}/spirv/unified1 \
    -DCMAKE_INSTALL_RPATH:BOOL=";"

%cmake_build

%install
%cmake_install

%files
%defattr(-,root,root)
%doc README.md
%{_libdir}/libLLVMSPIRVLib.so.*

%files tools
%defattr(-,root,root)
%{_bindir}/llvm-spirv

%files devel
%defattr(-,root,root)
%{_includedir}/LLVMSPIRVLib/
%{_libdir}/libLLVMSPIRVLib.so
%{_libdir}/pkgconfig/LLVMSPIRVLib.pc

%changelog
* Thu Jun 26 2025 Shivani Agarwal <shivania2@vmware.com> 18.1.13-1
- initial version required for libclc
