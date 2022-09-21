%global debug_package %{nil}

Name:            bcc
Summary:         BPF Compiler Collection (BCC)
Version:         0.16.0
Release:         3%{?dist}
License:         ASL 2.0
Vendor:          VMware, Inc.
Distribution:    Photon
Group:           Development/Languages
URL:             https://github.com/iovisor/bcc

Source0: https://github.com/iovisor/bcc/archive/%{name}-%{version}.tar.gz
%define sha512 %{name}=50d09d6d02335a63d7c01c22f16a706584f231ee16973a80df5b640c31b8e25775da13a2bdff9e57c04c7f6181bb8c46cf3bd11c1e59741234024da71c7f6cdb

Source1: https://github.com/iovisor/bcc/releases/download/v%{version}/bcc-src-with-submodule.tar.gz
%define sha512 bcc-src-with-submodule=ec2eec46ef45e96a269fe252de85734e12182bac839c7ee958852c6e7f4935b86f83536d6fd127933549f521d9b7af440544207818d5bd72a94567d41c6f3b75

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
BuildRequires:   python3-macros

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
# Using autosetup is not feasible
%setup -q -n %{name}-%{version}
# Using autosetup is not feasible
%setup -D -c -T -a 1 -n %{name}-%{version}/
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
%defattr(-,root,root)
%doc README.md
%license LICENSE.txt
%{_libdir}/lib%{name}.so.*
%{_libdir}/libbcc_bpf.so.*

%files devel
%defattr(-,root,root)
%{_libdir}/lib%{name}.so
%{_libdir}/libbcc_bpf.so
%{_libdir}/*.a
%{_libdir}/pkgconfig/lib%{name}.pc
%{_includedir}/%{name}/

%files -n python3-bcc
%defattr(-,root,root)
%{python3_sitelib}/%{name}*

%files examples
%defattr(-,root,root)
%{_datadir}/%{name}/examples/*

%files tools
%defattr(-,root,root)
%{_datadir}/%{name}/introspection/*
%{_datadir}/%{name}/tools/*
%{_datadir}/%{name}/man/*

%changelog
* Wed Sep 21 2022 Shreenidhi Shedi <sshedi@vmware.com> 0.16.0-3
- Use cmake macros
* Thu Dec 09 2021 Prashant S Chauhan <psinghchauha@vmware.com> 0.16.0-2
- Bump up to compile with python 3.10
* Wed Jul 22 2020 Gerrit Photon <photon-checkins@vmware.com> 0.16.0-1
- Automatic Version Bump
* Wed Jun 26 2019  Keerthana K <keerthanak@vmware.com> 0.10.0-1
- Initial bcc package for PhotonOS.
