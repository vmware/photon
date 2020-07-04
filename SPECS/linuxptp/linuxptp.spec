Summary:        The Linux PTP Project
Name:           linuxptp
Version:        2.0
Release:        1%{?dist}
License:        GPL v2
Group:          Productivity/Networking/Other
Url:            http://linuxptp.sourceforge.net/
Source0:        %{name}-%{version}.tgz
%define sha1    linuxptp=592ca42c6146a79c1fcabed7c19fa7af4803d4f6
Source1:        ptp4l.service
Source2:        phc2sys.service
Source3:        phc2sys
Source4:        ptp4l
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  ethtool
BuildRequires:  systemd
Requires:       systemd
Requires:       ethtool
Requires:       glibc

%description
This software is an implementation of the Precision Time Protocol (PTP)
according to IEEE standard 1588 for Linux. The dual design goals are to provide
a robust implementation of the standard and to use the most relevant and modern
Application Programming Interfaces (API) offered by the Linux kernel.

%prep
%setup -q

%build
make %{?_smp_mflags}

%install
make prefix=%{buildroot}%{_prefix} mandir=%{buildroot}%{_mandir} install
mkdir -p %{buildroot}/etc/sysconfig/
mkdir -p %{buildroot}/usr/lib/systemd/system/
install -Dm 0644 configs/default.cfg %{buildroot}/%{_sysconfdir}/ptp4l.conf
install -Dm 0644 %{SOURCE1} %{buildroot}/usr/lib/systemd/system/
install -Dm 0644 %{SOURCE2} %{buildroot}/usr/lib/systemd/system/
install -Dm 0644 %{SOURCE3}  %{buildroot}/etc/sysconfig/
install -Dm 0644 %{SOURCE4}  %{buildroot}/etc/sysconfig/

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig
%systemd_post ptp4l.service
%systemd_post phc2sys.service

%preun
/sbin/ldconfig
%systemd_preun ptp4l.service
%systemd_preun phc2sys.service

%postun -p /bin/sh
%systemd_postun_with_restart ptp4l.service
%systemd_postun_with_restart phc2sys.service

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/ptp4l.conf
%{_sysconfdir}/sysconfig/phc2sys
%{_sysconfdir}/sysconfig/ptp4l
%{_libdir}/systemd/system/phc2sys.service
%{_libdir}/systemd/system/ptp4l.service
%{_sbindir}/hwstamp_ctl
%{_sbindir}/nsm
%{_sbindir}/phc2sys
%{_sbindir}/phc_ctl
%{_sbindir}/pmc
%{_sbindir}/ptp4l
%{_sbindir}/timemaster
%{_mandir}/man8/hwstamp_ctl.8.gz
%{_mandir}/man8/phc2sys.8.gz
%{_mandir}/man8/phc_ctl.8.gz
%{_mandir}/man8/pmc.8.gz
%{_mandir}/man8/ptp4l.8.gz
%{_mandir}/man8/timemaster.8.gz


%changelog
*   Tue May 19 2020 Tapas Kundu <tkundu@vmware.com> 2.0-1
-   Initial version.
