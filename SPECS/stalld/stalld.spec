Summary:        Daemon that finds starving tasks in the system and gives them a temporary boost
Name:           stalld
Version:        1.15.0
Release:        1%{?dist}
License:        GPLv2
Group:          System/Tools
URL:            https://git.kernel.org/pub/scm/utils/stalld/stalld.git
Source0:        https://git.kernel.org/pub/scm/utils/stalld/stalld.git/snapshot/%{name}-%{version}.tar.gz
%define sha512  stalld=640e3a3715319233aae5f2e75ba9cd4a20ed1e4056a702f1c8d85832f5c32e93b44419c2c32791044e8bbf210ac3b2ce8c18bf89eaf64f22c90931f78945fb57
Vendor:         VMware, Inc.
Distribution:   Photon
Source1:        stalld.conf
Source2:        stalld.service
BuildRequires:  glibc-devel
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  systemd
Requires:       systemd
Patch0:         0001-stalld-Fix-for-failed-to-parse-cpu-info-warning.patch
Patch1:         0001-stalld-Add-error-handling-for-thread-creation-failur.patch
Patch2:         0001-stalld-Expose-verbose-parameter-in-the-config-file.patch
Patch3:         0001-stalld-Assign-name-to-stalld-thread.patch
Patch4:         0001-stalld-Fix-gcc-options-in-Makefile.patch
Patch5:         0001-stalld-Fix-single-threaded-mode-starvation-threshold.patch

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
%make_install \
     DESTDIR=%{buildroot} \
     DOCDIR=%{_docdir} \
     MANDIR=%{_mandir} \
     BINDIR=%{_bindir} \
     DATADIR=%{_datadir} \
     %{?_smp_mflags}
install -vdm 755 %{buildroot}/%{_sysconfdir}/sysconfig
cp %{SOURCE1} %{buildroot}/%{_sysconfdir}/sysconfig/stalld
chmod 644 %{buildroot}/%{_sysconfdir}/sysconfig/stalld
install -vdm 755 %{buildroot}/%{_unitdir}
install -vm 644 %{SOURCE2} %{buildroot}/%{_unitdir}

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
%{_unitdir}/%{name}.service
%config(noreplace) %{_sysconfdir}/sysconfig/stalld
%doc %{_docdir}/README.md
%doc %{_mandir}/man8/stalld.8*
%license %{_datadir}/licenses/%{name}/gpl-2.0.txt

%changelog
* Tue Apr 19 2022 Gerrit Photon <photon-checkins@vmware.com> 1.15.0-1
- Automatic Version Bump
* Thu Jun 24 2021 Vikash Bansal <bvikas@vmware.com> 1.3.0-3
- Fix for "error parsing CPU info" warning
* Tue Feb 16 2021 Sharan Turlapati <sturlapati@vmware.com> 1.3.0-2
- Support denylisting of tasks in stalld
* Mon Nov 23 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 1.3.0-1
- Add stalld to Photon OS.
