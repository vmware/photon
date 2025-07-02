%define network_required 1
%global debug_package   %{nil}
%define llvm_maj_ver    18

Summary:        A collection of modular and reusable compiler and toolchain technologies.
Name:           llvm
Version:        18.1.8
Release:        2%{?dist}
URL:            https://llvm.org
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/llvm/llvm-project/releases/tag/%{name}-%{version}.src.tar.xz

Source1: https://github.com/llvm/llvm-project/releases/download/cmake-%{version}.src.tar.xz

Source2: license.txt
%include %{SOURCE2}

BuildRequires:  cmake
BuildRequires:  libxml2-devel
BuildRequires:  libffi-devel
BuildRequires:  python3-devel
BuildRequires:  ninja-build
BuildRequires:  glibc-devel

Requires:       libllvm = %{version}-%{release}

Patch0: 0001-llvm-CodeGen-Fix-build-failure-for-MI-dump.patch

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
Group:          System Environment/Libraries
Requires:       libxml2

%description -n libllvm
The libllvm package contains shared libraries for llvm

%prep
%autosetup -p1 -n %{name}-%{version}.src -a1

%build
mv cmake-%{version}.src ../cmake

# if we use a bigger value, we will hit OOM, so don't increase it
# unless you are absolutely sure
build_jobs="$(( ($(nproc)+1) / 2 ))"
link_jobs="$(( (build_jobs + 1) / 2 ))"

%ifarch aarch64
[ "${build_jobs}" -gt 4 ] && build_jobs=4 || :
%endif

[ "${link_jobs}" -gt 2 ] && link_jobs=2 || :

%{cmake} -G Ninja \
  -DCMAKE_INSTALL_PREFIX=%{_usr} \
  -DBUILD_SHARED_LIBS:BOOL=ON \
  -DLLVM_PARALLEL_LINK_JOBS=${link_jobs} \
  -DLLVM_PARALLEL_COMPILE_JOBS=${build_jobs} \
  -DLLVM_ENABLE_FFI:BOOL=ON \
  -DCMAKE_BUILD_TYPE=Release \
  -DLLVM_INCLUDE_TESTS=OFF \
  -DLLVM_ENABLE_LIBPFM:BOOL=OFF \
  -DLLVM_INCLUDE_EXAMPLES:BOOL=OFF \
  -DLLVM_ENABLE_LIBCXX:BOOL=OFF \
  -DLLVM_BUILD_LLVM_DYLIB:BOOL=ON \
  -DLLVM_TARGETS_TO_BUILD="host;AMDGPU;BPF" \
  -DLLVM_INCLUDE_GO_TESTS=No \
  -DLLVM_ENABLE_RTTI:BOOL=ON \
  -DLLVM_INCLUDE_BENCHMARKS=OFF \
  -DCMAKE_C_FLAGS=-pipe \
  -DCMAKE_CXX_FLAGS=-pipe \
  -Wno-dev

# Build libLLVM.so first. This ensures that when libLLVM.so is linking, there
# are no other compile jobs running. This will help reduce OOM errors on the
# builders without having to artificially limit the number of concurrent jobs.
%{cmake_build} --target LLVM

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
%dir %{_datadir}/opt-viewer
%{_datadir}/opt-viewer/opt-diff.py
%{_datadir}/opt-viewer/opt-stats.py
%{_datadir}/opt-viewer/opt-viewer.py
%{_datadir}/opt-viewer/optpmap.py
%{_datadir}/opt-viewer/optrecord.py
%{_datadir}/opt-viewer/style.css

%files devel
%defattr(-,root,root)
%{_libdir}/cmake/*
%{_includedir}/*
%{_libdir}/*.so

%files -n libllvm
%defattr(-,root,root)
%{_libdir}/*.so.*

%changelog
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
