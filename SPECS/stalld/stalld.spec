Summary:        Daemon that finds starving tasks in the system and gives them a temporary boost
Name:           stalld
Version:        1.19.1
Release:        5%{?dist}
Group:          System/Tools
URL:            https://gitlab.com/rt-linux-tools/stalld
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://gitlab.com/rt-linux-tools/stalld/-/archive/v%{version}/%{name}-v%{version}.tar.gz

Source1: %{name}-tca.conf

Source2: license.txt
%include %{SOURCE2}

BuildRequires: build-essential
BuildRequires: systemd-devel
BuildRequires: libbpf-devel
%ifarch x86_64
BuildRequires: linux-rt-stalld-ebpf-plugin
Requires: linux-rt-stalld-ebpf-plugin
%endif
Requires: bash
Requires: systemd

Patch0: 0001-stalld-Fix-for-failed-to-parse-cpu-info-warning.patch
Patch1: 0002-stalld-Add-error-handling-for-thread-creation-failur.patch
Patch2: 0003-stalld-Expose-verbose-parameter-in-the-config-file.patch
Patch3: 0004-stalld-Assign-name-to-stalld-thread.patch
Patch4: 0005-stalld-Fix-gcc-options-in-Makefile.patch
Patch5: 0006-stalld-Fix-single-threaded-mode-starvation-threshold.patch
Patch6: 0007-stalld-Add-debug-print-for-starving-tasks.patch
Patch7: 0008-stalld-change-default-config_granularity-value-to-2s.patch
Patch8: 0009-stalld-Include-FF-and-CG-config-params-in-service-fi.patch
Patch9: 0001-stalld-Move-logging-to-dedicated-thread.patch
Patch10: 0002-stalld-Boost-and-Migrate-Feature.patch
%ifarch x86_64
Patch11: 0001-stalld-service-Include-BE-option-in-stalld-service-f.patch
Patch12: 0001-Disable-eBPF-skeleton-creation-instead-use-eBPF-obje.patch
%endif

%description
The stalld program monitors the set of system threads, looking for
threads that are ready-to-run but have not been given CPU time for
some threshold period. When a starved thread is found, it is given a
temporary boost using the SCHED_DEADLINE policy. The runtime given to
such stalled threads is configurable by the user.

%prep
%autosetup -p1 -n %{name}-v%{version}

%build
%ifarch x86_64
%make_build
%else
%make_build USE_BPF=0
%endif

%install
%make_install %{?_smp_mflags}
# overwrite default stalld conf with stalld-tca.conf
install -vm 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/sysconfig/%{name}

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
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%doc %{_docdir}/stalld/README.md
%doc %{_mandir}/man8/stalld.8*
%license %{_datadir}/licenses/%{name}/gpl-2.0.txt

%changelog
* Thu Dec 12 2024 Dweep Advani <dweep.advani@broadcom.com> 1.19.1-5
- Release bump for SRP compliance
* Thu Apr 04 2024 Him Kalyan Bordoloi <him-kalyan.bordoloi@broadcom.com> 1.19.1-4
- Fix ARM build failure
* Mon Mar 04 2024 Him Kalyan Bordoloi <him-kalyan.bordoloi@broadcom.com> 1.19.1-3
- Feature to move logging to a dedicated thread
- Feature to use boosting and task migration to alleviate stall
* Tue Feb 27 2024 Ankit Jain <ankit-ja.jain@broadcom.com> 1.19.1-2
- Fix for ARM build failure
* Mon Feb 05 2024 Ankit Jain <ankit-ja.jain@broadcom.com> 1.19.1-1
- Update version to 1.19.1 with eBPF based backend support
* Mon Mar 06 2023 Ankit Jain <ankitja@vmware.com> 1.17.1-3
- Fix freeing of invalid pointer
* Tue Nov 29 2022 Keerthana K <keerthanak@vmware.com> 1.17.1-2
- Fix service file and update stalld-tca.conf
* Wed Nov 16 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.17.1-1
- Upgrade to v1.17.1
* Tue Apr 19 2022 Gerrit Photon <photon-checkins@vmware.com> 1.15.0-1
- Automatic Version Bump
* Thu Jun 24 2021 Vikash Bansal <bvikas@vmware.com> 1.3.0-3
- Fix for "error parsing CPU info" warning
* Tue Feb 16 2021 Sharan Turlapati <sturlapati@vmware.com> 1.3.0-2
- Support denylisting of tasks in stalld
* Mon Nov 23 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 1.3.0-1
- Add stalld to Photon OS
