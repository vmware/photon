%global security_hardening none

%ifarch x86_64
%define arch x86_64
%define archdir x86
%endif

Summary:        Kernel
Name:           linux-aws
Version:        4.19.307
Release:        2%{?kat_build:.kat}%{?dist}
License:        GPLv2
URL:            http://www.kernel.org
Group:          System Environment/Kernel
Vendor:         VMware, Inc.
Distribution:   Photon

%define uname_r %{version}-%{release}-aws
%define _modulesdir /lib/modules/%{uname_r}

Source0: http://www.kernel.org/pub/linux/kernel/v4.x/linux-%{version}.tar.xz
%define sha512 linux=2be40ae405a61feb1f942e0d4c63f2ca13d4a4bbadd64afd1e0a372c5a515135a3f16ae440d77061231cc4f2d9fc9421a7249adc15c50db564796f40414e5967

%ifarch x86_64
Source1: config-aws
%endif
Source2: initramfs.trigger
# contains pre, postun, filetriggerun tasks
Source3: scriptlets.inc
Source4: check_for_config_applicability.inc

%global photon_checksum_generator_version 1.2
Source5: https://github.com/vmware/photon-checksum-generator/releases/photon-checksum-generator-%{photon_checksum_generator_version}.tar.gz
%define sha512 photon-checksum-generator=bc0e3fc039cffc7bbd019da0573a89ed4cf227fd51f85d1941de060cb2a595ea1ef45914419e3238a8ebcc23cdd83193be4f1a294806f954ef8c74cdede8886b

Source6: genhmac.inc

# common
Patch0: linux-4.14-Log-kmsg-dump-on-panic.patch
Patch1: double-tcp_mem-limits.patch
Patch3: SUNRPC-Do-not-reuse-srcport-for-TIME_WAIT-socket.patch
Patch4: SUNRPC-xs_bind-uses-ip_local_reserved_ports.patch
Patch5: vsock-transport-for-9p.patch
Patch6: 4.18-x86-vmware-STA-support.patch
Patch7: vsock-delay-detach-of-QP-with-outgoing-data.patch
Patch10: 0001-cgroup-v1-cgroup_stat-support.patch
Patch11: Performance-over-security-model.patch
#HyperV patches
Patch13: 0004-vmbus-Don-t-spam-the-logs-with-unknown-GUIDs.patch

# Expose Photon kernel macros to identify kernel flavor and version
Patch14: 0001-kbuild-simplify-access-to-the-kernel-s-version.patch
Patch15: 0002-kbuild-Fix-linux-version.h-for-empty-SUBLEVEL-or-PAT.patch
Patch16: 0003-kbuild-replace-if-A-A-B-with-or-A-B.patch
Patch17: 0004-kbuild-Makefile-Introduce-macros-to-distinguish-Phot.patch
Patch18: 0005-linux-aws-Makefile-Add-kernel-flavor-info-to-the-gen.patch

Patch26: 4.18-add-sysctl-to-disallow-unprivileged-CLONE_NEWUSER-by-default.patch
# Fix CVE-2017-1000252
Patch28: kvm-dont-accept-wrong-gsi-values.patch
# Out-of-tree patches from AppArmor:
Patch29: 4.17-0001-apparmor-patch-to-provide-compatibility-with-v2.x-ne.patch
Patch30: 4.17-0002-apparmor-af_unix-mediation.patch
Patch31: 4.17-0003-apparmor-fix-use-after-free-in-sk_peer_label.patch
# RDRAND-based RNG driver to enhance the kernel's entropy pool:
Patch32: 4.18-0001-hwrng-rdrand-Add-RNG-driver-based-on-x86-rdrand-inst.patch
# Fix for CVE-2019-12456
Patch33: 0001-scsi-mpt3sas_ctl-fix-double-fetch-bug-in-_ctl_ioctl_.patch
# Fix for CVE-2019-12379
Patch34: 0001-consolemap-Fix-a-memory-leaking-bug-in-drivers-tty-v.patch
# Fix for CVE-2019-12380
Patch35: 0001-efi-x86-Add-missing-error-handling-to-old_memmap-1-1.patch
# Fix for CVE-2019-12381
Patch36: 0001-ip_sockglue-Fix-missing-check-bug-in-ip_ra_control.patch
# Fix for CVE-2019-12378
Patch38: 0001-ipv6_sockglue-Fix-a-missing-check-bug-in-ip6_ra_cont.patch
# Fix for CVE-2019-12455
Patch39: 0001-clk-sunxi-fix-a-missing-check-bug-in-sunxi_divs_clk_.patch
#Fix for CVE-2019-20908
Patch40: efi-Restrict-efivar_ssdt_load-when-the-kernel-is-locked-down.patch
#Fix for CVE-2019-19338
Patch41: 0001-KVM-vmx-implement-MSR_IA32_TSX_CTRL-disable-RTM-func.patch
Patch42: 0001-KVM-vmx-use-MSR_IA32_TSX_CTRL-to-hard-disable-TSX-on.patch
#Fix for CVE-2024-0565
Patch44: 0001-smb-client-fix-OOB-in-receive_encrypted_standard.patch

# Fix for CVE-2020-16119
Patch55: 0001-dccp-ccid-move-timers-to-struct-dccp_sock.patch
Patch56: 0002-Revert-dccp-don-t-free-ccid2_hc_tx_sock-struct-in-dc.patch
#Fix for CVE-2020-16120
Patch57: 0001-ovl-pass-correct-flags-for-opening-real-directory.patch
Patch58: 0002-ovl-switch-to-mounter-creds-in-readdir.patch
Patch59: 0003-ovl-verify-permissions-in-ovl_path_open.patch
Patch60: 0004-ovl-call-secutiry-hook-in-ovl_real_ioctl.patch
Patch61: 0005-ovl-check-permission-to-open-real-file.patch

# Fix for CVE-2019-19770
Patch62: 0001-block-revert-back-to-synchronous-request_queue-remov.patch
Patch63: 0002-block-create-the-request_queue-debugfs_dir-on-regist.patch

#Fix for CVE-2020-36385
Patch64: 0001-RDMA-cma-Add-missing-locking-to-rdma_accept.patch
Patch65: 0001-RDMA-ucma-Rework-ucma_migrate_id-to-avoid-races-with.patch

#Fix for CVE-2022-1055
Patch66: 0001-net-sched-fix-use-after-free-in-tc_new_tfilter.patch

# Fix for CVE-2022-39189
Patch69: 0001-KVM-x86-do-not-report-a-vCPU-as-preempted-outside-in.patch

# Fix for CVE-2022-36123
Patch70: 0001-x86-xen-Use-clear_bss-for-Xen-PV-guests.patch

# Fix for CVE-2021-4037
Patch72: 0001-xfs-ensure-that-the-inode-uid-gid-match-values-match.patch
Patch73: 0002-xfs-remove-the-icdinode-di_uid-di_gid-members.patch
Patch74: 0003-xfs-fix-up-non-directory-creation-in-SGID-directorie.patch

# Fix for CVE-2022-3524 and CVE-2022-3567
Patch76: 0001-ipv6-annotate-some-data-races-around-sk-sk_prot.patch
Patch80: 0005-ipv6-Fix-data-races-around-sk-sk_prot.patch
Patch81: 0006-tcp-Fix-data-races-around-icsk-icsk_af_ops.patch

# CVE-2022-43945
Patch82: 0001-NFSD-Cap-rsize_bop-result-based-on-send-buffer-size.patch
Patch83: 0002-NFSD-Protect-against-send-buffer-overflow-in-NFSv3-R.patch
Patch84: 0003-NFSD-Protect-against-send-buffer-overflow-in-NFSv2-R.patch
Patch85: 0004-NFSD-Protect-against-send-buffer-overflow-in-NFSv3-R.patch

# Upgrade vmxnet3 driver to version 4
Patch86: 0000-vmxnet3-turn-off-lro-when-rxcsum-is-disabled.patch
Patch87: 0001-vmxnet3-prepare-for-version-4-changes.patch
Patch88: 0002-vmxnet3-add-support-to-get-set-rx-flow-hash.patch
Patch89: 0003-vmxnet3-add-geneve-and-vxlan-tunnel-offload-support.patch
Patch90: 0004-vmxnet3-update-to-version-4.patch
Patch91: 0005-vmxnet3-use-correct-hdr-reference-when-packet-is-enc.patch
Patch92: 0006-vmxnet3-allow-rx-flow-hash-ops-only-when-rss-is-enab.patch
Patch93: 0007-vmxnet3-use-correct-tcp-hdr-length-when-packet-is-en.patch
Patch94: 0008-vmxnet3-fix-cksum-offload-issues-for-non-udp-tunnels.patch

Patch95: 0009-vmxnet3-Remove-buf_info-from-device-accessible-struc.patch

# SEV, TDX
Patch96: 0001-x86-boot-Avoid-VE-during-boot-for-TDX-platforms.patch

# Patch to add drbg_pr_ctr_aes256 test vectors to testmgr
Patch97: 0001-Add-drbg_pr_ctr_aes256-test-vectors-and-test-to-test.patch
# Patch to call drbg and dh crypto tests from tcrypt
Patch98: 0001-tcrypt-disable-tests-that-are-not-enabled-in-photon.patch
# Disable tcrypt from tcrypt
Patch99: 0001-linux-aws-tcrypt-Remove-tests-for-deflate.patch

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
Patch150: 0056-Amazon-ENA-driver-Update-to-version-1.6.0.patch

# Disable md5 algorithm for sctp if fips is enabled.
Patch151: 0001-disable-md5-algorithm-for-sctp-if-fips-is-enabled.patch

# Update vmxnet3 driver to version 6
Patch161: 0001-vmxnet3-fix-cksum-offload-issues-for-tunnels-with-no.patch
Patch162: 0002-vmxnet3-prepare-for-version-6-changes.patch
Patch163: 0003-vmxnet3-add-support-for-32-Tx-Rx-queues.patch
Patch164: 0004-vmxnet3-add-support-for-ESP-IPv6-RSS.patch
Patch165: 0005-vmxnet3-set-correct-hash-type-based-on-rss-informati.patch
Patch166: 0006-vmxnet3-increase-maximum-configurable-mtu-to-9190.patch
Patch167: 0007-vmxnet3-update-to-version-6.patch
Patch168: 0008-vmxnet3-fix-minimum-vectors-alloc-issue.patch
Patch169: 0009-vmxnet3-remove-power-of-2-limitation-on-the-queues.patch

# Update vmxnet3 driver to version 7
Patch170: 0001-vmxnet3-prepare-for-version-7-changes.patch
Patch171: 0002-vmxnet3-add-support-for-capability-registers.patch
Patch172: 0003-vmxnet3-add-support-for-large-passthrough-BAR-regist.patch
Patch173: 0004-vmxnet3-add-support-for-out-of-order-rx-completion.patch
Patch174: 0005-vmxnet3-add-command-to-set-ring-buffer-sizes.patch
Patch175: 0006-vmxnet3-limit-number-of-TXDs-used-for-TSO-packet.patch
Patch176: 0007-vmxnet3-use-ext1-field-to-indicate-encapsulated-pack.patch
Patch177: 0008-vmxnet3-update-to-version-7.patch
Patch178: 0009-vmxnet3-disable-overlay-offloads-if-UPT-device-does-.patch
Patch179: 0001-vmxnet3-do-not-reschedule-napi-for-rx-processing.patch
Patch180: 0001-vmxnet3-correctly-report-encapsulated-LRO-packet.patch
Patch181: 0002-vmxnet3-use-correct-intrConf-reference-when-using-ex.patch
Patch182: 0001-vmxnet3-correctly-report-csum_level-for-encapsulated.patch
Patch183: 0001-vmxnet3-move-rss-code-block-under-eop-descriptor.patch
Patch184: 0001-vmxnet3-use-gro-callback-when-UPT-is-enabled.patch

# Patch to fix Panic due to nested priority inheritance in sched_deadline
Patch191: 0001-sched-deadline-Fix-BUG_ON-condition-for-deboosted-ta.patch

# Patch to distribute the tasks within affined cpus
Patch192: 0001-sched-core-Distribute-tasks-within-affinity-masks.patch

# Allow cpuidle subsystem to use acpi_idle driver when only one C-state is available
Patch193: 0001-ACPI-processor-idle-Allow-probing-on-platforms-with-.patch

#Fix for CVE-2022-0480
Patch301: 0001-memcg-enable-accounting-for-file-lock-caches.patch

#Fix for CVE-2022-3061
Patch302: 0001-video-fbdev-i740fb-Error-out-if-pixclock-equals-zero.patch

#Fix for CVE-2022-3303
Patch303: 0001-ALSA-pcm-oss-Fix-race-at-SNDCTL_DSP_SYNC.patch

# CVE-2022-1789
Patch304: 0001-KVM-x86-mmu-fix-NULL-pointer-dereference-on-guest-IN.patch

# Fix for CVE-2021-4204
Patch305: 0002-bpf-Disallow-unprivileged-bpf-by-default.patch

# Fix for CVE-2023-28466
Patch306: 0001-net-prevent-race-condition-in-do_tls_getsockopt_tx.patch

# CVE-2023-1611
Patch307: 0001-btrfs-fix-race-between-quota-disable-and-quota-assig.patch

#Fix for CVE-2023-1076
Patch308: 0001-net-add-sock_init_data_uid.patch
Patch309: 0001-tap-tap_open-correctly-initialize-socket-uid.patch
Patch310: 0001-tun-tun_chr_open-correctly-initialize-socket-uid.patch

#Fix for CVE-2021-3759
Patch312: 0001-memcg-enable-accounting-of-ipc-resources.patch

#Fix for CVE-2023-2124
Patch313: 0001-xfs-verify-buffer-contents-when-we-skip-log-replay.patch

#Fix for CVE-2023-39197
Patch314: 0001-netfilter-conntrack-dccp-copy-entire-header-to-stack.patch

#Fix CVE-2023-51779
Patch316: 0001-Bluetooth-af_bluetooth-Fix-Use-After-Free-in-bt_sock.patch

# Fix CVE-2024-23307
Patch317: 0001-md-raid5-fix-atomicity-violation-in-raid5_cache_coun.patch

# Fix CVE-2024-22099
Patch318: 0001-Bluetooth-rfcomm-Fix-null-ptr-deref-in-rfcomm_check_.patch

# Usermode helper fixes
Patch400: 0001-umh-Add-command-line-to-user-mode-helpers.patch
Patch401: 0002-umh-add-exit-routine-for-UMH-process.patch

# BPFilter fixes
Patch405: 0001-net-bpfilter-use-cleanup-callback-to-release-umh_inf.patch
Patch406: 0002-net-bpfilter-restart-bpfilter_umh-when-error-occurre.patch
Patch407: 0003-net-bpfilter-disallow-to-remove-bpfilter-module-whil.patch
Patch408: 0004-net-bpfilter-dont-use-module_init-in-non-modular-cod.patch
Patch409: 0005-net-bpfilter-fallback-to-netfilter-if-failed-to-load.patch

%if 0%{?kat_build}
Patch1000: fips-kat-tests.patch
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
BuildRequires:  audit-devel
BuildRequires:  bison
BuildRequires:  gettext

Requires:       filesystem
Requires:       kmod
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
Requires:       python3
Requires:       gawk
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
Summary:    HMAC SHA256/HMAC SHA512 generator
Group:      System Environment/Kernel
Requires:   %{name} = %{version}-%{release}
# kernel is needed during postun else hmacgen might get
# removed after kernel which will break keeping modules of
# running kernel till next boot feature
Requires(postun): %{name} = %{version}-%{release}
Enhances:   %{name}

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
%setup -q -T -D -b5 -n linux-%{version}

%autopatch -p1 -m0 -M160

# Update vmxnet3 driver to version 6
%autopatch -p1 -m161 -M169

# Update vmxnet3 driver to version 7
%autopatch -p1 -m170 -M184

%autopatch -p1 -m191 -M194

# CVE fixes
%autopatch -p1 -m300 -M318

# Usermode helper patches
%autopatch -p1 -m400 -M401

# bpfilter patches
%autopatch -p1 -m405 -M409

%if 0%{?kat_build}
%patch1000 -p1
%endif

make %{?_smp_mflags} mrproper

%ifarch x86_64
cp %{SOURCE1} .config
%endif

sed -i 's/CONFIG_LOCALVERSION="-aws"/CONFIG_LOCALVERSION="-%{release}-aws"/' .config

%include %{SOURCE4}

%build
make VERBOSE=1 KBUILD_BUILD_VERSION="1-photon" \
        KBUILD_BUILD_HOST="photon" ARCH=%{?arch} %{?_smp_mflags}

bldroot="${PWD}"

#build photon-checksum-generator module
pushd ../photon-checksum-generator-%{photon_checksum_generator_version}/kernel
make -C ${bldroot} M="${PWD}" modules %{?_smp_mflags}
popd

%define __modules_install_post \
for MODULE in $(find %{buildroot}%{_modulesdir} -name *.ko); do \
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
install -vdm 755 %{buildroot}%{_sysconfdir}
install -vdm 755 %{buildroot}/boot
install -vdm 755 %{buildroot}%{_defaultdocdir}/linux-%{uname_r}
install -vdm 755 %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}
install -vdm 755 %{buildroot}%{_libdir}/debug/%{_modulesdir}
make INSTALL_MOD_PATH=%{buildroot} modules_install %{?_smp_mflags}

bldroot="${PWD}"

#install photon-checksum-generator module
pushd ../photon-checksum-generator-%{photon_checksum_generator_version}/kernel
make -C ${bldroot} M="${PWD}" INSTALL_MOD_PATH=%{buildroot} modules_install %{?_smp_mflags}
popd

%ifarch x86_64

# Verify for build-id match
# We observe different IDs sometimes
# TODO: debug it
ID1=$(readelf -n vmlinux | grep "Build ID")
./scripts/extract-vmlinux arch/x86/boot/bzImage > extracted-vmlinux
ID2=$(readelf -n extracted-vmlinux | grep "Build ID")
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
cp -r Documentation/* %{buildroot}%{_defaultdocdir}/linux-%{uname_r}

%if 0%{?__debug_package}
install -vm 644 vmlinux %{buildroot}%{_libdir}/debug/%{_modulesdir}/vmlinux-%{uname_r}
# `perf test vmlinux` needs it
ln -s vmlinux-%{uname_r} %{buildroot}%{_libdir}/debug/%{_modulesdir}/vmlinux
%endif

cat > %{buildroot}/boot/linux-%{uname_r}.cfg << "EOF"
# GRUB Environment Block
photon_cmdline=init=/lib/systemd/systemd ro loglevel=3 quiet no-vmw-sta nvme_core.io_timeout=4294967295 cgroup.memory=nokmem
photon_linux=vmlinuz-%{uname_r}
photon_initrd=initrd.img-%{uname_r}
EOF

# Register myself to initramfs
mkdir -p %{buildroot}%{_sharedstatedir}/initramfs/kernel
cat > %{buildroot}%{_sharedstatedir}/initramfs/kernel/%{uname_r} << "EOF"
--add-drivers "tmem xen-scsifront xen-blkfront xen-evtchn xen-gntalloc xen-gntdev xen-privcmd xen-pciback xenfs hv_utils hv_vmbus hv_storvsc hv_netvsc hv_sock hv_balloon dm-mod nvme nvme-core"
EOF

# Cleanup dangling symlinks
rm -rf %{buildroot}%{_modulesdir}/source \
       %{buildroot}%{_modulesdir}/build

find . -name Makefile* -o -name Kconfig* -o -name *.pl | xargs sh -c 'cp --parents "$@" %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}' copy

find arch/%{?archdir}/include include scripts -type f | xargs sh -c 'cp --parents "$@" %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}' copy

find $(find arch/%{?archdir} -name include -o -name scripts -type d) -type f | xargs sh -c 'cp --parents "$@" %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}' copy

find arch/%{?archdir}/include Module.symvers include scripts -type f | xargs sh -c 'cp --parents "$@" %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}' copy

%ifarch x86_64
# CONFIG_STACK_VALIDATION=y requires objtool to build external modules
install -vsm 755 tools/objtool/objtool %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}/tools/objtool/
install -vsm 755 tools/objtool/fixdep %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}/tools/objtool/
%endif

cp .config %{buildroot}%{_usrsrc}/linux-headers-%{uname_r} # copy .config manually to be where it's expected to be
ln -sf "%{_usrsrc}/linux-headers-%{uname_r}" "%{buildroot}%{_modulesdir}/build"
find %{buildroot}/lib/modules -name '*.ko' -print0 | xargs -0 chmod u+x

# disable (JOBS=1) parallel build to fix this issue:
# fixdep: error opening depfile: ./.plugin_cfg80211.o.d: No such file or directory
# Linux version that was affected is 4.4.26

%include %{SOURCE2}
%include %{SOURCE3}

%post
/sbin/depmod -a %{uname_r}
ln -sf linux-%{uname_r}.cfg /boot/photon.cfg

%post hmacgen
/sbin/depmod -a %{uname_r}

%post drivers-gpu
/sbin/depmod -a %{uname_r}

%post sound
/sbin/depmod -a %{uname_r}

%ifarch x86_64
%post oprofile
/sbin/depmod -a %{uname_r}
%endif

%files
%defattr(-,root,root)
/boot/System.map-%{uname_r}
/boot/config-%{uname_r}
/boot/vmlinuz-%{uname_r}
/boot/.vmlinuz-%{uname_r}.hmac
%config(noreplace) /boot/linux-%{uname_r}.cfg
%config %{_sharedstatedir}/initramfs/kernel/%{uname_r}
%defattr(0644,root,root)
%{_modulesdir}/*
%exclude %{_modulesdir}/build
%exclude %{_modulesdir}/kernel/drivers/gpu
%exclude %{_modulesdir}/kernel/sound
%exclude %{_modulesdir}/extra/hmac_generator.ko.xz
%exclude %{_modulesdir}/extra/.hmac_generator.ko.xz.hmac
%ifarch x86_64
%exclude %{_modulesdir}/kernel/arch/x86/oprofile/
%endif

%files docs
%defattr(-,root,root)
%{_defaultdocdir}/linux-%{uname_r}/*

%files devel
%defattr(-,root,root)
%{_modulesdir}/build
%{_usrsrc}/linux-headers-%{uname_r}

%files drivers-gpu
%defattr(-,root,root)
%exclude %{_modulesdir}/kernel/drivers/gpu/drm/cirrus/
%{_modulesdir}/kernel/drivers/gpu

%files hmacgen
%defattr(-,root,root)
%{_modulesdir}/extra/hmac_generator.ko.xz
%{_modulesdir}/extra/.hmac_generator.ko.xz.hmac

%files sound
%defattr(-,root,root)
%{_modulesdir}/kernel/sound

%ifarch x86_64
%files oprofile
%defattr(-,root,root)
%{_modulesdir}/kernel/arch/x86/oprofile/
%endif

%changelog
* Mon Mar 11 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com>  4.19.307-2
- Fixes CVE-2024-23307 and CVE-2024-22099
* Wed Mar 06 2024 Srish Srinivasan <srish.srinivasan@broadcom.com> 4.19.307-1
- Update to version 4.19.307
* Fri Feb 23 2024 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 4.19.306-2
- Fix CVE-2023-51779
* Tue Feb 06 2024 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 4.19.306-1
- Update to version 4.19.306
* Mon Feb 05 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 4.19.305-5
- Fix CVE-2024-1086
* Mon Feb 05 2024 Ajay Kaher <ajay.kaher@broadcom.com> 4.19.305-4
- Fix CVE-2024-0607
* Mon Feb 05 2024 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 4.19.305-3
- Fix for CVE-2023-39197
* Tue Jan 30 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 4.19.305-2
- Fix CVE-2024-0565
* Mon Jan 29 2024 Ajay Kaher <ajay.kaher@broadcom.com> 4.19.305-1
- Update to version 4.19.305
* Tue Jan 16 2024 Ajay Kaher <ajay.kaher@broadcom.com> 4.19.303-2
- Fix CVE-2024-0340
* Mon Jan 01 2024 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 4.19.303-1
- Update to version 4.19.303
* Fri Nov 03 2023 Ankit Jain <ankitja@vmware.com> 4.19.297-1
- Update to version 4.19.297
* Sun Oct 01 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 4.19.295-3
- Fix for CVE-2023-42754
* Tue Sep 26 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 4.19.295-2
- Move kernel prep to %prep
* Mon Sep 25 2023 Keerthana K <keerthanak@vmware.com> 4.19.295-1
- Update to version 4.19.295
* Wed Sep 20 2023 Roye Eshed <eshedr@vmware.com> 4.19.292-2
- Fix for CVE-2023-42753
* Wed Aug 30 2023 Srish Srinivasan <ssrish@vmware.com> 4.19.292-1
- Update to version 4.19.292
- Patched CVE-2023-4128
* Tue Aug 29 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 4.19.290-2
- Fix TCP slab memory leak
* Thu Aug 10 2023 Ajay Kaher <akaher@vmware.com> 4.19.290-1
- Update to version 4.19.290
* Mon Jul 31 2023 Ajay Kaher <akaher@vmware.com> 4.19.288-4
- Fix: SEV: Guest should not disabled CR4.MCE
* Mon Jul 31 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 4.19.288-3
- Fix for CVE-2023-2124
* Mon Jul 24 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 4.19.288-2
- Fix for CVE-2021-3759
* Fri Jul 21 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 4.19.288-1
- Update to version 4.19.288
* Tue Jul 18 2023 Naadir Jeewa <jeewan@vmware.com> 4.19.285-2
- Fixes for bpfilter and usermode helpers
- Add additional build dependencies for container builds
* Wed Jun 14 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 4.19.285-1
- Update to version 4.19.285
* Wed Jun 14 2023 Srish Srinivasan <ssrish@vmware.com> 4.19.283-5
- Fix for CVE-2023-1076 and CVE-2023-1077
* Fri Jun 02 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 4.19.283-4
- Fix for CVE-2023-1611
* Fri Jun 02 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 4.19.283-3
- Add patch to address CVE-2023-28466
* Wed May 31 2023 Ankit Jain <ankitja@vmware.com> 4.19.283-2
- Allow cpuidle subsystem to use acpi_idle driver
- when only one C-state is available
* Wed May 17 2023 Ankit Jain <ankitja@vmware.com> 4.19.283-1
- Update to version 4.19.283
* Tue Apr 18 2023 Keerthana K <keerthanak@vmware.com> 4.19.280-1
- Update to version 4.19.280
* Mon Apr 17 2023 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.277-3
- Cleanup commented patch files
* Wed Mar 29 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 4.19.277-2
- update to latest ToT vmxnet3 driver pathes
* Tue Mar 14 2023 Roye Eshed <eshedr@vmware.com> 4.19.277-1
- Update to version 4.19.277
* Tue Feb 28 2023 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.272-2
- Expose Photon kernel macros to simplify building out-of-tree drivers.
* Thu Feb 16 2023 Srish Srinivasan <ssrish@vmware.com> 4.19.272-1
- Update to version 4.19.272
* Tue Feb 07 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 4.19.271-3
- Fix for CVE-2021-44879/2022-0480/CVE-2022-3061/CVE-2022-3303/CVE-2023-23454
* Mon Feb 06 2023 Alexey Makhalov <amakhalov@vmware.com> 4.19.271-2
- Implement performance over security option for RETBleed (pos=1)
* Wed Feb 01 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 4.19.271-1
- Update to version 4.19.271
* Thu Jan 05 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 4.19.269-2
- update to latest ToT vmxnet3 driver
- Include patch "vmxnet3: correctly report csum_level for encapsulated packet"
* Mon Dec 19 2022 srinidhira0 <srinidhir@vmware.com> 4.19.269-1
- Update to version 4.19.269
* Thu Dec 15 2022 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 4.19.268-2
- update to latest ToT vmxnet3 driver
* Fri Dec 09 2022 Ankit Jain <ankitja@vmware.com> 4.19.268-1
- Update to version 4.19.268
* Fri Dec 09 2022 Ankit Jain <ankitja@vmware.com> 4.19.264-4
- Distribute the tasks across affined cpus
* Tue Dec 06 2022 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 4.19.264-3
- Fix for CVE-2022-43945
* Mon Nov 07 2022 Ajay Kaher <akaher@vmware.com> 4.19.264-2
- Fix CVE-2022-3524 and CVE-2022-3567
* Thu Nov 03 2022 Ajay Kaher <akaher@vmware.com> 4.19.264-1
- Update to version 4.19.264
* Wed Oct 19 2022 Sharan Turlapati <sturlapati@vmware.com> 4.19.261-1
- Update to version 4.19.261
* Tue Sep 27 2022 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.256-4
- Fix for CVE-2022-34918
* Mon Sep 19 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 4.19.256-3
- Fix for CVE-2022-3028/2021-4037
* Tue Sep 13 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 4.19.256-2
- Fix for CVE-2022-36123/2022-39189
* Tue Aug 30 2022 Brennan Lamoreaux <blamoreaux@vmware.com> 4.19.256-1
- Update to version 4.19.256
* Fri Aug 05 2022 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.247-13
- Fix for CVE-2022-2586 and CVE-2022-2588
* Wed Aug 03 2022 Shreenidhi Shedi <sshedi@vmware.com> 4.19.247-12
- Scriptlets fixes and improvements
* Wed Aug 03 2022 Keerthana K <keerthanak@vmware.com> 4.19.247-11
- Fix linux headers, doc folder and linux-<uname -r>.cfg names
* Tue Aug 02 2022 Sharan Turlapati <sturlapati@vmware.com> 4.19.247-10
- Revert napi reschedule on rx in vmxnet3 driver
* Tue Aug 02 2022 Ankit Jain <ankitja@vmware.com> 4.19.247-9
- Fix BUG_ON for deboosted tasks
* Tue Jul 12 2022 Ankit Jain <ankitja@vmware.com> 4.19.247-8
- Backported the fix for CVE-2022-1789
* Thu Jul 07 2022 Shreenidhi Shedi <sshedi@vmware.com> 4.19.247-7
- Spec improvements
* Wed Jul 06 2022 Shreenidhi Shedi <sshedi@vmware.com> 4.19.247-6
- Add kernel as requires to hmacgen postun
* Thu Jun 30 2022 Ankit Jain <ankitja@vmware.com> 4.19.247-5
- Fixes panic due to nested priority inheritance
* Thu Jun 23 2022 Sharan Turlapati <sturlapati@vmware.com> 4.19.247-4
- Update vmxnet3 driver to version 7
* Wed Jun 22 2022 Sharan Turlapati <sturlapati@vmware.com> 4.19.247-3
- Update vmxnet3 driver to version 6
* Wed Jun 15 2022 Brennan Lamoreaux <blamoreaux@vmware.com> 4.19.247-2
- Enable config_livepatch and function tracer, which is needed for livepatch.
* Tue Jun 14 2022 Ajay Kaher <akaher@vmware.com> 4.19.247-1
- Update to version 4.19.247
* Thu May 26 2022 Sharan Turlapati <sturlapati@vmware.com> 4.19.245-1
- Update to version 4.19.245
* Mon May 16 2022 Brennan Lamoreaux <blamoreaux@vmware.com> 4.19.241-2
- Fix for CVE-2022-1048
* Wed May 11 2022 Brennan Lamoreaux <blamoreaux@vmware.com> 4.19.241-1
- Update to version 4.19.241
* Fri Apr 29 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 4.19.240-1
- Update to version 4.19.240
- Fix CVE-2022-1055
* Mon Mar 21 2022 Ajay Kaher <akaher@vmware.com> 4.19.232-2
- Fix for CVE-2022-1016
* Mon Mar 07 2022 srinidhira0 <srinidhir@vmware.com> 4.19.232-1
- Update to version 4.19.232
* Fri Feb 11 2022 Sharan Turlapati <sturlapati@vmware.com> 4.19.229-1
- Update to version 4.19.229
* Wed Feb 09 2022 Sharan Turlapati <sturlapati@vmware.com> 4.19.225-5
- Fix for CVE-2022-0435
* Mon Feb 07 2022 Sharan Turlapati <sturlapati@vmware.com> 4.19.225-4
- Fix for CVE-2022-0492
* Tue Jan 25 2022 Sharan Turlapati <sturlapati@vmware.com> 4.19.225-3
- Fix for CVE-2022-22942
* Tue Jan 25 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.225-2
- Fix CVE-2022-0330
* Fri Jan 21 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.225-1
- Update to version 4.19.225
* Sat Jan 08 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.224-2
- Fix CVE-2021-4155 and CVE-2021-4204
* Wed Jan 05 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.224-1
- Update to version 4.19.224
* Fri Dec 17 2021 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 4.19.219-3
- Disable md5 algorithm for sctp if fips is enabled.
* Tue Dec 14 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.219-2
- Fix for CVE-2020-36385
* Wed Dec 08 2021 srinidhira0 <srinidhir@vmware.com> 4.19.219-1
- Update to version 4.19.219
* Wed Nov 24 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.217-1
- Update to version 4.19.217
* Fri Oct 29 2021 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 4.19.214-2
- Fix for CVE-2020-36322/CVE-2021-28950
* Thu Oct 28 2021 Sharan Turlapati <sturlapati@vmware.com> 4.19.214-1
- Update to version 4.19.214
* Wed Sep 29 2021 Keerthana K <keerthanak@vmware.com> 4.19.208-1
- Update to version 4.19.208
* Fri Aug 27 2021 srinidhira0 <srinidhir@vmware.com> 4.19.205-1
- Update to version 4.19.205
* Wed Aug 11 2021 Vikash Bansal <bvikas@vmware.com> 4.19.198-2
- Remove deflate tests from tcrypt
* Tue Jul 27 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.198-1
- Update to version 4.19.198
* Thu Jul 15 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.191-3
- Fix for CVE-2021-33909
* Tue Jun 22 2021 Sharan Turlapati <sturlapati@vmware.com> 4.19.191-2
- Fix for CVE-2021-3609
* Tue Jun 01 2021 Keerthana K <keerthanak@vmware.com> 4.19.191-1
- Update to version 4.19.191
* Mon May 17 2021 Ajay Kaher <akaher@vmware.com> 4.19.190-1
- Update to version 4.19.190
* Wed May 12 2021 Sharan Turlapati <sturlapati@vmware.com> 4.19.189-3
- Fix for CVE-2021-23133
* Tue May 04 2021 Sharan Turlapati <sturlapati@vmware.com> 4.19.189-2
- Remove buf_info from device accessible structures in vmxnet3
* Thu Apr 29 2021 Ankit Jain <ankitja@vmware.com> 4.19.189-1
- Update to version 4.19.189
* Tue Apr 20 2021 Ankit Jain <ankitja@vmware.com> 4.19.186-3
- Fix for CVE-2021-3444
* Mon Apr 19 2021 Sharan Turlapati <sturlapati@vmware.com> 4.19.186-2
- Fix for CVE-2021-23133
* Mon Apr 19 2021 srinidhira0 <srinidhir@vmware.com> 4.19.186-1
- Update to version 4.19.186
* Thu Apr 15 2021 Keerthana K <keerthanak@vmware.com> 4.19.182-3
- photon-checksum-generator update to v1.2
* Tue Apr 06 2021 Alexey Makhalov <amakhalov@vmware.com> 4.19.182-2
- Disable kernel accounting for memory cgroups
- Enable cgroup v1 stats
- .config: enable PERCPU_STATS
* Mon Mar 22 2021 srinidhira0 <srinidhir@vmware.com> 4.19.182-1
- Update to version 4.19.182
* Fri Feb 26 2021 Sharan Turlapati <sturlapati@vmware.com> 4.19.177-1
- Update to version 4.19.177
* Fri Feb 19 2021 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.174-2
- Fix /boot/photon.cfg symlink when /boot is a separate partition.
* Tue Feb 09 2021 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.174-1
- Update to version 4.19.174
* Tue Jan 12 2021 Ankit Jain <ankitja@vmware.com> 4.19.164-2
- Disabled CONFIG_TARGET_CORE to fix CVE-2020-28374
* Mon Jan 04 2021 Ankit Jain <ankitja@vmware.com> 4.19.164-1
- Update to version 4.19.164
* Mon Dec 21 2020 Ajay Kaher <akaher@vmware.com> 4.19.163-2
- Fix for CVE-2020-29569
* Tue Dec 15 2020 Vikash Bansal <bvikas@vmware.com> 4.19.163-1
- Update to version 4.19.163
* Wed Dec 09 2020 Srinidhi Rao <srinidhir@vmware.com> 4.19.160-2
- Fix for CVE-2019-19770
* Tue Nov 24 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.160-1
- Update to version 4.19.160
- Fix CVE-2019-19338 and CVE-2019-20908
* Mon Nov 16 2020 Vikash Bansal <bvikas@vmware.com> 4.19.154-6
- hmacgen: Add path_put to hmac_gen_hash
* Fri Nov 13 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.154-5
- Fix CVE-2020-25668
* Tue Nov 10 2020 Keerthana K <keerthanak@vmware.com> 4.19.154-4
- Fix slab-out-of-bounds read in fbcon
* Tue Nov 10 2020 Keerthana K <keerthanak@vmware.com> 4.19.154-3
- Fix CVE-2020-8694
* Fri Nov 06 2020 Keerthana K <keerthanak@vmware.com> 4.19.154-2
- Fix CVE-2020-25704
* Mon Nov 02 2020 Keerthana K <keerthanak@vmware.com> 4.19.154-1
- Update to version 4.19.154
* Wed Oct 14 2020 Ajay Kaher <akaher@vmware.com> 4.19.150-1
- Update to version 4.19.150
* Wed Oct 14 2020 Ajay Kaher <akaher@vmware.com> 4.19.148-5
- Fix for CVE-2020-16120
* Mon Oct 12 2020 Ankit Jain <ankitja@vmware.com> 4.19.148-4
- Fix for CVE-2020-16119
* Wed Oct 07 2020 Ajay Kaher <akaher@vmware.com> 4.19.148-3
- Fix mp_irqdomain_activate crash
* Tue Oct 06 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.148-2
- Fix IPIP encapsulation issue in vmxnet3 driver.
* Mon Sep 28 2020 Ajay Kaher <akaher@vmware.com> 4.19.148-1
- Update to version 4.19.148
* Wed Sep 23 2020 Ajay Kaher <akaher@vmware.com> 4.19.145-4
- Fix for CVE-2020-14390
* Wed Sep 23 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.145-3
- Fix for CVE-2019-19813 and CVE-2019-19816
* Tue Sep 22 2020 Ajay Kaher <akaher@vmware.com> 4.19.145-2
- Fix for CVE-2020-25211
* Tue Sep 15 2020 Vikash Bansal <bvikas@vmware.com> 4.19.145-1
- Update to version 4.19.145
* Mon Sep 07 2020 Vikash Bansal <bvikas@vmware.com> 4.19.138-2
- Fix for CVE-2020-14386
* Sat Aug 08 2020 ashwin-h <ashwinh@vmware.com> 4.19.138-1
- Update to version 4.19.138
* Tue Aug 04 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.132-3
- Upgrade vmxnet3 driver to version 4
* Sun Jul 26 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.132-2
- Fix CVE-2020-14331
* Thu Jul 16 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.132-1
- Update to version 4.19.132
* Sat Jun 27 2020 Keerthana K <keerthanak@vmware.com> 4.19.129-1
- Update to version 4.19.129
* Tue Jun 23 2020 Ajay Kaher <akaher@vmware.com> 4.19.126-2
- Fix for CVE-2020-12888
* Fri Jun 05 2020 Vikash Bansal <bvikas@vmware.com> 4.19.126-1
- Update to version 4.19.126
* Thu Jun 04 2020 Ajay Kaher <akaher@vmware.com> 4.19.124-2
- Fix for CVE-2020-10757
* Thu May 28 2020 Ajay Kaher <akaher@vmware.com> 4.19.124-1
- Update to version 4.19.124
* Thu May 28 2020 Shreenidhi Shedi <sshedi@vmware.com> 4.19.115-6
- Keep modules of running kernel till next boot
* Fri May 22 2020 Ashwin H <ashwinh@vmware.com> 4.19.115-5
- Fix for CVE-2018-20669
* Fri May 15 2020 Vikash Bansal <bvikas@vmware.com> 4.19.115-4
- Fix for CVE-2019-18885
* Wed May 06 2020 Siddharth Chandrasekaran <csiddharth@vmware.com> 4.19.115-3
- Add patch to fix CVE-2020-10711
* Wed Apr 29 2020 Keerthana K <keerthanak@vmware.com> 4.19.115-2
- Photon-checksum-generator version update to 1.1.
* Mon Apr 13 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.115-1
- Update to version 4.19.115
* Wed Apr 08 2020 Vikash Bansal <bvikas@vmware.com> 4.19.112-2
- HMAC-SHA256 digest of hmac_generator module moved to hmacgen package
* Mon Mar 23 2020 Keerthana K <keerthanak@vmware.com> 4.19.112-1
- Update to version 4.19.112
* Tue Mar 17 2020 Vikash Bansal <bvikas@vmware.com> 4.19.104-3
- hmac generation of crypto modules and initrd generation changes if fips=1
* Mon Mar 16 2020 Keerthana K <keerthanak@vmware.com> 4.19.104-2
- Adding Enhances depedency to hmacgen.
* Mon Mar 09 2020 Siddharth Chandrasekaran <csiddharth@vmware.com> 4.19.104-1
- Update to version 4.19.104
* Wed Mar 04 2020 Vikash Bansal <bvikas@vmware.com> 4.19.97-5
- Backporting of patch continuous testing of RNG from urandom
* Tue Feb 25 2020 Ajay Kaher <akaher@vmware.com> 4.19.97-4
- Fix CVE-2019-16234
* Tue Feb 11 2020 Keerthana K <keerthanak@vmware.com> 4.19.97-3
- Add photon-checksum-generator source tarball and remove hmacgen patch.
- Exclude hmacgen.ko from base package.
* Wed Jan 29 2020 Keerthana K <keerthanak@vmware.com> 4.19.97-2
- Update tcrypt to test drbg_pr_sha256 and drbg_nopr_sha256.
- Update testmgr to add drbg_pr_ctr_aes256 test vectors.
* Fri Jan 17 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.97-1
- Update to version 4.19.97
* Thu Jan 02 2020 Keerthana K <keerthanak@vmware.com> 4.19.87-3
- Modify tcrypt to remove tests for algorithms that are not supported in photon.
- Added tests for DH, DRBG algorithms.
* Fri Dec 20 2019 Keerthana K <keerthanak@vmware.com> 4.19.87-2
- Update fips Kat tests.
* Fri Dec 06 2019 Ajay Kaher <akaher@vmware.com> 4.19.87-1
- Update to version 4.19.87
* Thu Dec 05 2019 Ajay Kaher <akaher@vmware.com> 4.19.84-4
- Adding nvme and nvme-core to initrd list
- Removing unwanted modules from initrd list
* Tue Dec 03 2019 Keerthana K <keerthanak@vmware.com> 4.19.84-3
- Adding hmac sha256/sha512 generator kernel module for fips.
* Tue Nov 26 2019 Ajay Kaher <akaher@vmware.com> 4.19.84-2
- Fix CVE-2019-19062, CVE-2019-19066, CVE-2019-19072,
- CVE-2019-19073, CVE-2019-19074, CVE-2019-19078
* Tue Nov 12 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.84-1
- Update to version 4.19.84
- Fix CVE-2019-18814
* Fri Nov 08 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.82-1
- Update to version 4.19.82
* Thu Nov 07 2019 Jorgen Hansen (VMware) <jhansen@vmware.com> 4.19.79-2
- Fix vsock QP detach with outgoing data
* Thu Oct 17 2019 Ajay Kaher <akaher@vmware.com> 4.19.79-1
- Update to version 4.19.79
- Fix CVE-2019-17133
* Thu Oct 10 2019 Harinadh D <hdommaraju@vmware.com> 4.19.76-2
- Adding lvm and dm-mod modules to support root as lvm
* Wed Oct 02 2019 Ajay Kaher <akaher@vmware.com> 4.19.76-1
- Update to version 4.19.76
* Thu Sep 19 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.72-2
- Avoid oldconfig which leads to potential build hang
* Wed Sep 11 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.72-1
- Update to version 4.19.72
* Fri Aug 30 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.69-1
- Update to version 4.19.69
* Tue Aug 06 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.65-1
- Update to version 4.19.65
- Fix CVE-2019-1125 (SWAPGS)
* Tue Jul 30 2019 Keerthana K <keerthanak@vmware.com> 4.19.52-3
- Fix Postun scriplet
* Thu Jun 27 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.52-2
- Deprecate linux-aws-tools in favor of linux-tools.
* Mon Jun 17 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.52-1
- Update to version 4.19.52
- Fix CVE-2019-12456, CVE-2019-12379, CVE-2019-12380, CVE-2019-12381,
- CVE-2019-12382, CVE-2019-12378, CVE-2019-12455
* Thu May 23 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.40-3
- Fix CVE-2019-11191 by deprecating a.out file format support.
* Tue May 14 2019 Keerthana K <keerthanak@vmware.com> 4.19.40-2
- Fix to parse through /boot folder and update symlink (/boot/photon.cfg) if
- mulitple kernels are installed and current linux kernel is removed.
* Tue May 07 2019 Ajay Kaher <akaher@vmware.com> 4.19.40-1
- Update to version 4.19.40
* Fri Mar 29 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.32-2
- Fix CVE-2019-10125
* Wed Mar 27 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.32-1
- Update to version 4.19.32
* Thu Mar 14 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.29-1
- Update to version 4.19.29
* Tue Mar 05 2019 Ajay Kaher <akaher@vmware.com> 4.19.26-1
- Update to version 4.19.26
* Thu Feb 21 2019 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.15-2
- Fix CVE-2019-8912
* Tue Jan 15 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.15-1
- Update to version 4.19.15
* Mon Jan 07 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.6-2
- Enable additional security hardening options in the config.
* Mon Dec 10 2018 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.6-1
- Update to version 4.19.6
- Enable EFI in config-aws to support kernel signing.
* Mon Dec 10 2018 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.1-3
- Set nvme io_timeout to maximum in kernel cmdline.
* Wed Nov 14 2018 Ajay Kaher <akaher@vmware.com> 4.19.1-2
- Adding BuildArch
* Tue Nov 06 2018 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.1-1
- Update to version 4.19.1
* Mon Oct 22 2018 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.18.9-1
- Update to version 4.18.9
* Mon Oct 08 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.14.67-2
- Add enhancements from Amazon.
* Wed Sep 19 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.14.67-1
- Update to version 4.14.67
* Tue Sep 18 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.14.54-4
- Add rdrand-based RNG driver to enhance kernel entropy.
* Sun Sep 02 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.14.54-3
- Add full retpoline support by building with retpoline-enabled gcc.
* Thu Aug 30 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.14.54-2
- Apply out-of-tree patches needed for AppArmor.
* Mon Jul 09 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.14.54-1
- Update to version 4.14.54
* Thu Feb 22 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.14.8-1
- First build based on linux.spec and config. No AWS-specific patches yet.
