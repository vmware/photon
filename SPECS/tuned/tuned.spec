Name:           tuned
Version:        2.21.0
Release:        2%{?dist}
Summary:        A dynamic adaptive system tuning daemon
Group:          System/Base
URL:            https://github.com/redhat-performance/tuned
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: tuned-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

Patch0:         remove_desktop_utils_dependency.patch
Patch1:         tuned-fix-bug-in-sysctl-verify.patch
Patch2:         bootloader-plugin-support-for-photon.patch
Patch3:         0001-Schedule-perf-events-iff-scheduler-per-process-confi.patch
Patch4:         0001-realtime-Modify-hung_task-detection-param.patch
Patch5:         0001-tuned-don-t-verify-irq-0-on-x86_64.patch
Patch6:         0001-plugin-bootloader-Support-for-ostree-boot.patch
Patch7:         0001-add-support-for-sched-kernel-cmdline-parameter.patch

BuildRequires:  python3-devel
BuildRequires:  systemd-devel

Requires:       dbus-python3
Requires:       ethtool
Requires:       gawk
Requires:       python3-configobj
Requires:       python3-decorator
Requires:       polkit
Requires:       python3-pyudev
Requires:       python3-linux-procfs
Requires:       python3-pygobject
Requires:       python3-schedutils
Requires:       python3-ethtool
Requires:       linux-python3-perf
Requires:       irqbalance
Requires:       systemd
Requires:       virt-what

%if 0%{?with_check}
BuildRequires:  curl-devel
BuildRequires:  python3-pip
BuildRequires:  python3-configobj
BuildRequires:  python3-pyudev
BuildRequires:  python3-decorator
BuildRequires:  dbus-python3
BuildRequires:  python3-pygobject
%endif

BuildArch:      noarch

%description
The tuned package contains a daemon that tunes system settings dynamically.
It does so by monitoring the usage of several system components periodically.
Based on that information components will then be put into lower or higher
power saving modes to adapt to the current usage. Currently only ethernet
network and ATA harddisk devices are implemented.

%package        utils-systemtap
Summary:        Disk and net statistic monitoring systemtap scripts
Group:          System/Base
Requires:       %{name} = %{version}-%{release}
Requires:       systemtap

%description    utils-systemtap
This package contains several systemtap scripts to allow detailed
manual monitoring of the system. Instead of the typical IO/sec it collects
minimal, maximal and average time between operations to be able to
identify applications that behave power inefficient (many small operations
instead of fewer large ones).

%prep
%autosetup -p1

%build
#The tuned daemon is written in pure Python. Nothing requires to be built.

%install
%make_install %{?_smp_mflags}
# conditional support for grub2, grub2 is not available on all architectures
# and tuned is noarch package, thus the following hack is needed
mkdir -p %{buildroot}%{_datadir}/tuned/grub2
mv %{buildroot}%{_sysconfdir}/grub.d/00_tuned %{buildroot}%{_datadir}/tuned/grub2/00_tuned
rmdir %{buildroot}%{_sysconfdir}/grub.d
mkdir -p %{buildroot}%{_var}/lib/tuned \
         %{buildroot}%{_sysconfdir}/modprobe.d
touch %{buildroot}%{_sysconfdir}/modprobe.d/kvm.rt.tuned.conf

#removing powertop2tuned as we do not have powertop for this.
rm %{buildroot}%{_bindir}/powertop2tuned

%check
pip3 install unittest2
make test %{?_smp_mflags}

%post
%systemd_post tuned.service

%preun
%systemd_preun tuned.service

%postun
%systemd_postun_with_restart tuned.service

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING README.md
%{python3_sitelib}/tuned
%{_sbindir}/tuned
%{_sbindir}/tuned-adm
%{_libexecdir}/tuned
%{_sysconfdir}/tuned/active_profile
%config(noreplace) %{_sysconfdir}/modprobe.d/kvm.rt.tuned.conf
%config(noreplace) %{_sysconfdir}/tuned/tuned-main.conf
%{_datadir}/dbus-1/system.d/com.redhat.tuned.conf
%config(noreplace) %{_sysconfdir}/modprobe.d/tuned.conf
%config(noreplace) /boot/tuned.cfg
%config(noreplace) %{_sysconfdir}/tuned/
%{_libdir}/tmpfiles.d
%{_unitdir}/tuned.service
%dir %{_localstatedir}/log/tuned
%dir /etc/tuned
%dir /var/lib/tuned
%{_mandir}/man5/tuned*
%{_mandir}/man8/tuned*
%{_datadir}/tuned/grub2
%{_libdir}/tuned/
%{_datadir}/doc
%exclude %{_datadir}/icons/hicolor/scalable/apps/tuned.svg
%{_datadir}/man/man7/*
%{_datadir}/polkit-1/actions/com.redhat.tuned.policy
%{_datadir}/bash-completion/completions/tuned-adm
%exclude %{_datadir}/tuned/ui/tuned-gui.glade
%exclude %{_sbindir}/tuned-gui
%exclude %{_libdir}/kernel/install.d/92-tuned.install

%files utils-systemtap
%defattr(-,root,root,-)
%doc doc/README.utils doc/README.scomes COPYING
%{_sbindir}/varnetload
%{_sbindir}/netdevstat
%{_sbindir}/diskdevstat
%{_sbindir}/scomes
%{_mandir}/man8/varnetload.*
%{_mandir}/man8/netdevstat.*
%{_mandir}/man8/diskdevstat.*
%{_mandir}/man8/scomes.*

%changelog
* Wed Dec 11 2024 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 2.21.0-2
- Release bump for SRP compliance
* Tue Jan 23 2024 Roye Eshed <roye.eshed@broadcom.com> 2.21.0-1
- Update Tuned to 2.21.0
* Tue Sep 12 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 2.19.0-10
- Add support for the 'sched' kernel cmdline parameter
* Fri Aug 25 2023 Ankit Jain <ankitja@vmware.com> 2.19.0-9
- Enable support for ostree-boot
* Wed Apr 26 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 2.19.0-8
- Patch tuned to ignore verification of smp affinity for irq 0 on x86.
* Thu Mar 16 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 2.19.0-7
- Fix bug setting netdev_queue_count
* Thu Mar 09 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 2.19.0-6
- Properly expand variable functions in plugin_net.py
* Thu Jan 12 2023 Keerthana K <keerthanak@vmware.com> 2.19.0-5
- Forward port patches from ph4
- Add /var/lib/tuned to rpm
* Tue Dec 06 2022 Prashant S Chauhan <psinghchauha@vmware.com> 2.19.0-4
- Update release to compile with python 3.11
* Fri Dec 02 2022 Srinidhi Rao <srinidhir@vmware.com> 2.19.0-3
- Bump version as a part of systemtap upgrade
* Tue Oct 04 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.19.0-2
- Bump version as a part of polkit upgrade
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 2.19.0-1
- Automatic Version Bump
* Tue Apr 19 2022 Gerrit Photon <photon-checkins@vmware.com> 2.18.0-1
- Automatic Version Bump
* Tue Oct 19 2021 Shreenidhi Shedi <sshedi@vmware.com> 2.15.0-2
- Bump version as a part of polkit upgrade
* Thu Apr 29 2021 Gerrit Photon <photon-checkins@vmware.com> 2.15.0-1
- Automatic Version Bump
* Fri Oct 09 2020 svasamsetty <svasamsetty@vmware.com> 2.14.0-3
- Re-enable tuned as it was deactivated due to openssl 1.1.1
* Wed Sep 23 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 2.14.0-2
- Bootloader plugin support for Photon
- sysctl plugin verify bug fix
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 2.14.0-1
- Automatic Version Bump
* Wed May 13 2020 Tapas Kundu <tkundu@vmware.com> 2.13.0-2
- Replaced requires from python3-perf to linux-python3-perf.
* Wed Mar 18 2020 Tapas Kundu <tkundu@vmware.com> 2.13.0-1
- Initial release.
