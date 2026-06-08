%global build_if %{photon_subrelease} >= 91

Name:           iotop-c
Version:        1.31
Release:        1%{?dist}
Summary:        Simple top-like I/O monitor (implemented in C)
URL:            https://github.com/Tomas-M/iotop/
Conflicts:      iotop
#Obsoletes:      iotop < 0.7
BuildRequires:  ncurses-devel
Group:          System/Monitoring
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/Tomas-M/iotop/archive/refs/tags/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

%description
iotop-c does for I/O usage what top(1) does for CPU usage. It watches I/O
usage information output by the Linux kernel and displays a table of
current I/O usage by processes on the system. It is handy for answering
the question "Why is the disk churning so much?".

iotop-c requires a Linux kernel built with the CONFIG_TASKSTATS,
CONFIG_TASK_DELAY_ACCT, CONFIG_TASK_IO_ACCOUNTING and
CONFIG_VM_EVENT_COUNTERS config options on.

iotop-c is an alternative re-implementation of iotop in C, optimized for
performance. Normally a monitoring tool intended to be used on a system
under heavy stress should use the least additional resources as
possible.

%prep
%autosetup -p1 -n iotop-%{version}

%build
%make_build

%install
V=1 STRIP=: BINDIR=%{buildroot}%{_bindir} %make_install

%files
%license COPYING
%license LICENSE
%{_bindir}/iotop
%{_mandir}/man8/iotop.8*

%changelog
* Wed Apr 29 2026 Tapas Kundu <tapas.kundu@broadcom.com> - 1.31-1
- Initial build
