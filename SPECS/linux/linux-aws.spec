%global security_hardening none
Summary:        Kernel
Name:           linux-aws
Version:        4.9.137
Release:        1%{?kat_build:.%kat_build}%{?dist}
License:    	GPLv2
URL:        	http://www.kernel.org/
Group:        	System Environment/Kernel
Vendor:         VMware, Inc.
Distribution: 	Photon
Source0:        http://www.kernel.org/pub/linux/kernel/v4.x/linux-%{version}.tar.xz
%define sha1 linux=bd0e5ecf3bee96cb8c81d90247cb3389cbdc0727
Source1:	config-aws
Source2:	initramfs.trigger
# common
Patch0:         x86-vmware-read-tsc_khz-only-once-at-boot-time.patch
Patch1:         x86-vmware-use-tsc_khz-value-for-calibrate_cpu.patch
Patch2:         x86-vmware-add-basic-paravirt-ops-support.patch
Patch3:         x86-vmware-add-paravirt-sched-clock.patch
Patch4:         x86-vmware-log-kmsg-dump-on-panic.patch
Patch5:         double-tcp_mem-limits.patch
Patch6:         linux-4.9-sysctl-sched_weighted_cpuload_uses_rla.patch
Patch7:         linux-4.9-watchdog-Disable-watchdog-on-virtual-machines.patch
Patch8:         Implement-the-f-xattrat-family-of-functions.patch
Patch9:         SUNRPC-Do-not-reuse-srcport-for-TIME_WAIT-socket.patch
Patch10:        SUNRPC-xs_bind-uses-ip_local_reserved_ports.patch
Patch11:        vsock-transport-for-9p.patch
Patch12:        x86-vmware-sta.patch
#HyperV patches
Patch13:        0004-vmbus-Don-t-spam-the-logs-with-unknown-GUIDs.patch
Patch14:        0005-Drivers-hv-utils-Fix-the-mapping-between-host-versio.patch
Patch15:        0006-Drivers-hv-vss-Improve-log-messages.patch
Patch16:        0007-Drivers-hv-vss-Operation-timeouts-should-match-host-.patch
Patch17:        0008-Drivers-hv-vmbus-Use-all-supported-IC-versions-to-ne.patch
Patch18:        0009-Drivers-hv-Log-the-negotiated-IC-versions.patch
Patch19:        0010-vmbus-fix-missed-ring-events-on-boot.patch
Patch20:        0011-vmbus-remove-goto-error_clean_msglist-in-vmbus_open.patch
Patch21:        0012-vmbus-dynamically-enqueue-dequeue-the-channel-on-vmb.patch
Patch23:        0014-hv_sock-introduce-Hyper-V-Sockets.patch
#FIPS patches - allow some algorithms
Patch24:        0001-Revert-crypto-testmgr-Disable-fips-allowed-for-authe.patch
Patch25:        0002-allow-also-ecb-cipher_null.patch
Patch26:        add-sysctl-to-disallow-unprivileged-CLONE_NEWUSER-by-default.patch
# Fix CVE-2017-1000252
Patch28:        kvm-dont-accept-wrong-gsi-values.patch
Patch30:        vmxnet3-avoid-xmit-reset-due-to-a-race-in-vmxnet3.patch
Patch31:        vmxnet3-use-correct-flag-to-indicate-LRO-feature.patch
Patch32:        netfilter-ipset-pernet-ops-must-be-unregistered-last.patch
Patch33:        vmxnet3-fix-incorrect-dereference-when-rxvlan-is-disabled.patch
# Fixes for CVE-2018-1000026
Patch34:        0001-net-create-skb_gso_validate_mac_len.patch
Patch35:        0002-bnx2x-disable-GSO-where-gso_size-is-too-big-for-hard.patch
# Fix for CVE-2018-8043
Patch38:        0001-net-phy-mdio-bcm-unimac-fix-potential-NULL-dereferen.patch
# Fix for CVE-2017-18241
Patch40:        0001-f2fs-fix-a-panic-caused-by-NULL-flush_cmd_control.patch
Patch42:        0001-hwrng-rdrand-Add-RNG-driver-based-on-x86-rdrand-inst.patch
# Fix for CVE-2017-18232
Patch43:        0001-scsi-libsas-direct-call-probe-and-destruct.patch
# Fix for CVE-2017-18249
Patch44:        0001-f2fs-fix-race-condition-in-between-free-nid-allocator-initializer.patch
# Fix for CVE-2018-10323
Patch45:        0001-xfs-set-format-back-to-extents-if-xfs_bmap_extents_t.patch
# Fix for CVE-2018-10322
Patch46:        0001-xfs-move-inode-fork-verifiers-to-xfs-dinode-verify.patch
Patch47:        0002-xfs-verify-dinode-header-first.patch
Patch48:        0003-xfs-enhance-dinode-verifier.patch

# Out-of-tree patches from AppArmor:
Patch71: 0001-UBUNTU-SAUCE-AppArmor-basic-networking-rules.patch
Patch72: 0002-apparmor-Fix-quieting-of-audit-messages-for-network-.patch
Patch73: 0003-UBUNTU-SAUCE-apparmor-Add-the-ability-to-mediate-mou.patch

# Amazon AWS
Patch101: 0002-lib-cpumask-Make-CPUMASK_OFFSTACK-usable-without-deb.patch
Patch102: 0009-bump-the-default-TTL-to-255.patch
Patch103: 0010-bump-default-tcp_wmem-from-16KB-to-20KB.patch
Patch104: 0012-drivers-introduce-AMAZON_DRIVER_UPDATES.patch
Patch105: 0013-drivers-amazon-add-network-device-drivers-support.patch
Patch106: 0014-drivers-amazon-introduce-AMAZON_IXGBEVF.patch
Patch107: 0015-drivers-amazon-import-out-of-tree-ixgbevf-4.0.3.patch
Patch108: 0016-drivers-amazon-ixgbevf-update-Makefile.patch
Patch109: 0017-drivers-amazon-introduce-AMAZON_ENA_ETHERNET.patch
Patch110: 0018-drivers-amazon-import-out-of-tree-ENA-driver-1.1.3.patch
Patch111: 0019-drivers-amazon-ena-update-Makefile.patch
Patch112: 0020-drivers-amazon-add-block-device-drivers-support.patch
Patch113: 0021-drivers-amazon-introduce-AMAZON_XEN_BLKDEV_FRONTEND.patch
Patch114: 0022-drivers-amazon-import-xen-blkfront-from-the-tree.patch
Patch115: 0023-drivers-amazon-xen-blkfront-add-persistent_grants-pa.patch
Patch116: 0024-drivers-amazon-xen-blkfront-resurrect-request-based-.patch
Patch117: 0025-xen-pvhvm-unplug-block-deivces-driven-by-out-of-tree.patch
Patch118: 0026-drivers-amazon-introduce-AMAZON_GPU_MODULES.patch
Patch119: 0027-drivers-amazon-xen-blkfront-add-uevent-for-size-chan.patch
Patch120: 0028-block-relax-check-on-sg-gap.patch
Patch121: 0029-block-fix-bio_will_gap-for-first-bvec-with-offset.patch
Patch122: 0030-drivers-amazon-ena-update-to-1.2.0.patch
Patch123: 0031-drivers-amazon-xen-blkfront-introduce-macro-to-check.patch
Patch124: 0032-drivers-amazon-xen-blkfront-convert-to-use-blkfront_.patch
Patch125: 0033-drivers-amazon-xen-blkfront-resurrect-per-device-loc.patch
Patch126: 0034-drivers-amazon-xen-blkfront-empty-the-request-queue-.patch
Patch127: 0035-drivers-amazon-xen-blkfront-use-a-right-index-when-c.patch
Patch128: 0036-xen-manage-keep-track-of-the-on-going-suspend-mode.patch
Patch129: 0037-xen-manage-introduce-helper-function-to-know-the-on-.patch
Patch130: 0038-xenbus-add-freeze-thaw-restore-callbacks-support.patch
Patch131: 0039-x86-xen-decouple-shared_info-mapping-from-xen_hvm_in.patch
Patch132: 0040-x86-xen-add-system-core-suspend-and-resume-callbacks.patch
Patch133: 0041-drivers-amazon-xen-blkfront-add-callbacks-for-PM-sus.patch
Patch134: 0042-xen-netfront-add-callbacks-for-PM-suspend-and-hibern.patch
Patch135: 0043-drivers-amazon-ixgbevf-use-pci-drvdata-correctly-in-.patch
Patch136: 0044-xen-time-introduce-xen_-save-restore-_steal_clock.patch
Patch137: 0045-x86-xen-save-and-restore-steal-clock.patch
Patch138: 0046-xen-events-add-xen_shutdown_pirqs-helper-function.patch
Patch139: 0047-x86-xen-close-event-channels-for-PIRQs-in-system-cor.patch
Patch140: 0048-drivers-amazon-ena-update-to-1.3.0.patch
Patch141: 0049-nvme-update-timeout-module-parameter-type.patch
Patch142: 0050-drivers-amazon-xen-blkfront-ensure-no-reqs-rsps-in-r.patch
Patch143: 0051-xen-netfront-add-longer-default-freeze-timeout-as-a-.patch
Patch144: 0052-drivers-amazon-ena-update-to-1.4.0.patch
Patch145: 0053-PM-hibernate-update-the-resume-offset-on-SNAPSHOT_SE.patch
Patch146: 0054-Not-for-upstream-PM-hibernate-Speed-up-hibernation-b.patch


%if 0%{?kat_build:1}
Patch1000:	%{kat_build}.patch
%endif
BuildRequires:  bc
BuildRequires:  kbd
BuildRequires:  kmod-devel
BuildRequires:  glib-devel
BuildRequires:  xerces-c-devel
BuildRequires:  xml-security-c-devel
BuildRequires:  libdnet-devel
BuildRequires:  libmspack-devel
BuildRequires:  Linux-PAM-devel
BuildRequires:  openssl-devel
BuildRequires:  procps-ng-devel
BuildRequires:	audit-devel
Requires:       filesystem kmod
Requires(post):(coreutils or toybox)
%define uname_r %{version}-%{release}-aws

%description
The Linux package contains the Linux kernel.


%package devel
Summary:        Kernel Dev
Group:          System Environment/Kernel
Requires:       %{name} = %{version}-%{release}
Requires:       python2 gawk
%description devel
The Linux package contains the Linux kernel dev files

%package drivers-gpu
Summary:        Kernel GPU Drivers
Group:          System Environment/Kernel
Requires:       %{name} = %{version}-%{release}
%description drivers-gpu
The Linux package contains the Linux kernel drivers for GPU

%package sound
Summary:        Kernel Sound modules
Group:          System Environment/Kernel
Requires:       %{name} = %{version}-%{release}
%description sound
The Linux package contains the Linux kernel sound support

%package docs
Summary:        Kernel docs
Group:          System Environment/Kernel
Requires:       python2
%description docs
The Linux package contains the Linux kernel doc files

%package oprofile
Summary:        Kernel driver for oprofile, a statistical profiler for Linux systems
Group:          System Environment/Kernel
Requires:       %{name} = %{version}-%{release}
%description oprofile
Kernel driver for oprofile, a statistical profiler for Linux systems

%package tools
Summary:        This package contains the 'perf' performance analysis tools for Linux kernel
Group:          System/Tools
Requires:       %{name} = %{version}-%{release}
Requires:       audit
%description tools
This package contains the 'perf' performance analysis tools for Linux kernel.


%prep
%setup -q -n linux-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1
%patch23 -p1
%patch24 -p1
%patch25 -p1
%patch26 -p1
%patch28 -p1
%patch30 -p1
%patch31 -p1
%patch32 -p1
%patch33 -p1
%patch34 -p1
%patch35 -p1
%patch38 -p1
%patch40 -p1
%patch42 -p1
%patch43 -p1
%patch44 -p1
%patch45 -p1
%patch46 -p1
%patch47 -p1
%patch48 -p1

%patch71 -p1
%patch72 -p1
%patch73 -p1

%patch101 -p1
%patch102 -p1
%patch103 -p1
%patch104 -p1
%patch105 -p1
%patch106 -p1
%patch107 -p1
%patch108 -p1
%patch109 -p1
%patch110 -p1
%patch111 -p1
%patch112 -p1
%patch113 -p1
%patch114 -p1
%patch115 -p1
%patch116 -p1
%patch117 -p1
%patch118 -p1
%patch119 -p1
%patch120 -p1
%patch121 -p1
%patch122 -p1
%patch123 -p1
%patch124 -p1
%patch125 -p1
%patch126 -p1
%patch127 -p1
%patch128 -p1
%patch129 -p1
%patch130 -p1
%patch131 -p1
%patch132 -p1
%patch133 -p1
%patch134 -p1
%patch135 -p1
%patch136 -p1
%patch137 -p1
%patch138 -p1
%patch139 -p1
%patch140 -p1
%patch141 -p1
%patch142 -p1
%patch143 -p1
%patch144 -p1
%patch145 -p1
%patch146 -p1


%if 0%{?kat_build:1}
%patch1000 -p1
%endif

%build
make mrproper
cp %{SOURCE1} .config
sed -i 's/CONFIG_LOCALVERSION="-aws"/CONFIG_LOCALVERSION="-%{release}-aws"/' .config
make LC_ALL= oldconfig
make VERBOSE=1 KBUILD_BUILD_VERSION="1-photon" KBUILD_BUILD_HOST="photon" ARCH="x86_64" %{?_smp_mflags}
make -C tools perf

%define __modules_install_post \
for MODULE in `find %{buildroot}/lib/modules/%{uname_r} -name *.ko` ; do \
    ./scripts/sign-file sha512 certs/signing_key.pem certs/signing_key.x509 $MODULE \
    rm -f $MODULE.{sig,dig} \
    xz $MODULE \
    done \
%{nil}

# We want to compress modules after stripping. Extra step is added to
# the default __spec_install_post.
%define __spec_install_post\
    %{?__debug_package:%{__debug_install_post}}\
    %{__arch_install_post}\
    %{__os_install_post}\
    %{__modules_install_post}\
%{nil}

%install
install -vdm 755 %{buildroot}/etc
install -vdm 755 %{buildroot}/boot
install -vdm 755 %{buildroot}%{_defaultdocdir}/%{name}-%{uname_r}
install -vdm 755 %{buildroot}/etc/modprobe.d
install -vdm 755 %{buildroot}/usr/src/%{name}-headers-%{uname_r}
install -vdm 755 %{buildroot}/usr/lib/debug/lib/modules/%{uname_r}
make INSTALL_MOD_PATH=%{buildroot} modules_install

# Verify for build-id match
# We observe different IDs sometimes
# TODO: debug it
ID1=`readelf -n vmlinux | grep "Build ID"`
./scripts/extract-vmlinux arch/x86/boot/bzImage > extracted-vmlinux
ID2=`readelf -n extracted-vmlinux | grep "Build ID"`
if [ "$ID1" != "$ID2" ] ; then
	echo "Build IDs do not match"
	echo $ID1
	echo $ID2
	exit 1
fi
install -vm 644 arch/x86/boot/bzImage %{buildroot}/boot/vmlinuz-%{uname_r}
# Restrict the permission on System.map-X file
install -vm 400 System.map %{buildroot}/boot/System.map-%{uname_r}
install -vm 644 .config %{buildroot}/boot/config-%{uname_r}
cp -r Documentation/*        %{buildroot}%{_defaultdocdir}/%{name}-%{uname_r}
install -vm 644 vmlinux %{buildroot}/usr/lib/debug/lib/modules/%{uname_r}/vmlinux-%{uname_r}
# `perf test vmlinux` needs it
ln -s vmlinux-%{uname_r} %{buildroot}/usr/lib/debug/lib/modules/%{uname_r}/vmlinux

cat > %{buildroot}/boot/%{name}-%{uname_r}.cfg << "EOF"
# GRUB Environment Block
photon_cmdline=init=/lib/systemd/systemd ro loglevel=3 quiet no-vmw-sta
photon_linux=vmlinuz-%{uname_r}
photon_initrd=initrd.img-%{uname_r}
EOF

# Register myself to initramfs
mkdir -p %{buildroot}/%{_localstatedir}/lib/initramfs/kernel
cat > %{buildroot}/%{_localstatedir}/lib/initramfs/kernel/%{uname_r} << "EOF"
--add-drivers "tmem xen-scsifront xen-blkfront xen-acpi-processor xen-evtchn xen-gntalloc xen-gntdev xen-privcmd xen-pciback xenfs hv_utils hv_vmbus hv_storvsc hv_netvsc hv_sock hv_balloon cn"
EOF

#    Cleanup dangling symlinks
rm -rf %{buildroot}/lib/modules/%{uname_r}/source
rm -rf %{buildroot}/lib/modules/%{uname_r}/build

find . -name Makefile* -o -name Kconfig* -o -name *.pl | xargs  sh -c 'cp --parents "$@" %{buildroot}/usr/src/%{name}-headers-%{uname_r}' copy
find arch/x86/include include scripts -type f | xargs  sh -c 'cp --parents "$@" %{buildroot}/usr/src/%{name}-headers-%{uname_r}' copy
find $(find arch/x86 -name include -o -name scripts -type d) -type f | xargs  sh -c 'cp --parents "$@" %{buildroot}/usr/src/%{name}-headers-%{uname_r}' copy
find arch/x86/include Module.symvers include scripts -type f | xargs  sh -c 'cp --parents "$@" %{buildroot}/usr/src/%{name}-headers-%{uname_r}' copy
# CONFIG_STACK_VALIDATION=y requires objtool to build external modules
install -vsm 755 tools/objtool/objtool %{buildroot}/usr/src/%{name}-headers-%{uname_r}/tools/objtool/
install -vsm 755 tools/objtool/fixdep %{buildroot}/usr/src/%{name}-headers-%{uname_r}/tools/objtool/

cp .config %{buildroot}/usr/src/%{name}-headers-%{uname_r} # copy .config manually to be where it's expected to be
ln -sf "/usr/src/%{name}-headers-%{uname_r}" "%{buildroot}/lib/modules/%{uname_r}/build"
find %{buildroot}/lib/modules -name '*.ko' -print0 | xargs -0 chmod u+x

# disable (JOBS=1) parallel build to fix this issue:
# fixdep: error opening depfile: ./.plugin_cfg80211.o.d: No such file or directory
# Linux version that was affected is 4.4.26
make -C tools JOBS=1 DESTDIR=%{buildroot} prefix=%{_prefix} perf_install

%include %{SOURCE2}

%post
/sbin/depmod -aq %{uname_r}
ln -sf %{name}-%{uname_r}.cfg /boot/photon.cfg

%post drivers-gpu
/sbin/depmod -aq %{uname_r}

%post sound
/sbin/depmod -aq %{uname_r}

%post oprofile
/sbin/depmod -aq %{uname_r}

%files
%defattr(-,root,root)
/boot/System.map-%{uname_r}
/boot/config-%{uname_r}
/boot/vmlinuz-%{uname_r}
%config(noreplace) /boot/%{name}-%{uname_r}.cfg
%config %{_localstatedir}/lib/initramfs/kernel/%{uname_r}
/lib/firmware/*
%defattr(0644,root,root)
/lib/modules/%{uname_r}/*
%exclude /lib/modules/%{uname_r}/build
%exclude /lib/modules/%{uname_r}/kernel/drivers/gpu
%exclude /lib/modules/%{uname_r}/kernel/sound
%exclude /lib/modules/%{uname_r}/kernel/arch/x86/oprofile/

%files docs
%defattr(-,root,root)
%{_defaultdocdir}/%{name}-%{uname_r}/*

%files devel
%defattr(-,root,root)
/lib/modules/%{uname_r}/build
/usr/src/%{name}-headers-%{uname_r}

%files drivers-gpu
%defattr(-,root,root)
%exclude /lib/modules/%{uname_r}/kernel/drivers/gpu/drm/cirrus/
/lib/modules/%{uname_r}/kernel/drivers/gpu

%files sound
%defattr(-,root,root)
/lib/modules/%{uname_r}/kernel/sound

%files oprofile
%defattr(-,root,root)
/lib/modules/%{uname_r}/kernel/arch/x86/oprofile/

%files tools
%defattr(-,root,root)
/usr/libexec
%exclude %{_libdir}/debug
/usr/lib64/traceevent
%{_bindir}
/etc/bash_completion.d/*
/usr/share/perf-core/strace/groups/file
/usr/share/doc/*

%changelog
*   Fri Nov 16 2018 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.9.137-1
-   Update to version 4.9.137
*   Tue Oct 02 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.130-2
-   Improve error-handling of rdrand-rng kernel driver.
*   Mon Oct 01 2018 srinidhira0 <srinidhir@vmware.com> 4.9.130-1
-   Update to version 4.9.130
*   Mon Sep 10 2018 Srinidhi Rao <srinidhir@vmware.com> 4.9.124-2
-   Fix for CVE-2018-13053
*   Fri Aug 24 2018 Bo Gan <ganb@vmware.com> 4.9.124-1
-   Update to version 4.9.124
*   Fri Aug 17 2018 Bo Gan <ganb@vmware.com> 4.9.120-1
-   Update to version 4.9.120 (l1tf fixes)
*   Thu Aug 09 2018 Srinidhi Rao <srinidhir@vmware.com> 4.9.118-2
-   Fix CVE-2018-12233
*   Tue Aug 07 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.118-1
-   Update to version 4.9.118
*   Mon Jul 30 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.116-1
-   Update to version 4.9.116 and clear stack on fork.
*   Mon Jul 23 2018 srinidhira0 <srinidhir@vmware.com> 4.9.114-1
-   Update to version 4.9.114
*   Thu Jul 19 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.111-5
-   Apply out-of-tree patches needed for AppArmor.
*   Tue Jul 17 2018 Srinidhi Rao <srinidhir@vmware.com> 4.9.111-4
-   Fix CVE-2018-10322
*   Thu Jul 12 2018 Srinidhi Rao <srinidhir@vmware.com> 4.9.111-3
-   Fix CVE-2017-18232, CVE-2017-18249 and CVE-2018-10323
*   Wed Jul 11 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.111-2
-   Enable and use AppArmor security module by default.
*   Sat Jul 07 2018 Alexey Makhalov <amakhalov@vmware.com> 4.9.111-1
-   Update to version 4.9.111
*   Wed Jun 27 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.109-2
-   Add rdrand-based RNG driver to enhance kernel entropy.
*   Thu Jun 21 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.109-1
-   Update to version 4.9.109
*   Mon May 21 2018 Alexey Makhalov <amakhalov@vmware.com> 4.9.101-2
-   Add the f*xattrat family of syscalls.
*   Mon May 21 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.101-1
-   Update to version 4.9.101 and fix CVE-2018-3639.
*   Wed May 09 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.99-1
-   Update to version 4.9.99
*   Fri May 04 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.98-2
-   Fix CVE-2017-18216, CVE-2018-8043, CVE-2018-8087, CVE-2017-18241,
-   CVE-2017-18224.
-   Disable floppy driver support (CONFIG_BLK_DEV_FD) in config-aws.
*   Fri May 04 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.98-1
-   Update to version 4.9.98
*   Wed May 02 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.97-3
-   Fix CVE-2017-18255.
*   Tue May 01 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.97-2
-   Fix CVE-2018-1000026.
*   Mon Apr 30 2018 Alexey Makhalov <amakhalov@vmware.com> 4.9.97-1
-   Update to version 4.9.97. Apply 3rd vmxnet3 patch.
*   Mon Apr 23 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.94-2
-   Add full retpoline support by building with retpoline-enabled gcc.
*   Wed Apr 18 2018 Alexey Makhalov <amakhalov@vmware.com> 4.9.94-1
-   Update to version 4.9.94. Fix panic in ip_set.
*   Mon Apr 02 2018 Alexey Makhalov <amakhalov@vmware.com> 4.9.92-1
-   Update to version 4.9.92. Apply vmxnet3 patches.
*   Tue Mar 27 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.90-1
-   Update to version 4.9.90
*   Thu Mar 22 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.89-1
-   Update to version 4.9.89
*   Fri Mar 16 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.80-4
-   Tweak config options to fix issues on AWS.
*   Thu Mar 1 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.80-3
-   Fix upgrade issue by removing 'Obsoletes: linux-dev'.
*   Mon Feb 19 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.80-2
-   Add enhancements from Amazon.
*   Mon Feb 05 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.80-1
-   First build based on linux.spec and config. No AWS-specific patches yet.
