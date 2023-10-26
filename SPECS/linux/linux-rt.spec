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

Summary:        Kernel
Name:           linux-rt
Version:        5.10.198
Release:        3%{?kat_build:.kat}%{?dist}
License:        GPLv2
URL:            http://www.kernel.org/
Group:          System Environment/Kernel
Vendor:         VMware, Inc.
Distribution:   Photon

# Keep rt_version matched up with localversion.patch
%define rt_version rt96
%define uname_r %{version}-%{release}-rt
%define _modulesdir /lib/modules/%{uname_r}

Source0:        http://www.kernel.org/pub/linux/kernel/v5.x/linux-%{version}.tar.xz
%define sha512 linux=3ccfbaff9b45d3239024e6c29e3a33af05460997971d767293e45f22c4db66f99595285d5dac1071f19926f35cdd90d323bd6e57809b57954f4988152ebe6342
Source1:    config-rt
Source2:    initramfs.trigger
# contains pre, postun, filetriggerun tasks
Source4:    scriptlets.inc
Source5:    check_for_config_applicability.inc

%ifarch x86_64
%define i40e_version 2.22.18
Source6:    https://sourceforge.net/projects/e1000/files/i40e%20stable/%{i40e_version}/i40e-%{i40e_version}.tar.gz
%define sha512 i40e=042fd064528cb807894dc1f211dcb34ff28b319aea48fc6dede928c93ef4bbbb109bdfc903c27bae98b2a41ba01b7b1dffc3acac100610e3c6e95427162a26ac

%define iavf_version 4.8.2
Source7:       https://sourceforge.net/projects/e1000/files/iavf%20stable/%{iavf_version}/iavf-%{iavf_version}.tar.gz
%define sha512 iavf=5406b86e61f6528adfd7bc3a5f330cec8bb3b4d6c67395961cc6ab78ec3bd325c3a8655b8f42bf56fb47c62a85fb7dbb0c1aa3ecb6fa069b21acb682f6f578cf

%define ice_version 1.11.14
Source8:       https://sourceforge.net/projects/e1000/files/ice%20stable/%{ice_version}/ice-%{ice_version}.tar.gz
%define sha512 ice=a2a6a498e553d41e4e6959a19cdb74f0ceff3a7dbcbf302818ad514fdc18e3d3b515242c88d55ef8a00c9d16925f0cd8579cb41b3b1c27ea6716ccd7e70fd847
%endif

%if 0%{?fips}
Source9:        check_fips_canister_struct_compatibility.inc

%define fips_canister_version 5.0.0-6.1.56-6.ph5-secure
Source16:       fips-canister-%{fips_canister_version}.tar.bz2
%define sha512 fips-canister=7e1dc80c5eecf2a8cf5e5fc964b5fa56dbcaff9d11a97393d0d57ab8f63ea343f0d164a4354d011c2dc946abd3fd6f772905f1a8e355b22ee318adcdd2fe6b26
%endif

Source21:        spec_install_post.inc
Source22:        %{name}-dracut.conf

%ifarch x86_64
%define jent_major_version 3.4.1
%define jent_ph_version 3
Source32: jitterentropy-%{jent_major_version}-%{jent_ph_version}.tar.bz2
%define sha512 jitterentropy=b5aa389d331e0a8b22e696e83cccaddb17f98da06fe9592e75cd7efb24877e1cb65b24c2f909e82d247e0dcbb77043b0235f8df94d40d6cb4c4f9a7c113b4f18
Source33: jitterentropy_canister_wrapper.c
Source34: jitterentropy_canister_wrapper.h
Source35: jitterentropy_canister_wrapper_asm.S
%endif

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

# ttyXRUSB support
Patch10: usb-acm-exclude-exar-usb-serial-ports-nxt.patch

Patch12: fork-add-sysctl-to-disallow-unprivileged-CLONE_NEWUSER-by.patch
# Out-of-tree patches from AppArmor:
Patch13: apparmor-patch-to-provide-compatibility-with-v2.x-ne.patch
Patch14: apparmor-af_unix-mediation.patch

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
Patch46: 0004-linux-rt-Makefile-Add-kernel-flavor-info-to-the-gene.patch

# VMW:
Patch55: x86-vmware-Use-Efficient-and-Correct-ALTERNATIVEs-fo-510.patch
Patch56: x86-vmware-Log-kmsg-dump-on-panic-510.patch
Patch57: 0001-x86-vmware-avoid-TSC-recalibration.patch

# CVE:
Patch100: apparmor-fix-use-after-free-in-sk_peer_label.patch
# Fix for CVE-2019-12379
Patch101: consolemap-Fix-a-memory-leaking-bug-in-drivers-tty-v.patch

# Next 2 patches are about to be merged into stable
Patch102: 0001-mm-fix-panic-in-__alloc_pages.patch

# Fix for CVE-2021-4204
Patch103: 0002-bpf-Disallow-unprivileged-bpf-by-default.patch

# Fix for CVE-2022-3522
Patch106: 0001-mm_hugetlb_handle_pte_markers_in_page_faults.patch
Patch107: 0002-mm_hugetlb_fix_race_condition_of_uffd_missing_minor_handling.patch
Patch108: 0003-mm_hugetlb_use_hugetlb_pte_stable_in_migration_race_check.patch

# Fix for CVE-2022-0500
Patch113: 0001-bpf-Introduce-composable-reg-ret-and-arg-types.patch
Patch114: 0002-bpf-Replace-ARG_XXX_OR_NULL-with-ARG_XXX-PTR_MAYBE_N.patch
Patch115: 0003-bpf-Replace-RET_XXX_OR_NULL-with-RET_XXX-PTR_MAYBE_N.patch
Patch116: 0004-bpf-Extract-nullable-reg-type-conversion-into-a-help.patch
Patch117: 0005-bpf-Replace-PTR_TO_XXX_OR_NULL-with-PTR_TO_XXX-PTR_M.patch
Patch118: 0006-bpf-Introduce-MEM_RDONLY-flag.patch
Patch119: 0007-bpf-Make-per_cpu_ptr-return-rdonly-PTR_TO_MEM.patch
Patch120: 0008-bpf-Add-MEM_RDONLY-for-helper-args-that-are-pointers.patch

# Fix for CVE-2022-3524 and CVE-2022-3567
Patch121: 0001-ipv6-annotate-some-data-races-around-sk-sk_prot.patch
Patch125: 0005-ipv6-Fix-data-races-around-sk-sk_prot.patch
Patch126: 0006-tcp-Fix-data-races-around-icsk-icsk_af_ops.patch

#Fix for CVE-2022-43945
Patch129: 0001-NFSD-Cap-rsize_bop-result-based-on-send-buffer-size.patch
Patch130: 0002-NFSD-Protect-against-send-buffer-overflow-in-NFSv3-R.patch
Patch131: 0003-NFSD-Protect-against-send-buffer-overflow-in-NFSv2-R.patch
Patch132: 0004-NFSD-Protect-against-send-buffer-overflow-in-NFSv3-R.patch

#Fix for CVE-2021-3699
Patch133: ipc-replace-costly-bailout-check-in-sysvipc_find_ipc.patch

# Allow PCI resets to be disabled from vfio_pci module
Patch200: 0001-drivers-vfio-pci-Add-kernel-parameter-to-allow-disab.patch
# Add PCI quirk to allow multiple devices under the same virtual PCI bridge
# to be put into separate IOMMU groups on ESXi.
Patch201: 0001-Add-PCI-quirk-for-VMware-PCIe-Root-Port.patch

# Enable CONFIG_DEBUG_INFO_BTF=y
Patch202: 0001-tools-resolve_btfids-Warn-when-having-multiple-IDs-f.patch

# Real-Time kernel (PREEMPT_RT patches)
# Source: http://cdn.kernel.org/pub/linux/kernel/projects/rt/5.10/
Patch301: 0001-z3fold-remove-preempt-disabled-sections-for-RT.patch
Patch302: 0002-stop_machine-Add-function-and-caller-debug-info.patch
Patch303: 0003-sched-Fix-balance_callback.patch
Patch304: 0004-sched-hotplug-Ensure-only-per-cpu-kthreads-run-durin.patch
Patch305: 0005-sched-core-Wait-for-tasks-being-pushed-away-on-hotpl.patch
Patch306: 0006-workqueue-Manually-break-affinity-on-hotplug.patch
Patch307: 0007-sched-hotplug-Consolidate-task-migration-on-CPU-unpl.patch
Patch308: 0008-sched-Fix-hotplug-vs-CPU-bandwidth-control.patch
Patch309: 0009-sched-Massage-set_cpus_allowed.patch
Patch310: 0010-sched-Add-migrate_disable.patch
Patch311: 0011-sched-Fix-migrate_disable-vs-set_cpus_allowed_ptr.patch
Patch312: 0012-sched-core-Make-migrate-disable-and-CPU-hotplug-coop.patch
Patch313: 0013-sched-rt-Use-cpumask_any-_distribute.patch
Patch314: 0014-sched-rt-Use-the-full-cpumask-for-balancing.patch
Patch315: 0015-sched-lockdep-Annotate-pi_lock-recursion.patch
Patch316: 0016-sched-Fix-migrate_disable-vs-rt-dl-balancing.patch
Patch317: 0017-sched-proc-Print-accurate-cpumask-vs-migrate_disable.patch
Patch318: 0018-sched-Add-migrate_disable-tracepoints.patch
Patch319: 0019-sched-Deny-self-issued-__set_cpus_allowed_ptr-when-m.patch
Patch320: 0020-sched-Comment-affine_move_task.patch
Patch321: 0021-sched-Unlock-the-rq-in-affine_move_task-error-path.patch
Patch322: 0022-sched-Fix-migration_cpu_stop-WARN.patch
Patch323: 0023-sched-core-Add-missing-completion-for-affine_move_ta.patch
Patch324: 0024-mm-highmem-Un-EXPORT-__kmap_atomic_idx.patch
Patch325: 0025-highmem-Remove-unused-functions.patch
Patch326: 0026-fs-Remove-asm-kmap_types.h-includes.patch
Patch327: 0027-sh-highmem-Remove-all-traces-of-unused-cruft.patch
Patch328: 0028-asm-generic-Provide-kmap_size.h.patch
Patch329: 0029-highmem-Provide-generic-variant-of-kmap_atomic.patch
Patch330: 0030-highmem-Make-DEBUG_HIGHMEM-functional.patch
Patch331: 0031-x86-mm-highmem-Use-generic-kmap-atomic-implementatio.patch
Patch332: 0032-arc-mm-highmem-Use-generic-kmap-atomic-implementatio.patch
Patch333: 0033-ARM-highmem-Switch-to-generic-kmap-atomic.patch
Patch334: 0034-csky-mm-highmem-Switch-to-generic-kmap-atomic.patch
Patch335: 0035-microblaze-mm-highmem-Switch-to-generic-kmap-atomic.patch
Patch336: 0036-mips-mm-highmem-Switch-to-generic-kmap-atomic.patch
Patch337: 0037-nds32-mm-highmem-Switch-to-generic-kmap-atomic.patch
Patch338: 0038-powerpc-mm-highmem-Switch-to-generic-kmap-atomic.patch
Patch339: 0039-sparc-mm-highmem-Switch-to-generic-kmap-atomic.patch
Patch340: 0040-xtensa-mm-highmem-Switch-to-generic-kmap-atomic.patch
Patch341: 0041-highmem-Get-rid-of-kmap_types.h.patch
Patch342: 0042-mm-highmem-Remove-the-old-kmap_atomic-cruft.patch
Patch343: 0043-io-mapping-Cleanup-atomic-iomap.patch
Patch344: 0044-Documentation-io-mapping-Remove-outdated-blurb.patch
Patch345: 0045-highmem-High-implementation-details-and-document-API.patch
Patch346: 0046-sched-Make-migrate_disable-enable-independent-of-RT.patch
Patch347: 0047-sched-highmem-Store-local-kmaps-in-task-struct.patch
Patch348: 0048-mm-highmem-Provide-kmap_local.patch
Patch349: 0049-io-mapping-Provide-iomap_local-variant.patch
Patch350: 0050-x86-crashdump-32-Simplify-copy_oldmem_page.patch
Patch351: 0051-mips-crashdump-Simplify-copy_oldmem_page.patch
Patch352: 0052-ARM-mm-Replace-kmap_atomic_pfn.patch
Patch353: 0053-highmem-Remove-kmap_atomic_pfn.patch
Patch354: 0054-drm-ttm-Replace-kmap_atomic-usage.patch
Patch355: 0055-drm-vmgfx-Replace-kmap_atomic.patch
Patch356: 0056-highmem-Remove-kmap_atomic_prot.patch
Patch357: 0057-drm-qxl-Replace-io_mapping_map_atomic_wc.patch
Patch358: 0058-drm-nouveau-device-Replace-io_mapping_map_atomic_wc.patch
Patch359: 0059-drm-i915-Replace-io_mapping_map_atomic_wc.patch
Patch360: 0060-io-mapping-Remove-io_mapping_map_atomic_wc.patch
Patch361: 0061-mm-highmem-Take-kmap_high_get-properly-into-account.patch
Patch362: 0062-highmem-Don-t-disable-preemption-on-RT-in-kmap_atomi.patch
Patch363: 0063-blk-mq-Don-t-complete-on-a-remote-CPU-in-force-threa.patch
Patch364: 0064-blk-mq-Always-complete-remote-completions-requests-i.patch
Patch365: 0065-blk-mq-Use-llist_head-for-blk_cpu_done.patch
Patch366: 0066-lib-test_lockup-Minimum-fix-to-get-it-compiled-on-PR.patch
Patch367: 0067-timers-Don-t-block-on-expiry_lock-for-TIMER_IRQSAFE.patch
Patch368: 0068-kthread-Move-prio-affinite-change-into-the-newly-cre.patch
Patch369: 0069-genirq-Move-prio-assignment-into-the-newly-created-t.patch
Patch370: 0070-notifier-Make-atomic_notifiers-use-raw_spinlock.patch
Patch371: 0071-rcu-Make-RCU_BOOST-default-on-CONFIG_PREEMPT_RT.patch
Patch372: 0072-rcu-Unconditionally-use-rcuc-threads-on-PREEMPT_RT.patch
Patch373: 0073-rcu-Enable-rcu_normal_after_boot-unconditionally-for.patch
Patch374: 0074-doc-Update-RCU-s-requirements-page-about-the-PREEMPT.patch
Patch375: 0075-doc-Use-CONFIG_PREEMPTION.patch
Patch376: 0076-tracing-Merge-irqflags-preempt-counter.patch
Patch377: 0077-tracing-Inline-tracing_gen_ctx_flags.patch
Patch378: 0078-tracing-Use-in_serving_softirq-to-deduct-softirq-sta.patch
Patch379: 0079-tracing-Remove-NULL-check-from-current-in-tracing_ge.patch
Patch380: 0080-printk-inline-log_output-log_store-in-vprintk_store.patch
Patch381: 0081-printk-remove-logbuf_lock-writer-protection-of-ringb.patch
Patch382: 0082-printk-limit-second-loop-of-syslog_print_all.patch
Patch383: 0083-printk-kmsg_dump-remove-unused-fields.patch
Patch384: 0084-printk-refactor-kmsg_dump_get_buffer.patch
Patch385: 0085-printk-consolidate-kmsg_dump_get_buffer-syslog_print.patch
Patch386: 0086-printk-introduce-CONSOLE_LOG_MAX-for-improved-multi-.patch
Patch387: 0087-printk-use-seqcount_latch-for-clear_seq.patch
Patch388: 0088-printk-use-atomic64_t-for-devkmsg_user.seq.patch
Patch389: 0089-printk-add-syslog_lock.patch
Patch390: 0090-printk-introduce-a-kmsg_dump-iterator.patch
Patch391: 0091-um-synchronize-kmsg_dumper.patch
Patch392: 0092-printk-remove-logbuf_lock.patch
Patch393: 0093-printk-kmsg_dump-remove-_nolock-variants.patch
Patch394: 0094-printk-kmsg_dump-use-kmsg_dump_rewind.patch
Patch395: 0095-printk-console-remove-unnecessary-safe-buffer-usage.patch
Patch396: 0096-printk-track-limit-recursion.patch
Patch397: 0097-printk-remove-safe-buffers.patch
Patch398: 0098-printk-convert-syslog_lock-to-spin_lock.patch
Patch399: 0099-console-add-write_atomic-interface.patch
Patch400: 0100-serial-8250-implement-write_atomic.patch
Patch401: 0101-printk-relocate-printk_delay-and-vprintk_default.patch
Patch402: 0102-printk-combine-boot_delay_msec-into-printk_delay.patch
Patch403: 0103-printk-change-console_seq-to-atomic64_t.patch
Patch404: 0104-printk-introduce-kernel-sync-mode.patch
Patch405: 0105-printk-move-console-printing-to-kthreads.patch
Patch406: 0106-printk-remove-deferred-printing.patch
Patch407: 0107-printk-add-console-handover.patch
Patch408: 0108-printk-add-pr_flush.patch
Patch409: 0109-cgroup-use-irqsave-in-cgroup_rstat_flush_locked.patch
Patch410: 0110-mm-workingset-replace-IRQ-off-check-with-a-lockdep-a.patch
Patch411: 0111-tpm-remove-tpm_dev_wq_lock.patch
Patch412: 0112-shmem-Use-raw_spinlock_t-for-stat_lock.patch
Patch413: 0113-net-Move-lockdep-where-it-belongs.patch
Patch414: 0114-parisc-Remove-bogus-__IRQ_STAT-macro.patch
Patch415: 0115-sh-Get-rid-of-nmi_count.patch
Patch416: 0116-irqstat-Get-rid-of-nmi_count-and-__IRQ_STAT.patch
Patch417: 0117-um-irqstat-Get-rid-of-the-duplicated-declarations.patch
Patch418: 0118-ARM-irqstat-Get-rid-of-duplicated-declaration.patch
Patch419: 0119-arm64-irqstat-Get-rid-of-duplicated-declaration.patch
Patch420: 0120-asm-generic-irqstat-Add-optional-__nmi_count-member.patch
Patch421: 0121-sh-irqstat-Use-the-generic-irq_cpustat_t.patch
Patch422: 0122-irqstat-Move-declaration-into-asm-generic-hardirq.h.patch
Patch423: 0123-preempt-Cleanup-the-macro-maze-a-bit.patch
Patch424: 0124-softirq-Move-related-code-into-one-section.patch
Patch425: 0125-sh-irq-Add-missing-closing-parentheses-in-arch_show_.patch
Patch426: 0126-sched-cputime-Remove-symbol-exports-from-IRQ-time-ac.patch
Patch427: 0127-s390-vtime-Use-the-generic-IRQ-entry-accounting.patch
Patch428: 0128-sched-vtime-Consolidate-IRQ-time-accounting.patch
Patch429: 0129-irqtime-Move-irqtime-entry-accounting-after-irq-offs.patch
Patch430: 0130-irq-Call-tick_irq_enter-inside-HARDIRQ_OFFSET.patch
Patch431: 0131-smp-Wake-ksoftirqd-on-PREEMPT_RT-instead-do_softirq.patch
Patch432: 0132-tasklets-Replace-barrier-with-cpu_relax-in-tasklet_u.patch
Patch433: 0133-tasklets-Use-static-inlines-for-stub-implementations.patch
Patch434: 0134-tasklets-Provide-tasklet_disable_in_atomic.patch
Patch435: 0135-tasklets-Use-spin-wait-in-tasklet_disable-temporaril.patch
Patch436: 0136-tasklets-Replace-spin-wait-in-tasklet_unlock_wait.patch
Patch437: 0137-tasklets-Replace-spin-wait-in-tasklet_kill.patch
Patch438: 0138-tasklets-Prevent-tasklet_unlock_spin_wait-deadlock-o.patch
Patch439: 0139-net-jme-Replace-link-change-tasklet-with-work.patch
Patch440: 0140-net-sundance-Use-tasklet_disable_in_atomic.patch
Patch441: 0141-ath9k-Use-tasklet_disable_in_atomic.patch
Patch442: 0142-atm-eni-Use-tasklet_disable_in_atomic-in-the-send-ca.patch
Patch443: 0143-PCI-hv-Use-tasklet_disable_in_atomic.patch
Patch444: 0144-firewire-ohci-Use-tasklet_disable_in_atomic-where-re.patch
Patch445: 0145-tasklets-Switch-tasklet_disable-to-the-sleep-wait-va.patch
Patch446: 0146-softirq-Add-RT-specific-softirq-accounting.patch
Patch447: 0147-irqtime-Make-accounting-correct-on-RT.patch
Patch448: 0148-softirq-Move-various-protections-into-inline-helpers.patch
Patch449: 0149-softirq-Make-softirq-control-and-processing-RT-aware.patch
Patch450: 0150-tick-sched-Prevent-false-positive-softirq-pending-wa.patch
Patch451: 0151-rcu-Prevent-false-positive-softirq-warning-on-RT.patch
Patch452: 0152-chelsio-cxgb-Replace-the-workqueue-with-threaded-int.patch
Patch453: 0153-chelsio-cxgb-Disable-the-card-on-error-in-threaded-i.patch
Patch454: 0154-x86-fpu-Simplify-fpregs_-un-lock.patch
Patch455: 0155-x86-fpu-Make-kernel-FPU-protection-RT-friendly.patch
Patch456: 0156-locking-rtmutex-Remove-cruft.patch
Patch457: 0157-locking-rtmutex-Remove-output-from-deadlock-detector.patch
Patch458: 0158-locking-rtmutex-Move-rt_mutex_init-outside-of-CONFIG.patch
Patch459: 0159-locking-rtmutex-Remove-rt_mutex_timed_lock.patch
Patch460: 0160-locking-rtmutex-Handle-the-various-new-futex-race-co.patch
Patch461: 0161-futex-Fix-bug-on-when-a-requeued-RT-task-times-out.patch
Patch462: 0162-locking-rtmutex-Make-lock_killable-work.patch
Patch463: 0163-locking-spinlock-Split-the-lock-types-header.patch
Patch464: 0164-locking-rtmutex-Avoid-include-hell.patch
Patch465: 0165-lockdep-Reduce-header-files-in-debug_locks.h.patch
Patch466: 0166-locking-split-out-the-rbtree-definition.patch
Patch467: 0167-locking-rtmutex-Provide-rt_mutex_slowlock_locked.patch
Patch468: 0168-locking-rtmutex-export-lockdep-less-version-of-rt_mu.patch
Patch469: 0169-sched-Add-saved_state-for-tasks-blocked-on-sleeping-.patch
Patch470: 0170-locking-rtmutex-add-sleeping-lock-implementation.patch
Patch471: 0171-locking-rtmutex-Allow-rt_mutex_trylock-on-PREEMPT_RT.patch
Patch472: 0172-locking-rtmutex-add-mutex-implementation-based-on-rt.patch
Patch473: 0173-locking-rtmutex-add-rwsem-implementation-based-on-rt.patch
Patch474: 0174-locking-rtmutex-add-rwlock-implementation-based-on-r.patch
Patch475: 0175-locking-rtmutex-wire-up-RT-s-locking.patch
Patch476: 0176-locking-rtmutex-add-ww_mutex-addon-for-mutex-rt.patch
Patch477: 0177-locking-rtmutex-Use-custom-scheduling-function-for-s.patch
Patch478: 0178-signal-Revert-ptrace-preempt-magic.patch
Patch479: 0179-preempt-Provide-preempt_-_-no-rt-variants.patch
Patch480: 0180-mm-vmstat-Protect-per-cpu-variables-with-preempt-dis.patch
Patch481: 0181-mm-memcontrol-Disable-preemption-in-__mod_memcg_lruv.patch
Patch482: 0182-xfrm-Use-sequence-counter-with-associated-spinlock.patch
Patch483: 0183-u64_stats-Disable-preemption-on-32bit-UP-SMP-with-RT.patch
Patch484: 0184-fs-dcache-use-swait_queue-instead-of-waitqueue.patch
Patch485: 0185-fs-dcache-disable-preemption-on-i_dir_seq-s-write-si.patch
Patch486: 0186-net-Qdisc-use-a-seqlock-instead-seqcount.patch
Patch487: 0187-net-Properly-annotate-the-try-lock-for-the-seqlock.patch
Patch488: 0188-kconfig-Disable-config-options-which-are-not-RT-comp.patch
Patch489: 0189-mm-Allow-only-SLUB-on-RT.patch
Patch490: 0190-sched-Disable-CONFIG_RT_GROUP_SCHED-on-RT.patch
Patch491: 0191-net-core-disable-NET_RX_BUSY_POLL-on-RT.patch
Patch492: 0192-efi-Disable-runtime-services-on-RT.patch
Patch493: 0193-efi-Allow-efi-runtime.patch
Patch494: 0194-rt-Add-local-irq-locks.patch
Patch495: 0195-signal-x86-Delay-calling-signals-in-atomic.patch
Patch496: 0196-Split-IRQ-off-and-zone-lock-while-freeing-pages-from.patch
Patch497: 0197-Split-IRQ-off-and-zone-lock-while-freeing-pages-from.patch
Patch498: 0198-mm-SLxB-change-list_lock-to-raw_spinlock_t.patch
Patch499: 0199-mm-SLUB-delay-giving-back-empty-slubs-to-IRQ-enabled.patch
Patch500: 0200-mm-slub-Always-flush-the-delayed-empty-slubs-in-flus.patch
Patch501: 0201-mm-slub-Don-t-resize-the-location-tracking-cache-on-.patch
Patch502: 0202-mm-page_alloc-Use-migrate_disable-in-drain_local_pag.patch
Patch503: 0203-mm-page_alloc-rt-friendly-per-cpu-pages.patch
Patch504: 0204-mm-slub-Make-object_map_lock-a-raw_spinlock_t.patch
Patch505: 0205-slub-Enable-irqs-for-__GFP_WAIT.patch
Patch506: 0206-slub-Disable-SLUB_CPU_PARTIAL.patch
Patch507: 0207-mm-memcontrol-Provide-a-local_lock-for-per-CPU-memcg.patch
Patch508: 0208-mm-memcontrol-Don-t-call-schedule_work_on-in-preempt.patch
Patch509: 0209-mm-memcontrol-Replace-local_irq_disable-with-local-l.patch
Patch510: 0210-mm-zsmalloc-copy-with-get_cpu_var-and-locking.patch
Patch511: 0211-mm-zswap-Use-local-lock-to-protect-per-CPU-data.patch
Patch512: 0212-x86-kvm-Require-const-tsc-for-RT.patch
Patch513: 0213-wait.h-include-atomic.h.patch
Patch514: 0214-sched-Limit-the-number-of-task-migrations-per-batch.patch
Patch515: 0215-sched-Move-mmdrop-to-RCU-on-RT.patch
Patch516: 0216-kernel-sched-move-stack-kprobe-clean-up-to-__put_tas.patch
Patch517: 0217-sched-Do-not-account-rcu_preempt_depth-on-RT-in-migh.patch
Patch518: 0218-sched-Disable-TTWU_QUEUE-on-RT.patch
Patch519: 0219-softirq-Check-preemption-after-reenabling-interrupts.patch
Patch520: 0220-softirq-Disable-softirq-stacks-for-RT.patch
Patch521: 0221-net-core-use-local_bh_disable-in-netif_rx_ni.patch
Patch522: 0222-pid.h-include-atomic.h.patch
Patch523: 0223-ptrace-fix-ptrace-vs-tasklist_lock-race.patch
Patch524: 0224-ptrace-fix-ptrace_unfreeze_traced-race-with-rt-lock.patch
Patch525: 0225-kernel-sched-add-put-get-_cpu_light.patch
Patch526: 0226-trace-Add-migrate-disabled-counter-to-tracing-output.patch
Patch527: 0227-locking-don-t-check-for-__LINUX_SPINLOCK_TYPES_H-on-.patch
Patch528: 0228-locking-Make-spinlock_t-and-rwlock_t-a-RCU-section-o.patch
Patch529: 0229-mm-vmalloc-Another-preempt-disable-region-which-suck.patch
Patch530: 0230-block-mq-do-not-invoke-preempt_disable.patch
Patch531: 0231-md-raid5-Make-raid5_percpu-handling-RT-aware.patch
Patch532: 0232-scsi-fcoe-Make-RT-aware.patch
Patch533: 0233-sunrpc-Make-svc_xprt_do_enqueue-use-get_cpu_light.patch
Patch534: 0234-rt-Introduce-cpu_chill.patch
Patch535: 0235-fs-namespace-Use-cpu_chill-in-trylock-loops.patch
Patch536: 0236-net-Use-skbufhead-with-raw-lock.patch
Patch537: 0237-net-Dequeue-in-dev_cpu_dead-without-the-lock.patch
Patch538: 0238-net-dev-always-take-qdisc-s-busylock-in-__dev_xmit_s.patch
Patch539: 0239-irqwork-push-most-work-into-softirq-context.patch
Patch540: 0240-x86-crypto-Reduce-preempt-disabled-regions.patch
Patch541: 0241-crypto-Reduce-preempt-disabled-regions-more-algos.patch
Patch542: 0242-crypto-limit-more-FPU-enabled-sections.patch
Patch543: 0243-panic-skip-get_random_bytes-for-RT_FULL-in-init_oops.patch
Patch544: 0244-x86-stackprotector-Avoid-random-pool-on-rt.patch
Patch545: 0245-net-Remove-preemption-disabling-in-netif_rx.patch
Patch546: 0246-lockdep-Make-it-RT-aware.patch
Patch547: 0247-lockdep-selftest-Only-do-hardirq-context-test-for-ra.patch
Patch548: 0248-lockdep-selftest-fix-warnings-due-to-missing-PREEMPT.patch
Patch549: 0249-lockdep-disable-self-test.patch
Patch550: 0250-drm-radeon-i915-Use-preempt_disable-enable_rt-where-.patch
Patch551: 0251-drm-i915-Don-t-disable-interrupts-on-PREEMPT_RT-duri.patch
Patch552: 0252-drm-i915-disable-tracing-on-RT.patch
Patch553: 0253-drm-i915-skip-DRM_I915_LOW_LEVEL_TRACEPOINTS-with-NO.patch
Patch554: 0254-drm-i915-gt-Only-disable-interrupts-for-the-timeline.patch
Patch555: 0255-cpuset-Convert-callback_lock-to-raw_spinlock_t.patch
Patch556: 0256-x86-Allow-to-enable-RT.patch
Patch557: 0257-mm-scatterlist-Do-not-disable-irqs-on-RT.patch
Patch558: 0258-sched-Add-support-for-lazy-preemption.patch
Patch559: 0259-x86-entry-Use-should_resched-in-idtentry_exit_cond_r.patch
Patch560: 0260-x86-Support-for-lazy-preemption.patch
Patch561: 0261-arm-Add-support-for-lazy-preemption.patch
Patch562: 0262-powerpc-Add-support-for-lazy-preemption.patch
Patch563: 0263-arch-arm64-Add-lazy-preempt-support.patch
Patch564: 0264-jump-label-disable-if-stop_machine-is-used.patch
Patch565: 0265-leds-trigger-disable-CPU-trigger-on-RT.patch
Patch566: 0266-tty-serial-omap-Make-the-locking-RT-aware.patch
Patch567: 0267-tty-serial-pl011-Make-the-locking-work-on-RT.patch
Patch568: 0268-ARM-enable-irq-in-translation-section-permission-fau.patch
Patch569: 0269-genirq-update-irq_set_irqchip_state-documentation.patch
Patch570: 0270-KVM-arm-arm64-downgrade-preempt_disable-d-region-to-.patch
Patch571: 0271-arm64-fpsimd-Delay-freeing-memory-in-fpsimd_flush_th.patch
Patch572: 0272-x86-Enable-RT-also-on-32bit.patch
Patch573: 0273-ARM-Allow-to-enable-RT.patch
Patch574: 0274-ARM64-Allow-to-enable-RT.patch
Patch575: 0275-powerpc-traps-Use-PREEMPT_RT.patch
Patch576: 0276-powerpc-pseries-iommu-Use-a-locallock-instead-local_.patch
Patch577: 0277-powerpc-kvm-Disable-in-kernel-MPIC-emulation-for-PRE.patch
Patch578: 0278-powerpc-stackprotector-work-around-stack-guard-init-.patch
Patch579: 0279-powerpc-Avoid-recursive-header-includes.patch
Patch580: 0280-POWERPC-Allow-to-enable-RT.patch
Patch581: 0281-drivers-block-zram-Replace-bit-spinlocks-with-rtmute.patch
Patch582: 0282-tpm_tis-fix-stall-after-iowrite-s.patch
Patch583: 0283-signals-Allow-rt-tasks-to-cache-one-sigqueue-struct.patch
Patch584: 0284-signal-Prevent-double-free-of-user-struct.patch
Patch585: 0285-genirq-Disable-irqpoll-on-rt.patch
Patch586: 0286-sysfs-Add-sys-kernel-realtime-entry.patch
Patch587: 0287-Add-localversion-for-RT-release.patch
Patch588: 0288-net-xfrm-Use-sequence-counter-with-associated-spinlo.patch
Patch589: 0289-sched-Fix-migration_cpu_stop-requeueing.patch
Patch590: 0290-sched-Simplify-migration_cpu_stop.patch
Patch591: 0291-sched-Collate-affine_move_task-stoppers.patch
Patch592: 0292-sched-Optimize-migration_cpu_stop.patch
Patch593: 0293-sched-Fix-affine_move_task-self-concurrency.patch
Patch594: 0294-sched-Simplify-set_affinity_pending-refcounts.patch
Patch595: 0295-sched-Don-t-defer-CPU-pick-to-migration_cpu_stop.patch
Patch596: 0296-printk-Enhance-the-condition-check-of-msleep-in-pr_f.patch
Patch597: 0297-locking-rwsem-rt-Remove-might_sleep-in-__up_read.patch
Patch598: 0298-mm-zsmalloc-Convert-zsmalloc_handle.lock-to-spinlock.patch
Patch599: 0299-sched-Fix-get_push_task-vs-migrate_disable.patch
Patch600: 0300-sched-Switch-wait_task_inactive-to-HRTIMER_MODE_REL_.patch
Patch601: 0301-preempt-Move-preempt_enable_no_resched-to-the-RT-blo.patch
Patch602: 0302-mm-Disable-NUMA_BALANCING_DEFAULT_ENABLED-and-TRANSP.patch
Patch603: 0303-fscache-Use-only-one-fscache_object_cong_wait.patch
Patch604: 0304-fscache-Use-only-one-fscache_object_cong_wait.patch
Patch605: 0305-locking-Drop-might_resched-from-might_sleep_no_state.patch
Patch606: 0306-drm-i915-gt-Queue-and-wait-for-the-irq_work-item.patch
Patch607: 0307-irq_work-Allow-irq_work_sync-to-sleep-if-irq_work-no.patch
Patch608: 0308-irq_work-Handle-some-irq_work-in-a-per-CPU-thread-on.patch
Patch609: 0309-irq_work-Also-rcuwait-for-IRQ_WORK_HARD_IRQ-on-PREEM.patch
Patch610: 0310-eventfd-Make-signal-recursion-protection-a-task-bit.patch
Patch611: 0311-stop_machine-Remove-this_cpu_ptr-from-print_stop_inf.patch
Patch612: 0312-aio-Fix-incorrect-usage-of-eventfd_signal_allowed.patch
Patch613: 0313-rt-remove-extra-parameter-from-__trace_stack.patch
Patch614: 0314-locking-rtmutex-switch-to-EXPORT_SYMBOL-for-ww_mutex.patch
Patch615: 0315-ftrace-Fix-improper-usage-of-__trace_stack-function.patch
Patch616: 0316-rt-arm64-make-_TIF_WORK_MASK-bits-contiguous.patch
Patch617: 0317-printk-ignore-consoles-without-write-callback.patch
Patch618: 0318-kernel-fork-set-wake_q_sleeper.next-NULL-again-in-du.patch
Patch619: 0319-Revert-mm-page_alloc-fix-potential-deadlock-on-zonel.patch
Patch620: 0320-Revert-printk-declare-printk_deferred_-enter-safe-in.patch
Patch621: 0321-arm64-signal-Use-ARCH_RT_DELAYS_SIGNAL_SEND.patch
# Keep rt_version matched up with this patch.
Patch622: 0322-Linux-5.10.197-rt96-REBASE.patch

#Ignore reading localversion-rt
Patch699: 0001-setlocalversion-Skip-reading-localversion-rt-file.patch

#Photon Specific Changes
Patch700: 0000-Revert-clockevents-Stop-unused-clockevent-devices.patch

# RT Runtime Greed
Patch701: 0001-RT-PATCH-sched-rt-RT_RUNTIME_GREED-sched-feature.patch
Patch702: use-kmsg_dump-iterator-for-RT.patch

# Patchset to conditional restart_tick upon idle_exit
# https://lore.kernel.org/lkml/162091184942.29796.4815200413212139734.tip-bot2@tip-bot2/
Patch703: 0001-tick-nohz-Evaluate-the-CPU-expression-after-the-stat.patch
Patch704: 0002-tick-nohz-Conditionally-restart-tick-on-idle-exit.patch
Patch705: 0003-tick-nohz-Remove-superflous-check-for-CONFIG_VIRT_CP.patch
Patch706: 0004-tick-nohz-Update-idle_exittime-on-actual-idle-exit.patch
Patch707: 0005-tick-nohz-Update-nohz_full-Kconfig-help.patch
Patch708: 0006-tick-nohz-Only-wakeup-a-single-target-cpu-when-kicki.patch
Patch709: 0007-tick-nohz-Change-signal-tick-dependency-to-wakeup-CP.patch
Patch710: 0008-tick-nohz-Kick-only-_queued_-task-whose-tick-depende.patch
Patch711: 0009-tick-nohz-Call-tick_nohz_task_switch-with-interrupts.patch
Patch712: 0010-MAINTAINERS-Add-myself-as-context-tracking-maintaine.patch

#Patch to enable nohz with idle=poll
Patch713: 0001-Allow-tick-sched-timer-to-be-turned-off-in-idle-poll.patch

# Disable md5 algorithm for sctp if fips is enabled.
Patch714: 0001-disable-md5-algorithm-for-sctp-if-fips-is-enabled.patch

#Backport hrtick changes
Patch715: 0001-sched-features-Distinguish-between-NORMAL-and-DEADLI.patch

#Patch to add timer padding on guest
Patch716: 0001-timer-padding-on-guest.patch

# Crypto:
# Patch to invoke crypto self-tests and add missing test vectors to testmgr
Patch1000: 0002-FIPS-crypto-self-tests.patch
# Patch to call drbg and dh crypto tests from tcrypt
Patch1001: tcrypt-disable-tests-that-are-not-enabled-in-photon.patch
Patch1002: 0001-Initialize-jitterentropy-before-ecdh.patch
# Patch to remove urandom usage in rng module
Patch1003: 0001-FIPS-crypto-rng-Jitterentropy-RNG-as-the-only-RND-source.patch
# Patch to remove urandom usage in drbg and ecc modules
Patch1004: 0003-FIPS-crypto-drbg-Jitterentropy-RNG-as-the-only-RND.patch

%ifarch x86_64
Patch1006: 0001-changes-to-build-with-jitterentropy-v3.4.1.patch
%endif

%if 0%{?fips}
# FIPS canister usage patch
Patch1008: 0001-FIPS-canister-binary-usage.patch
Patch1009: 0001-scripts-kallsyms-Extra-kallsyms-parsing.patch
Patch1010: FIPS-do-not-allow-not-certified-algos-in-fips-2.patch
%else
%if 0%{?kat_build}
Patch1011: 0003-FIPS-broken-kattest.patch
%endif
%endif

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
BuildRequires:  xml-security-c-devel
BuildRequires:  libdnet-devel
BuildRequires:  libmspack-devel
BuildRequires:  Linux-PAM-devel
BuildRequires:  openssl-devel
BuildRequires:  procps-ng-devel
BuildRequires:  audit-devel
BuildRequires:  python3-macros
BuildRequires:  elfutils-libelf-devel
BuildRequires:  bison
BuildRequires:  dwarves-devel

%if 0%{?fips}
BuildRequires: gdb
%endif

Requires: kmod
Requires: filesystem
Requires(pre): (coreutils or coreutils-selinux)
Requires(preun): (coreutils or coreutils-selinux)
Requires(post): (coreutils or coreutils-selinux)
Requires(postun): (coreutils or coreutils-selinux)

%description
The Linux package contains the Linux kernel with RT (real-time)
features.
Built with rt patchset version %{rt_version}.
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

%package docs
Summary:        Kernel docs
Group:          System Environment/Kernel
Requires:       python3
%description docs
The Linux package contains the Linux kernel doc files

%prep
# Using autosetup is not feasible
%setup -q -n linux-%{version}
%ifarch x86_64
# Using autosetup is not feasible
%setup -q -T -D -b 6 -n linux-%{version}
# Using autosetup is not feasible
%setup -q -T -D -b 7 -n linux-%{version}
# Using autosetup is not feasible
%setup -q -T -D -b 8 -n linux-%{version}
%endif
%if 0%{?fips}
# Using autosetup is not feasible
%setup -q -T -D -b 16 -n linux-%{version}
%endif

%ifarch x86_64
# Using autosetup is not feasible
%setup -q -T -D -b 32 -n linux-%{version}
%endif

%autopatch -p1 -m0 -M46

#VMW
%autopatch -p1 -m55 -M57

# CVE
%autopatch -p1 -m100 -M134

# Allow PCI resets to be disabled from vfio_pci module
%autopatch -p1 -m200 -M201

%autopatch -p1 -m202 -M202

# RT
%autopatch -p1 -m301 -M716

%autopatch -p1 -m1000 -M1004

%ifarch x86_64
%autopatch -p1 -m1006 -M1006
%endif

%if 0%{?fips}
%autopatch -p1 -m1008 -M1010
%else
%if 0%{?kat_build}
%patch1011 -p1
%endif
%endif

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

%build
%ifarch x86_64
cp -r ../jitterentropy-%{jent_major_version}-%{jent_ph_version}/ \
      crypto/jitterentropy-%{jent_major_version}/
cp %{SOURCE33} crypto/jitterentropy-%{jent_major_version}/
cp %{SOURCE34} crypto/jitterentropy-%{jent_major_version}/
cp %{SOURCE35} crypto/jitterentropy-%{jent_major_version}/
%endif

make %{?_smp_mflags} mrproper

%ifarch x86_64
cp %{SOURCE1} .config
arch="x86_64"
%endif
%if 0%{?fips}
cp ../fips-canister-%{fips_canister_version}/fips_canister.o \
   ../fips-canister-%{fips_canister_version}/fips_canister_wrapper.c \
   ../fips-canister-%{fips_canister_version}/.fips_canister.o.cmd \
   ../fips-canister-%{fips_canister_version}/fips_canister-kallsyms \
   ../fips-canister-%{fips_canister_version}/fips_canister_wrapper_asm.S \
   ../fips-canister-%{fips_canister_version}/fips_canister_wrapper_internal.h \
   ../fips-canister-%{fips_canister_version}/aesni-intel_glue_fips_canister_wrapper.c \
   ../fips-canister-%{fips_canister_version}/testmgr_fips_canister_wrapper.c \
   crypto/
%endif

sed -i 's/CONFIG_LOCALVERSION="-rt"/CONFIG_LOCALVERSION="-%{release}-rt"/' .config

%if 0%{?kat_build}
sed -i '/CONFIG_CRYPTO_SELF_TEST=y/a CONFIG_CRYPTO_BROKEN_KAT=y' .config
%endif

%include %{SOURCE5}

make %{?_smp_mflags} V=1 KBUILD_BUILD_VERSION="1-photon" \
    KBUILD_BUILD_HOST="photon" ARCH=${arch} %{?_smp_mflags}

%if 0%{?fips}
%include %{SOURCE9}
%endif

%ifarch x86_64

# build i40e module
bldroot="${PWD}"
pushd ../i40e-%{i40e_version}
make %{?_smp_mflags} -C src KSRC=${bldroot} clean
make -C src KSRC=${bldroot} %{?_smp_mflags}
popd

# build iavf module
pushd ../iavf-%{iavf_version}
make %{?_smp_mflags} -C src KSRC=${bldroot} clean
make -C src KSRC=${bldroot} %{?_smp_mflags}
popd

# build ice module
pushd ../ice-%{ice_version}
make %{?_smp_mflags} -C src KSRC=${bldroot} clean
make -C src KSRC=${bldroot} %{?_smp_mflags}
popd
%endif

%install
install -vdm 755 %{buildroot}%{_sysconfdir}
install -vdm 755 %{buildroot}/boot
install -vdm 755 %{buildroot}%{_docdir}/linux-%{uname_r}
install -vdm 755 %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}
install -vdm 755 %{buildroot}%{_libdir}/debug/%{_modulesdir}
make %{?_smp_mflags} INSTALL_MOD_PATH=%{buildroot} modules_install

%ifarch x86_64

# The auxiliary.ko kernel module is a common dependency for i40e, iavf
# and ice drivers.  Install it only once, along with the iavf driver
# and re-use it in the ice and i40e drivers.

# install i40e module
bldroot="${PWD}"
pushd ../i40e-%{i40e_version}
make %{?_smp_mflags} -C src KSRC=${bldroot} INSTALL_MOD_PATH=%{buildroot} \
    INSTALL_MOD_DIR=extra MANDIR=%{_mandir} modules_install_no_aux mandocs_install
popd

# install iavf module
pushd ../iavf-%{iavf_version}
make -C src KSRC=$bldroot INSTALL_MOD_PATH=%{buildroot} INSTALL_MOD_DIR=extra \
    INSTALL_AUX_DIR=extra/auxiliary MANDIR=%{_mandir} modules_install \
    mandocs_install %{?_smp_mflags}
install -Dvm 644 src/linux/auxiliary_bus.h \
    %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}/include/linux/auxiliary_bus.h
popd

# install ice module
pushd ../ice-%{ice_version}
make -C src KSRC=${bldroot} MANDIR=%{_mandir} INSTALL_MOD_PATH=%{buildroot} \
            mandocs_install %{?_smp_mflags}
make %{?_smp_mflags} -C src KSRC=${bldroot} INSTALL_MOD_PATH=%{buildroot} \
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
photon_cmdline=init=/lib/systemd/systemd ro loglevel=3 quiet nosoftlockup intel_idle.max_cstate=0 mce=ignore_ce nowatchdog cpuidle.off=1 nmi_watchdog=0 audit=0
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

mkdir -p %{buildroot}%{_modulesdir}/dracut.conf.d/
cp -p %{SOURCE22} %{buildroot}%{_modulesdir}/dracut.conf.d/%{name}.conf

%include %{SOURCE2}
%include %{SOURCE4}
%include %{SOURCE21}

%post
/sbin/depmod -a %{uname_r}
ln -sf linux-%{uname_r}.cfg /boot/photon.cfg

%files
%defattr(-,root,root)
/boot/System.map-%{uname_r}
/boot/config-%{uname_r}
/boot/vmlinuz-%{uname_r}
%config(noreplace) /boot/linux-%{uname_r}.cfg
%defattr(0644,root,root)
%{_modulesdir}/*
%exclude %{_modulesdir}/build
# iavf.conf is used to just blacklist the deprecated i40evf
# and create alias of i40evf to iavf.
# By default iavf is used for VF driver.
# This file creates conflict with other flavour of linux
# thus excluding this file from packaging
%exclude %{_sysconfdir}/modprobe.d/iavf.conf
# ICE driver firmware files are packaged in linux-firmware
%exclude /lib/firmware/updates/intel/ice

%config(noreplace) %{_modulesdir}/dracut.conf.d/%{name}.conf

%files docs
%defattr(-,root,root)
%{_defaultdocdir}/linux-%{uname_r}/*
%{_mandir}/*

%files devel
%defattr(-,root,root)
%{_modulesdir}/build
%{_usrsrc}/linux-headers-%{uname_r}

%changelog
* Thu Oct 26 2023 Srish Srinivasan <ssrish@vmware.com> 5.10.198-3
- Upgrade canister to 5.0.0-6.1.56-6
* Fri Oct 13 2023 Srish Srinivasan <ssrish@vmware.com> 5.10.198-2
- Ensure all the necessary crypto self-tests are run irrespective
  of whether the canister is used in the kernel build or not
- Fix tcrypt tests
- Apply jitterentropy builder patch before canister binary usage patch
* Fri Oct 13 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 5.10.198-1
- Update to version 5.10.198
- Fix CVE-2023-4244
- Update canister to 5.0.0-6.1.56-3
* Tue Oct 03 2023 Keerthana K <keerthanak@vmware.com> 5.10.197-1
- Update to version 5.10.197
* Fri Sep 29 2023 Srinidhi Rao <srinidhir@vmware.com> 5.10.190-2
- Jitterentropy wrapper changes.
* Wed Sep 27 2023 Keerthana K <keerthanak@vmware.com> 5.10.190-1
- Update to version 5.10.190
* Fri Sep 15 2023 Srish Srinivasan <ssrish@vmware.com> 5.10.183-6
- Use canister version 5.0.0-6.1.45-7
* Tue Sep 12 2023 Keerthana K <keerthanak@vmware.com> 5.10.183-5
- Build with jitterentropy v3.4.1-1
* Fri Sep 08 2023 Keerthana K <keerthanak@vmware.com> 5.10.183-4
- Use canister version 5.0.0-6.1.45-4
* Mon Jul 17 2023 Keerthana K <keerthanak@vmware.com> 5.10.183-3
- Use canister version 5.0.0-6.1.37-2
* Tue Jul 04 2023 Keerthana K <keerthanak@vmware.com> 5.10.183-2
- Use canister 5.0.0-6.1.10-18
* Thu Jun 08 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 5.10.183-1
- Update to version 5.10.183, fix some CVEs
* Wed May 17 2023 Ankit Jain <ankitja@vmware.com> 5.10.180-1
- Update to version 5.10.180
* Mon May 08 2023 Srish Srinivasan <ssrish@vmware.com> 5.10.175-5
- Enable CONFIG_DEBUG_INFO_BTF=y
* Wed Apr 12 2023 Shreenidhi Shedi <sshedi@vmware.com> 5.10.175-4
- Fix initrd generation logic
* Tue Apr 11 2023 Roye Eshed <eshedr@vmware.com> 5.10.175-3
- Fix for CVE-2022-39189
* Mon Apr 10 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 5.10.175-2
- update to latest ToT vmxnet3 driver pathes
* Tue Apr 04 2023 Roye Eshed <eshedr@vmware.com> 5.10.175-1
- Update to version 5.10.175
* Tue Apr 04 2023 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.168-5
- Fix IRQ affinity of i40e driver
* Thu Mar 30 2023 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.168-4
- Expose Photon kernel macros to simplify building out-of-tree drivers.
* Mon Mar 20 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 5.10.168-3
- Update intel ethernet drivers
- iavf: 4.8.2
- i40e: 2.22.18
- ice: 1.11.14
* Fri Feb 24 2023 Ankit Jain <ankitja@vmware.com> 5.10.168-2
- Exclude iavf.conf
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
* Mon Oct 17 2022 Sharan Turlapati <sturlapati@vmware.com> 5.10.142-3
- Fix for CVE-2022-2602
* Thu Oct 13 2022 Sharan Turlapati <sturlapati@vmware.com> 5.10.142-2
- Fixes for CVEs in the wifi subsystem
* Fri Sep 09 2022 srinidhira0 <srinidhir@vmware.com> 5.10.142-1
- Update to version 5.10.142
* Tue Aug 23 2022 Shivani Agarwal <shivania2@vmware.com> 5.10.132-2
- .config: Enable MPLS and other routing related options, namely,
- CGROUP_BPF, XFRM_INTERFACE, NFT_XFRM, NETFILTER_XT_TARGET_NOTRACK
- NET_ACT_BPF, MPLS_ROUTING, MPLS_IPTUNNEL, LWTUNNEL, LWTUNNEL_BPF, PPP
* Tue Aug 16 2022 srinidhira0 <srinidhir@vmware.com> 5.10.132-1
- Update to version 5.10.132
* Fri Aug 12 2022 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 5.10.118-19
- Backport fixes for CVE-2022-0500
* Wed Aug 10 2022 Shreenidhi Shedi <sshedi@vmware.com> 5.10.118-18
- Scriptlets fixes and improvements
* Wed Aug 10 2022 Sharan Turlapati <sturlapati@vmware.com> 5.10.118-17
- Correct SPEC file to autopatch vfio_pci patches
* Fri Aug 05 2022 Him Kalyan Bordoloi <bordoloih@vmware.com> 5.10.118-16
- Fix for CVE-2022-2585, CVE-2022-2586 and CVE-2022-2588
* Thu Jul 28 2022 Keerthana K <keerthanak@vmware.com> 5.10.118-15
- Fix linux headers, doc folder and linux-<uname -r>.cfg names
- Drop rt_version from uname_r
- Patch to skip reading localversion-rt
* Mon Jul 18 2022 Keerthana K <keerthanak@vmware.com> 5.10.118-14
- Update iavf driver to v4.4.2
- Update ice driver to v1.8.3
* Mon Jul 18 2022 Keerthana K <keerthanak@vmware.com> 5.10.118-13
- .config: enable CROSS_MEMORY_ATTACH
- Add elfutils-libelf-devel required to build objtool
* Mon Jul 18 2022 Keerthana K <keerthanak@vmware.com> 5.10.118-12
- Patch for timer padding on guest
* Fri Jul 15 2022 Keerthana K <keerthanak@vmware.com> 5.10.118-11
- Backport hrtick changes to fix lost timer wakeups
* Fri Jul 15 2022 Keerthana K <keerthanak@vmware.com> 5.10.118-10
- .config: enable CONFIG_NET_ACT_SIMP
* Fri Jul 15 2022 Keerthana K <keerthanak@vmware.com> 5.10.118-9
- Enable cgroup v1 stats
- .config: enable PERCPU_STATS
* Fri Jul 15 2022 Keerthana K <keerthanak@vmware.com> 5.10.118-8
- Avoid TSC recalibration
* Fri Jul 15 2022 Keerthana K <keerthanak@vmware.com> 5.10.118-7
- Enable config options needed to build N3000 FPGA driver.
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
- Enable config_livepatch
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
- crypto_self_test and broken kattest module enhancements
* Fri Dec 17 2021 Alexey Makhalov <amakhalov@vmware.com> 5.10.83-5
- mm: fix percpu alloacion for memoryless nodes
- pvscsi: fix disk detection issue
* Fri Dec 17 2021 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 5.10.83-4
- Disable md5 algorithm for sctp if fips is enabled.
* Tue Dec 14 2021 Harinadh D <hdommaraju@vmware.com> 5.10.83-3
- remove lvm in add-drivers list
- lvm drivers are built as part of dm-mod
* Thu Dec 09 2021 Prashant S Chauhan <psinghchauha@vmware.com> 5.10.83-2
- Bump up to compile with python 3.10
* Mon Dec 06 2021 srinidhira0 <srinidhir@vmware.com> 5.10.83-1
- Update to version 5.10.83
* Mon Nov 29 2021 Srinidhi Rao <srinidhir@vmware.com> 5.10.78-7
- Enable eBPF Net Packet filter support.
* Thu Nov 18 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 5.10.78-6
- Add vhost and vhost-net drivers in config
* Thu Nov 18 2021 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.78-5
- Add PCI quirk to allow multiple devices under the same virtual
- PCI bridge to be put into separate IOMMU groups.
* Wed Nov 17 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 5.10.78-4
- Enable nohz for idle=poll
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
* Thu Jun 24 2021 Ankit Jain <ankitja@vmware.com> 5.10.42-4
- Conditional tick_restart upon idle_exit
* Tue Jun 22 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.42-3
- Fix for CVE-2021-3609
* Thu Jun 10 2021 Keerthana K <keerthanak@vmware.com> 5.10.42-2
- Added script to check structure compatibility between fips_canister.o and vmlinux.
* Thu Jun 03 2021 Keerthana K <keerthanak@vmware.com> 5.10.42-1
- Update to version 5.10.42
- Remove XR usb driver support
- .config: Enable CONFIG_FANOTIFY_ACCESS_PERMISSIONS
* Wed Jun 02 2021 Keerthana K <keerthanak@vmware.com> 5.10.35-3
- Fix for CVE-2021-3573
* Thu May 20 2021 Ajay Kaher <akaher@vmware.com> 5.10.35-2
- Fix for CVE-2021-3564
* Mon May 17 2021 Ajay Kaher <akaher@vmware.com> 5.10.35-1
- Update to version 5.10.35
* Thu May 13 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.25-10
- Fix for CVE-2021-23133
* Tue May 11 2021 Ankit Jain <ankitja@vmware.com> 5.10.25-9
- .config: Enable INFINIBAND, MLX5_INFINIBAND
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
* Wed Mar 17 2021 Srinidhi Rao <srinidhir@vmware.com> 5.10.21-2
- Use jitterentropy rng instead of urandom in rng module.
* Tue Mar 16 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 5.10.21-1
- Update to version 5.10.21
* Mon Mar 01 2021 Alexey Makhalov <amakhalov@vmware.com> 5.10.4-10
- FIPS canister update
* Thu Feb 18 2021 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.4-9
- Fix /boot/photon.cfg symlink when /boot is a separate partition.
* Thu Feb 18 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.4-8
- Enable CONFIG_IFB
* Wed Feb 17 2021 Ankit Jain <ankitja@vmware.com> 5.10.4-7
- Added latest out of tree version of Intel ice driver
* Wed Feb 17 2021 Vikash Bansal <bvikas@vmware.com> 5.10.4-6
- Added support for RT RUNTIME GREED
* Mon Feb 15 2021 Keerthana K <keerthanak@vmware.com> 5.10.4-5
- Added crypto_self_test and kattest module.
- These patches are applied when kat_build is enabled.
* Wed Feb 03 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 5.10.4-4
- Update i40e driver to v2.13.10
- Add out of tree iavf driver
- Enable CONFIG_NET_TEAM
* Wed Jan 27 2021 Alexey Makhalov <amakhalov@vmware.com> 5.10.4-3
- Build kernel with FIPS canister.
* Mon Jan 25 2021 Ankit Jain <ankitja@vmware.com> 5.10.4-2
- Enabled CONFIG_WIREGUARD
* Mon Jan 11 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 5.10.4-1
- Update to version 5.10.4
* Tue Nov 10 2020 Keerthana K <keerthanak@vmware.com> 5.9.0-4
- Fix CVE-2020-8694
* Fri Nov 06 2020 Keerthana K <keerthanak@vmware.com> 5.9.0-3
- Fix CVE-2020-25704
* Tue Oct 27 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.9.0-2
- Revert d254087 (clockevents: Stop unused clockevent devices)
- Solve cyclictest regression introduced in 4.1
* Tue Oct 27 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.9.0-1
- Update to version 5.9.0
* Tue Oct 06 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.9.0-rc7.1
- Update to version 5.9.0-rc7
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 4.19.127-2
- openssl 1.1.1
* Tue Jun 23 2020 Keerthana K <keerthanak@vmware.com> 4.19.127-1
- Update to version 4.19.127
* Tue Jun 16 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.115-10
- Add latest out of tree version of i40e driver
* Wed Jun 10 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.115-9
- Enable CONFIG_VFIO_NOIOMMU
* Fri Jun 05 2020 Ankit Jain <ankitja@vmware.com> 4.19.115-8
- Enabled CONFIG_BINFMT_MISC
* Tue Jun 02 2020 Vikash Bansal <bvikas@vmware.com> 4.19.115-7
- Add patch to fix CVE-2019-18885
* Fri May 29 2020 Shreenidhi Shedi <sshedi@vmware.com> 4.19.115-6
- Keep modules of running kernel till next boot
* Fri May 22 2020 Tapas Kundu <tkundu@vmware.com> 4.19.115-5
- Deprecate linux-rt-tools in favor of linux-tools.
- Deprecate python3-perf in favor of linux-python3-perf.
* Thu May 21 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.115-4
- Add ICE network driver support in config
* Fri May 15 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.115-3
- Add uio_pic_generic driver support in config
* Wed May 06 2020 Siddharth Chandrasekaran <csiddharth@vmware.com> 4.19.115-2
- Add patch to fix CVE-2020-10711
* Wed May 06 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.115-1
- Upgrade to 4.19.115
* Wed Apr 29 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.98-5
- Enable additional config options.
* Mon Mar 23 2020 Alexey Makhalov <amakhalov@vmware.com> 4.19.98-4
- Fix perf compilation issue with binutils >= 2.34.
* Sun Mar 22 2020 Tapas Kundu <tkundu@vmware.com> 4.19.98-3
- Added python3-perf subpackage
* Tue Mar 17 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.98-2
- Add tools subpackage to include perf, turbostat and cpupower.
- Update the last few perf python scripts in Linux kernel to use
- python3 syntax.
* Tue Jan 28 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.98-1
- Upgrade to 4.19.98
* Thu Jan 16 2020 Srinidhi Rao <srinidhir@vmware.com> 4.19.82-4
- Enable DRBG HASH and DRBG CTR support.
* Fri Jan 03 2020 Keerthana K <keerthanak@vmware.com> 4.19.82-3
- Remove FIPS patch that enables fips for algorithms which are not fips allowed.
* Thu Dec 12 2019 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.82-2
- Fix patch that wont apply on 4.19.82. Revert when upgraded to 4.19.87 or more
* Tue Nov 12 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.82-1
- Introduce a new kernel flavor 'linux-rt' supporting real-time (RT) features.
