Summary:        Daemon that finds starving tasks in the system and gives them a temporary boost
Name:           stalld
Version:        1.17.1
Release:        3%{?dist}
License:        GPLv2
Group:          System/Tools
URL:            https://git.kernel.org/pub/scm/utils/stalld/stalld.git
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://git.kernel.org/pub/scm/utils/stalld/stalld.git/snapshot/%{name}-%{version}.tar.gz
%define sha512 %{name}=db5e2c129afe9f3ce90981250e1804b55b044bd3d8787695100cd5c9030f080e1c58866754bbd9e40448481c02c77bac758368b632ce2383c39508b8b70c5763

Source1: %{name}-tca.conf

BuildRequires: build-essential
BuildRequires: systemd-devel

Requires: bash
Requires: systemd

Patch0: 0001-stalld-Fix-for-failed-to-parse-cpu-info-warning.patch
Patch1: 0002-stalld-Add-error-handling-for-thread-creation-failur.patch
Patch2: 0003-stalld-Expose-verbose-parameter-in-the-config-file.patch
Patch3: 0004-stalld-Assign-name-to-stalld-thread.patch
Patch4: 0005-stalld-Fix-gcc-options-in-Makefile.patch
Patch5: 0006-stalld-Fix-single-threaded-mode-starvation-threshold.patch
Patch6: 0001-stalld-Add-debug-print-for-starving-tasks.patch
Patch7: 0001-stalld-change-default-config_granularity-value-to-2s.patch
Patch8: 0001-stalld-Include-FF-and-CG-config-params-in-service-fi.patch
Patch9: 0001-stalld-fix-bin-bash.patch
Patch10: 0001-stalld-utils-Fix-freeing-of-invalid-pointer.patch

%description
The stalld program monitors the set of system threads, looking for
threads that are ready-to-run but have not been given CPU time for
some threshold period. When a starved thread is found, it is given a
temporary boost using the SCHED_DEADLINE policy. The runtime given to
such stalled threads is configurable by the user.

%prep
%autosetup -p1

%build
%make_build

%install
%make_install %{?_smp_mflags}

install -vdm 755 %{buildroot}%{_sysconfdir}/sysconfig
cp %{SOURCE1} %{buildroot}%{_sysconfdir}/sysconfig/%{name}
chmod 644 %{buildroot}%{_sysconfdir}/sysconfig/%{name}
install -vdm 755 %{buildroot}%{_unitdir}
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
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%doc %{_docdir}/README.md
%doc %{_mandir}/man8/stalld.8*
%license %{_datadir}/licenses/%{name}/gpl-2.0.txt

%changelog
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
