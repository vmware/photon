%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

%global debug_package %{nil}
%global __python3 \/usr\/bin\/python3

Name:            bcc
Summary:         BPF Compiler Collection (BCC)
Version:         0.16.0
Release:         1%{?dist}
License:         ASL 2.0
Vendor:          VMware, Inc.
Distribution:    Photon
Group:           Development/Languages
URL:             https://github.com/iovisor/bcc
Source0:         https://github.com/iovisor/bcc/archive/%{name}-%{version}.tar.gz
%define sha1     bcc=26406a9a562756a8fcd2442e543486a77f2949c3
Source1:         https://github.com/iovisor/bcc/releases/download/v%{version}/bcc-src-with-submodule.tar.gz
%define sha1     bcc-src-with-submodule=ae5102ef4109f8af03c7282c1f9f2c3201c3a400
BuildRequires:   bison
BuildRequires:   cmake >= 2.8.7
BuildRequires:   flex
BuildRequires:   make
BuildRequires:   gcc
BuildRequires:   libstdc++
BuildRequires:   elfutils-libelf
BuildRequires:   elfutils-libelf-devel-static
BuildRequires:   python3-devel
BuildRequires:   llvm-devel
BuildRequires:   clang-devel
BuildRequires:   pkg-config
BuildRequires:   ncurses-devel

%description
BCC is a toolkit for creating efficient kernel tracing and manipulation programs,
and includes several useful tools and examples. It makes use of
extended BPF (Berkeley Packet Filters), formally known as eBPF,
a new feature that was first added to Linux 3.15.
Much of what BCC uses requires Linux 4.1 and above.

%package         devel
Summary:         Shared Library for BPF Compiler Collection (BCC)
Requires:        %{name} = %{version}-%{release}
%description     devel
%{name}-devel contains shared libraries and header files for
developing application.

%package -n      python3-%{name}
Summary:         Python3 bindings for BPF Compiler Collection (BCC)
Requires:        %{name} = %{version}-%{release}
%{?python_provide:%python_provide python3-bcc}
%description -n  python3-%{name}
Python bindings for BPF Compiler Collection (BCC)

%package         examples
Summary:         Examples for BPF Compiler Collection (BCC)
Requires:        python3-%{name} = %{version}-%{release}
%description     examples
Examples for BPF Compiler Collection (BCC)

%package         tools
Summary:         Command line tools for BPF Compiler Collection (BCC)
Requires:        python3-%{name} = %{version}-%{release}
%description     tools
Command line tools for BPF Compiler Collection (BCC)

%prep
%setup -q -n %{name}-%{version}
%setup -D -c -T -a 1 -n %{name}-%{version}/
cp -rf bcc/* .
rm -r bcc

%build
mkdir build
pushd build
cmake .. -DREVISION_LAST=%{version} -DREVISION=%{version} \
      -DCMAKE_INSTALL_PREFIX=/usr \
      -DPYTHON_CMD=python3 \
      %{?with_llvm_shared:-DENABLE_LLVM_SHARED=1}
make %{?_smp_mflags}
popd

%install
pushd build
make install/strip DESTDIR=%{buildroot}
# mangle shebangs
find %{buildroot}/usr/share/bcc/{tools,examples} -type f -exec \
    sed -i -e '1 s|^#!/usr/bin/python$|#!'%{__python3}'|' \
           -e '1 s|^#!/usr/bin/env python$|#!'%{__python3}'|' {} \;

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%doc README.md
%license LICENSE.txt
%{_lib64dir}/lib%{name}.so.*
%{_lib64dir}/libbcc_bpf.so.*

%files devel
%{_lib64dir}/lib%{name}.so
%{_lib64dir}/libbcc_bpf.so
%{_lib64dir}/*.a
%{_lib64dir}/pkgconfig/lib%{name}.pc
%{_includedir}/%{name}/

%files -n python3-bcc
%{python3_sitelib}/%{name}*

%files examples
%{_datadir}/%{name}/examples/*

%files tools
%{_datadir}/%{name}/introspection/*
%{_datadir}/%{name}/tools/*
%{_datadir}/%{name}/man/*

%changelog
*   Wed Nov 11 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 0.16.0-1
-   Version Bump to 0.16.0
*   Wed Jun 26 2019  Keerthana K <keerthanak@vmware.com> 0.10.0-1
-   Initial bcc package for PhotonOS.
