Summary:        C, C++, Objective C and Objective C++ front-end for the LLVM compiler.
Name:           clang
Version:        10.0.1
Release:        3%{?dist}
License:        NCSA
URL:            http://clang.llvm.org
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/llvm/llvm-project/releases/download/llvmorg-%{version}/%{name}-%{version}.src.tar.xz
%define sha1    clang=0e61e92b22a620fe7f833fa8b2a56f2db96f7335
BuildRequires:  cmake
BuildRequires:  llvm-devel = %{version}
BuildRequires:  ncurses-devel
BuildRequires:  zlib-devel
BuildRequires:  libxml2-devel
BuildRequires:  python3-devel
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
mkdir -p build
cd build
cmake -DCMAKE_INSTALL_PREFIX=/usr               \
      -DCMAKE_BUILD_TYPE=Release                \
      -DLLVM_MAIN_INCLUDE_DIR=/usr/include \
      -Wno-dev ..
make %{?_smp_mflags}

%install
[ %{buildroot} != "/" ] && rm -rf %{buildroot}/*
cd build
make DESTDIR=%{buildroot} install %{?_smp_mflags}

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%check
cd build
make clang-check %{?_smp_mflags}

%clean
rm -rf %{buildroot}/*

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
*   Thu Nov 18 2021 Nitesh Kumar <kunitesh@vmware.com> 10.0.1-3
-   Version bump up to use libxml2 2.9.11-4.
*   Tue Jul 27 2021 Tapas Kundu <tkundu@vmware.com> 10.0.1-2
-   Build with python3
*   Wed Nov 11 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 10.0.1-1
-   Version Bump to 10.0.1
*   Thu Aug 09 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 6.0.1-1
-   Update to version 6.0.1 to get it to build with gcc 7.3
*   Wed Jun 28 2017 Chang Lee <changlee@vmware.com> 4.0.0-2
-   Updated %check
*   Fri Apr 7 2017 Alexey Makhalov <amakhalov@vmware.com> 4.0.0-1
-   Version update
*   Wed Jan 11 2017 Xiaolin Li <xiaolinl@vmware.com>  3.9.1-1
-   Initial build.
