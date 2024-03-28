%global debug_package   %{nil}
%define llvm_maj_ver    15

Summary:        A collection of modular and reusable compiler and toolchain technologies.
Name:           llvm
Version:        15.0.7
Release:        4%{?dist}
License:        NCSA
URL:            https://llvm.org
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/llvm/llvm-project/releases/tag/%{name}-%{version}.src.tar.xz
%define sha512 %{name}=ed8d565515b1bc6164e4ff06d3388ba92e332850305496fd65db9adf1ec87bd9dd1bfde49dd41be5d5216289efc72bfd287cd7392f2bba80b740d4c314c749e5

Source1: https://github.com/llvm/llvm-project/releases/download/cmake-%{version}.src.tar.xz
%define sha512 cmake=a87c3c0976c7295e5d51f7a3dbd4129c4b5ff0dc95bac494a5011641743a5950a0aa7d9c44fae570284573b9f673a395fc3160b45b6b4ba54ced9ed5f21dd717

BuildRequires:  cmake
BuildRequires:  libxml2-devel
BuildRequires:  libffi-devel
BuildRequires:  python3-devel
BuildRequires:  ninja-build
BuildRequires:  glibc-devel

Requires:       libxml2
Requires:       libllvm = %{version}-%{release}

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
Requires:       %{name} = %{version}-%{release}
Group:          System Environment/Libraries
%description -n libllvm
The libllvm package contains shared libraries for llvm

%prep
%autosetup -p1 -n %{name}-%{version}.src -a1

%build
mv cmake-%{version}.src/Modules/*.cmake cmake/modules
# LLVM_PARALLEL_LINK_JOBS=4 is chosen as a middle ground number
# if we use a bigger value, we will hit OOM, so don't increase it
# unless you are absolutely sure

%cmake -G Ninja \
      -DCMAKE_INSTALL_PREFIX=%{_usr} \
      -DBUILD_SHARED_LIBS:BOOL=OFF \
      -DLLVM_PARALLEL_LINK_JOBS=4 \
      -DLLVM_PARALLEL_COMPILE_JOBS=$(nproc) \
      -DLLVM_ENABLE_FFI:BOOL=ON \
      -DCMAKE_BUILD_TYPE=Release \
      -DLLVM_BUILD_LLVM_DYLIB:BOOL=ON \
      -DLLVM_TARGETS_TO_BUILD="host;AMDGPU;BPF" \
      -DLLVM_INCLUDE_GO_TESTS=No \
      -DLLVM_ENABLE_RTTI:BOOL=ON \
      -DLLVM_INCLUDE_BENCHMARKS=OFF \
      -Wno-dev

%cmake_build

%install
%cmake_install

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%if 0%{?with_check}
%check
# deactivate security hardening for tests
rm -f $(dirname $(gcc -print-libgcc-file-name))/../specs
cd %{__cmake_builddir}
make %{?_smp_mflags} check-llvm
%endif

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so
%{_libdir}/*.so.*
%exclude %{_libdir}/libLLVM-%{version}.so
%exclude %{_libdir}/libLLVM-%{llvm_maj_ver}.so
%exclude %{_libdir}/libLLVM.so
%dir %{_datadir}/opt-viewer
%{_datadir}/opt-viewer/opt-diff.py
%{_datadir}/opt-viewer/opt-stats.py
%{_datadir}/opt-viewer/opt-viewer.py
%{_datadir}/opt-viewer/optpmap.py
%{_datadir}/opt-viewer/optrecord.py
%{_datadir}/opt-viewer/style.css

%files devel
%defattr(-,root,root)
%{_libdir}/*.a
%{_libdir}/cmake/*
%{_includedir}/*

%files -n libllvm
%defattr(-,root,root)
%{_libdir}/libLLVM*.so

%changelog
* Thu Mar 28 2024 Ashwin Dayanand Kamat <ashwin.kamat@broadcom.com> 15.0.7-4
- Bump version as a part of libxml2 upgrade
* Tue Feb 20 2024 Ashwin Dayanand Kamat <ashwin.kamat@broadcom.com> 15.0.7-3
- Bump version as a part of libxml2 upgrade
* Wed Apr 19 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 15.0.7-2
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
