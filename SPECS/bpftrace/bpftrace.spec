Name:           bpftrace
Version:        0.11.1
Release:        1%{?dist}
Summary:        High-level tracing language for Linux eBPF
License:        ASL 2.0
Vendor:         VMware, Inc.
Distribution:   Photon
Group:          System Environment/Security

URL:            https://github.com/iovisor/bpftrace
Source0:        https://github.com/iovisor/bpftrace/archive/%{name}-%{version}.tar.gz
%define sha1    bpftrace=6bb8d682de04ffd47d565eb2542bc7c7d7b5da84

BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  cmake
BuildRequires:  elfutils-libelf-devel
BuildRequires:  zlib-devel
BuildRequires:  llvm-devel
BuildRequires:  clang-devel
BuildRequires:  bcc-devel
BuildRequires:  git

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
%setup -n %{name}-%{version}

%build
%cmake . \
        -DCMAKE_BUILD_TYPE=RelWithDebInfo \
        -DSYSTEM_BCC_LIBRARY:BOOL=ON      \
        -DENABLE_TESTS:BOOL=OFF           \
        -DBUILD_SHARED_LIBS:BOOL=OFF      \
        -DBUILD_DEPS=OFF
make %{?_smp_mflags}

%install
%make_install

%files
%doc README.md CONTRIBUTING-TOOLS.md
%doc docs/reference_guide.md docs/tutorial_one_liners.md
%license LICENSE
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/tools
%{_bindir}/%{name}
%{_mandir}/man8/*
%attr(0755,-,-) %{_datadir}/%{name}/tools/*

%changelog
* Fri Sep 25 2020 Gerrit Photon <photon-checkins@vmware.com> 0.11.1-1
- Automatic Version Bump
* Wed Sep 09 2020 Susant Sahani <ssahani@vmware.com>  0.11.0-1
- Initial RPM release
