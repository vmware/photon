%global debug_package %{nil}

Name:            bcc
Summary:         BPF Compiler Collection (BCC)
Version:         0.25.0
Release:         2%{?dist}
License:         ASL 2.0
Vendor:          VMware, Inc.
Distribution:    Photon
Group:           Development/Languages
URL:             https://github.com/iovisor/bcc

Source0: https://github.com/iovisor/bcc/archive/%{name}-%{version}.tar.gz
%define sha512 %{name}=9f71f6c21d1f66054985562168d5848352f5029383e9c65c907a6f044258bc23df842cc65db20bfaaf33789e69c9b8e7b606a32dc882cbdf093b71768c8b521d
Source1: https://github.com/iovisor/bcc/releases/download/v%{version}/bcc-src-with-submodule-%{version}.tar.gz
%define sha512 %{name}-src-with-submodule=842e0957dd3a7cbb60e8aba497ae0841bfa564306ba27effca5348466dae6735557dc0a871d63a2519e3bba105632bcb279af7cfacf378dff9de2638484dac63

Patch0:          CVE-2024-2314-1.patch
Patch1:          CVE-2024-2314-2.patch

BuildRequires:   cmake
BuildRequires:   build-essential
BuildRequires:   libstdc++
BuildRequires:   elfutils-libelf
BuildRequires:   elfutils-libelf-devel-static
BuildRequires:   python3-devel
BuildRequires:   llvm-devel
BuildRequires:   clang-devel
BuildRequires:   pkg-config
BuildRequires:   ncurses-devel
BuildRequires:   curl-devel

Requires: curl
Requires: ncurses
Requires: libstdc++
Requires: zlib
Requires: elfutils
Requires: elfutils-libelf
Requires: glibc

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
%setup -q -D -c -T -a1 -n %{name}-%{version}
cp -rf %{name}/* .
rm -r %{name}

%patch0 -p1
%patch1 -p1

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
find %{buildroot}%{_datadir}/%{name}/{tools,examples} -type f -exec \
    sed -i -e '1 s|^#!/usr/bin/python$|#!'%{python3}'|' \
           -e '1 s|^#!/usr/bin/env python$|#!'%{python3}'|' {} \;

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_libdir}/lib%{name}.so.*
%{_libdir}/lib%{name}_bpf.so.*

%files devel
%defattr(-,root,root)
%{_libdir}/lib%{name}.so
%{_libdir}/lib%{name}_bpf.so
%{_libdir}/*.a
%{_libdir}/pkgconfig/lib%{name}.pc
%{_includedir}/%{name}/

%files -n python3-%{name}
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
* Mon Dec 23 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 0.25.0-2
- CVE-2024-2314 fix
* Tue Nov 22 2022 Shreenidhi Shedi <sshedi@vmware.com> 0.25.0-1
- Upgrade to v0.25.0
* Wed Sep 21 2022 Shreenidhi Shedi <sshedi@vmware.com> 0.16.0-3
- Use cmake macros
* Thu Dec 09 2021 Prashant S Chauhan <psinghchauha@vmware.com> 0.16.0-2
- Bump up to compile with python 3.10
* Wed Jul 22 2020 Gerrit Photon <photon-checkins@vmware.com> 0.16.0-1
- Automatic Version Bump
* Wed Jun 26 2019  Keerthana K <keerthanak@vmware.com> 0.10.0-1
- Initial bcc package for PhotonOS.
