%global security_hardening none
%global photon_checksum_generator_version 1.2
Summary:        Kernel
Name:           linux-aws
Version:        4.19.214
Release:        2%{?kat_build:.kat}%{?dist}
License:    	GPLv2
URL:        	http://www.kernel.org/
Group:        	System Environment/Kernel
Vendor:         VMware, Inc.
Distribution: 	Photon

%define uname_r %{version}-%{release}-aws

Source0:        http://www.kernel.org/pub/linux/kernel/v4.x/linux-%{version}.tar.xz
%define sha1 linux=0e29837f0d1ce72085e5ee9225927683f2e44ee1
Source1:        config-aws
Source2:        initramfs.trigger
Source3:        pre-preun-postun-tasks.inc
Source4:        check_for_config_applicability.inc
# Photon-checksum-generator kernel module
Source5:        https://github.com/vmware/photon-checksum-generator/releases/photon-checksum-generator-%{photon_checksum_generator_version}.tar.gz
%define sha1 photon-checksum-generator=20658a922c0beca840942bf27d743955711c043a
Source6:        genhmac.inc

# common
Patch0:         linux-4.14-Log-kmsg-dump-on-panic.patch
Patch1:         double-tcp_mem-limits.patch
# TODO: disable this patch, check for regressions
#Patch2:         linux-4.9-watchdog-Disable-watchdog-on-virtual-machines.patch
Patch3:         SUNRPC-Do-not-reuse-srcport-for-TIME_WAIT-socket.patch
Patch4:         SUNRPC-xs_bind-uses-ip_local_reserved_ports.patch
Patch5:         vsock-transport-for-9p.patch
Patch6:         4.18-x86-vmware-STA-support.patch
Patch7:         vsock-delay-detach-of-QP-with-outgoing-data.patch
Patch10:        0001-cgroup-v1-cgroup_stat-support.patch
#HyperV patches
Patch13:        0004-vmbus-Don-t-spam-the-logs-with-unknown-GUIDs.patch

# TODO: Is CONFIG_HYPERV_VSOCKETS the same?
#Patch23:        0014-hv_sock-introduce-Hyper-V-Sockets.patch
Patch26:        4.18-add-sysctl-to-disallow-unprivileged-CLONE_NEWUSER-by-default.patch
# Fix CVE-2017-1000252
Patch28:        kvm-dont-accept-wrong-gsi-values.patch
# Out-of-tree patches from AppArmor:
Patch29:        4.17-0001-apparmor-patch-to-provide-compatibility-with-v2.x-ne.patch
Patch30:        4.17-0002-apparmor-af_unix-mediation.patch
Patch31:        4.17-0003-apparmor-fix-use-after-free-in-sk_peer_label.patch
# RDRAND-based RNG driver to enhance the kernel's entropy pool:
Patch32:        4.18-0001-hwrng-rdrand-Add-RNG-driver-based-on-x86-rdrand-inst.patch
# Fix for CVE-2019-12456
Patch33:        0001-scsi-mpt3sas_ctl-fix-double-fetch-bug-in-_ctl_ioctl_.patch
# Fix for CVE-2019-12379
Patch34:        0001-consolemap-Fix-a-memory-leaking-bug-in-drivers-tty-v.patch
# Fix for CVE-2019-12380
Patch35:        0001-efi-x86-Add-missing-error-handling-to-old_memmap-1-1.patch
# Fix for CVE-2019-12381
Patch36:        0001-ip_sockglue-Fix-missing-check-bug-in-ip_ra_control.patch
# Fix for CVE-2019-12378
Patch38:        0001-ipv6_sockglue-Fix-a-missing-check-bug-in-ip6_ra_cont.patch
# Fix for CVE-2019-12455
Patch39:        0001-clk-sunxi-fix-a-missing-check-bug-in-sunxi_divs_clk_.patch
#Fix for CVE-2019-20908
Patch40:        efi-Restrict-efivar_ssdt_load-when-the-kernel-is-locked-down.patch
#Fix for CVE-2019-19338
Patch41:        0001-KVM-vmx-implement-MSR_IA32_TSX_CTRL-disable-RTM-func.patch
Patch42:        0001-KVM-vmx-use-MSR_IA32_TSX_CTRL-to-hard-disable-TSX-on.patch
# Fix for CVE-2020-16119
Patch55:        0001-dccp-ccid-move-timers-to-struct-dccp_sock.patch
Patch56:        0002-Revert-dccp-don-t-free-ccid2_hc_tx_sock-struct-in-dc.patch
#Fix for CVE-2020-16120
Patch57:        0001-ovl-pass-correct-flags-for-opening-real-directory.patch
Patch58:        0002-ovl-switch-to-mounter-creds-in-readdir.patch
Patch59:        0003-ovl-verify-permissions-in-ovl_path_open.patch
Patch60:        0004-ovl-call-secutiry-hook-in-ovl_real_ioctl.patch
Patch61:        0005-ovl-check-permission-to-open-real-file.patch

# Fix for CVE-2019-19770
Patch62:        0001-block-revert-back-to-synchronous-request_queue-remov.patch
Patch63:        0002-block-create-the-request_queue-debugfs_dir-on-regist.patch

# Upgrade vmxnet3 driver to version 4
Patch80:        0000-vmxnet3-turn-off-lro-when-rxcsum-is-disabled.patch
Patch81:        0001-vmxnet3-prepare-for-version-4-changes.patch
Patch82:        0002-vmxnet3-add-support-to-get-set-rx-flow-hash.patch
Patch83:        0003-vmxnet3-add-geneve-and-vxlan-tunnel-offload-support.patch
Patch84:        0004-vmxnet3-update-to-version-4.patch
Patch85:        0005-vmxnet3-use-correct-hdr-reference-when-packet-is-enc.patch
Patch86:        0006-vmxnet3-allow-rx-flow-hash-ops-only-when-rss-is-enab.patch
Patch87:        0007-vmxnet3-use-correct-tcp-hdr-length-when-packet-is-en.patch
Patch88:        0008-vmxnet3-fix-cksum-offload-issues-for-non-udp-tunnels.patch

Patch89:        0009-vmxnet3-Remove-buf_info-from-device-accessible-struc.patch

# Patch to add drbg_pr_ctr_aes256 test vectors to testmgr
Patch97:        0001-Add-drbg_pr_ctr_aes256-test-vectors-and-test-to-test.patch
# Patch to call drbg and dh crypto tests from tcrypt
Patch98:        0001-tcrypt-disable-tests-that-are-not-enabled-in-photon.patch
# Disable tcrypt from tcrypt
Patch99:        0001-linux-aws-tcrypt-Remove-tests-for-deflate.patch
# Patch to perform continuous testing on RNG from Noise Source
Patch100:       0001-crypto-drbg-add-FIPS-140-2-CTRNG-for-noise-source.patch

# Amazon AWS
Patch101: 0002-watchdog-Disable-watchdog-on-virtual-machines.patch
Patch102: 0004-bump-the-default-TTL-to-255.patch
Patch103: 0005-bump-default-tcp_wmem-from-16KB-to-20KB.patch
Patch105: 0009-drivers-introduce-AMAZON_DRIVER_UPDATES.patch
Patch106: 0010-drivers-amazon-add-network-device-drivers-support.patch
Patch107: 0011-drivers-amazon-introduce-AMAZON_ENA_ETHERNET.patch
Patch108: 0012-Importing-Amazon-ENA-driver-1.5.0-into-amazon-4.14.y.patch
Patch109: 0013-xen-manage-keep-track-of-the-on-going-suspend-mode.patch
Patch110: 0014-xen-manage-introduce-helper-function-to-know-the-on-.patch
Patch111: 0015-xenbus-add-freeze-thaw-restore-callbacks-support.patch
Patch112: 0016-x86-xen-Introduce-new-function-to-map-HYPERVISOR_sha.patch
Patch113: 0017-x86-xen-add-system-core-suspend-and-resume-callbacks.patch
Patch114: 0018-xen-blkfront-add-callbacks-for-PM-suspend-and-hibern.patch
Patch115: 0019-xen-netfront-add-callbacks-for-PM-suspend-and-hibern.patch
Patch116: 0020-xen-time-introduce-xen_-save-restore-_steal_clock.patch
Patch117: 0021-x86-xen-save-and-restore-steal-clock.patch
Patch118: 0022-xen-events-add-xen_shutdown_pirqs-helper-function.patch
Patch119: 0023-x86-xen-close-event-channels-for-PIRQs-in-system-cor.patch
Patch120: 0024-PM-hibernate-update-the-resume-offset-on-SNAPSHOT_SE.patch
Patch121: 0025-Not-for-upstream-PM-hibernate-Speed-up-hibernation-b.patch
Patch122: 0026-xen-blkfront-resurrect-request-based-mode.patch
Patch123: 0027-xen-blkfront-add-persistent_grants-parameter.patch
Patch125: 0029-Revert-xen-dont-fiddle-with-event-channel-masking-in.patch
Patch131: 0035-xen-blkfront-Fixed-blkfront_restore-to-remove-a-call.patch
Patch133: 0037-x86-tsc-avoid-system-instability-in-hibernation.patch
Patch152: 0056-Amazon-ENA-driver-Update-to-version-1.6.0.patch

#fix for CVE-2020-36322
Patch153:       0001-fuse-Switch-to-using-async-direct-IO-for-FOPEN_DIREC.patch
Patch154:       0002-fuse-lift-bad-inode-checks-into-callers.patch
Patch155:       0003-fuse-fix-bad-inode.patch

#fix for CVE-2021-28950
Patch156:       0001-fuse-fix-live-lock-in-fuse_iget.patch

%if 0%{?kat_build:1}
Patch1000:	fips-kat-tests.patch
%endif

BuildArch:      x86_64
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
Requires(pre): (coreutils or toybox)
Requires(preun): (coreutils or toybox)
Requires(post): (coreutils or toybox)
Requires(postun): (coreutils or toybox)

%description
The Linux package contains the Linux kernel.

%package devel
Summary:        Kernel Dev
Group:          System Environment/Kernel
Requires:       %{name} = %{version}-%{release}
Requires:       python3 gawk
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
Requires:       python3
%description docs
The Linux package contains the Linux kernel doc files

%package hmacgen
Summary:	HMAC SHA256/HMAC SHA512 generator
Group:		System Environment/Kernel
Requires:      %{name} = %{version}-%{release}
Enhances:       %{name}
%description hmacgen
This Linux package contains hmac sha generator kernel module.

%ifarch x86_64
%package oprofile
Summary:        Kernel driver for oprofile, a statistical profiler for Linux systems
Group:          System Environment/Kernel
Requires:       %{name} = %{version}-%{release}
%description oprofile
Kernel driver for oprofile, a statistical profiler for Linux systems
%endif

%prep
# Using autosetup is not feasible
%setup -q -n linux-%{version}
# Using autosetup is not feasible
%setup -D -b 5 -n linux-%{version}

%patch0 -p1
%patch1 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch10 -p1
%patch13 -p1
%patch26 -p1
%patch28 -p1
%patch29 -p1
%patch30 -p1
%patch31 -p1
%patch32 -p1
%patch33 -p1
%patch34 -p1
%patch35 -p1
%patch36 -p1
%patch38 -p1
%patch39 -p1
%patch40 -p1
%patch41 -p1
%patch42 -p1
%patch55 -p1
%patch56 -p1
%patch57 -p1
%patch58 -p1
%patch59 -p1
%patch60 -p1
%patch61 -p1
%patch62 -p1
%patch63 -p1

%patch80 -p1
%patch81 -p1
%patch82 -p1
%patch83 -p1
%patch84 -p1
%patch85 -p1
%patch86 -p1
%patch87 -p1
%patch88 -p1

%patch89 -p1

%patch97 -p1
%patch98 -p1
%patch99 -p1
%patch100 -p1

%patch101 -p1
%patch102 -p1
%patch103 -p1
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
%patch125 -p1
%patch131 -p1
%patch133 -p1
%patch152 -p1
%patch153 -p1
%patch154 -p1
%patch155 -p1
%patch156 -p1

%if 0%{?kat_build:1}
%patch1000 -p1
%endif

%build
make %{?_smp_mflags} mrproper

%ifarch x86_64
cp %{SOURCE1} .config
arch="x86_64"
archdir="x86"
%endif

sed -i 's/CONFIG_LOCALVERSION="-aws"/CONFIG_LOCALVERSION="-%{release}-aws"/' .config

%include %{SOURCE4}

make VERBOSE=1 KBUILD_BUILD_VERSION="1-photon" KBUILD_BUILD_HOST="photon" ARCH=${arch} %{?_smp_mflags}

#build photon-checksum-generator module
bldroot=`pwd`
pushd ../photon-checksum-generator-%{photon_checksum_generator_version}/kernel
make -C $bldroot M=`pwd` modules %{?_smp_mflags}
popd

%define __modules_install_post \
for MODULE in `find %{buildroot}/lib/modules/%{uname_r} -name *.ko` ; do \
    ./scripts/sign-file sha512 certs/signing_key.pem certs/signing_key.x509 $MODULE \
    rm -f $MODULE.{sig,dig} \
    xz $MODULE \
    done \
%{nil}

%include %{SOURCE6}

# We want to compress modules after stripping. Extra step is added to
# the default __spec_install_post.
%define __spec_install_post\
    %{?__debug_package:%{__debug_install_post}}\
    %{__arch_install_post}\
    %{__os_install_post}\
    %{__modules_install_post}\
    %{__modules_gen_hmac}\
%{nil}

%install
install -vdm 755 %{buildroot}/etc
install -vdm 755 %{buildroot}/boot
install -vdm 755 %{buildroot}%{_defaultdocdir}/%{name}-%{uname_r}
install -vdm 755 %{buildroot}/usr/src/%{name}-headers-%{uname_r}
install -vdm 755 %{buildroot}/usr/lib/debug/lib/modules/%{uname_r}
make INSTALL_MOD_PATH=%{buildroot} modules_install %{?_smp_mflags}

#install photon-checksum-generator module
bldroot=`pwd`
pushd ../photon-checksum-generator-%{photon_checksum_generator_version}/kernel
make -C $bldroot M=`pwd` INSTALL_MOD_PATH=%{buildroot} modules_install %{?_smp_mflags}
popd

%ifarch x86_64

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
%endif

# Restrict the permission on System.map-X file
install -vm 400 System.map %{buildroot}/boot/System.map-%{uname_r}
install -vm 644 .config %{buildroot}/boot/config-%{uname_r}
cp -r Documentation/*        %{buildroot}%{_defaultdocdir}/%{name}-%{uname_r}
install -vm 644 vmlinux %{buildroot}/usr/lib/debug/lib/modules/%{uname_r}/vmlinux-%{uname_r}
# `perf test vmlinux` needs it
ln -s vmlinux-%{uname_r} %{buildroot}/usr/lib/debug/lib/modules/%{uname_r}/vmlinux

cat > %{buildroot}/boot/%{name}-%{uname_r}.cfg << "EOF"
# GRUB Environment Block
photon_cmdline=init=/lib/systemd/systemd ro loglevel=3 quiet no-vmw-sta nvme_core.io_timeout=4294967295 cgroup.memory=nokmem
photon_linux=vmlinuz-%{uname_r}
photon_initrd=initrd.img-%{uname_r}
EOF

# Register myself to initramfs
mkdir -p %{buildroot}/%{_localstatedir}/lib/initramfs/kernel
cat > %{buildroot}/%{_localstatedir}/lib/initramfs/kernel/%{uname_r} << "EOF"
--add-drivers "tmem xen-scsifront xen-blkfront xen-evtchn xen-gntalloc xen-gntdev xen-privcmd xen-pciback xenfs hv_utils hv_vmbus hv_storvsc hv_netvsc hv_sock hv_balloon dm-mod nvme nvme-core"
EOF

#    Cleanup dangling symlinks
rm -rf %{buildroot}/lib/modules/%{uname_r}/source
rm -rf %{buildroot}/lib/modules/%{uname_r}/build

find . -name Makefile* -o -name Kconfig* -o -name *.pl | xargs  sh -c 'cp --parents "$@" %{buildroot}/usr/src/%{name}-headers-%{uname_r}' copy
find arch/${archdir}/include include scripts -type f | xargs  sh -c 'cp --parents "$@" %{buildroot}/usr/src/%{name}-headers-%{uname_r}' copy
find $(find arch/${archdir} -name include -o -name scripts -type d) -type f | xargs  sh -c 'cp --parents "$@" %{buildroot}/usr/src/%{name}-headers-%{uname_r}' copy
find arch/${archdir}/include Module.symvers include scripts -type f | xargs  sh -c 'cp --parents "$@" %{buildroot}/usr/src/%{name}-headers-%{uname_r}' copy
%ifarch x86_64
# CONFIG_STACK_VALIDATION=y requires objtool to build external modules
install -vsm 755 tools/objtool/objtool %{buildroot}/usr/src/%{name}-headers-%{uname_r}/tools/objtool/
install -vsm 755 tools/objtool/fixdep %{buildroot}/usr/src/%{name}-headers-%{uname_r}/tools/objtool/
%endif

cp .config %{buildroot}/usr/src/%{name}-headers-%{uname_r} # copy .config manually to be where it's expected to be
ln -sf "/usr/src/%{name}-headers-%{uname_r}" "%{buildroot}/lib/modules/%{uname_r}/build"
find %{buildroot}/lib/modules -name '*.ko' -print0 | xargs -0 chmod u+x

# disable (JOBS=1) parallel build to fix this issue:
# fixdep: error opening depfile: ./.plugin_cfg80211.o.d: No such file or directory
# Linux version that was affected is 4.4.26

%include %{SOURCE2}
%include %{SOURCE3}

%post
/sbin/depmod -aq %{uname_r}
ln -sf %{name}-%{uname_r}.cfg /boot/photon.cfg

%post hmacgen
/sbin/depmod -a %{uname_r}

%post drivers-gpu
/sbin/depmod -aq %{uname_r}

%post sound
/sbin/depmod -aq %{uname_r}

%ifarch x86_64
%post oprofile
/sbin/depmod -aq %{uname_r}
%endif

%files
%defattr(-,root,root)
/boot/System.map-%{uname_r}
/boot/config-%{uname_r}
/boot/vmlinuz-%{uname_r}
/boot/.vmlinuz-%{uname_r}.hmac
%config(noreplace) /boot/%{name}-%{uname_r}.cfg
%config %{_localstatedir}/lib/initramfs/kernel/%{uname_r}
%defattr(0644,root,root)
/lib/modules/%{uname_r}/*
%exclude /lib/modules/%{uname_r}/build
%exclude /lib/modules/%{uname_r}/kernel/drivers/gpu
%exclude /lib/modules/%{uname_r}/kernel/sound
%exclude /lib/modules/%{uname_r}/extra/hmac_generator.ko.xz
%exclude /lib/modules/%{uname_r}/extra/.hmac_generator.ko.xz.hmac
%ifarch x86_64
%exclude /lib/modules/%{uname_r}/kernel/arch/x86/oprofile/
%endif

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

%files hmacgen
%defattr(-,root,root)
/lib/modules/%{uname_r}/extra/hmac_generator.ko.xz
/lib/modules/%{uname_r}/extra/.hmac_generator.ko.xz.hmac

%files sound
%defattr(-,root,root)
/lib/modules/%{uname_r}/kernel/sound

%ifarch x86_64
%files oprofile
%defattr(-,root,root)
/lib/modules/%{uname_r}/kernel/arch/x86/oprofile/
%endif

%changelog
*   Fri Oct 29 2021 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 4.19.214-2
-   Fix for CVE-2020-36322/CVE-2021-28950
*   Thu Oct 28 2021 Sharan Turlapati <sturlapati@vmware.com> 4.19.214-1
-   Update to version 4.19.214
*   Wed Sep 29 2021 Keerthana K <keerthanak@vmware.com> 4.19.208-1
-   Update to version 4.19.208
*   Fri Aug 27 2021 srinidhira0 <srinidhir@vmware.com> 4.19.205-1
-   Update to version 4.19.205
*   Wed Aug 11 2021 Vikash Bansal <bvikas@vmware.com> 4.19.198-2
-   Remove deflate tests from tcrypt
*   Tue Jul 27 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.198-1
-   Update to version 4.19.198
*   Thu Jul 15 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.191-3
-   Fix for CVE-2021-33909
*   Tue Jun 22 2021 Sharan Turlapati <sturlapati@vmware.com> 4.19.191-2
-   Fix for CVE-2021-3609
*   Tue Jun 01 2021 Keerthana K <keerthanak@vmware.com> 4.19.191-1
-   Update to version 4.19.191
*   Mon May 17 2021 Ajay Kaher <akaher@vmware.com> 4.19.190-1
-   Update to version 4.19.190
*   Wed May 12 2021 Sharan Turlapati <sturlapati@vmware.com> 4.19.189-3
-   Fix for CVE-2021-23133
*   Tue May 04 2021 Sharan Turlapati <sturlapati@vmware.com> 4.19.189-2
-   Remove buf_info from device accessible structures in vmxnet3
*   Thu Apr 29 2021 Ankit Jain <ankitja@vmware.com> 4.19.189-1
-   Update to version 4.19.189
*   Tue Apr 20 2021 Ankit Jain <ankitja@vmware.com> 4.19.186-3
-   Fix for CVE-2021-3444
*   Mon Apr 19 2021 Sharan Turlapati <sturlapati@vmware.com> 4.19.186-2
-   Fix for CVE-2021-23133
*   Mon Apr 19 2021 srinidhira0 <srinidhir@vmware.com> 4.19.186-1
-   Update to version 4.19.186
*   Thu Apr 15 2021 Keerthana K <keerthanak@vmware.com> 4.19.182-3
-   photon-checksum-generator update to v1.2
*   Tue Apr 06 2021 Alexey Makhalov <amakhalov@vmware.com> 4.19.182-2
-   Disable kernel accounting for memory cgroups
-   Enable cgroup v1 stats
-   .config: enable PERCPU_STATS
*   Mon Mar 22 2021 srinidhira0 <srinidhir@vmware.com> 4.19.182-1
-   Update to version 4.19.182
*   Fri Feb 26 2021 Sharan Turlapati <sturlapati@vmware.com> 4.19.177-1
-   Update to version 4.19.177
*   Fri Feb 19 2021 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.174-2
-   Fix /boot/photon.cfg symlink when /boot is a separate partition.
*   Tue Feb 09 2021 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.174-1
-   Update to version 4.19.174
*   Tue Jan 12 2021 Ankit Jain <ankitja@vmware.com> 4.19.164-2
-   Disabled CONFIG_TARGET_CORE to fix CVE-2020-28374
*   Mon Jan 04 2021 Ankit Jain <ankitja@vmware.com> 4.19.164-1
-   Update to version 4.19.164
*   Mon Dec 21 2020 Ajay Kaher <akaher@vmware.com> 4.19.163-2
-   Fix for CVE-2020-29569
*   Tue Dec 15 2020 Vikash Bansal <bvikas@vmware.com> 4.19.163-1
-   Update to version 4.19.163
*   Wed Dec 09 2020 Srinidhi Rao <srinidhir@vmware.com> 4.19.160-2
-   Fix for CVE-2019-19770
*   Tue Nov 24 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.160-1
-   Update to version 4.19.160
-   Fix CVE-2019-19338 and CVE-2019-20908
*   Mon Nov 16 2020 Vikash Bansal <bvikas@vmware.com> 4.19.154-6
-   hmacgen: Add path_put to hmac_gen_hash
*   Fri Nov 13 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.154-5
-   Fix CVE-2020-25668
*   Tue Nov 10 2020 Keerthana K <keerthanak@vmware.com> 4.19.154-4
-   Fix slab-out-of-bounds read in fbcon
*   Tue Nov 10 2020 Keerthana K <keerthanak@vmware.com> 4.19.154-3
-   Fix CVE-2020-8694
*   Fri Nov 06 2020 Keerthana K <keerthanak@vmware.com> 4.19.154-2
-   Fix CVE-2020-25704
*   Mon Nov 02 2020 Keerthana K <keerthanak@vmware.com> 4.19.154-1
-   Update to version 4.19.154
*   Wed Oct 14 2020 Ajay Kaher <akaher@vmware.com> 4.19.150-1
-   Update to version 4.19.150
*   Wed Oct 14 2020 Ajay Kaher <akaher@vmware.com> 4.19.148-5
-   Fix for CVE-2020-16120
*   Mon Oct 12 2020 Ankit Jain <ankitja@vmware.com> 4.19.148-4
-   Fix for CVE-2020-16119
*   Wed Oct 07 2020 Ajay Kaher <akaher@vmware.com> 4.19.148-3
-   Fix mp_irqdomain_activate crash
*   Tue Oct 06 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.148-2
-   Fix IPIP encapsulation issue in vmxnet3 driver.
*   Mon Sep 28 2020 Ajay Kaher <akaher@vmware.com> 4.19.148-1
-   Update to version 4.19.148
*   Wed Sep 23 2020 Ajay Kaher <akaher@vmware.com> 4.19.145-4
-   Fix for CVE-2020-14390
*   Wed Sep 23 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.145-3
-   Fix for CVE-2019-19813 and CVE-2019-19816
*   Tue Sep 22 2020 Ajay Kaher <akaher@vmware.com> 4.19.145-2
-   Fix for CVE-2020-25211
*   Tue Sep 15 2020 Vikash Bansal <bvikas@vmware.com> 4.19.145-1
-   Update to version 4.19.145
*   Mon Sep 07 2020 Vikash Bansal <bvikas@vmware.com> 4.19.138-2
-   Fix for CVE-2020-14386
*   Sat Aug 08 2020 ashwin-h <ashwinh@vmware.com> 4.19.138-1
-   Update to version 4.19.138
*   Tue Aug 04 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.132-3
-   Upgrade vmxnet3 driver to version 4
*   Sun Jul 26 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.132-2
-   Fix CVE-2020-14331
*   Thu Jul 16 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.132-1
-   Update to version 4.19.132
*   Sat Jun 27 2020 Keerthana K <keerthanak@vmware.com> 4.19.129-1
-   Update to version 4.19.129
*   Tue Jun 23 2020 Ajay Kaher <akaher@vmware.com> 4.19.126-2
-   Fix for CVE-2020-12888
*   Fri Jun 05 2020 Vikash Bansal <bvikas@vmware.com> 4.19.126-1
-   Update to version 4.19.126
*   Thu Jun 04 2020 Ajay Kaher <akaher@vmware.com> 4.19.124-2
-   Fix for CVE-2020-10757
*   Thu May 28 2020 Ajay Kaher <akaher@vmware.com> 4.19.124-1
-   Update to version 4.19.124
*   Thu May 28 2020 Shreenidhi Shedi <sshedi@vmware.com> 4.19.115-6
-   Keep modules of running kernel till next boot
*   Fri May 22 2020 Ashwin H <ashwinh@vmware.com> 4.19.115-5
-   Fix for CVE-2018-20669
*   Fri May 15 2020 Vikash Bansal <bvikas@vmware.com> 4.19.115-4
-   Fix for CVE-2019-18885
*   Wed May 06 2020 Siddharth Chandrasekaran <csiddharth@vmware.com> 4.19.115-3
-   Add patch to fix CVE-2020-10711
*   Wed Apr 29 2020 Keerthana K <keerthanak@vmware.com> 4.19.115-2
-   Photon-checksum-generator version update to 1.1.
*   Mon Apr 13 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.115-1
-   Update to version 4.19.115
*   Wed Apr 08 2020 Vikash Bansal <bvikas@vmware.com> 4.19.112-2
-   HMAC-SHA256 digest of hmac_generator module moved to hmacgen package
*   Mon Mar 23 2020 Keerthana K <keerthanak@vmware.com> 4.19.112-1
-   Update to version 4.19.112
*   Tue Mar 17 2020 Vikash Bansal <bvikas@vmware.com> 4.19.104-3
-   hmac generation of crypto modules and initrd generation changes if fips=1
*   Mon Mar 16 2020 Keerthana K <keerthanak@vmware.com> 4.19.104-2
-   Adding Enhances depedency to hmacgen.
*   Mon Mar 09 2020 Siddharth Chandrasekaran <csiddharth@vmware.com> 4.19.104-1
-   Update to version 4.19.104
*   Wed Mar 04 2020 Vikash Bansal <bvikas@vmware.com> 4.19.97-5
-   Backporting of patch continuous testing of RNG from urandom
*   Tue Feb 25 2020 Ajay Kaher <akaher@vmware.com> 4.19.97-4
-   Fix CVE-2019-16234
*   Tue Feb 11 2020 Keerthana K <keerthanak@vmware.com> 4.19.97-3
-   Add photon-checksum-generator source tarball and remove hmacgen patch.
-   Exclude hmacgen.ko from base package.
*   Wed Jan 29 2020 Keerthana K <keerthanak@vmware.com> 4.19.97-2
-   Update tcrypt to test drbg_pr_sha256 and drbg_nopr_sha256.
-   Update testmgr to add drbg_pr_ctr_aes256 test vectors.
*   Fri Jan 17 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.97-1
-   Update to version 4.19.97
*   Thu Jan 02 2020 Keerthana K <keerthanak@vmware.com> 4.19.87-3
-   Modify tcrypt to remove tests for algorithms that are not supported in photon.
-   Added tests for DH, DRBG algorithms.
*   Fri Dec 20 2019 Keerthana K <keerthanak@vmware.com> 4.19.87-2
-   Update fips Kat tests.
*   Fri Dec 06 2019 Ajay Kaher <akaher@vmware.com> 4.19.87-1
-   Update to version 4.19.87
*   Thu Dec 05 2019 Ajay Kaher <akaher@vmware.com> 4.19.84-4
-   Adding nvme and nvme-core to initrd list
-   Removing unwanted modules from initrd list
*   Tue Dec 03 2019 Keerthana K <keerthanak@vmware.com> 4.19.84-3
-   Adding hmac sha256/sha512 generator kernel module for fips.
*   Tue Nov 26 2019 Ajay Kaher <akaher@vmware.com> 4.19.84-2
-   Fix CVE-2019-19062, CVE-2019-19066, CVE-2019-19072,
-   CVE-2019-19073, CVE-2019-19074, CVE-2019-19078
*   Tue Nov 12 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.84-1
-   Update to version 4.19.84
-   Fix CVE-2019-18814
*   Fri Nov 08 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.82-1
-   Update to version 4.19.82
*   Thu Nov 07 2019 Jorgen Hansen (VMware) <jhansen@vmware.com> 4.19.79-2
-   Fix vsock QP detach with outgoing data
*   Thu Oct 17 2019 Ajay Kaher <akaher@vmware.com> 4.19.79-1
-   Update to version 4.19.79
-   Fix CVE-2019-17133
*   Thu Oct 10 2019 Harinadh D <hdommaraju@vmware.com> 4.19.76-2
-   Adding lvm and dm-mod modules to support root as lvm
*   Wed Oct 02 2019 Ajay Kaher <akaher@vmware.com> 4.19.76-1
-   Update to version 4.19.76
*   Thu Sep 19 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.72-2
-   Avoid oldconfig which leads to potential build hang
*   Wed Sep 11 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.72-1
-   Update to version 4.19.72
*   Fri Aug 30 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.69-1
-   Update to version 4.19.69
*   Tue Aug 06 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.65-1
-   Update to version 4.19.65
-   Fix CVE-2019-1125 (SWAPGS)
*   Tue Jul 30 2019 Keerthana K <keerthanak@vmware.com> 4.19.52-3
-   Fix Postun scriplet
*   Thu Jun 27 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.52-2
-   Deprecate linux-aws-tools in favor of linux-tools.
*   Mon Jun 17 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.52-1
-   Update to version 4.19.52
-   Fix CVE-2019-12456, CVE-2019-12379, CVE-2019-12380, CVE-2019-12381,
-   CVE-2019-12382, CVE-2019-12378, CVE-2019-12455
*   Thu May 23 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.40-3
-   Fix CVE-2019-11191 by deprecating a.out file format support.
*   Tue May 14 2019 Keerthana K <keerthanak@vmware.com> 4.19.40-2
-   Fix to parse through /boot folder and update symlink (/boot/photon.cfg) if
-   mulitple kernels are installed and current linux kernel is removed.
*   Tue May 07 2019 Ajay Kaher <akaher@vmware.com> 4.19.40-1
-   Update to version 4.19.40
*   Fri Mar 29 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.32-2
-   Fix CVE-2019-10125
*   Wed Mar 27 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.32-1
-   Update to version 4.19.32
*   Thu Mar 14 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.29-1
-   Update to version 4.19.29
*   Tue Mar 05 2019 Ajay Kaher <akaher@vmware.com> 4.19.26-1
-   Update to version 4.19.26
*   Thu Feb 21 2019 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.15-2
-   Fix CVE-2019-8912
*   Tue Jan 15 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.15-1
-   Update to version 4.19.15
*   Mon Jan 07 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.6-2
-   Enable additional security hardening options in the config.
*   Mon Dec 10 2018 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.6-1
-   Update to version 4.19.6
-   Enable EFI in config-aws to support kernel signing.
*   Mon Dec 10 2018 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.1-3
-   Set nvme io_timeout to maximum in kernel cmdline.
*   Wed Nov 14 2018 Ajay Kaher <akaher@vmware.com> 4.19.1-2
-   Adding BuildArch
*   Tue Nov 06 2018 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.1-1
-   Update to version 4.19.1
*   Mon Oct 22 2018 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.18.9-1
-   Update to version 4.18.9
*   Mon Oct 08 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.14.67-2
-   Add enhancements from Amazon.
*   Wed Sep 19 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.14.67-1
-   Update to version 4.14.67
*   Tue Sep 18 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.14.54-4
-   Add rdrand-based RNG driver to enhance kernel entropy.
*   Sun Sep 02 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.14.54-3
-   Add full retpoline support by building with retpoline-enabled gcc.
*   Thu Aug 30 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.14.54-2
-   Apply out-of-tree patches needed for AppArmor.
*   Mon Jul 09 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.14.54-1
-   Update to version 4.14.54
*   Thu Feb 22 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.14.8-1
-   First build based on linux.spec and config. No AWS-specific patches yet.
