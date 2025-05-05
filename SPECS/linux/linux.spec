%global security_hardening none
%ifarch x86_64
%define arch x86_64
%define archdir x86

# Set this flag to 0 to build without canister
%global fips 1

# If kat_build is enabled, canister is not used.
%if 0%{?kat_build}
%global fips 0
%endif

%endif

%ifarch aarch64
%define arch arm64
%define archdir arm64
%global fips 0
%endif

Summary:        Kernel
Name:           linux
Version:        5.10.236
Release:        2%{?acvp_build:.acvp}%{?kat_build:.kat}%{?dist}
License:        GPLv2
URL:            http://www.kernel.org/
Group:          System Environment/Kernel
Vendor:         VMware, Inc.
Distribution:   Photon

%define uname_r %{version}-%{release}
%define _modulesdir /lib/modules/%{uname_r}

Source0:        http://www.kernel.org/pub/linux/kernel/v5.x/linux-%{version}.tar.xz
%define sha512 linux=835f10a8d3efb52094ef92aaba403a471143eabbb5da59ec2e26bea66840952bcc7f3f20056f1e1cf1277dcdb33b59e56c70a7aea05861aa9edf62b1508d0840
Source1:        config_%{_arch}
Source2:        initramfs.trigger

%ifarch x86_64
%define ena_version 2.4.0
Source3:    https://github.com/amzn/amzn-drivers/archive/ena_linux_%{ena_version}.tar.gz
%define sha512 ena_linux=e14b706d06444dcc832d73150a08bbdc0fc53b291d2fd233aef62d8f989f529b4aabc7865526fe27a895d43d5f8ba5993752a920601be8a1d3ed9ea973e9c6ef

%define sgx_version 1.8
Source5:    https://github.com/intel/SGXDataCenterAttestationPrimitives/archive/DCAP_%{sgx_version}.tar.gz
%define sha512 DCAP=79d0b4aba102559bed9baf9fe20917e9781a22d742fa52b49b2c1a00c452a452796e6ce1a92bad80d6e6fc92ad71fa72ee02c1b65a59bddbb562aaaad4b2d8b2
%endif

# contains pre, postun, filetriggerun tasks
Source6:        scriptlets.inc
Source7:        check_for_config_applicability.inc

%ifarch x86_64
%define i40e_version 2.22.18
Source10:       https://sourceforge.net/projects/e1000/files/i40e%20stable/%{i40e_version}/i40e-%{i40e_version}.tar.gz
%define sha512 i40e=042fd064528cb807894dc1f211dcb34ff28b319aea48fc6dede928c93ef4bbbb109bdfc903c27bae98b2a41ba01b7b1dffc3acac100610e3c6e95427162a26ac

%define iavf_version 4.8.2
Source11:       https://sourceforge.net/projects/e1000/files/iavf%20stable/%{iavf_version}/iavf-%{iavf_version}.tar.gz
%define sha512 iavf=5406b86e61f6528adfd7bc3a5f330cec8bb3b4d6c67395961cc6ab78ec3bd325c3a8655b8f42bf56fb47c62a85fb7dbb0c1aa3ecb6fa069b21acb682f6f578cf

Source12:       ena-Use-new-API-interface-after-napi_hash_del-.patch

%define ice_version 1.11.14
Source13:       https://sourceforge.net/projects/e1000/files/ice%20stable/%{ice_version}/ice-%{ice_version}.tar.gz
%define sha512 ice=a2a6a498e553d41e4e6959a19cdb74f0ceff3a7dbcbf302818ad514fdc18e3d3b515242c88d55ef8a00c9d16925f0cd8579cb41b3b1c27ea6716ccd7e70fd847
%endif

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
Source23:       %{name}-dracut-%{_arch}.conf

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
# Revert crypto api workqueue
Patch9: 0001-Revert-crypto-api-Use-work-queue-in-crypto_destroy_i.patch

# ttyXRUSB support
Patch10: usb-acm-exclude-exar-usb-serial-ports-nxt.patch
#HyperV patches
Patch11: vmbus-Don-t-spam-the-logs-with-unknown-GUIDs.patch

# TODO: Is CONFIG_HYPERV_VSOCKETS the same?
#Patchx: 0014-hv_sock-introduce-Hyper-V-Sockets.patch
Patch12: fork-add-sysctl-to-disallow-unprivileged-CLONE_NEWUSER-by.patch
# Out-of-tree patches from AppArmor:
Patch13: apparmor-patch-to-provide-compatibility-with-v2.x-ne.patch
Patch14: apparmor-af_unix-mediation.patch
# floppy:
Patch15: 0001-floppy-lower-printk-message-priority.patch

# Disable md5 algorithm for sctp if fips is enabled.
Patch16: 0001-disable-md5-algorithm-for-sctp-if-fips-is-enabled.patch

# VMware-specific patch to enable turbostat to work on ESXi
Patch17: 0001-tools-power-turbostat-Skip-some-CPUID-checks-if-runn.patch
# Backports of upstream patches to add Ice Lake support to turbostat
Patch18: 0002-tools-power-turbostat-Remove-Package-C6-Retention-on.patch
Patch19: 0003-tools-power-turbostat-Fix-DRAM-Energy-Unit-on-SKX.patch

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
Patch40: 0002-vmxnet3-use-correct-intrConf-reference-when-using-ex.patch
Patch41: 0001-vmxnet3-move-rss-code-block-under-eop-descriptor.patch
Patch42: 0001-vmxnet3-use-gro-callback-when-UPT-is-enabled.patch

# Expose Photon kernel macros to identify kernel flavor and version
Patch43: 0001-kbuild-simplify-access-to-the-kernel-s-version.patch
Patch44: 0002-kbuild-replace-if-A-A-B-with-or-A-B.patch
Patch45: 0003-kbuild-Makefile-Introduce-macros-to-distinguish-Phot.patch
Patch46: 0004-linux-Makefile-Add-kernel-flavor-info-to-the-generat.patch

%ifarch x86_64
# VMW: [55..65]
Patch55: x86-vmware-Use-Efficient-and-Correct-ALTERNATIVEs-fo-510.patch
Patch56: x86-vmware-Log-kmsg-dump-on-panic-510.patch
Patch57: x86-vmware-Fix-steal-time-clock-under-SEV.patch
Patch58: 0001-x86-vmware-avoid-TSC-recalibration.patch

#Kernel lockdown
Patch59: 0001-kernel-lockdown-when-UEFI-secure-boot-enabled.patch
%endif

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

#Fix for CVE-2024-50125
Patch122: 0001-Bluetooth-call-sock_hold-earlier-in-sco_conn_del.patch
Patch123: 0002-Bluetooth-SCO-Fix-UAF-on-sco_sock_timeout.patch

# Fix CVE-2025-21863
Patch124: 0001-io_uring-prevent-opcode-speculation.patch

# Fix CVE-2024-35937
Patch125: 0001-wifi-cfg80211-check-A-MSDU-format-more-carefully.patch

# Fix CVE-2024-56658
Patch126: 0001-net-defer-final-struct-net-free-in-netns-dismantle.patch

# Fix CVE-2024-26739
Patch130: 0001-net-sched-act_mirred-don-t-override-retval-if-we-alr.patch

# Fix CVE-2024-26718
Patch131: 0001-dm-crypt-dm-verity-disable-tasklets.patch

# Fix CVE-2024-26669
Patch132: 0001-net-sched-flower-Fix-chain-template-offload.patch

# Fix CVE-2024-26668
Patch133: 0001-netfilter-nft_limit-reject-configurations-that-cause.patch

#Fix for CVE-2023-0597
Patch136: 0001-x86-mm-Randomize-per-cpu-entry-area.patch
Patch137: 0002-x86-mm-Do-not-shuffle-CPU-entry-areas-without-KASLR.patch

#Fix CVE-2023-2176
Patch138: 0001-RDMA-core-Refactor-rdma_bind_addr.patch

#Fix CVE-2023-22995
Patch139: 0001-usb-dwc3-dwc3-qcom-Add-missing-platform_device_put-i.patch

#Fix CVE-2024-56604
Patch140: 0001-Bluetooth-RFCOMM-avoid-leaving-dangling-sk-pointer-i.patch

# Fix CVE-2024-26584
Patch143: 0001-tls-rx-simplify-async-wait.patch
Patch144: 0001-net-tls-factor-out-tls_-crypt_async_wait.patch
Patch145: 0001-net-tls-handle-backlogging-of-crypto-requests.patch

# Fix CVE-2023-1192
Patch146: 0001-cifs-Fix-UAF-in-cifs_demultiplex_thread.patch
# Fix CVE-2024-26583
Patch147: 0001-tls-fix-race-between-async-notify-and-socket-close.patch

# Fix CVE-2024-26585
Patch148: 0001-tls-fix-race-between-tx-work-scheduling-and-socket-c.patch

# Fix CVE-2024-26589
Patch149: 0001-bpf-Reject-variable-offset-alu-on-PTR_TO_FLOW_KEYS.patch

# Fix CVE-2024-41073
Patch150: 0001-nvme-avoid-double-free-special-payload.patch

#Fix CVE-2024-49960
Patch151: 0001-ext4-fix-timer-use-after-free-on-failed-mount.patch

# Fix CVE-2024-41071
Patch155: 0001-wifi-mac80211-Avoid-address-calculations-via-out-of-.patch

# Fix CVE-2024-24855
Patch157: 0001-scsi-lpfc-Fix-a-possible-data-race-in-lpfc_unregiste.patch

# Fix CVE-2024-42080
Patch158: 0001-RDMA-restrack-Fix-potential-invalid-address-access.patch

# Fix CVE-2021-47188
Patch159: 0001-scsi-ufs-core-Improve-SCSI-abort-handling.patch

# Fix CVE-2024-44934
Patch160: 0001-net-bridge-mcast-wait-for-previous-gc-cycles-when-re.patch

# Fix CVE-2025-21690
Patch162: 0001-scsi-storvsc-Ratelimit-warning-logs-to-prevent-VM-de.patch

# Fix CVE-2024-42322
Patch164: 0001-ipvs-properly-dereference-pe-in-ip_vs_add_service.patch

# Fix CVE-2024-27415
Patch165: 0001-netfilter-bridge-confirm-multicast-packets-before-pa.patch

# Fix CVE-2024-27018
Patch166: 0001-netfilter-br_netfilter-skip-conntrack-input-hook-for.patch

# Fix CVE-2023-52760
Patch167: 0001-gfs2-make-function-gfs2_make_fs_ro-to-void-type.patch
Patch168: 0002-gfs2-Fix-slab-use-after-free-in-gfs2_qd_dealloc.patch

# Fix CVE-2024-46834
Patch169: 0001-ethtool-Fail-number-of-channels-change-when-it-confl.patch
Patch170: 0002-ethtool-fail-closed-if-we-can-t-get-max-channel-used.patch

# Fix CVE-2024-41013
Patch171: 0001-xfs-No-need-for-inode-number-error-injection-in-__xf.patch
Patch172: 0002-xfs-don-t-walk-off-the-end-of-a-directory-data-block.patch

# Fix CVE-2024-41014
Patch173: 0001-xfs-add-bounds-checking-to-xlog_recover_process_data.patch

# Fix CVE-2024-47673
Patch175: 0001-wifi-iwlwifi-mvm-pause-TCM-when-the-firmware-is-stop.patch

# Fix CVE-2024-46848
Patch176: 0001-perf-x86-intel-Limit-the-period-on-Haswell.patch

# Fix CVE-2024-46802
Patch177: 0001-drm-amd-display-added-NULL-check-at-start-of-dc_vali.patch

# Fix CVE-2024-46816
Patch178: 0001-drm-amd-display-handle-invalid-connector-indices.patch
Patch179: 0001-drm-amd-display-Stop-amdgpu_dm-initialize-when-link-.patch

# Fix CVE-2024-50143
Patch180: 0001-udf-fix-uninit-value-use-in-udf_get_fileshortad.patch

# Fix CVE-2024-50154
Patch181: 0001-tcp-dccp-Don-t-use-timer_pending-in-reqsk_queue_unli.patch

# Fix CVE-2024-50014
Patch183: 0001-ext4-fix-access-to-uninitialised-lock-in-fc-replay-p.patch

# Fix CVE-2024-50018
Patch184: 0001-net-napi-Prevent-overflow-of-napi_defer_hard_irqs.patch

# Fix CVE-2024-50038
Patch185: 0001-netfilter-xtables-avoid-NFPROTO_UNSPEC-where-needed.patch
Patch186: 0002-netfilter-xtables-fix-typo-causing-some-targets-not-.patch

# Fixes CVE-2024-26661 and CVE-2024-26662
Patch187: 0001-drm-amd-display-Fix-panel_cntl-could-be-null-in-dcn2.patch
Patch188: 0002-drm-amd-display-Add-NULL-test-for-timing-generator-i.patch
Patch189: 0003-drm-amd-display-Fix-vs-typos.patch

# Fix CVE-2024-26656
Patch190: 0001-drm-amdgpu-fix-use-after-free-bug.patch

# Fix CVE-2024-26828
Patch191: 0001-cifs-fix-underflow-in-parse_server_interfaces.patch

# Fix CVE-2024-35817
Patch192: 0001-drm-amdgpu-amdgpu_ttm_gart_bind-set-gtt-bound-flag.patch

# Fix CVE-2024-27062
Patch193: 0001-nouveau-lock-the-client-object-tree.patch

# Fix CVE-2024-26915
Patch195: 0001-drm-amdgpu-Reset-IH-OVERFLOW_CLEAR-bit.patch

# Fix CVE-2024-26928
Patch196: smb-client-fix-potential-UAF-in-cifs_debug_files_pro.patch

# Fix CVE-2024-35863
Patch197: smb-client-fix-potential-UAF-in-is_valid_oplock_brea.patch

# Fix CVE-2024-35864
Patch198: smb-client-fix-potential-UAF-in-smb2_is_valid_lease_.patch

# Fix CVE-2024-35865
Patch199: smb-client-fix-potential-UAF-in-smb2_is_valid_oplock.patch

# Fix CVE-2024-35867
Patch200: smb-client-fix-potential-UAF-in-cifs_stats_proc_show.patch

# Fix CVE-2024-35868
Patch201: smb-client-fix-potential-UAF-in-cifs_stats_proc_writ.patch

# Fix CVE-2024-35878
Patch202: 0001-of-Update-of_device_get_modalias.patch
Patch203: 0002-of-module-prevent-NULL-pointer-dereference-in-vsnpri.patch

# Fix CVE-2021-47200
Patch204: 0001-drm-prime-Fix-use-after-free-in-mmap-with-drm_gem_tt.patch

# Fix CVE-2021-47101
Patch205: 0001-net-asix-fix-uninit-value-bugs.patch
Patch206: 0002-asix-fix-uninit-value-in-asix_mdio_read.patch

# Fix CVE-2023-52531
Patch207: 0001-wifi-iwlwifi-mvm-Fix-a-memory-corruption-issue.patch

# Fix CVE-2024-49991
Patch208: 0002-drm-amdkfd-amdkfd_free_gtt_mem-clear-the-correct-poi.patch

# Fix CVE-2024-50067
Patch209: 0003-uprobes-encapsulate-preparation-of-uprobe-args-buffe.patch
Patch210: 0004-uprobe-avoid-out-of-bounds-memory-access-of-fetching.patch

# Fix CVE-2023-52621
Patch211: 0005-bpf-Allow-RCU-protected-lookups-to-happen-from-bh-co.patch
Patch212: 0006-bpf-Check-rcu_read_lock_trace_held-before-calling-bp.patch

# Fix CVE-2024-35839
Patch213: 0001-netfilter-nfnetlink_log-use-proper-helper-for-fetchi.patch
Patch214: 0002-netfilter-nf_queue-remove-excess-nf_bridge-variable.patch
Patch215: 0003-netfilter-propagate-net-to-nf_bridge_get_physindev.patch
Patch216: 0004-netfilter-bridge-replace-physindev-with-physinif-in-.patch

%ifarch aarch64
# Rpi of_configfs patches
Patch301: 0001-OF-DT-Overlay-configfs-interface.patch
Patch302: 0002-of-configfs-Use-of_overlay_fdt_apply-API-call.patch
Patch303: 0003-of-overlay-Correct-symbol-path-fixups.patch

# Rpi fan driver
Patch304: 0001-Add-rpi-poe-fan-driver.patch
%endif

# Allow PCI resets to be disabled from vfio_pci module
Patch305: 0001-drivers-vfio-pci-Add-kernel-parameter-to-allow-disab.patch
# Add PCI quirk to allow multiple devices under the same virtual PCI bridge
# to be put into separate IOMMU groups on ESXi.
Patch306: 0001-Add-PCI-quirk-for-VMware-PCIe-Root-Port.patch
# Enable CONFIG_DEBUG_INFO_BTF=y
Patch307: 0001-tools-resolve_btfids-Warn-when-having-multiple-IDs-f.patch

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
Patch510: 0003-FIPS-broken-kattest.patch
%endif

%endif

%if 0%{?fips}
#retpoline
Patch511: 0001-retpoline-re-introduce-alternative-for-r11.patch
%endif

%if 0%{?acvp_build:1} && 0%{?fips}
#ACVP test harness patches.
#Need to be applied on top of FIPS canister usage patch to avoid HUNK failure
Patch512:       0001-crypto-AF_ALG-add-sign-verify-API.patch
Patch513:       0002-crypto-AF_ALG-add-setpubkey-setsockopt-call.patch
Patch514:       0003-crypto-AF_ALG-add-asymmetric-cipher.patch
Patch515:       0004-crypto-AF_ALG-add-DH-keygen-ssgen-API.patch
Patch516:       0005-crypto-AF_ALG-add-DH-param-ECDH-curve-setsockopt.patch
Patch517:       0006-crypto-AF_ALG-eliminate-code-duplication.patch
Patch518:       0007-crypto-AF_ALG-add-KPP-support.patch
Patch519:       0008-crypto-AF_ALG-add-ECC-support.patch
Patch520:       0009-kernels-net-Export-sock_getsockopt.patch
Patch521:       0010-DRBG-Fix-issues-with-DRBG.patch
%endif

%ifarch x86_64
# SEV on VMware:
Patch600: 0079-x86-sev-es-Disable-BIOS-ACPI-RSDP-probing-if-SEV-ES-.patch
Patch601: 0080-x86-boot-Enable-vmw-serial-port-via-Super-I-O.patch
Patch602: 0081-x86-sev-es-Disable-use-of-WP-via-PAT-for-__sme_early.patch
Patch603: x86-sev-es-load-idt-before-entering-long-mode-to-han-510.patch
Patch604: x86-swiotlb-Adjust-SWIOTLB-bounce-buffer-size-for-SE.patch
Patch605: x86-sev-es-Do-not-unroll-string-IO-for-SEV-ES-guests.patch
Patch606: 0001-x86-boot-Avoid-VE-during-boot-for-TDX-platforms.patch

#Patches for i40e driver
Patch1500: i40e-xdp-remove-XDP_QUERY_PROG-and-XDP_QUERY_PROG_HW-XDP-.patch
Patch1501: 0001-Add-support-for-gettimex64-interface.patch
Patch1502: i40e-don-t-install-auxiliary-module-on.patch
Patch1503: i40e-Make-i40e-driver-honor-default-and-user-defined.patch

#Patches for iavf driver
Patch1512: no-aux-symvers.patch

#Patches for ice driver
Patch1513: ice-don-t-install-auxiliary-module-on-modul.patch
Patch1514: ice-fix-redefinition-of-eth_hw_addr_set.patch
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

BuildRequires:  bc
BuildRequires:  kmod-devel
BuildRequires:  glib-devel
BuildRequires:  elfutils-devel
BuildRequires:  openssl-devel
BuildRequires:  procps-ng-devel
BuildRequires:  audit-devel
BuildRequires:  elfutils-libelf-devel
BuildRequires:  binutils-devel
BuildRequires:  xz-devel
BuildRequires:  slang-devel
BuildRequires:  python3-devel
BuildRequires:  bison
BuildRequires:  dwarves-devel

%ifarch x86_64
BuildRequires:  pciutils-devel
BuildRequires:  libcap-devel
%endif

%if 0%{?fips}
BuildRequires:  gdb
%endif

Requires: filesystem
Requires: kmod
Requires(pre): (coreutils or coreutils-selinux)
Requires(preun): (coreutils or coreutils-selinux)
Requires(post): (coreutils or coreutils-selinux)
Requires(postun): (coreutils or coreutils-selinux)

%description
The Linux package contains the Linux kernel.
%if 0%{?fips}
This kernel is FIPS certified.
%endif

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

%package drivers-sound
Summary:        Kernel Sound modules
Group:          System Environment/Kernel
Requires:       %{name} = %{version}-%{release}
%description drivers-sound
The Linux package contains the Linux kernel sound support

%package docs
Summary:        Kernel docs
Group:          System Environment/Kernel
Requires:       python3
%description docs
The Linux package contains the Linux kernel doc files

%ifarch x86_64
%package drivers-intel-sgx
Summary:    Intel SGX driver
Group:      System Environment/Kernel
Requires:   %{name} = %{version}-%{release}
Requires(post): /usr/sbin/groupadd
%description drivers-intel-sgx
This Linux package contains Intel SGX kernel module.

%package oprofile
Summary:        Kernel driver for oprofile, a statistical profiler for Linux systems
Group:          System Environment/Kernel
Requires:       %{name} = %{version}-%{release}
%description oprofile
Kernel driver for oprofile, a statistical profiler for Linux systems
%endif

%package tools
Summary:        This package contains the 'perf' performance analysis tools for Linux kernel
Group:          System/Tools
Requires:       (%{name} = %{version} or linux-esx = %{version} or linux-aws = %{version})
Requires:       audit elfutils-libelf binutils-libs
Requires:       xz-libs slang
Requires:       python3 traceevent-plugins
%ifarch x86_64
Requires:       pciutils
%endif
Obsoletes:      linux-aws-tools <= 4.19.52-1
Provides:       linux-aws-tools
%description tools
This package contains kernel tools like perf, turbostat and cpupower.

%package python3-perf
Summary:        Python bindings for applications that will manipulate perf events.
Group:          Development/Libraries
Requires:       linux-tools = %{version}-%{release}
Requires:       python3

%description python3-perf
This package provides a module that permits applications written in the
Python programming language to use the interface to manipulate perf events.

%package -n bpftool
Summary:    Inspection and simple manipulation of eBPF programs and maps
Group:      Development/Libraries
Requires:   linux-tools = %{version}-%{release}

%description -n bpftool
This package contains the bpftool, which allows inspection and simple
manipulation of eBPF programs and maps.

%prep
#TODO: remove rcN after 5.9 goes out of rc
# Using autosetup is not feasible
%setup -q -n linux-%{version}
%ifarch x86_64
# Using autosetup is not feasible
%setup -q -T -D -b 3 -n linux-%{version}
# Using autosetup is not feasible
%setup -q -T -D -b 5 -n linux-%{version}
# Using autosetup is not feasible
%setup -q -T -D -b 10 -n linux-%{version}
# Using autosetup is not feasible
%setup -q -T -D -b 11 -n linux-%{version}
# Using autosetup is not feasible
%setup -q -T -D -b 13 -n linux-%{version}
%endif

%if 0%{?fips}
# Using autosetup is not feasible
%setup -q -T -D -b 16 -n linux-%{version}
%endif

%autopatch -p1 -m0 -M48

%ifarch x86_64
# VMW x86
%autopatch -p1 -m55 -M65
%endif

# LTP
%autopatch -p1 -m81 -M82

# CVE: [100..300]
%autopatch -p1 -m100 -M300

%ifarch aarch64
# Rpi of_configfs patches
# Rpi fan driver
%autopatch -p1 -m301 -M304
%endif

# Allow PCI resets to be disabled from vfio_pci module
%autopatch -p1 -m305 -M306
%autopatch -p1 -m307 -M307

# crypto
%autopatch -p1 -m500 -M507

%if 0%{?fips}
%autopatch -p1 -m508 -M510
%else
%if 0%{?kat_build}
%patch510 -p1
%endif
%endif

%if 0%{?fips}
%autopatch -p1 -m511 -M511
%endif

%if 0%{?acvp_build:1} && 0%{?fips}
#ACVP test harness patches.
#Need to be applied on top of FIPS canister usage patch to avoid HUNK failure
%autopatch -p1 -m512 -M521
%endif

%ifarch x86_64
# SEV on VMware
%autopatch -p1 -m600 -M606

#Patches for i40e driver
pushd ../i40e-%{i40e_version}
%autopatch -p1 -m1500 -M1503
popd

#Patches for iavf driver
pushd ../iavf-%{iavf_version}
%patch1512 -p1
popd

#Patches for ice driver
pushd ../ice-%{ice_version}
%patch1513 -p1
%patch1514 -p1
popd

%endif

# vmci
%autopatch -p1 -m1521 -M1524
%autopatch -p1 -m1531 -M1544

%make_build mrproper
cp %{SOURCE1} .config
%if 0%{?acvp_build:1} && 0%{?fips}
#ACVP test harness changes in kernel configs.
sed -i 's/# CONFIG_CRYPTO_USER is not set/CONFIG_CRYPTO_USER=y/' .config
sed -i 's/# CONFIG_CRYPTO_DH is not set/CONFIG_CRYPTO_DH=y/' .config
sed -i 's/CONFIG_CRYPTO_USER_API=m/CONFIG_CRYPTO_USER_API=y/' .config
sed -i 's/CONFIG_CRYPTO_USER_API_HASH=m/CONFIG_CRYPTO_USER_API_HASH=y/' .config
sed -i 's/CONFIG_CRYPTO_USER_API_SKCIPHER=m/CONFIG_CRYPTO_USER_API_SKCIPHER=y/' .config
sed -i 's/# CONFIG_CRYPTO_USER_API_RNG is not set/CONFIG_CRYPTO_USER_API_RNG=y/' .config
sed -i 's/# CONFIG_CRYPTO_USER_API_RNG_CAVP is not set/CONFIG_CRYPTO_USER_API_RNG_CAVP=y/' .config
sed -i '/CONFIG_CRYPTO_USER_API_ENABLE_OBSOLETE/ a # CONFIG_CRYPTO_STATS is not set' .config
sed -i '/CONFIG_CRYPTO_STATS/ a CONFIG_CRYPTO_USER_API_AKCIPHER=y' .config
sed -i '/CONFIG_CRYPTO_USER_API_AKCIPHER/ a CONFIG_CRYPTO_USER_API_KPP=y' .config
sed -i '/CONFIG_CRYPTO_USER_API_KPP=y/ a CONFIG_CRYPTO_USER_API_ECC=y' .config
%endif

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

sed -i 's/CONFIG_LOCALVERSION=""/CONFIG_LOCALVERSION="-%{release}"/' .config

%if 0%{?kat_build}
sed -i '/CONFIG_CRYPTO_SELF_TEST=y/a CONFIG_CRYPTO_BROKEN_KAT=y' .config
%endif

%include %{SOURCE7}

# Set/add CONFIG_CROSS_COMPILE= if needed
if [ %{_host} != %{_build} ]; then
grep -q CONFIG_CROSS_COMPILE= .config && sed -i '/^CONFIG_CROSS_COMPILE=/c\CONFIG_CROSS_COMPILE="%{_host}-"' .config || \
  echo 'CONFIG_CROSS_COMPILE="%{_host}-"' >> .config
fi

%build
%make_build KBUILD_BUILD_VERSION="1-photon" KBUILD_BUILD_HOST="photon" ARCH=%{arch}

%if 0%{?fips}
%include %{SOURCE9}
%endif

%ifarch aarch64
ARCH_FLAGS="EXTRA_CFLAGS=-Wno-error=format-overflow"
%endif

%make_build ARCH=%{arch} -C tools perf PYTHON=python3 $ARCH_FLAGS
# verify perf has no dependency on libunwind
tools/perf/perf -vv | grep libunwind | grep OFF
tools/perf/perf -vv | grep dwarf | grep on

%ifarch x86_64
# build turbostat and cpupower
%make_build ARCH=%{arch} -C tools turbostat cpupower PYTHON=python3

# build ENA module
bldroot="${PWD}"
pushd ../amzn-drivers-ena_linux_%{ena_version}/kernel/linux/ena
patch -p4 < %{SOURCE12}
%make_build -C ${bldroot} M="${PWD}" modules
popd

# build Intel SGX module
pushd ../SGXDataCenterAttestationPrimitives-DCAP_%{sgx_version}/driver/linux
%make_build KDIR=${bldroot} ARCH=%{arch}
popd

# build i40e module
pushd ../i40e-%{i40e_version}
%make_build -C src KSRC=${bldroot} clean
%make_build -C src KSRC=${bldroot}
popd

# build iavf module
pushd ../iavf-%{iavf_version}
%make_build -C src KSRC=${bldroot} clean
%make_build -C src KSRC=${bldroot}
popd

# build ice module
pushd ../ice-%{ice_version}
%make_build -C src KSRC=${bldroot} clean
%make_build -C src KSRC=${bldroot}
popd
%endif

%install
install -vdm 755 %{buildroot}%{_sysconfdir}
install -vdm 755 %{buildroot}/boot
install -vdm 755 %{buildroot}%{_docdir}/linux-%{uname_r}
install -vdm 755 %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}
install -vdm 755 %{buildroot}%{_libdir}/debug/%{_modulesdir}
%make_build ARCH=%{arch} INSTALL_MOD_PATH=%{buildroot} modules_install

%ifarch x86_64
# install ENA module
bldroot="${PWD}"
pushd ../amzn-drivers-ena_linux_%{ena_version}/kernel/linux/ena
%make_build -C ${bldroot} M="${PWD}" INSTALL_MOD_PATH=%{buildroot} modules_install
popd

# install Intel SGX module
pushd ../SGXDataCenterAttestationPrimitives-DCAP_%{sgx_version}/driver/linux
mkdir -p %{buildroot}%{_sysconfdir}/udev/rules.d
install -vm 644 10-sgx.rules %{buildroot}/%{_sysconfdir}/udev/rules.d
mkdir -p %{buildroot}%{_modulesdir}/extra
install -vm 644 intel_sgx.ko %{buildroot}%{_modulesdir}/extra/
popd

# The auxiliary.ko kernel module is a common dependency for iavf, i40e
# and ice drivers.  Install it only once, along with the iavf driver
# and re-use it in the ice and i40e drivers.

# install i40e module
pushd ../i40e-%{i40e_version}
%make_build -C src KSRC=${bldroot} INSTALL_MOD_PATH=%{buildroot} \
    INSTALL_MOD_DIR=extra MANDIR=%{_mandir} modules_install_no_aux mandocs_install
popd

# install iavf module (with aux module)
pushd ../iavf-%{iavf_version}
%make_build -C src KSRC=$bldroot INSTALL_MOD_PATH=%{buildroot} INSTALL_MOD_DIR=extra \
    INSTALL_AUX_DIR=extra/auxiliary MANDIR=%{_mandir} modules_install \
    mandocs_install
install -Dvm 644 src/linux/auxiliary_bus.h \
       %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}/include/linux/auxiliary_bus.h
popd

# install ice module
pushd ../ice-%{ice_version}
%make_build -C src KSRC=${bldroot} MANDIR=%{_mandir} INSTALL_MOD_PATH=%{buildroot} \
            mandocs_install
%make_build -C src KSRC=${bldroot} INSTALL_MOD_PATH=%{buildroot} \
     INSTALL_MOD_DIR=extra modules_install_no_aux
popd

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

%ifarch aarch64
install -vm 644 arch/arm64/boot/Image %{buildroot}/boot/vmlinuz-%{uname_r}
%endif

# Restrict the permission on System.map-X file
install -vm 400 System.map %{buildroot}/boot/System.map-%{uname_r}
install -vm 644 .config %{buildroot}/boot/config-%{uname_r}
cp -r Documentation/* %{buildroot}%{_docdir}/linux-%{uname_r}

%if 0%{?__debug_package}
install -vm 644 vmlinux %{buildroot}%{_libdir}/debug/%{_modulesdir}/vmlinux-%{uname_r}
# `perf test vmlinux` needs it
ln -s vmlinux-%{uname_r} %{buildroot}%{_libdir}/debug/%{_modulesdir}/vmlinux
%endif

cat > %{buildroot}/boot/linux-%{uname_r}.cfg << "EOF"
# GRUB Environment Block
photon_cmdline=init=/lib/systemd/systemd ro loglevel=3 quiet
photon_linux=vmlinuz-%{uname_r}
photon_initrd=initrd.img-%{uname_r}
EOF

# Cleanup dangling symlinks
rm -rf %{buildroot}%{_modulesdir}/source \
       %{buildroot}%{_modulesdir}/build

find . -name Makefile* -o -name Kconfig* -o -name *.pl | xargs sh -c 'cp --parents "$@" %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}' copy
find arch/%{archdir}/include include scripts -type f | xargs sh -c 'cp --parents "$@" %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}' copy
find $(find arch/%{archdir} -name include -o -name scripts -type d) -type f | xargs sh -c 'cp --parents "$@" %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}' copy
find arch/%{archdir}/include Module.symvers include scripts -type f | xargs sh -c 'cp --parents "$@" %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}' copy
%ifarch x86_64
# CONFIG_STACK_VALIDATION=y requires objtool to build external modules
install -vsm 755 tools/objtool/objtool %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}/tools/objtool/
install -vsm 755 tools/objtool/fixdep %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}/tools/objtool/
%endif

cp .config %{buildroot}%{_usrsrc}/linux-headers-%{uname_r} # copy .config manually to be where it's expected to be
ln -sf "%{_usrsrc}/linux-headers-%{uname_r}" "%{buildroot}%{_modulesdir}/build"
find %{buildroot}/lib/modules -name '*.ko' -print0 | xargs -0 chmod u+x

%ifarch aarch64
ARCH_FLAGS="EXTRA_CFLAGS=-Wno-error=format-overflow"
%endif

%make_build -C tools ARCH=%{arch} DESTDIR=%{buildroot} \
     prefix=%{_prefix} perf_install PYTHON=python3 $ARCH_FLAGS

%make_build -C tools/perf ARCH=%{arch} DESTDIR=%{buildroot} \
     prefix=%{_prefix} PYTHON=python3 install-python_ext

%ifarch x86_64
%make_build -C tools ARCH=%{arch} DESTDIR=%{buildroot} \
     prefix=%{_prefix} mandir=%{_mandir} turbostat_install cpupower_install PYTHON=python3
%endif

make install %{?_smp_mflags} -C tools/bpf/bpftool prefix=%{_prefix} DESTDIR=%{buildroot}

mkdir -p %{buildroot}%{_modulesdir}/dracut.conf.d/
cp -p %{SOURCE23} %{buildroot}%{_modulesdir}/dracut.conf.d/%{name}.conf

%include %{SOURCE2}
%include %{SOURCE6}
%include %{SOURCE22}

%post
/sbin/depmod -a %{uname_r}
ln -sf linux-%{uname_r}.cfg /boot/photon.cfg

%post drivers-gpu
/sbin/depmod -a %{uname_r}

%post drivers-sound
/sbin/depmod -a %{uname_r}

%ifarch x86_64
%post drivers-intel-sgx
/sbin/depmod -a %{uname_r}
getent group sgx_prv >/dev/null || groupadd -r sgx_prv

%post oprofile
/sbin/depmod -a %{uname_r}
%endif

%files
%defattr(-,root,root)
/boot/System.map-%{uname_r}
/boot/config-%{uname_r}
/boot/vmlinuz-%{uname_r}
%config(noreplace) /boot/linux-%{uname_r}.cfg
%defattr(0644,root,root)
%{_modulesdir}/*
%exclude %{_modulesdir}/build
%exclude %{_modulesdir}/kernel/drivers/gpu
%exclude %{_modulesdir}/kernel/sound
%ifarch aarch64
%exclude %{_modulesdir}/kernel/drivers/staging/vc04_services/bcm2835-audio
%endif
%ifarch x86_64
%exclude %{_modulesdir}/kernel/arch/x86/oprofile/
%exclude %{_modulesdir}/extra/intel_sgx.ko.xz
# iavf.conf is used to just blacklist the deprecated i40evf
# and create alias of i40evf to iavf.
# By default iavf is used for VF driver.
# This file creates conflict with other flavour of linux
# thus excluding this file from packaging
%exclude %{_sysconfdir}/modprobe.d/iavf.conf
# ICE driver firmware files are packaged in linux-firmware
%exclude /lib/firmware/updates/intel/ice
%endif

%config(noreplace) %{_modulesdir}/dracut.conf.d/%{name}.conf

%files docs
%defattr(-,root,root)
%{_docdir}/linux-%{uname_r}/*
# For out-of-tree Intel i40e driver.
%ifarch x86_64
%{_mandir}/*
%endif

%files devel
%defattr(-,root,root)
%{_modulesdir}/build
%{_usrsrc}/linux-headers-%{uname_r}

%files drivers-gpu
%defattr(-,root,root)
%exclude %{_modulesdir}/kernel/drivers/gpu/drm/cirrus/
%{_modulesdir}/kernel/drivers/gpu

%files drivers-sound
%defattr(-,root,root)
%{_modulesdir}/kernel/sound

%ifarch aarch64
%{_modulesdir}/kernel/drivers/staging/vc04_services/bcm2835-audio
%endif

%ifarch x86_64
%files drivers-intel-sgx
%defattr(-,root,root)
%{_modulesdir}/extra/intel_sgx.ko.xz
%config(noreplace) %{_sysconfdir}/udev/rules.d/10-sgx.rules

%files oprofile
%defattr(-,root,root)
%{_modulesdir}/kernel/arch/x86/oprofile/
%endif

%files tools
%defattr(-,root,root)

%ifarch x86_64
%exclude %{_lib64}/traceevent
%endif

%ifarch aarch64
%exclude %{_libdir}/traceevent
%endif

%{_bindir}
%{_sysconfdir}/bash_completion.d/perf
%{_libexecdir}/perf-core
%{_datadir}/perf-core
%{_docdir}/perf-tip
%{_libdir}/perf/examples/bpf/*
%{_libdir}/perf/include/bpf/*

%ifarch x86_64
%{_includedir}/cpufreq.h
%{_includedir}/cpuidle.h
%{_lib64dir}/libcpupower.so*
%{_docdir}/packages/cpupower
%{_datadir}/bash-completion/completions/cpupower
%config(noreplace) %{_sysconfdir}/cpufreq-bench.conf
%{_sbindir}/cpufreq-bench
%{_datadir}/locale/*/LC_MESSAGES/cpupower.mo
%endif

%files python3-perf
%defattr(-,root,root)
%{python3_sitelib}/*

%files -n bpftool
%defattr(-,root,root)
%{_sbindir}/bpftool
%{_datadir}/bash-completion/completions/bpftool

%changelog
* Tue Apr 29 2025 Kuntal Nayak <kuntal.nayak@broadcom.com> 5.10.236-2
- Fix CVE-2024-26739
* Mon Apr 28 2025 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 5.10.236-1
- Update to version 5.10.236
* Mon Apr 14 2025 Kuntal Nayak <kuntal.nayak@broadcom.com> 5.10.235-6
- Fix CVE-2024-35839
* Mon Apr 14 2025 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 5.10.235-5
- Fix CVE-2023-52531, CVE-2024-49991, CVE-2024-50067, CVE-2023-52621
* Thu Apr 10 2025 Ajay Kaher <ajay.kaher@broadcom.com> 5.10.235-4
- Fix CVE-2025-21863
* Thu Apr 03 2025 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 5.10.235-3
- Fix CVE-2021-47200 and CVE-2021-47101
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
- CVE-2024-35878, CVE-2024-26928
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
- Fix CVE-2024-50125, CVE-2024-50256, CVE-2024-50121
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
- Fix CVE-2024-42080 and CVE-2021-47188
* Wed Sep 11 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 5.10.225-1
- Update to version 5.10.225
* Tue Sep 10 2024 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 5.10.224-7
- Fix CVE-2024-24855 and CVE-2024-42246
* Tue Sep 10 2024 Kuntal Nayak <kuntal.nayak@broadcom.com> 5.10.224-6
- Fix CVE-2024-41071
* Wed Sep 04 2024 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 5.10.224-5
- Fix CVE-2024-38577, CVE-2024-42228
* Wed Sep 04 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 5.10.224-4
- Fix CVE-2024-43853, CVE-2024-43854
* Tue Sep 03 2024 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 5.10.224-3
- Enable CONFIG_ARM64_ERRATUM_3194386.
* Tue Aug 27 2024 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 5.10.224-2
- Fix CVE-2024-41073
* Tue Aug 20 2024 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 5.10.224-1
- Update to version 5.10.224
* Tue Aug 20 2024 Keerthana K <keerthana.kalyanasundaram@broadcom.com> 5.10.223-2
- Binary patch aesni_cpu_id value in canister
* Sun Aug 18 2024 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 5.10.223-1
- Update to version 5.10.223
* Tue Aug 13 2024 Ajay Kaher <ajay.kaher@broadcom.com> 5.10.222-3
- Fix .config for aarch64
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
* Thu May 16 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 5.10.216-2
- Remove linux-rt from requires of linux-tools
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
- Fix for CVE-2023-52447/2023-52458/2023-52482
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
* Mon Sep 11 2023 Roye Eshed <eshedr@vmware.com> 5.10.194-1
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
* Fri Jul 21 2023 Ajay Kaher <akaher@vmware.com> 5.10.186-2
- Fix: SEV: Guest should not disabled CR4.MCE
* Fri Jul 14 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 5.10.186-1
- Update to version 5.10.186
* Mon Jul 10 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 5.10.183-2
- Fix for CVE-2023-0597
* Thu Jun 08 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 5.10.183-1
- Update to version 5.10.183, fix some CVEs
* Wed May 17 2023 Ankit Jain <ankitja@vmware.com> 5.10.180-1
- Update to version 5.10.180
* Wed May 17 2023 Srish Srinivasan <ssrish@vmware.com> 5.10.175-8
- Added support for ACVP build
* Mon May 08 2023 Srish Srinivasan <ssrish@vmware.com> 5.10.175-7
- Enable CONFIG_DEBUG_INFO_BTF=y
* Wed Apr 26 2023 Shreenidhi Shedi <sshedi@vmware.com> 5.10.175-6
- Fix aarch64 initrd driver list
* Sun Apr 16 2023 Shreenidhi Shedi <sshedi@vmware.com> 5.10.175-5
- Fix initrd generation logic
* Wed Apr 12 2023 Ajay Kaher <akaher@vmware.com> 5.10.175-4
- perf: remove libunwind dependency
* Tue Apr 11 2023 Roye Eshed <eshedr@vmware.com> 5.10.175-3
- Fix for CVE-2022-39189
* Mon Apr 10 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 5.10.175-2
- update to latest ToT vmxnet3 driver pathes
* Tue Apr 04 2023 Roye Eshed <eshedr@vmware.com> 5.10.175-1
- Update to version 5.10.175
* Tue Apr 04 2023 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.168-7
- Fix IRQ affinity of i40e driver
* Thu Mar 30 2023 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.168-6
- Expose Photon kernel macros to simplify building out-of-tree drivers.
* Fri Mar 17 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 5.10.168-5
- Update intel ethernet drivers to:
- i40e: 2.22.18
- iavf: 4.8.2
- ice: 1.11.14
* Tue Feb 28 2023 Ankit Jain <ankitja@vmware.com> 5.10.168-4
- Exclude iavf.conf
* Mon Feb 27 2023 Ajay Kaher <akaher@vmware.com> 5.10.168-3
- exclude man dir from linux-tools
* Fri Feb 17 2023 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.168-2
- Enable turbostat to work in the guest on VMware hypervisor.
- Add support for Intel Ice Lake server CPUs to turbostat.
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
* Thu Jan 12 2023 Alexey Makhalov <amakhalov@vmware.com> 5.10.159-4
- Introduce fips=2 and alg_request_report cmdline parameters
* Thu Jan 05 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 5.10.159-3
- update to latest ToT vmxnet3 driver
- Include patch "vmxnet3: correctly report csum_level for encapsulated packet"
* Thu Dec 22 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 5.10.159-2
- Enable CONFIG_PCI_PF_STUB
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
* Mon Oct 31 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.142-5
- Replace rpm macro 'name' with 'linux' to be consistent with other flavors.
* Mon Oct 17 2022 Sharan Turlapati <sturlapati@vmware.com> 5.10.142-4
- Fix for CVE-2022-2602
* Wed Oct 12 2022 Sharan Turlapati <sturlapati@vmware.com> 5.10.142-3
- Fixes for CVEs in the wifi subsystem
* Wed Sep 14 2022 Shreenidhi Shedi <sshedi@vmware.com> 5.10.142-2
- Add bpftool subpackage
* Fri Sep 09 2022 srinidhira0 <srinidhir@vmware.com> 5.10.142-1
- Update to version 5.10.142
* Tue Aug 16 2022 srinidhira0 <srinidhir@vmware.com> 5.10.132-1
- Update to version 5.10.132
* Fri Aug 12 2022 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 5.10.118-14
- Backport fixes for CVE-2022-0500
* Mon Aug 08 2022 Shreenidhi Shedi <sshedi@vmware.com> 5.10.118-13
- Scriptlets fixes and improvements
* Fri Aug 05 2022 Him Kalyan Bordoloi <bordoloih@vmware.com> 5.10.118-12
- Fix for CVE-2022-2585, CVE-2022-2586 and CVE-2022-2588
* Mon Jul 18 2022 Keerthana K <keerthanak@vmware.com> 5.10.118-11
- Update iavf driver to v4.4.2
- Update ice driver to v1.8.3
* Fri Jul 15 2022 Keerthana K <keerthanak@vmware.com> 5.10.118-10
- .config: enable CONFIG_NET_ACT_SIMP
* Fri Jul 15 2022 Keerthana K <keerthanak@vmware.com> 5.10.118-9
- .config: enable CONFIG_X86_CPU_RESCTRL
* Fri Jul 15 2022 Keerthana K <keerthanak@vmware.com> 5.10.118-8
- Enable cgroup v1 stats
- .config: enable PERCPU_STATS
* Fri Jul 15 2022 Keerthana K <keerthanak@vmware.com> 5.10.118-7
- Avoid TSC recalibration
* Wed Jul 13 2022 Srinidhi Rao <srinidhir@vmware.com> 5.10.118-6
- Fix for CVE-2022-21505
* Tue Jul 12 2022 Keerthana K <keerthanak@vmware.com> 5.10.118-5
- Reduce FIPS canister memory footprint by disabling CONFIG_KALLSYMS_ALL
- Add only fips_canister-kallsyms to vmlinux instead of all symbols
* Fri Jul 01 2022 Harinadh D <hdommaraju@vmware.com> 5.10.118-4
- VMCI patches & configs
* Fri Jun 24 2022 Shreenidhi Shedi <sshedi@vmware.com> 5.10.118-3
- Fix debug_package macro usage while adding vmlinux to debuginfo rpm
* Wed Jun 15 2022 Brennan Lamoreaux <blamoreaux@vmware.com> 5.10.118-2
- Enabling config_livepatch and related, including ftrace
* Mon Jun 13 2022 Sharan Turlapati <sturlapati@vmware.com> 5.10.118-1
- Update to version 5.10.118
* Wed Jun 01 2022 Ajay Kaher <akaher@vmware.com> 5.10.109-4
- Fix for CVE-2022-1966, CVE-2022-1972
* Mon May 23 2022 Sharan Turlapati <sturlapati@vmware.com> 5.10.109-3
- Fix for CVE-2022-21499
* Thu May 12 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 5.10.109-2
- Fix for CVE-2022-29582
* Fri Apr 29 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 5.10.109-1
- Update to version 5.10.109
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
* Sat Jan 08 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.83-7
- Fix CVE-2021-4155 and CVE-2021-4204
* Mon Dec 20 2021 Keerthana K <keerthanak@vmware.com> 5.10.83-6
- Enable crypto related configs in aarch64 similar to x86_64
- crypto_self_test and broken kattest module enhancements
* Fri Dec 17 2021 Alexey Makhalov <amakhalov@vmware.com> 5.10.83-5
- mm: fix percpu alloacion for memoryless nodes
- pvscsi: fix disk detection issue
* Fri Dec 17 2021 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 5.10.83-4
- Disable md5 algorithm for sctp if fips is enabled.
* Tue Dec 14 2021 Harinadh D <hdommaraju@vmware.com> 5.10.83-3
- remove tmem,lvm in add-drivers list
- lvm drivers are built as part of dm-mod
- tmem module is no longer exist
* Thu Dec 09 2021 Prashant S Chauhan <psinghchauha@vmware.com> 5.10.83-2
- Bump up to compile with python 3.10
* Mon Dec 06 2021 srinidhira0 <srinidhir@vmware.com> 5.10.83-1
- Update to version 5.10.83
* Mon Nov 29 2021 Srinidhi Rao <srinidhir@vmware.com> 5.10.78-5
- Enable eBPF Net Packet filter support.
* Thu Nov 18 2021 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.78-4
- Add PCI quirk to allow multiple devices under the same virtual
- PCI bridge to be put into separate IOMMU groups.
* Wed Nov 17 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.78-3
- Allow PCI resets disablement from vfio_pci
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
* Wed Aug 18 2021 Keerthana K <keerthanak@vmware.com> 5.10.52-2
- Update ice driver to v1.6.4
- Update i40e driver to v2.15.9
- Update iavf driver to v4.2.7
* Fri Jul 23 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 5.10.52-1
- Update to version 5.10.52
* Thu Jul 15 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 5.10.46-2
- Fix for CVE-2021-33909
* Mon Jun 28 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.46-1
- Update to version 5.10.46
* Tue Jun 22 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.42-3
- Fix for CVE-2021-3609
* Thu Jun 10 2021 Keerthana K <keerthanak@vmware.com> 5.10.42-2
- Added script to check structure compatibility between fips_canister.o and vmlinux.
* Thu Jun 03 2021 Keerthana K <keerthanak@vmware.com> 5.10.42-1
- Update to version 5.10.42
- Remove XR usb driver support
- .config: Enable CONFIG_FANOTIFY_ACCESS_PERMISSIONS
* Wed Jun 02 2021 Keerthana K <keerthanak@vmware.com> 5.10.35-4
- Fix for CVE-2021-3573
* Thu May 20 2021 Ajay Kaher <akaher@vmware.com> 5.10.35-3
- Add Rpi fan driver
* Thu May 20 2021 Ajay Kaher <akaher@vmware.com> 5.10.35-2
- Fix for CVE-2021-3564
* Mon May 17 2021 Ajay Kaher <akaher@vmware.com> 5.10.35-1
- Update to version 5.10.35
* Thu May 13 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.25-10
- Fix for CVE-2021-23133
* Tue May 11 2021 Ankit Jain <ankitja@vmware.com> 5.10.25-9
- .config: Enable MLX5_INFINIBAND
* Tue May 11 2021 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.25-8
- Fix CVE-2020-26147, CVE-2020-24587, CVE-2020-24586, CVE-2020-24588,
- CVE-2020-26145, CVE-2020-26141
* Tue May 11 2021 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.25-7
- Fix CVE-2021-3489, CVE-2021-3490, CVE-2021-3491
* Tue May 04 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.25-6
- Remove buf_info from device accessible structures in vmxnet3
* Thu Apr 29 2021 Alexey Makhalov <amakhalov@vmware.com> 5.10.25-5
- Update canister binary.
- use jent by drbg and ecc.
- Enable hmac(sha224) self test and broket KAT test.
* Thu Apr 22 2021 Keerthana K <keerthanak@vmware.com> 5.10.25-4
- Remove hmac(sha224) test from broken kat test.
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
* Mon Mar 01 2021 Alexey Makhalov <amakhalov@vmware.com> 5.10.4-17
- FIPS canister update
* Fri Feb 19 2021 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.4-16
- Fix /boot/photon.cfg symlink when /boot is a separate partition.
* Fri Feb 19 2021 Ajay Kaher <akaher@vmware.com> 5.10.4-15
- Added SEV-ES improvement patches
* Thu Feb 18 2021 Ajay Kaher <akaher@vmware.com> 5.10.4-14
- Enable CONFIG_WDAT_WDT
* Thu Feb 18 2021 Ajay Kaher <akaher@vmware.com> 5.10.4-13
- lower the loglevel for floppy driver
* Thu Feb 18 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.4-12
- Enable CONFIG_IFB
* Wed Feb 17 2021 Ankit Jain <ankitja@vmware.com> 5.10.4-11
- Added latest out of tree version of Intel ice driver
* Tue Feb 16 2021 Alexey Makhalov <amakhalov@vmware.com> 5.10.4-10
- Fix perf compilation issue with gcc-10.2.0 for aarch64
* Mon Feb 15 2021 Keerthana K <keerthanak@vmware.com> 5.10.4-9
- Added crypto_self_test and kattest module.
- These patches are applied when kat_build is enabled.
* Wed Feb 03 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 5.10.4-8
- Update i40e driver to v2.13.10
- Add out of tree iavf driver
- Enable CONFIG_NET_TEAM
* Thu Jan 28 2021 Alexey Makhalov <amakhalov@vmware.com> 5.10.4-7
- Use secure FIPS canister.
* Mon Jan 25 2021 Ankit Jain <ankitja@vmware.com> 5.10.4-6
- Enabled CONFIG_WIREGUARD
* Fri Jan 22 2021 Keerthana K <keerthanak@vmware.com> 5.10.4-5
- Build kernel with FIPS canister.
* Wed Jan 20 2021 Alexey Makhalov <amakhalov@vmware.com> 5.10.4-4
- Handle module.lds for aarch64 in the same way as for x86_64
* Wed Jan 13 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.4-3
- Remove traceevent/plugins from linux-tools
* Mon Jan 11 2021 Bo Gan <ganb@vmware.com> 5.10.4-2
- Fix aarch64 build failure
* Mon Jan 04 2021 Bo Gan <ganb@vmware.com> 5.10.4-1
- Update to 5.10.4
- Drop out-of-tree SEV-ES functional patches (already upstreamed).
* Wed Dec 09 2020 Ajay Kaher <akaher@vmware.com> 5.9.0-9
- To dynamic load Overlays adding of_configfs patches v5.9.y.
* Tue Dec 01 2020 Prashant S Chauhan <psinghchauha@vmware.com> 5.9.0-8
- Added ami for arm support in linux generic, added multiple drivers
- in aarch64 to support aws ami
* Thu Nov 12 2020 Ajay Kaher <akaher@vmware.com> 5.9.0-7
- .config: support for floppy disk and ch341 usb to serial
* Wed Nov 11 2020 Tapas Kundu <tkundu@vmware.com> 5.9.0-6
- Fix perf python script for compatibility with python 3.9
* Tue Nov 10 2020 Keerthana K <keerthanak@vmware.com> 5.9.0-5
- Fix CVE-2020-8694
* Fri Nov 06 2020 Keerthana K <keerthanak@vmware.com> 5.9.0-4
- Fix CVE-2020-25704
* Tue Nov 03 2020 Srinidhi Rao <srinidhir@vmware.com> 5.9.0-3
- Remove the support of fipsify and hmacgen
* Tue Oct 27 2020 Piyush Gupta <gpiyush@vmware.com> 5.9.0-2
- Fix aarch64 build failure due to missing CONFIG_FB_ARMLCD
* Mon Oct 19 2020 Bo Gan <ganb@vmware.com> 5.9.0-1
- Update to 5.9.0
* Wed Sep 30 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.9.0-rc7.1
- Update to version 5.9.0-rc7
* Mon Sep 21 2020 Bo Gan <ganb@vmware.com> 5.9.0-rc4.1
- Update to 5.9.0-rc4
- AMD SEV-ES Support
- RPI4 Support
- config_common: Reduce linked-in modules
- Drop NXP LS10XXa board support
* Tue Sep 08 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 4.19.127-6
- Fix build failure with binutils updated to 2.35
* Wed Aug 05 2020 Sharan Turlapati <sturlapati@vmware.com> 4.19.127-5
- Enable CONFIG_TCP_CONG_BBR
* Wed Jul 29 2020 Alexey Makhalov <amakhalov@vmware.com> 4.19.127-4
- .config: add zram module
* Mon Jul 27 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.127-3
- Fix CVE-2020-14331
* Fri Jul 17 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.127-2
- Fix aarch64 build failure due to missing i40e man pages.
* Tue Jun 23 2020 Keerthana K <keerthanak@vmware.com> 4.19.127-1
- Update to version 4.19.127
* Tue Jun 16 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.112-14
- Add latest out of tree version of i40e driver
* Wed Jun 10 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.112-13
- Enable CONFIG_VFIO_NOIOMMU
* Tue Jun 09 2020 Alexey Makhalov <amakhalov@vmware.com> 4.19.112-12
- Add intel_sgx module (-drivers-intel-sgx subpackage)
* Fri Jun 05 2020 Ankit Jain <ankitja@vmware.com> 4.19.112-11
- Enabled CONFIG_BINFMT_MISC
* Tue Jun 02 2020 Vikash Bansal <bvikas@vmware.com> 4.19.112-10
- Add patch to fix CVE-2019-18885
* Mon Jun 1 2020 Shreenidhi Shedi <sshedi@vmware.com> 4.19.112-9
- Keep modules of running kernel till next boot
* Sat May 30 2020 Alexey Makhalov <amakhalov@vmware.com> 4.19.112-8
- .config: add gs_usb module
* Wed May 20 2020 Tapas Kundu <tkundu@vmware.com> 4.19.112-7
- Added linux-python3-perf subpackage.
- Added turbostat and cpupower to tools for x86_64.
- linux-python3-perf replaces python3-perf.
* Fri May 15 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.112-6
- Add uio_pic_generic driver support in config
* Wed May 06 2020 Siddharth Chandrasekaran <csiddharth@vmware.com> 4.19.112-5
- Add patch to fix CVE-2020-10711
* Wed Apr 29 2020 Keerthana K <keerthanak@vmware.com> 4.19.112-4
- Photon-checksum-generator version update to 1.1.
* Wed Apr 29 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.112-3
- Enable additional config options.
* Wed Apr 15 2020 Vikash Bansal <bvikas@vmware.com> 4.19.112-2
- HMAC-SHA256 digest of hmac_generator module moved to hmacgen package
* Wed Apr 08 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.112-1
- Update to version 4.19.112
* Tue Mar 31 2020 Vikash Bansal <bvikas@vmware.com> 4.19.104-2
- hmac generation of crypto modules and initrd generation changes if fips=1
* Wed Mar 25 2020 Vikash Bansal <bvikas@vmware.com> 4.19.104-1
- Update to version 4.19.104
* Mon Mar 23 2020 Alexey Makhalov <amakhalov@vmware.com> 4.19.97-8
- Fix perf compilation issue with binutils >= 2.34.
* Mon Mar 16 2020 Keerthana K <keerthanak@vmware.com> 4.19.97-7
- Adding Enhances depedency to hmacgen.
* Wed Mar 04 2020 Vikash Bansal <bvikas@vmware.com> 4.19.97-6
- Backporting of patch continuous testing of RNG from urandom
* Tue Feb 25 2020 Ajay Kaher <akaher@vmware.com> 4.19.97-5
- Fix CVE-2019-16234
* Tue Feb 11 2020 Keerthana K <keerthanak@vmware.com> 4.19.97-4
- Add photon-checksum-generator source tarball and remove hmacgen patch.
- Exclude hmacgen.ko from base package.
* Fri Jan 31 2020 Ajay Kaher <akaher@vmware.com> 4.19.97-3
- Move snd-bcm2835.ko to linux-drivers-sound rpm
* Wed Jan 29 2020 Keerthana K <keerthanak@vmware.com> 4.19.97-2
- Update tcrypt to test drbg_pr_sha256 and drbg_nopr_sha256.
- Update testmgr to add drbg_pr_ctr_aes256 test vectors.
* Fri Jan 17 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.97-1
- Update to version 4.19.97
* Thu Jan 16 2020 Srinidhi Rao <srinidhir@vmware.com> 4.19.87-6
- Enable DRBG HASH and DRBG CTR support.
* Wed Jan 08 2020 Ajay Kaher <akaher@vmware.com> 4.19.87-5
- Enabled configs RTC_DRV_PL030, RTC_DRV_PL031
* Fri Jan 03 2020 Keerthana K <keerthanak@vmware.com> 4.19.87-4
- Modify tcrypt to remove tests for algorithms that are not supported in photon.
- Added tests for DH, DRBG algorithms.
* Thu Jan 02 2020 Keerthana K <keerthanak@vmware.com> 4.19.87-3
- Update fips Kat tests patch.
* Mon Dec 09 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.87-2
- Cross compilation support
* Fri Dec 06 2019 Ajay Kaher <akaher@vmware.com> 4.19.87-1
- Update to version 4.19.87
* Tue Dec 03 2019 Keerthana K <keerthanak@vmware.com> 4.19.84-4
- Adding hmac sha256/sha512 generator kernel module for fips.
* Tue Nov 26 2019 Ajay Kaher <akaher@vmware.com> 4.19.84-3
- Fix CVE-2019-19062, CVE-2019-19066, CVE-2019-19072,
- CVE-2019-19073, CVE-2019-19074, CVE-2019-19078
* Mon Nov 18 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.84-2
- .config: infiniband support.
* Tue Nov 12 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.84-1
- Update to version 4.19.84
- Fix CVE-2019-18814
* Fri Nov 08 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.82-1
- Update to version 4.19.82
* Thu Nov 07 2019 Jorgen Hansen (VMware) <jhansen@vmware.com> 4.19.79-3
- Fix vsock QP detach with outgoing data
* Thu Oct 24 2019 Ajay Kaher <akaher@vmware.com> 4.19.79-2
- Enabled WiFi and BT config for Dell 5K.
* Tue Oct 15 2019 Ajay Kaher <akaher@vmware.com> 4.19.79-1
- Update to version 4.19.79
- Fix CVE-2019-17133
* Mon Oct 14 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.76-5
- Add megaraid_sas driver to initramfs
* Mon Oct 14 2019 Bo Gan <ganb@vmware.com> 4.19.76-4
- Enable IMA with SHA256 as default hash algorithm
* Thu Oct 10 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.76-3
- Add additional BuildRequires and Requires to fix issues with perf, related to
- interactive UI and C++ symbol demangling. Also update the last few perf python
- scripts in Linux kernel to use python3 syntax.
* Thu Oct 10 2019 Harinadh D <hdommaraju@vmware.com> 4.19.76-2
- Adding lvm and dm-mod modules to support root as lvm
* Wed Oct 02 2019 Ajay Kaher <akaher@vmware.com> 4.19.76-1
- Update to version 4.19.76
- Enable USB_SERIAL_PL2303 for aarch64
* Mon Sep 30 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.72-1
- Update to version 4.19.72
* Thu Sep 05 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.69-3
- Avoid oldconfig which leads to potential build hang
- Fix archdir usage
* Thu Sep 05 2019 Ajay Kaher <akaher@vmware.com> 4.19.69-2
- Adding SPI and Audio interfaces in rpi3 device tree
- Adding spi0 and audio overlays
- Copying rpi dt in /boot/broadcom as u-boot picks from here
* Fri Aug 30 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.69-1
- Update to version 4.19.69
* Fri Aug 23 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.65-4
- NXP ls1046a frwy board support.
- config_aarch64: add fsl_dpaa2 support.
- fix fsl_dpaa_mac initialization issue.
* Wed Aug 14 2019 Raejoon Jung <rjung@vmware.com> 4.19.65-3
- Backport of Secure Boot UEFI certificate import from v5.2
* Mon Aug 12 2019 Ajay Kaher <akaher@vmware.com> 4.19.65-2
- Fix config_aarch64 for v4.19.65
* Tue Aug 06 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.65-1
- Update to version 4.19.65
- Fix CVE-2019-1125 (SWAPGS)
* Tue Jul 30 2019 Ajay Kaher <akaher@vmware.com> 4.19.52-7
- Added of_configfs patches to dynamic load Overlays.
* Thu Jul 25 2019 Keerthana K <keerthanak@vmware.com> 4.19.52-6
- Fix postun scriplet.
* Thu Jul 11 2019 Keerthana K <keerthanak@vmware.com> 4.19.52-5
- Enable kernel configs necessary for BPF Compiler Collection (BCC).
* Wed Jul 10 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.52-4
- Deprecate linux-aws-tools in favor of linux-tools.
* Tue Jul 02 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.52-3
- Fix 9p vsock 16bit port issue.
* Thu Jun 20 2019 Tapas Kundu <tkundu@vmware.com> 4.19.52-2
- Enabled CONFIG_I2C_CHARDEV to support lm-sensors
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
* Thu Apr 11 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.32-3
- Update config_aarch64 to fix ARM64 build.
* Fri Mar 29 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.32-2
- Fix CVE-2019-10125
* Wed Mar 27 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.32-1
- Update to version 4.19.32
* Thu Mar 14 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.29-1
- Update to version 4.19.29
* Tue Mar 05 2019 Ajay Kaher <akaher@vmware.com> 4.19.26-1
- Update to version 4.19.26
* Thu Feb 21 2019 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.15-3
- Fix CVE-2019-8912
* Thu Jan 24 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.15-2
- Add WiFi (ath10k), sensors (i2c,spi), usb support for NXP LS1012A board.
* Tue Jan 15 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.15-1
- Update to version 4.19.15
* Fri Jan 11 2019 Srinidhi Rao <srinidhir@vmware.com> 4.19.6-7
- Add Network support for NXP LS1012A board.
* Wed Jan 09 2019 Ankit Jain <ankitja@vmware.com> 4.19.6-6
- Enable following for x86_64 and aarch64:
-  Enable Kernel Address Space Layout Randomization.
-  Enable CONFIG_SECURITY_NETWORK_XFRM
* Fri Jan 04 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.6-5
- Enable AppArmor by default.
* Wed Jan 02 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.6-4
- .config: added Compulab fitlet2 device drivers
- .config_aarch64: added gpio sysfs support
- renamed -sound to -drivers-sound
* Tue Jan 01 2019 Ajay Kaher <akaher@vmware.com> 4.19.6-3
- .config: Enable CONFIG_PCI_HYPERV driver
* Wed Dec 19 2018 Srinidhi Rao <srinidhir@vmware.com> 4.19.6-2
- Add NXP LS1012A support.
* Mon Dec 10 2018 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.6-1
- Update to version 4.19.6
* Fri Dec 07 2018 Alexey Makhalov <amakhalov@vmware.com> 4.19.1-3
- .config: added qmi wwan module
* Mon Nov 12 2018 Ajay Kaher <akaher@vmware.com> 4.19.1-2
- Fix config_aarch64 for 4.19.1
* Mon Nov 05 2018 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.1-1
- Update to version 4.19.1
* Tue Oct 16 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.18.9-5
- Change in config to enable drivers for zigbee and GPS
* Fri Oct 12 2018 Ajay Kaher <akaher@vmware.com> 4.18.9-4
- Enable LAN78xx for aarch64 rpi3
* Fri Oct 5 2018 Ajay Kaher <akaher@vmware.com> 4.18.9-3
- Fix config_aarch64 for 4.18.9
- Add module.lds for aarch64
* Wed Oct 03 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.18.9-2
- Use updated steal time accounting patch.
- .config: Enable CONFIG_CPU_ISOLATION and a few networking options
- that got accidentally dropped in the last update.
* Mon Oct 1 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.18.9-1
- Update to version 4.18.9
* Tue Sep 25 2018 Ajay Kaher <akaher@vmware.com> 4.14.67-2
- Build hang (at make oldconfig) fix in config_aarch64
* Wed Sep 19 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.14.67-1
- Update to version 4.14.67
* Tue Sep 18 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.14.54-7
- Add rdrand-based RNG driver to enhance kernel entropy.
* Sun Sep 02 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.14.54-6
- Add full retpoline support by building with retpoline-enabled gcc.
* Thu Aug 30 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.14.54-5
- Apply out-of-tree patches needed for AppArmor.
* Wed Aug 22 2018 Alexey Makhalov <amakhalov@vmware.com> 4.14.54-4
- Fix overflow kernel panic in rsi driver.
- .config: enable BT stack, enable GPIO sysfs.
- Add Exar USB serial driver.
* Fri Aug 17 2018 Ajay Kaher <akaher@vmware.com> 4.14.54-3
- Enabled USB PCI in config_aarch64
- Build hang (at make oldconfig) fix in config_aarch64
* Thu Jul 19 2018 Alexey Makhalov <amakhalov@vmware.com> 4.14.54-2
- .config: usb_serial_pl2303=m,wlan=y,can=m,gpio=y,pinctrl=y,iio=m
* Mon Jul 09 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.14.54-1
- Update to version 4.14.54
* Fri Jan 26 2018 Alexey Makhalov <amakhalov@vmware.com> 4.14.8-2
- Added vchiq entry to rpi3 dts
- Added dtb-rpi3 subpackage
* Fri Dec 22 2017 Alexey Makhalov <amakhalov@vmware.com> 4.14.8-1
- Version update
* Wed Dec 13 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.66-4
- KAT build support
* Thu Dec 07 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.66-3
- Aarch64 support
* Tue Dec 05 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.66-2
- Sign and compress modules after stripping. fips=1 requires signed modules
* Mon Dec 04 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.66-1
- Version update
* Tue Nov 21 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.64-1
- Version update
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
* Mon Jul 03 2017 Xiaolin Li <xiaolinl@vmware.com> 4.9.34-3
- Add libdnet-devel, kmod-devel and libmspack-devel to BuildRequires
* Thu Jun 29 2017 Divya Thaluru <dthaluru@vmware.com> 4.9.34-2
- Added obsolete for deprecated linux-dev package
* Wed Jun 28 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.34-1
- [feature] 9P FS security support
- [feature] DM Delay target support
- Fix CVE-2017-1000364 ("stack clash") and CVE-2017-9605
* Thu Jun 8 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.31-1
- Fix CVE-2017-8890, CVE-2017-9074, CVE-2017-9075, CVE-2017-9076
    CVE-2017-9077 and CVE-2017-9242
- [feature] IPV6 netfilter NAT table support
* Fri May 26 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.30-1
- Added ENA driver for AMI
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
- Fix audit-devel BuildRequires.
- .config: build nvme and nvme-core in kernel.
* Mon Mar 6 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.13-2
- .config: NSX requirements for crypto and netfilter
* Tue Feb 28 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.13-1
- Update to linux-4.9.13 to fix CVE-2017-5986 and CVE-2017-6074
* Thu Feb 09 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.9-1
- Update to linux-4.9.9 to fix CVE-2016-10153, CVE-2017-5546,
    CVE-2017-5547, CVE-2017-5548 and CVE-2017-5576.
- .config: added CRYPTO_FIPS support.
* Tue Jan 10 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.2-1
- Update to linux-4.9.2 to fix CVE-2016-10088
- Move linux-tools.spec to linux.spec as -tools subpackage
* Mon Dec 19 2016 Xiaolin Li <xiaolinl@vmware.com> 4.9.0-2
- BuildRequires Linux-PAM-devel
* Mon Dec 12 2016 Alexey Makhalov <amakhalov@vmware.com> 4.9.0-1
- Update to linux-4.9.0
- Add paravirt stolen time accounting feature (from linux-esx),
    but disable it by default (no-vmw-sta cmdline parameter)
* Thu Dec  8 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.35-3
- net-packet-fix-race-condition-in-packet_set_ring.patch
    to fix CVE-2016-8655
* Wed Nov 30 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.35-2
- Expand `uname -r` with release number
- Check for build-id matching
- Added syscalls tracing support
- Compress modules
* Mon Nov 28 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.35-1
- Update to linux-4.4.35
- vfio-pci-fix-integer-overflows-bitmask-check.patch
    to fix CVE-2016-9083
* Tue Nov 22 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.31-4
- net-9p-vsock.patch
* Thu Nov 17 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.31-3
- tty-prevent-ldisc-drivers-from-re-using-stale-tty-fields.patch
    to fix CVE-2015-8964
* Tue Nov 15 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.31-2
- .config: add cgrup_hugetlb support
- .config: add netfilter_xt_{set,target_ct} support
- .config: add netfilter_xt_match_{cgroup,ipvs} support
* Thu Nov 10 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.31-1
- Update to linux-4.4.31
* Fri Oct 21 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.26-1
- Update to linux-4.4.26
* Wed Oct 19 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.20-6
- net-add-recursion-limit-to-GRO.patch
- scsi-arcmsr-buffer-overflow-in-arcmsr_iop_message_xfer.patch
* Tue Oct 18 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.20-5
- ipip-properly-mark-ipip-GRO-packets-as-encapsulated.patch
- tunnels-dont-apply-GRO-to-multiple-layers-of-encapsulation.patch
* Mon Oct  3 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.20-4
- Package vmlinux with PROGBITS sections in -debuginfo subpackage
* Tue Sep 27 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.20-3
- .config: CONFIG_IP_SET_HASH_{IPMARK,MAC}=m
* Tue Sep 20 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.20-2
- Add -release number for /boot/* files
- Use initrd.img with version and release number
- Rename -dev subpackage to -devel
* Wed Sep  7 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.20-1
- Update to linux-4.4.20
- apparmor-fix-oops-validate-buffer-size-in-apparmor_setprocattr.patch
- keys-fix-asn.1-indefinite-length-object-parsing.patch
* Thu Aug 25 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-11
- vmxnet3 patches to bumpup a version to 1.4.8.0
* Wed Aug 10 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-10
- Added VSOCK-Detach-QP-check-should-filter-out-non-matching-QPs.patch
- .config: pmem hotplug + ACPI NFIT support
- .config: enable EXPERT mode, disable UID16 syscalls
* Thu Jul 07 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-9
- .config: pmem + fs_dax support
* Fri Jun 17 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-8
- patch: e1000e-prevent-div-by-zero-if-TIMINCA-is-zero.patch
- .config: disable rt group scheduling - not supported by systemd
* Wed Jun 15 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.4.8-7
- fixed the capitalization for - System.map
* Thu May 26 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-6
- patch: REVERT-sched-fair-Beef-up-wake_wide.patch
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.4.8-5
- GA - Bump release of all rpms
* Mon May 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.4.8-4
- Fixed generation of debug symbols for kernel modules & vmlinux.
* Mon May 23 2016 Divya Thaluru <dthaluru@vmware.com> 4.4.8-3
- Added patches to fix CVE-2016-3134, CVE-2016-3135
* Wed May 18 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.4.8-2
- Enabled CONFIG_UPROBES in config as needed by ktap
* Wed May 04 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-1
- Update to linux-4.4.8
- Added net-Drivers-Vmxnet3-set-... patch
* Tue May 03 2016 Vinay Kulkarni <kulkarniv@vmware.com> 4.2.0-27
- Compile Intel GigE and VMXNET3 as part of kernel.
* Thu Apr 28 2016 Nick Shi <nshi@vmware.com> 4.2.0-26
- Compile cramfs.ko to allow mounting cramfs image
* Tue Apr 12 2016 Vinay Kulkarni <kulkarniv@vmware.com> 4.2.0-25
- Revert network interface renaming disable in kernel.
* Tue Mar 29 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-24
- Support kmsg dumping to vmware.log on panic
- sunrpc: xs_bind uses ip_local_reserved_ports
* Mon Mar 28 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.2.0-23
- Enabled Regular stack protection in Linux kernel in config
* Thu Mar 17 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.2.0-22
- Restrict the permissions of the /boot/System.map-X file
* Fri Mar 04 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-21
- Patch: SUNRPC: Do not reuse srcport for TIME_WAIT socket.
* Wed Mar 02 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-20
- Patch: SUNRPC: Ensure that we wait for connections to complete
    before retrying
* Fri Feb 26 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-19
- Disable watchdog under VMware hypervisor.
* Thu Feb 25 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-18
- Added rpcsec_gss_krb5 and nfs_fscache
* Mon Feb 22 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-17
- Added sysctl param to control weighted_cpuload() behavior
* Thu Feb 18 2016 Divya Thaluru <dthaluru@vmware.com> 4.2.0-16
- Disabling network renaming
* Sun Feb 14 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-15
- veth patch: don’t modify ip_summed
* Thu Feb 11 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-14
- Full tickless -> idle tickless + simple CPU time accounting
- SLUB -> SLAB
- Disable NUMA balancing
- Disable stack protector
- No build_forced no-CBs CPUs
- Disable Expert configuration mode
- Disable most of debug features from 'Kernel hacking'
* Mon Feb 08 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-13
- Double tcp_mem limits, patch is added.
* Wed Feb 03 2016 Anish Swaminathan <anishs@vmware.com>  4.2.0-12
- Fixes for CVE-2015-7990/6937 and CVE-2015-8660.
* Tue Jan 26 2016 Anish Swaminathan <anishs@vmware.com> 4.2.0-11
- Revert CONFIG_HZ=250
* Fri Jan 22 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-10
- Fix for CVE-2016-0728
* Wed Jan 13 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-9
- CONFIG_HZ=250
* Tue Jan 12 2016 Mahmoud Bassiouny <mbassiouny@vmware.com> 4.2.0-8
- Remove rootfstype from the kernel parameter.
* Mon Jan 04 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.2.0-7
- Disabled all the tracing options in kernel config.
- Disabled preempt.
- Disabled sched autogroup.
* Thu Dec 17 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.2.0-6
- Enabled kprobe for systemtap & disabled dynamic function tracing in config
* Fri Dec 11 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.2.0-5
- Added oprofile kernel driver sub-package.
* Fri Nov 13 2015 Mahmoud Bassiouny <mbassiouny@vmware.com> 4.2.0-4
- Change the linux image directory.
* Wed Nov 11 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.2.0-3
- Added the build essential files in the dev sub-package.
* Mon Nov 09 2015 Vinay Kulkarni <kulkarniv@vmware.com> 4.2.0-2
- Enable Geneve module support for generic kernel.
* Fri Oct 23 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.2.0-1
- Upgraded the generic linux kernel to version 4.2.0 & and updated timer handling to full tickless mode.
* Tue Sep 22 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.0.9-5
- Added driver support for frame buffer devices and ACPI
* Wed Sep 2 2015 Alexey Makhalov <amakhalov@vmware.com> 4.0.9-4
- Added mouse ps/2 module.
* Fri Aug 14 2015 Alexey Makhalov <amakhalov@vmware.com> 4.0.9-3
- Use photon.cfg as a symlink.
* Thu Aug 13 2015 Alexey Makhalov <amakhalov@vmware.com> 4.0.9-2
- Added environment file(photon.cfg) for grub.
* Wed Aug 12 2015 Sharath George <sharathg@vmware.com> 4.0.9-1
- Upgrading kernel version.
* Wed Aug 12 2015 Alexey Makhalov <amakhalov@vmware.com> 3.19.2-5
- Updated OVT to version 10.0.0.
- Rename -gpu-drivers to -drivers-gpu in accordance to directory structure.
- Added -sound package/
* Tue Aug 11 2015 Anish Swaminathan<anishs@vmware.com> 3.19.2-4
- Removed Requires dependencies.
* Fri Jul 24 2015 Harish Udaiya Kumar <hudaiyakumar@gmail.com> 3.19.2-3
- Updated the config file to include graphics drivers.
* Mon May 18 2015 Touseef Liaqat <tliaqat@vmware.com> 3.13.3-2
- Update according to UsrMove.
* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 3.13.3-1
- Initial build. First version
