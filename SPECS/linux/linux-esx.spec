%global security_hardening none
%global photon_checksum_generator_version 1.2
Summary:        Kernel
Name:           linux-esx
Version:        4.19.208
Release:        1%{?kat_build:.kat}%{?dist}
License:        GPLv2
URL:            http://www.kernel.org/
Group:          System Environment/Kernel
Vendor:         VMware, Inc.
Distribution:   Photon

%define uname_r %{version}-%{release}-esx

Source0:        http://www.kernel.org/pub/linux/kernel/v4.x/linux-%{version}.tar.xz
%define sha1 linux=2bd7234fd0085d2144b97115780bf38b451ba735
Source1:        config-esx
Source2:        initramfs.trigger
Source3:        pre-preun-postun-tasks.inc
Source4:        check_for_config_applicability.inc
# Photon-checksum-generator kernel module
Source5:        https://github.com/vmware/photon-checksum-generator/releases/photon-checksum-generator-%{photon_checksum_generator_version}.tar.gz
%define sha1 photon-checksum-generator=20658a922c0beca840942bf27d743955711c043a
Source6:        genhmac.inc
%define i40e_version 2.16.11
Source7:       https://sourceforge.net/projects/e1000/files/i40e%20stable/%{i40e_version}/i40e-%{i40e_version}.tar.gz
%define sha1 i40e=8fbfb9d0bf8feec0c74a5dc150613b430921fdcd
%define ice_version 1.6.4
Source8:       https://sourceforge.net/projects/e1000/files/ice%20stable/%{ice_version}/ice-%{ice_version}.tar.gz
%define sha1 ice=9e860bf3cafcabd1d4897e87e749334f73828bad

# common
Patch0:         linux-4.14-Log-kmsg-dump-on-panic.patch
Patch1:         double-tcp_mem-limits.patch
# TODO: disable this patch, check for regressions
#Patch2:         linux-4.9-watchdog-Disable-watchdog-on-virtual-machines.patch
Patch3:         SUNRPC-Do-not-reuse-srcport-for-TIME_WAIT-socket.patch
Patch4:         SUNRPC-xs_bind-uses-ip_local_reserved_ports.patch
Patch5:         vsock-transport-for-9p.patch
Patch6:         4.18-x86-vmware-STA-support.patch
Patch7:	        9p-trans_fd-extend-port-variable-to-u32.patch
Patch8:         init-do_mounts-recreate-dev-root.patch
Patch9:         vsock-delay-detach-of-QP-with-outgoing-data.patch
Patch10:        9p-file-attributes-caching-support.patch

# -esx
Patch11:        fs-9p-support-for-local-file-lock.patch
Patch12:        serial-8250-do-not-probe-U6-16550A-fifo-size.patch

# floppy:
Patch17:        0001-floppy-lower-printk-message-priority.patch

Patch28:        0001-Control-MEMCG_KMEM-config.patch
Patch29:        0001-cgroup-v1-cgroup_stat-support.patch
Patch30:        4.18-add-sysctl-to-disallow-unprivileged-CLONE_NEWUSER-by-default.patch

# Fix CVE-2017-1000252
Patch31:        kvm-dont-accept-wrong-gsi-values.patch
# RDRAND-based RNG driver to enhance the kernel's entropy pool:
Patch32:        4.18-0001-hwrng-rdrand-Add-RNG-driver-based-on-x86-rdrand-inst.patch
# Out-of-tree patches from AppArmor:
Patch33:        4.17-0001-apparmor-patch-to-provide-compatibility-with-v2.x-ne.patch
Patch34:        4.17-0002-apparmor-af_unix-mediation.patch
Patch35:        4.17-0003-apparmor-fix-use-after-free-in-sk_peer_label.patch
# Fix for CVE-2019-12456
Patch36:        0001-scsi-mpt3sas_ctl-fix-double-fetch-bug-in-_ctl_ioctl_.patch
# Fix for CVE-2019-12379
Patch37:        0001-consolemap-Fix-a-memory-leaking-bug-in-drivers-tty-v.patch
# Fix for CVE-2019-12380
Patch38:        0001-efi-x86-Add-missing-error-handling-to-old_memmap-1-1.patch
# Fix for CVE-2019-12381
Patch39:        0001-ip_sockglue-Fix-missing-check-bug-in-ip_ra_control.patch
# Fix for CVE-2019-12378
Patch40:        0001-ipv6_sockglue-Fix-a-missing-check-bug-in-ip6_ra_cont.patch
# Fix for CVE-2019-12455
Patch41:        0001-clk-sunxi-fix-a-missing-check-bug-in-sunxi_divs_clk_.patch
Patch42:        0001-Remove-OOM_SCORE_ADJ_MAX-limit-check.patch
#Fix for CVE-2019-20908
Patch43:        efi-Restrict-efivar_ssdt_load-when-the-kernel-is-locked-down.patch
#Fix for CVE-2019-19338
Patch44:        0001-KVM-vmx-implement-MSR_IA32_TSX_CTRL-disable-RTM-func.patch
Patch45:        0001-KVM-vmx-use-MSR_IA32_TSX_CTRL-to-hard-disable-TSX-on.patch

# Fix for CVE-2019-19770
Patch46:        0001-block-revert-back-to-synchronous-request_queue-remov.patch
Patch47:        0002-block-create-the-request_queue-debugfs_dir-on-regist.patch

# 9p patches
Patch54:        0001-fs-9p-Add-opt_metaonly-option.patch
Patch55:        0001-p9fs_dir_readdir-offset-support.patch
Patch56:	0002-Add-9p-zero-copy-data-path-using-crossfd.patch
Patch57:	0003-Enable-cache-loose-for-vdfs-9p.patch
Patch58:	0004-Calculate-zerocopy-pages-with-considering-buffer-ali.patch
Patch59:        0001-9p-Ensure-seekdir-take-effect-when-entries-in-readdi.patch
Patch60:        0001-9p-VDFS-Initialize-fid-iounit-during-creation-of-p9_.patch

# 9p new function iov_iter_to_pfns()
Patch61:        0001-lib-iov_iter-adding-new-function-iov_iter_to_pfns.patch
# 9p Enhance p9_client_read_dotx() and p9_client_write_dotx()
Patch62:        0001-net-9p-Enhance-p9_client_read_dotx-and-p9_client_wri.patch
# 9p improve readpages cache
Patch63:        0002-fs-9p-Add-read_cache_pages_inchunks.patch
# 9p improve write pages cache
Patch64:        0001-fs-9p-write-pages-together-if-pages-are-consecutive-.patch

# Fix for CVE-2020-16119
Patch73:        0001-dccp-ccid-move-timers-to-struct-dccp_sock.patch
Patch74:        0002-Revert-dccp-don-t-free-ccid2_hc_tx_sock-struct-in-dc.patch

#Fix for CVE-2020-16120
Patch75:        0001-ovl-pass-correct-flags-for-opening-real-directory.patch
Patch76:        0002-ovl-switch-to-mounter-creds-in-readdir.patch
Patch77:        0003-ovl-verify-permissions-in-ovl_path_open.patch
Patch78:        0004-ovl-call-secutiry-hook-in-ovl_real_ioctl.patch
Patch79:        0005-ovl-check-permission-to-open-real-file.patch

# inherit tcp_limit_output_bytes
Patch90:	tcp-inherit-TSQ-limit-from-root-namespace.patch

# Patch to add drbg_pr_ctr_aes256 test vectors to testmgr
Patch98:         0001-Add-drbg_pr_ctr_aes256-test-vectors-and-test-to-test.patch
# Patch to call drbg and dh crypto tests from tcrypt
Patch100:        0001-tcrypt-disable-tests-that-are-not-enabled-in-photon.patch
# Patch to perform continuous testing on RNG from Noise Source
Patch101:        0001-crypto-drbg-add-FIPS-140-2-CTRNG-for-noise-source.patch

# VDFS 9p recovery changes
Patch200:	0001-vdfs-9p-Initial-recovery-logic-in-9p.patch
Patch201:	0002-vdfs-9p-Add-lock-state-for-9P-fid-to-use-it-for-recovery.patch
Patch202:  	0003-vdfs-9p-Add-test-infra-to-test-9p-recovery-logic.patch
Patch203:	0004-vdfs-9p-Handle-failure-during-recovery.patch
Patch204:	0005-vdfs-9p-Adding-claim-tags-support-in-9p.patch
Patch205:	0006-vdfs-9p-xattrcreate-recovery.patch
Patch206:	0007-vdfs-9p-Fix-recovery-logic-and-cleanup-tags.patch

# VDFS 9p shared memory patches
Patch207:	0001-VDFS-9p-01-Add-shared-memory-support.patch
Patch208:	0002-VDFS-9p-2-shared-memory-support-ring-buffer-manageme.patch
Patch209:	0003-VDFS-9p-3-Add-9p-handlers-for-shared-memory-operatio.patch
Patch210:	0004-VDFS-9p-4-Add-poller-thread-for-polling-completion-r.patch
Patch211:	0005-VDFS-9p-05-Integrate-9p-IO-path-with-shared-memory.patch
Patch212:	0006-VDFS-9p-06-Add-support-for-claim-tags.patch
Patch213:	0007-VDFS-9p-07-Integrate-shared-memory-with-recovery-log.patch

# VDFS 9p changes
Patch225:      0001-9p-fscache-Don-t-use-writeback-fid-for-cache-when-en.patch
Patch226:      0001-9p-fscache-Only-fetch-attr-from-inode-cache-when-cac.patch
Patch227:      0001-9p-fscache-Make-dcache-work-with-case-insensitive-vo.patch
Patch228:      0001-9p-fscache-Ensure-consistent-blksize-is-returned-fro.patch

# VKD 9p changes
Patch250:        0001-fs-9p-support-no_icache-flag-to-disable-dentry-inode.patch
Patch251:        0001-fs-9p-add-ext9p-alias-and-implement-show_devname-for.patch
Patch252:        0001-fs-9p-fix-dirty-pages-writeback-in-v9fs_evict_inode.patch

# Upgrade vmxnet3 driver to version 4
Patch261:        0000-vmxnet3-turn-off-lro-when-rxcsum-is-disabled.patch
Patch262:        0001-vmxnet3-prepare-for-version-4-changes.patch
Patch263:        0002-vmxnet3-add-support-to-get-set-rx-flow-hash.patch
Patch264:        0003-vmxnet3-add-geneve-and-vxlan-tunnel-offload-support.patch
Patch265:        0004-vmxnet3-update-to-version-4.patch
Patch266:        0005-vmxnet3-use-correct-hdr-reference-when-packet-is-enc.patch
Patch267:        0006-vmxnet3-allow-rx-flow-hash-ops-only-when-rss-is-enab.patch
Patch268:        0007-vmxnet3-use-correct-tcp-hdr-length-when-packet-is-en.patch
Patch269:        0008-vmxnet3-fix-cksum-offload-issues-for-non-udp-tunnels.patch

Patch270:        0009-vmxnet3-Remove-buf_info-from-device-accessible-struc.patch

# Support for PTP_SYS_OFFSET_EXTENDED ioctl
Patch276:        0001-ptp-reorder-declarations-in-ptp_ioctl.patch
Patch277:        0002-ptp-add-PTP_SYS_OFFSET_EXTENDED-ioctl.patch
Patch278:        0003-ptp-deprecate-gettime64-in-favor-of-gettimex64.patch
Patch279:        0004-ptp-uapi-change-_IOW-to-IOWR-in-PTP_SYS_OFFSET_EXTEN.patch

# VMW:
Patch281:        0001-x86-vmware-Update-platform-detection-code-for-VMCALL.patch
Patch282:        0001-x86-vmware-Add-a-header-file-for-hypercall-definitio.patch
Patch283:        0001-x86-cpu-vmware-Use-the-full-form-of-INL-in-VMWARE_PO.patch
Patch284:        0001-x86-cpu-vmware-Use-the-full-form-of-INL-in-VMWARE_HY.patch
Patch285:        0001-x86-cpu-vmware-Fix-platform-detection-VMWARE_PORT-ma.patch
Patch286:        0001-x86-vmware-Steal-time-accounting-support.patch
Patch287:        0001-x86-alternatives-Add-an-ALTERNATIVE_3-macro.patch
Patch288:        0001-x86-vmware-Use-Efficient-and-Corrent-ALTERNATIVEs-fo.patch
Patch289:        0001-x86-vmware-Log-kmsg-dump-on-panic.patch
Patch290:        0006-x86-vmware-Fix-steal-time-clock-under-SEV.patch

Patch291:        0001-x86-insn-eval-Add-support-for-64-bit-kernel-mode.patch
Patch292:        0001-drm-vmwgfx-Update-the-backdoor-call-with-support-for.patch
Patch293:        0001-x86-vmware-avoid-TSC-recalibration.patch

# vmw: gfx
Patch301:        0001-drm-vmwgfx-Don-t-use-the-HB-port-if-memory-encryptio.patch
Patch302:        0002-drm-vmwgfx-Fix-the-refuse_dma-mode-when-using-guest-.patch
Patch303:        0003-drm-vmwgfx-Refuse-DMA-operation-when-SEV-encryption-.patch

# SEV-ES prerequisite: x86/efi,boot: GDT handling cleanup/fixes
Patch311:        0001-x86-boot-Save-several-bytes-in-decompressor.patch
Patch312:        0002-x86-boot-Remove-KEEP_SEGMENTS-support.patch
Patch313:        0003-efi-x86-Don-t-depend-on-firmware-GDT-layout.patch
Patch314:        0004-x86-boot-Reload-GDTR-after-copying-to-the-end-of-the.patch
Patch315:        0005-x86-boot-Clear-direction-and-interrupt-flags-in-star.patch
Patch316:        0006-efi-x86-Remove-GDT-setup-from-efi_main.patch
Patch317:        0007-x86-boot-GDT-limit-value-should-be-size-1.patch
Patch318:        0008-x86-boot-Micro-optimize-GDT-loading-instructions.patch
Patch319:        0009-x86-boot-compressed-Fix-reloading-of-GDTR-post-relocation.patch

# SEV-ES prerequisite: x86: Add guard pages to exception and interrupt stacks
Patch331:        0001-x86-dumpstack-Fix-off-by-one-errors-in-stack-identif.patch
Patch332:        0002-x86-irq-64-Remove-a-hardcoded-irq_stack_union-access.patch
Patch333:        0003-x86-irq-64-Sanitize-the-top-bottom-confusion.patch
Patch334:        0004-x86-idt-Remove-unused-macro-SISTG.patch
Patch335:        0005-x86-64-Remove-stale-CURRENT_MASK.patch
Patch336:        0006-x86-exceptions-Remove-unused-stack-defines-on-32bit.patch
Patch337:        0007-x86-exceptions-Make-IST-index-zero-based.patch
Patch338:        0008-x86-cpu_entry_area-Cleanup-setup-functions.patch
Patch339:        0009-x86-exceptions-Add-structs-for-exception-stacks.patch
Patch340:        0010-x86-cpu_entry_area-Prepare-for-IST-guard-pages.patch
Patch341:        0011-x86-cpu_entry_area-Provide-exception-stack-accessor.patch
Patch342:        0012-x86-traps-Use-cpu_entry_area-instead-of-orig_ist.patch
Patch343:        0013-x86-irq-64-Use-cpu-entry-area-instead-of-orig_ist.patch
Patch344:        0014-x86-dumpstack-64-Use-cpu_entry_area-instead-of-orig_.patch
Patch345:        0015-x86-cpu-Prepare-TSS.IST-setup-for-guard-pages.patch
Patch346:        0016-x86-cpu-Remove-orig_ist-array.patch
Patch347:        0017-x86-exceptions-Disconnect-IST-index-and-stack-order.patch
Patch348:        0018-x86-exceptions-Enable-IST-guard-pages.patch
Patch349:        0019-x86-exceptions-Split-debug-IST-stack.patch
Patch350:        0020-x86-dumpstack-64-Speedup-in_exception_stack.patch
Patch351:        0021-x86-irq-32-Define-IRQ_STACK_SIZE.patch
Patch352:        0022-x86-irq-32-Make-irq-stack-a-character-array.patch
Patch353:        0023-x86-irq-32-Rename-hard-softirq_stack-to-hard-softirq.patch
Patch354:        0024-x86-irq-64-Rename-irq_stack_ptr-to-hardirq_stack_ptr.patch
Patch355:        0025-x86-irq-32-Invoke-irq_ctx_init-from-init_IRQ.patch
Patch356:        0026-x86-irq-32-Handle-irq-stack-allocation-failure-prope.patch
Patch357:        0027-x86-irq-64-Init-hardirq_stack_ptr-during-CPU-hotplug.patch
Patch358:        0028-x86-irq-64-Split-the-IRQ-stack-into-its-own-pages.patch
Patch359:        0029-x86-irq-64-Remap-the-IRQ-stack-with-guard-pages.patch
Patch360:        0030-x86-irq-64-Remove-stack-overflow-debug-code.patch

Patch371:        0001-x86-ioremap-Add-an-ioremap_encrypted-helper.patch
Patch372:        0001-linkage-Introduce-new-macros-for-assembler-symbols.patch

# vmw_pvscsi
Patch381:        0001-scsi-vmw_pvscsi-switch-to-generic-DMA-API.patch
Patch382:        0002-scsi-vmw_pvscsi-Fix-swiotlb-operation.patch
Patch383:        0003-scsi-vmw_pvscsi-Silence-dma-mapping-errors.patch
Patch384:        0004-scsi-vmw_pvscsi-Avoid-repeated-dma-mapping-and-unmapping-of-sg-list-memory.patch
Patch385:        0005-scsi-vmw_pvscsi-Reduce-the-ring-size-when-SEV-is-active.patch
Patch386:        0006-scsi-vmw_pvscsi-Fix-uninitialized-sense-buffer-with-swiotlb.patch

# SEV-ES V3
Patch401:        0001-KVM-SVM-Add-GHCB-definitions.patch
Patch402:        0002-KVM-SVM-Add-GHCB-Accessor-functions.patch
Patch403:        0003-KVM-SVM-Use-__packed-shorthand.patch
Patch404:        0004-x86-cpufeatures-Add-SEV-ES-CPU-feature.patch
Patch405:        0005-x86-traps-Move-some-definitions-to-asm-trap_defs.h.patch
Patch406:        0006-x86-insn-Make-inat-tables.c-suitable-for-pre-decompr.patch
Patch407:        0007-x86-umip-Factor-out-instruction-fetch.patch
Patch408:        0008-x86-umip-Factor-out-instruction-decoding.patch
Patch409:        0009-x86-insn-Add-insn_get_modrm_reg_off.patch
Patch410:        0010-x86-insn-Add-insn_rep_prefix-helper.patch
Patch411:        0011-x86-boot-compressed-64-Disable-red-zone-usage.patch
Patch412:        0012-x86-boot-compressed-64-Switch-to-__KERNEL_CS-after-G.patch
Patch413:        0013-x86-boot-compressed-64-Add-IDT-Infrastructure.patch
Patch414:        0014-x86-boot-compressed-64-Rename-kaslr_64.c-to-ident_ma.patch
Patch415:        0015-x86-boot-compressed-64-Add-page-fault-handler.patch
Patch416:        0016-x86-boot-compressed-64-Always-switch-to-own-page-tab.patch
Patch417:        0017-x86-boot-compressed-64-Don-t-pre-map-memory-in-KASLR.patch
Patch418:        0018-x86-boot-compressed-64-Change-add_identity_map-to-ta.patch
Patch419:        0019-x86-boot-compressed-64-Add-VC-handler.patch
Patch420:        0020-x86-boot-compressed-64-Call-set_sev_encryption_mask.patch
Patch421:        0021-x86-boot-compressed-64-Check-return-value-of-kernel_.patch
Patch422:        0022-x86-boot-compressed-64-Add-set_page_en-decrypted-hel.patch
Patch423:        0023-x86-boot-compressed-64-Setup-GHCB-Based-VC-Exception.patch
Patch424:        0024-x86-boot-compressed-64-Unmap-GHCB-page-before-bootin.patch
Patch425:        0025-x86-sev-es-Add-support-for-handling-IOIO-exceptions.patch
Patch426:        0026-x86-fpu-Move-xgetbv-xsetbv-into-separate-header.patch
Patch427:        0027-x86-sev-es-Add-CPUID-handling-to-VC-handler.patch
Patch428:        0028-x86-idt-Move-IDT-to-data-segment.patch
Patch429:        0029-x86-idt-Split-idt_data-setup-out-of-set_intr_gate.patch
Patch430:        0030-x86-idt-Move-two-function-from-k-idt.c-to-i-a-desc.h.patch
Patch431:        0031-x86-head-64-Install-boot-GDT.patch
Patch432:        0032-x86-head-64-Reload-GDT-after-switch-to-virtual-addre.patch
Patch433:        0033-x86-head-64-Load-segment-registers-earlier.patch
Patch434:        0034-x86-head-64-Switch-to-initial-stack-earlier.patch
Patch435:        0035-x86-head-64-Build-k-head64.c-with-fno-stack-protecto.patch
Patch436:        0036-x86-head-64-Load-IDT-earlier.patch
Patch437:        0037-x86-head-64-Move-early-exception-dispatch-to-C-code.patch
Patch438:        0038-x86-sev-es-Add-SEV-ES-Feature-Detection.patch
Patch439:        0039-x86-sev-es-Print-SEV-ES-info-into-kernel-log.patch
Patch440:        0040-x86-sev-es-Compile-early-handler-code-into-kernel-im.patch
Patch441:        0041-x86-sev-es-Setup-early-VC-handler.patch
Patch442:        0042-x86-sev-es-Setup-GHCB-based-boot-VC-handler.patch
Patch443:        0043-x86-sev-es-Setup-per-cpu-GHCBs-for-the-runtime-handl.patch
Patch444:        0044-x86-sev-es-Allocate-and-Map-IST-stacks-for-VC-handle.patch
Patch445:        0045-x86-dumpstack-64-Handle-VC-exception-stacks.patch
Patch446:        0046-x86-sev-es-Shift-VC-IST-Stack-in-nmi_enter-nmi_exit.patch
Patch447:        0047-x86-sev-es-Add-Runtime-VC-Exception-Handler.patch
Patch448:        0048-x86-sev-es-Wire-up-existing-VC-exit-code-handlers.patch
Patch449:        0049-x86-sev-es-Handle-instruction-fetches-from-user-spac.patch
Patch450:        0050-x86-sev-es-Do-not-crash-on-VC-exceptions-from-user-s.patch
Patch451:        0051-x86-sev-es-Handle-MMIO-events.patch
Patch452:        0052-x86-sev-es-Handle-MMIO-String-Instructions.patch
Patch453:        0053-x86-sev-es-Handle-MSR-events.patch
Patch454:        0054-x86-sev-es-Handle-DR7-read-write-events.patch
Patch455:        0055-x86-sev-es-Handle-WBINVD-Events.patch
Patch456:        0056-x86-sev-es-Handle-RDTSC-P-Events.patch
Patch457:        0057-x86-sev-es-Handle-RDPMC-Events.patch
Patch458:        0058-x86-sev-es-Handle-INVD-Events.patch
Patch459:        0059-x86-sev-es-Handle-MONITOR-MONITORX-Events.patch
Patch460:        0060-x86-sev-es-Handle-MWAIT-MWAITX-Events.patch
Patch461:        0061-x86-sev-es-Handle-VMMCALL-Events.patch
Patch462:        0062-x86-sev-es-Handle-AC-Events.patch
Patch463:        0063-x86-sev-es-Handle-DB-Events.patch
Patch464:        0064-x86-sev-es-Cache-CPUID-results-for-improved-performa.patch
Patch465:        0065-x86-paravirt-Allow-hypervisor-specific-VMMCALL-handl.patch
Patch466:        0066-x86-kvm-Add-KVM-specific-VMMCALL-handling-under-SEV.patch
Patch467:        0067-x86-vmware-Add-VMware-specific-handling-for-VMMCALL.patch
Patch468:        0068-x86-realmode-Add-SEV-ES-specific-trampoline-entry-po.patch
Patch469:        0069-x86-realmode-Setup-AP-jump-table.patch
Patch470:        0070-x86-head-64-Setup-TSS-early-for-secondary-CPUs.patch
Patch471:        0071-x86-head-64-Don-t-call-verify_cpu-on-starting-APs.patch
Patch472:        0072-x86-head-64-Rename-start_cpu0.patch
Patch473:        0073-x86-sev-es-Support-CPU-offline-online.patch
Patch474:        0074-x86-sev-es-Handle-NMI-State.patch
Patch475:        0075-x86-efi-Add-GHCB-mappings-when-SEV-ES-is-active.patch
Patch476:        0001-x86-sev-es-Fix-crash-in-early_set_memory_enc_dec.patch
Patch477:        0001-x86-sev-es-Fix-attempt-to-move-org-backwards-error.patch
Patch478:        0001-swiotlb-Adjust-SWIOTBL-bounce-buffer-size-for-SEV-gu.patch

Patch480:        0001-x86-traps-Split-trap-numbers-out-in-a-separate-heade.patch
Patch481:        0079-x86-sev-es-Disable-BIOS-ACPI-RSDP-probing-if-SEV-ES-.patch
Patch482:        0080-x86-boot-Enable-vmw-serial-port-via-Super-I-O.patch
Patch483:        0081-x86-sev-es-Disable-use-of-WP-via-PAT-for-__sme_early.patch
Patch484:        0082-x86-sev-es-load-idt-before-entering-long-mode-to-han.patch
Patch485:        0001-x86-boot-64-Explicitly-map-boot_params-and-command-l.patch

# SEV-ES: Security Mitigate
Patch491:        0001-x86-boot-compressed-64-Introduce-sev_status.patch
Patch492:        0002-x86-boot-compressed-64-Sanity-check-CPUID-results-in.patch
Patch493:        0003-x86-boot-compressed-64-Check-SEV-encryption-in-64-bi.patch
Patch494:        0004-x86-head-64-Check-SEV-encryption-before-switching-to.patch
Patch495:        0005-x86-sev-es-Do-not-support-MMIO-to-from-encrypted-mem.patch
Patch496:        x86-sev-es-Do-not-unroll-string-IO-for-SEV-ES-guests.patch
Patch497:        x86-sev-es-Handle-string-port-IO-to-kernel-memory-properly.patch

# esx
Patch501:        01-clear-linux.patch
Patch502:        02-pci-probe.patch
Patch503:        03-poweroff.patch
Patch504:        04-quiet-boot.patch
Patch505:        05-pv-ops-clocksource.patch
Patch506:        06-pv-ops-boot_clock.patch
Patch507:        07-vmware-only.patch
Patch508:        initramfs-support-for-page-aligned-format-newca.patch
Patch509:        enabling-configuring-options-for-geneve-device.patch
Patch510:        initramfs-multiple-image-extraction-support.patch
Patch511:        halt-on-panic.patch
Patch512:        x86-setup-remove-redundant-mem-size-check.patch
Patch513:        0001-fs-A-new-VTARFS-file-system-to-mount-VTAR-archive.patch
Patch514:        initramfs-Introduce-kernel-panic-on-initramfs-unpack.patch
Patch515:        support-selective-freeing-of-initramfs-images.patch
Patch516:        initramfs-large-files-support-for-newca-format.patch

# Patches for i40e driver
Patch801:        0001-Add-support-for-gettimex64-interface.patch

# Patches for ice driver
Patch802:        0001-ice-Use-PTP_SYS_OFFSET_EXTENDED_IOCTL-support.patch

# ptp_vmw
Patch811:        0001-ptp-add-VMware-virtual-PTP-clock-driver.patch
Patch812:        0002-ptp-ptp_vmw-Implement-PTP-clock-adjustments-ops.patch
Patch813:        0003-ptp-ptp_vmw-Add-module-param-to-probe-device-using-h.patch

%if 0%{?kat_build:1}
Patch1000:      fips-kat-tests.patch
%endif

BuildArch:     x86_64
BuildRequires: bc
BuildRequires: kbd
BuildRequires: kmod-devel
BuildRequires: glib-devel
BuildRequires: xerces-c-devel
BuildRequires: xml-security-c-devel
BuildRequires: libdnet-devel
BuildRequires: libmspack-devel
BuildRequires: Linux-PAM-devel
BuildRequires: openssl-devel
BuildRequires: procps-ng-devel
BuildRequires: lz4
Requires:      filesystem kmod
Requires(pre): (coreutils or toybox)
Requires(preun): (coreutils or toybox)
Requires(post): (coreutils or toybox)
Requires(postun): (coreutils or toybox)

%description
The Linux kernel build for GOS for VMware hypervisor.

%package devel
Summary:       Kernel Dev
Group:         System Environment/Kernel
Requires:      python2 gawk
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
Summary:	HMAC SHA256/HMAC SHA512 generator
Group:		System Environment/Kernel
Requires:      %{name} = %{version}-%{release}
Enhances:        %{name}
%description hmacgen
This Linux package contains hmac sha generator kernel module.

%prep
# Using autosetup is not feasible
%setup -q -n linux-%{version}
# Using autosetup is not feasible
%setup -D -b 5 -n linux-%{version}
# Using autosetup is not feasible
%setup -D -b 7 -n linux-%{version}
# Using autosetup is not feasible
%setup -D -b 8 -n linux-%{version}

%patch1 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch17 -p1
%patch28 -p1
%patch29 -p1
%patch30 -p1
%patch31 -p1
%patch32 -p1
%patch33 -p1
%patch34 -p1
%patch35 -p1
%patch36 -p1
%patch37 -p1
%patch38 -p1
%patch39 -p1
%patch40 -p1
%patch41 -p1
%patch42 -p1
%patch43 -p1
%patch44 -p1
%patch45 -p1
%patch46 -p1
%patch47 -p1
%patch54 -p1
%patch55 -p1
%patch56 -p1
%patch57 -p1
%patch58 -p1
%patch59 -p1
%patch60 -p1
%patch61 -p1
%patch62 -p1
%patch63 -p1
%patch64 -p1
%patch73 -p1
%patch74 -p1
%patch75 -p1
%patch76 -p1
%patch77 -p1
%patch78 -p1
%patch79 -p1

%patch90 -p1
%patch98 -p1
%patch100 -p1
%patch101 -p1
%patch200 -p1
%patch201 -p1
%patch202 -p1
%patch203 -p1
%patch204 -p1
%patch205 -p1
%patch206 -p1
%patch207 -p1
%patch208 -p1
%patch209 -p1
%patch210 -p1
%patch211 -p1
%patch212 -p1
%patch213 -p1

%patch225 -p1
%patch226 -p1
%patch227 -p1
%patch228 -p1
%patch250 -p1
%patch251 -p1
%patch252 -p1

%patch261 -p1
%patch262 -p1
%patch263 -p1
%patch264 -p1
%patch265 -p1
%patch266 -p1
%patch267 -p1
%patch268 -p1
%patch269 -p1

%patch270 -p1

%patch276 -p1
%patch277 -p1
%patch278 -p1
%patch279 -p1

%patch281 -p1
%patch282 -p1
%patch283 -p1
%patch284 -p1
%patch285 -p1
%patch286 -p1
%patch287 -p1
%patch288 -p1
%patch289 -p1
%patch290 -p1
%patch291 -p1
%patch292 -p1
%patch293 -p1

%patch301 -p1
%patch302 -p1
%patch303 -p1
%patch311 -p1
%patch312 -p1
%patch313 -p1
%patch314 -p1
%patch315 -p1
%patch316 -p1
%patch317 -p1
%patch318 -p1
%patch319 -p1

%patch331 -p1
%patch332 -p1

%patch333 -p1
%patch334 -p1
%patch335 -p1
%patch336 -p1
%patch337 -p1
%patch338 -p1
%patch339 -p1
%patch340 -p1
%patch341 -p1
%patch342 -p1
%patch343 -p1
%patch344 -p1
%patch345 -p1
%patch346 -p1
%patch347 -p1
%patch348 -p1
%patch349 -p1
%patch350 -p1
%patch351 -p1
%patch352 -p1
%patch353 -p1
%patch354 -p1
%patch355 -p1
%patch356 -p1
%patch357 -p1
%patch358 -p1
%patch359 -p1
%patch360 -p1

%patch371 -p1
%patch372 -p1
%patch381 -p1
%patch382 -p1
%patch383 -p1
%patch384 -p1
%patch385 -p1
%patch386 -p1

%patch401 -p1
%patch402 -p1
%patch403 -p1
%patch404 -p1
%patch405 -p1
%patch406 -p1
%patch407 -p1
%patch408 -p1
%patch409 -p1
%patch410 -p1
%patch411 -p1
%patch412 -p1
%patch413 -p1
%patch414 -p1
%patch415 -p1

%patch416 -p1
%patch417 -p1
%patch418 -p1
%patch419 -p1
%patch420 -p1
%patch421 -p1
%patch422 -p1
%patch423 -p1
%patch424 -p1
%patch425 -p1
%patch426 -p1
%patch427 -p1
%patch428 -p1
%patch429 -p1
%patch430 -p1
%patch431 -p1
%patch432 -p1
%patch433 -p1
%patch434 -p1
%patch435 -p1
%patch436 -p1
%patch437 -p1
%patch438 -p1
%patch439 -p1
%patch440 -p1
%patch441 -p1
%patch442 -p1
%patch443 -p1
%patch444 -p1
%patch445 -p1
%patch446 -p1
%patch447 -p1
%patch448 -p1
%patch449 -p1
%patch450 -p1
%patch451 -p1
%patch452 -p1
%patch453 -p1
%patch454 -p1
%patch455 -p1
%patch456 -p1
%patch457 -p1
%patch458 -p1
%patch459 -p1
%patch460 -p1
%patch461 -p1
%patch462 -p1
%patch463 -p1
%patch465 -p1
%patch466 -p1
%patch467 -p1
%patch468 -p1
%patch469 -p1
%patch470 -p1
%patch471 -p1
%patch472 -p1
%patch473 -p1
%patch474 -p1
%patch475 -p1
%patch476 -p1
%patch477 -p1
%patch478 -p1

%patch480 -p1
%patch482 -p1
%patch483 -p1
%patch484 -p1
%patch485 -p1

# SEV-ES: Security Mitigate
%patch491 -p1
%patch492 -p1
%patch493 -p1
%patch494 -p1
%patch495 -p1
%patch496 -p1
%patch497 -p1

# esx
%patch501 -p1
%patch502 -p1
%patch503 -p1
%patch504 -p1
%patch505 -p1
%patch506 -p1
%patch507 -p1
%patch508 -p1
%patch509 -p1
%patch510 -p1
%patch511 -p1
%patch512 -p1
%patch513 -p1
%patch514 -p1
%patch515 -p1
%patch516 -p1

# Patches for i40e driver
pushd ../i40e-%{i40e_version}
%patch801 -p1
popd

# Patches for ice driver
pushd ../ice-%{ice_version}
%patch802 -p1
popd

# Patches for ptp_vmw driver
%patch811 -p1
%patch812 -p1
%patch813 -p1

%if 0%{?kat_build:1}
%patch1000 -p1
%endif

%build
# patch vmw_balloon driver
sed -i 's/module_init/late_initcall/' drivers/misc/vmw_balloon.c

# make doesn't support _smp_mflags
make mrproper
cp %{SOURCE1} .config
sed -i 's/CONFIG_LOCALVERSION="-esx"/CONFIG_LOCALVERSION="-%{release}-esx"/' .config

%include %{SOURCE4}

make VERBOSE=1 KBUILD_BUILD_VERSION="1-photon" KBUILD_BUILD_HOST="photon" ARCH="x86_64" %{?_smp_mflags}

# build i40e module
bldroot=`pwd`
pushd ../i40e-%{i40e_version}
# make doesn't support _smp_mflags
make -C src KSRC=$bldroot clean
make -C src KSRC=$bldroot %{?_smp_mflags}
popd

# build ice module
bldroot=`pwd`
pushd ../ice-%{ice_version}
# make doesn't support _smp_mflags
make -C src KSRC=$bldroot clean
make -C src KSRC=$bldroot %{?_smp_mflags}
popd

#build photon-checksum-generator module
bldroot=`pwd`
pushd ../photon-checksum-generator-%{photon_checksum_generator_version}/kernel
make -C $bldroot M=`pwd` modules %{?_smp_mflags}
popd

# Do not compress modules which will be loaded at boot time
# to speed up boot process
%define __modules_install_post \
    for MODULE in `find %{buildroot}/lib/modules/%{uname_r}/kernel/crypto -name *.ko` ; do \
        ./scripts/sign-file sha512 certs/signing_key.pem certs/signing_key.x509 $MODULE \
        rm -f $MODULE.{sig,dig} \
    done \
    find %{buildroot}/lib/modules/%{uname_r} -name "*.ko" \! \"(" -name "*evdev*" -o -name "*mousedev*" -o -name "*sr_mod*"  -o -name "*cdrom*" -o -name "*vmwgfx*" -o -name "*drm_kms_helper*" -o -name "*ttm*" -o -name "*psmouse*" -o -name "*drm*" -o -name "*apa_piix*" -o -name "*vmxnet3*" -o -name "*i2c_core*" -o -name "*libata*" -o -name "*processor*" -o -path "*ipv6*" \")" | xargs xz \
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
install -vdm 755 %{buildroot}%{_defaultdocdir}/linux-%{uname_r}
install -vdm 755 %{buildroot}/etc/modprobe.d
install -vdm 755 %{buildroot}/usr/src/linux-headers-%{uname_r}
make INSTALL_MOD_PATH=%{buildroot} modules_install %{?_smp_mflags}
cp -v arch/x86/boot/bzImage    %{buildroot}/boot/vmlinuz-%{uname_r}
cp -v System.map        %{buildroot}/boot/System.map-%{uname_r}
cp -v .config            %{buildroot}/boot/config-%{uname_r}
cp -r Documentation/*        %{buildroot}%{_defaultdocdir}/linux-%{uname_r}
install -vdm 755 %{buildroot}/usr/lib/debug/lib/modules/%{uname_r}
cp -v vmlinux %{buildroot}/usr/lib/debug/lib/modules/%{uname_r}/vmlinux-%{uname_r}

# install i40e module
bldroot=`pwd`
pushd ../i40e-%{i40e_version}
make -C src KSRC=$bldroot INSTALL_MOD_PATH=%{buildroot} INSTALL_MOD_DIR=extra MANDIR=%{_mandir} modules_install mandocs_install %{?_smp_mflags}
popd

# install ice module
bldroot=`pwd`
pushd ../ice-%{ice_version}
make -C src KSRC=$bldroot INSTALL_MOD_PATH=%{buildroot} INSTALL_MOD_DIR=extra MANDIR=%{_mandir} modules_install mandocs_install %{?_smp_mflags}
popd

#install photon-checksum-generator module
bldroot=`pwd`
pushd ../photon-checksum-generator-%{photon_checksum_generator_version}/kernel
make -C $bldroot M=`pwd` INSTALL_MOD_PATH=%{buildroot} modules_install %{?_smp_mflags}
popd

# TODO: noacpi acpi=off noapic pci=conf1,nodomains pcie_acpm=off pnpacpi=off
cat > %{buildroot}/boot/linux-%{uname_r}.cfg << "EOF"
# GRUB Environment Block
photon_cmdline=init=/lib/systemd/systemd rcupdate.rcu_expedited=1 rw systemd.show_status=0 quiet noreplace-smp cpu_init_udelay=0
photon_linux=vmlinuz-%{uname_r}
photon_initrd=initrd.img-%{uname_r}
EOF

# Register myself to initramfs
mkdir -p %{buildroot}/%{_localstatedir}/lib/initramfs/kernel
cat > %{buildroot}/%{_localstatedir}/lib/initramfs/kernel/%{uname_r} << "EOF"
--add-drivers "lvm dm-mod"
EOF

# cleanup dangling symlinks
rm -f %{buildroot}/lib/modules/%{uname_r}/source
rm -f %{buildroot}/lib/modules/%{uname_r}/build

# create /use/src/linux-headers-*/ content
find . -name Makefile* -o -name Kconfig* -o -name *.pl | xargs  sh -c 'cp --parents "$@" %{buildroot}/usr/src/linux-headers-%{uname_r}' copy
find arch/x86/include include scripts -type f | xargs  sh -c 'cp --parents "$@" %{buildroot}/usr/src/linux-headers-%{uname_r}' copy
find $(find arch/x86 -name include -o -name scripts -type d) -type f | xargs  sh -c 'cp --parents "$@" %{buildroot}/usr/src/linux-headers-%{uname_r}' copy
find arch/x86/include Module.symvers include scripts -type f | xargs  sh -c 'cp --parents "$@" %{buildroot}/usr/src/linux-headers-%{uname_r}' copy

# copy .config manually to be where it's expected to be
cp .config %{buildroot}/usr/src/linux-headers-%{uname_r}
# symling to the build folder
ln -sf /usr/src/linux-headers-%{uname_r} %{buildroot}/lib/modules/%{uname_r}/build
find %{buildroot}/lib/modules -name '*.ko' -print0 | xargs -0 chmod u+x

%include %{SOURCE2}
%include %{SOURCE3}

%post
/sbin/depmod -a %{uname_r}
ln -sf linux-%{uname_r}.cfg /boot/photon.cfg

%post hmacgen
/sbin/depmod -a %{uname_r}

%files
%defattr(-,root,root)
/boot/System.map-%{uname_r}
/boot/config-%{uname_r}
/boot/vmlinuz-%{uname_r}
/boot/.vmlinuz-%{uname_r}.hmac
%config(noreplace) /boot/linux-%{uname_r}.cfg
%config %{_localstatedir}/lib/initramfs/kernel/%{uname_r}
/lib/modules/*
%exclude /lib/modules/%{uname_r}/build
%exclude /usr/src
%exclude /lib/modules/%{uname_r}/extra/hmac_generator.ko.xz
%exclude /lib/modules/%{uname_r}/extra/.hmac_generator.ko.xz.hmac
# ICE driver firmware files are packaged in linux-firmware
%exclude /lib/firmware/updates/intel/ice

%files docs
%defattr(-,root,root)
%{_defaultdocdir}/linux-%{uname_r}/*
# For out-of-tree Intel i40e driver.
%{_mandir}/*

%files devel
%defattr(-,root,root)
/lib/modules/%{uname_r}/build
/usr/src/linux-headers-%{uname_r}

%files hmacgen
%defattr(-,root,root)
/lib/modules/%{uname_r}/extra/hmac_generator.ko.xz
/lib/modules/%{uname_r}/extra/.hmac_generator.ko.xz.hmac

%changelog
*   Wed Oct 06 2021 Keerthana K <keerthanak@vmware.com> 4.19.208-1
-   Update to version 4.19.208
*   Tue Oct 05 2021 Ankit Jain <ankitja@vmware.com> 4.19.205-4
-   vtarfs: Fix memory allocation for entry pages
*   Mon Sep 27 2021 Alexey Makhalov <amakhalov@vmware.com> 4.19.205-3
-   initramfs: large files support for newca
*   Mon Sep 13 2021 Ankit Jain <ankitja@vmware.com> 4.19.205-2
-   vtarfs: Added support for LongFilename/LongLink
*   Fri Aug 27 2021 srinidhira0 <srinidhir@vmware.com> 4.19.205-1
-   Update to version 4.19.205
*   Tue Aug 24 2021 Ankit Jain <ankitja@vmware.com> 4.19.198-3
-   vtarfs: Fix crash in vtarfs_file_read_iter()
*   Wed Aug 18 2021 Keerthana K <keerthanak@vmware.com> 4.19.198-2
-   Update ice driver to v1.6.4
-   Update i40e driver to v2.15.9
*   Tue Jul 27 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.198-1
-   Update to version 4.19.198
*   Thu Jul 15 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.191-5
-   Fix for CVE-2021-33909
*   Thu Jun 24 2021 Ankit Jain <ankitja@vmware.com> 4.19.191-4
-   vtarfs: Fixes fault handler
*   Thu Jun 24 2021 Ankit Jain <ankitja@vmware.com> 4.19.191-3
-   vtarfs: Fixed multiple mount executable issue
*   Tue Jun 22 2021 Sharan Turlapati <sturlapati@vmware.com> 4.19.191-2
-   Fix for CVE-2021-3609
*   Tue Jun 01 2021 Keerthana K <keerthanak@vmware.com> 4.19.191-1
-   Update to version 4.19.191
-   .config: Enable CONFIG_FANOTIFY_ACCESS_PERMISSIONS
*   Thu May 27 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.190-2
-   Add feature to support selective freeing of initrds
*   Mon May 17 2021 Ajay Kaher <akaher@vmware.com> 4.19.190-1
-   Update to version 4.19.190
*   Wed May 12 2021 Sharan Turlapati <sturlapati@vmware.com> 4.19.189-6
-   Fix for CVE-2021-23133
*   Tue May 11 2021 Vivek Thampi <vithampi@vmware.com> 4.19.189-5
-   Add ptp_vmw driver for virtual precision clock.
*   Mon May 10 2021 Ajay Kaher <akaher@vmware.com> 4.19.189-4
-   SEV-ES: update SWIOTLB bounce buffer patch
*   Mon May 10 2021 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.189-3
-   Add out-of-tree i40e and ice drivers.
-   Add support for PTP_SYS_OFFSET_EXTENDED ioctl.
*   Tue May 04 2021 Sharan Turlapati <sturlapati@vmware.com> 4.19.189-2
-   Remove buf_info from device accessible structures in vmxnet3
*   Thu Apr 29 2021 Ankit Jain <ankitja@vmware.com> 4.19.189-1
-   Update to version 4.19.189
*   Mon Apr 26 2021 Ankit Jain <ankitja@vmware.com> 4.19.186-5
-   Fix for CVE-2021-3444
*   Fri Apr 23 2021 Alexey Makhalov <amakhalov@vmware.com> 4.19.186-4
-   .config: enable vfio modules
*   Mon Apr 19 2021 Ajay Kaher <akaher@vmware.com> 4.19.186-3
-   Fixes for SEV-ES
*   Mon Apr 19 2021 Sharan Turlapati <sturlapati@vmware.com> 4.19.186-2
-   Fix for CVE-2021-23133
*   Mon Apr 19 2021 srinidhira0 <srinidhir@vmware.com> 4.19.186-1
-   Update to version 4.19.186
*   Thu Apr 15 2021 Keerthana K <keerthanak@vmware.com> 4.19.182-3
-   photon-checksum-generator update to v1.2
*   Tue Apr 06 2021 Alexey Makhalov <amakhalov@vmware.com> 4.19.182-2
-   .config: disable kernel accounting for memory cgroups
-   .config: enable PERCPU_STATS
-   Enable cgroup v1 stats
*   Thu Mar 25 2021 srinidhira0 <srinidhir@vmware.com> 4.19.182-1
-   Update to version 4.19.182
*   Thu Mar 25 2021 Mounesh Badiger <badigerm@vmware.com> 4.19.177-5
-   9p: VDFS: Integrate shared memory with recovery logic
-   9p: VDFS: Add support claim tags in shared memory
-   9p: VDFS: Integrate 9p IO path with shared memory
-   9p: VDFS: Poller thread for polling completion rings
-   9p: VDFS: Add 9p handlers for shared memory operatios
-   9p: VDFS: Shared memory ring buffer management support
-   9p: VDFS: Add shared memory mmap support in 9p
*   Wed Mar 17 2021 Sharan Turlapati <sturlapati@vmware.com> 4.19.177-4
-   Introduce kernel panic on initramfs unpack failure
*   Thu Mar 04 2021 Ankit Jain <ankitja@vmware.com> 4.19.177-3
-   Added vtarfs support
*   Wed Mar 03 2021 Ankit Jain <ankitja@vmware.com> 4.19.177-2
-   Enable CONFIG_ISCSI_TCP support
*   Fri Feb 26 2021 Sharan Turlapati <sturlapati@vmware.com> 4.19.177-1
-   Update to version 4.19.177
*   Fri Feb 19 2021 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.174-5
-   Fix /boot/photon.cfg symlink when /boot is a separate partition.
*   Thu Feb 11 2021 Ajay Kaher <akaher@vmware.com> 4.19.174-4
-   sev-es: security fixes
*   Thu Feb 11 2021 Srinidhi Rao <srinidhir@vmware.com> 4.19.174-3
-   Sign the crypto modules as they will be verified when FIPS mode is set.
*   Thu Feb 11 2021 Ajay Kaher <akaher@vmware.com> 4.19.174-2
-   Enable CONFIG_WDAT_WDT
*   Tue Feb 09 2021 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.174-1
-   Update to version 4.19.174
*   Tue Jan 12 2021 Alexey Makhalov <amakhalov@vmware.com> 4.19.164-3
-   Remove redundant mem size check.
*   Thu Jan 07 2021 Alexey Makhalov <amakhalov@vmware.com> 4.19.164-2
-   Avoid TSC recalibration
*   Mon Jan 04 2021 Ankit Jain <ankitja@vmware.com> 4.19.164-1
-   Update to version 4.19.164
*   Tue Dec 15 2020 Vikash Bansal <bvikas@vmware.com> 4.19.163-1
-   Update to version 4.19.163
*   Fri Dec 11 2020 Albert Guo <aguo@vmware.com> 4.19.160-4
-   9p: fscache: Ensure consistent blksize is returned from 9p client.
*   Wed Dec 09 2020 Srinidhi Rao <srinidhir@vmware.com> 4.19.160-3
-   Fix for CVE-2019-19770
*   Sun Dec 6 2020 Albert Guo <aguo@vmware.com> 4.19.160-2
-   9p: fscache: Make dcache work with case insensitive volumes
*   Fri Dec 4 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.160-1
-   Update to version 4.19.160
-   Fix CVE-2019-19338 and CVE-2019-20908
*   Fri Dec 4 2020 Albert Guo <aguo@vmware.com> 4.19.154-13
-   9p: fscache: Only fetch attr from inode cache when cache is valid
*   Mon Nov 30 2020 Vikash Bansal <bvikas@vmware.com> 4.19.154-12
-   Mark BAR0 (at offset 0x10) for PCI device 15ad:07b0 (VMXNET3) as variable
*   Fri Nov 20 2020 Ajay Kaher <akaher@vmware.com> 4.19.154-11
-   floppy: lower printk message priority
*   Thu Nov 19 2020 Vikash Bansal <bvikas@vmware.com> 4.19.154-10
-   hmacgen: Add path_put to hmac_gen_hash
*   Tue Nov 17 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.154-9
-   Fix kernel panic on hard-link in initrd
*   Fri Nov 13 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.154-8
-   Fix CVE-2020-25668
*   Wed Nov 11 2020 Albert Guo <aguo@vmware.com> 4.19.154-7
-   9P: Ensure seekdir work correctly when readdir hasn't reached eof
-   9P: [VDFS]Initialize fid->iounit during creation of p9_fid
*   Tue Nov 10 2020 Keerthana K <keerthanak@vmware.com> 4.19.154-6
-   Fix slab-out-of-bounds read in fbcon
*   Tue Nov 10 2020 Keerthana K <keerthanak@vmware.com> 4.19.154-5
-   Fix CVE-2020-8694
*   Fri Nov 06 2020 Keerthana K <keerthanak@vmware.com> 4.19.154-4
-   Fix CVE-2020-25704
*   Tue Nov 03 2020 Ajay Kaher <akaher@vmware.com> 4.19.154-3
-   Adding sev-es: patch set v3
*   Tue Nov 03 2020 Ajay Kaher <akaher@vmware.com> 4.19.154-2
-   Adding following patch series required for sev-es:
-   x86/efi,boot: GDT handling cleanup/fixes
-   x86: Add guard pages to exception and interrupt stacks
-   vmwgfx patches
*   Mon Nov 02 2020 Keerthana K <keerthanak@vmware.com> 4.19.154-1
-   Update to version 4.19.154
*   Mon Oct 26 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.150-4
-   panic on initramfs file overwrite
*   Thu Oct 22 2020 Alexey Makhalov <amakhalov@vmware.com> 4.19.150-3
-   halt_on_panic kernel cmdline.
*   Wed Oct 21 2020 Alexey Makhalov <amakhalov@vmware.com> 4.19.150-2
-   Improve 03-poweroff patch to support direct boot.
-   .config: enable CONFIG_POWER_RESET_PIIX4_POWEROFF.
*   Tue Oct 13 2020 Ajay Kaher <akaher@vmware.com> 4.19.150-1
-   Update to version 4.19.150
*   Mon Oct 12 2020 Ajay Kaher <akaher@vmware.com> 4.19.148-7
-   Fix for CVE-2020-16120
*   Mon Oct 12 2020 Ankit Jain <ankitja@vmware.com> 4.19.148-6
-   Fix for CVE-2020-16119
*   Wed Oct 07 2020 Sriram Patil <sriramp@vmware.com> 4.19.148-5
-   linux-esx: 9p: Fix recovery logic and cleanup tags when unmounting
*   Tue Oct 06 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.148-4
-   Fix IPIP encapsulation issue in vmxnet3 driver.
*   Mon Sep 28 2020 Ajay Kaher <akaher@vmware.com> 4.19.148-3
-   9p: writepages: corrected tofind size
*   Mon Sep 28 2020 Ajay Kaher <akaher@vmware.com> 4.19.148-2
-   9p: enhance performence of writepages for 9p fs cache
*   Mon Sep 28 2020 Ajay Kaher <akaher@vmware.com> 4.19.148-1
-   Update to version 4.19.148
*   Thu Sep 24 2020 Amod Mishra <mamod@vmware.com> 4.19.145-6
-   9p: Corrections have been added inside function
-   "iter_is_bvec" and "iter_is_kvec".
*   Wed Sep 23 2020 Ajay Kaher <akaher@vmware.com> 4.19.145-5
-   Fix for CVE-2020-14390
*   Wed Sep 23 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.145-4
-   Fix for CVE-2019-19813 and CVE-2019-19816
*   Tue Sep 22 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.145-3
-   Add extraction support for multi-image initramfs
*   Tue Sep 22 2020 Ajay Kaher <akaher@vmware.com> 4.19.145-2
-   Fix for CVE-2020-25211
*   Tue Sep 15 2020 Vikash Bansal <bvikas@vmware.com> 4.19.145-1
-   Update to version 4.19.145
*   Thu Sep 10 2020 Ajay Kaher <akaher@vmware.com> 4.19.138-13
-   9p: adding new function iov_iter_to_pfns()
*   Thu Sep 10 2020 Ajay Kaher <akaher@vmware.com> 4.19.138-12
-   Fix 9p lseek issue
*   Mon Sep 07 2020 Amod Mishra <mamod@vmware.com> 4.19.138-11
-   9p: Don't use writeback fid for cache when enabled for VDFS
*   Mon Sep 07 2020 Vikash Bansal <bvikas@vmware.com> 4.19.138-10
-   Fix for CVE-2020-14386
*   Tue Sep 01 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.138-9
-   Enable sysrq magic in config
-   Remove 9p cache container support patch
*   Tue Aug 25 2020 Mounesh Badiger <badigerm@vmware.com> 4.19.138-8
-   VDFS 9p Add xattrcreate to recovery list
*   Tue Aug 18 2020 Ajay Kaher <akaher@vmware.com> 4.19.138-7
-   9p: enhance performence of readpages for 9p fs cache
*   Tue Aug 18 2020 Ajay Kaher <akaher@vmware.com> 4.19.138-6
-   9p: Add opt_metaonly cache option
*   Tue Aug 18 2020 Kevin Kong <kkong@vmware.com> 4.19.138-5
-   fix dirty pages writeback in v9fs_evict_inode.
*   Tue Aug 18 2020 Kevin Kong <kkong@vmware.com> 4.19.138-4
-   VKD 9p Add ext9p alias and implement show_devname for ext9p
*   Tue Aug 18 2020 Kevin Kong <kkong@vmware.com> 4.19.138-3
-   VKD 9p Add no_icache flag to disable dentry/inode cache
*   Wed Aug 12 2020 Alexey Makhalov <amakhalov@vmware.com> 4.19.138-2
-   .config: floppy disk support
*   Wed Aug 12 2020 ashwin-h <ashwinh@vmware.com> 4.19.138-1
-   Update to version 4.19.138
*   Sun Aug 09 2020 Mounesh Badiger <badigerm@vmware.con> 4.19.132-5
-   VDFS 9p Initial recovery logic in 9p.
-   VDFS 9p Add lock state for 9P fid to use it for recovery
-   VDFS 9p Add test infra to test 9p recovery logic
-   VDFS 9p Handle failure during recover
-   VDFS 9p Adding claim tags support in 9p
*   Mon Aug 03 2020 Alexey Makhalov <amakhalov@vmware.com> 4.19.132-4
-   Inherit TSQ limit from root namespace
*   Tue Jul 28 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.132-3
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
*   Thu Jun 04 2020 Alexey Makhalov <amakhalov@vmware.com> 4.19.124-3
-   Support for NSX security requirements
*   Thu Jun 04 2020 Ajay Kaher <akaher@vmware.com> 4.19.124-2
-   Fix for CVE-2020-10757
*   Fri May 29 2020 Ajay Kaher <akaher@vmware.com> 4.19.124-1
-   Update to version 4.19.124
*   Fri May 29 2020 Alexey Makhalov <amakhalov@vmware.com> 4.19.115-10
-   fs/9p: local lock support
*   Fri May 29 2020 Alexey Makhalov <amakhalov@vmware.com> 4.19.115-9
-   initramfs: zero-copy support
*   Thu May 28 2020 Shreenidhi Shedi <sshedi@vmware.com> 4.19.115-8
-   Keep modules of running kernel till next boot
*   Fri May 22 2020 Ashwin H <ashwinh@vmware.com> 4.19.115-7
-   Fix for CVE-2018-20669
*   Fri May 15 2020 Vikash Bansal <bvikas@vmware.com> 4.19.115-6
-   Fix for CVE-2019-18885
*   Tue May 12 2020 Siddharth Chandrasekaran <csiddharth@vmware.com> 4.19.115-5
-   Add patch to fix CVE-2020-10711
*   Fri May 08 2020 Vikash Bansal <bvikas@vmware.com> 4.19.115-4
-   Backported Refactored PCI probe patch with from dev branch
*   Wed Apr 29 2020 Keerthana K <keerthanak@vmware.com> 4.19.115-3
-   Photon-checksum-generator version update to 1.1.
*   Mon Apr 20 2020 Keerthana K <keerthanak@vmware.com> 4.19.115-2
-   Fix __modules_install_post to skip compression for certain modules.
*   Mon Apr 13 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.115-1
-   Update to version 4.19.115
*   Wed Apr 08 2020 Vikash Bansal <bvikas@vmware.com> 4.19.112-5
-   HMAC-SHA256 digest of hmac_generator module moved to hmacgen package
*   Wed Apr 08 2020 Alexey Makhalov <amakhalov@vmware.com> 4.19.112-4
-   Improve hardcodded poweroff (03-poweroff.patch)
*   Wed Apr 08 2020 Mounesh Badiger <badigerm@vmware.com> 4.19.112-3
-   Initialize vdfs zero copy parameters in p9_client_create().
*   Fri Apr 03 2020 Alexey Makhalov <amakhalov@vmware.com> 4.19.112-2
-   9p: cache=container support
*   Mon Mar 23 2020 Keerthana K <keerthanak@vmware.com> 4.19.112-1
-   Update to version 4.19.112
*   Wed Mar 18 2020 Vikash Bansal <bvikas@vmware.com> 4.19.104-4
-   hmac generation of crypto modules and initrd generation changes if fips=1
*   Mon Mar 16 2020 Keerthana K <keerthanak@vmware.com> 4.19.104-3
-   Adding Enhances depedency to hmacgen.
*   Fri Mar 13 2020 Mounesh Badiger <badigerm@vmware.com> 4.19.104-2
-   p9fs_dir_readdir offset support
-   Add 9p zero copy data path using crossfd
-   Enable cache=loose for vdfs 9p
-   9p:Calculate zerocopy pages with considering buffer alignment
*   Mon Mar 09 2020 Siddharth Chandrasekaran <csiddharth@vmware.com> 4.19.104-1
-   Update to version 4.19.104
*   Wed Mar 04 2020 Vikash Bansal <bvikas@vmware.com> 4.19.97-7
-   Backporting of patch continuous testing of RNG from urandom
*   Mon Mar 02 2020 Alexey Makhalov <amakhalov@vmware.com> 4.19.97-6
-   9p: file attributes caching support (cache=stat)
*   Fri Feb 28 2020 Keerthana K <keerthanak@vmware.com> 4.19.97-5
-   Enable CONFIG_CRYPT_TEST for FIPS.
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
*   Tue Jan 14 2020 Srinidhi Rao <srinidhir@vmware.com> 4.19.87-5
-   Enable DRBG HASH and DRBG CTR support.
*   Mon Jan 06 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.87-4
-   Enable CONFIG_NF_CONNTRACK_ZONES
*   Thu Jan 02 2020 Keerthana K <keerthanak@vmware.com> 4.19.87-3
-   Modify tcrypt to remove tests for algorithms that are not supported in photon.
-   Added tests for DH, DRBG algorithms.
*   Fri Dec 20 2019 Keerthana K <keerthanak@vmware.com> 4.19.87-2
-   Update fips Kat tests.
*   Fri Dec 06 2019 Ajay Kaher <akaher@vmware.com> 4.19.87-1
-   Update to version 4.19.87
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
*   Mon Oct 14 2019 Harinadh D <hdommaraju@vmware.com> 4.19.76-4
-   Adding lvm and dm-mod modules to support root as lvm
*   Mon Oct 07 2019 Bo Gan <ganb@vmware.com> 4.19.76-3
-   Recreate /dev/root in init
*   Fri Oct 4 2019 Bo Gan <ganb@vmware.com> 4.19.76-2
-   Enable IMA with SHA256 as default hash algorithm
*   Wed Oct 02 2019 Ajay Kaher <akaher@vmware.com> 4.19.76-1
-   Update to version 4.19.76
*   Thu Sep 19 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.72-2
-   Avoid oldconfig which leads to potential build hang
*   Wed Sep 11 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.72-1
-   Update to version 4.19.72
*   Fri Aug 30 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.69-1
-   Update to version 4.19.69
*   Fri Aug 23 2019 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.65-3
-   .config: Enable CONFIG_IP_VS_WRR, CONFIG_IP_VS_SH, CONFIG_FB_EFI, CONFIG_TCG_TIS_CORE
*   Tue Aug 13 2019 Daniel Müller <danielmuller@vmware.com> 4.19.65-2
-   Add patch "Remove OOM_SCORE_ADJ_MAX limit check"
*   Tue Aug 06 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.65-1
-   Update to version 4.19.65
-   Fix CVE-2019-1125 (SWAPGS)
*   Tue Jul 30 2019 Keerthana K <keerthanak@vmware.com> 4.19.52-4
-   Fix Postun scriplet
*   Tue Jul 02 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.52-3
-   Fix 9p vsock 16bit port issue.
*   Fri Jun 21 2019 Srinidhi Rao <srinidhir@vmware.com> 4.19.52-2
-   Use LZ4 compression and enable VMXNET3 as built-in for linux-esx
*   Mon Jun 17 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.52-1
-   Update to version 4.19.52
-   Fix CVE-2019-12456, CVE-2019-12379, CVE-2019-12380, CVE-2019-12381,
-   CVE-2019-12382, CVE-2019-12378, CVE-2019-12455
*   Tue May 14 2019 Keerthana K <keerthanak@vmware.com> 4.19.40-2
-   Fix to parse through /boot folder and update symlink (/boot/photon.cfg) if
-   mulitple kernels are installed and current linux kernel is removed.
*   Tue May 07 2019 Ajay Kaher <akaher@vmware.com> 4.19.40-1
-   Update to version 4.19.40
*   Fri May 03 2019 Ajay Kaher <akaher@vmware.com> 4.19.32-3
-   Enable SELinux kernel config
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
-   .config: Enable USB_SERIAL and USB_ACM
*   Tue Jan 08 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.6-4
-   Additional security hardening options in the config.
*   Tue Jan 08 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.6-3
-   Fix crash on cpu hot-add.
*   Fri Jan 04 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.6-2
-   Add out-of-tree patches from AppArmor and enable it by default.
*   Mon Dec 10 2018 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.6-1
-   Update to version 4.19.6
*   Thu Nov 29 2018 Alexey Makhalov <amakhalov@vmware.com> 4.19.1-3
-   Fix BAR4 is zero issue for IDE devices
*   Thu Nov 15 2018 Ajay Kaher <akaher@vmware.com> 4.19.1-2
-   Adding BuildArch
*   Thu Nov 08 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.1-1
-   Update to version 4.19.1
*   Mon Sep 24 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.18.9-1
-   Update to version 4.18.9
*   Wed Sep 19 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.14.67-1
-   Update to version 4.14.67
*   Tue Sep 18 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.14.54-3
-   Add rdrand-based RNG driver to enhance kernel entropy.
*   Sun Sep 02 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.14.54-2
-   Add full retpoline support by building with retpoline-enabled gcc.
*   Mon Jul 09 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.14.54-1
-   Update to version 4.14.54
*   Fri Feb 02 2018 Alexey Makhalov <amakhalov@vmware.com> 4.14.8-1
-   Version update
*   Tue Dec 19 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.66-2
-   Enable audit support (CONFIG_AUDIT=y)
*   Mon Dec 04 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.66-1
-   Version update
*   Tue Nov 21 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.64-1
-   Version update
*   Mon Nov 06 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.60-1
-   Version update
*   Wed Oct 25 2017 Anish Swaminathan <anishs@vmware.com> 4.9.53-5
-   Enable x86 vsyscall emulation
*   Tue Oct 17 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.53-4
-   Enable vsyscall emulation
-   Do not use deprecated -q depmod option
*   Wed Oct 11 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.53-3
-   Add patch "KVM: Don't accept obviously wrong gsi values via
    KVM_IRQFD" to fix CVE-2017-1000252.
*   Tue Oct 10 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.53-2
-   Build hang (at make oldconfig) fix.
*   Thu Oct 05 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.53-1
-   Version update
*   Mon Oct 02 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.52-3
-   Allow privileged CLONE_NEWUSER from nested user namespaces.
*   Mon Oct 02 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.52-2
-   Fix CVE-2017-11472 (ACPICA: Namespace: fix operand cache leak)
*   Mon Oct 02 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.52-1
-   Version update
*   Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.47-2
-   Requires coreutils or toybox
*   Mon Sep 04 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.47-1
-   Fix CVE-2017-11600
*   Mon Aug 14 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.43-1
-   Version update
-   [feature] new sysctl option unprivileged_userns_clone
*   Wed Aug 09 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.41-2
-   [bugfix] Do not fallback to syscall from VDSO on clock_gettime(MONOTONIC)
-   Fix CVE-2017-7542
*   Mon Aug 07 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.41-1
-   Version update
*   Wed Jul 26 2017 Bo Gan <ganb@vmware.com> 4.9.38-3
-   Fix initramfs triggers
*   Thu Jul 20 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.38-2
-   Disable scheduler beef up patch
*   Tue Jul 18 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.38-1
-   [feature] IP tunneling support (CONFIG_NET_IPIP=m)
-   Fix CVE-2017-11176 and CVE-2017-10911
*   Mon Jul 03 2017 Xiaolin Li <xiaolinl@vmware.com> 4.9.34-2
-   Add libdnet-devel, kmod-devel and libmspack-devel to BuildRequires
*   Wed Jun 28 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.34-1
-   [feature] DM Delay target support
-   Fix CVE-2017-1000364 ("stack clash") and CVE-2017-9605
*   Thu Jun 8 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.31-1
-   Fix CVE-2017-8890, CVE-2017-9074, CVE-2017-9075, CVE-2017-9076
    CVE-2017-9077 and CVE-2017-9242
*   Thu Jun 1 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.30-2
-   [feature] ACPI NFIT support (for PMEM type 7)
*   Fri May 26 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.30-1
-   Fix CVE-2017-7487 and CVE-2017-9059
*   Wed May 17 2017 Vinay Kulkarni <kulkarniv@vmware.com> 4.9.28-2
-   Enable IPVLAN module.
*   Tue May 16 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.28-1
-   .config: built ATA drivers in a kernel
*   Wed May 10 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.27-1
-   New pci=scan_all cmdline parameter to verify hardcoded pci-probe values
-   pci-probe added more known values
-   vmw_balloon late initcall
*   Sun May 7 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.26-1
-   Version update
-   Use ordered rdtsc in clocksource_vmware
-   .config: added debug info
-   Removed version suffix from config file name
*   Thu Apr 27 2017 Bo Gan <ganb@vmware.com> 4.9.24-2
-   Support dynamic initrd generation
*   Tue Apr 25 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.24-1
-   Fix CVE-2017-6874 and CVE-2017-7618.
-   .config: build nvme and nvme-core in kernel.
*   Tue Feb 28 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.13-1
-   Update to linux-4.9.13 to fix CVE-2017-5986 and CVE-2017-6074
-   .config: enable PMEM support
-   .config: disable vsyscall
*   Thu Feb 09 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.9-1
-   Update to linux-4.9.9 to fix CVE-2016-10153, CVE-2017-5546,
    CVE-2017-5547, CVE-2017-5548 and CVE-2017-5576.
-   .config: added CRYPTO_FIPS and SYN_COOKIES support.
*   Tue Jan 10 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.2-1
-   Update to linux-4.9.2 to fix CVE-2016-10088
*   Wed Dec 21 2016 Alexey Makhalov <amakhalov@vmware.com> 4.9.0-3
-   .config: CONFIG_IPV6_MULTIPLE_TABLES=y
*   Mon Dec 19 2016 Xiaolin Li <xiaolinl@vmware.com> 4.9.0-2
-   BuildRequires Linux-PAM-devel
*   Mon Dec 12 2016 Alexey Makhalov <amakhalov@vmware.com> 4.9.0-1
-   Update to linux-4.9.0
*   Thu Dec  8 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.35-4
-   net-packet-fix-race-condition-in-packet_set_ring.patch
    to fix CVE-2016-8655
*   Wed Nov 30 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.35-3
-   Expand `uname -r` with release number
-   Compress modules
*   Tue Nov 29 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.35-2
-   Added btrfs module
*   Mon Nov 28 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.35-1
-   Update to linux-4.4.35
-   vfio-pci-fix-integer-overflows-bitmask-check.patch
    to fix CVE-2016-9083
*   Tue Nov 22 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.31-4
-   net-9p-vsock.patch
*   Thu Nov 17 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.31-3
-   tty-prevent-ldisc-drivers-from-re-using-stale-tty-fields.patch
    to fix CVE-2015-8964
*   Tue Nov 15 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.31-2
-   .config: add ip set support
-   .config: add ipvs_{tcp,udp} support
-   .config: add cgrup_{hugetlb,net_prio} support
*   Thu Nov 10 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.31-1
-   Update to linux-4.4.31
*   Thu Nov 10 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.26-2
-   .config: add ipvs modules for docker swarm
-   .config: serial driver built in kernel
-   serial-8250-do-not-probe-U6-16550A-fifo-size.patch - faster boot
*   Fri Oct 21 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.26-1
-   Update to linux-4.4.26
*   Wed Oct 19 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.20-7
-   net-add-recursion-limit-to-GRO.patch
*   Tue Oct 18 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.20-6
-   ipip-properly-mark-ipip-GRO-packets-as-encapsulated.patch
-   tunnels-dont-apply-GRO-to-multiple-layers-of-encapsulation.patch
*   Thu Oct  6 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.20-5
-   .config: added ADM PCnet32 support
-   vmci-1.1.4.0-use-32bit-atomics-for-queue-headers.patch
-   vmci-1.1.5.0-doorbell-create-and-destroy-fixes.patch
-   late_initcall for vmw_balloon driver
-   Minor fixed in pv-ops patchset
*   Mon Oct  3 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.20-4
-   Package vmlinux with PROGBITS sections in -debuginfo subpackage
*   Wed Sep 21 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.20-3
-   Add PCIE hotplug support
-   Switch processor type to generic
*   Tue Sep 20 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.20-2
-   Add -release number for /boot/* files
-   Fixed generation of debug symbols for kernel modules & vmlinux
*   Wed Sep  7 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.20-1
-   Update to linux-4.4.20
-   keys-fix-asn.1-indefinite-length-object-parsing.patch
*   Thu Aug 25 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-11
-   vmxnet3 patches to bumpup a version to 1.4.8.0
*   Wed Aug 24 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-10
-   .config: added NVME blk dev support
*   Wed Aug 10 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-9
-   Added VSOCK-Detach-QP-check-should-filter-out-non-matching-QPs.patch
*   Wed Jul 20 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-8
-   .config: added cgroups for pids,mem and blkio
*   Mon Jul 11 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-7
-   .config: added ip multible tables support
*   Fri Jun 17 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-6
-   patch: e1000e-prevent-div-by-zero-if-TIMINCA-is-zero.patch
-   .config: disable rt group scheduling - not supported by systemd
*   Fri May 27 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-5
-   patch: REVERT-sched-fair-Beef-up-wake_wide.patch
*   Wed May 25 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-4
-   .config: added net_9p and 9p_fs
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.4.8-3
-   GA - Bump release of all rpms
*   Mon May 23 2016 Divya Thaluru <dthaluru@vmware.com> 4.4.8-2
-   Added patches to fix CVE-2016-3134, CVE-2016-3135
*   Fri May 13 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-1
-   Update to linux-4.4.8
-   Added net-Drivers-Vmxnet3-set-... patch
-   Added e1000e module
*   Tue Mar 29 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-19
-   Support kmsg dumping to vmware.log on panic
-   sunrpc: xs_bind uses ip_local_reserved_ports
*   Thu Mar 24 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-18
-   Apply photon8 config (+stack protector regular)
-   pv-ops patch: added STA support
-   Added patches from generic kernel
*   Wed Mar 09 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.2.0-17
-   Enable ACPI hotplug support in kernel config
*   Sun Feb 14 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-16
-   veth patch: don’t modify ip_summed
*   Mon Feb 08 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-15
-   Double tcp_mem limits, patch is added.
*   Wed Feb 03 2016 Anish Swaminathan <anishs@vmware.com>  4.2.0-14
-   Fixes for CVE-2015-7990/6937 and CVE-2015-8660.
*   Fri Jan 22 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-13
-   Fix for CVE-2016-0728
*   Wed Jan 13 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-12
-   CONFIG_HZ=250
-   Disable sched autogroup.
*   Tue Jan 12 2016 Mahmoud Bassiouny <mbassiouny@vmware.com> 4.2.0-11
-   Remove rootfstype from the kernel parameter.
*   Tue Dec 15 2015 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-10
-   Skip rdrand reseed to improve boot time.
-   .config changes: jolietfs(m), default THP=always, hotplug_cpu(m)
*   Tue Nov 17 2015 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-9
-   nordrand cmdline param is removed.
-   .config: + serial 8250 driver (M).
*   Fri Nov 13 2015 Mahmoud Bassiouny <mbassiouny@vmware.com> 4.2.0-8
-   Change the linux image directory.
*   Tue Nov 10 2015 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-7
-   Get LAPIC timer frequency from HV, skip boot time calibration.
-   .config: + dummy net driver (M).
*   Mon Nov 09 2015 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-6
-   Rename subpackage dev -> devel.
-   Added the build essential files in the devel subpackage.
-   .config: added genede driver module.
*   Wed Oct 28 2015 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-5
-   Import patches from kernel2 repo.
-   Added pv-ops patch (timekeeping related improvements).
-   Removed unnecessary cmdline params.
-   .config changes: elevator=noop by default, paravirt clock enable,
    initrd support, openvswitch module, x2apic enable.
*   Mon Sep 21 2015 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-4
-   CDROM modules are added.
*   Thu Sep 17 2015 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-3
-   Fix for 05- patch (SVGA mem size)
-   Compile out: pci hotplug, sched smt.
-   Compile in kernel: vmware balloon & vmci.
-   Module for efi vars.
*   Fri Sep 4 2015 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-2
-   Hardcoded poweroff (direct write to piix4), no ACPI is required.
-   sd.c: Lower log level for "Assuming drive cache..." message.
*   Tue Sep 1 2015 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-1
-   Update to linux-4.2.0. Enable CONFIG_EFI
*   Fri Aug 28 2015 Alexey Makhalov <amakhalov@vmware.com> 4.1.3-5
-   Added MD/LVM/DM modules.
-   Pci probe improvements.
*   Fri Aug 14 2015 Alexey Makhalov <amakhalov@vmware.com> 4.1.3-4
-   Use photon.cfg as a symlink.
*   Thu Aug 13 2015 Alexey Makhalov <amakhalov@vmware.com> 4.1.3-3
-   Added environment file(photon.cfg) for a grub.
*   Tue Aug 11 2015 Alexey Makhalov <amakhalov@vmware.com> 4.1.3-2
-   Added pci-probe-vmware.patch. Removed unused modules. Decreased boot time.
*   Tue Jul 28 2015 Alexey Makhalov <amakhalov@vmware.com> 4.1.3-1
-   Initial commit. Use patchset from Clear Linux.
