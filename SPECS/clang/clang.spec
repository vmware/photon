%global debug_package %{nil}

Summary:        C, C++, Objective C and Objective C++ front-end for the LLVM compiler.
Name:           clang
Version:        15.0.7
Release:        5%{?dist}
URL:            http://clang.llvm.org
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/llvm/llvm-project/releases/tag/%{name}-%{version}.src.tar.xz
%define sha512 %{name}=9fd2736a9f5993ddbb5b3c507fe497234a6def64f6f418f379d1ca56c9c361ad1ae9a5445ab938230fbc1671ec00b4f802a412b048569023863c20dc6bb46a1f

Source1: license.txt
%include %{SOURCE1}

BuildRequires: cmake
BuildRequires: llvm-devel = %{version}
BuildRequires: ncurses-devel
BuildRequires: zlib-devel
BuildRequires: libxml2-devel
BuildRequires: python3-devel
BuildRequires: ninja-build

Requires: libstdc++-devel
Requires: ncurses
Requires: llvm
Requires: zlib
Requires: libxml2
Requires: python3

%description
The goal of the Clang project is to create a new C based language front-end:
C, C++, Objective C/C++, OpenCL C and others for the LLVM compiler. You can get and build the source today.

%package        devel
Summary:        Development headers for clang
Requires:       %{name} = %{version}-%{release}
Requires:       ncurses-devel
%description    devel
The clang-devel package contains libraries, header files and documentation for developing applications that use clang.

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

%{cmake} -G Ninja \
  -DCMAKE_INSTALL_PREFIX=%{_usr} \
  -DCMAKE_BUILD_TYPE=Release \
  -DLLVM_MAIN_INCLUDE_DIR=%{_includedir} \
  -DLLVM_PARALLEL_LINK_JOBS=${link_jobs} \
  -DLLVM_PARALLEL_COMPILE_JOBS=${build_jobs} \
  -DBUILD_SHARED_LIBS=OFF \
  -Wno-dev

# Build libclang-cpp.so separately to avoid OOM errors.
# This is to fix occasional OOM errors
%{cmake_build} --target libclang-cpp.so

%{cmake_build}

%install
%{cmake_install}

mkdir -p %{buildroot}%{python3_sitelib}
mv %{buildroot}%{_libdir}/{libear,libscanbuild} %{buildroot}%{python3_sitelib}

%if 0%{?with_check}
%check
%make_build -C %{__cmake_builddir} clang-check
%endif

%clean
rm -rf %{buildroot}/*

%post   -p /sbin/ldconfig
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
%{python3_sitelib}/libear
%{python3_sitelib}/libscanbuild

%changelog
* Wed Dec 11 2024 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 15.0.7-5
- Release bump for SRP compliance
* Thu Jun 01 2023 Nitesh Kumar <kunitesh@vmware.com> 15.0.7-4
- Bump version as a part of ncurses upgrade to v6.4
* Thu May 25 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 15.0.7-3
- Bump version as a part of libxml2 upgrade
* Fri Apr 14 2023 Shreenidhi Shedi <sshedi@vmware.com> 15.0.7-2
- Bump version as a part of zlib upgrade
* Sat Feb 18 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 15.0.7-1
- Upgrade to v15.0.7
* Fri Dec 02 2022 Shreenidhi Shedi <sshedi@vmware.com> 15.0.6-1
- Upgrade to v15.0.6
* Mon Oct 17 2022 Prashant S Chauhan <psinghchauha@vmware.com> 15.0.1-2
- Update release to compile with python 3.11
* Tue Sep 27 2022 Shreenidhi Shedi <sshedi@vmware.com> 15.0.1-1
- Upgrade to v15.0.1
* Thu Jul 14 2022 Shreenidhi Shedi <sshedi@vmware.com> 12.0.0-4
- Further fixes to cmake macro usages
* Mon Jun 20 2022 Shreenidhi Shedi <sshedi@vmware.com> 12.0.0-3
- Use cmake macros for build and install
* Wed Nov 17 2021 Nitesh Kumar <kunitesh@vmware.com> 12.0.0-2
- Release bump up to use libxml2 2.9.12-1.
* Mon Apr 12 2021 Gerrit Photon <photon-checkins@vmware.com> 12.0.0-1
- Automatic Version Bump
* Tue Mar 16 2021 Michael Paquier <mpaquier@vmware.com> 11.0.1-2
- Addition of required dependency to ncurses-devel for devel package.
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
