Name:           bpftrace
Version:        0.12.1
Release:        2%{?dist}
Summary:        High-level tracing language for Linux eBPF
License:        ASL 2.0
Vendor:         VMware, Inc.
Distribution:   Photon
Group:          System Environment/Security
URL:            https://github.com/iovisor/bpftrace

Source0:        https://github.com/iovisor/bpftrace/archive/%{name}-%{version}.tar.gz
%define sha512  %{name}=a578499668bd2eb7342689b6c0ef3db6ca263a971d8e6f1b9a68c502c27170d24ede212a0fc2a72263e72aff58924f488a5c80d447397503a08512dc47b63345

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
* Fri Jun 17 2022 Shreenidhi Shedi <sshedi@vmware.com> 0.12.1-2
- Fix build with latest cmake
* Thu Apr 29 2021 Gerrit Photon <photon-checkins@vmware.com> 0.12.1-1
- Automatic Version Bump
* Sat Oct 17 2020 Shreenidhi Shedi <sshedi@vmware.com> 0.11.1-2
- Fix aarch64 build errors
* Fri Sep 25 2020 Gerrit Photon <photon-checkins@vmware.com> 0.11.1-1
- Automatic Version Bump
* Wed Sep 09 2020 Susant Sahani <ssahani@vmware.com>  0.11.0-1
- Initial RPM release
