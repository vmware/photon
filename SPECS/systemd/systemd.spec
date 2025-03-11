%global udev_services %{name}-udevd.service %{name}-udev-settle.service %{name}-udev-trigger.service %{name}-udevd-control.socket %{name}-udevd-kernel.socket %{name}-timesyncd.service

Name:           systemd
URL:            http://www.freedesktop.org/wiki/Software/systemd
Version:        253.19
Release:        10%{?dist}
Summary:        System and Service Manager
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/systemd/systemd-stable/archive/%{name}-stable-%{version}.tar.gz
%define sha512 %{name}=42798768a5859ded6bb5f65bed2d0ced81c86eca06ebed275967352435e4bac93df8c95a4a3f841f43e1450457629c92e9e1a5f51159607055484dc53ffa1699

Source1:        99-vmware-hotplug.rules
Source2:        50-security-hardening.conf
Source3:        %{name}.cfg
Source4:        99-dhcp-en.network
%ifarch x86_64
Source5:        10-rdrand-rng.conf
%endif
Source6:        10-defaults.preset

Source11:       macros.sysusers
Source12:       sysusers.attr
Source13:       sysusers.prov
Source14:       sysusers.generate-pre.sh

Source15: license.txt
%include %{SOURCE15}

Patch0: enoX-uses-instance-number-for-vmware-hv.patch
Patch1: fetch-dns-servers-from-environment.patch
Patch2: execute-suppress-credentials-mount-if-empty.patch
Patch3: fix-lvrename-unmount.patch
Patch4: revert-network-delay-to-configure-address-until-it-i.patch
Patch5: do-not-build-with-trivial-auto-var-init-zero.patch
Patch6: do-not-allocate-1m-on-stack.patch
Patch7: 0001-Remove-unused-default-groups-rules-and-tmpfiles.patch

Requires:       Linux-PAM
Requires:       bzip2
Requires:       curl
Requires:       elfutils
Requires:       filesystem >= 1.1
Requires:       glib
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
BuildRequires:  glib-devel
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
BuildRequires:  python3-jinja2
BuildRequires:  shadow
BuildRequires:  util-linux-devel
BuildRequires:  XML-Parser
BuildRequires:  xz-devel
BuildRequires:  zlib-devel
BuildRequires:  photon-release

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
Requires:       glib-devel
Provides:       libudev-devel = %{version}

%description devel
Development headers for developing applications linking to libsystemd

%package udev
Summary: Rule-based device node and kernel event manager

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

%description container
Systemd tools to spawn and manage containers and virtual machines.

This package contains systemd-nspawn, machinectl, systemd-machined,
and %{name}-importd.

%package journal-remote
Summary:        Tools to send journal events over the network
Requires:       %{name} = %{version}-%{release}
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
       -Dsysusers=true
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
       -Dsystemd-network-uid=76
       -Dsystemd-resolve-uid=77
       -Dsystemd-timesync-uid=78
       -Dsysupdate=false
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

sed -i 's/#DefaultOOMPolicy=stop/DefaultOOMPolicy=continue/' %{buildroot}%{_sysconfdir}/%{name}/system.conf

rm -f %{buildroot}%{_var}/log/README \
      %{buildroot}%{_sysusersdir}/README

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

install -m 0644 -D -t %{buildroot}%{_rpmmacrodir}/ %{SOURCE11}
install -m 0644 -D -t %{buildroot}%{_rpmconfigdir}/fileattrs/ %{SOURCE12}
install -m 0755 -D -t %{buildroot}%{_rpmconfigdir}/ %{SOURCE13}
install -m 0755 -D -t %{buildroot}%{_rpmconfigdir}/ %{SOURCE14}

%find_lang %{name} ../%{name}.lang

%post
%{name}-machine-id-setup &>/dev/null || :

systemctl daemon-reexec &>/dev/null || {
  if [ $1 -gt 1 ] && [ -d /run/%{name}/system ] ; then
    kill -TERM 1 &>/dev/null || :
  fi
}

journalctl --update-catalog &>/dev/null || :
systemd-sysusers || :
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
%config(noreplace) %{_sysusersdir}/*.conf

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
%{_bindir}/%{name}-sysusers
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
%{_bindir}/%{name}-sysext
%{_bindir}/%{name}-creds
%{_bindir}/%{name}-ac-power

%{_tmpfilesdir}/etc.conf
%{_tmpfilesdir}/home.conf
%{_tmpfilesdir}/journal-nocow.conf
%{_tmpfilesdir}/legacy.conf
%{_tmpfilesdir}/portables.conf
%{_tmpfilesdir}/static-nodes-permissions.conf
%{_tmpfilesdir}/provision.conf
%{_tmpfilesdir}/%{name}-nologin.conf
%{_tmpfilesdir}/%{name}-tmp.conf
%{_tmpfilesdir}/%{name}.conf
%{_tmpfilesdir}/%{name}-resolve.conf
%{_tmpfilesdir}/%{name}-network.conf
%{_tmpfilesdir}/tmp.conf
%{_tmpfilesdir}/var.conf
%{_tmpfilesdir}/x11.conf
%{_tmpfilesdir}/credstore.conf
%{_tmpfilesdir}/README

%{_environmentdir}/99-environment.conf
%exclude %{_datadir}/locale
%{_libdir}/binfmt.d
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
%{_libdir}/lib%{name}.so
%{_includedir}/%{name}/*.h
%{_includedir}/libudev.h
%{_libdir}/pkgconfig/libudev.pc
%{_libdir}/pkgconfig/lib%{name}.pc
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
%{_bindir}/kernel-install
%{_bindir}/%{name}-hwdb
%{_bindir}/udevadm

%{_libdir}/udev/v4l_id
%{_libdir}/udev/dmi_memory_id
%{_libdir}/kernel
%{_libdir}/modprobe.d
%{_libdir}/modules-load.d
%{_systemd_util_dir}/network/99-default.link
%{_systemd_util_dir}/ntp-units.d/80-%{name}-timesync.list
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
%{_unitdir}/sysinit.target.wants/%{name}-hwdb-update.service
%{_unitdir}/sysinit.target.wants/%{name}-modules-load.service
%{_unitdir}/sysinit.target.wants/%{name}-random-seed.service
%{_unitdir}/sysinit.target.wants/%{name}-tmpfiles-setup-dev.service
%{_unitdir}/sysinit.target.wants/%{name}-udevd.service
%{_unitdir}/%{name}-backlight@.service
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

%{_datadir}/bash-completion/completions/kernel-install
%{_datadir}/bash-completion/completions/udevadm

%{_datadir}/dbus-1/system-services/org.freedesktop.timesync1.service
%{_datadir}/dbus-1/system.d/org.freedesktop.timesync1.conf

%{_datadir}/zsh/site-functions/_kernel-install
%{_datadir}/zsh/site-functions/_udevadm

%files libs
%defattr(-,root,root)
%{_libdir}/libnss_myhostname.so.2
%{_libdir}/libnss_mymachines.so.2
%{_libdir}/libnss_resolve.so.2
%{_libdir}/libnss_systemd.so.2
%{_libdir}/libsystemd.so.*
%{_libdir}/libudev.so.1.*
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
%{_rpmmacrodir}/*

%files tests
%defattr(-,root,root)
%{_systemd_util_dir}/tests

%files lang -f ../%{name}.lang

%changelog
* Thu Mar 20 2025 Ankit Jain <ankit-aj.jain@broadcom.com> 253.19-10
- Bump-up to build with kmod-34.1
* Wed Jan 22 2025 Tapas Kundu <tapas.kundu@broadcom.com> 253.19-9
- Bump version as a part of meson upgrade
* Thu Dec 12 2024 Dweep Advani <dweep.advani@broadcom.com> 253.19-8
- Release bump for SRP compliance
* Fri Nov 08 2024 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 253.19-7
- Remove standalone license exceptions
* Tue Nov 05 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 253.19-6
- Release bump for SRP compliance
* Tue Jun 18 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 253.19-5
- Disable sysupdate services through build
* Fri Jun 14 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 253.19-4
- Disable sysupdate timer through preset
* Fri Jun 07 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 253.19-3
- Disable sysupdate services through preset
* Thu May 30 2024 Nitesh Kumar <nitesh-nk.kumar@broadcom.com> 253.19-2
- Patched to remove unused groups from systemd
* Tue May 21 2024 Dweep Advani <dweep.advani@broadcom.com> 253.19-1
- Version upgrade to 253.19, avoid -ftrivial-auto-var-init=zero and do not alloc 1m on stack
* Mon Apr 29 2024 Susant Sahani <susant.sahani@broadcom.com> 253.17-1
- Upgrade to v253.17
* Sun Mar 24 2024 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 253.12-7
- Fix issue with VM reconfigure + static ip
* Tue Jan 09 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 253.12-6
- Remove '60-ioschedulers.rules' and 'use-bfq-scheduler.patch' files
* Tue Jan 02 2024 Ankit Jain <ankitja@vmware.com> 253.12-5
- Disable 'efi' and 'gnu-efi' support
* Wed Nov 29 2023 Shreenidhi Shedi <sshedi@vmware.com> 253.12-4
- Bump version as a part of gnutls upgrade
* Mon Nov 20 2023 Guruswamy Basavaiah <bguruswamy@vmware.com> 253.12-3
- Make mq-deadline default IO scheduler
* Fri Oct 27 2023 Harinadh D <hdommaraju@vmware.com> 253.12-2
- fix for lvrename unmounts the mount point
* Wed Oct 04 2023 Shreenidhi Shedi <sshedi@vmware.com> 253.12-1
- Upgrade to v253.12
* Wed Sep 27 2023 Prashant S Chauhan <psinghchauha@vmware.com> 253-9
- Add kbd in Requires for systemd-udev
* Wed Sep 13 2023 Srish Srinivasan <ssrish@vmware.com> 253-8
- Version bump as a part of libmicrohttpd version update
* Fri Sep 01 2023 Guruswamy Basavaiah <bguruswamy@vmware.com> 253-7
- Remove systemd.setenv=SYSTEMD_DEFAULT_MOUNT_RATE_LIMIT_BURST=20
- https://github.com/systemd/systemd/commit/21dd1de
* Mon Jul 17 2023 Piyush Gupta <gpiyush@vmware.com> 253-6
- Revert https://github.com/systemd/systemd/pull/26494.patch.
* Fri Jun 23 2023 Guruswamy Basavaiah <bguruswamy@vmware.com> 253-5
- Increase SYSTEMD_DEFAULT_MOUNT_RATE_LIMIT_BURST to 20
* Tue May 23 2023 Guruswamy Basavaiah <bguruswamy@vmware.com> 253-4
- no coredumps for setuid and setgid binaries
* Fri Apr 14 2023 Shreenidhi Shedi <sshedi@vmware.com> 253-3
- Bump version as a part of zlib upgrade
* Wed Mar 29 2023 Susant Sahani <ssahani@vmware.com> 253-2
- https://github.com/systemd/systemd/pull/26494.patch.
* Thu Feb 16 2023 Susant Sahani <ssahani@vmware.com> 253-1
- Version bump.
* Tue Feb 07 2023 Shreenidhi Shedi <sshedi@vmware.com> 252.4-9
- Fix requires
* Fri Feb 03 2023 Shreenidhi Shedi <sshedi@vmware.com> 252.4-8
- Enable sysusers
- Add a patch to use BFQ scheduler
- Remove test file packaging with main package
* Tue Jan 17 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 252.4-7
- Support OOMPolicy in scope units
* Sat Jan 14 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 252.4-6
- Bump version as a part of gettext upgrade
* Tue Jan 10 2023 Shreenidhi Shedi <sshedi@vmware.com> 252.4-5
- bump version as part of xz upgrade
* Fri Jan 06 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 252.4-4
- Bump up due to change in elfutils
* Tue Jan 03 2023 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 252.4-3
- Switch systemd cmdline to enable cgroup v2 by default
* Thu Dec 22 2022 Guruswamy Basavaiah <bguruswamy@vmware.com> 252.4-2
- Bump release as a part of libgpg-error upgrade to 1.46
* Wed Dec 21 2022 Susant Sahani <ssahani@vmware.com> 252.4-1
- Version bump. Use `SendRelease=no` drop false same as IPv6AcceptRA=
* Tue Dec 06 2022 Prashant S Chauhan <psinghchauha@vmware.com> 252.2-3
- Update release to compile with python 3.11
* Wed Nov 30 2022 Shreenidhi Shedi <sshedi@vmware.com> 252.2-2
- Add `SendRelease=false` to default network file.
* Tue Nov 29 2022 Susant Sahani <ssahani@vmware.com> 252.2-1
- Version bump
* Fri Nov 18 2022 Susant Sahani <ssahani@vmware.com> 252.1-1
- Version bump
* Tue Nov 01 2022 Susant Sahani <ssahani@vmware.com> 252-1
- Version bump
* Fri Oct 07 2022 Shreenidhi Shedi <sshedi@vmware.com> 251.4-3
- Bump version as a part of libxslt upgrade
* Tue Aug 30 2022 Shreenidhi Shedi <sshedi@vmware.com> 251.4-2
- Bump version as a part of gnutls upgrade
* Wed Aug 24 2022 Susant Sahani <ssahani@vmware.com> 251.4-1
- Version bump
* Tue Jul 26 2022 Shreenidhi Shedi <sshedi@vmware.com> 251.3-2
- Add libgpg-error-devel to BuildRequires
* Mon Jul 25 2022 Susant Sahani <ssahani@vmware.com> 251.3-1
- Version bump
* Mon Jul 18 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 251-4
- Bump version as a part of python3-lxml upgrade
* Thu Jul 07 2022 Shreenidhi Shedi <sshedi@vmware.com> 251-3
- Enable dns-over-tls support
- Enable default-dns-over-tls=opportunistic support
- Disable DNSSEC & DNSOverTLS by default
* Thu Jun 16 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 251-2
- Bump version as a part of libxslt upgrade
* Tue May 24 2022 Susant Sahani <ssahani@vmware.com>  251-1
- Version bump
* Mon Apr 04 2022 Shreenidhi Shedi <sshedi@vmware.com> 250.4-1
- Upgrade to v250.4
- Fix systemd-boot-update.service failure
* Wed Jan 12 2022 Nitesh Kumar <kunitesh@vmware.com> 250.2-2
- Added postun for systemd-tests.
* Tue Jan 11 2022 Shreenidhi Shedi <sshedi@vmware.com> 250.2-1
- Upgrade to v250.2, this fixes CVE-2021-3997
* Thu Dec 09 2021 Susant Sahani <ssahani@vmware.com> 249.7-1
- Version bump
* Mon Nov 08 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 249.2-3
- Bump up release for openssl
* Thu Aug 19 2021 Shreenidhi Shedi <sshedi@vmware.com> 249.2-2
- Add systemd-rpm-macros to extra build requires
* Mon Aug 02 2021 Susant Sahani <ssahani@vmware.com>  249.2-1
- Version bump and define network, resolve timesyc uid
* Thu Jul 22 2021 Susant Sahani <ssahani@vmware.com>  249.1-1
- Version bump
* Wed Jul 14 2021 Susant Sahani <ssahani@vmware.com>  249-2
- Switch to meson
* Mon Jul 12 2021 Susant Sahani <ssahani@vmware.com>  249-1
- Version bump
* Mon Apr 5 2021 Susant Sahani <ssahani@vmware.com>  248-1
- Version bump
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
- disable-elfutils.
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
