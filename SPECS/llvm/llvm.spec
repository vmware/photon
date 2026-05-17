%global build_if %{photon_subrelease} >= 91

%define network_required 1
%global debug_package   %{nil}
%define llvm_maj_ver    22

Summary:        A collection of modular and reusable compiler and toolchain technologies.
Name:           llvm
Version:        22.1.0
Release:        2%{?dist}
URL:            https://llvm.org
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/llvm/llvm-project/releases/download/llvmorg-%{version}/%{name}-project-%{version}.src.tar.xz
Source1: https://github.com/KhronosGroup/SPIRV-LLVM-Translator/archive/refs/tags/SPIRV-LLVM-Translator-%{version}.tar.gz

Source2: license.txt
%include %{SOURCE2}

Patch0: llvm-spirv-translator-photon.patch

BuildRequires:  cmake
BuildRequires:  libxml2-devel
BuildRequires:  libffi-devel
BuildRequires:  python3-devel
BuildRequires:  ninja-build
BuildRequires:  glibc-devel
BuildRequires:  swig
BuildRequires:  libedit-devel
BuildRequires:  ncurses-devel
BuildRequires:  xz-devel
BuildRequires:  zlib-devel
BuildRequires:  spirv-headers-devel
BuildRequires:  spirv-tools-devel

Requires:       libllvm = %{version}-%{release}
Requires:       libclang = %{version}-%{release}
Requires:       spirv-llvm-translator = %{version}-%{release}
Requires:       zlib
Requires:       zstd-libs

%description
The LLVM Project is a collection of modular and reusable compiler and toolchain technologies.
Despite its name, LLVM has little to do with traditional virtual machines, though it does
provide helpful libraries that can be used to build them. The name "LLVM" itself is not an
acronym; it is the full name of the project.

%package        devel
Summary:        Development headers for llvm
Requires:       %{name} = %{version}-%{release}

%description    devel
The llvm-devel package contains libraries, header files and documentation
for developing applications that use llvm.

%package -n     libllvm
Summary:        llvm shared library
Requires:       libedit
Requires:       libffi
Requires:       libxml2
Requires:       zlib
Requires:       zstd-libs

%description -n libllvm
The libllvm package contains shared libraries for llvm

%package -n     clang
Summary:        C, C++, Objective C and Objective C++ front-end for the LLVM compiler.
Requires:       libclang = %{version}-%{release}
Requires:       llvm = %{version}-%{release}
Requires:       libstdc++-devel
Requires:       ncurses
Requires:       zlib
Requires:       libxml2
Requires:       python3

%description -n clang
The goal of the Clang project is to create a new C based language front-end:
C, C++, Objective C/C++, OpenCL C and others for the LLVM compiler. You can get and build the source today.

%package -n     clang-devel
Summary:        Development headers for clang
Requires:       clang = %{version}-%{release}
Requires:       llvm-devel = %{version}-%{release}
Requires:       ncurses-devel

%description -n clang-devel
The clang-devel package contains libraries, header files and documentation for developing applications that use clang.

%package -n     libclang
Summary:        clang shared library

%description -n libclang
The libclang package contains shared libraries for clang

%package -n     libclc
Summary:        OpenCL C language library implementation
Requires:       spirv-llvm-translator-tools

%description -n libclc
libclc is an open source implementation of the OpenCL C programming language
library requirements, as specified by the OpenCL 1.1 Specification.

%package -n     libclc-devel
Summary:        Development files for libclc
Requires:       libclc = %{version}-%{release}
Requires:       clang-devel

%description -n libclc-devel
Development files for libclc, including headers and pkg-config files.

%package -n     libclc-spirv
Summary:        SPIR-V subset of libclc
Requires:       libclc = %{version}-%{release}
Requires:       spirv-tools

%description -n libclc-spirv
The libclc-spirv package contains only the spirv*-mesa3d-.spv files,
which are needed for Mesa OpenCL support with RustiCL.

%package -n     lldb
Summary:        A next generation, high-performance debugger.
Requires:       liblldb = %{version}-%{release}
Requires:       clang = %{version}-%{release}
Requires:       lua

%description -n lldb
LLDB is a next generation, high-performance debugger.
It is built as a set of reusable components which highly leverage existing libraries in the larger LLVM Project,
such as the Clang expression parser and LLVM disassembler.

%package -n     lldb-devel
Summary:        Development headers for lldb
Requires:       lldb = %{version}-%{release}

%description -n lldb-devel
The lldb-devel package contains libraries, header files and documentation
for developing applications that use lldb.

%package -n     liblldb
Summary:        lldb shared library
Group:          System Environment/Libraries

%description -n liblldb
The liblldb package contains shared libraries for lldb

%package -n     python3-lldb
Summary:        Python module for lldb
Requires:       lldb = %{version}-%{release}
Requires:       python3-six

%description -n python3-lldb
The package contains the LLDB Python3 module.

%package -n     spirv-llvm-translator
Summary:        LLVM to SPIR-V Translator
Requires:       libllvm = %{version}-%{release}

%description -n spirv-llvm-translator
A tool and library for translating between LLVM IR and SPIR-V.

%package -n     spirv-llvm-translator-devel
Summary:        Development files for the LLVM to SPIR-V Translator
Requires:       spirv-llvm-translator = %{version}-%{release}
%description -n spirv-llvm-translator-devel
Headers and libraries for spirv-llvm-translator.

%package -n     spirv-llvm-translator-tools
Summary:        SPIRV-LLVM-Translator command-line tools
Requires:       spirv-llvm-translator = %{version}-%{release}

%description -n spirv-llvm-translator-tools
This package contains command-line tools for SPIRV-LLVM-Translator, such as llvm-spirv.

%prep
%autosetup -p1 -n %{name}-project-%{version}.src -a1

%build
# Calculate build jobs to prevent OOM
build_jobs="$(( ($(nproc)+1) / 2 ))"
link_jobs="$(( (build_jobs + 1) / 2 ))"

%ifarch aarch64
[ "${build_jobs}" -gt 4 ] && build_jobs=4 || :
%endif
[ "${link_jobs}" -gt 2 ] && link_jobs=2 || :

cd llvm

%cmake -G Ninja \
  -DCMAKE_INSTALL_PREFIX=%{_usr} \
  -DCMAKE_BUILD_TYPE=Release \
  "-DLLVM_ENABLE_PROJECTS=clang;lldb" \
  "-DLLVM_ENABLE_RUNTIMES=libclc" \
  "-DLLVM_EXTERNAL_PROJECTS=SPIRV-LLVM-Translator" \
  "-DLLVM_EXTERNAL_SPIRV_LLVM_TRANSLATOR_SOURCE_DIR=%{_builddir}/%{name}-project-%{version}.src/SPIRV-LLVM-Translator-%{version}" \
  -DBUILD_SHARED_LIBS:BOOL=OFF \
  -DLLVM_BUILD_LLVM_DYLIB:BOOL=ON \
  -DLLVM_LINK_LLVM_DYLIB:BOOL=ON \
  -DLLVM_PARALLEL_LINK_JOBS=${link_jobs} \
  -DLLVM_PARALLEL_COMPILE_JOBS=${build_jobs} \
  -DLLVM_ENABLE_FFI:BOOL=ON \
  -DLLVM_ENABLE_RTTI:BOOL=ON \
  "-DLLVM_TARGETS_TO_BUILD=host;AMDGPU;BPF" \
  -DLLVM_INCLUDE_TESTS=OFF \
  -DLLVM_INCLUDE_EXAMPLES=OFF \
  -DLLVM_INCLUDE_BENCHMARKS=OFF \
  -DLLDB_ENABLE_PYTHON=ON \
  -DLLDB_PYTHON_EXE_RELATIVE_PATH=%{python3} \
  -Wno-dev

# Build the core LLVM shared library first to mitigate OOM errors
%{cmake_build} --target LLVM

# Build the clang core library next
%{cmake_build} --target libclang-cpp.so

%{cmake_build} --target llvm-spirv

# Build the rest of the monorepo
%{cmake_build}

%install
cd llvm
%{cmake_install}

mkdir -p %{buildroot}%{python3_sitelib}
mv %{buildroot}%{_libdir}/{libear,libscanbuild} %{buildroot}%{python3_sitelib}

mkdir -p %{buildroot}%{_libdir}/clc
mv %{buildroot}%{_libdir}/clang/*/lib/libclc/* %{buildroot}%{_libdir}/clc/
sed -i 's|libexecdir=.*|libexecdir=%{_libdir}/clc|' %{buildroot}%{_datadir}/pkgconfig/libclc.pc

mkdir -p %{buildroot}%{_includedir}/clc
cp -a %{_builddir}/%{name}-project-%{version}.src/libclc/clc/include/clc/* %{buildroot}%{_includedir}/clc/

find %{buildroot}%{_libdir} -name '*.a' -delete
# Patch LLVM and Clang CMake manifests to not crash when finding missing .a files
sed -i 's/FATAL_ERROR "The imported target/WARNING "The imported target/g' %{buildroot}%{_libdir}/cmake/llvm/LLVMExports.cmake
sed -i 's/FATAL_ERROR "The imported target/WARNING "The imported target/g' %{buildroot}%{_libdir}/cmake/clang/ClangTargets.cmake

%if 0%{?with_check}
%check
# deactivate security hardening for tests
rm -f $(dirname $(gcc -print-libgcc-file-name))/../specs
ninja -C build check-llvm
%endif

%clean
rm -rf %{buildroot}/*

%ldconfig_scriptlets -n libllvm
%ldconfig_scriptlets -n libclang
%ldconfig_scriptlets -n liblldb
%ldconfig_scriptlets -n spirv-llvm-translator

%files
%defattr(-,root,root)
%{_bindir}/bugpoint
%{_bindir}/dsymutil
%{_bindir}/llvm-*
%{_bindir}/llc
%{_bindir}/lli
%{_bindir}/opt
%{_bindir}/sancov
%{_bindir}/sanstats
%{_bindir}/verify-uselistorder
%{_bindir}/reduce-chunk-list
%{_bindir}/yaml2macho-core
%dir %{_datadir}/opt-viewer
%{_datadir}/opt-viewer/opt-diff.py
%{_datadir}/opt-viewer/opt-stats.py
%{_datadir}/opt-viewer/opt-viewer.py
%{_datadir}/opt-viewer/optpmap.py
%{_datadir}/opt-viewer/optrecord.py
%{_datadir}/opt-viewer/style.css

%files devel
%defattr(-,root,root)
%{_libdir}/cmake/llvm/*
%{_includedir}/llvm
%{_includedir}/llvm-c/
%{_libdir}/libLLVM*.so
%{_libdir}/libLTO.so
%{_libdir}/libRemarks.so

%files -n libllvm
%defattr(-,root,root)
%{_libdir}/libLLVM*.so.*
%{_libdir}/libLTO.so.*
%{_libdir}/libRemarks.so.*

%files -n clang
%defattr(-,root,root)
%{_bindir}/amdgpu-arch
%{_bindir}/analyze-build
%{_bindir}/clang
%{_bindir}/clang++
%{_bindir}/clang-*
%{_bindir}/diagtool
%{_bindir}/git-clang-format
%{_bindir}/hmaptool
%{_bindir}/intercept-build
%{_bindir}/nvptx-arch
%{_bindir}/offload-arch
%{_bindir}/scan-build
%{_bindir}/scan-build-py
%{_bindir}/scan-view
%{_libexecdir}/*
%{_datadir}/clang
%{_datadir}/man
%{_datadir}/scan-build
%{_datadir}/scan-view

%files -n clang-devel
%defattr(-,root,root)
%{_libdir}/libclang*.so
%{_libdir}/cmake/clang/*
%{_libdir}/clang/*
%{_includedir}/clang
%{_includedir}/clang-c/
%{python3_sitelib}/libear
%{python3_sitelib}/libscanbuild

%files -n libclang
%{_libdir}/libclang*.so.*

%files -n libclc
%defattr(-,root,root)
%dir %{_libdir}/clc
%{_libdir}/clc/*.bc

%files -n libclc-spirv
%defattr(-,root,root)
%dir %{_libdir}/clc
%{_libdir}/clc/spirv-mesa3d-.spv
%{_libdir}/clc/spirv64-mesa3d-.spv

%files -n libclc-devel
%defattr(-,root,root)
%dir %{_includedir}/clc
%{_includedir}/clc/*
%{_datadir}/pkgconfig/libclc.pc

%files -n lldb
%defattr(-,root,root)
%{_bindir}/lldb
%{_bindir}/lldb-*

%files -n lldb-devel
%defattr(-,root,root)
%{_libdir}/liblldb.so
%{_libdir}/liblldbIntelFeatures.so
%{_libdir}/lua/*/lldb.so
%{_includedir}/lldb

%files -n liblldb
%{_libdir}/liblldb.so.*
%{_libdir}/liblldbIntelFeatures.so.*

%files -n python3-lldb
%defattr(-,root,root,-)
%{python3_sitelib}/lldb

%files -n spirv-llvm-translator
%defattr(-,root,root)
%{_libdir}/libLLVMSPIRVLib.so.*

%files -n spirv-llvm-translator-tools
%defattr(-,root,root)
%{_bindir}/llvm-spirv

%files -n spirv-llvm-translator-devel
%defattr(-,root,root)
%{_includedir}/LLVMSPIRVLib/
%{_libdir}/libLLVMSPIRVLib.so
%{_libdir}/pkgconfig/LLVMSPIRVLib.pc

%changelog
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 22.1.0-2
- Extended to build for subrelease 91 and above
* Wed Mar 18 2026 Ankit Jain <ankit-aj.jain@broadcom.com> 22.1.0-1
- Update llvm to 22.1.0 to build latest version of rust-1.93.1
* Wed Mar 18 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 18.1.8-3
- Bump version as a part of python3.14 upgrade
* Fri Oct 24 2025 Shivani Agarwal <shivani.agarwal@broadcom.com> 18.1.8-2
- Enable BUILD_SHARED_LIBS=ON to avoid duplicate LLVM command-line option registration errors
* Thu Oct 23 2025 Ankit Jain <ankit-aj.jain@broadcom.com> 18.1.8-1
- Update llvm to 18.1.8 to build latest version of rust-1.87.0
* Tue Sep 02 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 15.0.7-6
- Enable shared libs
* Tue Jan 28 2025 Alexey Makhalov <alexey.makhalov@broadcom.com> 15.0.7-5
- Use compiler -pipe option to reduce storage pressure
* Thu Dec 12 2024 Ajay Kaher <ajay.kaher@broadcom.com> 15.0.7-4
- Release bump for SRP compliance
* Mon Oct 30 2023 Harinadh D <hdommaraju@vmware.com> 15.0.7-3
- remove llvm dependency for libllvm
* Thu May 25 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 15.0.7-2
- Bump version as a part of libxml2 upgrade
* Sat Feb 18 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 15.0.7-1
- Upgrade to v15.0.7
* Fri Dec 16 2022 Shreenidhi Shedi <sshedi@vmware.com> 15.0.6-1
- Upgrade to v15.0.6
- Don't package libLLVM shared libraries
* Tue Dec 06 2022 Prashant S Chauhan <psinghchauha@vmware.com> 15.0.1-2
- Update release to compile with python 3.11
* Tue Sep 27 2022 Shreenidhi Shedi <sshedi@vmware.com> 15.0.1-1
- Upgrade to v15.0.1
* Mon Jun 20 2022 Shreenidhi Shedi <sshedi@vmware.com> 12.0.0-4
- Use cmake macros for build
* Wed May 11 2022 Shreenidhi Shedi <sshedi@vmware.com> 12.0.0-3
- Bump version as a part of libffi upgrade
* Wed Nov 17 2021 Nitesh Kumar <kunitesh@vmware.com> 12.0.0-2
- Release bump up to use libxml2 2.9.12-1.
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 12.0.0-1
- Automatic Version Bump
* Thu Feb 04 2021 Shreenidhi Shedi <sshedi@vmware.com> 11.0.1-1
- Upgrade to v11.0.1
* Tue Sep 22 2020 Harinadh D <hdommaraju@vmware.com> 10.0.1-1
- add libLLVM.so to libllvm
* Thu Sep 10 2020 Susant Sahani Sahani <ssahani@vmware.com> 10.0.1-2
- Enable LLVM_ENABLE_RTTI
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 10.0.1-1
- Automatic Version Bump
* Tue Jun 23 2020 Tapas Kundu <tkundu@vmware.com> 6.0.1-4
- Build with python3
- Mass removal python2
* Wed Jun 26 2019 Keerthana K <keerthanak@vmware.com> 6.0.1-3
- Enable target BPF
* Tue Jan 08 2019 Alexey Makhalov <amakhalov@vmware.com> 6.0.1-2
- Added BuildRequires python2
* Thu Aug 09 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 6.0.1-1
- Update to version 6.0.1 to get it to build with gcc 7.3
* Thu Aug 10 2017 Alexey Makhalov <amakhalov@vmware.com> 4.0.0-3
- Make check fix
* Fri Apr 14 2017 Alexey Makhalov <amakhalov@vmware.com> 4.0.0-2
- BuildRequires libffi-devel
* Fri Apr 7 2017 Alexey Makhalov <amakhalov@vmware.com> 4.0.0-1
- Version update
* Wed Jan 11 2017 Xiaolin Li <xiaolinl@vmware.com>  3.9.1-1
- Initial build.
