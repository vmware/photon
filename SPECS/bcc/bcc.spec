%global debug_package %{nil}

Name:            bcc
Summary:         BPF Compiler Collection (BCC)
Version:         0.19.0
Release:         2%{?dist}
License:         ASL 2.0
Vendor:          VMware, Inc.
Distribution:    Photon
Group:           Development/Languages
URL:             https://github.com/iovisor/bcc

Source0:        https://github.com/iovisor/bcc/archive/%{name}-%{version}.tar.gz
%define sha512  %{name}=b6180462a45c768f219e026d8a4b43424b7cad4e07db8101725bd2bc31ee4de117774c0ad8d157502c97c1187057b45c7a491e7198ac2c59e6d56e58797f4df3

#https://github.com/iovisor/bcc/releases/download/v%{version}/bcc-src-with-submodule.tar.gz
Source1:        bcc-src-with-submodule-%{version}.tar.gz
%define sha512  bcc-src-with-submodule=66a1ac0199e3e0405a795d0e4f0d7895a9df38260ac0d77e857a69c81457ff9976e1eb285fe49818a8e21461abd748c66837ce49cc9d3e0952278db92c611fb5

BuildRequires:   bison
BuildRequires:   cmake
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

%package -n      python3-bcc
Summary:         Python3 bindings for BPF Compiler Collection (BCC)
Requires:        %{name} = %{version}-%{release}

%description -n  python3-bcc
Python bindings for BPF Compiler Collection (BCC)

%package         examples
Summary:         Examples for BPF Compiler Collection (BCC)
Requires:        python3-bcc = %{version}-%{release}

%description     examples
Examples for BPF Compiler Collection (BCC)

%package         tools
Summary:         Command line tools for BPF Compiler Collection (BCC)
Requires:        python3-%{name} = %{version}-%{release}

%description     tools
Command line tools for BPF Compiler Collection (BCC)

%prep
# Using autosetup is not feasible
%setup -q -n %{name}-%{version}
# Using autosetup is not feasible
%setup -D -c -T -a 1 -n %{name}-%{version}
cp -rf bcc/* .
rm -r bcc

%build
%cmake -DREVISION_LAST=%{version} \
       -DREVISION=%{version} \
       -DPYTHON_CMD=%{python3} \
       %{?with_llvm_shared:-DENABLE_LLVM_SHARED=1} \
       -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
       -DCMAKE_BUILD_TYPE=Debug

%cmake_build

%install
%cmake_install
# mangle shebangs
find %{buildroot}%{_datadir}/bcc/{tools,examples} -type f -exec \
    sed -i -e '1 s|^#!/usr/bin/python$|#!'%{python3}'|' \
           -e '1 s|^#!/usr/bin/env python$|#!'%{python3}'|' {} \;

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%doc README.md
%license LICENSE.txt
%{_libdir}/lib%{name}.so.*
%{_libdir}/libbcc_bpf.so.*

%files devel
%{_libdir}/lib%{name}.so
%{_libdir}/libbcc_bpf.so
%{_libdir}/*.a
%{_libdir}/pkgconfig/lib%{name}.pc
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
* Mon Jun 20 2022 Shreenidhi Shedi <sshedi@vmware.com> 0.19.0-2
- Use cmake macros for build and install
* Mon Apr 12 2021 Gerrit Photon <photon-checkins@vmware.com> 0.19.0-1
- Automatic Version Bump
* Wed Jul 22 2020 Gerrit Photon <photon-checkins@vmware.com> 0.16.0-1
- Automatic Version Bump
* Wed Jun 26 2019  Keerthana K <keerthanak@vmware.com> 0.10.0-1
- Initial bcc package for PhotonOS.
