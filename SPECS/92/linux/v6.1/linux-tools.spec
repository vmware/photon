%global build_if %{photon_subrelease} >= 100

%define uname_r %{version}-%{release}

Summary:        Linux kernel userspace tools
Name:           linux-tools
Version:        6.1.177
Release:        1%{?acvp_build:.acvp}%{?kat_build:.kat}%{?dist}
Group:          System/Tools
URL:            http://www.kernel.org
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://www.kernel.org/pub/linux/kernel/v6.x/linux-%{version}.tar.xz

# glibc-2.43 build error fixes
Source1: glibc-2.43-build-error-fix.patches
%include %{SOURCE1}

Source2: license.txt
%include %{SOURCE2}

# Build compilation fixes
Patch0: 0001-perf-python-Stop-using-deprecated-PyUnicode_AsString.patch

# perf: off-cpu sample
Patch50: 0001-perf-core-add-logic-to-collect-off-cpu-sample.patch
Patch51: 0002-perf-record-add-options-to-off-cpu.patch
Patch52: 0003-perf-display-off-cpu-samples.patch

# Enable this if there should one 1:1 mapping b/n tools and kernel
#BuildRequires:  linux = %{version}-%{release}
BuildRequires:  bc
BuildRequires:  elfutils-devel
BuildRequires:  openssl-devel
BuildRequires:  slang-devel
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  binutils-devel
BuildRequires:  xz-devel
BuildRequires:  perl
BuildRequires:  flex
BuildRequires:  bison
BuildRequires:  cmake
BuildRequires:  which

%ifarch x86_64
BuildRequires:  pciutils-devel
BuildRequires:  libcap-devel
%endif

Requires:       audit
Requires:       elfutils-libelf
Requires:       binutils-libs
Requires:       xz-libs
Requires:       slang
Requires:       python3
Requires:       traceevent-plugins
%ifarch x86_64
Requires:       pciutils
%endif
Requires: linux-python3-perf = %{version}-%{release}
Requires: bpftool = %{version}-%{release}

%description
Linux kernel userspace tools including perf, turbostat, cpupower and bpftool.

%package -n linux-python3-perf
Summary:        Python bindings for perf
Requires:       %{name} = %{version}-%{release}
Requires:       python3

%description -n linux-python3-perf
Python bindings for perf events.

%package -n bpftool
Summary:        eBPF inspection tool
Requires:       %{name} = %{version}-%{release}

%description -n bpftool
bpftool for inspecting and manipulating eBPF programs and maps.

%prep
%autosetup -p1 -n linux-%{version}

%build
%ifarch aarch64
ARCH_FLAGS="EXTRA_CFLAGS=-Wno-error=format-overflow"
%endif

ARCH_FLAGS="${ARCH_FLAGS} EXTRA_CFLAGS=-Wno-error=deprecated-declarations"

%make_build ARCH=%{_arch} -C tools perf PYTHON=python3 $ARCH_FLAGS

tools/perf/perf -vv | grep libunwind | grep OFF
tools/perf/perf -vv | grep dwarf | grep on

%ifarch x86_64
%make_build ARCH=%{_arch} -C tools turbostat cpupower PYTHON=python3
%endif

%make_build install -C tools/bpf/bpftool prefix=%{_prefix}

%install
%ifarch aarch64
ARCH_FLAGS="EXTRA_CFLAGS=-Wno-error=format-overflow"
%endif

ARCH_FLAGS="${ARCH_FLAGS} EXTRA_CFLAGS=-Wno-error=deprecated-declarations"

%make_build -C tools ARCH=%{_arch} DESTDIR=%{buildroot} \
     prefix=%{_prefix} perf_install PYTHON=python3 $ARCH_FLAGS

%make_build -C tools/perf ARCH=%{_arch} DESTDIR=%{buildroot} \
     prefix=%{_prefix} PYTHON=python3 install-python_ext

%ifarch x86_64
%make_build -C tools ARCH=%{_arch} DESTDIR=%{buildroot} \
      prefix=%{_prefix} mandir=%{_mandir} turbostat_install cpupower_install PYTHON=python3
%endif

%make_build install -C tools/bpf/bpftool \
      prefix=%{_prefix} DESTDIR=%{buildroot}

%files
%defattr(-,root,root)
%ifarch x86_64
%exclude %{_lib64}/traceevent
%endif
%ifarch aarch64
%exclude %{_libdir}/traceevent
%endif
%{_bindir}/*
%{_sysconfdir}/bash_completion.d/perf
%{_libexecdir}/perf-core
%{_docdir}/perf-tip
%{_libdir}/perf/examples/bpf/*
%{_libdir}/perf/include/bpf/*
%{_includedir}/perf/*
%ifarch x86_64
%{_mandir}/*
%{_datadir}/perf-core
%{_includedir}/cpufreq.h
%{_includedir}/cpuidle.h
%{_lib64dir}/libcpupower.so*
%{_docdir}/packages/cpupower
%{_datadir}/bash-completion/completions/cpupower
%config(noreplace) %{_sysconfdir}/cpufreq-bench.conf
%{_sbindir}/cpufreq-bench
%{_datadir}/locale/*/LC_MESSAGES/cpupower.mo
%endif

%files -n linux-python3-perf
%defattr(-,root,root)
%{python3_sitelib}/*

%files -n bpftool
%defattr(-,root,root)
%{_sbindir}/bpftool
%{_datadir}/bash-completion/completions/bpftool

%changelog
* Mon Jul 06 2026 Gerrit Photon <svc.photon-ci@broadcom.com> 6.1.177-1
- Update to version 6.1.177
* Wed Jun 24 2026 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 6.1.176-1
- Update to version 6.1.176
* Mon Jun 01 2026 Keerthana K <keerthana.kalyanasundaram@broadcom.com> 6.1.175-1
- Update to version 6.1.175
* Thu May 28 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 6.1.174-2
- Fix aarch64 build
* Mon May 25 2026 Gerrit Photon <svc.photon-ci@broadcom.com> 6.1.174-1
- Update to version 6.1.174
* Sat May 16 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 6.1.172-2
- Split linux-tools out of linux.spec
