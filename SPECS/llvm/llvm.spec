Summary:        A collection of modular and reusable compiler and toolchain technologies.
Name:           llvm
Version:        4.0.0
Release:        2%{?dist}
License:        NCSA
URL:            http://lldb.llvm.org
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://releases.llvm.org/%{version}/%{name}-%{version}.src.tar.xz
%define sha1    llvm=aee4524e2407f9fe5afc6f70c753180b907011d0
BuildRequires:  cmake
BuildRequires:  libxml2-devel
BuildRequires:  libffi-devel
Requires:       libxml2

%description
The LLVM Project is a collection of modular and reusable compiler and toolchain technologies. Despite its name, LLVM has little to do with traditional virtual machines, though it does provide helpful libraries that can be used to build them. The name "LLVM" itself is not an acronym; it is the full name of the project.

%package devel
Summary:        Development headers for llvm
Requires:       %{name} = %{version}-%{release}

%description devel
The llvm-devel package contains libraries, header files and documentation
for developing applications that use llvm.

%prep
%setup -q -n %{name}-%{version}.src

%build
mkdir -p build
cd build
cmake -DCMAKE_INSTALL_PREFIX=/usr           \
      -DLLVM_ENABLE_FFI=ON                  \
      -DCMAKE_BUILD_TYPE=Release            \
      -DLLVM_BUILD_LLVM_DYLIB=ON            \
      -DLLVM_TARGETS_TO_BUILD="host;AMDGPU" \
      -Wno-dev ..

make %{?_smp_mflags}
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
cd build
make DESTDIR=%{buildroot} install

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%check
make %{?_smp_mflags} check

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so
%{_libdir}/*.so.*

%files devel
%{_libdir}/*.a
%{_libdir}/cmake/*
%{_includedir}/*

%changelog
*   Fri Apr 14 2017 Alexey Makhalov <amakhalov@vmware.com> 4.0.0-2
-   BuildRequires libffi-devel
*   Fri Apr 7 2017 Alexey Makhalov <amakhalov@vmware.com> 4.0.0-1
-   Version update
*   Wed Jan 11 2017 Xiaolin Li <xiaolinl@vmware.com>  3.9.1-1
-   Initial build.
