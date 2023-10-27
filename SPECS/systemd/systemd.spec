%global udev_services %{name}-udevd.service %{name}-udev-settle.service %{name}-udev-trigger.service %{name}-udevd-control.socket %{name}-udevd-kernel.socket %{name}-timesyncd.service

Name:           systemd
URL:            http://www.freedesktop.org/wiki/Software/systemd
Version:        247.13
Release:        8%{?dist}
License:        LGPLv2+ and GPLv2+ and MIT
Summary:        System and Service Manager
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/systemd/systemd-stable/archive/%{name}-stable-%{version}.tar.gz
%define sha512 %{name}=9bbf5db0eaa74af658a32c0a9b541a460c4634d041e5d0c1d7d528e3c9d8480714029db0a4b081e33d1334f9656ea536793da2115fa7cd2fa216aee8c0c5ad8b

Source1:        99-vmware-hotplug.rules
Source2:        50-security-hardening.conf
Source3:        systemd.cfg
Source4:        99-dhcp-en.network
%ifarch x86_64
Source5:        10-rdrand-rng.conf
%endif
Source6:        10-defaults.preset

Patch0:         systemd-247-enoX-uses-instance-number-for-vmware-hv.patch
Patch1:         systemd-247-default-dns-from-env.patch
Patch2:         timesync-Make-delaying-attempts-to-contact-servers-c.patch
Patch3:         network-Fix-crash-while-dhcp4-address-gets-update.patch
Patch4:         systemd-ignore-DEVICE_FOUND_UDEV-bit-on-switching-root.patch
Patch5:         network-attempt-to-trigger-kernel-IPv6LL-address-gen.patch
Patch6:         sd-netlink-make-default-timeout-configurable.patch

Requires:       Linux-PAM
Requires:       bzip2
Requires:       curl
Requires:       elfutils
Requires:       filesystem >= 1.1
Requires:       glib >= 2.68.4
Requires:       gnutls
Requires:       kmod
Requires:       %{name}-pam = %{version}-%{release}
Requires:       %{name}-rpm-macros = %{version}-%{release}
Requires:       %{name}-libs = %{version}-%{release}
Requires:       libacl
Requires:       libcap
Requires:       libgcrypt
Requires:       libmicrohttpd
Requires:       libseccomp
Requires:       libselinux
Requires:       lz4
Requires:       pcre
Requires:       xz
Requires:       libgpg-error

BuildRequires:  libgpg-error-devel
BuildRequires:  bzip2-devel
BuildRequires:  curl-devel
BuildRequires:  docbook-xml
BuildRequires:  docbook-xsl
BuildRequires:  gettext
BuildRequires:  glib-devel >= 2.68.4
BuildRequires:  gnutls-devel
BuildRequires:  gperf
BuildRequires:  intltool
BuildRequires:  kbd
BuildRequires:  kmod-devel
BuildRequires:  libacl-devel
BuildRequires:  libcap-devel
BuildRequires:  libgcrypt-devel
BuildRequires:  libseccomp
BuildRequires:  libseccomp-devel
BuildRequires:  libselinux-devel
BuildRequires:  libxslt-devel
BuildRequires:  Linux-PAM-devel
BuildRequires:  lz4-devel
BuildRequires:  meson
BuildRequires:  libmicrohttpd-devel
BuildRequires:  ninja-build
BuildRequires:  openssl-devel
BuildRequires:  pcre-devel
BuildRequires:  pkg-config
BuildRequires:  python3-devel
BuildRequires:  python3-lxml
BuildRequires:  shadow
BuildRequires:  util-linux-devel
BuildRequires:  XML-Parser
BuildRequires:  xz
BuildRequires:  xz-devel
BuildRequires:  zlib-devel
# rpmbuild needs /lib/rpm/macros.d/macros.systemd in order to expand %systemd_* actions.
# systemd-rpm-macros is not build yet, so consume it from publishrpms, similarly to as
# openjdk does it for Vivace rpms.
# Other packages using %system_* pre/post actions must use "BuildRequires:systemd-rpm-macros"
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
Requires(post): (coreutils or coreutils-selinux or toybox)
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
Requires:       glib-devel >= 2.68.4
Provides:       libudev-devel = %{version}-%{release}

%description devel
Development headers for developing applications linking to libsystemd

%package udev
Summary: Rule-based device node and kernel event manager
License:        LGPLv2+

Requires:       %{name} = %{version}-%{release}
Requires(post):   %{name} = %{version}-%{release}
Requires(preun):  %{name} = %{version}-%{release}
Requires(postun): %{name} = %{version}-%{release}
Requires(post):   grep
Requires:         kmod
Requires:         kbd
Provides:         udev = %{version}-%{release}

%description udev
This package contains systemd-udev and the rules and hardware database
needed to manage device nodes. This package is necessary on physical
machines and in virtual machines, but not in containers.

%package container
Summary: Tools for containers and VMs
Requires:       %{name} = %{version}-%{release}
Requires(post):   %{name} = %{version}-%{release}
Requires(preun):  %{name} = %{version}-%{release}
Requires(postun): %{name} = %{version}-%{release}
License:          LGPLv2+

%description container
Systemd tools to spawn and manage containers and virtual machines.

This package contains systemd-nspawn, machinectl, systemd-machined,
and systemd-importd.

%package journal-remote
Summary:        Tools to send journal events over the network
Requires:       %{name} = %{version}-%{release}
License:        LGPLv2+
Requires(post):   %{name} = %{version}-%{release}
Requires(preun):  %{name} = %{version}-%{release}
Requires(postun): %{name} = %{version}-%{release}
Requires:         libmicrohttpd
Provides:         %{name}-journal-gateway = %{version}-%{release}

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
%autosetup -p1 -n %{name}-stable-%{version}

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
       -Dmode=release
       -Dkmod=true
       -Duser-path=%{_usr}/local/bin:%{_usr}/local/sbin:%{_bindir}:%{_sbindir}
       -Dservice-watchdog=
       -Dblkid=true
       -Dseccomp=true
       -Ddefault-dnssec=no
       -Dfirstboot=false
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
       -Ddefault-dns-over-tls=opportunistic
       -Ddns-over-tls=true
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
       -Dsysvinit-path=%{_sysconfdir}/rc.d/init.d
       -Drc-local=%{_sysconfdir}/rc.d/rc.local
       -Dfallback-hostname=photon
       -Doomd=false
       -Dhomed=false
       -Dversion-tag=v%{version}-%{release}
       $CROSS_COMPILE_CONFIG
)

%{meson} "${CONFIGURE_OPTS[@]}"
%{meson_build}

%install
%{meson_install}

sed -i '/srv/d' %{buildroot}%{_tmpfilesdir}/home.conf
sed -i "s:0775 root lock:0755 root root:g" %{buildroot}%{_tmpfilesdir}/legacy.conf
sed -i "s:NamePolicy=kernel database onboard slot path:NamePolicy=kernel database:g" %{buildroot}%{_systemd_util_dir}/network/99-default.link

sed -i "s:#LLMNR=yes:LLMNR=no:g" %{buildroot}%{_sysconfdir}/%{name}/resolved.conf
sed -i "s:#DNSSEC=no:DNSSEC=no:g" %{buildroot}%{_sysconfdir}/%{name}/resolved.conf
sed -i "s:#DNSOverTLS=opportunistic:DNSOverTLS=no:g" %{buildroot}%{_sysconfdir}/%{name}/resolved.conf

rm -f %{buildroot}%{_var}/log/README

mkdir -p %{buildroot}%{_var}/opt/journal/log \
         %{buildroot}%{_var}/log

ln -sfr %{buildroot}%{_var}/opt/journal/log %{buildroot}%{_var}/log/journal

find %{buildroot} -name '*.la' -delete
install -Dm 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/udev/rules.d
install -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysctl.d
install -dm 0755 %{buildroot}/boot/
install -m 0644 %{SOURCE3} %{buildroot}/boot/
install -dm 0755 %{buildroot}%{_sysconfdir}/%{name}/network
install -m 0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/%{name}/network
install -m 0644 %{SOURCE6} %{buildroot}%{_presetdir}

rm %{buildroot}%{_unitdir}/default.target
ln -sfv multi-user.target %{buildroot}%{_unitdir}/default.target

%ifarch x86_64
install -m 0644 %{SOURCE5} %{buildroot}%{_sysconfdir}/modules-load.d
%endif
%find_lang %{name} ../%{name}.lang

%post
%{name}-machine-id-setup &>/dev/null || :

systemctl daemon-reexec &>/dev/null || {
  if [ $1 -gt 1 ] && [ -d /run/%{name}/system ] ; then
    kill -TERM 1 &>/dev/null || :
  fi
}

journalctl --update-catalog &>/dev/null || :
%{name}-tmpfiles --create &>/dev/null || :

if [ $1 -eq 1 ] ; then
  systemctl preset-all &>/dev/null || :
  systemctl --global preset-all &>/dev/null || :
fi

%clean
rm -rf %{buildroot}/*

%post udev
udevadm hwdb --update &>/dev/null || :

%systemd_post %udev_services

%preun udev
%systemd_preun %udev_services

%postun udev
%systemd_postun_with_restart %{name}-udevd.service

%files
%defattr(-,root,root)
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/user
%dir %{_sysconfdir}/%{name}/network
%dir %{_sysconfdir}/tmpfiles.d
%dir %{_sysconfdir}/sysctl.d
%dir %{_sysconfdir}/modules-load.d
%dir %{_sysconfdir}/binfmt.d

%{_sysconfdir}/X11/xinit/xinitrc.d/50-%{name}-user.sh
%{_sysconfdir}/sysctl.d/50-security-hardening.conf
%{_sysconfdir}/xdg/%{name}
%{_sysconfdir}/rc.d/init.d/README

%config(noreplace) %{_sysconfdir}/%{name}/sleep.conf
%config(noreplace) %{_sysconfdir}/%{name}/system.conf
%config(noreplace) %{_sysconfdir}/%{name}/user.conf
%config(noreplace) %{_sysconfdir}/%{name}/logind.conf
%config(noreplace) %{_sysconfdir}/%{name}/journald.conf
%config(noreplace) %{_sysconfdir}/%{name}/resolved.conf
%config(noreplace) %{_sysconfdir}/%{name}/coredump.conf
%config(noreplace) %{_sysconfdir}/%{name}/timesyncd.conf
%config(noreplace) %{_sysconfdir}/%{name}/networkd.conf
%config(noreplace) %{_sysconfdir}/%{name}/pstore.conf

%ifarch x86_64
%config(noreplace) %{_sysconfdir}/modules-load.d/10-rdrand-rng.conf
%endif
%config(noreplace) %{_sysconfdir}/%{name}/network/99-dhcp-en.network

%config(noreplace) /boot/%{name}.cfg

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
%{_bindir}/%{name}-analyze
%{_bindir}/%{name}-ask-password
%{_bindir}/%{name}-cat
%{_bindir}/%{name}-cgls
%{_bindir}/%{name}-cgtop
%{_bindir}/%{name}-delta
%{_bindir}/%{name}-detect-virt
%{_bindir}/%{name}-escape
%{_bindir}/%{name}-id128
%{_bindir}/%{name}-inhibit
%{_bindir}/%{name}-machine-id-setup
%{_bindir}/%{name}-mount
%{_bindir}/%{name}-notify
%{_bindir}/%{name}-path
%{_bindir}/%{name}-resolve
%{_bindir}/%{name}-run
%{_bindir}/%{name}-socket-activate
%{_bindir}/%{name}-stdio-bridge
%{_bindir}/%{name}-tmpfiles
%{_bindir}/%{name}-tty-ask-password-agent
%{_bindir}/%{name}-umount
%{_bindir}/timedatectl
%{_bindir}/userdbctl
%{_bindir}/%{name}-repart
%{_bindir}/%{name}-dissect

%{_tmpfilesdir}/etc.conf
%{_tmpfilesdir}/home.conf
%{_tmpfilesdir}/journal-nocow.conf
%{_tmpfilesdir}/legacy.conf
%{_tmpfilesdir}/portables.conf
%{_tmpfilesdir}/static-nodes-permissions.conf
%{_tmpfilesdir}/%{name}-nologin.conf
%{_tmpfilesdir}/%{name}-tmp.conf
%{_tmpfilesdir}/%{name}.conf
%{_tmpfilesdir}/tmp.conf
%{_tmpfilesdir}/var.conf
%{_tmpfilesdir}/x11.conf
%{_tmpfilesdir}/README

%{_environmentdir}/99-environment.conf
%exclude %{_datadir}/locale
%{_libdir}/rpm/*
%{_libdir}/sysctl.d/*
%{_systemd_util_dir}/catalog/*
%{_systemd_util_dir}/*.so
%{_systemd_util_dir}/network/*
%{_systemd_util_dir}/ntp-units.d/*
%{_systemd_util_dir}/portable/*
%{_systemd_util_dir}/resolv.conf
%{_systemd_util_dir}/%{name}*
%{_systemd_util_dir}/user*
%{_systemd_util_dir}/import-pubring.gpg
%{_unitdir}/*
%{_presetdir}/*
%{_systemdgeneratordir}/*
%{_datadir}/bash-completion/*
%{_datadir}/factory/*
%{_datadir}/dbus-1
%{_datadir}/doc/*
%{_datadir}/polkit-1
%{_datadir}/%{name}
%{_datadir}/zsh/*
%{_var}/log/journal

%ghost %dir %attr(0755,-,-) %{_sysconfdir}/%{name}/system/basic.target.wants
%ghost %dir %attr(0755,-,-) %{_sysconfdir}/%{name}/system/bluetooth.target.wants
%ghost %dir %attr(0755,-,-) %{_sysconfdir}/%{name}/system/default.target.wants
%ghost %dir %attr(0755,-,-) %{_sysconfdir}/%{name}/system/getty.target.wants
%ghost %dir %attr(0755,-,-) %{_sysconfdir}/%{name}/system/graphical.target.wants
%ghost %dir %attr(0755,-,-) %{_sysconfdir}/%{name}/system/local-fs.target.wants
%ghost %dir %attr(0755,-,-) %{_sysconfdir}/%{name}/system/machines.target.wants
%ghost %dir %attr(0755,-,-) %{_sysconfdir}/%{name}/system/multi-user.target.wants
%ghost %dir %attr(0755,-,-) %{_sysconfdir}/%{name}/system/network-online.target.wants
%ghost %dir %attr(0755,-,-) %{_sysconfdir}/%{name}/system/printer.target.wants
%ghost %dir %attr(0755,-,-) %{_sysconfdir}/%{name}/system/remote-fs.target.wants
%ghost %dir %attr(0755,-,-) %{_sysconfdir}/%{name}/system/sockets.target.wants
%ghost %dir %attr(0755,-,-) %{_sysconfdir}/%{name}/system/sysinit.target.wants
%ghost %dir %attr(0755,-,-) %{_sysconfdir}/%{name}/system/system-update.target.wants
%ghost %dir %attr(0755,-,-) %{_sysconfdir}/%{name}/system/timers.target.wants
%ghost %dir %attr(0755,-,-) %{_sysconfdir}/%{name}/system

%files devel
%defattr(-,root,root)
%dir %{_includedir}/%{name}
%{_libdir}/libudev.so
%{_libdir}/libsystemd.so
%{_includedir}/%{name}/*.h
%{_includedir}/libudev.h
%{_libdir}/pkgconfig/libudev.pc
%{_libdir}/pkgconfig/libsystemd.pc
%{_datadir}/pkgconfig/%{name}.pc
%{_datadir}/pkgconfig/udev.pc

%files udev
%defattr(-,root,root)
%dir %{_sysconfdir}/udev
%{_sysconfdir}/udev/rules.d/99-vmware-hotplug.rules
%dir %{_sysconfdir}/kernel
%dir %{_sysconfdir}/modules-load.d
%{_sysconfdir}/%{name}/pstore.conf
%{_sysconfdir}/%{name}/sleep.conf
%{_sysconfdir}/%{name}/timesyncd.conf
%{_sysconfdir}/udev/udev.conf
%{_tmpfilesdir}/%{name}-pstore.conf
%{_bindir}/bootctl
%{_bindir}/kernel-install
%{_bindir}/%{name}-hwdb
%{_bindir}/udevadm

%{_libdir}/udev/v4l_id
%{_libdir}/kernel
%{_libdir}/modprobe.d
%{_libdir}/modules-load.d
%{_systemd_util_dir}/network/99-default.link
%{_systemd_util_dir}/ntp-units.d/80-%{name}-timesync.list
%{_systemd_util_dir}/system-generators/%{name}-bless-boot-generator
%{_systemd_util_dir}/system-generators/%{name}-hibernate-resume-generator
%{_systemd_util_dir}/system-sleep
%{_unitdir}/hibernate.target
%{_unitdir}/hybrid-sleep.target
%{_unitdir}/initrd-udevadm-cleanup-db.service
%{_unitdir}/kmod-static-nodes.service
%{_unitdir}/quotaon.service
%{_unitdir}/sleep.target
%{_unitdir}/sockets.target.wants/%{name}-udevd-control.socket
%{_unitdir}/sockets.target.wants/%{name}-udevd-kernel.socket
%{_unitdir}/suspend-then-hibernate.target
%{_unitdir}/suspend.target
%{_unitdir}/sysinit.target.wants/kmod-static-nodes.service
%{_unitdir}/sysinit.target.wants/%{name}-boot-system-token.service
%{_unitdir}/sysinit.target.wants/%{name}-hwdb-update.service
%{_unitdir}/sysinit.target.wants/%{name}-modules-load.service
%{_unitdir}/sysinit.target.wants/%{name}-random-seed.service
%{_unitdir}/sysinit.target.wants/%{name}-tmpfiles-setup-dev.service
%{_unitdir}/sysinit.target.wants/%{name}-udevd.service
%{_unitdir}/%{name}-backlight@.service
%{_unitdir}/%{name}-bless-boot.service
%{_unitdir}/%{name}-boot-system-token.service
%{_unitdir}/%{name}-fsck-root.service
%{_unitdir}/%{name}-fsck@.service
%{_unitdir}/%{name}-hibernate-resume@.service
%{_unitdir}/%{name}-hibernate.service
%{_unitdir}/%{name}-hwdb-update.service
%{_unitdir}/%{name}-hybrid-sleep.service
%{_unitdir}/%{name}-modules-load.service
%{_unitdir}/%{name}-pstore.service
%{_unitdir}/%{name}-quotacheck.service
%{_unitdir}/%{name}-random-seed.service
%{_unitdir}/%{name}-remount-fs.service
%{_unitdir}/%{name}-rfkill.service
%{_unitdir}/%{name}-rfkill.socket
%{_unitdir}/%{name}-suspend-then-hibernate.service
%{_unitdir}/%{name}-suspend.service
%{_unitdir}/%{name}-timesyncd.service
%{_unitdir}/%{name}-tmpfiles-setup-dev.service
%{_unitdir}/%{name}-udev-settle.service
%{_unitdir}/%{name}-udevd-control.socket
%{_unitdir}/%{name}-udevd-kernel.socket
%{_unitdir}/%{name}-udevd.service
%{_unitdir}/%{name}-vconsole-setup.service
%{_unitdir}/%{name}-volatile-root.service
%{_systemd_util_dir}/%{name}-backlight
%{_systemd_util_dir}/%{name}-bless-boot
%{_systemd_util_dir}/%{name}-fsck
%{_systemd_util_dir}/%{name}-growfs
%{_systemd_util_dir}/%{name}-hibernate-resume
%{_systemd_util_dir}/%{name}-makefs
%{_systemd_util_dir}/%{name}-modules-load
%{_systemd_util_dir}/%{name}-pstore
%{_systemd_util_dir}/%{name}-quotacheck
%{_systemd_util_dir}/%{name}-random-seed
%{_systemd_util_dir}/%{name}-remount-fs
%{_systemd_util_dir}/%{name}-rfkill
%{_systemd_util_dir}/%{name}-sleep
%{_systemd_util_dir}/%{name}-timesyncd
%{_systemd_util_dir}/%{name}-udevd
%{_systemd_util_dir}/%{name}-vconsole-setup
%{_systemd_util_dir}/%{name}-volatile-root

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
%{_libdir}/pam.d/%{name}-user

%files container
%defattr(-,root,root)
%{_bindir}/%{name}-nspawn
%{_bindir}/machinectl

%{_systemd_util_dir}/%{name}-machined
%{_unitdir}/%{name}-machined.service
%{_unitdir}/%{name}-nspawn@.service
%{_unitdir}/dbus-org.freedesktop.machine1.service
%{_unitdir}/var-lib-machines.mount
%{_unitdir}/machine.slice
%{_unitdir}/machines.target.wants
%{_tmpfilesdir}/%{name}-nspawn.conf

%{_datadir}/dbus-1/system.d/org.freedesktop.machine1.conf
%{_datadir}/dbus-1/system-services/org.freedesktop.machine1.service
%{_datadir}/polkit-1/actions/org.freedesktop.machine1.policy

%files journal-remote
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/%{name}/journal-upload.conf
%config(noreplace) %{_sysconfdir}/%{name}/journal-remote.conf

%{_systemd_util_dir}/%{name}-journal-gatewayd
%{_systemd_util_dir}/%{name}-journal-remote
%{_systemd_util_dir}/%{name}-journal-upload

%{_unitdir}/%{name}-journal-gatewayd.service
%{_unitdir}/%{name}-journal-gatewayd.socket
%{_unitdir}/%{name}-journal-remote.service
%{_unitdir}/%{name}-journal-remote.socket
%{_unitdir}/%{name}-journal-upload.service

%files rpm-macros
%defattr(-,root,root)
%{_libdir}/rpm/macros.d

%files tests
%defattr(-,root,root)
%{_systemd_util_dir}/tests

%files lang -f ../%{name}.lang
%defattr(-,root,root)

%changelog
* Fri Oct 20 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 247.13-8
- Bump version as part of glib upgrade
* Mon Oct 09 2023 Susant Sahani <ssahani@vmware.com> 247.13-7
- Backport sd-netlink: make the default timeout configurable
* Wed Sep 27 2023 Prashant S Chauhan <psinghchauha@vmware.com> 247.13-6
- Add kbd in Requires for systemd-udev
* Wed Aug 02 2023 Shreenidhi Shedi <sshedi@vmware.com> 247.13-5
- Fix inet6 issue
- Fixes: https://github.com/systemd/systemd/issues/22424
* Thu Jun 08 2023 Harinadh D <hdommaraju@vmware.com> 247.13-4
- Fix unmounts issue on first boot
- issue: On first boot systemd believes some successfully
- mounted block devices have been unplugged and unmounts them
* Sat Apr 29 2023 Harinadh D <hdommaraju@vmware.com> 247.13-3
- Fix for requires
* Fri Feb 03 2023 Shreenidhi Shedi <sshedi@vmware.com> 247.13-2
- Remove test files from main package
* Wed Dec 21 2022 Susant Sahani <ssahani@vmware.com> 247.13-1
- Update to stable version 247.13
* Mon Dec 12 2022 Shreenidhi Shedi <sshedi@vmware.com> 247.11-6
- Fix CVE-2022-4415
* Wed Nov 30 2022 Shreenidhi Shedi <sshedi@vmware.com> 247.11-5
- Add `SendRelease=false` to default network file.
* Wed Aug 10 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 247.11-4
- Bump version as part of lxml update
* Thu Jul 07 2022 Shreenidhi Shedi <sshedi@vmware.com> 247.11-3
- Enable dns-over-tls support
- Enable default-dns-over-tls=opportunistic support
- Disable DNSSEC & DNSOverTLS by default
* Thu Feb 10 2022 Shreenidhi Shedi <sshedi@vmware.com> 247.11-2
- Add libgpg-error-devel to BuildRequires
* Tue Jan 18 2022 Susant Sahani <ssahani@vmware.com>  247.11-1
- Update to stable version 247.11
* Mon Jan 10 2022 Nitesh Kumar <kunitesh@vmware.com> 247.10-6
- Added postun for systemd-tests.
* Sat Jan 08 2022 Shreenidhi Shedi <sshedi@vmware.com> 247.10-5
- Fix CVE-2021-3997
* Mon Jan 03 2022 Sujay G <gsujay@vmware.com> 247.10-4
- Bump version to build with updated python3-lxml
* Thu Dec 09 2021 Prashant S Chauhan <psinghchauha@vmware.com> 247.10-3
- Bump up to compile with python 3.10
* Mon Nov 08 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 247.10-2
- Bump up release for openssl
* Wed Nov 03 2021 Susant Sahani <ssahani@vmware.com>  247.10-1
- Update to stable version 247.10
* Wed Sep 08 2021 Nitesh Kumar <kunitesh@vmware.com> 247.8-2
- Replacement of ITS suggested words.
* Thu Jul 22 2021 Susant Sahani <ssahani@vmware.com>  247.8-1
- Update to version 247.8-1
* Mon Jul 19 2021 Susant Sahani <ssahani@vmware.com>  247.7-1
- Switch to meson, update version, fix netword crash and CVE-2020-13529
* Fri Jul 16 2021 Him Kalyan Bordoloi <bordoloih@vmware.com>  247.6-2
- Fix for CVE-2021-33910
* Tue Mar 30 2021 Susant Sahani <ssahani@vmware.com>  247.6-1
- Add systemd-rpm-macros to extra build requires and update version
* Tue Mar 16 2021 Susant Sahani <ssahani@vmware.com>  247.4-1
- Version bump and fix udev preun macro
* Wed Feb 03 2021 Susant Sahani <ssahani@vmware.com>  247.3-1
- Version bump
* Mon Jan 04 2021 Susant Sahani <ssahani@vmware.com>  247.2-2
- Backport timesync: ConnectionRetrySec=
* Thu Dec 17 2020 Susant Sahani <ssahani@vmware.com>  247.2-1
- Upgrade to 247.2
- Enable openssl and drop systemd-oomd
* Mon Dec 14 2020 Susant Sahani <ssahani@vmware.com>  247-1
- Upgrade to 247
- Split out systemd package to multiple packages
* Tue Oct 27 2020 Susant Sahani <ssahani@vmware.com>  245.5-3
- util: return the correct correct wd from inotify helpers
* Sun Aug 16 2020 Susant Sahani <ssahani@vmware.com>  245.5-2
- Drop meson macro
* Tue May 12 2020 Susant Sahani <ssahani@vmware.com>  245.5-1
- Update to version 245.5 stable
* Mon May 04 2020 Alexey Makhalov <amakhalov@vmware.com> 239-14
- Fix compilation issue with gcc-8.4.0
- Build with debug info.
* Sat Apr 18 2020 Alexey Makhalov <amakhalov@vmware.com> 239-13
- Enable SELinux support
* Thu Oct 31 2019 Alexey Makhalov <amakhalov@vmware.com> 239-12
- Cross compilation support
* Tue Oct 22 2019 Piyush Gupta <guptapi@vmware.com>  239-11
- Added requires elfutils
* Thu Jan 10 2019 Anish Swaminathan <anishs@vmware.com>  239-10
- Fix CVE-2018-16864, CVE-2018-16865, CVE-2018-16866
* Wed Jan 09 2019 Keerthana K <keerthanak@vmware.com> 239-9
- Seting default values for tcp_timestamps, tcp_challenge_ack_limit and ip_forward.
* Wed Jan 02 2019 Anish Swaminathan <anishs@vmware.com>  239-8
- Fix CVE-2018-15686, CVE-2018-15687
* Sun Nov 11 2018 Tapas Kundu <tkundu@vmware.com> 239-7
- Fix CVE-2018-15688
* Fri Oct 26 2018 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 239-6
- Auto-load rdrand-rng kernel module only on x86.
* Fri Oct 26 2018 Anish Swaminathan <anishs@vmware.com>  239-5
- Revert the commit that causes GCE networkd timeout
- https://github.com/systemd/systemd/commit/44b598a1c9d11c23420a5ef45ff11bcb0ed195eb
* Mon Oct 08 2018 Srinidhi Rao <srinidhir@vmware.com> 239-4
- Add glib-devel as a Requirement to systemd-devel
* Fri Sep 21 2018 Alexey Makhalov <amakhalov@vmware.com> 239-3
- Fix compilation issue against glibc-2.28
* Tue Sep 18 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 239-2
- Automatically load rdrand-rng kernel module on every boot.
* Tue Aug 28 2018 Anish Swaminathan <anishs@vmware.com>  239-1
- Update systemd to 239
* Wed Apr 11 2018 Xiaolin Li <xiaolinl@vmware.com>  236-3
- Build systemd with util-linux 2.32.
* Wed Jan 17 2018 Divya Thaluru <dthaluru@vmware.com>  236-2
- Fixed the log file directory structure
* Fri Dec 29 2017 Anish Swaminathan <anishs@vmware.com>  236-1
- Update systemd to 236
* Thu Nov 09 2017 Vinay Kulkarni <kulkarniv@vmware.com>  233-11
- Fix CVE-2017-15908 dns packet loop fix.
* Tue Nov 07 2017 Vinay Kulkarni <kulkarniv@vmware.com>  233-10
- Fix nullptr access during link deactivate.
* Mon Sep 18 2017 Anish Swaminathan <anishs@vmware.com>  233-9
- Backport router solicitation backoff from systemd 234
* Fri Sep 15 2017 Anish Swaminathan <anishs@vmware.com>  233-8
- Move network file to systemd package
* Tue Aug 15 2017 Alexey Makhalov <amakhalov@vmware.com> 233-7
- Fix compilation issue for glibc-2.26
* Fri Jul 21 2017 Vinay Kulkarni <kulkarniv@vmware.com>  233-6
- Fix for CVE-2017-1000082.
* Fri Jul 07 2017 Vinay Kulkarni <kulkarniv@vmware.com>  233-5
- Fix default-dns-from-env patch.
* Wed Jul 05 2017 Xiaolin Li <xiaolinl@vmware.com> 233-4
- Add kmod-devel to BuildRequires
* Thu Jun 29 2017 Vinay Kulkarni <kulkarniv@vmware.com>  233-3
- Fix for CVE-2017-9445.
* Tue Jun 20 2017 Anish Swaminathan <anishs@vmware.com>  233-2
- Fix for CVE-2017-9217
* Mon Mar 06 2017 Vinay Kulkarni <kulkarniv@vmware.com>  233-1
- Update systemd to 233
* Tue Jan 3 2017 Alexey Makhalov <amakhalov@vmware.com>  232-5
- Added /boot/systemd.cfg
* Tue Dec 20 2016 Alexey Makhalov <amakhalov@vmware.com>  232-4
- Fix initrd-switch-root issue
* Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> 232-3
- BuildRequires Linux-PAM-devel
* Thu Dec 01 2016 Xiaolin Li <xiaolinl@vmware.com> 232-2
- deactivate-elfutils.
* Fri Nov 18 2016 Anish Swaminathan <anishs@vmware.com>  232-1
- Update systemd to 232
* Thu Nov 3 2016 Divya Thaluru <dthaluru@vmware.com>  228-32
- Added logic to reload services incase of rpm upgrade
* Thu Sep 29 2016 Vinay Kulkarni <kulkarniv@vmware.com>  228-31
- Fix a CVE in systemd-notify socket.
* Mon Aug 29 2016 Alexey Makhalov <amakhalov@vmware.com>  228-30
- 02-install-general-aliases.patch to create absolute symlinks
* Fri Aug 26 2016 Anish Swaminathan <anishs@vmware.com>  228-29
- Change config file properties for 99-default.link
* Tue Aug 16 2016 Vinay Kulkarni <kulkarniv@vmware.com>  228-28
- systemd-resolved: Fix DNS_TRANSACTION_PENDING assert.
* Mon Aug 1 2016 Divya Thaluru <dthaluru@vmware.com> 228-27
- Removed packaging of symlinks and will be created during installation
* Tue Jul 12 2016 Vinay Kulkarni <kulkarniv@vmware.com>  228-26
- systemd-resolved: Fix DNS domains resolv.conf search issue for static DNS.
* Mon Jul 11 2016 Vinay Kulkarni <kulkarniv@vmware.com>  228-25
- systemd-networkd: Update DUID/IAID config interface to systemd v230 spec.
* Tue Jun 21 2016 Anish Swaminathan <anishs@vmware.com>  228-24
- Change config file properties
* Fri Jun 17 2016 Vinay Kulkarni <kulkarniv@vmware.com>  228-23
- systemd-resolved: Configure initial DNS servers from environment var.
* Mon Jun 06 2016 Alexey Makhalov <amakhalov@vmware.com>  228-22
- systemd-resolved: deactivate LLMNR
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 228-21
- GA - Bump release of all rpms
* Tue May 17 2016 Anish Swaminathan <anishs@vmware.com>  228-20
- Added patch for letting kernel handle ndisc
* Tue May 17 2016 Divya Thaluru <dthaluru@vmware.com> 228-19
- Updated systemd-user PAM configuration
* Mon May 16 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 228-18
- Updated the MaxTasks to infinity in system.conf file
* Thu Apr 21 2016 Mahmoud Bassiouny <mbassiouny@vmware.com>  228-17
- Set the default.target to the multi-user.target
* Tue Apr 12 2016 Vinay Kulkarni <kulkarniv@vmware.com>  228-16
- Deactivate network interface renaming.
* Thu Mar 31 2016 Vinay Kulkarni <kulkarniv@vmware.com>  228-15
- Patch to query DHCP DUID, IAID.f
* Wed Mar 30 2016 Vinay Kulkarni <kulkarniv@vmware.com>  228-14
- Update DHCP DUID, IAID configuration patch.
* Wed Mar 30 2016 Kumar Kaushik <kaushikk@vmware.com>  228-13
- Install the security hardening script as part of systemd.
* Tue Mar 29 2016 Kumar Kaushik <kaushikk@vmware.com>  228-12
- Added patch for timedatectl /etc/adjtime PR2749.
* Fri Mar 11 2016 Anish Swaminathan <anishs@vmware.com>  228-11
- Added patch for dhcp preservation via duid iaid configurability
* Fri Mar 11 2016 Anish Swaminathan <anishs@vmware.com>  228-10
- Added patch for swap disconnect order
* Thu Mar 10 2016 XIaolin Li <xiaolinl@vmware.com> 228-9
- Enable manpages.
* Fri Feb 19 2016 Anish Swaminathan <anishs@vmware.com>  228-8
- Added patch to get around systemd-networkd wait online timeout
* Sat Feb 06 2016 Alexey Makhalov <amakhalov@vmware.com>  228-7
- Added patch: fix-reading-routes.
* Wed Feb 03 2016 Anish Swaminathan <anishs@vmware.com>  228-6
- Add hotplug udev rules.
* Tue Jan 12 2016 Anish Swaminathan <anishs@vmware.com>  228-5
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
