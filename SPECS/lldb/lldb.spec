%global debug_package %{nil}

Summary:        A next generation, high-performance debugger.
Name:           lldb
Version:        15.0.7
Release:        6%{?dist}
URL:            http://lldb.llvm.org
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/llvm/llvm-project/releases/tag/%{name}-%{version}.src.tar.xz
%define sha512 %{name}=27f94fd87827d08959a572038c22fd558e1776f94e1678e900d6e28517ae6fe2d89cbc719d9c65cd2879fc6bd97d291f90c4b8e6fe283f02fdf210ed138c80fa

Source1: license.txt
%include %{SOURCE1}

BuildRequires: cmake
BuildRequires: llvm-devel = %{version}
BuildRequires: clang-devel = %{version}
BuildRequires: ncurses-devel
BuildRequires: swig
BuildRequires: zlib-devel
BuildRequires: libxml2-devel
BuildRequires: python3-devel
BuildRequires: lua-devel
BuildRequires: ninja-build

Requires: lua
Requires: llvm = %{version}
Requires: clang = %{version}
Requires: ncurses
Requires: zlib
Requires: libxml2

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
%autosetup -p1 -n %{name}-%{version}.src

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
  -DCMAKE_BUILD_TYPE=Release \
  -DLLDB_PATH_TO_LLVM_BUILD=%{_prefix} \
  -DLLDB_PATH_TO_CLANG_BUILD=%{_prefix} \
  -DLLVM_DIR=%{_libdir}/cmake/llvm \
  -DLLVM_BUILD_LLVM_DYLIB=ON \
  -DLLDB_DISABLE_LIBEDIT:BOOL=ON \
  -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
  -DLLDB_PYTHON_EXE_RELATIVE_PATH=%{python3} \
  -DLLVM_PARALLEL_LINK_JOBS=${link_jobs} \
  -DLLVM_PARALLEL_COMPILE_JOBS=${build_jobs}

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
* Thu Dec 12 2024 Ajay Kaher <ajay.kaher@broadcom.com> 15.0.7-6
- Release bump for SRP compliance
* Tue Jun 20 2023 Shreenidhi Shedi <sshedi@vmware.com> 15.0.7-5
- Bump version as a part of lua upgrade
* Thu Jun 01 2023 Nitesh Kumar <kunitesh@vmware.com> 15.0.7-4
- Bump version as a part of ncurses upgrade to v6.4
* Thu May 25 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 15.0.7-3
- Bump version as a part of libxml2 upgrade
* Fri Apr 14 2023 Shreenidhi Shedi <sshedi@vmware.com> 15.0.7-2
- Bump version as a part of zlib upgrade
* Sat Feb 18 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 15.0.7-1
- Upgrade to v15.0.7
* Thu Jan 12 2023 Him Kalyan Bordoloi <bordoloih@vmware.com> 15.0.6-2
- Bump up version no. as part of swig upgrade
* Fri Dec 16 2022 Shreenidhi Shedi <sshedi@vmware.com> 15.0.6-1
- Upgrade to v15.0.6
* Tue Dec 06 2022 Prashant S Chauhan <psinghchauha@vmware.com> 15.0.1-2
- Update release to compile with python 3.11
* Tue Sep 27 2022 Shreenidhi Shedi <sshedi@vmware.com> 15.0.1-1
- Upgrade to v15.0.1
* Tue Jul 19 2022 Shreenidhi Shedi <sshedi@vmware.com> 12.0.0-4
- Use cmake macros for build
* Mon Nov 29 2021 Shreenidhi Shedi <sshedi@vmware.com> 12.0.0-3
- Add lua to Requires
* Wed Nov 17 2021 Nitesh Kumar <kunitesh@vmware.com> 12.0.0-2
- Release bump up to use libxml2 2.9.12-1.
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 12.0.0-1
- Automatic Version Bump
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
