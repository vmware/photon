Summary:        The Linux PTP Project
Name:           linuxptp
Version:        3.1
Release:        3%{?dist}
License:        GPL v2
Group:          Productivity/Networking/Other
Url:            http://linuxptp.sourceforge.net/
Source0:        %{name}-%{version}.tgz
%define sha1    linuxptp=9a3869dbd322252c9a6bc0dbdfe8941586810a7f
Source1:        ptp4l.service
Source2:        phc2sys.service
Source3:        phc2sys
Source4:        ptp4l
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  ethtool
BuildRequires:  systemd
BuildRequires:  libmnl
Requires:       systemd
Requires:       ethtool
Requires:       glibc
# Fix for CVE-2021-3570
Patch0:         0001-Validate-the-messageLength-field-of-incoming-message.patch
# Fix for CVE-2021-3571
Patch1:         0002-tc-Fix-length-of-follow-up-message-of-one-step-sync.patch

%description
This software is an implementation of the Precision Time Protocol (PTP)
according to IEEE standard 1588 for Linux. The dual design goals are to provide
a robust implementation of the standard and to use the most relevant and modern
Application Programming Interfaces (API) offered by the Linux kernel.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

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
install -vdm755 %{buildroot}%{_libdir}/systemd/system-preset
echo "disable ptp4l.service" > %{buildroot}/usr/lib/systemd/system-preset/50-ptp4l.preset

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
%{_libdir}/systemd/system-preset/50-ptp4l.preset
%{_sbindir}/hwstamp_ctl
%{_sbindir}/nsm
%{_sbindir}/phc2sys
%{_sbindir}/phc_ctl
%{_sbindir}/pmc
%{_sbindir}/ptp4l
%{_sbindir}/timemaster
%{_sbindir}/ts2phc
%{_mandir}/man8/hwstamp_ctl.8.gz
%{_mandir}/man8/phc2sys.8.gz
%{_mandir}/man8/phc_ctl.8.gz
%{_mandir}/man8/pmc.8.gz
%{_mandir}/man8/ptp4l.8.gz
%{_mandir}/man8/timemaster.8.gz
%{_mandir}/man8/nsm.8.gz
%{_mandir}/man8/ts2phc.8.gz

%changelog
*   Tue Jul 06 2021 Vikash Bansal <bvikas@vmware.com> 3.1-3
-   Fix for CVE-2021-3570 and CVE-2021-3571
*   Wed Apr 14 2021 Vikash Bansal <bvikas@vmware.com> 3.1-2
-   Disable ptp4l service by default
*   Fri Sep 25 2020 Gerrit Photon <photon-checkins@vmware.com> 3.1-1
-   Automatic Version Bump
*   Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 3.0-1
-   Automatic Version Bump
*   Tue May 19 2020 Tapas Kundu <tkundu@vmware.com> 2.0-1
-   Initial version.
