%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
Summary:        A next generation, high-performance debugger.
Name:           lldb
Version:        3.9.1
Release:        3%{?dist}
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
BuildRequires:  ncurses-devel >= 6.0-3
BuildRequires:  swig
BuildRequires:  zlib-devel
BuildRequires:  libxml2-devel
Requires:       llvm = %{version}
Requires:       clang = %{version}
Requires:       ncurses >= 6.0-3
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

%package -n python-lldb
Summary:        Python module for lldb
Requires:       %{name} = %{version}-%{release}
BuildRequires:  python2-devel
Requires:       python-six

%description -n python-lldb
The package contains the LLDB Python module.

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

#Remove bundled python-six files
rm -f %{buildroot}%{python2_sitelib}/six.*

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%check
make %{?_smp_mflags} check

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/liblldb.so.*

%files devel
%defattr(-,root,root)
%{_libdir}/liblldb.so
%{_libdir}/*.a
%{_includedir}/*

%files -n python-lldb
%defattr(-,root,root)
%{python2_sitelib}/*

%changelog
*   Wed Jul 5 2017 Divya Thaluru <dthaluru@vmware.com> 3.9.1-3
-   Added python-lldb package
-   Removed built-in python-six module and added dependency on python-six
*   Mon Apr 3 2017 Alexey Makhalov <amakhalov@vmware.com> 3.9.1-2
-   Use specified version of ncurses wich has long chtype and mmask_t
    (see ncurses changelog)
*   Wed Jan 11 2017 Xiaolin Li <xiaolinl@vmware.com>  3.9.1-1
-   Initial build.
