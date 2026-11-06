%package tools
Summary:        Linux kernel userspace tools including perf, turbostat, cpupower and bpftool
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
Requires:       linux-python3-perf = %{version}-%{release}
Requires:       bpftool = %{version}-%{release}

%description tools
Linux kernel userspace tools including perf, turbostat, cpupower and bpftool.

%package python3-perf
Summary:        Python bindings for perf
Requires:       %{name}-tools = %{version}-%{release}
Requires:       python3

%description python3-perf
Python bindings for perf events.

%package -n bpftool
Summary:        eBPF inspection tool
Requires:       %{name}-tools = %{version}-%{release}

%description -n bpftool
bpftool for inspecting and manipulating eBPF programs and maps.

