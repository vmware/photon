Summary:        Daemon that finds starving tasks in the system and gives them a temporary boost
Name:           stalld
Version:        1.3.0
Release:        1%{?dist}
License:        GPLv2
Group:          System/Tools
URL:            https://git.kernel.org/pub/scm/utils/stalld/stalld.git
Source0:        https://git.kernel.org/pub/scm/utils/stalld/stalld.git/snapshot/%{name}-%{version}.tar.gz
%define sha1 stalld=461f44e36ee4448324d05d1f2ec7cc054aedd62c
Vendor:         VMware, Inc.
Distribution:   Photon
Source1:        stalld.conf
Source2:        stalld.service

BuildRequires:  glibc-devel
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  systemd
Requires:       systemd

%description
The stalld program monitors the set of system threads, looking for
threads that are ready-to-run but have not been given CPU time for
some threshold period. When a starved thread is found, it is given a
temporary boost using the SCHED_DEADLINE policy. The runtime given to
such stalled threads is configurable by the user.

%prep
%autosetup

%build
make %{?_smp_mflags}

%install
%make_install DESTDIR=%{buildroot} DOCDIR=%{_docdir} MANDIR=%{_mandir} BINDIR=%{_bindir} DATADIR=%{_datadir}
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
* Mon Nov 23 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 1.3.0-1
- Add stalld to Photon OS.
