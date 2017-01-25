Summary:        A next generation, high-performance debugger.
Name:           lldb
Version:        3.9.1
Release:        1%{?dist}
License:        NCSA
URL:            http://lldb.llvm.org
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://releases.llvm.org/%{version}/%{name}-%{version}.src.tar.xz
%define sha1    lldb=f6da59c9ed570c4c7091c25f0abe59aba0e29de3
Patch0:         Replace-uses-of-MIUtilParse-CRegexParser-with-llvm-Regex.patch
Patch1:         Remove-MIUtilParse.patch
BuildRequires:  cmake
BuildRequires:  llvm-devel = %{version}
BuildRequires:  clang-devel = %{version}
BuildRequires:  ncurses-devel
BuildRequires:  swig
BuildRequires:  zlib-devel
BuildRequires:  libxml2-devel
Requires:       llvm = %{version}
Requires:       clang = %{version}
Requires:       ncurses
Requires:       zlib
Requires:       libxml2

%description
LLDB is a next generation, high-performance debugger. It is built as a set of reusable components which highly leverage existing libraries in the larger LLVM Project, such as the Clang expression parser and LLVM disassembler.

%package devel
Summary:        Development headers for lldb
Requires:       %{name} = %{version}-%{release}

%description devel
The lldb-devel package contains libraries, header files and documentation
for developing applications that use lldb.

%prep
%setup -q -n %{name}-%{version}.src
%patch0
%patch1

%build
mkdir -p build
cd build
cmake -DCMAKE_INSTALL_PREFIX=/usr           \
      -DCMAKE_BUILD_TYPE=Release            \
      -DLLDB_PATH_TO_LLVM_BUILD=%{_prefix}  \
      -DLLDB_PATH_TO_CLANG_BUILD=%{_prefix} \
      -DLLVM_DIR=/usr/lib/cmake/llvm        \
      -DLLVM_BUILD_LLVM_DYLIB=ON ..         \
      -DLLDB_DISABLE_LIBEDIT:BOOL=ON

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
%{_libdir}/python2.7/*
%{_libdir}/liblldb.so.*

%files devel
%defattr(-,root,root)
%{_libdir}/liblldb.so
%{_libdir}/*.a
%{_includedir}/*

%changelog
*   Wed Jan 11 2017 Xiaolin Li <xiaolinl@vmware.com>  3.9.1-1
-   Initial build.
