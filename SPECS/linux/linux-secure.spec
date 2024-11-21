%global security_hardening none

Summary:        Kernel
Name:           linux-secure
Version:        4.19.324
Release:        1%{?kat_build:.kat}%{?dist}
License:        GPLv2
URL:            http://www.kernel.org
Group:          System Environment/Kernel
Vendor:         VMware, Inc.
Distribution:   Photon

%define uname_r %{version}-%{release}-secure
%define _modulesdir /lib/modules/%{uname_r}

Source0: http://www.kernel.org/pub/linux/kernel/v4.x/linux-%{version}.tar.xz
%define sha512 linux=42cf5e8f14c12077661c7426ed1637e2fc984205ea39d3e87d2d2fb85210587c87bd9b97fe4b1abc1a4fab3e2d625a0997a1cec3c33b1ca547b0e150b71f2021

Source1: config-secure
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
Patch7: 9p-trans_fd-extend-port-variable-to-u32.patch
Patch8: vsock-delay-detach-of-QP-with-outgoing-data.patch
Patch10: 0001-cgroup-v1-cgroup_stat-support.patch
Patch11: Performance-over-security-model.patch
# secure
Patch12: 0001-bpf-ext4-bonding-Fix-compilation-errors.patch
Patch13: 0001-NOWRITEEXEC-and-PAX-features-MPROTECT-EMUTRAMP.patch
Patch14: 0002-Added-PAX_RANDKSTACK.patch
Patch15: 0003-Added-rap_plugin.patch
# HyperV Patches
Patch16: 0004-vmbus-Don-t-spam-the-logs-with-unknown-GUIDs.patch

# Expose Photon kernel macros to identify kernel flavor and version
Patch17: 0001-kbuild-simplify-access-to-the-kernel-s-version.patch
Patch18: 0002-kbuild-Fix-linux-version.h-for-empty-SUBLEVEL-or-PAT.patch
Patch19: 0003-kbuild-replace-if-A-A-B-with-or-A-B.patch
Patch20: 0004-kbuild-Makefile-Introduce-macros-to-distinguish-Phot.patch
Patch21: 0005-linux-secure-Makefile-Add-kernel-flavor-info-to-the-.patch

Patch26: 4.18-add-sysctl-to-disallow-unprivileged-CLONE_NEWUSER-by-default.patch
# Fix CVE-2017-1000252
Patch31: kvm-dont-accept-wrong-gsi-values.patch
# Out-of-tree patches from AppArmor:
Patch32: 4.17-0001-apparmor-patch-to-provide-compatibility-with-v2.x-ne.patch
Patch33: 4.17-0002-apparmor-af_unix-mediation.patch
Patch34: 4.17-0003-apparmor-fix-use-after-free-in-sk_peer_label.patch
# RDRAND-based RNG driver to enhance the kernel's entropy pool:
Patch35: 4.18-0001-hwrng-rdrand-Add-RNG-driver-based-on-x86-rdrand-inst.patch
# Fix for CVE-2019-12456
Patch36: 0001-scsi-mpt3sas_ctl-fix-double-fetch-bug-in-_ctl_ioctl_.patch
# Fix for CVE-2019-12379
Patch37: 0001-consolemap-Fix-a-memory-leaking-bug-in-drivers-tty-v.patch
# Fix for CVE-2019-12380
Patch38: 0001-efi-x86-Add-missing-error-handling-to-old_memmap-1-1.patch
# Fix for CVE-2019-12381
Patch39: 0001-ip_sockglue-Fix-missing-check-bug-in-ip_ra_control.patch
# Fix for CVE-2019-12378
Patch41: 0001-ipv6_sockglue-Fix-a-missing-check-bug-in-ip6_ra_cont.patch
# Fix for CVE-2019-12455
Patch42: 0001-clk-sunxi-fix-a-missing-check-bug-in-sunxi_divs_clk_.patch
#Fix for CVE-2019-19338
Patch43: 0001-KVM-vmx-implement-MSR_IA32_TSX_CTRL-disable-RTM-func.patch
Patch44: 0001-KVM-vmx-use-MSR_IA32_TSX_CTRL-to-hard-disable-TSX-on.patch
#Fix for CVE-2024-0565
Patch46: 0001-smb-client-fix-OOB-in-receive_encrypted_standard.patch
# Fix for CVE-2020-16119
Patch57: 0001-dccp-ccid-move-timers-to-struct-dccp_sock.patch
Patch58: 0002-Revert-dccp-don-t-free-ccid2_hc_tx_sock-struct-in-dc.patch

#Fix for CVE-2020-16120
Patch59: 0001-ovl-pass-correct-flags-for-opening-real-directory.patch
Patch60: 0002-ovl-switch-to-mounter-creds-in-readdir.patch
Patch61: 0003-ovl-verify-permissions-in-ovl_path_open.patch
Patch62: 0004-ovl-call-secutiry-hook-in-ovl_real_ioctl.patch
Patch63: 0005-ovl-check-permission-to-open-real-file.patch

# Fix for CVE-2019-19770
Patch64: 0001-block-revert-back-to-synchronous-request_queue-remov.patch
Patch65: 0002-block-create-the-request_queue-debugfs_dir-on-regist.patch

#Fix for CVE-2020-36385
Patch66: 0001-RDMA-cma-Add-missing-locking-to-rdma_accept.patch
Patch67: 0001-RDMA-ucma-Rework-ucma_migrate_id-to-avoid-races-with.patch

#Fix for CVE-2022-1055
Patch68: 0001-net-sched-fix-use-after-free-in-tc_new_tfilter.patch

# CVE-2022-1789
Patch69: 0001-KVM-x86-mmu-fix-NULL-pointer-dereference-on-guest-IN.patch

# Fix for CVE-2022-39189
Patch72: 0001-KVM-x86-do-not-report-a-vCPU-as-preempted-outside-in.patch

# Fix for CVE-2022-36123
Patch73: 0001-x86-xen-Use-clear_bss-for-Xen-PV-guests.patch

# Fix for CVE-2021-4037
Patch75: 0001-xfs-ensure-that-the-inode-uid-gid-match-values-match.patch
Patch76: 0002-xfs-remove-the-icdinode-di_uid-di_gid-members.patch
Patch77: 0003-xfs-fix-up-non-directory-creation-in-SGID-directorie.patch

# SEV, TDX
Patch85: 0001-x86-boot-Avoid-VE-during-boot-for-TDX-platforms.patch

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

# Patch to add drbg_pr_ctr_aes256 test vectors to testmgr
Patch98: 0001-Add-drbg_pr_ctr_aes256-test-vectors-and-test-to-test.patch
# NSX requirements (should be removed)
Patch99: LKCM.patch
# Patch to call drbg and dh crypto tests from tcrypt
Patch100: 0001-tcrypt-disable-tests-that-are-not-enabled-in-photon.patch
#HCX-Patches
Patch102: 0001-Active-probing-of-dst-mac-of-unknown-unicast.patch
Patch103: 0002-Skip-IP_ECN_decapsulate-for-gretap-devices.patch
Patch104: 0003-Handle-ipsec-in-ipip-more-correctly.patch
Patch105: 0004-De-cap-fou-traffic-into-correct-tunnel-device-s.patch
Patch106: 0005-Add-unknown-fou-tracking-to-kernel.patch
Patch107: 0006-Add-initial-support-for-vxlan-trunk-to-cgw-kernel-wi.patch
Patch108: 0007-Changes-for-bridge-vlan-arp-filtering-to-work-right.patch
Patch109: 0008-Add-support-for-mac-flapping-and-long-mac-flapping-p.patch
Patch110: 0009-vmxnet3-Avoid-fragmentation-by-giving-each-vmxnet3-d.patch
Patch111: 0010-RPS-flow-balance.patch
Patch112: 0011-add-mss-clamp-support-to-gretap-baseimage.patch
Patch113: 0012-set-max_mtu-as-IP_MAX_MTU.patch
Patch114: 0013-set-max_mtu-as-IP_MAX_MTU_for_vlan.patch
Patch115: 0014-iptunnel-mark-xfrm-multi-parts.patch
Patch116: 0015-disable-pskb_inet_may_pull-in-tunnel.patch
Patch117: 0016-gre_tap-interface-mss_clamp-support.patch

# Update vmxnet3 driver to version 6
Patch120: 0001-vmxnet3-fix-cksum-offload-issues-for-tunnels-with-no.patch
Patch121: 0002-vmxnet3-prepare-for-version-6-changes.patch
Patch122: 0003-vmxnet3-add-support-for-32-Tx-Rx-queues.patch
Patch123: 0004-vmxnet3-add-support-for-ESP-IPv6-RSS.patch
Patch124: 0001-vmxnet3-set-correct-hash-type-based-on-rss-informati.patch
Patch125: 0006-vmxnet3-increase-maximum-configurable-mtu-to-9190.patch
Patch126: 0007-vmxnet3-update-to-version-6.patch
Patch127: 0008-vmxnet3-fix-minimum-vectors-alloc-issue.patch
Patch128: 0009-vmxnet3-remove-power-of-2-limitation-on-the-queues.patch

# Update vmxnet3 driver to version 7
Patch130: 0001-vmxnet3-prepare-for-version-7-changes.patch
Patch131: 0002-vmxnet3-add-support-for-capability-registers.patch
Patch132: 0003-vmxnet3-add-support-for-large-passthrough-BAR-regist.patch
Patch133: 0004-vmxnet3-add-support-for-out-of-order-rx-completion.patch
Patch134: 0005-vmxnet3-add-command-to-set-ring-buffer-sizes.patch
Patch135: 0006-vmxnet3-limit-number-of-TXDs-used-for-TSO-packet.patch
Patch136: 0007-vmxnet3-use-ext1-field-to-indicate-encapsulated-pack.patch
Patch137: 0008-vmxnet3-update-to-version-7.patch
Patch138: 0009-vmxnet3-disable-overlay-offloads-if-UPT-device-does-.patch
Patch139: 0001-vmxnet3-do-not-reschedule-napi-for-rx-processing.patch
Patch140: 0001-vmxnet3-correctly-report-encapsulated-LRO-packet.patch
Patch141: 0002-vmxnet3-use-correct-intrConf-reference-when-using-ex.patch
Patch142: 0001-vmxnet3-correctly-report-csum_level-for-encapsulated.patch
# Custom patch to compatible with HCX changes
Patch143: 0001-hcx-vmxnet3-move-rss-code-block-under-eop-descriptor.patch
Patch144: 0001-vmxnet3-use-gro-callback-when-UPT-is-enabled.patch

# Patch to fix Panic due to nested priority inheritance in sched_deadline
Patch145: 0001-sched-deadline-Fix-BUG_ON-condition-for-deboosted-ta.patch

# Patch to distribute the tasks within affined cpus
Patch146: 0001-sched-core-Distribute-tasks-within-affinity-masks.patch

# Allow cpuidle subsystem to use acpi_idle driver when only one C-state is available
Patch147: 0001-ACPI-processor-idle-Allow-probing-on-platforms-with-.patch

# Lockdown support
Patch150: lockdown/0001-Add-the-ability-to-lock-down-access-to-the-running-k.patch
Patch151: lockdown/0003-ima-require-secure_boot-rules-in-lockdown-mode.patch
Patch152: lockdown/0004-Enforce-module-signatures-if-the-kernel-is-locked-do.patch
Patch153: lockdown/0005-Restrict-dev-mem-kmem-port-when-the-kernel-is-locked.patch
Patch154: lockdown/0006-kexec-Disable-at-runtime-if-the-kernel-is-locked-dow.patch
Patch155: lockdown/0007-Copy-secure_boot-flag-in-boot-params-across-kexec-re.patch
Patch156: lockdown/0008-kexec_file-Restrict-at-runtime-if-the-kernel-is-lock.patch
Patch157: lockdown/0009-hibernate-Disable-when-the-kernel-is-locked-down.patch
Patch158: lockdown/0010-uswsusp-Disable-when-the-kernel-is-locked-down.patch
Patch159: lockdown/0011-PCI-Lock-down-BAR-access-when-the-kernel-is-locked-d.patch
Patch160: lockdown/0012-x86-Lock-down-IO-port-access-when-the-kernel-is-lock.patch
Patch161: lockdown/0013-x86-msr-Restrict-MSR-access-when-the-kernel-is-locke.patch
Patch162: lockdown/0014-asus-wmi-Restrict-debugfs-interface-when-the-kernel-.patch
Patch163: lockdown/0015-ACPI-Limit-access-to-custom_method-when-the-kernel-i.patch
Patch164: lockdown/0016-acpi-Ignore-acpi_rsdp-kernel-param-when-the-kernel-h.patch
Patch165: lockdown/0017-acpi-Disable-ACPI-table-override-if-the-kernel-is-lo.patch
Patch166: lockdown/0018-acpi-Disable-APEI-error-injection-if-the-kernel-is-l.patch
Patch167: lockdown/0020-Prohibit-PCMCIA-CIS-storage-when-the-kernel-is-locke.patch
Patch168: lockdown/0021-Lock-down-TIOCSSERIAL.patch
Patch169: lockdown/0022-Lock-down-module-params-that-specify-hardware-parame.patch
Patch170: lockdown/0023-x86-mmiotrace-Lock-down-the-testmmiotrace-module.patch
Patch171: lockdown/0024-debugfs-Disallow-use-of-debugfs-files-when-the-kerne.patch
Patch172: lockdown/0025-Lock-down-proc-kcore.patch
Patch173: lockdown/0026-Lock-down-kprobes.patch
Patch174: lockdown/0027-bpf-Restrict-kernel-image-access-functions-when-the-.patch
Patch175: lockdown/0028-efi-Add-an-EFI_SECURE_BOOT-flag-to-indicate-secure-b.patch
Patch176: lockdown/0029-efi-Lock-down-the-kernel-if-booted-in-secure-boot-mo.patch
Patch177: lockdown/enable-cold-boot-attack-mitigation.patch
Patch178: lockdown/mtd-disable-slram-and-phram-when-locked-down.patch
Patch179: lockdown/security-Add-a-locked-down-LSM-hook.patch
Patch180: lockdown/ACPI-Limit-access-to-custom_method-when-the-kernel-i.patch
Patch181: lockdown/efi-Restrict-efivar_ssdt_load-when-the-kernel-is-locked-down.patch
Patch182: lockdown/ACPI-configfs-Disallow-loading-ACPI-tables-when-locked-down.patch

# Next 2 patches are about to be merged into stable
Patch187: 0001-mm-fix-panic-in-__alloc_pages.patch

# Disable md5 algorithm for sctp if fips is enabled.
Patch189: 0001-disable-md5-algorithm-for-sctp-if-fips-is-enabled.patch

# Fix for CVE-2021-4204
Patch192: 0002-bpf-Disallow-unprivileged-bpf-by-default.patch

# CVE-2022-43945
Patch193: 0001-NFSD-Cap-rsize_bop-result-based-on-send-buffer-size.patch
Patch194: 0002-NFSD-Protect-against-send-buffer-overflow-in-NFSv3-R.patch
Patch195: 0003-NFSD-Protect-against-send-buffer-overflow-in-NFSv2-R.patch
Patch196: 0004-NFSD-Protect-against-send-buffer-overflow-in-NFSv3-R.patch

#Fix for CVE-2022-0480
Patch198: 0001-memcg-enable-accounting-for-file-lock-caches.patch

#Fix for CVE-2022-3061
Patch199: 0001-video-fbdev-i740fb-Error-out-if-pixclock-equals-zero.patch

#Fix for CVE-2022-3303
Patch200: 0001-ALSA-pcm-oss-Fix-race-at-SNDCTL_DSP_SYNC.patch

# Fix for CVE-2023-28466
Patch201: 0001-net-prevent-race-condition-in-do_tls_getsockopt_tx.patch

# CVE-2023-1611
Patch202: 0001-btrfs-fix-race-between-quota-disable-and-quota-assig.patch

#Fix for CVE-2023-1076
Patch203: 0001-net-add-sock_init_data_uid.patch
Patch204: 0001-tap-tap_open-correctly-initialize-socket-uid.patch
Patch205: 0001-tun-tun_chr_open-correctly-initialize-socket-uid.patch

#Fix for CVE-2023-2124
Patch208: 0001-xfs-verify-buffer-contents-when-we-skip-log-replay.patch

#Fix for CVE-2023-39197
Patch209: 0001-netfilter-conntrack-dccp-copy-entire-header-to-stack.patch

#Fix CVE-2023-51779
Patch211: 0001-Bluetooth-af_bluetooth-Fix-Use-After-Free-in-bt_sock.patch

# Fix CVE-2024-23307
Patch212: 0001-md-raid5-fix-atomicity-violation-in-raid5_cache_coun.patch

#Fix CVE-2023-52509
Patch214: 0001-ravb-Fix-use-after-free-issue-in-ravb_tx_timeout_wor.patch

#Fix CVE-2023-52458
Patch215: 0001-block-add-check-that-partition-length-needs-to-be-al.patch

# Fix CVE-2021-46952
Patch217: 0001-NFS-fs_context-validate-UDP-retrans-to-prevent-shift.patch

#Fix CVE-2024-26882
Patch221: 0001-net-ip_tunnel-make-sure-to-pull-inner-header-in-ip_tunnel_rcv.patch

# Fix CVE-2024-38538
Patch222: 0001-net-bridge-xmit-make-sure-we-have-at-least-eth-heade.patch

# Fix CVE-2024-38588
Patch223: 0001-ftrace-Fix-possible-use-after-free-issue-in-ftrace_l.patch

%if 0%{?kat_build}
Patch1000: fips-kat-tests.patch
%endif

# Usermode helper fixes
Patch1540: 0001-umh-Add-command-line-to-user-mode-helpers.patch
Patch1541: 0002-umh-add-exit-routine-for-UMH-process.patch

# BPFilter fixes
Patch1545: 0001-net-bpfilter-use-cleanup-callback-to-release-umh_inf.patch
Patch1546: 0002-net-bpfilter-restart-bpfilter_umh-when-error-occurre.patch
Patch1547: 0003-net-bpfilter-disallow-to-remove-bpfilter-module-whil.patch
Patch1548: 0004-net-bpfilter-dont-use-module_init-in-non-modular-cod.patch
Patch1549: 0005-net-bpfilter-fallback-to-netfilter-if-failed-to-load.patch

BuildArch: x86_64

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
BuildRequires:  bison
BuildRequires:  gettext

Requires:       filesystem
Requires:       kmod
Requires(pre): (coreutils or toybox)
Requires(preun): (coreutils or toybox)
Requires(post): (coreutils or toybox)
Requires(postun): (coreutils or toybox)

%description
Security hardened Linux kernel.

%package lkcm
Summary:       LKCM module
Group:         System Environment/Kernel
Requires:      %{name} = %{version}-%{release}
%description lkcm
The Linux package contains the LKCM driver module

%package devel
Summary:       Kernel Dev
Group:         System Environment/Kernel
Requires:      python2
Requires:      gawk
Requires:      %{name} = %{version}-%{release}
%description devel
The Linux package contains the Linux kernel dev files

%package docs
Summary:       Kernel docs
Group:         System Environment/Kernel
Requires:      python2
Requires:      %{name} = %{version}-%{release}
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

%prep
# Using autosetup is not feasible
%setup -q -n linux-%{version}
# Using autosetup is not feasible
%setup -q -T -D -b5 -n linux-%{version}

%autopatch -p1 -m0 -M98

pushd ..
%patch99 -p0
popd

%autopatch -p1 -m100 -M191

# CVE Fixes
%autopatch -p1 -m192 -M223

%if 0%{?kat_build}
%patch1000 -p1
%endif

# Usermode helper patches
%autopatch -p1 -m1540 -M1541

# bpfilter patches
%autopatch -p1 -m1545 -M1549

make mrproper %{?_smp_mflags}
cp %{SOURCE1} .config
sed -i 's/CONFIG_LOCALVERSION="-secure"/CONFIG_LOCALVERSION="-%{release}-secure"/' .config

%include %{SOURCE4}

# patch vmw_balloon driver
sed -i 's/module_init/late_initcall/' drivers/misc/vmw_balloon.c

%build
make VERBOSE=1 KBUILD_BUILD_VERSION="1-photon" \
            KBUILD_BUILD_HOST="photon" ARCH="x86_64" %{?_smp_mflags}

bldroot="${PWD}"

# build LKCM module
pushd ../LKCM
sed -i '/#include <asm\/uaccess.h>/d' drv_fips_test.c
sed -i '/#include <asm\/uaccess.h>/d' fips_test.c
make -C ${bldroot} M="${PWD}" modules %{?_smp_mflags}
popd

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

# __os_install_post strips signature from modules. We need to resign it again
# and then compress. Extra step is added to the default __spec_install_post.
%define __spec_install_post \
  %{?__debug_package:%{__debug_install_post}} \
  %{__arch_install_post} \
  %{__os_install_post} \
  %{__modules_install_post} \
  %{__modules_gen_hmac} \
%{nil}

%install
install -vdm 755 %{buildroot}%{_sysconfdir}
install -vdm 755 %{buildroot}/boot
install -vdm 755 %{buildroot}%{_defaultdocdir}/linux-%{uname_r}
install -vdm 755 %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}
make INSTALL_MOD_PATH=%{buildroot} modules_install %{?_smp_mflags}

bldroot="${PWD}"

# install LKCM module
pushd ../LKCM
make -C ${bldroot} M="${PWD}" INSTALL_MOD_PATH=%{buildroot} \
            modules_install %{?_smp_mflags}
popd

#install photon-checksum-generator module
pushd ../photon-checksum-generator-%{photon_checksum_generator_version}/kernel
make -C ${bldroot} M="${PWD}" INSTALL_MOD_PATH=%{buildroot} \
            modules_install %{?_smp_mflags}
popd

cp -v arch/x86/boot/bzImage %{buildroot}/boot/vmlinuz-%{uname_r}
cp -v System.map %{buildroot}/boot/System.map-%{uname_r}
cp -v .config %{buildroot}/boot/config-%{uname_r}
cp -r Documentation/* %{buildroot}%{_defaultdocdir}/linux-%{uname_r}

%if 0%{?__debug_package}
install -vdm 755 %{buildroot}%{_libdir}/debug/%{_modulesdir}
cp -v vmlinux %{buildroot}%{_libdir}/debug/%{_modulesdir}/vmlinux-%{uname_r}
%endif

# Since we use compressed modules we cann't use load pinning,
# because .ko files will be loaded from the memory (LoadPin: obj=<unknown>)
cat > %{buildroot}/boot/linux-%{uname_r}.cfg << "EOF"
# GRUB Environment Block
photon_cmdline=init=/lib/systemd/systemd ro loglevel=3 quiet no-vmw-sta loadpin.enabled=0 audit=1 slub_debug=P page_poison=1 slab_nomerge pti=on cgroup.memory=nokmem
photon_linux=vmlinuz-%{uname_r}
photon_initrd=initrd.img-%{uname_r}
EOF

# Register myself to initramfs
mkdir -p %{buildroot}%{_sharedstatedir}/initramfs/kernel
cat > %{buildroot}%{_sharedstatedir}/initramfs/kernel/%{uname_r} << "EOF"
--add-drivers "xen-scsifront xen-blkfront xen-acpi-processor xen-evtchn xen-gntalloc xen-gntdev xen-privcmd xen-pciback xenfs hv_utils hv_vmbus hv_storvsc hv_netvsc hv_sock hv_balloon cn dm-mod"
EOF

# cleanup dangling symlinks
rm -f %{buildroot}%{_modulesdir}/source \
      %{buildroot}%{_modulesdir}/build

# create /use/src/linux-headers-*/ content
find . -name Makefile* -o -name Kconfig* -o -name *.pl | xargs sh -c 'cp --parents "$@" %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}' copy

find arch/x86/include include scripts -type f | xargs sh -c 'cp --parents "$@" %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}' copy

find $(find arch/x86 -name include -o -name scripts -type d) -type f | xargs sh -c 'cp --parents "$@" %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}' copy

find arch/x86/include Module.symvers include scripts -type f | xargs sh -c 'cp --parents "$@" %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}' copy

# CONFIG_STACK_VALIDATION=y requires objtool to build external modules
install -vsm 755 tools/objtool/objtool %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}/tools/objtool/
install -vsm 755 tools/objtool/fixdep %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}/tools/objtool/

# copy .config manually to be where it's expected to be
cp .config %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}
# symlink to the build folder
ln -sf %{_usrsrc}/linux-headers-%{uname_r} %{buildroot}%{_modulesdir}/build

%include %{SOURCE2}
%include %{SOURCE3}

%post
/sbin/depmod -a %{uname_r}
ln -sf linux-%{uname_r}.cfg /boot/photon.cfg

%post lkcm
/sbin/depmod -a %{uname_r}

%post hmacgen
/sbin/depmod -a %{uname_r}

%files
%defattr(-,root,root)
/boot/System.map-%{uname_r}
/boot/config-%{uname_r}
/boot/vmlinuz-%{uname_r}
/boot/.vmlinuz-%{uname_r}.hmac
%config(noreplace) /boot/linux-%{uname_r}.cfg
%config %{_sharedstatedir}/initramfs/kernel/%{uname_r}
/lib/modules/*
%exclude %{_modulesdir}/build
%exclude %{_usrsrc}
%exclude %{_modulesdir}/extra/fips_lkcm.ko.xz
%exclude %{_modulesdir}/extra/hmac_generator.ko.xz
%exclude %{_modulesdir}/extra/.hmac_generator.ko.xz.hmac

%files lkcm
%defattr(-,root,root)
%{_modulesdir}/extra/fips_lkcm.ko.xz

%files hmacgen
%defattr(-,root,root)
%{_modulesdir}/extra/hmac_generator.ko.xz
%{_modulesdir}/extra/.hmac_generator.ko.xz.hmac

%files docs
%defattr(-,root,root)
%{_defaultdocdir}/linux-%{uname_r}/*

%files devel
%defattr(-,root,root)
%{_modulesdir}/build
%{_usrsrc}/linux-headers-%{uname_r}

%changelog
* Tue Nov 19 2024 Ajay Kaher <ajay.kaher@broadcom.com> 4.19.324-1
- Update to version 4.19.324
* Mon Nov 04 2024 Kuntal Nayak <kuntal.nayak@broadcom.com> 4.19.323-1
- Update to version 4.19.323
- Fix CVE-2024-38588
* Thu Sep 26 2024 Ankit Jain <ankit-aj.jain@broadcom.com> 4.19.321-2
- Fix for CVE-2024-38538
* Tue Sep 10 2024 Ankit Jain <ankit-aj.jain@broadcom.com> 4.19.321-1
- Update to version 4.19.321
* Wed Aug 21 2024 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 4.19.320-1
- Update to version 4.19.320
* Mon Aug 12 2024 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 4.19.319-1
- Update to version 4.19.319
* Tue Aug 06 2024 Ajay Kaher <ajay.kaher@broadcom.com> 4.19.317-2
- Fix hcx crash while executing rmmod ipip
* Wed Jul 10 2024 Ajay Kaher <ajay.kaher@broadcom.com> 4.19.317-1
- Update to version 4.19.317
* Wed Jun 19 2024 Ashwin Dayanand Kamat <ashwin.kamat@broadcom.com> 4.19.316-1
- Update to version 4.19.316
* Thu May 30 2024 Kuntal Nayak <kuntal.nayak@broadcom.com> 4.19.315-1
- Update to version 4.19.315, rt134
* Tue May 14 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 4.19.313-1
- Update to version 4.19.313
* Mon May 06 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 4.19.311-4
- Fixes CVE-2024-26882
* Thu Apr 25 2024 Ankit Jain <ankit-aj.jain@broadcom.com> 4.19.311-3
- Fixes CVE-2021-46952
* Fri Apr 05 2024 Srish Srinivasan <srish.srinivasan@broadcom.com> 4.19.311-2
- Patched CVE-2023-52429/CVE-2024-23851
* Wed Apr 03 2024 Keerthana K <keerthana.kalyanasundaram@broadcom.com> 4.19.311-1
- Update to version 4.19.311
* Mon Apr 01 2024 Keerthana K <keerthana.kalyanasundaram@broadcom.com> 4.19.307-6
- Fix CVE-2024-26642, CVE-2023-52620
* Mon Mar 25 2024 Ashwin Dayanand Kamat <ashwin.kamat@broadcom.com> 4.19.307-5
- Fix for CVE-2023-52458
* Thu Mar 21 2024 Kuntal Nayak <kuntal.nayak@broadcom.com> 4.19.307-4
- Fix CVE-2022-48627
* Wed Mar 20 2024 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 4.19.307-3
- Fix CVE-2023-52509
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
* Wed Sep 20 2023 Roye Eshed <eshedr@vmware.com> 4.19.292-3
- Fix for CVE-2023-42753
* Fri Sep 01 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 4.19.292-2
- Disable CONFIG_SCSI_DPT_I2O to fix CVE-2023-2007
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
- Fix for CVE-2022-39189/2022-36123
* Tue Aug 30 2022 Brennan Lamoreaux <blamoreaux@vmware.com> 4.19.256-1
- Update to version 4.19.256
* Tue Aug 09 2022 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.247-12
- Fix for CVE-2022-2586 and CVE-2022-2588
* Mon Aug 08 2022 Jonathan Shao <sjonathan@vmware.com> 4.19.247-11
- Add HCX specific patches
* Wed Aug 03 2022 Shreenidhi Shedi <sshedi@vmware.com> 4.19.247-10
- Scriptlets fixes and improvements
* Tue Aug 02 2022 Sharan Turlapati <sturlapati@vmware.com> 4.19.247-9
- Revert napi reschedule on rx in vmxnet3 driver
* Tue Aug 02 2022 Ankit Jain <ankitja@vmware.com> 4.19.247-8
- Fix BUG_ON for deboosted tasks
* Tue Jul 12 2022 Ankit Jain <ankitja@vmware.com> 4.19.247-7
- Backported the fix for CVE-2022-1789
* Thu Jul 07 2022 Shreenidhi Shedi <sshedi@vmware.com> 4.19.247-6
- Spec improvements
* Wed Jul 06 2022 Shreenidhi Shedi <sshedi@vmware.com> 4.19.247-5
- Add kernel as requires to hmacgen postun
* Thu Jun 30 2022 Ankit Jain <ankitja@vmware.com> 4.19.247-4
- Fixes panic due to nested priority inheritance
* Thu Jun 23 2022 Sharan Turlapati <sturlapati@vmware.com> 4.19.247-3
- Update vmxnet3 driver to version 7
* Wed Jun 22 2022 Sharan Turlapati <sturlapati@vmware.com> 4.19.247-2
- Update vmxnet3 driver to version 6
* Tue Jun 14 2022 Ajay Kaher <akaher@vmware.com> 4.19.247-1
- Update to version 4.19.247
* Thu May 26 2022 Sharan Turlapati <sturlapati@vmware.com> 4.19.245-1
- Update to version 4.19.245
* Mon May 16 2022 Brennan Lamoreaux <blamoreaux@vmware.com> 4.19.241-3
- Fix for CVE-2022-1048
* Fri May 13 2022 Alexey Makhalov <amakhalov@vmware.com> 4.19.241-2
- Add objtool to the -devel package.
* Wed May 11 2022 Brennan Lamoreaux <blamoreaux@vmware.com> 4.19.241-1
- Update to version 4.19.241
* Fri Apr 29 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 4.19.240-1
- Update to version 4.19.240
- Fix CVE-2022-1055
* Mon Apr 18 2022 Harinadh D <hdommaraju@vmware.com> 4.19.232-4
- Set max MTU as IP_MAX_MTU for type vlan
* Mon Apr 18 2022 Harinadh D <hdommaraju@vmware.com> 4.19.232-3
- Set max MTU as IP_MAX_MTU for type vxlantrunk
* Mon Mar 21 2022 Ajay Kaher <akaher@vmware.com> 4.19.232-2
- Fix for CVE-2022-1016
* Mon Mar 07 2022 srinidhira0 <srinidhir@vmware.com> 4.19.232-1
- Update to version 4.19.232
* Tue Feb 15 2022 Alexey Makhalov <amakhalov@vmware.com> 4.19.229-2
- .config: enable zstd compression for squashfs.
- .config: enable crypto user api rng.
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
* Mon Jan 03 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 4.19.219-5
- Disable md5 algorithm for sctp if fips is enabled.
* Mon Dec 20 2021 Harinadh D <hdommaraju@vmware.com> 4.19.219-4
- remove lvm in add-drivers list
- lvm drivers are built as part of dm-mod module
* Wed Dec 15 2021 Alexey Makhalov <amakhalov@vmware.com> 4.19.219-3
- mm: fix percpu alloacion for memoryless nodes
- pvscsi: fix disk detection issue
* Tue Dec 14 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.219-2
- Fix for CVE-2020-36385
* Wed Dec 08 2021 srinidhira0 <srinidhir@vmware.com> 4.19.219-1
- Update to version 4.19.219
* Wed Nov 24 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.217-1
- Update to version 4.19.217
* Tue Nov 23 2021 Keerthana K <keerthanak@vmware.com> 4.19.214-3
- HCX: fix fou_unknown netlink registration
* Fri Oct 29 2021 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 4.19.214-2
- Fix for CVE-2020-36322/CVE-2021-28950
* Thu Oct 28 2021 Sharan Turlapati <sturlapati@vmware.com> 4.19.214-1
- Update to version 4.19.214
* Wed Sep 29 2021 Keerthana K <keerthanak@vmware.com> 4.19.208-1
- Update to version 4.19.208
* Fri Aug 27 2021 srinidhira0 <srinidhir@vmware.com> 4.19.205-1
- Update to version 4.19.205
* Tue Jul 27 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.198-1
- Update to version 4.19.198
* Thu Jul 15 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.191-5
- Fix for CVE-2021-33909
* Fri Jul 02 2021 Keerthana K <keerthanak@vmware.com> 4.19.191-4
- HCX custom patches
- Enable HCX kernel configs
* Thu Jun 24 2021 Loïc <4661917+HacKurx@users.noreply.github.com> 4.19.191-3
- EMUTRAMP: use the prefix X86_ for error codes
* Tue Jun 22 2021 Sharan Turlapati <sturlapati@vmware.com> 4.19.191-2
- Fix for CVE-2021-3609
* Tue Jun 01 2021 Keerthana K <keerthanak@vmware.com> 4.19.191-1
- Update to version 4.19.191
- .config: Enable CONFIG_FANOTIFY_ACCESS_PERMISSIONS
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
- Enable KPP and ECDH configs for FIPS.
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
* Mon Jan 04 2021 Ankit Jain <ankitja@vmware.com> 4.19.164-1
- Update to version 4.19.164
* Tue Dec 15 2020 Vikash Bansal <bvikas@vmware.com> 4.19.163-1
- Update to version 4.19.163
* Wed Dec 09 2020 Srinidhi Rao <srinidhir@vmware.com> 4.19.160-2
- Fix for CVE-2019-19770
* Wed Dec 02 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.160-1
- Update to version 4.19.160
- Fix CVE-2019-19338
* Tue Dec 01 2020 Vikash Bansal <bvikas@vmware.com> 4.19.154-7
- Lockdown patches
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
* Tue Oct 13 2020 Ajay Kaher <akaher@vmware.com> 4.19.150-1
- Update to version 4.19.150
* Mon Oct 12 2020 Ajay Kaher <akaher@vmware.com> 4.19.148-4
- Fix for CVE-2020-16120
* Mon Oct 12 2020 Ankit Jain <ankitja@vmware.com> 4.19.148-3
- Fix for CVE-2020-16119
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
* Wed Aug 05 2020 Harinadh D <hdommaraju@vmware.com> 4.19.132-5
- Apply HCX mac-flap and mac-flap-long patches
* Tue Aug 04 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.132-4
- Upgrade vmxnet3 driver to version 4
* Wed Jul 29 2020 Keerthana K <keerthanak@vmware.com> 4.19.132-3
- Apply HCX patches
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
* Tue Jan 14 2020 Srinidhi Rao <srinidhir@vmware.com> 4.19.87-4
- Enable DRBG HASH and DRBG CTR support.
* Thu Jan 02 2020 Keerthana K <keerthanak@vmware.com> 4.19.87-3
- Modify tcrypt to remove tests for algorithms that are not supported in photon.
- Added tests for DH, DRBG algorithms.
* Fri Dec 20 2019 Keerthana K <keerthanak@vmware.com> 4.19.87-2
- Update fips Kat tests.
* Fri Dec 06 2019 Ajay Kaher <akaher@vmware.com> 4.19.87-1
- Update to version 4.19.87
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
* Tue Jul 02 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.52-2
- Fix 9p vsock 16bit port issue.
* Mon Jun 17 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.52-1
- Update to version 4.19.52
- Fix CVE-2019-12456, CVE-2019-12379, CVE-2019-12380, CVE-2019-12381,
- CVE-2019-12382, CVE-2019-12378, CVE-2019-12455
* Tue May 28 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.40-3
- Change default I/O scheduler to 'deadline' to fix performance issue.
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
* Thu Jan 10 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.6-4
- cmdline: added audit=1 pti=on
- config: PANIC_TIMEOUT=-1, DEBUG_RODATA_TEST=y
* Wed Jan 09 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.6-3
- Additional security hardening options in the config.
* Fri Jan 04 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.6-2
- Enable AppArmor by default.
* Mon Dec 10 2018 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.6-1
- Update to version 4.19.6
* Thu Nov 15 2018 Ajay Kaher <akaher@vmware.com> 4.19.1-2
- Adding BuildArch
* Thu Nov 08 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.1-1
- Update to version 4.19.1
* Tue Oct 30 2018 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.18.9-3
- Fix PAX randkstack and RAP plugin patches to avoid boot panic.
* Mon Oct 22 2018 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.18.9-2
- Use updated steal time accounting patch.
* Tue Sep 25 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.18.9-1
- Update to version 4.18.9
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
* Mon Mar 19 2018 Alexey Makhalov <amakhalov@vmware.com> 4.14.8-2
- Extra hardening: slab_nomerge and some .config changes
* Fri Feb 16 2018 Alexey Makhalov <amakhalov@vmware.com> 4.14.8-1
- Version update to v4.14 LTS. Drop aufs support.
* Mon Dec 04 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.66-1
- Version update
* Tue Nov 21 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.64-1
- Version update
* Wed Nov 08 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.60-2
- Update LKCM module
- Add -lkcm subpackage
* Mon Nov 06 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.60-1
- Version update
* Wed Oct 11 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.53-3
- Add patch "KVM: Don't accept obviously wrong gsi values via
    KVM_IRQFD" to fix CVE-2017-1000252.
* Tue Oct 10 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.53-2
- Build hang (at make oldconfig) fix.
* Thu Oct 05 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.53-1
- Version update
* Mon Oct 02 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.52-3
- Allow privileged CLONE_NEWUSER from nested user namespaces.
* Mon Oct 02 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.52-2
- Fix CVE-2017-11472 (ACPICA: Namespace: fix operand cache leak)
* Mon Oct 02 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.52-1
- Version update
* Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.47-2
- Requires coreutils or toybox
* Mon Sep 04 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.47-1
- Fix CVE-2017-11600
* Tue Aug 22 2017 Anish Swaminathan <anishs@vmware.com> 4.9.43-2
- Add missing xen block drivers
* Mon Aug 14 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.43-1
- Version update
- [feature] new sysctl option unprivileged_userns_clone
* Wed Aug 09 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.41-2
- Fix CVE-2017-7542
- [bugfix] Added ccm,gcm,ghash,lzo crypto modules to avoid
    panic on modprobe tcrypt
* Mon Aug 07 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.41-1
- Version update
* Fri Aug 04 2017 Bo Gan <ganb@vmware.com> 4.9.38-6
- Fix initramfs triggers
* Tue Aug 01 2017 Anish Swaminathan <anishs@vmware.com> 4.9.38-5
- Allow some algorithms in FIPS mode
- Reverts 284a0f6e87b0721e1be8bca419893902d9cf577a and backports
- bcf741cb779283081db47853264cc94854e7ad83 in the kernel tree
- Enable additional NF features
* Fri Jul 21 2017 Anish Swaminathan <anishs@vmware.com> 4.9.38-4
- Add patches in Hyperv codebase
* Fri Jul 21 2017 Anish Swaminathan <anishs@vmware.com> 4.9.38-3
- Add missing hyperv drivers
* Thu Jul 20 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.38-2
- Disable scheduler beef up patch
* Tue Jul 18 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.38-1
- Fix CVE-2017-11176 and CVE-2017-10911
* Fri Jul 14 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.34-3
- Remove aufs source tarballs from git repo
* Mon Jul 03 2017 Xiaolin Li <xiaolinl@vmware.com> 4.9.34-2
- Add libdnet-devel, kmod-devel and libmspack-devel to BuildRequires
* Wed Jun 28 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.34-1
- [feature] 9P FS security support
- [feature] DM Delay target support
- Fix CVE-2017-1000364 ("stack clash") and CVE-2017-9605
* Thu Jun 8 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.31-1
- Fix CVE-2017-8890, CVE-2017-9074, CVE-2017-9075, CVE-2017-9076
    CVE-2017-9077 and CVE-2017-9242
- [feature] IPV6 netfilter NAT table support
* Fri May 26 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.30-1
- Fix CVE-2017-7487 and CVE-2017-9059
* Wed May 17 2017 Vinay Kulkarni <kulkarniv@vmware.com> 4.9.28-2
- Enable IPVLAN module.
* Tue May 16 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.28-1
- Version update
* Wed May 10 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.27-1
- Version update
* Sun May 7 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.26-1
- Version update
- Removed version suffix from config file name
* Thu Apr 27 2017 Bo Gan <ganb@vmware.com> 4.9.24-2
- Support dynamic initrd generation
* Tue Apr 25 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.24-1
- Fix CVE-2017-6874 and CVE-2017-7618.
- .config: build nvme and nvme-core in kernel.
* Tue Mar 21 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.13-3
- Added LKCM module
* Mon Mar 6 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.13-2
- .config: NSX requirements for crypto and netfilter
* Tue Feb 28 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.13-1
- Update to linux-4.9.13 to fix CVE-2017-5986 and CVE-2017-6074
- .config: disable XEN guest (needs rap_plugin verification)
* Wed Feb 22 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.9-2
- rap_plugin improvement: throw error on function type casting
  function signatures were cleaned up using this feature.
- Added RAP_ENTRY for asm functions.
* Thu Feb 09 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.9-1
- Update to linux-4.9.9 to fix CVE-2016-10153, CVE-2017-5546,
    CVE-2017-5547, CVE-2017-5548 and CVE-2017-5576.
- Added aufs support.
- Added PAX_RANDKSTACK feature.
- Extra func signatures cleanup to fix 1809717 and 1809722.
- .config: added CRYPTO_FIPS support.
* Tue Jan 10 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.2-1
- Update to linux-4.9.2 to fix CVE-2016-10088
- Rename package to linux-secure.
- Added KSPP cmdline params: slub_debug=P page_poison=1
* Mon Dec 19 2016 Xiaolin Li <xiaolinl@vmware.com> 4.9.0-2
- BuildRequires Linux-PAM-devel
* Mon Dec 12 2016 Alexey Makhalov <amakhalov@vmware.com> 4.9.0-1
- Update to linux-4.9.0
- Add paravirt stolen time accounting feature (from linux-esx),
    but disable it by default (no-vmw-sta cmdline parameter)
- Use vmware_io_delay() to keep "void fn(void)" signature
* Wed Nov 30 2016 Alexey Makhalov <amakhalov@vmware.com> 4.8.0-2
- Expand `uname -r` with release number
- Resign and compress modules after stripping
- .config: add syscalls tracing support
- .config: add cgrup_hugetlb support
- .config: add netfilter_xt_{set,target_ct} support
- .config: add netfilter_xt_match_{cgroup,ipvs} support
- .config: disable /dev/mem
* Mon Oct 17 2016 Alexey Makhalov <amakhalov@vmware.com> 4.8.0-1
- Initial commit.
