# The post hooks strip the binary which removes
# the BEGIN_trigger and END_trigger functions
# which are needed for the BEGIN and END probes
%global __os_install_post       %{nil}
%global _find_debuginfo_opts    -g

Name:           bpftrace
Version:        0.21.2
Release:        1%{?dist}
Summary:        High-level tracing language for Linux eBPF
Vendor:         VMware, Inc.
Distribution:   Photon
Group:          System Environment/Security
URL:            https://github.com/iovisor/bpftrace

Source0: https://github.com/iovisor/bpftrace/archive/%{name}-%{version}.tar.gz
%define sha512 %{name}=8c64de94da29030dcde0680be90e3c16a5cd965a0066b1abe3c0740f11a78d70f383bf2e0bbe2fce639eddc7d45cb44508cc8a78743c205d7efa45734151e743

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  cmake
BuildRequires:  elfutils-libelf-devel
BuildRequires:  zlib-devel
BuildRequires:  llvm-devel
BuildRequires:  clang-devel
BuildRequires:  libbpf-devel
BuildRequires:  binutils-devel
BuildRequires:  cereal-devel
BuildRequires:  curl-devel
BuildRequires:  libbpf-devel
BuildRequires:  bcc-devel
BuildRequires:  libxml2-devel
BuildRequires:  libffi-devel
BuildRequires:  libpcap-devel
BuildRequires:  systemtap-sdt-devel

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
export LDFLAGS="-lz"
%{cmake} \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    -DBUILD_TESTING:BOOL=OFF \
    -DBUILD_SHARED_LIBS:BOOL=OFF \
    -DENABLE_TESTS:BOOL=OFF \
    -DBUILD_DEPS=OFF \
    -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
    -DUSE_SYSTEM_BPF_BCC=ON

%{cmake_build}

%install
%{cmake_install}

find %{buildroot}%{_datadir}/%{name}/tools -type f -exec \
  sed -i -e '1s=^#!/usr/bin/env %{name}\([0-9.]\+\)\?$=#!%{_bindir}/%{name}=' {} \;

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%doc README.md CONTRIBUTING-TOOLS.md
%doc docs/reference_guide.md docs/tutorial_one_liners.md
%license LICENSE
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
* Mon Dec 23 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 0.21.2-1
- Upgrade to v0.21.2, fixes CVE-2024-2313
* Thu Dec 12 2024 HarinadhD <harinadh.dommaraju@broadcom.com> 0.18.0-2
- Release bump for SRP compliance
* Mon Aug 28 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.18.0-1
- Upgrade to v0.18.0
* Wed Apr 19 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 0.16.0-4
- Bump version as a part of libbpf upgrade
* Fri Apr 14 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.16.0-3
- Bump version as a part of zlib upgrade
* Fri Jan 06 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 0.16.0-2
- Bump up due to change in elfutils
* Tue Sep 27 2022 Shreenidhi Shedi <sshedi@vmware.com> 0.16.0-1
- Upgrade to v0.16.0
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
