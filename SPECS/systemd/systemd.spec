Name:             systemd
URL:              http://www.freedesktop.org/wiki/Software/systemd/
Version:          247.6
Release:          2%{?dist}
License:          LGPLv2+ and GPLv2+ and MIT
Summary:          System and Service Manager

Group:            System Environment/Security
Vendor:           VMware, Inc.
Distribution:     Photon

Source0:          https://github.com/systemd/systemd-stable/archive/%{name}-stable-%{version}.tar.gz
%define sha1      systemd=30af650e8cf2109cb2cf1a4ae2025e5ac939cceb
Source1:          99-vmware-hotplug.rules
Source2:          50-security-hardening.conf
Source3:          systemd.cfg
Source4:          99-dhcp-en.network
Source5:          10-rdrand-rng.conf
Source6:          10-defaults.preset

Patch0:           systemd-247-enoX-uses-instance-number-for-vmware-hv.patch
Patch1:           systemd-247-default-dns-from-env.patch
Patch2:           timesync-Make-delaying-attempts-to-contact-servers-c.patch
Patch3:           CVE-2021-33910.patch

Requires:         Linux-PAM
Requires:         bzip2
Requires:         curl
Requires:         elfutils
Requires:         filesystem >= 1.1
Requires:         glib
Requires:         gnutls
Requires:         kmod
Requires:         %{name}-pam = %{version}-%{release}
Requires:         %{name}-rpm-macros = %{version}-%{release}
Requires:         %{name}-libs = %{version}-%{release}
Requires:         libacl
Requires:         libcap
Requires:         libgcrypt
Requires:         libmicrohttpd
Requires:         libseccomp
Requires:         libselinux
Requires:         lz4
Requires:         pcre
Requires:         xz

BuildRequires:   bzip2-devel
BuildRequires:   curl-devel
BuildRequires:   docbook-xml
BuildRequires:   docbook-xsl
BuildRequires:   gettext
BuildRequires:   glib-devel
BuildRequires:   gnutls-devel
BuildRequires:   gperf
BuildRequires:   intltool
BuildRequires:   kbd
BuildRequires:   kmod-devel
BuildRequires:   libacl-devel
BuildRequires:   libcap-devel
BuildRequires:   libgcrypt-devel
BuildRequires:   libseccomp
BuildRequires:   libseccomp-devel
BuildRequires:   libselinux-devel
BuildRequires:   libxslt
BuildRequires:   Linux-PAM-devel
BuildRequires:   lz4-devel
BuildRequires:   meson
BuildRequires:   libmicrohttpd-devel
BuildRequires:   ninja-build
BuildRequires:   openssl-devel
BuildRequires:   pcre-devel
BuildRequires:   pkg-config
BuildRequires:   python3-devel
BuildRequires:   python3-lxml
BuildRequires:   shadow
BuildRequires:   util-linux-devel
BuildRequires:   XML-Parser
BuildRequires:   xz
BuildRequires:   xz-devel
BuildRequires:   zlib-devel
# rpmbuild needs /lib/rpm/macros.d/macros.systemd in order to expand %systemd_* actions.
# systemd-rpm-macros is not build yet, so consume it from publishrpms, similarly to as
# openjdk does it for Vivace rpms.
# Other packages using %system_* pre/post actions must use "BuildRequires: systemd-rpm-macros"
%define ExtraBuildRequires systemd-rpm-macros

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

%package libs
Summary:        systemd libraries
License:        LGPLv2+ and MIT
Provides:       nss-myhostname = 0.4
Requires(post): coreutils
Requires(post): sed
Requires(post): grep

%description libs
Libraries for systemd and udev.

%package pam
Summary:        systemd PAM module
Requires:       %{name} = %{version}-%{release}

%description pam
Systemd PAM module registers the session with systemd-logind.

%package rpm-macros
Summary:        Macros that define paths and scriptlets related to systemd
BuildArch:      noarch

%description rpm-macros
Just the definitions of rpm macros.

%package devel
Summary:        Development headers for systemd
Requires:       %{name}-libs = %{version}-%{release}
Requires:       %{name}-pam = %{version}-%{release}
Requires:       glib-devel
Provides:       libudev-devel = %{version}

%description devel
Development headers for developing applications linking to libsystemd

%package udev
Summary: Rule-based device node and kernel event manager
License:        LGPLv2+

Requires:       %{name} = %{version}-%{release}
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd
Requires(post):   grep
Requires:         kmod
Provides:         udev = %{version}

%description udev
This package contains systemd-udev and the rules and hardware database
needed to manage device nodes. This package is necessary on physical
machines and in virtual machines, but not in containers.

%package container
Summary: Tools for containers and VMs
Requires:       %{name} = %{version}-%{release}
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd
License:          LGPLv2+

%description container
Systemd tools to spawn and manage containers and virtual machines.

This package contains systemd-nspawn, machinectl, systemd-machined,
and systemd-importd.

%package journal-remote
Summary:        Tools to send journal events over the network
Requires:       %{name} = %{version}-%{release}
License:        LGPLv2+
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd
Requires:         libmicrohttpd
Provides:         systemd-journal-gateway = %{version}-%{release}

%description journal-remote
Programs to forward journal entries over the network, using encrypted HTTP,
and to write journal files from serialized journal contents.

This package contains systemd-journal-gatewayd,
systemd-journal-remote, and systemd-journal-upload.

%package lang
Summary:        Language pack for systemd
Requires:       %{name} = %{version}-%{release}

%description lang
Language pack for systemd

%package tests
Summary:       Internal unit tests for systemd
Requires:      %{name} = %{version}-%{release}
License:       LGPLv2+

%description tests
"Installed tests" that are usually run as part of the build system.
They can be useful to test systemd internals.

%prep
%autosetup -n %{name}-stable-%{version} -p1

sed -i "s#\#DefaultTasksMax=512#DefaultTasksMax=infinity#g" src/core/system.conf.in

%build
if [ %{_host} != %{_build} ]; then
CPU_FAMILY=""
test %{_arch} == "aarch64" && CPU_FAMILY="aarch64"
test %{_arch} == "i686" && CPU_FAMILY="x86"

cat > cross-compile-config.txt << EOF
[binaries]
c = '%{_host}-gcc'
cpp = '%{_host}-g++'
ar = '%{_host}-ar'
ld = '%{_host}-ld'
ranlib = '%{_host}-ranlib'
strip = '%{_host}-strip'
pkgconfig = '%{_host}-pkg-config'

[properties]
needs_exe_wrapper = true
c_args = ['--sysroot=/target-%{_arch}']
cpp_args = ['--sysroot=/target-%{_arch}']
c_link_args = ['-lssp']
cpp_link_args = ['-lssp']

[host_machine]
system = 'linux'
cpu_family = '$CPU_FAMILY'
cpu = '%{_arch}'
endian = 'little'
EOF

  CROSS_COMPILE_CONFIG="--cross-file ./cross-compile-config.txt"
else
  CROSS_COMPILE_CONFIG=
fi

CONFIGURE_OPTS=(
       --prefix=%{_prefix}
       -Dmode=release
       -Dkmod=true
       -Duser-path=/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin
       -Dservice-watchdog=
       -Dblkid=true
       -Dseccomp=true
       -Ddefault-dnssec=no
       -Dfirstboot=false
       -Dinstall-tests=false
       -Dldconfig=false
       -Dxz=true
       -Dzlib=true
       -Dbzip2=true
       -Dlz4=true
       -Dacl=true
       -Dsmack=true
       -Dgcrypt=true
       -Dsplit-usr=true
       -Dsysusers=false
       -Dpam=true
       -Dpolkit=true
       -Dselinux=true
       -Dlibcurl=true
       -Dgnutls=true
       -Dopenssl=true
       -Db_ndebug=false
       -Dhwdb=true
       -Ddefault-kill-user-processes=false
       -Dtests=unsafe
       -Dinstall-tests=true
       -Dnobody-user=nobody
       -Dnobody-group=nobody
       -Dsplit-usr=false
       -Dsplit-bin=true
       -Db_lto=true
       -Db_ndebug=false
       -Ddefault-hierarchy=hybrid
       -Dsysvinit-path=/etc/rc.d/init.d
       -Drc-local=/etc/rc.d/rc.local
       -Dfallback-hostname=photon
       -Doomd=false
       -Dhomed=false
       -Dversion-tag=v%{version}-%{release}
       $CROSS_COMPILE_CONFIG
)

export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8

meson build ${CONFIGURE_OPTS[@]}
ninja -C build

%install
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
DESTDIR=%{buildroot} ninja -C build install

sed -i '/srv/d' %{buildroot}/usr/lib/tmpfiles.d/home.conf
sed -i "s:0775 root lock:0755 root root:g" %{buildroot}/usr/lib/tmpfiles.d/legacy.conf
sed -i "s:NamePolicy=kernel database onboard slot path:NamePolicy=kernel database:g" %{buildroot}/usr/lib/systemd/network/99-default.link
sed -i "s:#LLMNR=yes:LLMNR=false:g" %{buildroot}/etc/systemd/resolved.conf

rm -f %{buildroot}%{_var}/log/README
mkdir -p %{buildroot}%{_localstatedir}/opt/journal/log
mkdir -p %{buildroot}%{_localstatedir}/log
ln -sfv %{_localstatedir}/opt/journal/log %{buildroot}%{_localstatedir}/log/journal

find %{buildroot} -name '*.la' -delete
install -Dm 0644 %{SOURCE1} %{buildroot}/%{_sysconfdir}/udev/rules.d
install -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysctl.d
install -dm 0755 %{buildroot}/boot/
install -m 0644 %{SOURCE3} %{buildroot}/boot/
install -dm 0755 %{buildroot}/%{_sysconfdir}/systemd/network
install -m 0644 %{SOURCE4} %{buildroot}/%{_sysconfdir}/systemd/network
install -m 0644 %{SOURCE6} %{buildroot}/%{_libdir}/systemd/system-preset

rm %{buildroot}/usr/lib/systemd/system/default.target
ln -sfv multi-user.target %{buildroot}/usr/lib/systemd/system/default.target

%ifarch x86_64
install -m 0644 %{SOURCE5} %{buildroot}%{_sysconfdir}/modules-load.d
%endif
%find_lang %{name} ../%{name}.lang

%post
systemd-machine-id-setup &>/dev/null || :

systemctl daemon-reexec &>/dev/null || {
    if [ $1 -gt 1 ] && [ -d /run/systemd/system ] ; then
        kill -TERM 1 &>/dev/null || :
    fi
}

journalctl --update-catalog &>/dev/null || :
systemd-tmpfiles --create &>/dev/null || :

if [ $1 -eq 1 ] ; then
        systemctl preset-all &>/dev/null || :
        systemctl --global preset-all &>/dev/null || :
fi

%clean
rm -rf %{buildroot}/*

%global udev_services systemd-udevd.service systemd-udev-settle.service systemd-udev-trigger.service systemd-udevd-control.socket systemd-udevd-kernel.socket systemd-timesyncd.service

%post udev
udevadm hwdb --update &>/dev/null || :

%systemd_post %udev_services

%preun udev
%systemd_preun %udev_services

%postun udev
%systemd_postun_with_restart systemd-udevd.service

%files
%defattr(-,root,root)
%dir %{_sysconfdir}/systemd
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

%config(noreplace) %{_sysconfdir}/systemd/sleep.conf
%config(noreplace) %{_sysconfdir}/systemd/system.conf
%config(noreplace) %{_sysconfdir}/systemd/user.conf
%config(noreplace) %{_sysconfdir}/systemd/logind.conf
%config(noreplace) %{_sysconfdir}/systemd/journald.conf
%config(noreplace) %{_sysconfdir}/systemd/resolved.conf
%config(noreplace) %{_sysconfdir}/systemd/coredump.conf
%config(noreplace) %{_sysconfdir}/systemd/timesyncd.conf
%config(noreplace) %{_sysconfdir}/systemd/networkd.conf
%config(noreplace) %{_sysconfdir}/systemd/pstore.conf

%ifarch x86_64
%config(noreplace) %{_sysconfdir}/modules-load.d/10-rdrand-rng.conf
%endif
%config(noreplace) %{_sysconfdir}/systemd/network/99-dhcp-en.network

%config(noreplace) /boot/systemd.cfg

%{_sbindir}/halt
%{_sbindir}/init
%{_sbindir}/poweroff
%{_sbindir}/reboot
%{_sbindir}/runlevel
%{_sbindir}/shutdown
%{_sbindir}/telinit
%{_sbindir}/resolvconf

%{_bindir}/busctl
%{_bindir}/coredumpctl
%{_bindir}/hostnamectl
%{_bindir}/journalctl
%{_bindir}/localectl
%{_bindir}/loginctl
%{_bindir}/networkctl
%{_bindir}/portablectl
%{_bindir}/resolvectl
%{_bindir}/systemctl
%{_bindir}/systemd-analyze
%{_bindir}/systemd-ask-password
%{_bindir}/systemd-cat
%{_bindir}/systemd-cgls
%{_bindir}/systemd-cgtop
%{_bindir}/systemd-delta
%{_bindir}/systemd-detect-virt
%{_bindir}/systemd-escape
%{_bindir}/systemd-id128
%{_bindir}/systemd-inhibit
%{_bindir}/systemd-machine-id-setup
%{_bindir}/systemd-mount
%{_bindir}/systemd-notify
%{_bindir}/systemd-path
%{_bindir}/systemd-resolve
%{_bindir}/systemd-run
%{_bindir}/systemd-socket-activate
%{_bindir}/systemd-stdio-bridge
%{_bindir}/systemd-tmpfiles
%{_bindir}/systemd-tty-ask-password-agent
%{_bindir}/systemd-umount
%{_bindir}/timedatectl
%{_bindir}/userdbctl
%{_bindir}/systemd-repart
%{_bindir}/systemd-dissect

%{_libdir}/tmpfiles.d/etc.conf
%{_libdir}/tmpfiles.d/home.conf
%{_libdir}/tmpfiles.d/journal-nocow.conf
%{_libdir}/tmpfiles.d/legacy.conf
%{_libdir}/tmpfiles.d/portables.conf
%{_libdir}/tmpfiles.d/static-nodes-permissions.conf
%{_libdir}/tmpfiles.d/systemd-nologin.conf
%{_libdir}/tmpfiles.d/systemd-tmp.conf
%{_libdir}/tmpfiles.d/systemd.conf
%{_libdir}/tmpfiles.d/tmp.conf
%{_libdir}/tmpfiles.d/var.conf
%{_libdir}/tmpfiles.d/x11.conf

%{_libdir}/environment.d/99-environment.conf
%exclude %{_datadir}/locale
%{_libdir}/binfmt.d
%{_libdir}/rpm
%{_libdir}/sysctl.d
%{_libdir}/systemd

%{_datadir}/bash-completion/*
%{_datadir}/factory/*
%{_datadir}/dbus-1
%{_datadir}/doc/*
%{_datadir}/polkit-1
%{_datadir}/systemd
%{_datadir}/zsh/*
%{_localstatedir}/log/journal

%ghost %dir %attr(0755,-,-) /etc/systemd/system/basic.target.wants
%ghost %dir %attr(0755,-,-) /etc/systemd/system/bluetooth.target.wants
%ghost %dir %attr(0755,-,-) /etc/systemd/system/default.target.wants
%ghost %dir %attr(0755,-,-) /etc/systemd/system/getty.target.wants
%ghost %dir %attr(0755,-,-) /etc/systemd/system/graphical.target.wants
%ghost %dir %attr(0755,-,-) /etc/systemd/system/local-fs.target.wants
%ghost %dir %attr(0755,-,-) /etc/systemd/system/machines.target.wants
%ghost %dir %attr(0755,-,-) /etc/systemd/system/multi-user.target.wants
%ghost %dir %attr(0755,-,-) /etc/systemd/system/network-online.target.wants
%ghost %dir %attr(0755,-,-) /etc/systemd/system/printer.target.wants
%ghost %dir %attr(0755,-,-) /etc/systemd/system/remote-fs.target.wants
%ghost %dir %attr(0755,-,-) /etc/systemd/system/sockets.target.wants
%ghost %dir %attr(0755,-,-) /etc/systemd/system/sysinit.target.wants
%ghost %dir %attr(0755,-,-) /etc/systemd/system/system-update.target.wants
%ghost %dir %attr(0755,-,-) /etc/systemd/system/timers.target.wants
%ghost %dir %attr(0755,-,-) /etc/systemd/system

%files devel
%defattr(-,root,root)
%dir %{_includedir}/systemd
%{_libdir}/libudev.so
%{_libdir}/libsystemd.so
%{_includedir}/systemd/*.h
%{_includedir}/libudev.h
%{_libdir}/pkgconfig/libudev.pc
%{_libdir}/pkgconfig/libsystemd.pc
%{_datadir}/pkgconfig/systemd.pc
%{_datadir}/pkgconfig/udev.pc

%files udev
%defattr(-,root,root)
%dir %{_sysconfdir}/udev
%{_sysconfdir}/udev/rules.d/99-vmware-hotplug.rules
%dir %{_sysconfdir}/kernel
%dir %{_sysconfdir}/modules-load.d
%{_sysconfdir}/systemd/pstore.conf
%{_sysconfdir}/systemd/sleep.conf
%{_sysconfdir}/systemd/timesyncd.conf
%{_sysconfdir}/udev/udev.conf
%{_libdir}/tmpfiles.d/systemd-pstore.conf
%{_bindir}/bootctl
%{_bindir}/kernel-install
%{_bindir}/systemd-hwdb
%{_bindir}/udevadm

%{_libdir}/udev/v4l_id
%{_libdir}/kernel
%{_libdir}/modprobe.d
%{_libdir}/modules-load.d
%{_libdir}/systemd/network/99-default.link
%{_libdir}/systemd/ntp-units.d/80-systemd-timesync.list
%{_libdir}/systemd/system-generators/systemd-bless-boot-generator
%{_libdir}/systemd/system-generators/systemd-hibernate-resume-generator
%{_libdir}/systemd/system-sleep
%{_libdir}/systemd/system/hibernate.target
%{_libdir}/systemd/system/hybrid-sleep.target
%{_libdir}/systemd/system/initrd-udevadm-cleanup-db.service
%{_libdir}/systemd/system/kmod-static-nodes.service
%{_libdir}/systemd/system/quotaon.service
%{_libdir}/systemd/system/sleep.target
%{_libdir}/systemd/system/sockets.target.wants/systemd-udevd-control.socket
%{_libdir}/systemd/system/sockets.target.wants/systemd-udevd-kernel.socket
%{_libdir}/systemd/system/suspend-then-hibernate.target
%{_libdir}/systemd/system/suspend.target
%{_libdir}/systemd/system/sysinit.target.wants/kmod-static-nodes.service
%{_libdir}/systemd/system/sysinit.target.wants/systemd-boot-system-token.service
%{_libdir}/systemd/system/sysinit.target.wants/systemd-hwdb-update.service
%{_libdir}/systemd/system/sysinit.target.wants/systemd-modules-load.service
%{_libdir}/systemd/system/sysinit.target.wants/systemd-random-seed.service
%{_libdir}/systemd/system/sysinit.target.wants/systemd-tmpfiles-setup-dev.service
%{_libdir}/systemd/system/sysinit.target.wants/systemd-udevd.service
%{_libdir}/systemd/system/systemd-backlight@.service
%{_libdir}/systemd/system/systemd-bless-boot.service
%{_libdir}/systemd/system/systemd-boot-system-token.service
%{_libdir}/systemd/system/systemd-fsck-root.service
%{_libdir}/systemd/system/systemd-fsck@.service
%{_libdir}/systemd/system/systemd-hibernate-resume@.service
%{_libdir}/systemd/system/systemd-hibernate.service
%{_libdir}/systemd/system/systemd-hwdb-update.service
%{_libdir}/systemd/system/systemd-hybrid-sleep.service
%{_libdir}/systemd/system/systemd-modules-load.service
%{_libdir}/systemd/system/systemd-pstore.service
%{_libdir}/systemd/system/systemd-quotacheck.service
%{_libdir}/systemd/system/systemd-random-seed.service
%{_libdir}/systemd/system/systemd-remount-fs.service
%{_libdir}/systemd/system/systemd-rfkill.service
%{_libdir}/systemd/system/systemd-rfkill.socket
%{_libdir}/systemd/system/systemd-suspend-then-hibernate.service
%{_libdir}/systemd/system/systemd-suspend.service
%{_libdir}/systemd/system/systemd-timesyncd.service
%{_libdir}/systemd/system/systemd-tmpfiles-setup-dev.service
%{_libdir}/systemd/system/systemd-udev-settle.service
%{_libdir}/systemd/system/systemd-udevd-control.socket
%{_libdir}/systemd/system/systemd-udevd-kernel.socket
%{_libdir}/systemd/system/systemd-udevd.service
%{_libdir}/systemd/system/systemd-vconsole-setup.service
%{_libdir}/systemd/system/systemd-volatile-root.service
%{_libdir}/systemd/systemd-backlight
%{_libdir}/systemd/systemd-bless-boot
%{_libdir}/systemd/systemd-fsck
%{_libdir}/systemd/systemd-growfs
%{_libdir}/systemd/systemd-hibernate-resume
%{_libdir}/systemd/systemd-makefs
%{_libdir}/systemd/systemd-modules-load
%{_libdir}/systemd/systemd-pstore
%{_libdir}/systemd/systemd-quotacheck
%{_libdir}/systemd/systemd-random-seed
%{_libdir}/systemd/systemd-remount-fs
%{_libdir}/systemd/systemd-rfkill
%{_libdir}/systemd/systemd-sleep
%{_libdir}/systemd/systemd-timesyncd
%{_libdir}/systemd/systemd-udevd
%{_libdir}/systemd/systemd-vconsole-setup
%{_libdir}/systemd/systemd-volatile-root

%dir %{_libdir}/udev
%{_libdir}/udev/ata_id
%{_libdir}/udev/cdrom_id
%{_libdir}/udev/fido_id

%dir %{_libdir}/udev/hwdb.d
%{_libdir}/udev/hwdb.d/*
%{_libdir}/udev/mtd_probe

%dir %{_libdir}/udev/rules.d
%{_libdir}/udev/rules.d/*
%{_libdir}/udev/scsi_id

%{_datadir}/bash-completion/completions/bootctl
%{_datadir}/bash-completion/completions/kernel-install
%{_datadir}/bash-completion/completions/udevadm

%{_datadir}/dbus-1/system-services/org.freedesktop.timesync1.service
%{_datadir}/dbus-1/system.d/org.freedesktop.timesync1.conf

%{_datadir}/zsh/site-functions/_bootctl
%{_datadir}/zsh/site-functions/_kernel-install
%{_datadir}/zsh/site-functions/_udevadm

%files libs
%defattr(-,root,root)
%{_libdir}/libnss_myhostname.so.2
%{_libdir}/libnss_mymachines.so.2
%{_libdir}/libnss_resolve.so.2
%{_libdir}/libnss_systemd.so.2
%{_libdir}/libsystemd.so.0
%{_libdir}/libsystemd.so.0.30.0
%{_libdir}/libudev.so.1.7.0
%{_libdir}/libudev.so.1

%files pam
%defattr(-,root,root)
%{_libdir}/security/pam_systemd.so
%{_libdir}/pam.d/systemd-user

%files container
%defattr(-,root,root)
%{_bindir}/systemd-nspawn
%{_bindir}/machinectl

%{_libdir}/systemd/systemd-machined
%{_libdir}/systemd/system/systemd-machined.service
%{_libdir}/systemd/system/systemd-nspawn@.service
%{_libdir}/systemd/system/dbus-org.freedesktop.machine1.service
%{_libdir}/systemd/system/var-lib-machines.mount
%{_libdir}/systemd/system/machine.slice
%{_libdir}/systemd/system/machines.target.wants
%{_libdir}/tmpfiles.d/systemd-nspawn.conf

%{_datadir}/dbus-1/system.d/org.freedesktop.machine1.conf
%{_datadir}/dbus-1/system-services/org.freedesktop.machine1.service
%{_datadir}/polkit-1/actions/org.freedesktop.machine1.policy

%files journal-remote
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/systemd/journal-upload.conf
%config(noreplace) %{_sysconfdir}/systemd/journal-remote.conf

%{_libdir}/systemd/systemd-journal-gatewayd
%{_libdir}/systemd/systemd-journal-remote
%{_libdir}/systemd/systemd-journal-upload

%{_libdir}/systemd/system/systemd-journal-gatewayd.service
%{_libdir}/systemd/system/systemd-journal-gatewayd.socket
%{_libdir}/systemd/system/systemd-journal-remote.service
%{_libdir}/systemd/system/systemd-journal-remote.socket
%{_libdir}/systemd/system/systemd-journal-upload.service

%files rpm-macros
%{_libdir}/rpm/macros.d

%files tests
%{_libdir}/systemd/tests

%files lang -f ../%{name}.lang

%changelog
*    Fri Jul 16 2021 Him Kalyan Bordoloi <bordoloih@vmware.com>  247.6-2
-    Fix for CVE-2021-33910
*    Tue Mar 30 2021 Susant Sahani <ssahani@vmware.com>  247.6-1
-    Add systemd-rpm-macros to extra build requires and update version
*    Tue Mar 16 2021 Susant Sahani <ssahani@vmware.com>  247.4-1
-    Version bump and fix udev preun macro
*    Wed Feb 03 2021 Susant Sahani <ssahani@vmware.com>  247.3-1
-    Version bump
*    Mon Jan 04 2021 Susant Sahani <ssahani@vmware.com>  247.2-2
-    Backport timesync: ConnectionRetrySec=
*    Thu Dec 17 2020 Susant Sahani <ssahani@vmware.com>  247.2-1
-    Upgrade to 247.2
-    Enable openssl and drop systemd-oomd
*    Mon Dec 14 2020 Susant Sahani <ssahani@vmware.com>  247-1
-    Upgrade to 247
-    Split out systemd package to multiple packages
*    Tue Oct 27 2020 Susant Sahani <ssahani@vmware.com>  245.5-3
-    util: return the correct correct wd from inotify helpers
*    Sun Aug 16 2020 Susant Sahani <ssahani@vmware.com>  245.5-2
-    Drop meson macro
*    Tue May 12 2020 Susant Sahani <ssahani@vmware.com>  245.5-1
-    Update to version 245.5 stable
*    Mon May 04 2020 Alexey Makhalov <amakhalov@vmware.com> 239-14
-    Fix compilation issue with gcc-8.4.0
-    Build with debug info.
*    Sat Apr 18 2020 Alexey Makhalov <amakhalov@vmware.com> 239-13
-    Enable SELinux support
*    Thu Oct 31 2019 Alexey Makhalov <amakhalov@vmware.com> 239-12
-    Cross compilation support
*    Tue Oct 22 2019 Piyush Gupta <guptapi@vmware.com>  239-11
-    Added requires elfutils
*    Thu Jan 10 2019 Anish Swaminathan <anishs@vmware.com>  239-10
-    Fix CVE-2018-16864, CVE-2018-16865, CVE-2018-16866
*    Wed Jan 09 2019 Keerthana K <keerthanak@vmware.com> 239-9
-    Seting default values for tcp_timestamps, tcp_challenge_ack_limit and ip_forward.
*    Wed Jan 02 2019 Anish Swaminathan <anishs@vmware.com>  239-8
-    Fix CVE-2018-15686, CVE-2018-15687
*    Sun Nov 11 2018 Tapas Kundu <tkundu@vmware.com> 239-7
-    Fix CVE-2018-15688
*    Fri Oct 26 2018 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 239-6
-    Auto-load rdrand-rng kernel module only on x86.
*    Fri Oct 26 2018 Anish Swaminathan <anishs@vmware.com>  239-5
-    Revert the commit that causes GCE networkd timeout
-    https://github.com/systemd/systemd/commit/44b598a1c9d11c23420a5ef45ff11bcb0ed195eb
*    Mon Oct 08 2018 Srinidhi Rao <srinidhir@vmware.com> 239-4
-    Add glib-devel as a Requirement to systemd-devel
*    Fri Sep 21 2018 Alexey Makhalov <amakhalov@vmware.com> 239-3
-    Fix compilation issue against glibc-2.28
*    Tue Sep 18 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 239-2
-    Automatically load rdrand-rng kernel module on every boot.
*    Tue Aug 28 2018 Anish Swaminathan <anishs@vmware.com>  239-1
-    Update systemd to 239
*    Wed Apr 11 2018 Xiaolin Li <xiaolinl@vmware.com>  236-3
-    Build systemd with util-linux 2.32.
*    Wed Jan 17 2018 Divya Thaluru <dthaluru@vmware.com>  236-2
-    Fixed the log file directory structure
*    Fri Dec 29 2017 Anish Swaminathan <anishs@vmware.com>  236-1
-    Update systemd to 236
*    Thu Nov 09 2017 Vinay Kulkarni <kulkarniv@vmware.com>  233-11
-    Fix CVE-2017-15908 dns packet loop fix.
*    Tue Nov 07 2017 Vinay Kulkarni <kulkarniv@vmware.com>  233-10
-    Fix nullptr access during link disable.
*    Mon Sep 18 2017 Anish Swaminathan <anishs@vmware.com>  233-9
-    Backport router solicitation backoff from systemd 234
*    Fri Sep 15 2017 Anish Swaminathan <anishs@vmware.com>  233-8
-    Move network file to systemd package
*    Tue Aug 15 2017 Alexey Makhalov <amakhalov@vmware.com> 233-7
-    Fix compilation issue for glibc-2.26
*    Fri Jul 21 2017 Vinay Kulkarni <kulkarniv@vmware.com>  233-6
-    Fix for CVE-2017-1000082.
*    Fri Jul 07 2017 Vinay Kulkarni <kulkarniv@vmware.com>  233-5
-    Fix default-dns-from-env patch.
*    Wed Jul 05 2017 Xiaolin Li <xiaolinl@vmware.com> 233-4
-    Add kmod-devel to BuildRequires
*    Thu Jun 29 2017 Vinay Kulkarni <kulkarniv@vmware.com>  233-3
-    Fix for CVE-2017-9445.
*    Tue Jun 20 2017 Anish Swaminathan <anishs@vmware.com>  233-2
-    Fix for CVE-2017-9217
*    Mon Mar 06 2017 Vinay Kulkarni <kulkarniv@vmware.com>  233-1
-    Update systemd to 233
*    Tue Jan 3 2017 Alexey Makhalov <amakhalov@vmware.com>  232-5
-    Added /boot/systemd.cfg
*    Tue Dec 20 2016 Alexey Makhalov <amakhalov@vmware.com>  232-4
-    Fix initrd-switch-root issue
*    Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> 232-3
-    BuildRequires Linux-PAM-devel
*    Thu Dec 01 2016 Xiaolin Li <xiaolinl@vmware.com> 232-2
-    disable-elfutils.
*    Fri Nov 18 2016 Anish Swaminathan <anishs@vmware.com>  232-1
-    Update systemd to 232
*    Thu Nov 3 2016 Divya Thaluru <dthaluru@vmware.com>  228-32
-    Added logic to reload services incase of rpm upgrade
*    Thu Sep 29 2016 Vinay Kulkarni <kulkarniv@vmware.com>  228-31
-    Fix a CVE in systemd-notify socket.
*    Mon Aug 29 2016 Alexey Makhalov <amakhalov@vmware.com>  228-30
-    02-install-general-aliases.patch to create absolute symlinks
*    Fri Aug 26 2016 Anish Swaminathan <anishs@vmware.com>  228-29
-    Change config file properties for 99-default.link
*    Tue Aug 16 2016 Vinay Kulkarni <kulkarniv@vmware.com>  228-28
-    systemd-resolved: Fix DNS_TRANSACTION_PENDING assert.
*    Mon Aug 1 2016 Divya Thaluru <dthaluru@vmware.com> 228-27
-    Removed packaging of symlinks and will be created during installation
*    Tue Jul 12 2016 Vinay Kulkarni <kulkarniv@vmware.com>  228-26
-    systemd-resolved: Fix DNS domains resolv.conf search issue for static DNS.
*    Mon Jul 11 2016 Vinay Kulkarni <kulkarniv@vmware.com>  228-25
-    systemd-networkd: Update DUID/IAID config interface to systemd v230 spec.
*    Tue Jun 21 2016 Anish Swaminathan <anishs@vmware.com>  228-24
-    Change config file properties
*    Fri Jun 17 2016 Vinay Kulkarni <kulkarniv@vmware.com>  228-23
-    systemd-resolved: Configure initial DNS servers from environment var.
*    Mon Jun 06 2016 Alexey Makhalov <amakhalov@vmware.com>  228-22
-    systemd-resolved: disable LLMNR
*    Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 228-21
-    GA - Bump release of all rpms
*    Tue May 17 2016 Anish Swaminathan <anishs@vmware.com>  228-20
-    Added patch for letting kernel handle ndisc
*    Tue May 17 2016 Divya Thaluru <dthaluru@vmware.com> 228-19
-    Updated systemd-user PAM configuration
*    Mon May 16 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 228-18
-    Updated the MaxTasks to infinity in system.conf file
*    Thu Apr 21 2016 Mahmoud Bassiouny <mbassiouny@vmware.com>  228-17
-    Set the default.target to the multi-user.target
*    Tue Apr 12 2016 Vinay Kulkarni <kulkarniv@vmware.com>  228-16
-    Disable network interface renaming.
*    Thu Mar 31 2016 Vinay Kulkarni <kulkarniv@vmware.com>  228-15
-    Patch to query DHCP DUID, IAID.f
*    Wed Mar 30 2016 Vinay Kulkarni <kulkarniv@vmware.com>  228-14
-    Update DHCP DUID, IAID configuration patch.
*    Wed Mar 30 2016 Kumar Kaushik <kaushikk@vmware.com>  228-13
-    Install the security hardening script as part of systemd.
*    Tue Mar 29 2016 Kumar Kaushik <kaushikk@vmware.com>  228-12
-    Added patch for timedatectl /etc/adjtime PR2749.
*    Fri Mar 11 2016 Anish Swaminathan <anishs@vmware.com>  228-11
-    Added patch for dhcp preservation via duid iaid configurability
*    Fri Mar 11 2016 Anish Swaminathan <anishs@vmware.com>  228-10
-    Added patch for swap disconnect order
*    Thu Mar 10 2016 XIaolin Li <xiaolinl@vmware.com> 228-9
-    Enable manpages.
*    Fri Feb 19 2016 Anish Swaminathan <anishs@vmware.com>  228-8
-    Added patch to get around systemd-networkd wait online timeout
*    Sat Feb 06 2016 Alexey Makhalov <amakhalov@vmware.com>  228-7
-    Added patch: fix-reading-routes.
*    Wed Feb 03 2016 Anish Swaminathan <anishs@vmware.com>  228-6
-    Add hotplug udev rules.
*    Tue Jan 12 2016 Anish Swaminathan <anishs@vmware.com>  228-5
-    Change config file attributes.
*    Wed Jan 06 2016 Anish Swaminathan <anishs@vmware.com> 228-4
-    Patches for minor network fixes.
*    Wed Dec 16 2015 Anish Swaminathan <anishs@vmware.com> 228-3
-    Patch for ostree.
*    Wed Dec 16 2015 Anish Swaminathan <anishs@vmware.com> 228-2
-    Patch for loopback address.
*    Fri Dec 11 2015 Anish Swaminathan <anishs@vmware.com> 228-1
-    Upgrade systemd version.
*    Mon Nov 30 2015 Mahmoud Bassiouny <mbassiouny@vmware.com> 216-13
-    Removing the reference of lock user
*    Fri Oct 9 2015 Xiaolin Li <xiaolinl@vmware.com> 216-12
-    Removing la files from packages.
*    Fri Sep 18 2015 Divya Thaluru <dthaluru@vmware.com> 216-11
-    Packaging journal log directory
*    Thu Sep 10 2015 Alexey Makhalov <amakhalov@vmware.com> 216-10
-    Improve enoX renaming in VMware HV case. Patch is added.
*    Tue Aug 25 2015 Alexey Makhalov <amakhalov@vmware.com> 216-9
-    Reduce systemd-networkd boot time (exclude if-rename patch).
*    Mon Jul 20 2015 Divya Thaluru <dthaluru@vmware.com> 216-8
-    Adding sysvinit support
*    Mon Jul 06 2015 Kumar Kaushik <kaushikk@vmware.com> 216-7
-    Fixing networkd/udev race condition for renaming interface.
*    Thu Jun 25 2015 Sharath George <sharathg@vmware.com> 216-6
-    Remove debug files.
*    Tue Jun 23 2015 Divya Thaluru <dthaluru@vmware.com> 216-5
-    Building compat libs
*    Mon Jun 1 2015 Alexey Makhalov <amakhalov@vmware.com> 216-4
-    gudev support
*    Wed May 27 2015 Divya Thaluru <dthaluru@vmware.com> 216-3
-    Removing packing of PAM configuration files
*    Mon May 18 2015 Touseef Liaqat <tliaqat@vmware.com> 216-2
-    Update according to UsrMove.
*    Mon Oct 27 2014 Sharath George <sharathg@vmware.com> 216-1
-    Initial build. First version
