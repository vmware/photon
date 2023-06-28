Summary:        The Linux PTP Project
Name:           linuxptp
Version:        3.1.1
Release:        5%{?dist}
License:        GPL v2
Group:          Productivity/Networking/Other
Url:            http://linuxptp.sourceforge.net/
Source0:        %{name}-%{version}.tgz
%define sha512  linuxptp=c3c40987fe68480a8473097ebc3c506fb4f8f3b6456bbe637b2b3cb0b3e0182f1513b511fdc04b3607d5f7d8bd1bd22502bb86eb13f9fa4fa63a3331846b33ec
Source1:        ptp4l.service
Source2:        phc2sys.service
Source3:        ts2phc.service
Source4:        phc2sys
Source5:        ptp4l
Source6:        ts2phc
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  ethtool
BuildRequires:  systemd
Requires:       systemd
Requires:       ethtool
Requires:       glibc
Requires:       tzdata >= 2020f-2
Patch0:         0001-Clock-Class-Threshold-Feature-addition-for-PTP4L.patch
Patch1:         0002-clock-Reset-state-when-switching-port-with-same-best.patch
Patch2:         0003-clock-Reset-clock-check-on-best-clock-port-change.patch
Patch3:         0004-port-Don-t-check-timestamps-from-non-slave-ports.patch
Patch4:         0005-port-Don-t-renew-raw-transport.patch
Patch5:         0006-clockcheck-Increase-minimum-interval.patch
Patch6:         0007-phc2sys-move-read_phc-into-clock_adj.c.patch
Patch7:         0008-clockadj-Change-clockadj_compare-to-return-errno.patch
Patch8:         0009-sysoff-Change-sysoff_measure-to-return-errno.patch
Patch9:         0010-sysoff-Change-log-level-of-ioctl-error-messages.patch
Patch10:        0011-sysoff-Retry-on-EBUSY-when-probing-supported-ioctls.patch
Patch11:        0012-phc2sys-Don-t-exit-when-reading-of-PHC-fails-with-EB.patch
Patch12:        0013-sk-Handle-EINTR-when-waiting-for-transmit-timestamp.patch
Patch13:        0014-servo-stop-rounding-initial-frequency-to-nearest-ppb.patch
Patch14:        0015-Don-t-re-arm-fault-clearing-timer-on-unrelated-netli.patch

%description
This software is an implementation of the Precision Time Protocol (PTP)
according to IEEE standard 1588 for Linux. The dual design goals are to provide
a robust implementation of the standard and to use the most relevant and modern
Application Programming Interfaces (API) offered by the Linux kernel.

%prep
%autosetup -n %{name}-%{version} -p1

%build
%make_build

%install
make install %{?_smp_mflags} prefix=%{buildroot}%{_prefix} mandir=%{buildroot}%{_mandir}
mkdir -p %{buildroot}/etc/sysconfig/
mkdir -p %{buildroot}/usr/lib/systemd/system/
install -Dm 0644 configs/default.cfg %{buildroot}/%{_sysconfdir}/ptp4l.conf
install -Dm 0644 configs/ts2phc-generic.cfg %{buildroot}/%{_sysconfdir}/ts2phc.conf
install -Dm 0644 %{SOURCE1} %{buildroot}/usr/lib/systemd/system/
install -Dm 0644 %{SOURCE2} %{buildroot}/usr/lib/systemd/system/
install -Dm 0644 %{SOURCE3} %{buildroot}/usr/lib/systemd/system/
install -Dm 0644 %{SOURCE4}  %{buildroot}/etc/sysconfig/
install -Dm 0644 %{SOURCE5}  %{buildroot}/etc/sysconfig/
install -Dm 0644 %{SOURCE6}  %{buildroot}/etc/sysconfig/
install -vdm755 %{buildroot}%{_libdir}/systemd/system-preset
echo "disable ptp4l.service" > %{buildroot}/usr/lib/systemd/system-preset/50-ptp4l.preset
echo "disable phc2sys.service" > %{buildroot}/usr/lib/systemd/system-preset/50-phc2sys.preset
echo "disable ts2phc.service" > %{buildroot}/usr/lib/systemd/system-preset/50-ts2phc.preset

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig
%systemd_post ptp4l.service
%systemd_post phc2sys.service
%systemd_post ts2phc.service

%preun
/sbin/ldconfig
%systemd_preun ptp4l.service
%systemd_preun phc2sys.service
%systemd_preun ts2phc.service

%postun -p /bin/sh
%systemd_postun_with_restart ptp4l.service
%systemd_postun_with_restart phc2sys.service
%systemd_postun_with_restart ts2phc.service

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/ptp4l.conf
%config(noreplace) %{_sysconfdir}/ts2phc.conf
%config(noreplace) %{_sysconfdir}/sysconfig/phc2sys
%config(noreplace) %{_sysconfdir}/sysconfig/ptp4l
%config(noreplace) %{_sysconfdir}/sysconfig/ts2phc
%{_libdir}/systemd/system/phc2sys.service
%{_libdir}/systemd/system/ptp4l.service
%{_libdir}/systemd/system/ts2phc.service
%{_libdir}/systemd/system-preset/50-ptp4l.preset
%{_libdir}/systemd/system-preset/50-phc2sys.preset
%{_libdir}/systemd/system-preset/50-ts2phc.preset
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
*   Wed Jun 28 2023 Him Kalyan Bordoloi <bordoloih@vmware.com> 3.1.1-5
-   Don't replace config files during update
*   Fri Jun 02 2023 Him Kalyan Bordoloi <bordoloih@vmware.com> 3.1.1-4
-   Backport upstream patches
*   Tue Feb 14 2023 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 3.1.1-3
-   Disable phc2sys service by default
*   Fri Jan 13 2023 Him Kalyan Bordoloi <bordoloih@vmware.com> 3.1.1-2
-   Add service for ts2phc
*   Tue Sep 06 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 3.1.1-1
-   Update to version 3.1.1
*   Tue Jul 06 2021 Vikash Bansal <bvikas@vmware.com> 3.1-3
-   Fix for CVE-2021-3570 and CVE-2021-3571
*   Wed Apr 14 2021 Vikash Bansal <bvikas@vmware.com> 3.1-2
-   Disable ptp4l service by default
*   Mon Nov 09 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 3.1-1
-   Update to version 3.1
*   Tue May 19 2020 Tapas Kundu <tkundu@vmware.com> 2.0-1
-   Initial version.
