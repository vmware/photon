Summary:        A collection of modular and reusable compiler and toolchain technologies.
Name:           llvm
Version:        11.0.1
Release:        5%{?dist}
License:        NCSA
URL:            http://lldb.llvm.org
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://releases.llvm.org/%{version}/%{name}-%{version}.src.tar.xz
%define sha512 llvm=b42c67ef88e09dd94171f85cdf49a421a15cfc82ff715c7ce6de22f98cefbe6c7cdf6bf4af7ca017d56ecf6aa3e36df3d823a78cf2dd5312de4301b54b43dbe8

BuildRequires:  cmake
BuildRequires:  libxml2-devel
BuildRequires:  libffi-devel
BuildRequires:  python3-devel
BuildRequires:  ninja-build

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
Group:          System Environment/Libraries
%description -n libllvm
The libllvm package contains shared libraries for llvm

%prep
%autosetup -n %{name}-%{version}.src -p1

%build
%cmake -G Ninja \
      -DCMAKE_INSTALL_PREFIX=%{_usr} \
      -DBUILD_SHARED_LIBS:BOOL=OFF \
      -DLLVM_PARALLEL_LINK_JOBS=1 \
      -DLLVM_ENABLE_FFI:BOOL=ON \
      -DCMAKE_BUILD_TYPE=RelWithDebInfo \
      -DLLVM_BUILD_LLVM_DYLIB:BOOL=ON \
      -DLLVM_TARGETS_TO_BUILD="host;AMDGPU;BPF" \
      -DLLVM_INCLUDE_GO_TESTS=No \
      -DLLVM_ENABLE_RTTI:BOOL=ON \
      -Wno-dev

%cmake_build

%install
%cmake_install

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%if 0%{?with_check}
%check
# deactivate security hardening for tests
rm -f $(dirname $(gcc -print-libgcc-file-name))/../specs
cd build
make %{?_smp_mflags} check-llvm
%endif

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so
%{_libdir}/*.so.*
%exclude %{_libdir}/libLLVM-11.0.1.so
%exclude %{_libdir}/libLLVM-11.so
%exclude %{_libdir}/libLLVM.so
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
* Thu Dec 09 2021 Prashant S Chauhan <psinghchauha@vmware.com> 11.0.1-5
- Bump up to compile with python 3.10
* Thu Nov 18 2021 Nitesh Kumar <kunitesh@vmware.com> 11.0.1-4
- Release bump up to use libxml2 2.9.12-1.
* Mon Oct 25 2021 Harinadh D<hdommaraju@vmware.com> 11.0.1-3
- remove llvm dependency for libllvm
- remove libLLVM.so files from llvm package
- add libllvm as requires for llvm
* Wed Sep 08 2021 Nitesh Kumar <kunitesh@vmware.com> 11.0.1-2
- Replacement of ITS suggested words.
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
