Summary:        Daemon that finds starving tasks in the system and gives them a temporary boost
Name:           stalld
Version:        1.14.1
Release:        3%{?dist}
License:        GPLv2
Group:          System/Tools
URL:            https://git.kernel.org/pub/scm/utils/stalld/stalld.git
Source0:        https://git.kernel.org/pub/scm/utils/stalld/stalld.git/snapshot/%{name}-%{version}.tar.gz
%define sha512 stalld=439cd930ae95435415fccc0658f3733b4b7b0cffa91eeb0c72dde8dd805a622a72df617f8b9cb1feb5278e39db9da654ef171e73058d2ab3b7c264a522de818c
Vendor:         VMware, Inc.
Distribution:   Photon
Source1:        stalld-tca.conf
BuildRequires:  glibc-devel
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  systemd
Requires:       systemd
Requires:       bash
Patch0:         0001-stalld-Fix-for-failed-to-parse-cpu-info-warning.patch
Patch1:         0001-stalld-Add-error-handling-for-thread-creation-failur.patch
Patch2:         0001-stalld-Expose-verbose-parameter-in-the-config-file.patch
Patch3:         0001-stalld-Assign-name-to-stalld-thread.patch
Patch4:         0001-utils.c-Add-error-handling-for-enabling-HRTICK.patch
Patch5:         0001-stalld-Fix-nr_periods-calculation-in-do_fifo_boost.patch
Patch6:         0001-stalld-Fix-gcc-options-in-Makefile.patch
Patch7:         0001-stalld-Fix-single-threaded-mode-starvation-threshold.patch
Patch8:         0001-stalld-Add-debug-print-for-starving-tasks.patch
Patch9:         0001-stalld-change-default-config_granularity-value-to-2s.patch
Patch10:        0001-stalld-Include-FF-and-CG-config-params-in-service-fi.patch
Patch11:        0001-stalld-fix-bin-bash.patch
Patch12:        0001-stalld-Skip-get_cpu_idle_time-warning-for-offline-cp.patch
Patch13:        0001-throttling-Always-null-terminate-sched_rt_runtime_us.patch
Patch14:        0001-stalld-print-process-comm-and-cpu-when-boosting.patch
Patch15:        0001-stalld-Fix-memory-leak-in-print_boosted_info.patch
Patch16:        0001-stalld-Detect-runnable-dying-tasks.patch
Patch17:        0001-stalld-utils-Fix-freeing-of-invalid-pointer.patch

%description
The stalld program monitors the set of system threads, looking for
threads that are ready-to-run but have not been given CPU time for
some threshold period. When a starved thread is found, it is given a
temporary boost using the SCHED_DEADLINE policy. The runtime given to
such stalled threads is configurable by the user.

%prep
%autosetup -p1

%build
make %{?_smp_mflags}

%install
%make_install DESTDIR=%{buildroot} DOCDIR=%{_docdir} MANDIR=%{_mandir} BINDIR=%{_bindir} DATADIR=%{_datadir}
install -vdm 755 %{buildroot}/%{_sysconfdir}/sysconfig
cp %{SOURCE1} %{buildroot}/%{_sysconfdir}/sysconfig/stalld
chmod 644 %{buildroot}/%{_sysconfdir}/sysconfig/stalld
install -vdm 755 %{buildroot}/%{_unitdir}
install -vm 644 redhat/stalld.service %{buildroot}/%{_unitdir}
install -p scripts/throttlectl.sh %{buildroot}/%{_bindir}/throttlectl

%clean
rm -rf %{buildroot}

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%defattr(-,root,root)
%{_bindir}/%{name}
%{_bindir}/throttlectl
%{_unitdir}/%{name}.service
%config(noreplace) %{_sysconfdir}/sysconfig/stalld
%doc %{_docdir}/README.md
%doc %{_mandir}/man8/stalld.8*
%license %{_datadir}/licenses/%{name}/gpl-2.0.txt

%changelog
* Mon Mar 06 2023 Ankit Jain <ankitja@vmware.com> 1.14.1-3
- Fix freeing of invalid pointer
* Tue Feb 07 2023 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 1.14.1-2
- Detect and boost runnable dying tasks
* Tue Jul 12 2022 Keerthana K <keerthanak@vmware.com> 1.14.1-1
- Update to version 1.14.1
- Package TCA's stalld config file as default config
* Mon Jun 27 2022 Sharan Turlapati <sturlapati@vmware.com> 1.3.0-11
- Fix nr_periods calculation while boosting using SCHED_FIFO
- Expose FORCE_FIFO as an option in the conf file
* Mon Apr 11 2022 Sharan Turlapati <sturlapati@vmware.com> 1.3.0-10
- Exit early if enabling HRTICK fails when using SCHED_DEADLINE
* Fri Mar 25 2022 Sharan Turlapati <sturlapati@vmware.com> 1.3.0-9
- Add HRTICK_DL support for stalld
* Mon Sep 20 2021 Ankit Jain <ankitja@vmware.com> 1.3.0-8
- Assign name to stalld threads.
* Tue Sep 07 2021 Ankit Jain <ankitja@vmware.com> 1.3.0-7
- Removing D-state task stack dumping changes
* Mon Jun 28 2021 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 1.3.0-6
- Expose verbose logging parameter in the config file.
* Mon Jun 28 2021 Vikash Bansal <bvikas@vmware.com> 1.3.0-5
- Detect tasks in D state and log their stack traces for analysis.
* Mon Jun 28 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 1.3.0-4
- Add error handling for thread creation failure.
* Wed Mar 03 2021 Vikash Bansal <bvikas@vmware.com> 1.3.0-3
- Fix for "error parsing CPU info" warning
* Tue Feb 16 2021 Sharan Turlapati <sturlapati@vmware.com> 1.3.0-2
- Support denylisting of tasks in stalld
* Mon Nov 23 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 1.3.0-1
- Add stalld to Photon OS.
