Summary:        The Linux PTP Project
Name:           linuxptp
Version:        4.0
Release:        2%{?dist}
License:        GPL v2
Group:          Productivity/Networking/Other
Url:            http://linuxptp.sourceforge.net/
Source0:        %{name}-%{version}.tgz
%define sha512  linuxptp=763de5654f0426f2f489223e02fb3dd39a3a830751b366406657efe33bb923b5b38edada7b62de3efed6d257d5d386ece0d42a5eb92da5e5d443eac9b32e105d
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
Requires:       tzdata >= 2023c-1

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
%{_sbindir}/tz2alt
%{_mandir}/man8/hwstamp_ctl.8.gz
%{_mandir}/man8/phc2sys.8.gz
%{_mandir}/man8/phc_ctl.8.gz
%{_mandir}/man8/pmc.8.gz
%{_mandir}/man8/ptp4l.8.gz
%{_mandir}/man8/timemaster.8.gz
%{_mandir}/man8/nsm.8.gz
%{_mandir}/man8/ts2phc.8.gz
%{_mandir}/man8/tz2alt.8.gz

%changelog
*   Wed Jul 05 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 4.0-2
-   Build with latest tzdata for accurate timing
*   Thu Jun 29 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 4.0-1
-   Update to version 4.0
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
