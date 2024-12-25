Name:           bpftrace
Version:        0.16.0
Release:        3%{?dist}
Summary:        High-level tracing language for Linux eBPF
License:        ASL 2.0
Vendor:         VMware, Inc.
Distribution:   Photon
Group:          System Environment/Security
URL:            https://github.com/iovisor/bpftrace

Source0: https://github.com/iovisor/bpftrace/archive/%{name}-%{version}.tar.gz
%define sha512 %{name}=52ca4fea4e2f8d2cbf0f9f1bc69af0ee3408201f019006dd2e838b9458cfc01761eba3df24c39e05cf93220d85d0cecc69bb44ec72f9f44cec0eb94479bff734

Patch0:         CVE-2024-2313-1.patch
Patch1:         CVE-2024-2313-2.patch

BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  cmake
BuildRequires:  elfutils-libelf-devel
BuildRequires:  zlib-devel
BuildRequires:  llvm-devel
BuildRequires:  clang-devel
BuildRequires:  bcc-devel >= 0.11.0-2
BuildRequires:  libbpf-devel >= 1.0.0
BuildRequires:  binutils-devel
BuildRequires:  cereal-devel
BuildRequires:  curl-devel

Requires:       bcc
Requires:       bcc-tools
Requires:       clang
Requires:       llvm
Requires:       zlib
Requires:       libbpf >= 1.0.0

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
%cmake \
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

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/tools
%dir %{_datadir}/%{name}/tools/doc
%{_bindir}/%{name}
%{_bindir}/%{name}-aotrt
%{_mandir}/man8/*
%attr(0755,-,-) %{_datadir}/%{name}/tools/*.bt
%attr(0755,-,-) %{_datadir}/%{name}/tools/old/*.bt
%{_datadir}/%{name}/tools/doc/*.txt

%changelog
* Wed Dec 25 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 0.16.0-3
- CVE-2024-2313 fix
* Fri Apr 14 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 0.16.0-2
- Bump version as a part of libbpf upgrade
* Tue Sep 27 2022 Shreenidhi Shedi <sshedi@vmware.com> 0.16.0-1
- Upgrade to v0.16.0
* Mon Feb 08 2021 Shreenidhi Shedi <sshedi@vmware.com> 0.11.4-1
- Upgrade to v0.11.4
* Sat Oct 17 2020 Shreenidhi Shedi <sshedi@vmware.com> 0.11.1-2
- Fix aarch64 build errors
* Fri Sep 25 2020 Gerrit Photon <photon-checkins@vmware.com> 0.11.1-1
- Automatic Version Bump
* Wed Sep 09 2020 Susant Sahani <ssahani@vmware.com>  0.11.0-1
- Initial RPM release
