Summary:          systemd-239
Name:             systemd
Version:          239
Release:          47%{?dist}
License:          LGPLv2+ and GPLv2+ and MIT
URL:              http://www.freedesktop.org/wiki/Software/systemd/
Group:            System Environment/Security
Vendor:           VMware, Inc.
Distribution:     Photon

Source0:          %{name}-%{version}.tar.gz
%define sha512    %{name}=fd44590dfd148504c5ed1e67521efce50d84b627b7fc77015fa95dfa76d7a42297c56cc89eff40181809732024b16d48f2a87038cf435e0c63bc2b95ecd86b0f

Source1:          99-vmware-hotplug.rules
Source2:          50-security-hardening.conf
Source3:          systemd.cfg
Source4:          99-dhcp-en.network
Source5:          10-rdrand-rng.conf

Patch0:           01-enoX-uses-instance-number-for-vmware-hv.patch
Patch1:           02-install-general-aliases.patch
Patch2:           systemd-239-default-dns-from-env.patch
Patch3:           systemd-macros.patch
Patch4:           systemd-239-query-duid.patch
# Fix glibc-2.28 build issue. Checked in upstream after v239
Patch5:           systemd-239-glibc-build-fix.patch
Patch6:           systemd-239-revert-mtu.patch
Patch7:           systemd-239-CVE-2018-15688.patch
Patch8:           systemd-239-CVE-2018-15686.patch
Patch9:           systemd-239-CVE-2018-15687.patch
Patch10:          systemd-239-CVE-2018-16864.patch
Patch11:          systemd-239-CVE-2018-16865.patch
Patch12:          systemd-239-CVE-2018-16866.patch
Patch13:          systemd-239-CVE-2019-3842.patch
Patch14:          systemd-239-CVE-2019-6454.patch
Patch15:          systemd-239-CVE-2019-3833-3844.patch
Patch16:          systemd-239-CVE-2019-15718.patch
Patch17:          systemd-239-bz-2471962.patch
Patch18:          systemd-239-issue-962.patch
Patch19:          systemd-239-CVE-2019-20386.patch
Patch20:          shared-conf-parser-be-nice-and-ignore-lines-without.patch
Patch21:          systemd-239-bz-2527177.patch
Patch22:          ipv6ra-allow-to-ignore-addresses.patch
Patch23:          sd-bus-make-rqueue-wqueue-sizes-of-type-size_t.patch
Patch24:          sd-bus-reorder-bus-ref-and-bus-message-ref-handling.patch
Patch25:          sd-bus-make-sure-dispatch_rqueue-initializes-return-.patch
Patch26:          sd-bus-drop-two-inappropriate-empty-lines.patch
Patch27:          sd-bus-initialize-mutex-after-we-allocated-the-wqueu.patch
Patch28:          sd-bus-always-go-through-sd_bus_unref-to-free-messag.patch
Patch29:          bus-message-introduce-two-kinds-of-references-to-bus.patch
Patch30:          sd-bus-introduce-API-for-re-enqueuing-incoming-messa.patch
Patch31:          sd-event-add-sd_event_source_disable_unref-helper.patch
Patch32:          polkit-when-authorizing-via-PK-let-s-re-resolve-call.patch
Patch33:          services-shouldnot-start-if-there-is-residual-processes-left-over.patch
Patch34:          modify_systemd_watchdog_timeout.patch
Patch35:          detect-vmware-hypervisor.patch
Patch36:          safe-atou32-full.patch
Patch37:          systemd-239-CVE-2020-13776.patch
Patch38:          systemd-mount-fixes.patch
Patch39:          systemd-239-bz-2597079.patch
Patch40:          sd-bus-use-queue-message-references-for-managing-r-w.patch
Patch41:          network-make-Route.Type-support-local-broadcast-anyc.patch
Patch42:          ignore-classless-route-gateway.patch
Patch43:          increase-watchdog-tmo.patch
Patch44:          timedate-increment-reference-count-of-sd_bus_message.patch
Patch45:          timedate-defer-the-property-changed-signal-until-job.patch
Patch46:          systemd-239-CVE-2021-33910.patch
Patch47:          systemd-239-CVE-2020-13529.patch
Patch48:          bus-socket-Fix-line_begins-to-accept-word-matching-f.patch
Patch49:          sd-bus-make-bus_slot_disconnect-also-unref-the-slot-object.patch
Patch50:          meson-debug.patch
Patch51:          systemd-239-CVE-2022-2526.patch
Patch52:          systemd-239-CVE--2022-3821-time-util-fix-buffer-over-run.patch
Patch53:          CVE-2022-4415-1.patch
Patch54:          CVE-2022-4415-2.patch
Patch55:          CVE-2022-4415-3.patch
Patch56:          timedated-add-back-support-for-ntp-units.d.patch

Requires:         Linux-PAM
Requires:         libcap
Requires:         xz
Requires:         kmod
Requires:         glib
Requires:         libgcrypt
Requires:         filesystem >= 1.1
Requires:         elfutils
Requires:         gnutls
Requires:         libacl

BuildRequires:    intltool
BuildRequires:    gperf
BuildRequires:    libcap-devel
BuildRequires:    xz-devel
BuildRequires:    Linux-PAM-devel
BuildRequires:    XML-Parser
BuildRequires:    kbd
BuildRequires:    kmod-devel
BuildRequires:    util-linux-devel >= 2.30
BuildRequires:    libxslt
BuildRequires:    docbook-xsl
BuildRequires:    docbook-xml
BuildRequires:    glib-devel
BuildRequires:    meson
BuildRequires:    gettext
BuildRequires:    shadow
BuildRequires:    libgcrypt-devel
BuildRequires:    gnutls-devel
BuildRequires:    libacl-devel

%description
systemd is a system and service manager that runs as PID 1 and starts
the rest of the system. It provides aggressive parallelization
capabilities, uses socket and D-Bus activation for starting services,
offers on-demand starting of daemons, keeps track of processes using
Linux control groups, maintains mount and automount points, and
implements an elaborate transactional dependency-based service control
logic. systemd supports SysV and LSB init scripts and works as a
replacement for sysvinit. Other parts of this package are a logging daemon,
utilities to control basic system configuration like the hostname,
date, locale, maintain a list of logged-in users, system accounts,
runtime directories and settings, and daemons to manage simple network
configuration, network time synchronization, log forwarding, and name
resolution.

%package   devel
Summary:   Development headers for systemd
Requires:  %{name} = %{version}-%{release}
Requires:  glib-devel

%description devel
Development headers for developing applications linking to libsystemd

%package lang
Summary:   Language pack for systemd
Requires:  %{name} = %{version}-%{release}

%description lang
Language pack for systemd

%prep
%autosetup -p1
cat > config.cache << "EOF"
KILL=/bin/kill
HAVE_BLKID=1
BLKID_LIBS="-lblkid"
BLKID_CFLAGS="-I/usr/include/blkid"
cc_cv_CFLAGS__flto=no
EOF

sed -i "s#\#DefaultTasksMax=512#DefaultTasksMax=infinity#g" src/core/system.conf.in

%build
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
meson  --prefix %{_prefix}                                            \
       --sysconfdir /etc                                              \
       --localstatedir /var                                           \
       -Dblkid=true                                                   \
       -Dbuildtype=release                                            \
       -Ddefault-dnssec=no                                            \
       -Dfirstboot=false                                              \
       -Dinstall-tests=false                                          \
       -Dldconfig=false                                               \
       -Drootprefix=                                                  \
       -Drootlibdir=/lib                                              \
       -Dsplit-usr=true                                               \
       -Dsysusers=false                                               \
       -Dpam=true                                                     \
       -Dpolkit=true                                                  \
       -Ddbuspolicydir=/etc/dbus-1/system.d                           \
       -Ddbussessionservicedir=%{_prefix}/share/dbus-1/services       \
       -Ddbussystemservicedir=%{_prefix}/share/dbus-1/system-services \
       -Dsysvinit-path=/etc/rc.d/init.d                               \
       -Drc-local=/etc/rc.d/rc.local                                  \
       -Ddefault-dns-over-tls=opportunistic                           \
       -Ddns-over-tls=true                                            \
       -Dgnutls=true                                                  \
       -Dacl=true                                                     \
       $PWD build &&
       cd build &&
       %ninja_build

%install
cd build && %ninja_install

install -vdm 755 %{buildroot}/sbin
for tool in runlevel reboot shutdown poweroff halt telinit; do
     ln -sfv ../bin/systemctl %{buildroot}/sbin/${tool}
done
ln -sfv ../lib/systemd/systemd %{buildroot}/sbin/init
sed -i '/srv/d' %{buildroot}/usr/lib/tmpfiles.d/home.conf
sed -i "s:0775 root lock:0755 root root:g" %{buildroot}/usr/lib/tmpfiles.d/legacy.conf
sed -i "s:NamePolicy=kernel database onboard slot path:NamePolicy=kernel database:g" %{buildroot}/lib/systemd/network/99-default.link
sed -i "s:#LLMNR=yes:LLMNR=no:g" %{buildroot}%{_sysconfdir}/%{name}/resolved.conf
sed -i "s:#DNSSEC=no:DNSSEC=no:g" %{buildroot}%{_sysconfdir}/%{name}/resolved.conf
sed -i "s:#DNSOverTLS=opportunistic:DNSOverTLS=no:g" %{buildroot}%{_sysconfdir}/%{name}/resolved.conf
rm -f %{buildroot}%{_var}/log/README
mkdir -p %{buildroot}%{_localstatedir}/opt/journal/log
mkdir -p %{buildroot}%{_localstatedir}/log
ln -sfv %{_localstatedir}/opt/journal/log %{buildroot}%{_localstatedir}/log/journal

find %{buildroot} -name '*.la' -delete
install -Dm 0644 %{SOURCE1} %{buildroot}/%{_sysconfdir}/udev/rules.d
install -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysctl.d
install -dm 0755 %{buildroot}/boot/
install -m 0644 %{SOURCE3} %{buildroot}/boot/
rm %{buildroot}/lib/systemd/system/default.target
ln -sfv multi-user.target %{buildroot}/lib/systemd/system/default.target
install -dm 0755 %{buildroot}/%{_sysconfdir}/systemd/network
install -m 0644 %{SOURCE4} %{buildroot}/%{_sysconfdir}/systemd/network
%ifarch x86_64
install -m 0644 %{SOURCE5} %{buildroot}%{_sysconfdir}/modules-load.d
%endif
%find_lang %{name} ../%{name}.lang

%post
#we will restart services only while upgrade
if [ $1 -eq 2 ] ; then
    systemd-machine-id-setup &>/dev/null || :

    systemctl daemon-reexec &>/dev/null || {
        if [ $1 -gt 1 ] && [ -d /run/systemd/system ] ; then
            kill -TERM 1 &>/dev/null || :
        fi
    }

    journalctl --update-catalog &>/dev/null || :
    systemd-tmpfiles --create &>/dev/null || :
    udevadm hwdb --update &>/dev/null || :

    systemctl restart systemd-udevd.service systemd-udevd-kernel.socket systemd-udevd-control.socket
    systemctl restart systemd-logind.service
    systemctl restart systemd-networkd.service systemd-networkd.socket

fi
/sbin/ldconfig

%postun
/sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%dir %{_sysconfdir}/systemd
%dir %{_sysconfdir}/systemd/system
%dir %{_sysconfdir}/systemd/user
%dir %{_sysconfdir}/systemd/network
%dir %{_sysconfdir}/tmpfiles.d
%dir %{_sysconfdir}/sysctl.d
%dir %{_sysconfdir}/modules-load.d
%dir %{_sysconfdir}/binfmt.d
%{_sysconfdir}/X11/xinit/xinitrc.d/50-systemd-user.sh
%{_sysconfdir}/sysctl.d/50-security-hardening.conf
%{_sysconfdir}/xdg/systemd
%{_sysconfdir}/rc.d/init.d/README
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/org.freedesktop.systemd1.conf
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/org.freedesktop.hostname1.conf
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/org.freedesktop.login1.conf
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/org.freedesktop.locale1.conf
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/org.freedesktop.timedate1.conf
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/org.freedesktop.resolve1.conf
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/org.freedesktop.network1.conf
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/org.freedesktop.machine1.conf
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/org.freedesktop.portable1.conf
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/org.freedesktop.timesync1.conf
%config(noreplace) %{_sysconfdir}/systemd/system.conf
%config(noreplace) %{_sysconfdir}/systemd/user.conf
%config(noreplace) %{_sysconfdir}/systemd/logind.conf
%config(noreplace) %{_sysconfdir}/systemd/journald.conf
%config(noreplace) %{_sysconfdir}/systemd/resolved.conf
%config(noreplace) %{_sysconfdir}/systemd/coredump.conf
%config(noreplace) %{_sysconfdir}/systemd/timesyncd.conf
%config(noreplace) %{_sysconfdir}/pam.d/systemd-user
%ifarch x86_64
%config(noreplace) %{_sysconfdir}/modules-load.d/10-rdrand-rng.conf
%endif
%config(noreplace) %{_sysconfdir}/systemd/network/99-dhcp-en.network

%dir %{_sysconfdir}/udev
%dir %{_sysconfdir}/udev/rules.d
%dir %{_sysconfdir}/udev/hwdb.d
%{_sysconfdir}/udev/rules.d/99-vmware-hotplug.rules
%config(noreplace) %{_sysconfdir}/udev/udev.conf
%config(noreplace) /boot/systemd.cfg
%{_sysconfdir}/systemd/system/*
/lib/udev/*
/lib/systemd/systemd*
/lib/systemd/system-*
/lib/systemd/system/*
/lib/systemd/network/80-container*
/lib/systemd/*.so
/lib/systemd/resolv.conf
/lib/systemd/portablectl
%config(noreplace) /lib/systemd/network/99-default.link
%config(noreplace) /lib/systemd/ntp-units.d/80-%{name}-timesync.list
%config(noreplace) /lib/systemd/portable/profile/default/service.conf
%config(noreplace) /lib/systemd/portable/profile/nonetwork/service.conf
%config(noreplace) /lib/systemd/portable/profile/strict/service.conf
%config(noreplace) /lib/systemd/portable/profile/trusted/service.conf
%{_libdir}/environment.d/99-environment.conf
%exclude %dir %{_libdir}/debug
%exclude %{_datadir}/locale
%{_libdir}/binfmt.d
%{_libdir}/kernel
%{_libdir}/modules-load.d
%{_libdir}/rpm
/lib/security
%{_libdir}/sysctl.d
%{_libdir}/systemd
%{_libdir}/tmpfiles.d
/lib/*.so*
/lib/modprobe.d/systemd.conf
%{_bindir}/*
/bin/*
/sbin/*
%{_datadir}/bash-completion/*
%{_datadir}/factory/*
%{_datadir}/dbus-1
%{_datadir}/doc/*
%{_mandir}/man[1578]/*
%{_datadir}/polkit-1
%{_datadir}/systemd
%{_datadir}/zsh/*
%dir %{_localstatedir}/opt/journal/log
%{_localstatedir}/log/journal

%files devel
%dir %{_includedir}/systemd
/lib/libudev.so
/lib/libsystemd.so
%{_includedir}/systemd/*.h
%{_includedir}/libudev.h
%{_libdir}/pkgconfig/libudev.pc
%{_libdir}/pkgconfig/libsystemd.pc
%{_datadir}/pkgconfig/systemd.pc
%{_datadir}/pkgconfig/udev.pc
%{_mandir}/man3/*

%files lang -f %{name}.lang

%changelog
* Wed Mar 01 2023 Shivani Agarwal <shivania2@vmware.com> 239-47
- Add timedated back support for ntp units directory
* Mon Feb 13 2023 Shreenidhi Shedi <sshedi@vmware.com> 239-46
- Fix CVE-2022-4415
* Mon Nov 14 2022 Susant Sahani <ssahani@vmware.com> 239-45
- Fix CVE-2022-3821
* Tue Sep 20 2022 Mukul Sikka <msikka@vmware.com> 239-44
- Fix for CVE-2022-2526
* Tue Aug 09 2022 Shreenidhi Shedi <sshedi@vmware.com> 239-43
- meson: rename -Ddebug to -Ddebug-extra
* Mon Jul 04 2022 Shreenidhi Shedi <sshedi@vmware.com> 239-42
- Disable DNSSEC & DNSOverTLS by default
* Tue Jun 21 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 239-41
- Bump version as a part of libxslt upgrade
* Mon Jun 20 2022 Susant Sahani <ssahani@vmware.com> 239-40
- Enable ACL
* Thu May 05 2022 Alexey Makhalov <amakhalov@vmware.com> 239-39
- Fix memory leak in sd-bus.
* Wed May 4 2022 Michelle Wang <michellew@vmware.com> 239-38
- Update sha1 to sha512
* Thu Apr 28 2022 Susant Sahani <ssahani@vmware.com> 239-37
- Enable dns-over-tls
* Wed Feb 16 2022 Susant Sahani <ssahani@vmware.com> 239-36
- Enable default-dns-over-tls=opportunistic
* Sun Oct 03 2021 Susant Sahani <ssahani@vmware.com> 239-35
- Backport bus-socket: Fix line_begins() to accept word matching full string
* Wed Jul 21 2021 Susant Sahani <ssahani@vmware.com> 239-34
- Fix for CVE-2020-13529
* Thu Jul 15 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 239-33
- Fix for CVE-2021-33910
* Wed May 19 2021 Susant Sahani <ssahani@vmware.com> 239-32
- timedate: defer the property changed signal until job of
- starting/stopping NTP service is finished
* Tue Dec 22 2020 Shreenidhi Shedi <sshedi@vmware.com> 239-31
- Bump version as a part of autospec library upgrade
* Sat Nov 14 2020 Susant Sahani <ssahani@vmware.com> 239-30
- switch to autosetup
* Wed Sep 09 2020 Susant Sahani <ssahani@vmware.com> 239-29
- Increase WatchdogSec of systemd-journald, systemd-resolved and systemd-udevd
* Mon Aug 24 2020 Susant Sahani <ssahani@vmware.com> 239-28
- network - add option to ignore classless routes and GW
* Thu Jul 09 2020 Susant Sahani <ssahani@vmware.com> 239-27
- sd-bus: use "queue" message references for managing r/w message queus in connection objects
- Backport network - Route.Type
* Fri Jul 03 2020 Susant Sahani <ssahani@vmware.com> 239-26
- Fix BZ-2597079
* Tue Jun 23 2020 Harinadh Dommaraju <hdommaraju@vmware.com> 239-25
- mount fixes
* Sat Jun 06 2020 Susant Sahani <ssahani@vmware.com> 239-24
- Fix CVE-2020-13776
* Wed May 27 2020 Shreenidhi Shedi <sshedi@vmware.com> 239-23
- Added patch to detect vmware hypervisor
* Thu May 21 2020 Tapas Kundu <tkundu@vmware.com> 239-22
- systemd: services shouldn't start if there is residual processes left over
- Services restart after systemd update
- Increase watchdog timeout
* Mon Apr 13 2020 Susant Sahani <ssahani@vmware.com> 239-21
- Fix CVE-2020-1712
* Tue Mar 24 2020 Susant Sahani <ssahani@vmware.com> 239-20
- networkd: ipv6ra allow to ignore addresses
* Thu Mar 12 2020 Susant Sahani <ssahani@vmware.com> 239-19
- Don't treat syntax error as fatal, fix bz 2527776 and drop
- patch 16 as upstream dropped it.
* Tue Feb 04 2020 Susant Sahani <ssahani@vmware.com> 239-18
- Fix CVE-2019-20386
* Thu Jan 02 2020 Susant Sahani <ssahani@vmware.com> 239-17
- Fix If system has invalid hostname, systemd-networkd dhcpv4 does not run
- and obscure error message is also sligtly update generatedRoutingPolicyRule
* Fri Dec 06 2019 Susant Sahani <ssahani@vmware.com> 239-16
- Fix RoutingPolicyRule does not always apply - applies alternately.
* Mon Oct 28 2019 Piyush Gupta <guptapi@vmware.com> 239-15
- Added requires elfutils
* Wed Sep 11 2019 Susant Sahani <ssahani@vmware.com> 239-14
- Fix CVE-2019-15718
* Fri Jun 28 2019 Susant Sahani <ssahani@vmware.com> 239-13
- Fix BZ-2361840
* Fri Jun 28 2019 Susant Sahani <ssahani@vmware.com> 239-12
- Fix CVE-2019-6454, CVE-2019-3843 CVE-2019-3844
* Thu Apr 18 2019 Anish Swaminathan <anishs@vmware.com> 239-11
- Fix CVE-2019-3842
* Thu Jan 10 2019 Anish Swaminathan <anishs@vmware.com> 239-10
- Fix CVE-2018-16864, CVE-2018-16865, CVE-2018-16866
* Wed Jan 09 2019 Keerthana K <keerthanak@vmware.com> 239-9
- Seting default values for tcp_timestamps, tcp_challenge_ack_limit and ip_forward.
* Wed Jan 02 2019 Anish Swaminathan <anishs@vmware.com> 239-8
- Fix CVE-2018-15686, CVE-2018-15687
* Sun Nov 11 2018 Tapas Kundu <tkundu@vmware.com> 239-7
- Fix CVE-2018-15688
* Fri Oct 26 2018 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 239-6
- Auto-load rdrand-rng kernel module only on x86.
* Fri Oct 26 2018 Anish Swaminathan <anishs@vmware.com> 239-5
- Revert the commit that causes GCE networkd timeout
- https://github.com/systemd/systemd/commit/44b598a1c9d11c23420a5ef45ff11bcb0ed195eb
* Mon Oct 08 2018 Srinidhi Rao <srinidhir@vmware.com> 239-4
- Add glib-devel as a Requirement to systemd-devel
* Fri Sep 21 2018 Alexey Makhalov <amakhalov@vmware.com> 239-3
- Fix compilation issue against glibc-2.28
* Tue Sep 18 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 239-2
- Automatically load rdrand-rng kernel module on every boot.
* Tue Aug 28 2018 Anish Swaminathan <anishs@vmware.com> 239-1
- Update systemd to 239
* Wed Apr 11 2018 Xiaolin Li <xiaolinl@vmware.com> 236-3
- Build systemd with util-linux 2.32.
* Wed Jan 17 2018 Divya Thaluru <dthaluru@vmware.com> 236-2
- Fixed the log file directory structure
* Fri Dec 29 2017 Anish Swaminathan <anishs@vmware.com> 236-1
- Update systemd to 236
* Thu Nov 09 2017 Vinay Kulkarni <kulkarniv@vmware.com> 233-11
- Fix CVE-2017-15908 dns packet loop fix.
* Tue Nov 07 2017 Vinay Kulkarni <kulkarniv@vmware.com> 233-10
- Fix nullptr access during link disable.
* Mon Sep 18 2017 Anish Swaminathan <anishs@vmware.com> 233-9
- Backport router solicitation backoff from systemd 234
* Fri Sep 15 2017 Anish Swaminathan <anishs@vmware.com> 233-8
- Move network file to systemd package
* Tue Aug 15 2017 Alexey Makhalov <amakhalov@vmware.com> 233-7
- Fix compilation issue for glibc-2.26
* Fri Jul 21 2017 Vinay Kulkarni <kulkarniv@vmware.com> 233-6
- Fix for CVE-2017-1000082.
* Fri Jul 07 2017 Vinay Kulkarni <kulkarniv@vmware.com> 233-5
- Fix default-dns-from-env patch.
* Wed Jul 05 2017 Xiaolin Li <xiaolinl@vmware.com> 233-4
- Add kmod-devel to BuildRequires
* Thu Jun 29 2017 Vinay Kulkarni <kulkarniv@vmware.com> 233-3
- Fix for CVE-2017-9445.
* Tue Jun 20 2017 Anish Swaminathan <anishs@vmware.com> 233-2
- Fix for CVE-2017-9217
* Mon Mar 06 2017 Vinay Kulkarni <kulkarniv@vmware.com> 233-1
- Update systemd to 233
* Tue Jan 3 2017 Alexey Makhalov <amakhalov@vmware.com> 232-5
- Added /boot/systemd.cfg
* Tue Dec 20 2016 Alexey Makhalov <amakhalov@vmware.com> 232-4
- Fix initrd-switch-root issue
* Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> 232-3
- BuildRequires Linux-PAM-devel
* Thu Dec 01 2016 Xiaolin Li <xiaolinl@vmware.com> 232-2
- disable-elfutils.
* Fri Nov 18 2016 Anish Swaminathan <anishs@vmware.com> 232-1
- Update systemd to 232
* Thu Nov 3 2016 Divya Thaluru <dthaluru@vmware.com> 228-32
- Added logic to reload services incase of rpm upgrade
* Thu Sep 29 2016 Vinay Kulkarni <kulkarniv@vmware.com> 228-31
- Fix a CVE in systemd-notify socket.
* Mon Aug 29 2016 Alexey Makhalov <amakhalov@vmware.com> 228-30
- 02-install-general-aliases.patch to create absolute symlinks
* Fri Aug 26 2016 Anish Swaminathan <anishs@vmware.com> 228-29
- Change config file properties for 99-default.link
* Tue Aug 16 2016 Vinay Kulkarni <kulkarniv@vmware.com> 228-28
- systemd-resolved: Fix DNS_TRANSACTION_PENDING assert.
* Mon Aug 1 2016 Divya Thaluru <dthaluru@vmware.com> 228-27
- Removed packaging of symlinks and will be created during installation
* Tue Jul 12 2016 Vinay Kulkarni <kulkarniv@vmware.com> 228-26
- systemd-resolved: Fix DNS domains resolv.conf search issue for static DNS.
* Mon Jul 11 2016 Vinay Kulkarni <kulkarniv@vmware.com> 228-25
- systemd-networkd: Update DUID/IAID config interface to systemd v230 spec.
* Tue Jun 21 2016 Anish Swaminathan <anishs@vmware.com> 228-24
- Change config file properties
* Fri Jun 17 2016 Vinay Kulkarni <kulkarniv@vmware.com> 228-23
- systemd-resolved: Configure initial DNS servers from environment var.
* Mon Jun 06 2016 Alexey Makhalov <amakhalov@vmware.com> 228-22
- systemd-resolved: disable LLMNR
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 228-21
- GA - Bump release of all rpms
* Tue May 17 2016 Anish Swaminathan <anishs@vmware.com> 228-20
- Added patch for letting kernel handle ndisc
* Tue May 17 2016 Divya Thaluru <dthaluru@vmware.com> 228-19
- Updated systemd-user PAM configuration
* Mon May 16 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 228-18
- Updated the MaxTasks to infinity in system.conf file
* Thu Apr 21 2016 Mahmoud Bassiouny <mbassiouny@vmware.com> 228-17
- Set the default.target to the multi-user.target
* Tue Apr 12 2016 Vinay Kulkarni <kulkarniv@vmware.com> 228-16
- Disable network interface renaming.
* Thu Mar 31 2016 Vinay Kulkarni <kulkarniv@vmware.com> 228-15
- Patch to query DHCP DUID, IAID.f
* Wed Mar 30 2016 Vinay Kulkarni <kulkarniv@vmware.com> 228-14
- Update DHCP DUID, IAID configuration patch.
* Wed Mar 30 2016 Kumar Kaushik <kaushikk@vmware.com> 228-13
- Install the security hardening script as part of systemd.
* Tue Mar 29 2016 Kumar Kaushik <kaushikk@vmware.com> 228-12
- Added patch for timedatectl /etc/adjtime PR2749.
* Fri Mar 11 2016 Anish Swaminathan <anishs@vmware.com> 228-11
- Added patch for dhcp preservation via duid iaid configurability
* Fri Mar 11 2016 Anish Swaminathan <anishs@vmware.com> 228-10
- Added patch for swap disconnect order
* Thu Mar 10 2016 XIaolin Li <xiaolinl@vmware.com> 228-9
- Enable manpages.
* Fri Feb 19 2016 Anish Swaminathan <anishs@vmware.com> 228-8
- Added patch to get around systemd-networkd wait online timeout
* Sat Feb 06 2016 Alexey Makhalov <amakhalov@vmware.com> 228-7
- Added patch: fix-reading-routes.
* Wed Feb 03 2016 Anish Swaminathan <anishs@vmware.com> 228-6
- Add hotplug udev rules.
* Tue Jan 12 2016 Anish Swaminathan <anishs@vmware.com> 228-5
- Change config file attributes.
* Wed Jan 06 2016 Anish Swaminathan <anishs@vmware.com> 228-4
- Patches for minor network fixes.
* Wed Dec 16 2015 Anish Swaminathan <anishs@vmware.com> 228-3
- Patch for ostree.
* Wed Dec 16 2015 Anish Swaminathan <anishs@vmware.com> 228-2
- Patch for loopback address.
* Fri Dec 11 2015 Anish Swaminathan <anishs@vmware.com> 228-1
- Upgrade systemd version.
* Mon Nov 30 2015 Mahmoud Bassiouny <mbassiouny@vmware.com> 216-13
- Removing the reference of lock user
* Fri Oct 9 2015 Xiaolin Li <xiaolinl@vmware.com> 216-12
- Removing la files from packages.
* Fri Sep 18 2015 Divya Thaluru <dthaluru@vmware.com> 216-11
- Packaging journal log directory
* Thu Sep 10 2015 Alexey Makhalov <amakhalov@vmware.com> 216-10
- Improve enoX renaming in VMware HV case. Patch is added.
* Tue Aug 25 2015 Alexey Makhalov <amakhalov@vmware.com> 216-9
- Reduce systemd-networkd boot time (exclude if-rename patch).
* Mon Jul 20 2015 Divya Thaluru <dthaluru@vmware.com> 216-8
- Adding sysvinit support
* Mon Jul 06 2015 Kumar Kaushik <kaushikk@vmware.com> 216-7
- Fixing networkd/udev race condition for renaming interface.
* Thu Jun 25 2015 Sharath George <sharathg@vmware.com> 216-6
- Remove debug files.
* Tue Jun 23 2015 Divya Thaluru <dthaluru@vmware.com> 216-5
- Building compat libs
* Mon Jun 1 2015 Alexey Makhalov <amakhalov@vmware.com> 216-4
- gudev support
* Wed May 27 2015 Divya Thaluru <dthaluru@vmware.com> 216-3
- Removing packing of PAM configuration files
* Mon May 18 2015 Touseef Liaqat <tliaqat@vmware.com> 216-2
- Update according to UsrMove.
* Mon Oct 27 2014 Sharath George <sharathg@vmware.com> 216-1
- Initial build. First version
