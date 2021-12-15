Summary:        A collection of modular and reusable compiler and toolchain technologies.
Name:           llvm
Version:        10.0.1
Release:        2%{?dist}
License:        NCSA
URL:            http://lldb.llvm.org
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://releases.llvm.org/%{version}/%{name}-%{version}.src.tar.xz
%define sha1    llvm=25d07260f3b7bf4f647e115c4a663fdeda130fbd
BuildRequires:  cmake
BuildRequires:  libxml2-devel
BuildRequires:  libffi-devel
BuildRequires:  python2
Requires:       libxml2

%description
The LLVM Project is a collection of modular and reusable compiler and toolchain technologies.
Despite its name, LLVM has little to do with traditional virtual machines, though it does provide helpful libraries that can be used to build them.
The name "LLVM" itself is not an acronym; it is the full name of the project.

%package        devel
Summary:        Development headers for llvm
Requires:       %{name} = %{version}-%{release}
%description    devel
The llvm-devel package contains libraries, header files and documentation
for developing applications that use llvm.

%prep
%autosetup -n %{name}-%{version}.src -p1

%build
mkdir -p build
cd build
cmake -DCMAKE_INSTALL_PREFIX=/usr           \
      -DLLVM_ENABLE_FFI=BOOL=ON                  \
      -DCMAKE_BUILD_TYPE=Release            \
      -DLLVM_BUILD_LLVM_DYLIB=BOOL=ON            \
      -DLLVM_TARGETS_TO_BUILD="host;AMDGPU;BPF" \
      -DLLVM_INCLUDE_GO_TESTS=No            \
      -DLLVM_ENABLE_RTTI:BOOL=ON            \
      -Wno-dev ..
make %{?_smp_mflags}
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
cd build
make DESTDIR=%{buildroot} install %{?_smp_mflags}

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%check
# disable security hardening for tests
rm -f $(dirname $(gcc -print-libgcc-file-name))/../specs
cd build
make %{?_smp_mflags} check-llvm

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so
%{_libdir}/*.so.*
%dir %{_datadir}/opt-viewer
%{_datadir}/opt-viewer/opt-diff.py
%{_datadir}/opt-viewer/opt-stats.py
%{_datadir}/opt-viewer/opt-viewer.py
%{_datadir}/opt-viewer/optpmap.py
%{_datadir}/opt-viewer/optrecord.py
%{_datadir}/opt-viewer/style.css

%files devel
%{_libdir}/*.a
%{_libdir}/cmake/*
%{_includedir}/*

%changelog
*   Thu Nov 18 2021 Nitesh Kumar <kunitesh@vmware.com> 10.0.1-2
-   Version bump up to use libxml2 2.9.11-4.
*   Wed Nov 11 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 10.0.1-1
-   Version Bump to 10.0.1
-   Enable LLVM_ENABLE_RTTI
*   Mon Jan 06 2020 Prashant S Chauhan <psinghchauha@vmware.com> 6.0.1-3
-   Added python2 dependency
*   Wed Jun 26 2019 Keerthana K <keerthanak@vmware.com> 6.0.1-2
-   Enable target BPF
*   Thu Aug 09 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 6.0.1-1
-   Update to version 6.0.1 to get it to build with gcc 7.3
*   Thu Aug 10 2017 Alexey Makhalov <amakhalov@vmware.com> 4.0.0-3
-   Make check fix
*   Fri Apr 14 2017 Alexey Makhalov <amakhalov@vmware.com> 4.0.0-2
-   BuildRequires libffi-devel
*   Fri Apr 7 2017 Alexey Makhalov <amakhalov@vmware.com> 4.0.0-1
-   Version update
*   Wed Jan 11 2017 Xiaolin Li <xiaolinl@vmware.com>  3.9.1-1
-   Initial build.
