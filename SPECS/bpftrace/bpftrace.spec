Name:           bpftrace
Version:        0.11.4
Release:        1%{?dist}
Summary:        High-level tracing language for Linux eBPF
License:        ASL 2.0
Vendor:         VMware, Inc.
Distribution:   Photon
Group:          System Environment/Security
URL:            https://github.com/iovisor/bpftrace

Source0: https://github.com/iovisor/bpftrace/archive/%{name}-%{version}.tar.gz
%define sha512 %{name}=611a7e61dbd1f4cc52b7e51a1a143296ff7b2df115b3a28034c674d8eefb5d482cac551ab82d6b7cc2f6fc0668b07d2d9e283dff371fd9a3f649c80113fdca82

BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  cmake
BuildRequires:  elfutils-libelf-devel
BuildRequires:  zlib-devel
BuildRequires:  llvm-devel
BuildRequires:  clang-devel
BuildRequires:  bcc-devel >= 0.11.0-2
BuildRequires:  libbpf-devel
BuildRequires:  binutils-devel

Requires:       bcc
Requires:       bcc-tools
Requires:       clang
Requires:       llvm
Requires:       zlib
Requires:       libbpf

%description
BPFtrace is a high-level tracing language for Linux enhanced Berkeley Packet
Filter (eBPF) available in recent Linux kernels (4.x). BPFtrace uses LLVM as a
backend to compile scripts to BPF-bytecode and makes use of BCC for
interacting with the Linux BPF system, as well as existing Linux tracing
capabilities: kernel dynamic tracing (kprobes), user-level dynamic tracing
(uprobes), and tracepoints. The BPFtrace language is inspired by awk and C,
and predecessor tracers such as DTrace and SystemTap

%prep
%autosetup -p1

%build
%cmake . \
        -DCMAKE_BUILD_TYPE=RelWithDebInfo \
        -DBUILD_TESTING:BOOL=OFF \
        -DBUILD_SHARED_LIBS:BOOL=OFF \
        -DENABLE_TESTS:BOOL=OFF \
        -DBUILD_DEPS=OFF \
        -DCMAKE_INSTALL_LIBDIR=%{_libdir}

%cmake_build

%install
%cmake_install

find %{buildroot}%{_datadir}/%{name}/tools -type f -exec \
  sed -i -e '1s=^#!/usr/bin/env %{name}\([0-9.]\+\)\?$=#!%{_bindir}/%{name}=' {} \;

%files
%defattr(-,root,root)
%doc README.md CONTRIBUTING-TOOLS.md
%doc docs/reference_guide.md docs/tutorial_one_liners.md
%license LICENSE
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/tools
%dir %{_datadir}/%{name}/tools/doc
%{_bindir}/%{name}
%{_mandir}/man8/*
%attr(0755,-,-) %{_datadir}/%{name}/tools/*.bt
%{_datadir}/%{name}/tools/doc/*.txt

%changelog
* Mon Feb 08 2021 Shreenidhi Shedi <sshedi@vmware.com> 0.11.4-1
- Upgrade to v0.11.4
* Sat Oct 17 2020 Shreenidhi Shedi <sshedi@vmware.com> 0.11.1-2
- Fix aarch64 build errors
* Fri Sep 25 2020 Gerrit Photon <photon-checkins@vmware.com> 0.11.1-1
- Automatic Version Bump
* Wed Sep 09 2020 Susant Sahani <ssahani@vmware.com>  0.11.0-1
- Initial RPM release
