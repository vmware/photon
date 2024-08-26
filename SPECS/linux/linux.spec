%global security_hardening none

%ifarch x86_64
%define arch x86_64
%endif

%ifarch aarch64
%define arch arm64
%endif

Summary:        Kernel
Name:           linux
Version:        4.19.320
Release:        1%{?kat_build:.kat}%{?dist}
License:        GPLv2
URL:            http://www.kernel.org
Group:          System Environment/Kernel
Vendor:         VMware, Inc.
Distribution:   Photon

%define uname_r %{version}-%{release}
%define _modulesdir /lib/modules/%{uname_r}

Source0: http://www.kernel.org/pub/linux/kernel/v4.x/linux-%{version}.tar.xz
%define sha512 linux=7c2c79dcd6ae82a0142f795f46200f7eda40732ededb9dd5bdaebcbd41b06ea7e0c959bcf8d88332bd454b551c9b5641ac662b5a030393eeb4c1f74ca3620014

%ifarch x86_64
Source1: config
%endif

Source2: initramfs.trigger

%define ena_version 1.6.0
Source3: https://github.com/amzn/amzn-drivers/archive/ena_linux_%{ena_version}.tar.gz
%define sha512 ena_linux=3106ed2f098ae0963875443e6d6f96c6ccb6e379abd5616e8f4dd8c11f0adad45d2d2699729e658819b2141e87eff97517518b43b27ce94de1c0bf593ba77ad7

%ifarch aarch64
Source4: config_aarch64
%endif

# contains pre, postun, filetriggerun tasks
Source6: scriptlets.inc
Source7: check_for_config_applicability.inc

%global photon_checksum_generator_version 1.2
Source8: https://github.com/vmware/photon-checksum-generator/releases/photon-checksum-generator-%{photon_checksum_generator_version}.tar.gz
%define sha512 photon-checksum-generator=bc0e3fc039cffc7bbd019da0573a89ed4cf227fd51f85d1941de060cb2a595ea1ef45914419e3238a8ebcc23cdd83193be4f1a294806f954ef8c74cdede8886b

Source9: genhmac.inc

%define dcap_version 1.6
Source10: https://github.com/intel/SGXDataCenterAttestationPrimitives/archive/DCAP_%{dcap_version}.tar.gz
%define sha512 DCAP=264c2c9e6554e533c41df34291d5809bd18b32384c5d871687dae7d3587b200459fcfffe0a95d93063cb29c6b5a50feebc99612e3d7403c24c410c43b0e2f64c

%define i40e_version 2.23.17
Source11: https://sourceforge.net/projects/e1000/files/i40e%20stable/%{i40e_version}/i40e-%{i40e_version}.tar.gz
%define sha512 i40e=5dbe5186f23d14aac185f74283377d9bfc0837ab16b145a107f735d5439a207e27db871e278656cd06ba595f426d7095a294d39110df5ad6b30ea9f6d3a2a3a7

%define iavf_version 4.9.5
Source13: https://sourceforge.net/projects/e1000/files/iavf%20stable/%{iavf_version}/iavf-%{iavf_version}.tar.gz
%define sha512 iavf=2e97671d1fd51b5b0017b49dcfa62854ef55a85182fcd4990d2d7faea0c3dc9532fe3896c81eabff3c30fb3b2b9573c22416adfec3a1e0f0107c44a9216fbf3a

%define ice_version 1.13.7
Source14: https://sourceforge.net/projects/e1000/files/ice%20stable/%{ice_version}/ice-%{ice_version}.tar.gz
%define sha512 ice=6167a0240624915ee6dce8f2186d6980c224baab8bcccee2b1d991d5cc15510b95b7b2a309cc60e57eae7dfffc4e2186730650ba104a231e54711c3b01f20f7b

# common
Patch1: double-tcp_mem-limits.patch
Patch3: SUNRPC-Do-not-reuse-srcport-for-TIME_WAIT-socket.patch
Patch4: SUNRPC-xs_bind-uses-ip_local_reserved_ports.patch
Patch5: vsock-transport-for-9p.patch
Patch6: 9p-trans_fd-extend-port-variable-to-u32.patch
Patch7: perf-scripts-python-Convert-python2-scripts-to-python3.patch
Patch8: vsock-delay-detach-of-QP-with-outgoing-data.patch
Patch9: 0001-cgroup-v1-cgroup_stat-support.patch
Patch10: Performance-over-security-model.patch
#HyperV patches
Patch11: 0004-vmbus-Don-t-spam-the-logs-with-unknown-GUIDs.patch

# Expose Photon kernel macros to identify kernel flavor and version
Patch12: 0001-kbuild-simplify-access-to-the-kernel-s-version.patch
Patch13: 0002-kbuild-Fix-linux-version.h-for-empty-SUBLEVEL-or-PAT.patch
Patch14: 0003-kbuild-replace-if-A-A-B-with-or-A-B.patch
Patch15: 0004-kbuild-Makefile-Introduce-macros-to-distinguish-Phot.patch
Patch16: 0005-linux-Makefile-Add-kernel-flavor-info-to-the-generat.patch

%ifarch x86_64
# floppy:
Patch17: 0001-floppy-lower-printk-message-priority.patch
%endif

Patch25: 0001-tools-perf-fix-compilation-error.patch
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
# Secure boot uefi certificate import patches
Patch40: secure-boot-patches/0001-security-integrity-remove-unnecessary-init_keyring-v.patch
Patch41: secure-boot-patches/0002-integrity-Define-a-trusted-platform-keyring.patch
Patch42: secure-boot-patches/0003-integrity-Load-certs-to-the-platform-keyring.patch
Patch43: secure-boot-patches/0004-efi-Add-EFI-signature-data-types.patch
Patch44: secure-boot-patches/0005-efi-Add-an-EFI-signature-blob-parser.patch
Patch45: secure-boot-patches/0006-efi-Import-certificates-from-UEFI-Secure-Boot.patch

#Fix for CVE-2019-19338
Patch47: 0001-KVM-vmx-implement-MSR_IA32_TSX_CTRL-disable-RTM-func.patch
Patch48: 0001-KVM-vmx-use-MSR_IA32_TSX_CTRL-to-hard-disable-TSX-on.patch

#Fix for CVE-2024-0565
Patch50: 0001-smb-client-fix-OOB-in-receive_encrypted_standard.patch

# Fix for CVE-2020-16119
Patch59: 0001-dccp-ccid-move-timers-to-struct-dccp_sock.patch
Patch60: 0002-Revert-dccp-don-t-free-ccid2_hc_tx_sock-struct-in-dc.patch

#Fix for CVE-2020-16120
Patch61: 0001-ovl-pass-correct-flags-for-opening-real-directory.patch
Patch62: 0002-ovl-switch-to-mounter-creds-in-readdir.patch
Patch63: 0003-ovl-verify-permissions-in-ovl_path_open.patch
Patch64: 0004-ovl-call-secutiry-hook-in-ovl_real_ioctl.patch
Patch65: 0005-ovl-check-permission-to-open-real-file.patch

# Fix for CVE-2019-19770
Patch66: 0001-block-revert-back-to-synchronous-request_queue-remov.patch
Patch67: 0002-block-create-the-request_queue-debugfs_dir-on-regist.patch

#Fix for CVE-2020-36385
Patch68: 0001-RDMA-cma-Add-missing-locking-to-rdma_accept.patch
Patch69: 0001-RDMA-ucma-Rework-ucma_migrate_id-to-avoid-races-with.patch

#Fix for CVE-2022-1055
Patch70: 0001-net-sched-fix-use-after-free-in-tc_new_tfilter.patch

#Fix for 9p
Patch77: 0001-9p-Ensure-seekdir-take-effect-when-entries-in-readdi.patch
Patch78: 0001-9p-VDFS-Initialize-fid-iounit-during-creation-of-p9_.patch

# Upgrade vmxnet3 driver to version 4
Patch80: 0000-vmxnet3-turn-off-lro-when-rxcsum-is-disabled.patch
Patch81: 0001-vmxnet3-prepare-for-version-4-changes.patch
Patch82: 0002-vmxnet3-add-support-to-get-set-rx-flow-hash.patch
Patch83: 0003-vmxnet3-add-geneve-and-vxlan-tunnel-offload-support.patch
Patch84: 0004-vmxnet3-update-to-version-4.patch
Patch85: 0005-vmxnet3-use-correct-hdr-reference-when-packet-is-enc.patch
Patch86: 0006-vmxnet3-allow-rx-flow-hash-ops-only-when-rss-is-enab.patch
Patch87: 0007-vmxnet3-use-correct-tcp-hdr-length-when-packet-is-en.patch
Patch88: 0008-vmxnet3-fix-cksum-offload-issues-for-non-udp-tunnels.patch

Patch89: 0009-vmxnet3-Remove-buf_info-from-device-accessible-struc.patch

# inherit tcp_limit_output_bytes
Patch90: tcp-inherit-TSQ-limit-from-root-namespace.patch
# Patch to add drbg_pr_ctr_aes256 test vectors to testmgr
Patch98: 0001-Add-drbg_pr_ctr_aes256-test-vectors-and-test-to-test.patch
# Patch to call drbg and dh crypto tests from tcrypt
Patch100: 0001-tcrypt-disable-tests-that-are-not-enabled-in-photon.patch

# Next 2 patches are about to be merged into stable
Patch102: 0001-mm-fix-panic-in-__alloc_pages.patch

# Update vmxnet3 driver to version 6
Patch110: 0001-vmxnet3-fix-cksum-offload-issues-for-tunnels-with-no.patch
Patch111: 0002-vmxnet3-prepare-for-version-6-changes.patch
Patch112: 0003-vmxnet3-add-support-for-32-Tx-Rx-queues.patch
Patch113: 0004-vmxnet3-add-support-for-ESP-IPv6-RSS.patch
Patch114: 0005-vmxnet3-set-correct-hash-type-based-on-rss-informati.patch
Patch115: 0006-vmxnet3-increase-maximum-configurable-mtu-to-9190.patch
Patch116: 0007-vmxnet3-update-to-version-6.patch
Patch117: 0008-vmxnet3-fix-minimum-vectors-alloc-issue.patch
Patch118: 0009-vmxnet3-remove-power-of-2-limitation-on-the-queues.patch

# Support for PTP_SYS_OFFSET_EXTENDED ioctl
Patch121: 0001-ptp-reorder-declarations-in-ptp_ioctl.patch
Patch122: 0002-ptp-add-PTP_SYS_OFFSET_EXTENDED-ioctl.patch
Patch123: 0003-ptp-deprecate-gettime64-in-favor-of-gettimex64.patch
Patch124: 0004-ptp-uapi-change-_IOW-to-IOWR-in-PTP_SYS_OFFSET_EXTEN.patch

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
Patch143: 0001-vmxnet3-move-rss-code-block-under-eop-descriptor.patch
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

# CVE-2022-1789
Patch185: 0001-KVM-x86-mmu-fix-NULL-pointer-dereference-on-guest-IN.patch

# CVE-2022-43945
Patch188: 0001-NFSD-Cap-rsize_bop-result-based-on-send-buffer-size.patch
Patch189: 0002-NFSD-Protect-against-send-buffer-overflow-in-NFSv3-R.patch
Patch190: 0003-NFSD-Protect-against-send-buffer-overflow-in-NFSv2-R.patch
Patch191: 0004-NFSD-Protect-against-send-buffer-overflow-in-NFSv3-R.patch

# Fix CVE-2021-46952
Patch192: 0001-NFS-fs_context-validate-UDP-retrans-to-prevent-shift.patch

%ifarch aarch64
# Rpi of_configfs patches
Patch200: 0001-OF-DT-Overlay-configfs-interface.patch
Patch201: 0002-of-configfs-Use-of_overlay_fdt_apply-API-call.patch
Patch202: 0003-arm64-dts-broadcom-Add-symbols-to-dtb.patch
# Rpi add 'spidev' to spidev_dt_ids compatible list
Patch203: 0001-spidev-Add-spidev-compatible-string-to-silence-warni.patch
# Rpi device tree patch
Patch204: 0001-Add-SPI-and-Sound-to-rpi3-device-trees.patch
# Rpi Overlays
Patch205: 0001-Infrastructure-to-compile-Overlays.patch
Patch206: 0002-spi0-overlays-files.patch
Patch207: 0003-audio-overlays-files.patch

# NXP LS10XXa FRWY patches
Patch211: 0001-staging-fsl_ppfe-eth-header-files-for-pfe-driver.patch
Patch212: 0002-staging-fsl_ppfe-eth-introduce-pfe-driver.patch
Patch213: 0003-staging-fsl_ppfe-eth-fix-RGMII-tx-delay-issue.patch
Patch214: 0004-staging-fsl_ppfe-eth-remove-unused-functions.patch
Patch215: 0005-staging-fsl_ppfe-eth-fix-read-write-ack-idx-issue.patch
Patch216: 0006-staging-fsl_ppfe-eth-Make-phy_ethtool_ksettings_get-.patch
Patch217: 0007-staging-fsl_ppfe-eth-add-function-to-update-tmu-cred.patch
Patch218: 0008-staging-fsl_ppfe-eth-Avoid-packet-drop-at-TMU-queues.patch
Patch219: 0009-staging-fsl_ppfe-eth-Enable-PFE-in-clause-45-mode.patch
Patch220: 0010-staging-fsl_ppfe-eth-Disable-autonegotiation-for-2.5.patch
Patch221: 0011-staging-fsl_ppfe-eth-add-missing-included-header-fil.patch
Patch222: 0012-staging-fsl_ppfe-eth-clean-up-iounmap-pfe-ddr_basead.patch
Patch223: 0013-staging-fsl_ppfe-eth-calculate-PFE_PKT_SIZE-with-SKB.patch
Patch224: 0014-staging-fsl_ppfe-eth-support-for-userspace-networkin.patch
Patch225: 0015-staging-fsl_ppfe-eth-unregister-netdev-after-pfe_phy.patch
Patch226: 0016-staging-fsl_ppfe-eth-HW-parse-results-for-DPDK.patch
Patch227: 0017-staging-fsl_ppfe-eth-reorganize-pfe_netdev_ops.patch
Patch228: 0018-staging-fsl_ppfe-eth-use-mask-for-rx-max-frame-len.patch
Patch229: 0019-staging-fsl_ppfe-eth-define-pfe-ndo_change_mtu-funct.patch
Patch230: 0020-staging-fsl_ppfe-eth-remove-jumbo-frame-enable-from-.patch
Patch231: 0021-staging-fsl_ppfe-eth-disable-CRC-removal.patch
Patch232: 0022-staging-fsl_ppfe-eth-handle-ls1012a-errata_a010897.patch
Patch233: 0023-staging-fsl_ppfe-eth-Modify-Kconfig-to-enable-pfe-dr.patch
Patch234: 0001-fsl_dpaa_mac-wait-for-phy-probe-to-complete.patch
%endif

%ifarch x86_64
# VMW:
Patch281: 0001-x86-vmware-Update-platform-detection-code-for-VMCALL.patch
Patch282: 0001-x86-vmware-Add-a-header-file-for-hypercall-definitio.patch
Patch283: 0001-x86-cpu-vmware-Use-the-full-form-of-INL-in-VMWARE_PO.patch
Patch284: 0001-x86-cpu-vmware-Use-the-full-form-of-INL-in-VMWARE_HY.patch
Patch285: 0001-x86-cpu-vmware-Fix-platform-detection-VMWARE_PORT-ma.patch
Patch286: 0001-x86-vmware-Steal-time-accounting-support.patch
Patch287: 0001-x86-alternatives-Add-an-ALTERNATIVE_3-macro.patch
Patch288: 0001-x86-vmware-Use-Efficient-and-Corrent-ALTERNATIVEs-fo.patch
Patch289: 0001-x86-vmware-Log-kmsg-dump-on-panic.patch
Patch290: 0006-x86-vmware-Fix-steal-time-clock-under-SEV.patch

Patch291: 0001-x86-insn-eval-Add-support-for-64-bit-kernel-mode.patch
Patch292: 0001-drm-vmwgfx-Update-the-backdoor-call-with-support-for.patch
Patch293: 0001-x86-vmware-avoid-TSC-recalibration.patch

# vmw: gfx
Patch301: 0001-drm-vmwgfx-Don-t-use-the-HB-port-if-memory-encryptio.patch
Patch302: 0002-drm-vmwgfx-Fix-the-refuse_dma-mode-when-using-guest-.patch
Patch303: 0003-drm-vmwgfx-Refuse-DMA-operation-when-SEV-encryption-.patch

# SEV-ES prerequisite: x86/efi,boot: GDT handling cleanup/fixes
Patch311: 0001-x86-boot-Save-several-bytes-in-decompressor.patch
Patch312: 0002-x86-boot-Remove-KEEP_SEGMENTS-support.patch
Patch313: 0003-efi-x86-Don-t-depend-on-firmware-GDT-layout.patch
Patch314: 0004-x86-boot-Reload-GDTR-after-copying-to-the-end-of-the.patch
Patch315: 0005-x86-boot-Clear-direction-and-interrupt-flags-in-star.patch
Patch316: 0006-efi-x86-Remove-GDT-setup-from-efi_main.patch
Patch317: 0007-x86-boot-GDT-limit-value-should-be-size-1.patch
Patch318: 0008-x86-boot-Micro-optimize-GDT-loading-instructions.patch
Patch319: 0009-x86-boot-compressed-Fix-reloading-of-GDTR-post-relocation.patch

# SEV-ES prerequisite: x86: Add guard pages to exception and interrupt stacks
Patch331: 0001-x86-dumpstack-Fix-off-by-one-errors-in-stack-identif.patch
Patch332: 0002-x86-irq-64-Remove-a-hardcoded-irq_stack_union-access.patch
Patch333: 0003-x86-irq-64-Sanitize-the-top-bottom-confusion.patch
Patch334: 0004-x86-idt-Remove-unused-macro-SISTG.patch
Patch335: 0005-x86-64-Remove-stale-CURRENT_MASK.patch
Patch336: 0006-x86-exceptions-Remove-unused-stack-defines-on-32bit.patch
Patch337: 0007-x86-exceptions-Make-IST-index-zero-based.patch
Patch338: 0008-x86-cpu_entry_area-Cleanup-setup-functions.patch
Patch339: 0009-x86-exceptions-Add-structs-for-exception-stacks.patch
Patch340: 0010-x86-cpu_entry_area-Prepare-for-IST-guard-pages.patch
Patch341: 0011-x86-cpu_entry_area-Provide-exception-stack-accessor.patch
Patch342: 0012-x86-traps-Use-cpu_entry_area-instead-of-orig_ist.patch
Patch343: 0013-x86-irq-64-Use-cpu-entry-area-instead-of-orig_ist.patch
Patch344: 0014-x86-dumpstack-64-Use-cpu_entry_area-instead-of-orig_.patch
Patch345: 0015-x86-cpu-Prepare-TSS.IST-setup-for-guard-pages.patch
Patch346: 0016-x86-cpu-Remove-orig_ist-array.patch
Patch347: 0017-x86-exceptions-Disconnect-IST-index-and-stack-order.patch
Patch348: 0018-x86-exceptions-Enable-IST-guard-pages.patch
Patch349: 0019-x86-exceptions-Split-debug-IST-stack.patch
Patch350: 0020-x86-dumpstack-64-Speedup-in_exception_stack.patch
Patch351: 0021-x86-irq-32-Define-IRQ_STACK_SIZE.patch
Patch352: 0022-x86-irq-32-Make-irq-stack-a-character-array.patch
Patch353: 0023-x86-irq-32-Rename-hard-softirq_stack-to-hard-softirq.patch
Patch354: 0024-x86-irq-64-Rename-irq_stack_ptr-to-hardirq_stack_ptr.patch
Patch355: 0025-x86-irq-32-Invoke-irq_ctx_init-from-init_IRQ.patch
Patch356: 0026-x86-irq-32-Handle-irq-stack-allocation-failure-prope.patch
Patch357: 0027-x86-irq-64-Init-hardirq_stack_ptr-during-CPU-hotplug.patch
Patch358: 0028-x86-irq-64-Split-the-IRQ-stack-into-its-own-pages.patch
Patch359: 0029-x86-irq-64-Remap-the-IRQ-stack-with-guard-pages.patch
Patch360: 0030-x86-irq-64-Remove-stack-overflow-debug-code.patch

Patch371: 0001-x86-ioremap-Add-an-ioremap_encrypted-helper.patch
Patch372: 0001-linkage-Introduce-new-macros-for-assembler-symbols.patch

# vmw_pvscsi
Patch381: 0001-scsi-vmw_pvscsi-switch-to-generic-DMA-API.patch
Patch382: 0002-scsi-vmw_pvscsi-Fix-swiotlb-operation.patch
Patch383: 0003-scsi-vmw_pvscsi-Silence-dma-mapping-errors.patch
Patch384: 0004-scsi-vmw_pvscsi-Avoid-repeated-dma-mapping-and-unmapping-of-sg-list-memory.patch
Patch385: 0005-scsi-vmw_pvscsi-Reduce-the-ring-size-when-SEV-is-active.patch
Patch386: 0006-scsi-vmw_pvscsi-Fix-uninitialized-sense-buffer-with-swiotlb.patch

# SEV-ES V3
Patch401: 0001-KVM-SVM-Add-GHCB-definitions.patch
Patch402: 0002-KVM-SVM-Add-GHCB-Accessor-functions.patch
Patch403: 0003-KVM-SVM-Use-__packed-shorthand.patch
Patch404: 0004-x86-cpufeatures-Add-SEV-ES-CPU-feature.patch
Patch405: 0005-x86-traps-Move-some-definitions-to-asm-trap_defs.h.patch
Patch406: 0006-x86-insn-Make-inat-tables.c-suitable-for-pre-decompr.patch
Patch407: 0007-x86-umip-Factor-out-instruction-fetch.patch
Patch408: 0008-x86-umip-Factor-out-instruction-decoding.patch
Patch409: 0009-x86-insn-Add-insn_get_modrm_reg_off.patch
Patch410: 0010-x86-insn-Add-insn_rep_prefix-helper.patch
Patch411: 0011-x86-boot-compressed-64-Disable-red-zone-usage.patch
Patch412: 0012-x86-boot-compressed-64-Switch-to-__KERNEL_CS-after-G.patch
Patch413: 0013-x86-boot-compressed-64-Add-IDT-Infrastructure.patch
Patch414: 0014-x86-boot-compressed-64-Rename-kaslr_64.c-to-ident_ma.patch
Patch415: 0015-x86-boot-compressed-64-Add-page-fault-handler.patch
Patch416: 0016-x86-boot-compressed-64-Always-switch-to-own-page-tab.patch
Patch417: 0017-x86-boot-compressed-64-Don-t-pre-map-memory-in-KASLR.patch
Patch418: 0018-x86-boot-compressed-64-Change-add_identity_map-to-ta.patch
Patch419: 0019-x86-boot-compressed-64-Add-VC-handler.patch
Patch420: 0020-x86-boot-compressed-64-Call-set_sev_encryption_mask.patch
Patch421: 0021-x86-boot-compressed-64-Check-return-value-of-kernel_.patch
Patch422: 0022-x86-boot-compressed-64-Add-set_page_en-decrypted-hel.patch
Patch423: 0023-x86-boot-compressed-64-Setup-GHCB-Based-VC-Exception.patch
Patch424: 0024-x86-boot-compressed-64-Unmap-GHCB-page-before-bootin.patch
Patch425: 0025-x86-sev-es-Add-support-for-handling-IOIO-exceptions.patch
Patch426: 0026-x86-fpu-Move-xgetbv-xsetbv-into-separate-header.patch
Patch427: 0027-x86-sev-es-Add-CPUID-handling-to-VC-handler.patch
Patch428: 0028-x86-idt-Move-IDT-to-data-segment.patch
Patch429: 0029-x86-idt-Split-idt_data-setup-out-of-set_intr_gate.patch
Patch430: 0030-x86-idt-Move-two-function-from-k-idt.c-to-i-a-desc.h.patch
Patch431: 0031-x86-head-64-Install-boot-GDT.patch
Patch432: 0032-x86-head-64-Reload-GDT-after-switch-to-virtual-addre.patch
Patch433: 0033-x86-head-64-Load-segment-registers-earlier.patch
Patch434: 0034-x86-head-64-Switch-to-initial-stack-earlier.patch
Patch435: 0035-x86-head-64-Build-k-head64.c-with-fno-stack-protecto.patch
Patch436: 0036-x86-head-64-Load-IDT-earlier.patch
Patch437: 0037-x86-head-64-Move-early-exception-dispatch-to-C-code.patch
Patch438: 0038-x86-sev-es-Add-SEV-ES-Feature-Detection.patch
Patch439: 0039-x86-sev-es-Print-SEV-ES-info-into-kernel-log.patch
Patch440: 0040-x86-sev-es-Compile-early-handler-code-into-kernel-im.patch
Patch441: 0041-x86-sev-es-Setup-early-VC-handler.patch
Patch442: 0042-x86-sev-es-Setup-GHCB-based-boot-VC-handler.patch
Patch443: 0043-x86-sev-es-Setup-per-cpu-GHCBs-for-the-runtime-handl.patch
Patch444: 0044-x86-sev-es-Allocate-and-Map-IST-stacks-for-VC-handle.patch
Patch445: 0045-x86-dumpstack-64-Handle-VC-exception-stacks.patch
Patch446: 0046-x86-sev-es-Shift-VC-IST-Stack-in-nmi_enter-nmi_exit.patch
Patch447: 0047-x86-sev-es-Add-Runtime-VC-Exception-Handler.patch
Patch448: 0048-x86-sev-es-Wire-up-existing-VC-exit-code-handlers.patch
Patch449: 0049-x86-sev-es-Handle-instruction-fetches-from-user-spac.patch
Patch450: 0050-x86-sev-es-Do-not-crash-on-VC-exceptions-from-user-s.patch
Patch451: 0051-x86-sev-es-Handle-MMIO-events.patch
Patch452: 0052-x86-sev-es-Handle-MMIO-String-Instructions.patch
Patch453: 0053-x86-sev-es-Handle-MSR-events.patch
Patch454: 0054-x86-sev-es-Handle-DR7-read-write-events.patch
Patch455: 0055-x86-sev-es-Handle-WBINVD-Events.patch
Patch456: 0056-x86-sev-es-Handle-RDTSC-P-Events.patch
Patch457: 0057-x86-sev-es-Handle-RDPMC-Events.patch
Patch458: 0058-x86-sev-es-Handle-INVD-Events.patch
Patch459: 0059-x86-sev-es-Handle-MONITOR-MONITORX-Events.patch
Patch460: 0060-x86-sev-es-Handle-MWAIT-MWAITX-Events.patch
Patch461: 0061-x86-sev-es-Handle-VMMCALL-Events.patch
Patch462: 0062-x86-sev-es-Handle-AC-Events.patch
Patch463: 0063-x86-sev-es-Handle-DB-Events.patch
Patch465: 0065-x86-paravirt-Allow-hypervisor-specific-VMMCALL-handl.patch
Patch466: 0066-x86-kvm-Add-KVM-specific-VMMCALL-handling-under-SEV.patch
Patch467: 0067-x86-vmware-Add-VMware-specific-handling-for-VMMCALL.patch
Patch468: 0068-x86-realmode-Add-SEV-ES-specific-trampoline-entry-po.patch
Patch469: 0069-x86-realmode-Setup-AP-jump-table.patch
Patch470: 0070-x86-head-64-Setup-TSS-early-for-secondary-CPUs.patch
Patch471: 0071-x86-head-64-Don-t-call-verify_cpu-on-starting-APs.patch
Patch472: 0072-x86-head-64-Rename-start_cpu0.patch
Patch473: 0073-x86-sev-es-Support-CPU-offline-online.patch
Patch474: 0074-x86-sev-es-Handle-NMI-State.patch
Patch475: 0075-x86-efi-Add-GHCB-mappings-when-SEV-ES-is-active.patch
Patch476: 0001-x86-sev-es-Fix-crash-in-early_set_memory_enc_dec.patch
Patch477: 0001-x86-sev-es-Fix-attempt-to-move-org-backwards-error.patch
Patch478: 0001-swiotlb-Adjust-SWIOTBL-bounce-buffer-size-for-SEV-gu.patch

Patch480: 0001-x86-traps-Split-trap-numbers-out-in-a-separate-heade.patch
Patch482: 0080-x86-boot-Enable-vmw-serial-port-via-Super-I-O.patch
Patch483: 0081-x86-sev-es-Disable-use-of-WP-via-PAT-for-__sme_early.patch
Patch485: 0001-x86-boot-64-Explicitly-map-boot_params-and-command-l.patch
Patch486: 0001-x86-sev-Map-all-the-pages-of-exception-stack.patch
Patch487: 0001-x86-sev-es_Use_GHCB_accessor_for_setting_the_MMIO_scratch_buffer.patch
Patch488: 0001-drm_vmwgfx_Dont_use_screen_objects_when_SEV_is_active.patch
Patch489: 0001-x86-boot-Avoid-VE-during-boot-for-TDX-platforms.patch

# SEV-ES: Security Mitigate
Patch491: 0001-x86-boot-compressed-64-Introduce-sev_status.patch
Patch492: 0002-x86-boot-compressed-64-Sanity-check-CPUID-results-in.patch
Patch493: 0003-x86-boot-compressed-64-Check-SEV-encryption-in-64-bi.patch
Patch494: 0004-x86-head-64-Check-SEV-encryption-before-switching-to.patch
Patch495: 0005-x86-sev-es-Do-not-support-MMIO-to-from-encrypted-mem.patch
Patch496: x86-sev-es-Do-not-unroll-string-IO-for-SEV-ES-guests.patch
Patch497: x86-sev-es-Handle-string-port-IO-to-kernel-memory-properly.patch

# Allow PCI resets to be disabled from vfio_pci module
Patch500: 0001-drivers-vfio-pci-Add-kernel-parameter-to-allow-disab.patch
# Add PCI quirk to allow multiple devices under the same virtual PCI bridge
# to be put into separate IOMMU groups on ESXi.
Patch501: 0001-Add-PCI-quirk-for-VMware-PCIe-Root-Port.patch

# Disable md5 algorithm for sctp if fips is enabled.
Patch506: 0001-disable-md5-algorithm-for-sctp-if-fips-is-enabled.patch

# VMware-specific patch to enable turbostat to work on ESXi
Patch800: 0001-tools-power-turbostat-Skip-some-CPUID-checks-if-runn.patch
# Backports of upstream patches to add Ice Lake support to turbostat
Patch801: 0002-tools-power-turbostat-Support-Ice-Lake-server.patch
Patch802: 0003-tools-power-turbostat-Remove-Package-C6-Retention-on.patch
Patch803: 0004-tools-power-turbostat-Fix-DRAM-Energy-Unit-on-SKX.patch
Patch804: 0005-tools-power-turbostat-fix-ICX-DRAM-power-numbers.patch
Patch805: 0006-tools-power-turbostat-Make-interval-calculation-per-.patch
Patch806: 0007-tools-power-turbostat-Fix-CPU-C1-display-value.patch
Patch807: 0008-turbostat-fix-PC6-displaying-on-some-systems.patch
# Backports of upstream patches to add Sapphire Rapids support to turbostat
Patch808: 0009-x86-cpu-Add-Sapphire-Rapids-CPU-model-number.patch
Patch809: 0010-tools-power-turbostat-separate-SPR-from-ICX.patch
Patch810: 0011-tools-power-turbostat-fix-SPR-PC6-limits.patch
Patch811: 0012-tools-power-turbostat-do-not-decode-ACC-for-ICX-and-.patch
Patch812: 0013-tools-power-turbostat-Use-standard-Energy-Unit-for-S.patch
Patch813: 0014-tools-power-turbostat-harden-against-cpu-hotplug.patch
Patch814: 0015-tools-power-turbostat-elevate-priority-of-interval-m.patch
Patch815: 0016-tools-power-turbostat-Use-sched_getcpu-instead-of-ha.patch
Patch816: 0017-tools-power-turbostat-Restore-ability-to-execute-in-.patch
Patch817: 0018-tools-power-turbostat-reduce-debug-output.patch

#Patches for i40e driver
Patch1503: i40e-v2.23.17-Add-support-for-gettimex64-interface.patch
Patch1504: i40e-v2.23.17-i40e-Make-i40e-driver-honor-default-and-user-defined.patch
Patch1505: i40e-v2.23.17-don-t-install-auxiliary-module-on.patch

#Patches for iavf driver
Patch1512: iavf-v4.9.5-no-aux-symvers.patch
Patch1513: iavf-v4.9.5-iavf-Makefile-added-alias-for-i40evf.patch

#Patches for ice driver
Patch1523: ice-v1.13.7-don-t-install-auxiliary-module-on-modul.patch
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

# Fix for CVE-2021-4204
Patch1550: 0002-bpf-Disallow-unprivileged-bpf-by-default.patch

# Fix for CVE-2022-39189
Patch1551: 0001-KVM-x86-do-not-report-a-vCPU-as-preempted-outside-in.patch

# Fix for CVE-2022-36123
Patch1552: 0001-x86-xen-Use-clear_bss-for-Xen-PV-guests.patch

# Fix for CVE-2021-4037
Patch1553: 0001-xfs-ensure-that-the-inode-uid-gid-match-values-match.patch
Patch1554: 0002-xfs-remove-the-icdinode-di_uid-di_gid-members.patch
Patch1555: 0003-xfs-fix-up-non-directory-creation-in-SGID-directorie.patch

#Fix for CVE-2022-0480
Patch1557: 0001-memcg-enable-accounting-for-file-lock-caches.patch

#Fix for CVE-2022-3061
Patch1558: 0001-video-fbdev-i740fb-Error-out-if-pixclock-equals-zero.patch

#Fix for CVE-2022-3303
Patch1559: 0001-ALSA-pcm-oss-Fix-race-at-SNDCTL_DSP_SYNC.patch

#Fix for CVE-2023-1611
Patch1560: 0001-btrfs-fix-race-between-quota-disable-and-quota-assig.patch

#Fix for CVE-2023-1076
Patch1561: 0001-net-add-sock_init_data_uid.patch
Patch1562: 0001-tap-tap_open-correctly-initialize-socket-uid.patch
Patch1563: 0001-tun-tun_chr_open-correctly-initialize-socket-uid.patch

#Fix for CVE-2021-3759
Patch1565: 0001-memcg-enable-accounting-of-ipc-resources.patch

#Fix for CVE-2023-2124
Patch1566: 0001-xfs-verify-buffer-contents-when-we-skip-log-replay.patch

#Fix for CVE-2023-39197
Patch1567: 0001-netfilter-conntrack-dccp-copy-entire-header-to-stack.patch

#Fix CVE-2023-51779
Patch1569: 0001-Bluetooth-af_bluetooth-Fix-Use-After-Free-in-bt_sock.patch

# Fix CVE-2024-23307
Patch1570: 0001-md-raid5-fix-atomicity-violation-in-raid5_cache_coun.patch

#Fix CVE-2024-26882
Patch1571:0001-net-ip_tunnel-make-sure-to-pull-inner-header-in-ip_t.patch

#Fix CVE-2023-52509
Patch1572: 0001-ravb-Fix-use-after-free-issue-in-ravb_tx_timeout_wor.patch

# Fix CVE-2023-52458
Patch1573: 0001-block-add-check-that-partition-length-needs-to-be-al.patch

%if 0%{?kat_build}
Patch1000: fips-kat-tests.patch
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
BuildRequires:  audit-devel
BuildRequires:  elfutils-libelf-devel
BuildRequires:  binutils-devel
BuildRequires:  xz-devel
BuildRequires:  libunwind-devel
BuildRequires:  slang-devel
BuildRequires:  python3-devel
BuildRequires:  bison
BuildRequires:  gettext
BuildRequires:  which
%ifarch x86_64
BuildRequires:  pciutils-devel
%endif

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
Obsoletes:      linux-dev
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
Requires:       (%{name} = %{version} or linux-esx = %{version} or linux-aws = %{version} or linux-rt = %{version})
Requires:       audit elfutils-libelf binutils-libs xz-libs libunwind slang python3 traceevent-plugins
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

%ifarch aarch64
%package dtb-rpi3
Summary:        Kernel Device Tree Blob files for Raspberry Pi3
Group:          System Environment/Kernel
Requires:       %{name} = %{version}-%{release}
%description dtb-rpi3
Kernel Device Tree Blob files for Raspberry Pi3

%package dtb-ls1012afrwy
Summary:        Kernel Device Tree Blob files for NXP FRWY ls1012a and ls1046a boards
Group:          System Environment/Kernel
Requires:       %{name} = %{version}-%{release}
%description dtb-ls1012afrwy
Kernel Device Tree Blob files for NXP FRWY ls1012a and ls1046a boards
%endif

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
%ifarch x86_64
# Using autosetup is not feasible
%setup -q -T -D -b3 -n linux-%{version}
# Using autosetup is not feasible
%setup -q -T -D -b10 -n linux-%{version}
# Using autosetup is not feasible
%setup -q -T -D -b11 -n linux-%{version}
# Using autosetup is not feasible
%setup -q -T -D -b13 -n linux-%{version}
# Using autosetup is not feasible
%setup -q -T -D -b14 -n linux-%{version}
%endif
# Using autosetup is not feasible
%setup -q -T -D -b8 -n linux-%{version}

%autopatch -p1 -m1 -M16

%ifarch x86_64
%autopatch -p1 -m17 -M17
%endif

%autopatch -p1 -m18 -M194

%ifarch aarch64
# Rpi of_configfs patches
%autopatch -p1 -m200 -M234
%endif

%ifarch x86_64
%autopatch -p1 -m281 -M519

%autopatch -p1 -m800 -M817

# Patches for i40e driver
pushd ../i40e-%{i40e_version}
%autopatch -p1 -m1503 -M1505
popd

#Patches for iavf driver
pushd ../iavf-%{iavf_version}
%autopatch -p1 -m1512 -M1513
popd

# Patches for ice driver
pushd ../ice-%{ice_version}
%autopatch -p1 -m1523 -M1523
popd

%endif

# Usermode helper patches
%autopatch -p1 -m1540 -M1541

# bpfilter patches
%autopatch -p1 -m1545 -M1549

# CVE Patches
%autopatch -p1 -m1550 -M1575

%if 0%{?kat_build}
%patch1000 -p1
%endif

make mrproper %{?_smp_mflags}

%ifarch x86_64
cp %{SOURCE1} .config
%endif

%ifarch aarch64
cp %{SOURCE4} .config
%endif

sed -i 's/CONFIG_LOCALVERSION=""/CONFIG_LOCALVERSION="-%{release}"/' .config

%include %{SOURCE7}

%build
make VERBOSE=1 KBUILD_BUILD_VERSION="1-photon" \
        KBUILD_BUILD_HOST="photon" ARCH=%{?arch} %{?_smp_mflags}

make -C tools perf PYTHON=python3 %{?_smp_mflags}

bldroot="${PWD}"

%ifarch x86_64
#build turbostat and cpupower
make ARCH=%{?arch} -C tools turbostat cpupower PYTHON=python3 %{?_smp_mflags}

# build ENA module
pushd ../amzn-drivers-ena_linux_%{ena_version}/kernel/linux/ena
make -C ${bldroot} M="${PWD}" VERBOSE=1 modules %{?_smp_mflags}
popd

# build Intel SGX module
pushd ../SGXDataCenterAttestationPrimitives-DCAP_%{dcap_version}/driver/linux
make KDIR=${bldroot} %{?_smp_mflags}
popd

# build i40e module
pushd ../i40e-%{i40e_version}
# make doesn't support _smp_mflags
make -C src KSRC=${bldroot} clean
make -C src KSRC=${bldroot} %{?_smp_mflags}
popd

# build iavf module
pushd ../iavf-%{iavf_version}
# make doesn't support _smp_mflags
make -C src KSRC=${bldroot} clean
make -C src KSRC=${bldroot} %{?_smp_mflags}
popd

# build ice module
pushd ../ice-%{ice_version}
# make doesn't support _smp_mflags
make -C src KSRC=${bldroot} clean
make -C src KSRC=${bldroot} %{?_smp_mflags}
popd
%endif

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

%include %{SOURCE9}

# We want to compress modules after stripping. Extra step is added to
# the default __spec_install_post.
%define __spec_install_post \
  %{?__debug_package:%{__debug_install_post}} \
  %{__arch_install_post} \
  %{__os_install_post} \
  %{__modules_install_post} \
  %{__modules_gen_hmac} \
%{nil}

%install
%ifarch x86_64
archdir="x86"
%endif

%ifarch aarch64
archdir="arm64"
%endif

install -vdm 755 %{buildroot}%{_sysconfdir}
install -vdm 755 %{buildroot}/boot
install -vdm 755 %{buildroot}%{_defaultdocdir}/%{name}-%{uname_r}
install -vdm 755 %{buildroot}%{_usrsrc}/%{name}-headers-%{uname_r}
install -vdm 755 %{buildroot}%{_libdir}/debug/%{_modulesdir}
make INSTALL_MOD_PATH=%{buildroot} modules_install %{?_smp_mflags}

bldroot="${PWD}"

%ifarch x86_64
# install ENA module
pushd ../amzn-drivers-ena_linux_%{ena_version}/kernel/linux/ena
make -C ${bldroot} M="${PWD}" INSTALL_MOD_PATH=%{buildroot} \
            modules_install %{?_smp_mflags}
popd

# install Intel SGX module
pushd ../SGXDataCenterAttestationPrimitives-DCAP_%{dcap_version}/driver/linux
mkdir -p %{buildroot}%{_sysconfdir}/udev/rules.d
install -vm 644 10-sgx.rules %{buildroot}%{_sysconfdir}/udev/rules.d
install -vm 644 intel_sgx.ko %{buildroot}%{_modulesdir}/extra/
popd

# The intel_auxiliary.ko kernel module is a common dependency for i40e, iavf
# and ice drivers.  Install it only once, along with the iavf driver
# and re-use it in the ice and i40e drivers.

# install i40e module
pushd ../i40e-%{i40e_version}
make -C src KSRC=${bldroot} INSTALL_MOD_PATH=%{buildroot} \
            INSTALL_MOD_DIR=extra MANDIR=%{_mandir} \
            modules_install_no_aux mandocs_install %{?_smp_mflags}
popd

# install iavf module
pushd ../iavf-%{iavf_version}
make -C src KSRC=${bldroot} INSTALL_MOD_PATH=%{buildroot} \
            INSTALL_MOD_DIR=extra INSTALL_AUX_DIR=extra/auxiliary MANDIR=%{_mandir} \
            modules_install mandocs_install %{?_smp_mflags}

# keep this updated in line with AUX_BUS_HEADERS in iavf-<version>/src/common.mk
aux_bus_headers=("linux/auxiliary_bus.h" "auxiliary_compat.h" "kcompat_generated_defs.h")
for header in "${aux_bus_headers[@]}"; do
    install -Dvm 644 "src/$header" \
            %{buildroot}%{_usrsrc}/%{name}-headers-%{uname_r}/include/linux/"${header##*/}"
done
popd

# install ice module
pushd ../ice-%{ice_version}
make -C src KSRC=${bldroot} INSTALL_MOD_PATH=%{buildroot} \
            INSTALL_MOD_DIR=extra modules_install_no_aux %{?_smp_mflags}

make -C src KSRC=${bldroot} MANDIR=%{_mandir} INSTALL_MOD_PATH=%{buildroot} \
            mandocs_install %{?_smp_mflags}
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

#install photon-checksum-generator module
pushd ../photon-checksum-generator-%{photon_checksum_generator_version}/kernel

make -C ${bldroot} M="${PWD}" INSTALL_MOD_PATH=%{buildroot} \
         modules_install %{?_smp_mflags}
popd

%ifarch aarch64
install -vm 644 arch/arm64/boot/Image %{buildroot}/boot/vmlinuz-%{uname_r}
# Install DTB and Overlays files
install -vdm 755 %{buildroot}/boot/broadcom
install -vdm 755 %{buildroot}/boot/broadcom/overlays
install -vdm 755 %{buildroot}/boot/dtb
install -vm 640 arch/arm64/boot/dts/broadcom/*.dtb %{buildroot}/boot/broadcom/
install -vm 640 arch/arm64/boot/dts/overlays/*.dtbo %{buildroot}/boot/broadcom/overlays/
install -vm 640 arch/arm64/boot/dts/freescale/fsl-ls1012a-frwy.dtb %{buildroot}/boot/dtb/
install -vm 640 arch/arm64/boot/dts/freescale/fsl-ls1046a-rdb.dtb %{buildroot}/boot/dtb/
%endif

# Restrict the permission on System.map-X file
install -vm 400 System.map %{buildroot}/boot/System.map-%{uname_r}
install -vm 644 .config %{buildroot}/boot/config-%{uname_r}
cp -r Documentation/* %{buildroot}%{_defaultdocdir}/%{name}-%{uname_r}

%if 0%{?__debug_package}
install -vm 644 vmlinux %{buildroot}%{_libdir}/debug/%{_modulesdir}/vmlinux-%{uname_r}
# `perf test vmlinux` needs it
ln -s vmlinux-%{uname_r} %{buildroot}%{_libdir}/debug/%{_modulesdir}/vmlinux
%endif

cat > %{buildroot}/boot/%{name}-%{uname_r}.cfg << "EOF"
# GRUB Environment Block
photon_cmdline=init=/lib/systemd/systemd ro loglevel=3 quiet no-vmw-sta cgroup.memory=nokmem
photon_linux=vmlinuz-%{uname_r}
photon_initrd=initrd.img-%{uname_r}
EOF

# Register myself to initramfs
mkdir -p %{buildroot}%{_sharedstatedir}/initramfs/kernel
cat > %{buildroot}%{_sharedstatedir}/initramfs/kernel/%{uname_r} << "EOF"
--add-drivers "tmem xen-scsifront xen-blkfront xen-acpi-processor xen-evtchn xen-gntalloc xen-gntdev xen-privcmd xen-pciback xenfs hv_utils hv_vmbus hv_storvsc hv_netvsc hv_sock hv_balloon cn dm-mod megaraid_sas"
EOF

# Cleanup dangling symlinks
rm -rf %{buildroot}%{_modulesdir}/source \
       %{buildroot}%{_modulesdir}/build

find . -name Makefile* -o -name Kconfig* -o -name *.pl | xargs sh -c 'cp --parents "$@" %{buildroot}%{_usrsrc}/%{name}-headers-%{uname_r}' copy
find arch/${archdir}/include include scripts -type f | xargs sh -c 'cp --parents "$@" %{buildroot}%{_usrsrc}/%{name}-headers-%{uname_r}' copy
find $(find arch/${archdir} -name include -o -name scripts -type d) -type f | xargs sh -c 'cp --parents "$@" %{buildroot}%{_usrsrc}/%{name}-headers-%{uname_r}' copy
find arch/${archdir}/include Module.symvers include scripts -type f | xargs sh -c 'cp --parents "$@" %{buildroot}%{_usrsrc}/%{name}-headers-%{uname_r}' copy

%ifarch x86_64
# CONFIG_STACK_VALIDATION=y requires objtool to build external modules
install -vsm 755 tools/objtool/objtool %{buildroot}%{_usrsrc}/%{name}-headers-%{uname_r}/tools/objtool/
install -vsm 755 tools/objtool/fixdep %{buildroot}%{_usrsrc}/%{name}-headers-%{uname_r}/tools/objtool/
%endif

# copy .config manually to be where it's expected to be
cp .config %{buildroot}%{_usrsrc}/%{name}-headers-%{uname_r}
ln -sf "%{_usrsrc}/%{name}-headers-%{uname_r}" "%{buildroot}%{_modulesdir}/build"
find %{buildroot}/lib/modules -name '*.ko' -print0 | xargs -0 chmod u+x

%ifarch aarch64
cp arch/arm64/kernel/module.lds \
        %{buildroot}%{_usrsrc}/%{name}-headers-%{uname_r}/arch/arm64/kernel/
%endif

# disable (JOBS=1) parallel build to fix this issue:
# fixdep: error opening depfile: ./.plugin_cfg80211.o.d: No such file or directory
# Linux version that was affected is 4.4.26
make -C tools JOBS=1 DESTDIR=%{buildroot} prefix=%{_prefix} \
        perf_install PYTHON=python3 %{?_smp_mflags}

make -C tools/perf ARCH=%{?arch} JOBS=1 DESTDIR=%{buildroot} \
        prefix=%{_prefix} PYTHON=python3 \
        install-python_ext %{?_smp_mflags}

%ifarch x86_64
make -C tools ARCH=%{?arch} JOBS=1 DESTDIR=%{buildroot} \
        prefix=%{_prefix} mandir=%{_mandir} \
        turbostat_install cpupower_install \
        PYTHON=python3 %{?_smp_mflags}
%endif

%include %{SOURCE2}
%include %{SOURCE6}

%post
/sbin/depmod -a %{uname_r}
ln -sf %{name}-%{uname_r}.cfg /boot/photon.cfg

%post hmacgen
/sbin/depmod -a %{uname_r}

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
/boot/.vmlinuz-%{uname_r}.hmac
%config(noreplace) /boot/%{name}-%{uname_r}.cfg
%config %{_sharedstatedir}/initramfs/kernel/%{uname_r}
%defattr(0644,root,root)
%{_modulesdir}/*
%exclude %{_modulesdir}/build
%exclude %{_modulesdir}/kernel/drivers/gpu
%exclude %{_modulesdir}/kernel/sound
%exclude %{_modulesdir}/extra/hmac_generator.ko.xz
%exclude %{_modulesdir}/extra/.hmac_generator.ko.xz.hmac

%ifarch aarch64
%exclude %{_modulesdir}/kernel/drivers/staging/vc04_services/bcm2835-audio
%endif

%ifarch x86_64
%exclude %{_modulesdir}/kernel/arch/x86/oprofile/
%exclude %{_modulesdir}/extra/intel_sgx.ko.xz
%{_sysconfdir}/modprobe.d/iavf.conf
# ICE driver firmware files are packaged in linux-firmware
%exclude /lib/firmware/updates/intel/ice
%endif

%files docs
%defattr(-,root,root)
%{_defaultdocdir}/%{name}-%{uname_r}/*
# For out-of-tree Intel i40e driver.
%ifarch x86_64
%{_mandir}/*
%endif

%files devel
%defattr(-,root,root)
%{_modulesdir}/build
%{_usrsrc}/%{name}-headers-%{uname_r}

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

%files hmacgen
%defattr(-,root,root)
%{_modulesdir}/extra/hmac_generator.ko.xz
%{_modulesdir}/extra/.hmac_generator.ko.xz.hmac

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
%{_libexecdir}
%exclude %dir %{_libdir}/debug
%ifarch x86_64
%exclude %{_lib64}/traceevent
%endif
%ifarch aarch64
%exclude %{_libdir}/traceevent
%endif
%{_bindir}
%{_sysconfdir}/bash_completion.d/*
%{_datadir}/perf-core/strace/groups/file
%{_datadir}/doc/*
%{_libdir}/perf/examples/bpf/*
%{_libdir}/perf/include/bpf/*
%ifarch x86_64
%{_includedir}/cpufreq.h
%{_includedir}/cpuidle.h
%{_lib64dir}/libcpupower.so
%{_lib64dir}/libcpupower.so.*
%config(noreplace) %{_sysconfdir}/cpufreq-bench.conf
%{_sbindir}/cpufreq-bench
%{_datadir}/locale/*
%endif

%files python3-perf
%defattr(-,root,root)
%{python3_sitelib}/*

%ifarch aarch64
%files dtb-rpi3
%defattr(-,root,root)
/boot/broadcom/*

%files dtb-ls1012afrwy
%defattr(-,root,root)
/boot/dtb/fsl-ls1012a-frwy.dtb
/boot/dtb/fsl-ls1046a-rdb.dtb
%endif

%changelog
* Wed Aug 21 2024 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 4.19.320-1
- Update to version 4.19.320
* Mon Aug 05 2024 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 4.19.319-1
- Update to version 4.19.319
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
* Mon Feb 05 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 4.19.305-6
- Fix CVE-2024-1086
* Mon Feb 05 2024 Ajay Kaher <ajay.kaher@broadcom.com> 4.19.305-5
- Fix CVE-2024-0607
* Mon Feb 05 2024 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 4.19.305-4
- Fix for CVE-2023-39197
* Wed Jan 31 2024 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 4.19.305-3
- Upgrade iavf driver to 4.9.5, ice driver to 1.13.7
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
* Mon Oct 09 2023 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.295-4
- Remove patch to fix compilation issues in ice, iavf and i40e drivers
- Replace ice-1.12.6 with ice-1.12.7
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
* Tue Aug 29 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 4.19.290-3
- Fix TCP slab memory leak
* Mon Aug 14 2023 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.290-2
- Add i40e-2.23.17, iavf-4.9.1 and ice-1.12.6 driver subpackages
- Enable CONFIG_CRYPTO_XCBC
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
* Wed Jun 14 2023 Srish Srinivasan <ssrish@vmware.com> 4.19.283-4
- Fix for CVE-2023-1076 and CVE-2023-1077
* Fri Jun 02 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 4.19.283-3
- Fix for CVE-2023-1611
* Wed May 31 2023 Ankit Jain <ankitja@vmware.com> 4.19.283-2
- Add support for Intel Sapphire Rapids server CPUs to turbostat.
- Allow cpuidle subsystem to use acpi_idle driver
- when only one C-state is available
* Wed May 17 2023 Ankit Jain <ankitja@vmware.com> 4.19.283-1
- Update to version 4.19.283
* Tue Apr 18 2023 Keerthana K <keerthanak@vmware.com> 4.19.280-1
- Update to version 4.19.280
* Mon Apr 17 2023 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.277-4
- Cleanup commented patch files
* Wed Mar 29 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 4.19.277-3
- update to latest ToT vmxnet3 driver pathes
* Thu Mar 16 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 4.19.277-2
- Patch drivers to not install aux module on modules_install_no_aux
- Clean up driver installation code
* Tue Mar 14 2023 Roye Eshed <eshedr@vmware.com> 4.19.277-1
- Update to version 4.19.277
* Thu Mar 02 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 4.19.272-5
- Upgrade ice driver to 1.11.14
- Upgrade iavf driver to 4.8.2
- Upgrade i40e driver to 2.22.18
* Thu Mar 02 2023 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.272-4
- Use Photon kernel macros to simplify building i40e, iavf and ice drivers
* Tue Feb 28 2023 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.272-3
- Expose Photon kernel macros to simplify building out-of-tree drivers.
* Mon Feb 27 2023 Ajay Kaher <akaher@vmware.com> 4.19.272-2
- exclude man dir from linux-tools
* Thu Feb 16 2023 Srish Srinivasan <ssrish@vmware.com> 4.19.272-1
- Update to version 4.19.272
* Tue Feb 07 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 4.19.271-3
- Fix for CVE-2021-44879/2022-0480/CVE-2022-3061/CVE-2022-3303/CVE-2023-23454
* Mon Feb 06 2023 Alexey Makhalov <amakhalov@vmware.com> 4.19.271-2
- Implement performance over security option for RETBleed (pos=1)
* Wed Feb 01 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 4.19.271-1
- Update to version 4.19.271
* Thu Jan 05 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 4.19.269-3
- update to latest ToT vmxnet3 driver
- Include patch "vmxnet3: correctly report csum_level for encapsulated packet"
* Wed Dec 21 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.269-2
- Enable turbostat to work in the guest on VMware hypervisor.
- Add support for Intel Ice Lake server CPUs to turbostat.
* Mon Dec 19 2022 srinidhira0 <srinidhir@vmware.com> 4.19.269-1
- Update to version 4.19.269
* Thu Dec 15 2022 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 4.19.268-3
- update to latest ToT vmxnet3 driver
* Wed Dec 14 2022 Ajay Kaher <akaher@vmware.com> 4.19.268-2
- Fix: Don't use screen objects when SEV is active
* Fri Dec 09 2022 Ankit Jain <ankitja@vmware.com> 4.19.268-1
- Update to version 4.19.268
* Fri Dec 09 2022 Ankit Jain <ankitja@vmware.com> 4.19.264-7
- Distribute the tasks across affined cpus
* Tue Dec 06 2022 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 4.19.264-6
- Fix for CVE-2022-43945
* Fri Nov 25 2022 Ajay Kaher <akaher@vmware.com> 4.19.264-5
- SEV-ES: fix MMIO scratch buffer
* Mon Nov 21 2022 Ankit Jain <ankitja@vmware.com> 4.19.264-4
- Updated ice driver to v1.9.11
- Updated iavf driver to v4.5.3
* Wed Nov 16 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.264-3
- Fix IRQ affinities of i40e, iavf and ice drivers
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
* Fri Aug 05 2022 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.247-13
- Fix for CVE-2022-2586 and CVE-2022-2588
* Wed Aug 03 2022 Shreenidhi Shedi <sshedi@vmware.com> 4.19.247-12
- Scriptlets fixes and improvements
* Tue Aug 02 2022 Sharan Turlapati <sturlapati@vmware.com> 4.19.247-11
- Revert napi reschedule on rx in vmxnet3 driver
* Tue Aug 02 2022 Ankit Jain <ankitja@vmware.com> 4.19.247-10
- Fix BUG_ON for deboosted tasks
* Tue Jul 12 2022 Ankit Jain <ankitja@vmware.com> 4.19.247-9
- Backported the fix for CVE-2022-1789
* Wed Jul 06 2022 Shreenidhi Shedi <sshedi@vmware.com> 4.19.247-8
- Spec improvements
* Wed Jul 06 2022 Shreenidhi Shedi <sshedi@vmware.com> 4.19.247-7
- Add kernel as requires to hmacgen postun
* Tue Jul 05 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.247-6
- Update iavf driver to v4.4.2
- Update ice driver to v1.8.3
- .config: Enable CONFIG_NET_DEVLINK=y (ice v1.8.3 needs it).
* Thu Jun 30 2022 Ankit Jain <ankitja@vmware.com> 4.19.247-5
- Fixes panic due to nested priority inheritance
* Thu Jun 23 2022 Sharan Turlapati <sturlapati@vmware.com> 4.19.247-4
- Update vmxnet3 driver to version 7
* Wed Jun 22 2022 Sharan Turlapati <sturlapati@vmware.com> 4.19.247-3
- Update vmxnet3 driver to version 6
* Wed Jun 15 2022 Brennan Lamoreaux <blamoreaux@vmware.com> 4.19.247-2
- Enable config_livepatch.
* Tue Jun 14 2022 Ajay Kaher <akaher@vmware.com> 4.19.247-1
- Update to version 4.19.247
* Thu May 26 2022 Sharan Turlapati <sturlapati@vmware.com> 4.19.245-1
- Update to version 4.19.245
* Mon May 16 2022 Brennan Lamoreaux <blamoreaux@vmware.com> 4.19.241-2
- Fix for CVE-2022-1048
* Wed May 11 2022 Brennan Lamoreaux <blamoreaux@vmware.com> 4.19.241-1
- Update to version 4.19.241
* Wed May 11 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 4.19.240-2
- Enabling CONFIG_MITIGATE_SPECTRE_BRANCH_HISTORY
* Fri Apr 29 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 4.19.240-1
- Update to version 4.19.240
- Fix CVE-2022-1055
* Sat Mar 26 2022 Shreenidhi Shedi <sshedi@vmware.com> 4.19.232-4
- Exclude debug symbols properly
* Mon Mar 21 2022 Ajay Kaher <akaher@vmware.com> 4.19.232-3
- Fix for CVE-2022-1016
* Thu Mar 10 2022 Sharan Turlapati <sturlapati@vmware.com> 4.19.232-2
- Enable function and function_graph tracing on linux
* Mon Mar 07 2022 srinidhira0 <srinidhir@vmware.com> 4.19.232-1
- Update to version 4.19.232
* Mon Feb 28 2022 Alexey Makhalov <amakhalov@vmware.com> 4.19.229-3
- .config: enable squashfs module, enable crypto user api rng.
* Fri Feb 25 2022 Ajay Kaher <akaher@vmware.com> 4.19.229-2
- Fix sev-es exception stack mapping
* Sat Feb 12 2022 Sharan Turlapati <sturlapati@vmware.com> 4.19.229-1
- Update to version 4.19.229
* Fri Feb 11 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.225-6
- .config: Enable CONFIG_NET_ACT_SIMP
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
* Mon Dec 20 2021 srinidhira0 <srinidhir@vmware.com> 4.19.219-4
- remove lvm ,nvme and nvme-core in add-drivers list
- lvm drivers are built as part of dm-mod
* Wed Dec 15 2021 Alexey Makhalov <amakhalov@vmware.com> 4.19.219-3
- mm: fix percpu alloacion for memoryless nodes
- pvscsi: fix disk detection issue
* Tue Dec 14 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.219-2
- Fix for CVE-2020-36385
- nvme ,nvme-core are in-built modules
* Wed Dec 08 2021 srinidhira0 <srinidhir@vmware.com> 4.19.219-1
- Update to version 4.19.219
* Wed Nov 24 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.217-1
- Update to version 4.19.217
* Thu Nov 11 2021 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.214-4
- .config: Enable CONFIG_INTEL_RDT, CONFIG_USERFAULTFD, and
- CONFIG_NFT_{CHAIN_ROUTE, CHAIN_NAT, MASQ, REDIR}_IPV4.
* Fri Oct 29 2021 Srinidhi Rao <srinidhir@vmware.com> 4.19.214-3
- Add support for eBPF packet filter
* Fri Oct 29 2021 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 4.19.214-2
- Fix for CVE-2020-36322/CVE-2021-28950
* Thu Oct 28 2021 Sharan Turlapati <sturlapati@vmware.com> 4.19.214-1
- Update to version 4.19.214
* Wed Sep 29 2021 Keerthana K <keerthanak@vmware.com> 4.19.208-1
- Update to version 4.19.208
* Fri Aug 27 2021 srinidhira0 <srinidhir@vmware.com> 4.19.205-1
- Update to version 4.19.205
* Tue Aug 24 2021 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.198-4
- Add PCI quirk to allow multiple devices under the same virtual
- PCI bridge to be put into separate IOMMU groups.
* Wed Aug 18 2021 Keerthana K <keerthanak@vmware.com> 4.19.198-3
- Update ice driver to v1.6.4
- Update i40e driver to v2.15.9
- Update iavf driver to v4.2.7
* Mon Aug 16 2021 Sharan Turlapati <sturlapati@vmware.com> 4.19.198-2
- Allow PCI resets disablement from vfio_pci
* Tue Jul 27 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.198-1
- Update to version 4.19.198
* Thu Jul 15 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.191-3
- Fix for CVE-2021-33909
* Tue Jun 22 2021 Sharan Turlapati <sturlapati@vmware.com> 4.19.191-2
- Fix for CVE-2021-3609
* Thu Jun 03 2021 Keerthana K <keerthanak@vmware.com> 4.19.191-1
- Update to version 4.19.191
- Remove XR usb driver support
- .config: Enable CONFIG_FANOTIFY_ACCESS_PERMISSIONS
* Wed Jun 02 2021 Keerthana K <keerthanak@vmware.com> 4.19.190-3
- Fix for CVE-2021-3573
* Thu May 20 2021 Ajay Kaher <akaher@vmware.com> 4.19.190-2
- Fix for CVE-2021-3564
* Mon May 17 2021 Ajay Kaher <akaher@vmware.com> 4.19.190-1
- Update to version 4.19.190
* Wed May 12 2021 Sharan Turlapati <sturlapati@vmware.com> 4.19.189-5
- Fix for CVE-2021-23133
* Mon May 10 2021 Ajay Kaher <akaher@vmware.com> 4.19.189-4
- SEV-ES: update SWIOTLB bounce buffer patch
* Fri May 07 2021 Ankit Jain <ankitja@vmware.com> 4.19.189-3
- .config: Enable MLX5_INFINIBAND
* Tue May 04 2021 Sharan Turlapati <sturlapati@vmware.com> 4.19.189-2
- Remove buf_info from device accessible structures in vmxnet3
* Thu Apr 29 2021 Ankit Jain <ankitja@vmware.com> 4.19.189-1
- Update to version 4.19.189
* Tue Apr 20 2021 Ankit Jain <ankitja@vmware.com> 4.19.186-4
- Fix for CVE-2021-3444
* Mon Apr 19 2021 Ajay Kaher <akaher@vmware.com> 4.19.186-3
- Fixes for SEV-ES
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
* Wed Mar 03 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.177-2
- Update iavf driver to v4.0.2
* Fri Feb 26 2021 Sharan Turlapati <sturlapati@vmware.com> 4.19.177-1
- Update to version 4.19.177
* Fri Feb 19 2021 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.174-5
- Fix /boot/photon.cfg symlink when /boot is a separate partition.
* Thu Feb 11 2021 Ajay Kaher <akaher@vmware.com> 4.19.174-4
- sev-es: security fixes
* Thu Feb 11 2021 Ankit Jain <ankitja@vmware.com> 4.19.174-3
- Added latest out of tree version of Intel ice driver
* Thu Feb 11 2021 Ajay Kaher <akaher@vmware.com> 4.19.174-2
- Enable CONFIG_WDAT_WDT
* Tue Feb 09 2021 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.174-1
- Update to version 4.19.174
* Thu Jan 07 2021 Alexey Makhalov <amakhalov@vmware.com> 4.19.164-2
- Avoid TSC recalibration
* Mon Jan 04 2021 Ankit Jain <ankitja@vmware.com> 4.19.164-1
- Update to version 4.19.164
* Mon Dec 21 2020 Ajay Kaher <akaher@vmware.com> 4.19.163-2
- Fix for CVE-2020-29569
* Tue Dec 15 2020 Vikash Bansal <bvikas@vmware.com> 4.19.163-1
- Update to version 4.19.163
* Fri Dec 11 2020 Ajay Kaher <akaher@vmware.com> 4.19.160-6
- Adding sev-es: patch set v3
- x86/efi,boot: GDT handling cleanup/fixes
* Thu Dec 10 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.160-5
- Add latest out of tree version of iavf driver
- Enable CONFIG_NET_TEAM
* Wed Dec 09 2020 Srinidhi Rao <srinidhir@vmware.com> 4.19.160-4
- Fix for CVE-2019-19770
* Tue Dec 08 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.160-3
- Change PTP_SYS_OFFSET_EXTENDED IOCTL to _IOWR
* Tue Dec 08 2020 Ankit Jain <ankitja@vmware.com> 4.19.160-2
- Enable CONFIG_NET_VENDOR_AMAZON and CONFIG_ENA_ETHERNET
- to add support for ami in arm in linux generic
- Added nvme and nvme-core to initrd modules
* Wed Dec 02 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.160-1
- Update to version 4.19.160
- Fix CVE-2019-19338
* Tue Dec 01 2020 Vikash Bansal <bvikas@vmware.com> 4.19.154-11
- Fix issue with lockdown patch
* Fri Nov 20 2020 Ajay Kaher <akaher@vmware.com> 4.19.154-10
- floppy: lower printk message priority
* Mon Nov 16 2020 Vikash Bansal <bvikas@vmware.com> 4.19.154-9
- hmacgen: Add path_put to hmac_gen_hash
* Fri Nov 13 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.154-8
- Fix CVE-2020-25668
* Thu Nov 12 2020 Sharan Turlapati <sturlapati@vmware.com> 4.19.154-7
- Enable CONFIG_IFB
* Wed Nov 11 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.154-6
- Add support for PTP_SYS_OFFSET_EXTENDED ioctl
- Update i40e out-of-tree driver to version 2.13.10
* Wed Nov 11 2020 Albert Guo <aguo@vmware.com> 4.19.154-5
- 9P: Ensure seekdir work correctly when readdir hasn't reached eof
- 9P: [VDFS]Initialize fid->iounit during creation of p9_fid
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
* Mon Oct 12 2020 Ajay Kaher <akaher@vmware.com> 4.19.148-5
- Fix for CVE-2020-16120
* Mon Oct 12 2020 Ankit Jain <ankitja@vmware.com> 4.19.148-4
- Fix for CVE-2020-16119
* Wed Oct 07 2020 Ajay Kaher <akaher@vmware.com> 4.19.148-3
- Fix mp_irqdomain_activate crash
* Mon Oct 05 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.148-2
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
* Wed Sep 09 2020 Sharan Turlapati <sturlapati@vmware.com> 4.19.138-4
- Remove traceevent/plugins from linux-tools
* Mon Sep 07 2020 Vikash Bansal <bvikas@vmware.com> 4.19.138-3
- Fix for CVE-2020-14386
* Wed Aug 12 2020 Alexey Makhalov <amakhalov@vmware.com> 4.19.138-2
- .config: support for floppy disk and ch341 usb to serial
* Sat Aug 08 2020 ashwin-h <ashwinh@vmware.com> 4.19.138-1
- Update to version 4.19.138
* Thu Aug 06 2020 Sharan Turlapati <sturlapati@vmware.com> 4.19.132-6
- Enable CONFIG_TCP_CONG_BBR
* Tue Aug 04 2020 Alexey Makhalov <amakhalov@vmware.com> 4.19.132-5
- Inherit TSQ limit from root namespace
* Tue Aug 04 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.132-4
- Upgrade vmxnet3 driver to version 4
* Mon Jul 27 2020 Alexey Makhalov <amakhalov@vmware.com> 4.19.132-3
- Lockdown support
* Sun Jul 26 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.132-2
- Fix CVE-2020-14331
* Thu Jul 16 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.132-1
- Update to version 4.19.132
* Thu Jul 16 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.129-3
- Add latest out of tree version of i40e driver
* Sat Jun 27 2020 Alexey Makhalov <amakhalov@vmware.com> 4.19.129-2
- .config: add zram module
* Sat Jun 27 2020 Keerthana K <keerthanak@vmware.com> 4.19.129-1
- Update to version 4.19.129
* Tue Jun 23 2020 Ajay Kaher <akaher@vmware.com> 4.19.126-4
- Fix for CVE-2020-12888
* Mon Jun 15 2020 Alexey Makhalov <amakhalov@vmware.com> 4.19.126-3
- Add intel_sgx module (-drivers-intel-sgx subpackage)
* Wed Jun 10 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.126-2
- Enable CONFIG_VFIO_NOIOMMU
* Fri Jun 05 2020 Vikash Bansal <bvikas@vmware.com> 4.19.126-1
- Update to version 4.19.126
* Thu Jun 04 2020 Ajay Kaher <akaher@vmware.com> 4.19.124-2
- Fix for CVE-2020-10757
* Thu May 28 2020 Ajay Kaher <akaher@vmware.com> 4.19.124-1
- Update to version 4.19.124
* Thu May 28 2020 Shreenidhi Shedi <sshedi@vmware.com> 4.19.115-10
- Keep modules of running kernel till next boot
* Thu May 28 2020 Tapas Kundu <tkundu@vmware.com> 4.19.115-9
- Added linux-python3-perf subpackage.
- Added turbostat and cpupower to tools for x86_64.
* Fri May 22 2020 Ashwin H <ashwinh@vmware.com> 4.19.115-8
- Fix for CVE-2018-20669
* Fri May 15 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.115-7
- Add uio_pic_generic driver support in config
* Fri May 15 2020 Vikash Bansal <bvikas@vmware.com> 4.19.115-6
- Fix for CVE-2019-18885
* Tue May 12 2020 Siddharth Chandrasekaran <csiddharth@vmware.com> 4.19.115-5
- Add patch to fix CVE-2020-10711
* Wed May 06 2020 Ajay Kaher <akaher@vmware.com> 4.19.115-4
- Adding vmwgfx patches to support sev-es
* Wed Apr 29 2020 Keerthana K <keerthanak@vmware.com> 4.19.115-3
- Photon-cheksum-generator version update to 1.1.
* Wed Apr 29 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.115-2
- Enable additional config options.
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
* Tue Jan 14 2020 Srinidhi Rao <srinidhir@vmware.com> 4.19.87-5
- Enable DRBG HASH and DRBG CTR support.
* Wed Jan 08 2020 Ajay Kaher <akaher@vmware.com> 4.19.87-4
- Enabled configs RTC_DRV_PL030, RTC_DRV_PL031
* Thu Jan 02 2020 Keerthana K <keerthanak@vmware.com> 4.19.87-3
- Modify tcrypt to remove tests for algorithms that are not supported in photon.
- Added tests for DH, DRBG algorithms.
* Fri Dec 20 2019 Keerthana K <keerthanak@vmware.com> 4.19.87-2
- Update fips Kat tests patch.
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
* Thu Oct 17 2019 Ajay Kaher <akaher@vmware.com> 4.19.79-1
- Update to version 4.19.79
- Fix CVE-2019-17133
* Mon Oct 14 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.76-5
- Add megaraid_sas driver to initramfs
* Mon Oct 14 2019 Harinadh D <hdommaraju@vmware.com> 4.19.76-4
- Adding lvm and dm-mod modules to support root as lvm
* Fri Oct 11 2019 Bo Gan <ganb@vmware.com> 4.19.76-3
- Enable IMA with SHA256 as default hash algorithm
* Thu Oct 10 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.76-2
- Add additional BuildRequires and Requires to fix issues with perf, related to
- interactive UI and C++ symbol demangling. Also update the last few perf python
- scripts in Linux kernel to use python3 syntax.
* Wed Oct 02 2019 Ajay Kaher <akaher@vmware.com> 4.19.76-1
- Update to version 4.19.76
- Enable USB_SERIAL_PL2303 for aarch64
* Thu Sep 19 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.72-2
- Avoid oldconfig which leads to potential build hang
- Fix archdir usage
* Wed Sep 11 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.72-1
- Update to version 4.19.72
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
* Tue Jul 02 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.52-4
- Fix 9p vsock 16bit port issue.
* Thu Jun 27 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.52-3
- Deprecate linux-aws-tools in favor of linux-tools.
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
- Enable Kernel Address Space Layout Randomization.
- Enable CONFIG_SECURITY_NETWORK_XFRM
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
