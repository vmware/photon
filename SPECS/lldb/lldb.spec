Summary:        A next generation, high-performance debugger.
Name:           lldb
Version:        12.0.0
Release:        2%{?dist}
License:        NCSA
URL:            http://lldb.llvm.org
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://releases.llvm.org/%{version}/%{name}-%{version}.src.tar.xz
%define sha512 %{name}=20acd58ea9a8a8f237dc7ade44702cf610c80f48d157f77a4f35cf210f4b89fa783e9e7bf747010a2ef921f8dc1658b63d3f3563c0e19c6019a3d9af41378a22

BuildRequires:  cmake
BuildRequires:  llvm-devel = %{version}
BuildRequires:  clang-devel = %{version}
BuildRequires:  ncurses-devel
BuildRequires:  swig
BuildRequires:  zlib-devel
BuildRequires:  libxml2-devel
BuildRequires:  python3-devel
BuildRequires:  lua-devel
BuildRequires:  ninja-build

Requires:       lua
Requires:       llvm = %{version}
Requires:       clang = %{version}
Requires:       ncurses
Requires:       zlib
Requires:       libxml2

%description
LLDB is a next generation, high-performance debugger.
It is built as a set of reusable components which highly leverage existing libraries in the larger LLVM Project,
such as the Clang expression parser and LLVM disassembler.

%package        devel
Summary:        Development headers for lldb
Requires:       %{name} = %{version}-%{release}
%description    devel
The lldb-devel package contains libraries, header files and documentation
for developing applications that use lldb.

%package -n     python3-lldb
Summary:        Python module for lldb
Requires:       %{name} = %{version}-%{release}
Requires:       python3-six
%description -n python3-lldb
The package contains the LLDB Python3 module.

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

%{cmake} -G Ninja\
      -DCMAKE_BUILD_TYPE=RelWithDebInfo \
      -DLLDB_PATH_TO_LLVM_BUILD=%{_prefix} \
      -DLLDB_PATH_TO_CLANG_BUILD=%{_prefix} \
      -DLLVM_DIR=%{_libdir}/cmake/llvm \
      -DLLVM_BUILD_LLVM_DYLIB=ON \
      -DLLDB_DISABLE_LIBEDIT:BOOL=ON \
      -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
      -DCMAKE_C_FLAGS=-pipe \
      -DCMAKE_CXX_FLAGS=-pipe

%{cmake_build}

%install
%{cmake_install}

# Remove bundled python-six files
rm -f %{buildroot}%{python3_sitelib}/six.*

%clean
rm -rf %{buildroot}/*

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/liblldb.so.*
%{_libdir}/liblldbIntelFeatures.so.*

%files devel
%defattr(-,root,root)
%{_libdir}/liblldb.so
%{_libdir}/liblldbIntelFeatures.so
%{_includedir}/*

%files -n python3-lldb
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Thu Feb 20 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 12.0.0-2
- Build instruction improvements to reduce resource consumption
* Mon Nov 21 2022 Shreenidhi Shedi <sshedi@vmware.com> 12.0.0-1
- Upgrade to v12.0.0
* Thu Dec 09 2021 Prashant S Chauhan <psinghchauha@vmware.com> 11.0.1-4
- Bump up to compile with python 3.10
* Mon Nov 29 2021 Shreenidhi Shedi <sshedi@vmware.com> 11.0.1-3
- Add lua to Requires
* Thu Nov 18 2021 Nitesh Kumar <kunitesh@vmware.com> 11.0.1-2
- Release bump up to use libxml2 2.9.12-1.
* Thu Feb 04 2021 Shreenidhi Shedi <sshedi@vmware.com> 11.0.1-1
- Upgrade to v11.0.1
* Mon Aug 24 2020 Gerrit Photon <photon-checkins@vmware.com> 10.0.1-1
- Automatic Version Bump
* Fri Jun 19 2020 Tapas Kundu <tkundu@vmware.com> 6.0.1-2
- Removed python2
* Thu Aug 09 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 6.0.1-1
- Update to version 6.0.1 to get it to build with gcc 7.3
- Make python2_sitelib macro global to fix build error.
* Mon Jul 10 2017 Chang Lee <changlee@vmware.com> 4.0.0-3
- Commented out %check due to no test existence.
* Wed Jul 5 2017 Divya Thaluru <dthaluru@vmware.com> 4.0.0-2
- Added python-lldb package
* Fri Apr 7 2017 Alexey Makhalov <amakhalov@vmware.com> 4.0.0-1
- Version update
* Wed Jan 11 2017 Xiaolin Li <xiaolinl@vmware.com>  3.9.1-1
- Initial build.
