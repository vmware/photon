%global debug_package %{nil}

Summary:        C, C++, Objective C and Objective C++ front-end for the LLVM compiler.
Name:           clang
Version:        12.0.0
Release:        2%{?dist}
License:        NCSA
URL:            http://clang.llvm.org
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/llvm/llvm-project/releases/download/llvmorg-%{version}/%{name}-%{version}.src.tar.xz
%define sha512 %{name}=f5613b9bffc962467d3bedb7f66b4e057e2781eb63c5dadfd3cf0b02453e29eff0a4f844889031292f06a8b4c081d4d41c515b7f719826ce5c4209a09df9f1f6

BuildRequires:  cmake
BuildRequires:  llvm-devel = %{version}
BuildRequires:  ncurses-devel
BuildRequires:  zlib-devel
BuildRequires:  libxml2-devel
BuildRequires:  python3-devel
BuildRequires:  ninja-build
BuildRequires:  bison

Requires:       libstdc++-devel
Requires:       ncurses
Requires:       llvm
Requires:       zlib
Requires:       libxml2
Requires:       python3

%description
The goal of the Clang project is to create a new C based language front-end:
C, C++, Objective C/C++, OpenCL C and others for the LLVM compiler. You can get and build the source today.

%package        devel
Summary:        Development headers for clang
Requires:       %{name} = %{version}-%{release}
%description    devel
The clang-devel package contains libraries, header files and documentation for developing applications that use clang.

%prep
%autosetup -n %{name}-%{version}.src -p1

%build
# if we use a bigger value, we will hit OOM, so don't increase it
# unless you are absolutely sure
build_jobs="$(( ($(nproc)+1) / 2 ))"
link_jobs="$(( (build_jobs + 1) / 2 ))"

%ifarch aarch64
[ "${build_jobs}" -gt 4 ] && build_jobs=4 || :
%endif

[ "${link_jobs}" -gt 2 ] && link_jobs=2 || :

%{cmake} -G Ninja \
    -DLLVM_PARALLEL_LINK_JOBS=1 \
    -DCMAKE_INSTALL_PREFIX=%{_usr} \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    -DLLVM_MAIN_INCLUDE_DIR=%{_includedir} \
    -DBUILD_SHARED_LIBS=OFF \
    -DCMAKE_C_FLAGS=-pipe \
    -DCMAKE_CXX_FLAGS=-pipe \
    -Wno-dev

# Build libclang-cpp.so first. This ensures that when libLLVM.so is linking, there
# are no other compile jobs running. This will help reduce OOM errors on the
# builders without having to artificially limit the number of concurrent jobs.
%{cmake_build} --target libclang-cpp.so

%{cmake_build}

%install
%{cmake_install}

%if 0%{?with_check}
%check
# deactivate security hardening for tests
rm -f $(dirname $(gcc -print-libgcc-file-name))/../specs
%{make_build} -C %{__cmake_builddir} check-llvm
%endif

%clean
rm -rf %{buildroot}/*

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libexecdir}/*
%{_libdir}/*.so.*
%{_datadir}/*

%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/cmake/*
%{_libdir}/clang/*
%{_includedir}/*

%changelog
* Thu Feb 20 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 12.0.0-2
- Build instruction improvements to reduce resource consumption
* Mon Nov 21 2022 Shreenidhi Shedi <sshedi@vmware.com> 12.0.0-1
- Upgrade to v12.0.0
* Thu Dec 09 2021 Prashant S Chauhan <psinghchauha@vmware.com> 11.0.1-3
- Bump up to compile with python 3.10
* Thu Nov 18 2021 Nitesh Kumar <kunitesh@vmware.com> 11.0.1-2
- Release bump up to use libxml2 2.9.12-1.
* Thu Feb 04 2021 Shreenidhi Shedi <sshedi@vmware.com> 11.0.1-1
- Upgrade to v11.0.1
* Mon Aug 24 2020 Gerrit Photon <photon-checkins@vmware.com> 10.0.1-1
- Automatic Version Bump
* Tue Jun 23 2020 Tapas Kundu <tkundu@vmware.com> 6.0.1-2
- Build with python3
- Mass removal python2
* Thu Aug 09 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 6.0.1-1
- Update to version 6.0.1 to get it to build with gcc 7.3
* Wed Jun 28 2017 Chang Lee <changlee@vmware.com> 4.0.0-2
- Updated %check
* Fri Apr 7 2017 Alexey Makhalov <amakhalov@vmware.com> 4.0.0-1
- Version update
* Wed Jan 11 2017 Xiaolin Li <xiaolinl@vmware.com>  3.9.1-1
- Initial build.
