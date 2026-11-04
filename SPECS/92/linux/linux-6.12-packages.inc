%package tools
Summary:        This package contains the 'perf' performance analysis tools for Linux kernel
Group:          System/Tools
Requires:       audit elfutils-libelf binutils-libs
Requires:       xz-libs
Requires:       slang
Requires:       python3
Requires:       traceevent-plugins
%ifarch x86_64
Requires:       pciutils
%endif
%description tools
This package contains kernel tools like perf, turbostat and cpupower.

%package python3-perf
Summary:        Python bindings for applications that will manipulate perf events.
Group:          Development/Libraries
Requires:       linux-tools = %{version}-%{release}
Requires:       python3

%description python3-perf
This package provides a module that permits applications written in the
Python programming language to use the interface to manipulate perf events.

%package -n bpftool
Summary:    Inspection and simple manipulation of eBPF programs and maps
Group:      Development/Libraries
Requires:   linux-tools = %{version}-%{release}

%description -n bpftool
This package contains the bpftool, which allows inspection and simple
manipulation of eBPF programs and maps.

