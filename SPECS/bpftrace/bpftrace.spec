# The post hooks strip the binary which removes
# the BEGIN_trigger and END_trigger functions
# which are needed for the BEGIN and END probes
%global __os_install_post       %{nil}
%global _find_debuginfo_opts    -g

Name:           bpftrace
Version:        0.18.0
Release:        3%{?dist}
Summary:        High-level tracing language for Linux eBPF
License:        ASL 2.0
Vendor:         VMware, Inc.
Distribution:   Photon
Group:          System Environment/Security
URL:            https://github.com/iovisor/bpftrace

Source0: https://github.com/iovisor/bpftrace/archive/%{name}-%{version}.tar.gz
%define sha512 %{name}=b7da273d251f03a81b3a7097407352e7ad1d023972852bdb883176e97bab7046f9f327bd03bca51fe853ecaab5f60adc6994e75cb450a033a5b91118f719c36d

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
* Thu Mar 28 2024 Ashwin Dayanand Kamat <ashwin.kamat@broadcom.com> 0.18.0-3
- Bump version as a part of libxml2 upgrade
* Tue Feb 20 2024 Ashwin Dayanand Kamat <ashwin.kamat@broadcom.com> 0.18.0-2
- Bump version as a part of libxml2 upgrade
* Mon Aug 28 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.18.0-1
- Upgrade to v0.18.0
* Tue Jul 11 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.16.0-5
- Bump version as a part of elfutils upgrade
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
