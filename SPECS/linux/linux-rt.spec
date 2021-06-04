%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%global security_hardening none

%ifarch x86_64
%define arch x86_64
%define archdir x86

# Set this flag to 0 to build without canister
%global fips 1

# If kat_build is enabled, canister is not used.
%if 0%{?kat_build:1}
%global fips 0
%endif

%endif

Summary:        Kernel
Name:           linux-rt
Version:        5.10.42
# Keep rt_version matched up with localversion.patch
%define rt_version rt42
Release:        1%{?kat_build:.kat}%{?dist}
License:    	GPLv2
URL:        	http://www.kernel.org/
Group:        	System Environment/Kernel
Vendor:         VMware, Inc.
Distribution: 	Photon

%define uname_r %{version}-%{rt_version}-%{release}-rt

Source0:        http://www.kernel.org/pub/linux/kernel/v5.x/linux-%{version}.tar.xz
%define sha1 linux=e6346df31e1623af112c154c412f96f59487dbeb
Source1:	config-rt
Source2:	initramfs.trigger
Source4:        pre-preun-postun-tasks.inc
Source5:        check_for_config_applicability.inc
%define i40e_version 2.13.10
Source6:	https://sourceforge.net/projects/e1000/files/i40e%20stable/%{i40e_version}/i40e-%{i40e_version}.tar.gz
%define sha1 i40e=126bfdabd708033b38840e49762d7ec3e64bbc96
%define iavf_version 4.0.2
Source7:       https://sourceforge.net/projects/e1000/files/iavf%20stable/%{iavf_version}/iavf-%{iavf_version}.tar.gz
%define sha1 iavf=a53cb104a3b04cbfbec417f7cadda6fddf51b266
%define ice_version 1.3.2
Source8:       https://sourceforge.net/projects/e1000/files/ice%20stable/%{ice_version}/ice-%{ice_version}.tar.gz
%define sha1 ice=19507794824da33827756389ac8018aa84e9c427
%if 0%{?fips}
%define fips_canister_version 4.0.1-5.10.21-3-secure
Source16:       fips-canister-%{fips_canister_version}.tar.bz2
%define sha1 fips-canister=e793f09579cf7b17608095ed80c973000f5f8407
%endif
Source17:        modify_kernel_configs.inc

# common
Patch0:         net-Double-tcp_mem-limits.patch
Patch1:         SUNRPC-Do-not-reuse-srcport-for-TIME_WAIT-socket.patch
Patch2:         SUNRPC-xs_bind-uses-ip_local_reserved_ports.patch
Patch3:         9p-transport-for-9p.patch
Patch4:         9p-trans_fd-extend-port-variable-to-u32.patch
Patch5:         vsock-delay-detach-of-QP-with-outgoing-data-59.patch
# RDRAND-based RNG driver to enhance the kernel's entropy pool:
Patch6:         hwrng-rdrand-Add-RNG-driver-based-on-x86-rdrand-inst.patch

# ttyXRUSB support
Patch10:        usb-acm-exclude-exar-usb-serial-ports-nxt.patch

Patch12:        fork-add-sysctl-to-disallow-unprivileged-CLONE_NEWUSER-by.patch
# Out-of-tree patches from AppArmor:
Patch13:        apparmor-patch-to-provide-compatibility-with-v2.x-ne.patch
Patch14:        apparmor-af_unix-mediation.patch

#vmxnet3
Patch20:        0001-vmxnet3-Remove-buf_info-from-device-accessible-struc.patch

# VMW:
Patch55:        x86-vmware-Use-Efficient-and-Correct-ALTERNATIVEs-fo-510.patch
Patch56:        x86-vmware-Log-kmsg-dump-on-panic-510.patch

# CVE:
Patch100:       apparmor-fix-use-after-free-in-sk_peer_label.patch
# Fix for CVE-2019-12379
Patch101:       consolemap-Fix-a-memory-leaking-bug-in-drivers-tty-v.patch
# Fix for CVE-2021-3564
Patch128:       0001-Bluetooth-fix-the-erroneous-flush_work-order.patch
# Fix for CVE-2021-3573
Patch129:       0001-bluetooth-use-correct-lock-to-prevent-UAF-of-hdev-ob.patch

# Real-Time kernel (PREEMPT_RT patches)
# Source: http://cdn.kernel.org/pub/linux/kernel/projects/rt/5.10/
Patch301:       0001-z3fold-remove-preempt-disabled-sections-for-RT.patch
Patch302:       0002-stop_machine-Add-function-and-caller-debug-info.patch
Patch303:       0003-sched-Fix-balance_callback.patch
Patch304:       0004-sched-hotplug-Ensure-only-per-cpu-kthreads-run-durin.patch
Patch305:       0005-sched-core-Wait-for-tasks-being-pushed-away-on-hotpl.patch
Patch306:       0006-workqueue-Manually-break-affinity-on-hotplug.patch
Patch307:       0007-sched-hotplug-Consolidate-task-migration-on-CPU-unpl.patch
Patch308:       0008-sched-Fix-hotplug-vs-CPU-bandwidth-control.patch
Patch309:       0009-sched-Massage-set_cpus_allowed.patch
Patch310:       0010-sched-Add-migrate_disable.patch
Patch311:       0011-sched-Fix-migrate_disable-vs-set_cpus_allowed_ptr.patch
Patch312:       0012-sched-core-Make-migrate-disable-and-CPU-hotplug-coop.patch
Patch313:       0013-sched-rt-Use-cpumask_any-_distribute.patch
Patch314:       0014-sched-rt-Use-the-full-cpumask-for-balancing.patch
Patch315:       0015-sched-lockdep-Annotate-pi_lock-recursion.patch
Patch316:       0016-sched-Fix-migrate_disable-vs-rt-dl-balancing.patch
Patch317:       0017-sched-proc-Print-accurate-cpumask-vs-migrate_disable.patch
Patch318:       0018-sched-Add-migrate_disable-tracepoints.patch
Patch319:       0019-sched-Deny-self-issued-__set_cpus_allowed_ptr-when-m.patch
Patch320:       0020-sched-Comment-affine_move_task.patch
Patch321:       0021-sched-Unlock-the-rq-in-affine_move_task-error-path.patch
Patch322:       0022-sched-Fix-migration_cpu_stop-WARN.patch
Patch323:       0023-sched-core-Add-missing-completion-for-affine_move_ta.patch
Patch324:       0024-mm-highmem-Un-EXPORT-__kmap_atomic_idx.patch
Patch325:       0025-highmem-Remove-unused-functions.patch
Patch326:       0026-fs-Remove-asm-kmap_types.h-includes.patch
Patch327:       0027-sh-highmem-Remove-all-traces-of-unused-cruft.patch
Patch328:       0028-asm-generic-Provide-kmap_size.h.patch
Patch329:       0029-highmem-Provide-generic-variant-of-kmap_atomic.patch
Patch330:       0030-highmem-Make-DEBUG_HIGHMEM-functional.patch
Patch331:       0031-x86-mm-highmem-Use-generic-kmap-atomic-implementatio.patch
Patch332:       0032-arc-mm-highmem-Use-generic-kmap-atomic-implementatio.patch
Patch333:       0033-ARM-highmem-Switch-to-generic-kmap-atomic.patch
Patch334:       0034-csky-mm-highmem-Switch-to-generic-kmap-atomic.patch
Patch335:       0035-microblaze-mm-highmem-Switch-to-generic-kmap-atomic.patch
Patch336:       0036-mips-mm-highmem-Switch-to-generic-kmap-atomic.patch
Patch337:       0037-nds32-mm-highmem-Switch-to-generic-kmap-atomic.patch
Patch338:       0038-powerpc-mm-highmem-Switch-to-generic-kmap-atomic.patch
Patch339:       0039-sparc-mm-highmem-Switch-to-generic-kmap-atomic.patch
Patch340:       0040-xtensa-mm-highmem-Switch-to-generic-kmap-atomic.patch
Patch341:       0041-highmem-Get-rid-of-kmap_types.h.patch
Patch342:       0042-mm-highmem-Remove-the-old-kmap_atomic-cruft.patch
Patch343:       0043-io-mapping-Cleanup-atomic-iomap.patch
Patch344:       0044-Documentation-io-mapping-Remove-outdated-blurb.patch
Patch345:       0045-highmem-High-implementation-details-and-document-API.patch
Patch346:       0046-sched-Make-migrate_disable-enable-independent-of-RT.patch
Patch347:       0047-sched-highmem-Store-local-kmaps-in-task-struct.patch
Patch348:       0048-mm-highmem-Provide-kmap_local.patch
Patch349:       0049-io-mapping-Provide-iomap_local-variant.patch
Patch350:       0050-x86-crashdump-32-Simplify-copy_oldmem_page.patch
Patch351:       0051-mips-crashdump-Simplify-copy_oldmem_page.patch
Patch352:       0052-ARM-mm-Replace-kmap_atomic_pfn.patch
Patch353:       0053-highmem-Remove-kmap_atomic_pfn.patch
Patch354:       0054-drm-ttm-Replace-kmap_atomic-usage.patch
Patch355:       0055-drm-vmgfx-Replace-kmap_atomic.patch
Patch356:       0056-highmem-Remove-kmap_atomic_prot.patch
Patch357:       0057-drm-qxl-Replace-io_mapping_map_atomic_wc.patch
Patch358:       0058-drm-nouveau-device-Replace-io_mapping_map_atomic_wc.patch
Patch359:       0059-drm-i915-Replace-io_mapping_map_atomic_wc.patch
Patch360:       0060-io-mapping-Remove-io_mapping_map_atomic_wc.patch
Patch361:       0061-mm-highmem-Take-kmap_high_get-properly-into-account.patch
Patch362:       0062-highmem-Don-t-disable-preemption-on-RT-in-kmap_atomi.patch
Patch363:       0063-timers-Move-clearing-of-base-timer_running-under-bas.patch
Patch364:       0064-blk-mq-Don-t-complete-on-a-remote-CPU-in-force-threa.patch
Patch365:       0065-blk-mq-Always-complete-remote-completions-requests-i.patch
Patch366:       0066-blk-mq-Use-llist_head-for-blk_cpu_done.patch
Patch367:       0067-lib-test_lockup-Minimum-fix-to-get-it-compiled-on-PR.patch
Patch368:       0068-timers-Don-t-block-on-expiry_lock-for-TIMER_IRQSAFE.patch
Patch369:       0069-kthread-Move-prio-affinite-change-into-the-newly-cre.patch
Patch370:       0070-genirq-Move-prio-assignment-into-the-newly-created-t.patch
Patch371:       0071-notifier-Make-atomic_notifiers-use-raw_spinlock.patch
Patch372:       0072-rcu-Make-RCU_BOOST-default-on-CONFIG_PREEMPT_RT.patch
Patch373:       0073-rcu-Unconditionally-use-rcuc-threads-on-PREEMPT_RT.patch
Patch374:       0074-rcu-Enable-rcu_normal_after_boot-unconditionally-for.patch
Patch375:       0075-doc-Update-RCU-s-requirements-page-about-the-PREEMPT.patch
Patch376:       0076-doc-Use-CONFIG_PREEMPTION.patch
Patch377:       0077-tracing-Merge-irqflags-preempt-counter.patch
Patch378:       0078-tracing-Inline-tracing_gen_ctx_flags.patch
Patch379:       0079-tracing-Use-in_serving_softirq-to-deduct-softirq-sta.patch
Patch380:       0080-tracing-Remove-NULL-check-from-current-in-tracing_ge.patch
Patch381:       0081-printk-inline-log_output-log_store-in-vprintk_store.patch
Patch382:       0082-printk-remove-logbuf_lock-writer-protection-of-ringb.patch
Patch383:       0083-printk-limit-second-loop-of-syslog_print_all.patch
Patch384:       0084-printk-kmsg_dump-remove-unused-fields.patch
Patch385:       0085-printk-refactor-kmsg_dump_get_buffer.patch
Patch386:       0086-printk-consolidate-kmsg_dump_get_buffer-syslog_print.patch
Patch387:       0087-printk-introduce-CONSOLE_LOG_MAX-for-improved-multi-.patch
Patch388:       0088-printk-use-seqcount_latch-for-clear_seq.patch
Patch389:       0089-printk-use-atomic64_t-for-devkmsg_user.seq.patch
Patch390:       0090-printk-add-syslog_lock.patch
Patch391:       0091-printk-introduce-a-kmsg_dump-iterator.patch
Patch392:       0092-um-synchronize-kmsg_dumper.patch
Patch393:       0093-printk-remove-logbuf_lock.patch
Patch394:       0094-printk-kmsg_dump-remove-_nolock-variants.patch
Patch395:       0095-printk-kmsg_dump-use-kmsg_dump_rewind.patch
Patch396:       0096-printk-console-remove-unnecessary-safe-buffer-usage.patch
Patch397:       0097-printk-track-limit-recursion.patch
Patch398:       0098-printk-remove-safe-buffers.patch
Patch399:       0099-printk-convert-syslog_lock-to-spin_lock.patch
Patch400:       0100-console-add-write_atomic-interface.patch
Patch401:       0101-serial-8250-implement-write_atomic.patch
Patch402:       0102-printk-relocate-printk_delay-and-vprintk_default.patch
Patch403:       0103-printk-combine-boot_delay_msec-into-printk_delay.patch
Patch404:       0104-printk-change-console_seq-to-atomic64_t.patch
Patch405:       0105-printk-introduce-kernel-sync-mode.patch
Patch406:       0106-printk-move-console-printing-to-kthreads.patch
Patch407:       0107-printk-remove-deferred-printing.patch
Patch408:       0108-printk-add-console-handover.patch
Patch409:       0109-printk-add-pr_flush.patch
Patch410:       0110-cgroup-use-irqsave-in-cgroup_rstat_flush_locked.patch
Patch411:       0111-mm-workingset-replace-IRQ-off-check-with-a-lockdep-a.patch
Patch412:       0112-tpm-remove-tpm_dev_wq_lock.patch
Patch413:       0113-shmem-Use-raw_spinlock_t-for-stat_lock.patch
Patch414:       0114-net-Move-lockdep-where-it-belongs.patch
Patch415:       0115-tcp-Remove-superfluous-BH-disable-around-listening_h.patch
Patch416:       0116-parisc-Remove-bogus-__IRQ_STAT-macro.patch
Patch417:       0117-sh-Get-rid-of-nmi_count.patch
Patch418:       0118-irqstat-Get-rid-of-nmi_count-and-__IRQ_STAT.patch
Patch419:       0119-um-irqstat-Get-rid-of-the-duplicated-declarations.patch
Patch420:       0120-ARM-irqstat-Get-rid-of-duplicated-declaration.patch
Patch421:       0121-arm64-irqstat-Get-rid-of-duplicated-declaration.patch
Patch422:       0122-asm-generic-irqstat-Add-optional-__nmi_count-member.patch
Patch423:       0123-sh-irqstat-Use-the-generic-irq_cpustat_t.patch
Patch424:       0124-irqstat-Move-declaration-into-asm-generic-hardirq.h.patch
Patch425:       0125-preempt-Cleanup-the-macro-maze-a-bit.patch
Patch426:       0126-softirq-Move-related-code-into-one-section.patch
Patch427:       0127-sh-irq-Add-missing-closing-parentheses-in-arch_show_.patch
Patch428:       0128-sched-cputime-Remove-symbol-exports-from-IRQ-time-ac.patch
Patch429:       0129-s390-vtime-Use-the-generic-IRQ-entry-accounting.patch
Patch430:       0130-sched-vtime-Consolidate-IRQ-time-accounting.patch
Patch431:       0131-irqtime-Move-irqtime-entry-accounting-after-irq-offs.patch
Patch432:       0132-irq-Call-tick_irq_enter-inside-HARDIRQ_OFFSET.patch
Patch433:       0133-smp-Wake-ksoftirqd-on-PREEMPT_RT-instead-do_softirq.patch
Patch434:       0134-net-arcnet-Fix-RESET-flag-handling.patch
Patch435:       0135-tasklets-Replace-barrier-with-cpu_relax-in-tasklet_u.patch
Patch436:       0136-tasklets-Use-static-inlines-for-stub-implementations.patch
Patch437:       0137-tasklets-Provide-tasklet_disable_in_atomic.patch
Patch438:       0138-tasklets-Use-spin-wait-in-tasklet_disable-temporaril.patch
Patch439:       0139-tasklets-Replace-spin-wait-in-tasklet_unlock_wait.patch
Patch440:       0140-tasklets-Replace-spin-wait-in-tasklet_kill.patch
Patch441:       0141-tasklets-Prevent-tasklet_unlock_spin_wait-deadlock-o.patch
Patch442:       0142-net-jme-Replace-link-change-tasklet-with-work.patch
Patch443:       0143-net-sundance-Use-tasklet_disable_in_atomic.patch
Patch444:       0144-ath9k-Use-tasklet_disable_in_atomic.patch
Patch445:       0145-atm-eni-Use-tasklet_disable_in_atomic-in-the-send-ca.patch
Patch446:       0146-PCI-hv-Use-tasklet_disable_in_atomic.patch
Patch447:       0147-firewire-ohci-Use-tasklet_disable_in_atomic-where-re.patch
Patch448:       0148-tasklets-Switch-tasklet_disable-to-the-sleep-wait-va.patch
Patch449:       0149-softirq-Add-RT-specific-softirq-accounting.patch
Patch450:       0150-irqtime-Make-accounting-correct-on-RT.patch
Patch451:       0151-softirq-Move-various-protections-into-inline-helpers.patch
Patch452:       0152-softirq-Make-softirq-control-and-processing-RT-aware.patch
Patch453:       0153-tick-sched-Prevent-false-positive-softirq-pending-wa.patch
Patch454:       0154-rcu-Prevent-false-positive-softirq-warning-on-RT.patch
Patch455:       0155-chelsio-cxgb-Replace-the-workqueue-with-threaded-int.patch
Patch456:       0156-chelsio-cxgb-Disable-the-card-on-error-in-threaded-i.patch
Patch457:       0157-x86-fpu-Simplify-fpregs_-un-lock.patch
Patch458:       0158-x86-fpu-Make-kernel-FPU-protection-RT-friendly.patch
Patch459:       0159-locking-rtmutex-Remove-cruft.patch
Patch460:       0160-locking-rtmutex-Remove-output-from-deadlock-detector.patch
Patch461:       0161-locking-rtmutex-Move-rt_mutex_init-outside-of-CONFIG.patch
Patch462:       0162-locking-rtmutex-Remove-rt_mutex_timed_lock.patch
Patch463:       0163-locking-rtmutex-Handle-the-various-new-futex-race-co.patch
Patch464:       0164-futex-Fix-bug-on-when-a-requeued-RT-task-times-out.patch
Patch465:       0165-locking-rtmutex-Make-lock_killable-work.patch
Patch466:       0166-locking-spinlock-Split-the-lock-types-header.patch
Patch467:       0167-locking-rtmutex-Avoid-include-hell.patch
Patch468:       0168-lockdep-Reduce-header-files-in-debug_locks.h.patch
Patch469:       0169-locking-split-out-the-rbtree-definition.patch
Patch470:       0170-locking-rtmutex-Provide-rt_mutex_slowlock_locked.patch
Patch471:       0171-locking-rtmutex-export-lockdep-less-version-of-rt_mu.patch
Patch472:       0172-sched-Add-saved_state-for-tasks-blocked-on-sleeping-.patch
Patch473:       0173-locking-rtmutex-add-sleeping-lock-implementation.patch
Patch474:       0174-locking-rtmutex-Allow-rt_mutex_trylock-on-PREEMPT_RT.patch
Patch475:       0175-locking-rtmutex-add-mutex-implementation-based-on-rt.patch
Patch476:       0176-locking-rtmutex-add-rwsem-implementation-based-on-rt.patch
Patch477:       0177-locking-rtmutex-add-rwlock-implementation-based-on-r.patch
Patch478:       0178-locking-rtmutex-wire-up-RT-s-locking.patch
Patch479:       0179-locking-rtmutex-add-ww_mutex-addon-for-mutex-rt.patch
Patch480:       0180-locking-rtmutex-Use-custom-scheduling-function-for-s.patch
Patch481:       0181-signal-Revert-ptrace-preempt-magic.patch
Patch482:       0182-preempt-Provide-preempt_-_-no-rt-variants.patch
Patch483:       0183-mm-vmstat-Protect-per-cpu-variables-with-preempt-dis.patch
Patch484:       0184-mm-memcontrol-Disable-preemption-in-__mod_memcg_lruv.patch
Patch485:       0185-xfrm-Use-sequence-counter-with-associated-spinlock.patch
Patch486:       0186-u64_stats-Disable-preemption-on-32bit-UP-SMP-with-RT.patch
Patch487:       0187-fs-dcache-use-swait_queue-instead-of-waitqueue.patch
Patch488:       0188-fs-dcache-disable-preemption-on-i_dir_seq-s-write-si.patch
Patch489:       0189-net-Qdisc-use-a-seqlock-instead-seqcount.patch
Patch490:       0190-net-Properly-annotate-the-try-lock-for-the-seqlock.patch
Patch491:       0191-kconfig-Disable-config-options-which-are-not-RT-comp.patch
Patch492:       0192-mm-Allow-only-SLUB-on-RT.patch
Patch493:       0193-sched-Disable-CONFIG_RT_GROUP_SCHED-on-RT.patch
Patch494:       0194-net-core-disable-NET_RX_BUSY_POLL-on-RT.patch
Patch495:       0195-efi-Disable-runtime-services-on-RT.patch
Patch496:       0196-efi-Allow-efi-runtime.patch
Patch497:       0197-rt-Add-local-irq-locks.patch
Patch498:       0198-signal-x86-Delay-calling-signals-in-atomic.patch
Patch499:       0199-Split-IRQ-off-and-zone-lock-while-freeing-pages-from.patch
Patch500:       0200-Split-IRQ-off-and-zone-lock-while-freeing-pages-from.patch
Patch501:       0201-mm-SLxB-change-list_lock-to-raw_spinlock_t.patch
Patch502:       0202-mm-SLUB-delay-giving-back-empty-slubs-to-IRQ-enabled.patch
Patch503:       0203-mm-slub-Always-flush-the-delayed-empty-slubs-in-flus.patch
Patch504:       0204-mm-slub-Don-t-resize-the-location-tracking-cache-on-.patch
Patch505:       0205-mm-page_alloc-Use-migrate_disable-in-drain_local_pag.patch
Patch506:       0206-mm-page_alloc-rt-friendly-per-cpu-pages.patch
Patch507:       0207-mm-slub-Make-object_map_lock-a-raw_spinlock_t.patch
Patch508:       0208-slub-Enable-irqs-for-__GFP_WAIT.patch
Patch509:       0209-slub-Disable-SLUB_CPU_PARTIAL.patch
Patch510:       0210-mm-memcontrol-Provide-a-local_lock-for-per-CPU-memcg.patch
Patch511:       0211-mm-memcontrol-Don-t-call-schedule_work_on-in-preempt.patch
Patch512:       0212-mm-memcontrol-Replace-local_irq_disable-with-local-l.patch
Patch513:       0213-mm-zsmalloc-copy-with-get_cpu_var-and-locking.patch
Patch514:       0214-mm-zswap-Use-local-lock-to-protect-per-CPU-data.patch
Patch515:       0215-x86-kvm-Require-const-tsc-for-RT.patch
Patch516:       0216-wait.h-include-atomic.h.patch
Patch517:       0217-sched-Limit-the-number-of-task-migrations-per-batch.patch
Patch518:       0218-sched-Move-mmdrop-to-RCU-on-RT.patch
Patch519:       0219-kernel-sched-move-stack-kprobe-clean-up-to-__put_tas.patch
Patch520:       0220-sched-Do-not-account-rcu_preempt_depth-on-RT-in-migh.patch
Patch521:       0221-sched-Disable-TTWU_QUEUE-on-RT.patch
Patch522:       0222-softirq-Check-preemption-after-reenabling-interrupts.patch
Patch523:       0223-softirq-Disable-softirq-stacks-for-RT.patch
Patch524:       0224-net-core-use-local_bh_disable-in-netif_rx_ni.patch
Patch525:       0225-pid.h-include-atomic.h.patch
Patch526:       0226-ptrace-fix-ptrace-vs-tasklist_lock-race.patch
Patch527:       0227-ptrace-fix-ptrace_unfreeze_traced-race-with-rt-lock.patch
Patch528:       0228-kernel-sched-add-put-get-_cpu_light.patch
Patch529:       0229-trace-Add-migrate-disabled-counter-to-tracing-output.patch
Patch530:       0230-locking-don-t-check-for-__LINUX_SPINLOCK_TYPES_H-on-.patch
Patch531:       0231-locking-Make-spinlock_t-and-rwlock_t-a-RCU-section-o.patch
Patch532:       0232-rcutorture-Avoid-problematic-critical-section-nestin.patch
Patch533:       0233-mm-vmalloc-Another-preempt-disable-region-which-suck.patch
Patch534:       0234-block-mq-do-not-invoke-preempt_disable.patch
Patch535:       0235-md-raid5-Make-raid5_percpu-handling-RT-aware.patch
Patch536:       0236-scsi-fcoe-Make-RT-aware.patch
Patch537:       0237-sunrpc-Make-svc_xprt_do_enqueue-use-get_cpu_light.patch
Patch538:       0238-rt-Introduce-cpu_chill.patch
Patch539:       0239-fs-namespace-Use-cpu_chill-in-trylock-loops.patch
Patch540:       0240-debugobjects-Make-RT-aware.patch
Patch541:       0241-net-Use-skbufhead-with-raw-lock.patch
Patch542:       0242-net-Dequeue-in-dev_cpu_dead-without-the-lock.patch
Patch543:       0243-net-dev-always-take-qdisc-s-busylock-in-__dev_xmit_s.patch
Patch544:       0244-irqwork-push-most-work-into-softirq-context.patch
Patch545:       0245-x86-crypto-Reduce-preempt-disabled-regions.patch
Patch546:       0246-crypto-Reduce-preempt-disabled-regions-more-algos.patch
Patch547:       0247-crypto-limit-more-FPU-enabled-sections.patch
Patch548:       0248-crypto-cryptd-add-a-lock-instead-preempt_disable-loc.patch
Patch549:       0249-panic-skip-get_random_bytes-for-RT_FULL-in-init_oops.patch
Patch550:       0250-x86-stackprotector-Avoid-random-pool-on-rt.patch
Patch551:       0251-random-Make-it-work-on-rt.patch
Patch552:       0252-net-Remove-preemption-disabling-in-netif_rx.patch
Patch553:       0253-lockdep-Make-it-RT-aware.patch
Patch554:       0254-lockdep-selftest-Only-do-hardirq-context-test-for-ra.patch
Patch555:       0255-lockdep-selftest-fix-warnings-due-to-missing-PREEMPT.patch
Patch556:       0256-lockdep-disable-self-test.patch
Patch557:       0257-drm-radeon-i915-Use-preempt_disable-enable_rt-where-.patch
Patch558:       0258-drm-i915-Don-t-disable-interrupts-on-PREEMPT_RT-duri.patch
Patch559:       0259-drm-i915-disable-tracing-on-RT.patch
Patch560:       0260-drm-i915-skip-DRM_I915_LOW_LEVEL_TRACEPOINTS-with-NO.patch
Patch561:       0261-drm-i915-gt-Only-disable-interrupts-for-the-timeline.patch
Patch562:       0262-cpuset-Convert-callback_lock-to-raw_spinlock_t.patch
Patch563:       0263-x86-Allow-to-enable-RT.patch
Patch564:       0264-mm-scatterlist-Do-not-disable-irqs-on-RT.patch
Patch565:       0265-sched-Add-support-for-lazy-preemption.patch
Patch566:       0266-x86-entry-Use-should_resched-in-idtentry_exit_cond_r.patch
Patch567:       0267-x86-Support-for-lazy-preemption.patch
Patch568:       0268-arm-Add-support-for-lazy-preemption.patch
Patch569:       0269-powerpc-Add-support-for-lazy-preemption.patch
Patch570:       0270-arch-arm64-Add-lazy-preempt-support.patch
Patch571:       0271-jump-label-disable-if-stop_machine-is-used.patch
Patch572:       0272-leds-trigger-disable-CPU-trigger-on-RT.patch
Patch573:       0273-tty-serial-omap-Make-the-locking-RT-aware.patch
Patch574:       0274-tty-serial-pl011-Make-the-locking-work-on-RT.patch
Patch575:       0275-ARM-enable-irq-in-translation-section-permission-fau.patch
Patch576:       0276-genirq-update-irq_set_irqchip_state-documentation.patch
Patch577:       0277-KVM-arm-arm64-downgrade-preempt_disable-d-region-to-.patch
Patch578:       0278-arm64-fpsimd-Delay-freeing-memory-in-fpsimd_flush_th.patch
Patch579:       0279-x86-Enable-RT-also-on-32bit.patch
Patch580:       0280-ARM-Allow-to-enable-RT.patch
Patch581:       0281-ARM64-Allow-to-enable-RT.patch
Patch582:       0282-powerpc-traps-Use-PREEMPT_RT.patch
Patch583:       0283-powerpc-pseries-iommu-Use-a-locallock-instead-local_.patch
Patch584:       0284-powerpc-kvm-Disable-in-kernel-MPIC-emulation-for-PRE.patch
Patch585:       0285-powerpc-stackprotector-work-around-stack-guard-init-.patch
Patch586:       0286-powerpc-Avoid-recursive-header-includes.patch
Patch587:       0287-POWERPC-Allow-to-enable-RT.patch
Patch588:       0288-drivers-block-zram-Replace-bit-spinlocks-with-rtmute.patch
Patch589:       0289-tpm_tis-fix-stall-after-iowrite-s.patch
Patch590:       0290-signals-Allow-rt-tasks-to-cache-one-sigqueue-struct.patch
Patch591:       0291-signal-Prevent-double-free-of-user-struct.patch
Patch592:       0292-genirq-Disable-irqpoll-on-rt.patch
Patch593:       0293-sysfs-Add-sys-kernel-realtime-entry.patch
Patch594:       0294-Add-localversion-for-RT-release.patch
Patch595:       0295-net-xfrm-Use-sequence-counter-with-associated-spinlo.patch

# Keep rt_version matched up with this patch.
Patch596:       0296-Linux-5.10.41-rt42-REBASE.patch

#Photon Specific Changes
Patch600:       0000-Revert-clockevents-Stop-unused-clockevent-devices.patch

# RT Runtime Greed
Patch601:       0001-RT-PATCH-sched-rt-RT_RUNTIME_GREED-sched-feature.patch
Patch602:       use-kmsg_dump-iterator-for-RT.patch

# Crypto:
# Patch to add drbg_pr_ctr_aes256 test vectors to testmgr
Patch1000:       crypto-testmgr-Add-drbg_pr_ctr_aes256-test-vectors.patch
# Patch to call drbg and dh crypto tests from tcrypt
Patch1001:       tcrypt-disable-tests-that-are-not-enabled-in-photon.patch
Patch1002:       0001-Initialize-jitterentropy-before-ecdh.patch
Patch1003:       0002-FIPS-crypto-self-tests.patch
# Patch to remove urandom usage in rng module
Patch1004:       0001-FIPS-crypto-rng-Jitterentropy-RNG-as-the-only-RND-source.patch
# Patch to remove urandom usage in drbg and ecc modules
Patch1005:       0003-FIPS-crypto-drbg-Jitterentropy-RNG-as-the-only-RND.patch
%if 0%{?fips}
# FIPS canister usage patch
Patch1008:       0001-FIPS-canister-binary-usage.patch
%else
%if 0%{?kat_build:1}
Patch1010:       0003-FIPS-broken-kattest.patch
%endif
%endif

#Patches for i40e driver
Patch1500:      i40e-xdp-remove-XDP_QUERY_PROG-and-XDP_QUERY_PROG_HW-XDP-.patch
Patch1501:      i40e-Fix-minor-compilation-error.patch
Patch1502:      0001-Add-support-for-gettimex64-interface.patch

#Patches for ice driver
Patch1510:      0001-Use-PTP_SYS_OFFSET_EXTENDED_IOCTL-support.patch

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
Requires:       filesystem kmod
Requires(pre): (coreutils or toybox)
Requires(preun): (coreutils or toybox)
Requires(post):(coreutils or toybox)
Requires(postun):(coreutils or toybox)

%description
The Linux package contains the Linux kernel with RT (real-time)
features.
%if 0%{?fips}
This kernel is FIPS certified.
%endif

%package devel
Summary:        Kernel Dev
Group:          System Environment/Kernel
Requires:       %{name} = %{version}-%{release}
Requires:       python3 gawk
%description devel
The Linux package contains the Linux kernel dev files

%package docs
Summary:        Kernel docs
Group:          System Environment/Kernel
Requires:       python3
%description docs
The Linux package contains the Linux kernel doc files

%prep
%setup -q -n linux-%{version}
%ifarch x86_64
%setup -D -b 6 -n linux-%{version}
%setup -D -b 7 -n linux-%{version}
%setup -D -b 8 -n linux-%{version}
%endif
%if 0%{?fips}
%setup -D -b 16 -n linux-%{version}
%endif

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

%patch10 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1

#vmxnet3
%patch20 -p1

#VMW
%patch55 -p1
%patch56 -p1

# CVE
%patch100 -p1
%patch101 -p1
%patch128 -p1
%patch129 -p1

# RT
%patch301 -p1
%patch302 -p1
%patch303 -p1
%patch304 -p1
%patch305 -p1
%patch306 -p1
%patch307 -p1
%patch308 -p1
%patch309 -p1
%patch310 -p1
%patch311 -p1
%patch312 -p1
%patch313 -p1
%patch314 -p1
%patch315 -p1
%patch316 -p1
%patch317 -p1
%patch318 -p1
%patch319 -p1
%patch320 -p1
%patch321 -p1
%patch322 -p1
%patch323 -p1
%patch324 -p1
%patch325 -p1
%patch326 -p1
%patch327 -p1
%patch328 -p1
%patch329 -p1
%patch330 -p1
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
%patch361 -p1
%patch362 -p1
%patch363 -p1
%patch364 -p1
%patch365 -p1
%patch366 -p1
%patch367 -p1
%patch368 -p1
%patch369 -p1
%patch370 -p1
%patch371 -p1
%patch372 -p1
%patch373 -p1
%patch374 -p1
%patch375 -p1
%patch376 -p1
%patch377 -p1
%patch378 -p1
%patch379 -p1
%patch380 -p1
%patch381 -p1
%patch382 -p1
%patch383 -p1
%patch384 -p1
%patch385 -p1
%patch386 -p1
%patch387 -p1
%patch388 -p1
%patch389 -p1
%patch390 -p1
%patch391 -p1
%patch392 -p1
%patch393 -p1
%patch394 -p1
%patch395 -p1
%patch396 -p1
%patch397 -p1
%patch398 -p1
%patch399 -p1
%patch400 -p1
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
%patch464 -p1
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
%patch479 -p1
%patch480 -p1
%patch481 -p1
%patch482 -p1
%patch483 -p1
%patch484 -p1
%patch485 -p1
%patch486 -p1
%patch487 -p1
%patch488 -p1
%patch489 -p1
%patch490 -p1
%patch491 -p1
%patch492 -p1
%patch493 -p1
%patch494 -p1
%patch495 -p1
%patch496 -p1
%patch497 -p1
%patch498 -p1
%patch499 -p1
%patch500 -p1
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
%patch517 -p1
%patch518 -p1
%patch519 -p1
%patch520 -p1
%patch521 -p1
%patch522 -p1
%patch523 -p1
%patch524 -p1
%patch525 -p1
%patch526 -p1
%patch527 -p1
%patch528 -p1
%patch529 -p1
%patch530 -p1
%patch531 -p1
%patch532 -p1
%patch533 -p1
%patch534 -p1
%patch535 -p1
%patch536 -p1
%patch537 -p1
%patch538 -p1
%patch539 -p1
%patch540 -p1
%patch541 -p1
%patch542 -p1
%patch543 -p1
%patch544 -p1
%patch545 -p1
%patch546 -p1
%patch547 -p1
%patch548 -p1
%patch549 -p1
%patch550 -p1
%patch551 -p1
%patch552 -p1
%patch553 -p1
%patch554 -p1
%patch555 -p1
%patch556 -p1
%patch557 -p1
%patch558 -p1
%patch559 -p1
%patch560 -p1
%patch561 -p1
%patch562 -p1
%patch563 -p1
%patch564 -p1
%patch565 -p1
%patch566 -p1
%patch567 -p1
%patch568 -p1
%patch569 -p1
%patch570 -p1
%patch571 -p1
%patch572 -p1
%patch573 -p1
%patch574 -p1
%patch575 -p1
%patch576 -p1
%patch577 -p1
%patch578 -p1
%patch579 -p1
%patch580 -p1
%patch581 -p1
%patch582 -p1
%patch583 -p1
%patch584 -p1
%patch585 -p1
%patch586 -p1
%patch587 -p1
%patch588 -p1
%patch589 -p1
%patch590 -p1
%patch591 -p1
%patch592 -p1
%patch593 -p1
%patch594 -p1
%patch595 -p1
%patch596 -p1

%patch600 -p1
%patch601 -p1
%patch602 -p1

%patch1000 -p1
%patch1001 -p1
%patch1002 -p1
%patch1003 -p1
%patch1004 -p1
%patch1005 -p1
%if 0%{?fips}
%patch1008 -p1
%else
%if 0%{?kat_build:1}
%patch1010 -p1
%endif
%endif

#Patches for i40e driver
pushd ../i40e-%{i40e_version}
%patch1500 -p1
%patch1501 -p1
%patch1502 -p1
popd

#Patches for ice driver
pushd ../ice-%{ice_version}
%patch1510 -p1
popd

%build
make mrproper

%ifarch x86_64
cp %{SOURCE1} .config
arch="x86_64"
%endif
%if 0%{?fips}
cp ../fips-canister-%{fips_canister_version}/fips_canister.o crypto/
cp ../fips-canister-%{fips_canister_version}/fips_canister_wrapper.c crypto/
# Change m to y for modules that are in the canister
%include %{SOURCE17}
%else
%if 0%{?kat_build:1}
# Change m to y for modules in katbuild
%include %{SOURCE17}
%endif
%endif

sed -i 's/CONFIG_LOCALVERSION="-rt"/CONFIG_LOCALVERSION="-%{release}-rt"/' .config

%include %{SOURCE5}

make V=1 KBUILD_BUILD_VERSION="1-photon" KBUILD_BUILD_HOST="photon" ARCH=${arch} %{?_smp_mflags}

%ifarch x86_64

# build i40e module
bldroot=`pwd`
pushd ../i40e-%{i40e_version}
make -C src KSRC=$bldroot clean
make -C src KSRC=$bldroot %{?_smp_mflags}
popd

# build iavf module
bldroot=`pwd`
pushd ../iavf-%{iavf_version}
make -C src KSRC=$bldroot clean
make -C src KSRC=$bldroot %{?_smp_mflags}
popd

# build ice module
bldroot=`pwd`
pushd ../ice-%{ice_version}
make -C src KSRC=$bldroot clean
make -C src KSRC=$bldroot %{?_smp_mflags}
popd
%endif

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

install -vdm 755 %{buildroot}%{_sysconfdir}
install -vdm 755 %{buildroot}/boot
install -vdm 755 %{buildroot}%{_docdir}/%{name}-%{uname_r}
install -vdm 755 %{buildroot}%{_usrsrc}/%{name}-headers-%{uname_r}
install -vdm 755 %{buildroot}/usr/lib/debug/lib/modules/%{uname_r}
make INSTALL_MOD_PATH=%{buildroot} modules_install

%ifarch x86_64

# install i40e module
bldroot=`pwd`
pushd ../i40e-%{i40e_version}
make -C src KSRC=$bldroot INSTALL_MOD_PATH=%{buildroot} INSTALL_MOD_DIR=extra MANDIR=%{_mandir} modules_install mandocs_install
popd

# install iavf module
bldroot=`pwd`
pushd ../iavf-%{iavf_version}
make -C src KSRC=$bldroot INSTALL_MOD_PATH=%{buildroot} INSTALL_MOD_DIR=extra MANDIR=%{_mandir} modules_install mandocs_install
popd

# install ice module
bldroot=`pwd`
pushd ../ice-%{ice_version}
make -C src KSRC=$bldroot INSTALL_MOD_PATH=%{buildroot} INSTALL_MOD_DIR=extra MANDIR=%{_mandir} modules_install mandocs_install
popd

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
cp -r Documentation/*        %{buildroot}%{_docdir}/%{name}-%{uname_r}
install -vm 644 vmlinux %{buildroot}/usr/lib/debug/lib/modules/%{uname_r}/vmlinux-%{uname_r}
# `perf test vmlinux` needs it
ln -s vmlinux-%{uname_r} %{buildroot}/usr/lib/debug/lib/modules/%{uname_r}/vmlinux

cat > %{buildroot}/boot/%{name}-%{uname_r}.cfg << "EOF"
# GRUB Environment Block
photon_cmdline=init=/lib/systemd/systemd ro loglevel=3 quiet no-vmw-sta nosoftlockup intel_idle.max_cstate=0 mce=ignore_ce nowatchdog cpuidle.off=1 nmi_watchdog=0 audit=0
photon_linux=vmlinuz-%{uname_r}
photon_initrd=initrd.img-%{uname_r}
EOF

# Register myself to initramfs
mkdir -p %{buildroot}/%{_localstatedir}/lib/initramfs/kernel
cat > %{buildroot}/%{_localstatedir}/lib/initramfs/kernel/%{uname_r} << "EOF"
--add-drivers "cn lvm dm-mod megaraid_sas"
EOF

#    Cleanup dangling symlinks
rm -rf %{buildroot}/lib/modules/%{uname_r}/source
rm -rf %{buildroot}/lib/modules/%{uname_r}/build

find . -name Makefile* -o -name Kconfig* -o -name *.pl | xargs  sh -c 'cp --parents "$@" %{buildroot}%{_usrsrc}/%{name}-headers-%{uname_r}' copy
find arch/%{archdir}/include include scripts -type f | xargs  sh -c 'cp --parents "$@" %{buildroot}%{_usrsrc}/%{name}-headers-%{uname_r}' copy
find $(find arch/%{archdir} -name include -o -name scripts -type d) -type f | xargs  sh -c 'cp --parents "$@" %{buildroot}%{_usrsrc}/%{name}-headers-%{uname_r}' copy
find arch/%{archdir}/include Module.symvers include scripts -type f | xargs  sh -c 'cp --parents "$@" %{buildroot}%{_usrsrc}/%{name}-headers-%{uname_r}' copy
%ifarch x86_64
# CONFIG_STACK_VALIDATION=y requires objtool to build external modules
install -vsm 755 tools/objtool/objtool %{buildroot}%{_usrsrc}/%{name}-headers-%{uname_r}/tools/objtool/
install -vsm 755 tools/objtool/fixdep %{buildroot}%{_usrsrc}/%{name}-headers-%{uname_r}/tools/objtool/
%endif

cp .config %{buildroot}%{_usrsrc}/%{name}-headers-%{uname_r} # copy .config manually to be where it's expected to be
ln -sf "%{_usrsrc}/%{name}-headers-%{uname_r}" "%{buildroot}/lib/modules/%{uname_r}/build"
find %{buildroot}/lib/modules -name '*.ko' -print0 | xargs -0 chmod u+x

%include %{SOURCE2}
%include %{SOURCE4}

%post
/sbin/depmod -a %{uname_r}
ln -sf %{name}-%{uname_r}.cfg /boot/photon.cfg

%files
%defattr(-,root,root)
/boot/System.map-%{uname_r}
/boot/config-%{uname_r}
/boot/vmlinuz-%{uname_r}
%config(noreplace) /boot/%{name}-%{uname_r}.cfg
%config %{_localstatedir}/lib/initramfs/kernel/%{uname_r}
%defattr(0644,root,root)
/lib/modules/%{uname_r}/*
%exclude /lib/modules/%{uname_r}/build
/etc/modprobe.d/iavf.conf
# ICE driver firmware files are packaged in linux-firmware
%exclude /lib/firmware/updates/intel/ice

%files docs
%defattr(-,root,root)
%{_defaultdocdir}/%{name}-%{uname_r}/*
%{_mandir}/*

%files devel
%defattr(-,root,root)
/lib/modules/%{uname_r}/build
%{_usrsrc}/%{name}-headers-%{uname_r}

%changelog
*   Thu Jun 03 2021 Keerthana K <keerthanak@vmware.com> 5.10.42-1
-   Update to version 5.10.42
-   Remove XR usb driver support
-   .config: Enable CONFIG_FANOTIFY_ACCESS_PERMISSIONS
*   Wed Jun 02 2021 Keerthana K <keerthanak@vmware.com> 5.10.35-3
-   Fix for CVE-2021-3573
*   Thu May 20 2021 Ajay Kaher <akaher@vmware.com> 5.10.35-2
-   Fix for CVE-2021-3564
*   Mon May 17 2021 Ajay Kaher <akaher@vmware.com> 5.10.35-1
-   Update to version 5.10.35
*   Thu May 13 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.25-10
-   Fix for CVE-2021-23133
*   Tue May 11 2021 Ankit Jain <ankitja@vmware.com> 5.10.25-9
-   .config: Enable INFINIBAND, MLX5_INFINIBAND
*   Tue May 11 2021 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.25-8
-   Fix CVE-2020-26147, CVE-2020-24587, CVE-2020-24586, CVE-2020-24588,
-   CVE-2020-26145, CVE-2020-26141
*   Tue May 11 2021 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.25-7
-   Fix CVE-2021-3489, CVE-2021-3490, CVE-2021-3491
*   Tue May 04 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.25-6
-   Remove buf_info from device accessible structures in vmxnet3
*   Thu Apr 29 2021 Alexey Makhalov <amakhalov@vmware.com> 5.10.25-5
-   Update canister binary.
-   use jent by drbg and ecc.
-   Enable hmac(sha224) self test and broket KAT test.
*   Thu Apr 22 2021 Keerthana K <keerthanak@vmware.com> 5.10.25-4
-   Remove hmac(sha224) from broken kat test.
*   Mon Apr 19 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.25-3
-   Fix for CVE-2021-23133
*   Thu Apr 15 2021 Srinidhi Rao <srinidhir@vmware.com> 5.10.25-2
-   Fix for CVE-2021-29154
*   Mon Mar 22 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 5.10.25-1
-   Update to version 5.10.25
*   Sun Mar 21 2021 Alexey Makhalov <amakhalov@vmware.com> 5.10.21-3
-   Do not execute some tests twice
-   Support future disablement of des3
-   Do verbose build
-   Canister update.
*   Wed Mar 17 2021 Srinidhi Rao <srinidhir@vmware.com> 5.10.21-2
-   Use jitterentropy rng instead of urandom in rng module.
*   Tue Mar 16 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 5.10.21-1
-   Update to version 5.10.21
*   Mon Mar 01 2021 Alexey Makhalov <amakhalov@vmware.com> 5.10.4-10
-   FIPS canister update
*   Thu Feb 18 2021 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.4-9
-   Fix /boot/photon.cfg symlink when /boot is a separate partition.
*   Thu Feb 18 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.4-8
-   Enable CONFIG_IFB
*   Wed Feb 17 2021 Ankit Jain <ankitja@vmware.com> 5.10.4-7
-   Added latest out of tree version of Intel ice driver
*   Wed Feb 17 2021 Vikash Bansal <bvikas@vmware.com> 5.10.4-6
-   Added support for RT RUNTIME GREED
*   Mon Feb 15 2021 Keerthana K <keerthanak@vmware.com> 5.10.4-5
-   Added crypto_self_test and kattest module.
-   These patches are applied when kat_build is enabled.
*   Wed Feb 03 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 5.10.4-4
-   Update i40e driver to v2.13.10
-   Add out of tree iavf driver
-   Enable CONFIG_NET_TEAM
*   Wed Jan 27 2021 Alexey Makhalov <amakhalov@vmware.com> 5.10.4-3
-   Build kernel with FIPS canister.
*   Mon Jan 25 2021 Ankit Jain <ankitja@vmware.com> 5.10.4-2
-   Enabled CONFIG_WIREGUARD
*   Mon Jan 11 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 5.10.4-1
-   Update to version 5.10.4
*   Tue Nov 10 2020 Keerthana K <keerthanak@vmware.com> 5.9.0-4
-   Fix CVE-2020-8694
*   Fri Nov 06 2020 Keerthana K <keerthanak@vmware.com> 5.9.0-3
-   Fix CVE-2020-25704
*   Tue Oct 27 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.9.0-2
-   Revert d254087 (clockevents: Stop unused clockevent devices)
-   Solve cyclictest regression introduced in 4.1
*   Tue Oct 27 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.9.0-1
-   Update to version 5.9.0
*   Tue Oct 06 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.9.0-rc7.1
-   Update to version 5.9.0-rc7
*   Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 4.19.127-2
-   openssl 1.1.1
*   Tue Jun 23 2020 Keerthana K <keerthanak@vmware.com> 4.19.127-1
-   Update to version 4.19.127
*   Tue Jun 16 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.115-10
-   Add latest out of tree version of i40e driver
*   Wed Jun 10 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.115-9
-   Enable CONFIG_VFIO_NOIOMMU
*   Fri Jun 05 2020 Ankit Jain <ankitja@vmware.com> 4.19.115-8
-   Enabled CONFIG_BINFMT_MISC
*   Tue Jun 02 2020 Vikash Bansal <bvikas@vmware.com> 4.19.115-7
-   Add patch to fix CVE-2019-18885
*   Fri May 29 2020 Shreenidhi Shedi <sshedi@vmware.com> 4.19.115-6
-   Keep modules of running kernel till next boot
*   Fri May 22 2020 Tapas Kundu <tkundu@vmware.com> 4.19.115-5
-   Deprecate linux-rt-tools in favor of linux-tools.
-   Deprecate python3-perf in favor of linux-python3-perf.
*   Thu May 21 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.115-4
-   Add ICE network driver support in config
*   Fri May 15 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.115-3
-   Add uio_pic_generic driver support in config
*   Wed May 06 2020 Siddharth Chandrasekaran <csiddharth@vmware.com> 4.19.115-2
-   Add patch to fix CVE-2020-10711
*   Wed May 06 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.115-1
-   Upgrade to 4.19.115
*   Wed Apr 29 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.98-5
-   Enable additional config options.
*   Mon Mar 23 2020 Alexey Makhalov <amakhalov@vmware.com> 4.19.98-4
-   Fix perf compilation issue with binutils >= 2.34.
*   Sun Mar 22 2020 Tapas Kundu <tkundu@vmware.com> 4.19.98-3
-   Added python3-perf subpackage
*   Tue Mar 17 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.98-2
-   Add tools subpackage to include perf, turbostat and cpupower.
-   Update the last few perf python scripts in Linux kernel to use
-   python3 syntax.
*   Tue Jan 28 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.98-1
-   Upgrade to 4.19.98
*   Thu Jan 16 2020 Srinidhi Rao <srinidhir@vmware.com> 4.19.82-4
-   Enable DRBG HASH and DRBG CTR support.
*   Fri Jan 03 2020 Keerthana K <keerthanak@vmware.com> 4.19.82-3
-   Remove FIPS patch that enables fips for algorithms which are not fips allowed.
*   Thu Dec 12 2019 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.82-2
-   Fix patch that wont apply on 4.19.82. Revert when upgraded to 4.19.87 or more
*   Tue Nov 12 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.82-1
-   Introduce a new kernel flavor 'linux-rt' supporting real-time (RT) features.
