%global security_hardening none

# Set this flag to 0 to build without canister
%global fips 1

# If kat_build is enabled, canister is not used.
%if 0%{?kat_build}
%global fips 0
%endif

Summary:        Kernel
Name:           linux-secure
Version:        5.10.235
Release:        2%{?kat_build:.kat}%{?dist}
License:        GPLv2
URL:            http://www.kernel.org
Group:          System Environment/Kernel
Vendor:         VMware, Inc.
Distribution:   Photon

%define uname_r %{version}-%{release}-secure
%define _modulesdir /lib/modules/%{uname_r}

Source0:        http://www.kernel.org/pub/linux/kernel/v5.x/linux-%{version}.tar.xz
%define sha512 linux=2f9e7b7689f19b7fd16a577f0f51cb4dd7ecc52b7b7c39f3e518e2760d3f639940c5a212976b92531298ff534d49a7ae667137540d30f7f25e5f7db6dce2abb6
Source1:        config-secure
Source2:        initramfs.trigger
# contains pre, postun, filetriggerun tasks
Source3:        scriptlets.inc
Source4:        check_for_config_applicability.inc

%if 0%{?fips}
Source9:        check_fips_canister_struct_compatibility.inc

%define fips_canister_version 4.0.1-5.10.21-3-secure
Source16:       fips-canister-%{fips_canister_version}.tar.bz2
%define sha512 fips-canister=1d3b88088a23f7d6e21d14b1e1d29496ea9e38c750d8a01df29e1343034f74b0f3801d1f72c51a3d27e9c51113c808e6a7aa035cb66c5c9b184ef8c4ed06f42a
Source18:       fips_canister-kallsyms
Source19:       FIPS-do-not-allow-not-certified-algos-in-fips-2.patch
Source20:       Add-alg_request_report-cmdline.patch
Source21:       0001-LKCM-4.0.1-binary-patching-to-fix-jent-on-AMD-EPYC.patch
Source24:       0001-LKCM-4.0.1-binary-patching-to-fix-struct-aesni_cpu_i.patch
%endif

Source22:       spec_install_post.inc
Source23:       %{name}-dracut.conf

# common
Patch0: net-Double-tcp_mem-limits.patch
Patch1: SUNRPC-Do-not-reuse-srcport-for-TIME_WAIT-socket.patch
Patch2: SUNRPC-xs_bind-uses-ip_local_reserved_ports.patch
Patch3: 9p-transport-for-9p.patch
Patch4: 9p-trans_fd-extend-port-variable-to-u32.patch
Patch5: vsock-delay-detach-of-QP-with-outgoing-data-59.patch

# RDRAND-based RNG driver to enhance the kernel's entropy pool:
Patch6: hwrng-rdrand-Add-RNG-driver-based-on-x86-rdrand-inst.patch
Patch7: 0001-cgroup-v1-cgroup_stat-support.patch

Patch8: Performance-over-security-model.patch

#HyperV patches
Patch11: vmbus-Don-t-spam-the-logs-with-unknown-GUIDs.patch
Patch12: fork-add-sysctl-to-disallow-unprivileged-CLONE_NEWUSER-by.patch

# Out-of-tree patches from AppArmor:
Patch13: apparmor-patch-to-provide-compatibility-with-v2.x-ne.patch
Patch14: apparmor-af_unix-mediation.patch

# Revert crypto api workqueue
Patch15: 0001-Revert-crypto-api-Use-work-queue-in-crypto_destroy_i.patch

#vmxnet3
Patch20: 0001-vmxnet3-Remove-buf_info-from-device-accessible-struc.patch
# Upgrade to version 6
Patch21: 0001-vmxnet3-prepare-for-version-6-changes.patch
Patch22: 0002-vmxnet3-add-support-for-32-Tx-Rx-queues.patch
Patch23: 0003-vmxnet3-remove-power-of-2-limitation-on-the-queues.patch
Patch24: 0004-vmxnet3-add-support-for-ESP-IPv6-RSS.patch
Patch25: 0005-vmxnet3-set-correct-hash-type-based-on-rss-informati.patch
Patch26: 0006-vmxnet3-increase-maximum-configurable-mtu-to-9190.patch
Patch27: 0007-vmxnet3-update-to-version-6.patch
Patch28: 0001-vmxnet3-fix-minimum-vectors-alloc-issue.patch
# Upgrade to version 7
Patch29: 0001-vmxnet3-prepare-for-version-7-changes.patch
Patch30: 0002-vmxnet3-add-support-for-capability-registers.patch
Patch31: 0003-vmxnet3-add-support-for-large-passthrough-BAR-regist.patch
Patch32: 0004-vmxnet3-add-support-for-out-of-order-rx-completion.patch
Patch33: 0005-vmxnet3-add-command-to-set-ring-buffer-sizes.patch
Patch34: 0006-vmxnet3-limit-number-of-TXDs-used-for-TSO-packet.patch
Patch35: 0007-vmxnet3-use-ext1-field-to-indicate-encapsulated-pack.patch
Patch36: 0008-vmxnet3-update-to-version-7.patch
Patch37: 0001-vmxnet3-disable-overlay-offloads-if-UPT-device-does-.patch
Patch38: 0001-vmxnet3-do-not-reschedule-napi-for-rx-processing.patch
Patch39: 0002-vmxnet3-use-correct-intrConf-reference-when-using-ex.patch
Patch40: 0001-vmxnet3-move-rss-code-block-under-eop-descriptor.patch
Patch41: 0001-vmxnet3-use-gro-callback-when-UPT-is-enabled.patch

# Disable md5 algorithm for sctp if fips is enabled.
Patch42: 0001-disable-md5-algorithm-for-sctp-if-fips-is-enabled.patch

# Expose Photon kernel macros to identify kernel flavor and version
Patch43: 0001-kbuild-simplify-access-to-the-kernel-s-version.patch
Patch44: 0002-kbuild-replace-if-A-A-B-with-or-A-B.patch
Patch45: 0003-kbuild-Makefile-Introduce-macros-to-distinguish-Phot.patch
Patch46: 0004-linux-secure-Makefile-Add-kernel-flavor-info-to-the-.patch

# VMW: [55..60]
%ifarch x86_64
Patch55: x86-vmware-Use-Efficient-and-Correct-ALTERNATIVEs-fo.patch
Patch56: x86-vmware-Log-kmsg-dump-on-panic-510.patch
Patch57: 0001-x86-vmware-avoid-TSC-recalibration.patch

#Kernel lockdown
Patch58: 0001-kernel-lockdown-when-UEFI-secure-boot-enabled.patch
%endif

# SEV, TDX:
%ifarch x86_64
Patch61: 0001-x86-boot-Avoid-VE-during-boot-for-TDX-platforms.patch
%endif

#Secure:
Patch90: 0001-bpf-ext4-bonding-Fix-compilation-errors.patch
Patch91: 0001-NOWRITEEXEC-and-PAX-features-MPROTECT-EMUTRAMP.patch
Patch92: 0002-Added-PAX_RANDKSTACK.patch
Patch93: 0003-Added-rap_plugin.patch
Patch94: 0004-Fix-PAX-function-pointer-overwritten-for-tasklet-cal.patch

# CVE: [100..300]
Patch100: apparmor-fix-use-after-free-in-sk_peer_label.patch
# Fix CVE-2017-1000252
Patch101: KVM-Don-t-accept-obviously-wrong-gsi-values-via-KVM_.patch
# Fix for CVE-2019-12379
Patch102: consolemap-Fix-a-memory-leaking-bug-in-drivers-tty-v.patch

# Next 2 patches are about to be merged into stable
Patch103: 0001-mm-fix-panic-in-__alloc_pages.patch

# Fix for CVE-2021-4204
Patch104: 0002-bpf-Disallow-unprivileged-bpf-by-default.patch

# Fix for CVE-2022-3522
Patch106: 0001-mm_hugetlb_handle_pte_markers_in_page_faults.patch
Patch107: 0002-mm_hugetlb_fix_race_condition_of_uffd_missing_minor_handling.patch
Patch108: 0003-mm_hugetlb_use_hugetlb_pte_stable_in_migration_race_check.patch

# Fix for CVE-2024-50256
Patch109:  0001-netfilter-nf_reject_ipv6-fix-potential-crash-in-nf_s.patch

# Fix for CVE-2021-47489
Patch110:  0001-drm-amdgpu-Fix-even-more-out-of-bound-writes-from-de.patch

# Fix for CVE-2021-47265
Patch111:  0001-IB-mlx4-Use-port-iterator-and-validation-APIs.patch
Patch112:  0002-RDMA-Verify-port-when-creating-flow-rule.patch

# Fix for CVE-2024-26830
Patch113: 0001-i40e-Do-not-allow-untrusted-VF-to-remove-administrat.patch

# Fix for CVE-2022-0500
Patch114: 0001-bpf-Introduce-composable-reg-ret-and-arg-types.patch
Patch115: 0002-bpf-Replace-ARG_XXX_OR_NULL-with-ARG_XXX-PTR_MAYBE_N.patch
Patch116: 0003-bpf-Replace-RET_XXX_OR_NULL-with-RET_XXX-PTR_MAYBE_N.patch
Patch117: 0004-bpf-Extract-nullable-reg-type-conversion-into-a-help.patch
Patch118: 0005-bpf-Replace-PTR_TO_XXX_OR_NULL-with-PTR_TO_XXX-PTR_M.patch
Patch119: 0006-bpf-Introduce-MEM_RDONLY-flag.patch
Patch120: 0007-bpf-Make-per_cpu_ptr-return-rdonly-PTR_TO_MEM.patch
Patch121: 0008-bpf-Add-MEM_RDONLY-for-helper-args-that-are-pointers.patch

# Fix CVE-2024-35937
Patch123: 0001-wifi-cfg80211-check-A-MSDU-format-more-carefully.patch

# Fix CVE-2024-56658
Patch124: 0001-net-defer-final-struct-net-free-in-netns-dismantle.patch

# Fix CVE-2024-26718
Patch131: 0001-dm-crypt-dm-verity-disable-tasklets.patch

# Fix CVE-2024-26669
Patch132: 0001-net-sched-flower-Fix-chain-template-offload.patch

# Fix CVE-2024-26668
Patch133: 0001-netfilter-nft_limit-reject-configurations-that-cause.patch

#Fix for CVE-2023-0597
Patch137: 0001-x86-mm-Randomize-per-cpu-entry-area.patch
Patch138: 0002-x86-mm-Do-not-shuffle-CPU-entry-areas-without-KASLR.patch

#Fix CVE-2023-2176
Patch139: 0001-RDMA-core-Refactor-rdma_bind_addr.patch

#Fix CVE-2023-22995
Patch140: 0001-usb-dwc3-dwc3-qcom-Add-missing-platform_device_put-i.patch

#Fix CVE-2024-56604
Patch141: 0001-Bluetooth-RFCOMM-avoid-leaving-dangling-sk-pointer-i.patch

# Fix CVE-2024-26584
Patch146: 0001-tls-rx-simplify-async-wait.patch
Patch147: 0001-net-tls-factor-out-tls_-crypt_async_wait.patch
Patch148: 0001-net-tls-handle-backlogging-of-crypto-requests.patch

#Fix CVE-2024-49960
Patch150: 0001-ext4-fix-timer-use-after-free-on-failed-mount.patch

# Fix CVE-2024-26583
Patch151: 0001-tls-fix-race-between-async-notify-and-socket-close.patch

# Fix CVE-2024-26585
Patch152: 0001-tls-fix-race-between-tx-work-scheduling-and-socket-c.patch

# Fix CVE-2024-26589
Patch153: 0001-bpf-Reject-variable-offset-alu-on-PTR_TO_FLOW_KEYS.patch

# Fix CVE-2023-1192
Patch154: 0001-cifs-Fix-UAF-in-cifs_demultiplex_thread.patch

# Fix CVE-2024-26904
Patch155: 0001-btrfs-fix-data-race-at-btrfs_use_block_rsv.patch

# Fix CVE-2024-41073
Patch156: 0001-nvme-avoid-double-free-special-payload.patch

# Fix CVE-2024-42322
Patch157: 0001-ipvs-properly-dereference-pe-in-ip_vs_add_service.patch

# Fix CVE-2024-24855
Patch162: 0001-scsi-lpfc-Fix-a-possible-data-race-in-lpfc_unregiste.patch

# Fix CVE-2024-42080
Patch163: 0001-RDMA-restrack-Fix-potential-invalid-address-access.patch

# Fix CVE-2021-47188
Patch164: 0001-scsi-ufs-core-Improve-SCSI-abort-handling.patch

# Fix CVE-2024-44934
Patch165: 0001-net-bridge-mcast-wait-for-previous-gc-cycles-when-re.patch

# Fix CVE-2024-27415
Patch166: 0001-netfilter-bridge-confirm-multicast-packets-before-pa.patch

# Fix CVE-2024-27018
Patch167: 0001-netfilter-br_netfilter-skip-conntrack-input-hook-for.patch

# Fix CVE-2025-21690
Patch169: 0001-scsi-storvsc-Ratelimit-warning-logs-to-prevent-VM-de.patch

# Fix CVE-2023-52760
Patch170: 0001-gfs2-make-function-gfs2_make_fs_ro-to-void-type.patch
Patch171: 0002-gfs2-Fix-slab-use-after-free-in-gfs2_qd_dealloc.patch

# Fix CVE-2024-46834
Patch172: 0001-ethtool-Fail-number-of-channels-change-when-it-confl.patch
Patch173: 0002-ethtool-fail-closed-if-we-can-t-get-max-channel-used.patch

# Fix CVE-2024-41013
Patch174: 0001-xfs-No-need-for-inode-number-error-injection-in-__xf.patch
Patch175: 0002-xfs-don-t-walk-off-the-end-of-a-directory-data-block.patch

# Fix CVE-2024-41014
Patch176: 0001-xfs-add-bounds-checking-to-xlog_recover_process_data.patch

# Fix CVE-2024-46821
Patch177: 0001-drm-amd-pm-Fix-negative-array-index-read.patch

# Fix CVE-2024-47673
Patch178: 0001-wifi-iwlwifi-mvm-pause-TCM-when-the-firmware-is-stop.patch

# Fix CVE-2024-46848
Patch179: 0001-perf-x86-intel-Limit-the-period-on-Haswell.patch

# Fix CVE-2024-46802
Patch180: 0001-drm-amd-display-added-NULL-check-at-start-of-dc_vali.patch

# Fix CVE-2024-46816
Patch181: 0001-drm-amd-display-handle-invalid-connector-indices.patch
Patch182: 0001-drm-amd-display-Stop-amdgpu_dm-initialize-when-link-.patch

# Fix CVE-2024-50143
Patch183: 0001-udf-fix-uninit-value-use-in-udf_get_fileshortad.patch

# Fix CVE-2024-50154
Patch184: 0001-tcp-dccp-Don-t-use-timer_pending-in-reqsk_queue_unli.patch

# Fix CVE-2024-8805
Patch185: 0001-Bluetooth-hci_event-Align-BR-EDR-JUST_WORKS-paring-w.patch

# Fix CVE-2024-50014
Patch186: 0001-ext4-fix-access-to-uninitialised-lock-in-fc-replay-p.patch

# Fix CVE-2024-50018
Patch187: 0001-net-napi-Prevent-overflow-of-napi_defer_hard_irqs.patch

# Fix CVE-2024-50038
Patch188: 0001-netfilter-xtables-avoid-NFPROTO_UNSPEC-where-needed.patch
Patch189: 0002-netfilter-xtables-fix-typo-causing-some-targets-not-.patch

# Fixes CVE-2024-26661 and CVE-2024-26662
Patch190: 0001-drm-amd-display-Fix-panel_cntl-could-be-null-in-dcn2.patch
Patch191: 0002-drm-amd-display-Add-NULL-test-for-timing-generator-i.patch
Patch192: 0003-drm-amd-display-Fix-vs-typos.patch

# Fix CVE-2024-26656
Patch193: 0001-drm-amdgpu-fix-use-after-free-bug.patch

# Fix CVE-2024-26828
Patch194: 0001-cifs-fix-underflow-in-parse_server_interfaces.patch

# Fix CVE-2024-35817
Patch195: 0001-drm-amdgpu-amdgpu_ttm_gart_bind-set-gtt-bound-flag.patch

# Fix CVE-2024-27062
Patch196: 0001-nouveau-lock-the-client-object-tree.patch

# Fix CVE-2024-26915
Patch198: 0001-drm-amdgpu-Reset-IH-OVERFLOW_CLEAR-bit.patch

# Fix CVE-2024-26928
Patch199: smb-client-fix-potential-UAF-in-cifs_debug_files_pro.patch

# Fix CVE-2024-35863
Patch200: smb-client-fix-potential-UAF-in-is_valid_oplock_brea.patch

# Fix CVE-2024-35864
Patch201: smb-client-fix-potential-UAF-in-smb2_is_valid_lease_.patch

# Fix CVE-2024-35865
Patch202: smb-client-fix-potential-UAF-in-smb2_is_valid_oplock.patch

# Fix CVE-2024-35867
Patch203: smb-client-fix-potential-UAF-in-cifs_stats_proc_show.patch

# Fix CVE-2024-35868
Patch204: smb-client-fix-potential-UAF-in-cifs_stats_proc_writ.patch

# Crypto:
# Patch to add drbg_pr_ctr_aes256 test vectors to testmgr
Patch500: crypto-testmgr-Add-drbg_pr_ctr_aes256-test-vectors.patch
# Patch to call drbg and dh crypto tests from tcrypt
Patch501: tcrypt-disable-tests-that-are-not-enabled-in-photon.patch
Patch502: 0001-Initialize-jitterentropy-before-ecdh.patch
Patch503: 0002-FIPS-crypto-self-tests.patch
# Patch to remove urandom usage in rng module
Patch504: 0001-FIPS-crypto-rng-Jitterentropy-RNG-as-the-only-RND-source.patch
# Patch to remove urandom usage in drbg and ecc modules
Patch505: 0003-FIPS-crypto-drbg-Jitterentropy-RNG-as-the-only-RND.patch
#Patch to not make shash_no_setkey static
Patch506: 0001-fips-Continue-to-export-shash_no_setkey.patch
#Patch to introduce wrappers for random callback functions
Patch507: 0001-linux-crypto-Add-random-ready-callbacks-support.patch

%if 0%{?fips}
# FIPS canister usage patch
Patch508: 0001-FIPS-canister-binary-usage.patch
Patch509: 0001-scripts-kallsyms-Extra-kallsyms-parsing.patch
Patch510: 0001-Introduce_module_put_and_exit-function-to-address.patch
%else
%if 0%{?kat_build}
Patch510: 0001-Skip-rap-plugin-for-aesni-intel-modules.patch
Patch511: 0003-FIPS-broken-kattest.patch
%endif
%endif

%if 0%{?fips}
#retpoline
Patch512: 0001-retpoline-re-introduce-alternative-for-r11.patch
%endif

#Patches for vmci driver
Patch1521:       001-return-correct-error-code.patch
Patch1522:       002-switch-to-kvfree_rcu-API.patch
Patch1523:       003-print-unexpanded-names-of-ioctl.patch
Patch1524:       004-enforce-queuepair-max-size-for-IOCTL_VMCI_QUEUEPAIR_ALLOC.patch
Patch1531:       0001-whitespace-formatting-change-for-vmci-register-defines.patch
Patch1532:       0002-add-MMIO-access-to-registers.patch
Patch1533:       0003-detect-DMA-datagram-capability.patch
Patch1534:       0004-set-OS-page-size.patch
Patch1535:       0005-register-dummy-IRQ-handlers-for-DMA-datagrams.patch
Patch1536:       0006-allocate-send-receive-buffers-for-DMAdatagrams.patch
Patch1537:       0007-add-support-for-DMA-datagrams-send.patch
Patch1538:       0008-add-support-for-DMA-datagrams-receive.patch
Patch1539:       0009-fix-the-description-of-vmci_check_host_caps.patch
Patch1540:       0010-no-need-to-clear-memory-after-dma_alloc_coherent.patch
Patch1541:       0011-fix-error-handling-paths-in-vmci_guest_probe_device.patch
Patch1542:       0012-check-exclusive-vectors-when-freeing-interrupt1.patch
Patch1543:       0013-release-notification-bitmap-inn-error-path.patch
Patch1544:       0014-add-support-for-arm64.patch

BuildArch:      x86_64

BuildRequires:  bc
BuildRequires:  kbd
BuildRequires:  kmod-devel
BuildRequires:  glib-devel
BuildRequires:  xerces-c-devel
BuildRequires:  libdnet-devel
BuildRequires:  libmspack-devel
BuildRequires:  Linux-PAM-devel
BuildRequires:  openssl-devel
BuildRequires:  procps-ng-devel
BuildRequires:  bison

%if 0%{?fips}
BuildRequires: gdb
%endif

Requires: kmod
Requires: filesystem
Requires(pre): (coreutils or coreutils-selinux)
Requires(preun): (coreutils or coreutils-selinux)
Requires(post): (coreutils or coreutils-selinux)
Requires(postun): (coreutils or coreutils-selinux)
# Linux-secure handles user.pax.flags extended attribute
# User must have setfattr/getfattr tools available
Requires: attr

%description
Security hardened Linux kernel.
%if 0%{?fips}
This kernel is FIPS certified.
%endif

%package devel
Summary:       Kernel Dev
Group:         System Environment/Kernel
Requires:      python3 gawk
Requires:      %{name} = %{version}-%{release}
%description devel
The Linux package contains the Linux kernel dev files

%package docs
Summary:       Kernel docs
Group:         System Environment/Kernel
Requires:      python3
Requires:      %{name} = %{version}-%{release}
%description docs
The Linux package contains the Linux kernel doc files

%prep
# Using autosetup is not feasible
%setup -q -n linux-%{version}
%if 0%{?fips}
# Using autosetup is not feasible
%setup -q -T -D -b 16 -n linux-%{version}
%endif

%autopatch -p1 -m0 -M48

%ifarch x86_64
# VMW x86
%autopatch -p1 -m55 -M60
%endif

# SEV, TDX
%ifarch x86_64
%autopatch -p1 -m61 -M61
%endif

# LTP
%autopatch -p1 -m81 -M82

#Secure
%autopatch -p1 -m90 -M94

# CVE: [100..300]
%autopatch -p1 -m100 -M204

# crypto
%autopatch -p1 -m500 -M507

%if 0%{?fips}
%autopatch -p1 -m508 -M510
%else
%if 0%{?kat_build}
%autopatch -p1 -m510 -M511
%endif
%endif

%if 0%{?fips}
%autopatch -p1 -m512 -M512
%endif

# vmci
%patch1521 -p1
%patch1522 -p1
%patch1523 -p1
%patch1524 -p1
%patch1531 -p1
%patch1532 -p1
%patch1533 -p1
%patch1534 -p1
%patch1535 -p1
%patch1536 -p1
%patch1537 -p1
%patch1538 -p1
%patch1539 -p1
%patch1540 -p1
%patch1541 -p1
%patch1542 -p1
%patch1543 -p1
%patch1544 -p1

%make_build mrproper
cp %{SOURCE1} .config

%if 0%{?fips}
cp ../fips-canister-%{fips_canister_version}/fips_canister.o crypto/
cp ../fips-canister-%{fips_canister_version}/fips_canister_wrapper.c crypto/
cp %{SOURCE18} crypto/
# Patch canister wrapper
patch -p1 < %{SOURCE19}
patch -p1 < %{SOURCE20}
patch -p1 < %{SOURCE21}
patch -p1 < %{SOURCE24}
%endif

sed -i 's/CONFIG_LOCALVERSION="-secure"/CONFIG_LOCALVERSION="-%{release}-secure"/' .config

%if 0%{?kat_build}
sed -i '/CONFIG_CRYPTO_SELF_TEST=y/a CONFIG_CRYPTO_BROKEN_KAT=y' .config
%endif

%include %{SOURCE4}

%build
%make_build KBUILD_BUILD_VERSION="1-photon" \
    KBUILD_BUILD_HOST="photon" ARCH="x86_64"

%if 0%{?fips}
%include %{SOURCE9}
%endif

%install
install -vdm 755 %{buildroot}/%{_sysconfdir}
install -vdm 755 %{buildroot}/boot
install -vdm 755 %{buildroot}%{_docdir}/linux-%{uname_r}
install -vdm 755 %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}
%make_build INSTALL_MOD_PATH=%{buildroot} modules_install

install -vm 644 arch/x86/boot/bzImage %{buildroot}/boot/vmlinuz-%{uname_r}
install -vm 400 System.map %{buildroot}/boot/System.map-%{uname_r}
install -vm 644 .config %{buildroot}/boot/config-%{uname_r}
cp -r Documentation/* %{buildroot}%{_docdir}/linux-%{uname_r}

%if 0%{?__debug_package}
install -vdm 755 %{buildroot}%{_libdir}/debug/%{_modulesdir}
install -vm 644 vmlinux %{buildroot}%{_libdir}/debug/%{_modulesdir}/vmlinux-%{uname_r}
%endif

# Since we use compressed modules we cann't use load pinning,
# because .ko files will be loaded from the memory (LoadPin: obj=<unknown>)
cat > %{buildroot}/boot/linux-%{uname_r}.cfg << "EOF"
# GRUB Environment Block
photon_cmdline=init=/lib/systemd/systemd ro loglevel=3 quiet loadpin.enabled=0 audit=1 slub_debug=P page_poison=1 slab_nomerge pti=on
photon_linux=vmlinuz-%{uname_r}
photon_initrd=initrd.img-%{uname_r}
EOF

mkdir -p %{buildroot}%{_modulesdir}/dracut.conf.d/
cp -p %{SOURCE23} %{buildroot}%{_modulesdir}/dracut.conf.d/%{name}.conf

# cleanup dangling symlinks
rm -f %{buildroot}%{_modulesdir}/source \
      %{buildroot}%{_modulesdir}/build

# create /use/src/linux-headers-*/ content
find . -name Makefile* -o -name Kconfig* -o -name *.pl | xargs sh -c 'cp --parents "$@" %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}' copy
find arch/x86/include include scripts -type f | xargs sh -c 'cp --parents "$@" %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}' copy
find $(find arch/x86 -name include -o -name scripts -type d) -type f | xargs sh -c 'cp --parents "$@" %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}' copy
find arch/x86/include Module.symvers include scripts -type f | xargs sh -c 'cp --parents "$@" %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}' copy
%ifarch x86_64
# CONFIG_STACK_VALIDATION=y requires objtool to build external modules
install -vsm 755 tools/objtool/objtool %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}/tools/objtool/
install -vsm 755 tools/objtool/fixdep %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}/tools/objtool/
%endif

# copy .config manually to be where it's expected to be
cp .config %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}
# symling to the build folder
ln -sf %{_usrsrc}/linux-headers-%{uname_r} %{buildroot}%{_modulesdir}/build

%include %{SOURCE2}
%include %{SOURCE3}
%include %{SOURCE22}

%post
/sbin/depmod -a %{uname_r}
ln -sf linux-%{uname_r}.cfg /boot/photon.cfg

%files
%defattr(-,root,root)
/boot/System.map-%{uname_r}
/boot/config-%{uname_r}
/boot/vmlinuz-%{uname_r}
%config(noreplace) /boot/linux-%{uname_r}.cfg
/lib/modules/*
%exclude %{_modulesdir}/build
%exclude %{_usrsrc}

%config(noreplace) %{_modulesdir}/dracut.conf.d/%{name}.conf

%files docs
%defattr(-,root,root)
%{_defaultdocdir}/linux-%{uname_r}/*

%files devel
%defattr(-,root,root)
%{_modulesdir}/build
%{_usrsrc}/linux-headers-%{uname_r}

%changelog
* Fri Mar 28 2025 Ajay Kaher <ajay.kaher@broadcom.com> 5.10.235-2
- CVE-2024-35937, CVE-2024-56658
* Mon Mar 17 2025 Harinadh Dommaraju  <Harinadh.Dommaraju@broadcom.com> 5.10.235-1
- Update to version 5.10.235
* Mon Mar 03 2025 Kuntal Nayak <kuntal.nayak@broadcom.com> 5.10.234-9
- Fix CVE-2024-26718, CVE-2024-26668, CVE-2024-26669
* Fri Feb 28 2025 Ajay Kaher <ajay.kaher@broadcom.com> 5.10.234-8
- CVE-2021-47489, CVE-2021-47265, CVE-2024-26830
* Fri Feb 28 2025 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 5.10.234-7
- Fixes CVE-2025-21703 and CVE-2025-21690
* Tue Feb 18 2025 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 5.10.234-6
- Fix CVE-2024-35863, CVE-2024-35864, CVE-2024-35865,  CVE-2024-35867, CVE-2024-35868,
- CVE-2024-26928
* Thu Feb 13 2025 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 5.10.234-5
- Fixes CVE-2024-27415 and CVE-2024-27018
* Mon Feb 10 2025 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 5.10.234-4
- Fixes CVE-2024-8805
* Fri Feb 07 2025 Kuntal Nayak <kuntal.nayak@broadcom.com> 5.10.234-3
- Fix CVE-2024-26915, CVE-2024-26982, CVE-2024-27062, CVE-2024-35817
* Fri Feb 07 2025 Ankit Jain <ankit-aj.jain@broadcom.com> 5.10.234-2
- Fix for CVE-2024-26828, CVE-2024-26661, CVE-2024-26662, CVE-2024-26656
* Wed Feb 05 2025 Kuntal Nayak <kuntal.nayak@broadcom.com> 5.10.234-1
- Update to v5.10.234
* Tue Feb 04 2025 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 5.10.233-3
- Fixes CVE-2024-56604
* Tue Jan 21 2025 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 5.10.233-2
- Fixes CVE-2024-56631
* Tue Jan 21 2025 Ajay Kaher <ajay.kaher@broadcom.com> 5.10.233-1
- Update to version 5.10.233
* Mon Jan 20 2025 Keerthana K <keerthana.kalyanasundaram@broadcom.com> 5.10.232-3
- Fix CVE-2023-52760
* Thu Jan 16 2025 Keerthana K <keerthana.kalyanasundaram@broadcom.com> 5.10.232-2
- Fix CVE-2024-35966
* Fri Dec 20 2024 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 5.10.232-1
- Update to version 5.10.232
* Tue Nov 26 2024 Ajay Kaher <ajay.kaher@broadcom.com> 5.10.230-1
- Update to version 5.10.230
* Tue Nov 26 2024 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 5.10.229-5
- Fix CVE-2024-50154, CVE-2024-50055, CVE-2024-50143, CVE-2024-50014, CVE-2024-50018,
- CVE-2024-50038
* Tue Nov 26 2024 Srinidhi Rao <srinidhi.rao@broadcom.com> 5.10.229-4
- Fix CVE-2024-49960
* Mon Nov 18 2024 Keerthana K <keerthana.kalyanasundaram@broadcom.com> 5.10.229-3
- Fix CVE-2024-46848, CVE-2024-46802, CVE-2024-46816
* Mon Nov 11 2024 Ajay Kaher <ajay.kaher@broadcom.com> 5.10.229-2
- CVE-2024-50256, CVE-2024-50121
* Mon Oct 28 2024 Srinidhi Rao <srinidhi.rao@broadcom.com> 5.10.229-1
- Update to version 5.10.229
- Fix CVE-2024-49983 & CVE-2024-49967
* Fri Oct 25 2024 Srinidhi Rao <srinidhi.rao@broadcom.com> 5.10.226-6
- Fix CVE-2024-46821
* Mon Oct 21 2024 Kuntal Nayak <kuntal.nayak@broadcom.com> 5.10.226-5
- Fix CVE-2024-41013 and CVE-2024-41014
* Thu Oct 03 2024 Keerthana K <keerthana.kalyanasundaram@broadcom.com> 5.10.226-4
- Fix CVE-2024-46809, CVE-2024-46841, CVE-2024-46834
* Mon Sep 30 2024 Guruswamy Basavaiah <guruswamy.basavaih@broadcom.com> 5.10.226-3
- Fix CVE-2024-42322 and CVE-2024-38591
* Thu Sep 26 2024 Ankit Jain <ankit-aj.jain@broadcom.com> 5.10.226-2
- Fix for CVE-2024-44934, CVE-2024-44986, CVE-2024-38538
* Mon Sep 23 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 5.10.226-1
- Update to version 5.10.226
* Fri Sep 13 2024 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 5.10.225-2
- Fix CVE-2024-42080, CVE-2021-47188
* Wed Sep 11 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 5.10.225-1
- Update to version 5.10.225
* Tue Sep 10 2024 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 5.10.224-5
- Fix CVE-2024-24855 and CVE-2024-42246
* Sat Aug 31 2024 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 5.10.224-4
- Fix CVE-2024-38577, CVE-2024-42228
* Wed Aug 28 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 5.10.224-3
- Fix CVE-2024-43853, CVE-2024-43854
* Tue Aug 27 2024 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 5.10.224-2
- Fix CVE-2024-41073
* Tue Aug 20 2024 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 5.10.224-1
- Update to version 5.10.224
* Tue Aug 20 2024 Keerthana K <keerthana.kalyanasundaram@broadcom.com> 5.10.223-2
- Binary patch aesni_cpu_id value in canister
* Sun Aug 18 2024 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 5.10.223-1
- Update to version 5.10.223
* Tue Jul 23 2024 Harinadh Dommaraju <Harinadh.Dommaraju@broadcom.com> 5.10.222-2
- Fix CVE-2024-27397
* Fri Jul 19 2024 Ajay Kaher <ajay.kaher@broadcom.com> 5.10.222-1
- Update to version 5.10.222
- Fix for LTP fanotify22
* Tue Jul 09 2024 Ajay Kaher <ajay.kaher@broadcom.com> 5.10.219-3
- Fix for CVE-2022-48666
* Thu Jun 27 2024 Ashwin Dayanand Kamat <ashwin.kamat@broadcom.com> 5.10.219-2
- Fix for CVE-2024-36901
* Wed Jun 19 2024 Ashwin Dayanand Kamat <ashwin.kamat@broadcom.com> 5.10.219-1
- Update to version 5.10.219
* Tue May 07 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 5.10.216-1
- Update to version 5.10.216
* Fri Apr 12 2024 Ankit Jain <ankit-aj.jain@broadcom.com> 5.10.214-3
- Fix for CVE-2023-1192
* Wed Apr 03 2024 Kuntal Nayak <kuntal.nayak@broadcom.com> 5.10.214-2
- Patched CVE-2024-26643
* Wed Apr 03 2024 Keerthana K <keerthana.kalyanasundaram@broadcom.com> 5.10.214-1
- Update to version 5.10.214
- Fix CVE-2024-26642, CVE-2023-52620
* Mon Apr 01 2024 Ajay Kaher <ajay.kaher@broadcom.com> 5.10.212-4
- Fix CVE-2023-52585
* Mon Mar 25 2024 Srish Srinivasan <srish.srinivasan@broadcom.com> 5.10.212-3
- Patched CVE-2024-26583, CVE-2024-26585, and CVE-2024-26589
* Tue Mar 19 2024 Ashwin Dayanand Kamat <ashwin.kamat@broadcom.com> 5.10.212-2
- Fix for CVE-2023-52458/2023-52482
* Mon Mar 11 2024 Srish Srinivasan <srish.srinivasan@broadcom.com> 5.10.212-1
- Update to version 5.10.212, patched CVE-2024-26584
* Mon Mar 11 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com>  5.10.210-3
- Fixes CVE-2024-23307 and CVE-2024-22099
* Wed Feb 28 2024 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 5.10.210-2
- Fix CVE-2024-0841
* Mon Feb 26 2024 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 5.10.210-1
- Update to version 5.10.210
* Mon Feb 05 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 5.10.209-3
- Patch from the same series that resolved CVE-2024-0565
* Mon Feb 05 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 5.10.209-2
- Fix CVE-2024-1086
* Sun Jan 28 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 5.10.209-1
- Update to version 5.10.209
* Mon Jan 22 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 5.10.206-5
- Fixes CVE-2024-0565 and CVE-2023-6915
* Mon Jan 22 2024 Ajay Kaher <ajay.kaher@broadcom.com> 5.10.206-4
- Fix CVE-2024-0607
* Tue Jan 16 2024 Ajay Kaher <ajay.kaher@broadcom.com> 5.10.206-3
- Fix CVE-2024-0340
* Mon Jan 15 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 5.10.206-2
- Build with gcc-10.5.0
* Tue Jan 09 2024 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 5.10.206-1
- Update to version 5.10.206
* Mon Nov 27 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 5.10.201-1
- Update to version 5.10.201
* Wed Nov 15 2023 Kuntal Nayak <nkuntal@vmware.com> 5.10.200-2
- Kconfig to lockdown kernel in UEFI Secure Boot
* Thu Nov 09 2023 Ankit Jain <ankitja@vmware.com> 5.10.200-1
- Update to version 5.10.200
* Fri Oct 13 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 5.10.198-1
- Update to version 5.10.198
- Fix CVE-2023-4244
* Thu Oct 12 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 5.10.197-2
- Move kernel prep to %prep
* Tue Oct 03 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 5.10.197-1
- Update to version 5.10.197
- Undo commit 625bf86bf53eb7a8ee60fb9dc45b272b77e5ce1c as it breaks canister usage.
* Mon Oct 02 2023 Alexey Makhalov <amakhalov@vmware.com> 5.10.194-6
- LKCM: jitterentropy fix
* Sun Oct 01 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 5.10.194-5
- Fix for CVE-2023-42754
* Mon Sep 25 2023 Keerthana K <keerthanak@vmware.com> 5.10.194-4
- Fix CVE-2023-42756
* Mon Sep 25 2023 Keerthana K <keerthanak@vmware.com> 5.10.194-3
- Fix CVE-2023-42755
* Wed Sep 20 2023 Keerthana K <keerthanak@vmware.com> 5.10.194-2
- Fix CVE-2023-42753
* Tue Sep 12 2023 Roye Eshed <eshedr@vmware.com> 5.10.194-1
- Update to version 5.10.194
* Tue Sep 05 2023 Ankit Jain <ankitja@vmware.com> 5.10.190-4
- Fixes CVE-2023-22995
* Tue Sep 05 2023 Ankit Jain <ankitja@vmware.com> 5.10.190-3
- Fixes CVE-2023-2176
* Wed Aug 30 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com>  5.10.190-2
- Disable CONFIG_SCSI_DPT_I2O to fix CVE-2023-2007
* Tue Aug 29 2023 Ajay Kaher <akaher@vmware.com> 5.10.190-1
- Update to version 5.10.190
* Fri Aug 25 2023 Srish Srinivasan <ssrish@vmware.com> 5.10.188-2
- Patched CVE-2023-4147, CVE-2023-4128
* Tue Aug 01 2023 Kuntal Nayak <nkuntal@vmware.com> 5.10.188-1
- Update to version 5.10.188
* Fri Jul 28 2023 Ajay Kaher <akaher@vmware.com> 5.10.186-2
- Fix: SEV: Guest should not disabled CR4.MCE
* Fri Jul 14 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 5.10.186-1
- Update to version 5.10.186
* Mon Jul 10 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 5.10.183-2
- Fix for CVE-2023-0597
* Thu Jun 08 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 5.10.183-1
- Update to version 5.10.183, fix some CVEs
* Wed May 31 2023 Ankit Jain <ankitja@vmware.com> 5.10.180-1
- Update to version 5.10.180
* Wed May 24 2023 Alexey Makhalov <amakhalov@vmware.com> 5.10.175-6
- PaX: Support xattr 'em' file markings
* Tue Apr 25 2023 Keerthana K <keerthanak@vmware.com> 5.10.175-5
- Disable strcture randomization
* Wed Apr 12 2023 Shreenidhi Shedi <sshedi@vmware.com> 5.10.175-4
- Fix initrd generation logic
* Tue Apr 11 2023 Roye Eshed <eshedr@vmware.com> 5.10.175-3
- Fix for CVE-2022-39189
* Mon Apr 10 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 5.10.175-2
- update to latest ToT vmxnet3 driver pathes
* Tue Apr 04 2023 Roye Eshed <eshedr@vmware.com> 5.10.175-1
- Update to version 5.10.175
* Thu Mar 30 2023 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.168-2
- Expose Photon kernel macros to simplify building out-of-tree drivers.
* Thu Feb 16 2023 Srish Srinivasan <ssrish@vmware.com> 5.10.168-1
- Update to version 5.10.168
* Tue Feb 14 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 5.10.165-2
- Fix for CVE-2022-2196/CVE-2022-4379
* Wed Feb 08 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 5.10.165-1
- Update to version 5.10.165
* Fri Feb 03 2023 Alexey Makhalov <amakhalov@vmware.com> 5.10.162-2
- Implement performance over security option for RETBleed (pos=1)
* Tue Jan 17 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 5.10.162-1
- Update to version 5.10.162
* Thu Jan 12 2023 Alexey Makhalov <amakhalov@vmware.com> 5.10.159-3
- Introduce fips=2 and alg_request_report cmdline parameters
* Thu Jan 05 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 5.10.159-2
- update to latest ToT vmxnet3 driver
- Include patch "vmxnet3: correctly report csum_level for encapsulated packet"
* Mon Dec 19 2022 srinidhira0 <srinidhir@vmware.com> 5.10.159-1
- Update to version 5.10.159
* Wed Dec 14 2022 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 5.10.158-2
- update to latest ToT vmxnet3 driver
* Mon Dec 12 2022 Ankit Jain <ankitja@vmware.com> 5.10.158-1
- Update to version 5.10.158
* Tue Dec 06 2022 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 5.10.152-9
- Fix for CVE-2022-43945
* Mon Dec 05 2022 Srish Srinivasan <ssrish@vmware.com> 5.10.152-8
- Enable CONFIG_NET_CLS_FLOWER=m
* Wed Nov 30 2022 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 5.10.152-7
- Fix for CVE-2022-3564
* Mon Nov 28 2022 Ankit Jain <ankitja@vmware.com> 5.10.152-6
- Fix for CVE-2022-4139
* Mon Nov 28 2022 Ajay Kaher <akaher@vmware.com> 5.10.152-5
- Fix for CVE-2022-3522
* Mon Nov 14 2022 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 5.10.152-4
- vmxnet3 version 6, 7 patches
* Wed Nov 09 2022 Ajay Kaher <akaher@vmware.com> 5.10.152-3
- Fix for CVE-2022-3623
* Fri Nov 04 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.152-2
- Fix CVE-2022-3524 and CVE-2022-3567
* Mon Oct 31 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.152-1
- Update to version 5.10.152
* Mon Oct 17 2022 Sharan Turlapati <sturlapati@vmware.com> 5.10.142-3
- Fix for CVE-2022-2602
* Thu Oct 13 2022 Sharan Turlapati <sturlapati@vmware.com> 5.10.142-2
- Fixes for CVEs in the wifi subsystem
* Fri Sep 09 2022 srinidhira0 <srinidhir@vmware.com> 5.10.142-1
- Update to version 5.10.142
* Tue Aug 16 2022 srinidhira0 <srinidhir@vmware.com> 5.10.132-1
- Update to version 5.10.132
* Fri Aug 12 2022 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 5.10.118-10
- Backport fixes for CVE-2022-0500
* Mon Aug 08 2022 Shreenidhi Shedi <sshedi@vmware.com> 5.10.118-9
- Scriptlets fixes and improvements
* Fri Aug 05 2022 Him Kalyan Bordoloi <bordoloih@vmware.com> 5.10.118-8
- Fix for CVE-2022-2585, CVE-2022-2586 and CVE-2022-2588
* Fri Jul 15 2022 Keerthana K <keerthanak@vmware.com> 5.10.118-7
- Enable cgroup v1 stats
- .config: enable PERCPU_STATS
* Fri Jul 15 2022 Keerthana K <keerthanak@vmware.com> 5.10.118-6
- Avoid TSC recalibration
* Wed Jul 13 2022 Srinidhi Rao <srinidhir@vmware.com> 5.10.118-5
- Fix for CVE-2022-21505
* Tue Jul 12 2022 Keerthana K <keerthanak@vmware.com> 5.10.118-4
- Reduce FIPS canister memory footprint by disabling CONFIG_KALLSYMS_ALL
- Add only fips_canister-kallsyms to vmlinux instead of all symbols
* Fri Jul 01 2022 HarinadhD <hdommaraju@vmware.com> 5.10.118-3
- VMCI patches & configs
* Fri Jun 24 2022 Shreenidhi Shedi <sshedi@vmware.com> 5.10.118-2
- Fix debug_package macro usage while adding vmlinux to debuginfo rpm
* Mon Jun 13 2022 Sharan Turlapati <sturlapati@vmware.com> 5.10.118-1
- Update to version 5.10.118
* Wed Jun 01 2022 Ajay Kaher <akaher@vmware.com> 5.10.109-4
- Fix for CVE-2022-1966, CVE-2022-1972
* Tue May 24 2022 Sharan Turlapati <sturlapati@vmware.com> 5.10.109-3
- Fix for CVE-2022-21499
* Thu May 12 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 5.10.109-2
- Fix for CVE-2022-29582
* Fri Apr 29 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 5.10.109-1
- Update to version 5.10.109
* Mon Apr 18 2022 Alexey Makhalov <amakhalov@vmware.com> 5.10.103-5
- Add objtool to the -devel package.
* Tue Apr 05 2022 Alexey Makhalov <amakhalov@vmware.com> 5.10.103-4
- .config: enable zstd compression for squashfs.
- .config: enable crypto user api rng.
- .config: enable CONFIG_EXT2_FS_XATTR
* Mon Mar 21 2022 Ajay Kaher <akaher@vmware.com> 5.10.103-3
- Fix for CVE-2022-1016
* Mon Mar 14 2022 Bo Gan <ganb@vmware.com> 5.10.103-2
- Fix SEV and Hypercall alternative inst. patches
* Tue Mar 08 2022 srinidhira0 <srinidhir@vmware.com> 5.10.103-1
- Update to version 5.10.103
* Wed Feb 09 2022 Sharan Turlapati <sturlapati@vmware.com> 5.10.93-5
- Fix for CVE-2022-0435
* Sat Feb 05 2022 Sharan Turlapati <sturlapati@vmware.com> 5.10.93-4
- Fix for CVE-2022-0492
* Tue Jan 25 2022 Sharan Turlapati <sturlapati@vmware.com> 5.10.93-3
- Fix for CVE-2022-22942
* Tue Jan 25 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.93-2
- Fix CVE-2022-0330
* Fri Jan 21 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.93-1
- Update to version 5.10.93
* Sat Jan 08 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.83-6
- Fix CVE-2021-4155 and CVE-2021-4204
* Mon Dec 20 2021 Keerthana K <keerthanak@vmware.com> 5.10.83-5
- crypto_self_test and broken kattest module enhancements
* Fri Dec 17 2021 Alexey Makhalov <amakhalov@vmware.com> 5.10.83-4
- mm: fix percpu alloacion for memoryless nodes
- pvscsi: fix disk detection issue
* Fri Dec 17 2021 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 5.10.83-3
- Disable md5 algorithm for sctp if fips is enabled.
* Tue Dec 14 2021 Harinadh D <hdommaraju@vmware.com> 5.10.83-2
- remove lvm, tmem in add-drivers list
- lvm drivers are built as part of dm-mod
- tmem module is no longer exist
* Mon Dec 06 2021 srinidhira0 <srinidhir@vmware.com> 5.10.83-1
- Update to version 5.10.83
* Thu Nov 11 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 5.10.78-2
- compile with openssl 3.0.0
* Mon Nov 08 2021 Vikash Bansal <bvikas@vmware.com> 5.10.78-1
- Update to version 5.10.78
* Tue Oct 26 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.75-1
- Update to version 5.10.75
* Thu Sep 09 2021 Alexey Makhalov <amakhalov@vmware.com> 5.10.61-2
- .config enable CONFIG_MOUSE_PS2_VMMOUSE and CONFIG_INPUT_UINPUT
- Enable sta by default
* Fri Aug 27 2021 Ankit Jain <ankitja@vmware.com> 5.10.61-1
- Update to version 5.10.61
* Fri Jul 23 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 5.10.52-1
- Update to version 5.10.52
* Thu Jul 15 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 5.10.46-2
- Fix for CVE-2021-33909
* Mon Jun 28 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.46-1
- Update to version 5.10.46
* Thu Jun 24 2021 Loïc <4661917+HacKurx@users.noreply.github.com> 5.10.42-4
- EMUTRAMP: use the prefix X86_ for error codes
* Tue Jun 22 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.42-3
- Fix for CVE-2021-3609
* Thu Jun 10 2021 Keerthana K <keerthanak@vmware.com> 5.10.42-2
- Added script to check structure compatibility between fips_canister.o and vmlinux.
* Thu Jun 03 2021 Keerthana K <keerthanak@vmware.com> 5.10.42-1
- Update to version 5.10.42
- .config: Enable CONFIG_FANOTIFY_ACCESS_PERMISSIONS
* Mon May 17 2021 Ajay Kaher <akaher@vmware.com> 5.10.35-1
- Update to version 5.10.35
* Thu May 13 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.25-9
- Fix for CVE-2021-23133
* Tue May 11 2021 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.25-8
- Fix CVE-2020-26147, CVE-2020-24587, CVE-2020-24586, CVE-2020-24588,
- CVE-2020-26145, CVE-2020-26141
* Tue May 11 2021 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.25-7
- Fix CVE-2021-3489, CVE-2021-3490, CVE-2021-3491
* Thu Apr 29 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.25-6
- Remove buf_info from device accessible structures in vmxnet3
* Thu Apr 29 2021 Alexey Makhalov <amakhalov@vmware.com> 5.10.25-5
- Update canister binary.
- use jent by drbg and ecc.
- Enable hmac(sha224) self test and broket KAT test.
* Thu Apr 22 2021 Keerthana K <keerthanak@vmware.com> 5.10.25-4
- Update 0001-Skip-rap-plugin-for-aesni-intel-modules.patch for 5.10.25 kernel.
- Remove hmac(sha224) from broken kat test.
* Mon Apr 19 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.25-3
- Fix for CVE-2021-23133
* Thu Apr 15 2021 Srinidhi Rao <srinidhir@vmware.com> 5.10.25-2
- Fix for CVE-2021-29154
* Mon Mar 22 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 5.10.25-1
- Update to version 5.10.25
* Sun Mar 21 2021 Alexey Makhalov <amakhalov@vmware.com> 5.10.21-3
- Do not execute some tests twice
- Support future disablement of des3
- Do verbose build
- Canister update.
* Mon Mar 15 2021 Srinidhi Rao <srinidhir@vmware.com> 5.10.21-2
- Use jitterentropy rng instead of urandom in rng module.
* Mon Mar 08 2021 Vikash Bansal <bvikas@vmware.com> 5.10.21-1
- Update to version 5.10.21
* Mon Mar 01 2021 Alexey Makhalov <amakhalov@vmware.com> 5.10.4-8
- FIPS canister update
* Thu Feb 18 2021 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.4-7
- Fix /boot/photon.cfg symlink when /boot is a separate partition.
* Tue Feb 02 2021 Keerthana K <keerthanak@vmware.com> 5.10.4-6
- Added crypto_self_test and kattest module.
- These patches are applied when kat_build is enabled.
* Thu Jan 28 2021 Alexey Makhalov <amakhalov@vmware.com> 5.10.4-5
- Build with secure FIPS canister.
* Thu Jan 28 2021 Ankit Jain <ankitja@vmware.com> 5.10.4-4
- Enabled CONFIG_WIREGUARD
* Wed Jan 27 2021 Keerthana K <keerthanak@vmware.com> 5.10.4-3
- Fix rap_plugin code to generate rap_hashes when abs-finish is enabled.
* Wed Jan 13 2021 Keerthana K <keerthanak@vmware.com> 5.10.4-2
- Fix build failure.
* Wed Jan 06 2021 Keerthana K <keerthanak@vmware.com> 5.10.4-1
- Update to 5.10.4.
* Tue Nov 10 2020 Keerthana K <keerthanak@vmware.com> 5.9.0-4
- Fix CVE-2020-8694
* Fri Nov 06 2020 Keerthana K <keerthanak@vmware.com> 5.9.0-3
- Fix CVE-2020-25704
* Tue Nov 03 2020 Srinidhi Rao <srinidhir@vmware.com> 5.9.0-2
- Remove the support of fipsify and hmacgen
* Thu Oct 22 2020 Keerthana K <keerthanak@vmware.com> 5.9.0-1
- Update to 5.9.0
* Wed Oct 14 2020 Keerthana K <keerthanak@vmware.com> 5.9.0-rc7.1
- Update to 5.9.0-rc7
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 4.19.127-4
- openssl 1.1.1
* Mon Jul 27 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.127-3
- Fix CVE-2020-14331
* Tue Jun 23 2020 Tapas Kundu <tkundu@vmware.com> 4.19.127-2
- Require python3
* Tue Jun 23 2020 Keerthana K <keerthanak@vmware.com> 4.19.127-1
- Update to version 4.19.127
* Fri Jun 05 2020 Ankit Jain <ankitja@vmware.com> 4.19.112-8
- Enabled CONFIG_BINFMT_MISC
* Tue Jun 02 2020 Vikash Bansal <bvikas@vmware.com> 4.19.112-7
- Add patch to fix CVE-2019-18885
* Fri May 29 2020 Shreenidhi Shedi <sshedi@vmware.com> 4.19.112-6
- Keep modules of running kernel till next boot
* Wed May 06 2020 Siddharth Chandrasekaran <csiddharth@vmware.com> 4.19.112-5
- Add patch to fix CVE-2020-10711
* Mon May 04 2020 Alexey Makhalov <amakhalov@vmware.com> 4.19.112-4
- Updated pax_rap patch to support gcc-8.4.0
* Wed Apr 29 2020 Keerthana K <keerthanak@vmware.com> 4.19.112-3
- Photon-checksum-generator version update to 1.1.
* Wed Apr 15 2020 Vikash Bansal <bvikas@vmware.com> 4.19.112-2
- HMAC-SHA256 digest of hmac_generator module moved to hmacgen package
* Wed Apr 08 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.112-1
- Update to version 4.19.112
* Tue Mar 31 2020 Vikash Bansal <bvikas@vmware.com> 4.19.104-2
- hmac generation of crypto modules and initrd generation changes if fips=1
* Wed Mar 25 2020 Vikash Bansal <bvikas@vmware.com> 4.19.104-1
- Update to version 4.19.104
* Mon Mar 16 2020 Keerthana K <keerthanak@vmware.com> 4.19.97-6
- Adding Enhances depedency to hmacgen.
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
* Thu Jan 16 2020 Srinidhi Rao <srinidhir@vmware.com> 4.19.87-4
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
* Tue Oct 15 2019 Ajay Kaher <akaher@vmware.com> 4.19.79-1
- Update to version 4.19.79
- Fix CVE-2019-17133
* Thu Oct 10 2019 Harinadh D <hdommaraju@vmware.com> 4.19.76-2
- Adding lvm and dm-mod modules to support root as lvm
* Wed Oct 02 2019 Ajay Kaher <akaher@vmware.com> 4.19.76-1
- Update to version 4.19.76
* Mon Sep 30 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.72-1
- Update to version 4.19.72
* Thu Sep 05 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.69-2
- Avoid oldconfig which leads to potential build hang
* Fri Aug 30 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.69-1
- Update to version 4.19.69
* Tue Aug 06 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.65-1
- Update to version 4.19.65
- Fix CVE-2019-1125 (SWAPGS)
* Tue Jul 30 2019 Keerthana K <keerthanak@vmware.com> 4.19.52-3
- Fix postun script.
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
