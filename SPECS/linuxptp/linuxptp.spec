Summary:        The Linux PTP Project
Name:           linuxptp
Version:        4.2
Release:        2%{?dist}
Group:          Productivity/Networking/Other
Url:            http://linuxptp.sourceforge.net/
Source0:        %{name}-%{version}.tgz
Source1:        ptp4l.service
Source2:        phc2sys.service
Source3:        ts2phc.service
Source4:        phc2sys
Source5:        ptp4l
Source6:        ts2phc

Source7: license.txt
%include %{SOURCE7}
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  ethtool
BuildRequires:  systemd-devel
BuildRequires:  libmnl
Requires:       systemd
Requires:       ethtool
Requires:       glibc
Requires:       tzdata >= 2022g-2

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
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
mkdir -p %{buildroot}%{_unitdir}
install -Dm 0644 configs/default.cfg %{buildroot}%{_sysconfdir}/ptp4l.conf
install -Dm 0644 configs/ts2phc-generic.cfg %{buildroot}%{_sysconfdir}/ts2phc.conf
install -Dm 0644 %{SOURCE1} %{buildroot}%{_unitdir}
install -Dm 0644 %{SOURCE2} %{buildroot}%{_unitdir}
install -Dm 0644 %{SOURCE3} %{buildroot}%{_unitdir}
install -Dm 0644 %{SOURCE4}  %{buildroot}%{_sysconfdir}/sysconfig/
install -Dm 0644 %{SOURCE5}  %{buildroot}%{_sysconfdir}/sysconfig/
install -Dm 0644 %{SOURCE6}  %{buildroot}%{_sysconfdir}/sysconfig/
install -vdm755 %{buildroot}%{_presetdir}
echo "disable ptp4l.service" > %{buildroot}%{_presetdir}/50-ptp4l.preset
echo "disable phc2sys.service" > %{buildroot}%{_presetdir}/50-phc2sys.preset
echo "disable ts2phc.service" > %{buildroot}%{_presetdir}/50-ts2phc.preset

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
%{_sysconfdir}/sysconfig/phc2sys
%{_sysconfdir}/sysconfig/ptp4l
%{_sysconfdir}/sysconfig/ts2phc
%{_unitdir}/phc2sys.service
%{_unitdir}/ptp4l.service
%{_unitdir}/ts2phc.service
%{_presetdir}/50-ptp4l.preset
%{_presetdir}/50-phc2sys.preset
%{_presetdir}/50-ts2phc.preset
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
*   Thu Dec 12 2024 Ajay Kaher <ajay.kaher@broadcom.com> 4.2-2
-   Release bump for SRP compliance
*   Thu Mar 21 2024 Roye Eshed <roye.eshed@broadcom.com> 4.2-1
-   Upgrade linuxptp to version 4.2
*   Wed Aug 16 2023 Roye Eshed <eshedr@vmware.com> 4.0-1
-   Port linuxptp 4.0 update from Photon 3.0 (from Brennan Lamoreaux)
*   Fri Jun 02 2023 Him Kalyan Bordoloi <bordoloih@vmware.com> 3.1.1-4
-   Backport upstream patches
*   Mon Mar 06 2023 Him Kalyan Bordoloi <bordoloih@vmware.com> 3.1.1-3
-   Add service for ts2phc
*   Mon Jan 23 2023 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 3.1.1-2
-   Disable phc2sys service by default
*   Tue Sep 06 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 3.1.1-1
-   Update to version 3.1.1
*   Wed Apr 14 2021 Vikash Bansal <bvikas@vmware.com> 3.1-2
-   Disable ptp4l service by default
*   Fri Sep 25 2020 Gerrit Photon <photon-checkins@vmware.com> 3.1-1
-   Automatic Version Bump
*   Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 3.0-1
-   Automatic Version Bump
*   Tue May 19 2020 Tapas Kundu <tkundu@vmware.com> 2.0-1
-   Initial version.
