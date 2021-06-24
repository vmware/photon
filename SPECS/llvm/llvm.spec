Summary:        A collection of modular and reusable compiler and toolchain technologies.
Name:           llvm
Version:        12.0.0
Release:        1%{?dist}
License:        NCSA
URL:            http://lldb.llvm.org
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://releases.llvm.org/%{version}/%{name}-%{version}.src.tar.xz
%define sha1    llvm=dbc1cf6aa2dbdeccd7ad26c9215b56963a5686d3
BuildRequires:  cmake
BuildRequires:  libxml2-devel
BuildRequires:  libffi-devel
BuildRequires:  python3
Requires:       libxml2

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
%setup -q -n %{name}-%{version}.src

%build
mkdir -p build
cd build
cmake -DCMAKE_INSTALL_PREFIX=/usr               \
      -DLLVM_ENABLE_FFI:BOOL=ON                 \
      -DCMAKE_BUILD_TYPE=Release                \
      -DLLVM_BUILD_LLVM_DYLIB:BOOL=ON           \
      -DLLVM_TARGETS_TO_BUILD="host;AMDGPU;BPF" \
      -DLLVM_INCLUDE_GO_TESTS=No                \
      -DLLVM_ENABLE_RTTI:BOOL=ON                \
      -Wno-dev ..
make %{?_smp_mflags}
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
cd build
make DESTDIR=%{buildroot} install

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%check
# deactivate security hardening for tests
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

%files -n libllvm
%defattr(-,root,root)
%{_libdir}/libLLVM*.so

%changelog
*   Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 12.0.0-1
-   Automatic Version Bump
*   Thu Feb 04 2021 Shreenidhi Shedi <sshedi@vmware.com> 11.0.1-1
-   Upgrade to v11.0.1
*   Tue Sep 22 2020 Harinadh D <hdommaraju@vmware.com> 10.0.1-1
-   add libLLVM.so to libllvm
*   Thu Sep 10 2020 Susant Sahani Sahani <ssahani@vmware.com> 10.0.1-2
-   Enable LLVM_ENABLE_RTTI
*   Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 10.0.1-1
-   Automatic Version Bump
*   Tue Jun 23 2020 Tapas Kundu <tkundu@vmware.com> 6.0.1-4
-   Build with python3
-   Mass removal python2
*   Wed Jun 26 2019 Keerthana K <keerthanak@vmware.com> 6.0.1-3
-   Enable target BPF
*   Tue Jan 08 2019 Alexey Makhalov <amakhalov@vmware.com> 6.0.1-2
-   Added BuildRequires python2
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
