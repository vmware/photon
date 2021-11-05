%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
Name:           tuned
Version:        2.15.0
Release:        3%{?dist}
Summary:        A dynamic adaptive system tuning daemon
License:        GNU GENERAL PUBLIC LICENSE Version 2
Group:          System/Base
Url:            https://github.com/redhat-performance/tuned
Source:         tuned-%{version}.tar.gz
%define         sha1 tuned=bfb3def0b687bbdae2b3e191d2fda46b3ffca1c0
Patch0:         remove_desktop_utils_dependency.patch
Patch1:         0001-bootloader-plugin-support-for-photon.patch
Patch2:         0001-tuned-fix-bug-in-sysctl-verify.patch
Patch3:         0001-Schedule-perf-events-iff-scheduler-per-process-confi.patch
Patch4:         0001-realtime-Modify-hung_task-detection-param.patch
Vendor:         VMware, Inc.
Distribution:   Photon
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
%if %{with_check}
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

%package utils-systemtap
Summary:        Disk and net statistic monitoring systemtap scripts
Group:          System/Base
Requires:       %{name} = %{version}
Requires:       systemtap

%description utils-systemtap
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
make install DESTDIR=%{buildroot} %{?_smp_mflags}

# conditional support for grub2, grub2 is not available on all architectures
# and tuned is noarch package, thus the following hack is needed
mkdir -p %{buildroot}%{_datadir}/tuned/grub2
mv %{buildroot}%{_sysconfdir}/grub.d/00_tuned %{buildroot}%{_datadir}/tuned/grub2/00_tuned
rmdir %{buildroot}%{_sysconfdir}/grub.d
mkdir -p %{buildroot}%{_var}/lib/tuned
mkdir -p %{buildroot}%{_sysconfdir}/modprobe.d
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
%doc AUTHORS COPYING README
%{python3_sitelib}/tuned
%{_sbindir}/tuned
%{_sbindir}/tuned-adm
%{_libexecdir}/tuned
%{_sysconfdir}/tuned/active_profile
%config(noreplace) %{_sysconfdir}/modprobe.d/kvm.rt.tuned.conf
%config(noreplace) %{_sysconfdir}/tuned/tuned-main.conf
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/com.redhat.tuned.conf
%config(noreplace) %{_sysconfdir}/modprobe.d/tuned.conf
%config(noreplace) /boot/tuned.cfg
%config(noreplace) %{_sysconfdir}/tuned
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
*   Thu Oct 21 2021 Ankit Jain <ankitja@vmware.com> 2.15.0-3
-   realtime: modified hung_task detection sysctl param
-   to log D-state tasks
*   Thu Aug 12 2021 Keerthana K <keerthanak@vmware.com> 2.15.0-2
-   Schedule perf events iff scheduler per process configurations are set.
*   Thu Mar 25 2021 Ankit Jain <ankitja@vmware.com> 2.15.0-1
-   Update to latest version 2.15.0
*   Thu Jan 14 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 2.13.0-4
-   Add /var/lib/tuned folder to rpm
*   Mon Sep 14 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 2.13.0-3
-   sysctl plugin verify bug fix
*   Mon Aug 17 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 2.13.0-2
-   Bootloader plugin support for Photon
*   Wed Mar 18 2020 Tapas Kundu <tkundu@vmware.com> 2.13.0-1
-   Initial release.
