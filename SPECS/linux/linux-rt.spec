%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%global security_hardening none

%ifarch x86_64
%define arch x86_64
%define archdir x86
%endif

Summary:        Kernel
Name:           linux-rt
Version:        5.10.4
# Keep rt_version matched up with localversion.patch
%define rt_version rt22
Release:        1%{?kat_build:.kat}%{?dist}
License:    	GPLv2
URL:        	http://www.kernel.org/
Group:        	System Environment/Kernel
Vendor:         VMware, Inc.
Distribution: 	Photon

%define uname_r %{version}-%{rt_version}-%{release}-rt

Source0:        http://www.kernel.org/pub/linux/kernel/v5.x/linux-%{version}.tar.xz
%define sha1 linux=62605305a3cbae68780612d35e0585cfc4983afd
Source1:	config-rt
Source2:	initramfs.trigger
Source3:	xr_usb_serial_common_lnx-3.6-and-newer-pak.tar.xz
%define sha1 xr=74df7143a86dd1519fa0ccf5276ed2225665a9db
Source4:        pre-preun-postun-tasks.inc
Source5:        check_for_config_applicability.inc
%define i40e_version 2.12.6
Source6:	https://sourceforge.net/projects/e1000/files/i40e%20stable/%{i40e_version}/i40e-%{i40e_version}.tar.gz
%define sha1 i40e=e1a28cdf7c122f177ed75b7615a0a0e221d21ff4


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

# VMW:
Patch55:        x86-vmware-Use-Efficient-and-Correct-ALTERNATIVEs-fo-510.patch
Patch56:        x86-vmware-Log-kmsg-dump-on-panic-510.patch

# CVE:
Patch100:       apparmor-fix-use-after-free-in-sk_peer_label.patch
# Fix for CVE-2019-12379
Patch101:       consolemap-Fix-a-memory-leaking-bug-in-drivers-tty-v.patch

# Real-Time kernel (PREEMPT_RT patches)
Patch301:	0003-z3fold-remove-preempt-disabled-sections-for-RT.patch
Patch302:	0001-stop_machine-Add-function-and-caller-debug-info.patch
Patch303:	0002-sched-Fix-balance_callback.patch
Patch304:	0003-sched-hotplug-Ensure-only-per-cpu-kthreads-run-durin.patch
Patch305:	0004-sched-core-Wait-for-tasks-being-pushed-away-on-hotpl.patch
Patch306:	0005-workqueue-Manually-break-affinity-on-hotplug.patch
Patch307:	0006-sched-hotplug-Consolidate-task-migration-on-CPU-unpl.patch
Patch308:	0007-sched-Fix-hotplug-vs-CPU-bandwidth-control.patch
Patch309:	0008-sched-Massage-set_cpus_allowed.patch
Patch310:	0009-sched-Add-migrate_disable.patch
Patch311:	0010-sched-Fix-migrate_disable-vs-set_cpus_allowed_ptr.patch
Patch312:	0011-sched-core-Make-migrate-disable-and-CPU-hotplug-coop.patch
Patch313:	0012-sched-rt-Use-cpumask_any-_distribute.patch
Patch314:	0013-sched-rt-Use-the-full-cpumask-for-balancing.patch
Patch315:	0014-sched-lockdep-Annotate-pi_lock-recursion.patch
Patch316:	0015-sched-Fix-migrate_disable-vs-rt-dl-balancing.patch
Patch317:	0016-sched-proc-Print-accurate-cpumask-vs-migrate_disable.patch
Patch318:	0017-sched-Add-migrate_disable-tracepoints.patch
Patch319:	0018-sched-Deny-self-issued-__set_cpus_allowed_ptr-when-m.patch
Patch320:	0019-sched-Comment-affine_move_task.patch
Patch321:	sched-Unlock-the-rq-in-affine_move_task-error-path.patch
Patch322:	sched-Fix-migration_cpu_stop-WARN.patch
Patch323:	sched-core-Add-missing-completion-for-affine_move_ta.patch
Patch324:	0001-mm-highmem-Un-EXPORT-__kmap_atomic_idx.patch
Patch325:	0002-highmem-Remove-unused-functions.patch
Patch326:	0003-fs-Remove-asm-kmap_types.h-includes.patch
Patch327:	0004-sh-highmem-Remove-all-traces-of-unused-cruft.patch
Patch328:	0005-asm-generic-Provide-kmap_size.h.patch
Patch329:	0006-highmem-Provide-generic-variant-of-kmap_atomic.patch
Patch330:	0007-highmem-Make-DEBUG_HIGHMEM-functional.patch
Patch331:	0008-x86-mm-highmem-Use-generic-kmap-atomic-implementatio.patch
Patch332:	0009-arc-mm-highmem-Use-generic-kmap-atomic-implementatio.patch
Patch333:	0010-ARM-highmem-Switch-to-generic-kmap-atomic.patch
Patch334:	0011-csky-mm-highmem-Switch-to-generic-kmap-atomic.patch
Patch335:	0012-microblaze-mm-highmem-Switch-to-generic-kmap-atomic.patch
Patch336:	0013-mips-mm-highmem-Switch-to-generic-kmap-atomic.patch
Patch337:	0014-nds32-mm-highmem-Switch-to-generic-kmap-atomic.patch
Patch338:	0015-powerpc-mm-highmem-Switch-to-generic-kmap-atomic.patch
Patch339:	0016-sparc-mm-highmem-Switch-to-generic-kmap-atomic.patch
Patch340:	0017-xtensa-mm-highmem-Switch-to-generic-kmap-atomic.patch
Patch341:	0018-highmem-Get-rid-of-kmap_types.h.patch
Patch342:	0019-mm-highmem-Remove-the-old-kmap_atomic-cruft.patch
Patch343:	0020-io-mapping-Cleanup-atomic-iomap.patch
Patch344:	0021-Documentation-io-mapping-Remove-outdated-blurb.patch
Patch345:	0022-highmem-High-implementation-details-and-document-API.patch
Patch346:	0023-sched-Make-migrate_disable-enable-independent-of-RT.patch
Patch347:	0024-sched-highmem-Store-local-kmaps-in-task-struct.patch
Patch348:	0025-mm-highmem-Provide-kmap_local.patch
Patch349:	0026-io-mapping-Provide-iomap_local-variant.patch
Patch350:	0027-x86-crashdump-32-Simplify-copy_oldmem_page.patch
Patch351:	0028-mips-crashdump-Simplify-copy_oldmem_page.patch
Patch352:	0029-ARM-mm-Replace-kmap_atomic_pfn.patch
Patch353:	0030-highmem-Remove-kmap_atomic_pfn.patch
Patch354:	0031-drm-ttm-Replace-kmap_atomic-usage.patch
Patch355:	0032-drm-vmgfx-Replace-kmap_atomic.patch
Patch356:	0033-highmem-Remove-kmap_atomic_prot.patch
Patch357:	0034-drm-qxl-Replace-io_mapping_map_atomic_wc.patch
Patch358:	0035-drm-nouveau-device-Replace-io_mapping_map_atomic_wc.patch
Patch359:	0036-drm-i915-Replace-io_mapping_map_atomic_wc.patch
Patch360:	0037-io-mapping-Remove-io_mapping_map_atomic_wc.patch
Patch361:	mm-highmem-Take-kmap_high_get-properly-into-account.patch
Patch362:	highmem-Don-t-disable-preemption-on-RT-in-kmap_atomi.patch
Patch363:	timers-Move-clearing-of-base-timer_running-under-bas.patch
Patch364:	0001-blk-mq-Don-t-complete-on-a-remote-CPU-in-force-threa.patch
Patch365:	0002-blk-mq-Always-complete-remote-completions-requests-i.patch
Patch366:	0003-blk-mq-Use-llist_head-for-blk_cpu_done.patch
Patch367:	block-mq-Disable-preemption-in-blk_mq_complete_reque.patch
Patch368:	lib-test_lockup-Minimum-fix-to-get-it-compiled-on-PR.patch
Patch369:	timers-Don-t-block-on-expiry_lock-for-TIMER_IRQSAFE.patch
Patch370:	0001-kthread-Move-prio-affinite-change-into-the-newly-cre.patch
Patch371:	0002-genirq-Move-prio-assignment-into-the-newly-created-t.patch
Patch372:	notifier-Make-atomic_notifiers-use-raw_spinlock.patch
Patch373:	0001-rcu-Make-RCU_BOOST-default-on-CONFIG_PREEMPT_RT.patch
Patch374:	0002-rcu-Unconditionally-use-rcuc-threads-on-PREEMPT_RT.patch
Patch375:	0003-rcu-Enable-rcu_normal_after_boot-unconditionally-for.patch
Patch376:	0004-doc-Update-RCU-s-requirements-page-about-the-PREEMPT.patch
Patch377:	0005-doc-Use-CONFIG_PREEMPTION.patch
Patch378:	tracing-Merge-irqflags-preemt-counter-add-RT-bits.patch
Patch379:	0001-printk-inline-log_output-log_store-in-vprintk_store.patch
Patch380:	0002-printk-remove-logbuf_lock-writer-protection-of-ringb.patch
Patch381:	0003-printk-use-seqcount_latch-for-clear_seq.patch
Patch382:	0004-printk-use-atomic64_t-for-devkmsg_user.seq.patch
Patch383:	0005-printk-add-syslog_lock.patch
Patch384:	0006-define-CONSOLE_LOG_MAX-in-printk.h.patch
Patch385:	0007-printk-track-limit-recursion.patch
Patch386:	0008-printk-invoke-dumper-using-a-copy-of-the-iterator.patch
Patch387:	0009-printk-remove-logbuf_lock.patch
Patch388:	0010-printk-remove-safe-buffers.patch
Patch389:	0011-printk-refactor-kmsg_dump_get_buffer.patch
Patch390:	0012-console-add-write_atomic-interface.patch
Patch391:	0013-serial-8250-implement-write_atomic.patch
Patch392:	0014-printk-relocate-printk_delay-and-vprintk_default.patch
Patch393:	0015-printk-combine-boot_delay_msec-into-printk_delay.patch
Patch394:	0016-printk-change-console_seq-to-atomic64_t.patch
Patch395:	0017-printk-introduce-kernel-sync-mode.patch
Patch396:	0018-printk-move-console-printing-to-kthreads.patch
Patch397:	0019-printk-remove-deferred-printing.patch
Patch398:	0020-printk-add-console-handover.patch
Patch399:	0021-printk-add-pr_flush.patch
Patch400:	cgroup-use-irqsave-in-cgroup_rstat_flush_locked.patch
Patch401:	mm-workingset-replace-IRQ-off-check-with-a-lockdep-a.patch
Patch402:	tpm-remove-tpm_dev_wq_lock.patch
Patch403:	shmem-Use-raw_spinlock_t-for-stat_lock.patch
Patch404:	net--Move-lockdep-where-it-belongs.patch
Patch405:	tcp-Remove-superfluous-BH-disable-around-listening_h.patch
Patch406:	0001-parisc-Remove-bogus-__IRQ_STAT-macro.patch
Patch407:	0002-sh-Get-rid-of-nmi_count.patch
Patch408:	0003-irqstat-Get-rid-of-nmi_count-and-__IRQ_STAT.patch
Patch409:	0004-um-irqstat-Get-rid-of-the-duplicated-declarations.patch
Patch410:	0005-ARM-irqstat-Get-rid-of-duplicated-declaration.patch
Patch411:	0006-arm64-irqstat-Get-rid-of-duplicated-declaration.patch
Patch412:	0007-asm-generic-irqstat-Add-optional-__nmi_count-member.patch
Patch413:	0008-sh-irqstat-Use-the-generic-irq_cpustat_t.patch
Patch414:	0009-irqstat-Move-declaration-into-asm-generic-hardirq.h.patch
Patch415:	0010-preempt-Cleanup-the-macro-maze-a-bit.patch
Patch416:	0011-softirq-Move-related-code-into-one-section.patch
Patch417:	0012-sh-irq-Add-missing-closing-parentheses-in-arch_show_.patch
Patch418:	0001-sched-cputime-Remove-symbol-exports-from-IRQ-time-ac.patch
Patch419:	0002-s390-vtime-Use-the-generic-IRQ-entry-accounting.patch
Patch420:	0003-sched-vtime-Consolidate-IRQ-time-accounting.patch
Patch421:	0004-irqtime-Move-irqtime-entry-accounting-after-irq-offs.patch
Patch422:	0005-irq-Call-tick_irq_enter-inside-HARDIRQ_OFFSET.patch
Patch423:	softirq_Add_RT_specific_softirq_accounting.patch
Patch424:	softirq_Move_various_protections_into_inline_helpers.patch
Patch425:	softirq_Make_softirq_control_and_processing_RT_aware.patch
Patch426:	tick_sched_Prevent_false_positive_softirq_pending_warnings_on_RT.patch
Patch427:	rcu_Prevent_false_positive_softirq_warning_on_RT.patch
Patch428:	softirq_Replace_barrier_with_cpu_relax_in_tasklet_unlock_wait_.patch
Patch429:	tasklets_Use_static_inlines_for_stub_implementations.patch
Patch430:	tasklets_Prevent_kill_unlock_wait_deadlock_on_RT.patch
Patch431:	irqtime-Use-irq_count-instead-of-preempt_count.patch
Patch432:	x86-fpu-Simplify-fpregs_-un-lock.patch
Patch433:	x86-fpu-Make-kernel-FPU-protection-RT-friendly.patch
Patch434:	0001-locking-rtmutex-Remove-cruft.patch
Patch435:	0002-locking-rtmutex-Remove-output-from-deadlock-detector.patch
Patch436:	0003-locking-rtmutex-Move-rt_mutex_init-outside-of-CONFIG.patch
Patch437:	0004-locking-rtmutex-Remove-rt_mutex_timed_lock.patch
Patch438:	0005-locking-rtmutex-Handle-the-various-new-futex-race-co.patch
Patch439:	0006-futex-Fix-bug-on-when-a-requeued-RT-task-times-out.patch
Patch440:	0007-locking-rtmutex-Make-lock_killable-work.patch
Patch441:	0008-locking-spinlock-Split-the-lock-types-header.patch
Patch442:	0009-locking-rtmutex-Avoid-include-hell.patch
Patch443:	0010-lockdep-Reduce-header-files-in-debug_locks.h.patch
Patch444:	0011-locking-split-out-the-rbtree-definition.patch
Patch445:	0012-locking-rtmutex-Provide-rt_mutex_slowlock_locked.patch
Patch446:	0013-locking-rtmutex-export-lockdep-less-version-of-rt_mu.patch
Patch447:	0014-sched-Add-saved_state-for-tasks-blocked-on-sleeping-.patch
Patch448:	0015-locking-rtmutex-add-sleeping-lock-implementation.patch
Patch449:	0016-locking-rtmutex-Allow-rt_mutex_trylock-on-PREEMPT_RT.patch
Patch450:	0017-locking-rtmutex-add-mutex-implementation-based-on-rt.patch
Patch451:	0018-locking-rtmutex-add-rwsem-implementation-based-on-rt.patch
Patch452:	0019-locking-rtmutex-add-rwlock-implementation-based-on-r.patch
Patch453:	0020-locking-rtmutex-wire-up-RT-s-locking.patch
Patch454:	0021-locking-rtmutex-add-ww_mutex-addon-for-mutex-rt.patch
Patch455:	0022-locking-rtmutex-Use-custom-scheduling-function-for-s.patch
Patch456:	signal-revert-ptrace-preempt-magic.patch
Patch457:	preempt-nort-rt-variants.patch
Patch458:	mm-make-vmstat-rt-aware.patch
Patch459:	mm-memcontrol-Disable-preemption-in-__mod_memcg_lruv.patch
Patch460:	0024-xfrm-Use-sequence-counter-with-associated-spinlock.patch
Patch461:	u64_stats-Disable-preemption-on-32bit-UP-SMP-with-RT.patch
Patch462:	fs-dcache-use-swait_queue-instead-of-waitqueue.patch
Patch463:	fs-dcache-disable-preemption-on-i_dir_seq-s-write-si.patch
Patch464:	net-Qdisc-use-a-seqlock-instead-seqcount.patch
Patch465:	net-Properly-annotate-the-try-lock-for-the-seqlock.patch
Patch466:	kconfig-disable-a-few-options-rt.patch
Patch467:	mm-disable-sloub-rt.patch
Patch468:	sched-disable-rt-group-sched-on-rt.patch
Patch469:	net_disable_NET_RX_BUSY_POLL.patch
Patch470:	efi-Disable-runtime-services-on-RT.patch
Patch471:	efi-Allow-efi-runtime.patch
Patch472:	rt-local-irq-lock.patch
Patch473:	oleg-signal-rt-fix.patch
Patch474:	0001-Split-IRQ-off-and-zone-lock-while-freeing-pages-from.patch
Patch475:	0002-Split-IRQ-off-and-zone-lock-while-freeing-pages-from.patch
Patch476:	0003-mm-SLxB-change-list_lock-to-raw_spinlock_t.patch
Patch477:	0004-mm-SLUB-delay-giving-back-empty-slubs-to-IRQ-enabled.patch
Patch478:	mm-slub-Always-flush-the-delayed-empty-slubs-in-flus.patch
Patch479:	mm-page_alloc-Use-migrate_disable-in-drain_local_pag.patch
Patch480:	mm-page_alloc-rt-friendly-per-cpu-pages.patch
Patch481:	mm-slub-Make-object_map_lock-a-raw_spinlock_t.patch
Patch482:	slub-enable-irqs-for-no-wait.patch
Patch483:	slub-disable-SLUB_CPU_PARTIAL.patch
Patch484:	mm-memcontrol-Provide-a-local_lock-for-per-CPU-memcg.patch
Patch485:	mm-memcontrol-Don-t-call-schedule_work_on-in-preempt.patch
Patch486:	mm-memcontrol-do_not_disable_irq.patch
Patch487:	mm_zsmalloc_copy_with_get_cpu_var_and_locking.patch
Patch488:	mm-zswap-Use-local-lock-to-protect-per-CPU-data.patch
Patch489:	x86-kvm-require-const-tsc-for-rt.patch
Patch490:	wait.h-include-atomic.h.patch
Patch491:	sched-limit-nr-migrate.patch
Patch492:	sched-mmdrop-delayed.patch
Patch493:	kernel-sched-move-stack-kprobe-clean-up-to-__put_tas.patch
Patch494:	sched-might-sleep-do-not-account-rcu-depth.patch
Patch495:	sched-disable-ttwu-queue.patch
Patch496:	softirq-preempt-fix-3-re.patch
Patch497:	softirq-disable-softirq-stacks-for-rt.patch
Patch498:	net-core-use-local_bh_disable-in-netif_rx_ni.patch
Patch499:	pid.h-include-atomic.h.patch
Patch500:	ptrace-fix-ptrace-vs-tasklist_lock-race.patch
Patch501:	ptrace-fix-ptrace_unfreeze_traced-race-with-rt-lock.patch
Patch502:	add_cpu_light.patch
Patch503:	ftrace-migrate-disable-tracing.patch
Patch504:	locking-don-t-check-for-__LINUX_SPINLOCK_TYPES_H-on-.patch
Patch505:	locking-Make-spinlock_t-and-rwlock_t-a-RCU-section-o.patch
Patch506:	rcutorture-Avoid-problematic-critical-section-nestin.patch
Patch507:	mm-vmalloc-use-get-cpu-light.patch
Patch508:	block-mq-drop-preempt-disable.patch
Patch509:	md-raid5-percpu-handling-rt-aware.patch
Patch510:	scsi-fcoe-rt-aware.patch
Patch511:	sunrpc-make-svc_xprt_do_enqueue-use-get_cpu_light.patch
Patch512:	rt-introduce-cpu-chill.patch
Patch513:	fs-namespace-use-cpu-chill-in-trylock-loops.patch
Patch514:	debugobjects-rt.patch
Patch515:	skbufhead-raw-lock.patch
Patch516:	net-Dequeue-in-dev_cpu_dead-without-the-lock.patch
Patch517:	net-dev-always-take-qdisc-s-busylock-in-__dev_xmit_s.patch
Patch518:	irqwork-push_most_work_into_softirq_context.patch
Patch519:	x86-crypto-reduce-preempt-disabled-regions.patch
Patch520:	crypto-Reduce-preempt-disabled-regions-more-algos.patch
Patch521:	crypto-limit-more-FPU-enabled-sections.patch
Patch522:	crypto-cryptd-add-a-lock-instead-preempt_disable-loc.patch
Patch523:	panic-disable-random-on-rt.patch
Patch524:	x86-stackprot-no-random-on-rt.patch
Patch525:	random-make-it-work-on-rt.patch
Patch526:	upstream-net-rt-remove-preemption-disabling-in-netif_rx.patch
Patch527:	lockdep-no-softirq-accounting-on-rt.patch
Patch528:	lockdep-selftest-only-do-hardirq-context-test-for-raw-spinlock.patch
Patch529:	lockdep-selftest-fix-warnings-due-to-missing-PREEMPT.patch
Patch530:	lockdep-disable-self-test.patch
Patch531:	drmradeoni915_Use_preempt_disableenable_rt_where_recommended.patch
Patch532:	drm-i915-Don-t-disable-interrupts-on-PREEMPT_RT-duri.patch
Patch533:	drm-i915-disable-tracing-on-RT.patch
Patch534:	drm-i915-skip-DRM_I915_LOW_LEVEL_TRACEPOINTS-with-NO.patch
Patch535:	drm-i915-gt-Only-disable-interrupts-for-the-timeline.patch
Patch536:	cpuset-Convert-callback_lock-to-raw_spinlock_t.patch
Patch537:	x86-Enable-RT.patch
Patch538:	mm-scatterlist-dont-disable-irqs-on-RT.patch
Patch539:	preempt-lazy-support.patch
Patch540:	x86-entry-Use-should_resched-in-idtentry_exit_cond_r.patch
Patch541:	x86-preempt-lazy.patch
Patch542:	arm-preempt-lazy-support.patch
Patch543:	powerpc-preempt-lazy-support.patch
Patch544:	arch-arm64-Add-lazy-preempt-support.patch
Patch545:	jump-label-rt.patch
Patch546:	leds-trigger-disable-CPU-trigger-on-RT.patch
Patch547:	drivers-tty-fix-omap-lock-crap.patch
Patch548:	drivers-tty-pl011-irq-disable-madness.patch
Patch549:	ARM-enable-irq-in-translation-section-permission-fau.patch
Patch550:	genirq-update-irq_set_irqchip_state-documentation.patch
Patch551:	KVM-arm-arm64-downgrade-preempt_disable-d-region-to-.patch
Patch552:	arm64-fpsimd-use-preemp_disable-in-addition-to-local.patch
Patch553:	x86-Enable-RT-also-on-32bit.patch
Patch554:	ARM-Allow-to-enable-RT.patch
Patch555:	ARM64-Allow-to-enable-RT.patch
Patch556:	powerpc-traps.patch
Patch557:	powerpc-pseries-iommu-Use-a-locallock-instead-local_ir.patch
Patch558:	powerpc-kvm-Disable-in-kernel-MPIC-emulation-for-PRE.patch
Patch559:	powerpc-stackprotector-work-around-stack-guard-init-.patch
Patch560:	powerpc-Avoid-recursive-header-includes.patch
Patch561:	POWERPC-Allow-to-enable-RT.patch
Patch562:	drivers-block-zram-Replace-bit-spinlocks-with-rtmute.patch
Patch563:	tpm_tis-fix-stall-after-iowrite-s.patch
Patch564:	signals-allow-rt-tasks-to-cache-one-sigqueue-struct.patch
Patch565:	signal-Prevent-double-free-of-user-struct.patch
Patch566:	genirq-disable-irqpoll-on-rt.patch
Patch567:	sysfs-realtime-entry.patch
# Keep rt_version matched up with this patch.
Patch568:        localversion.patch

Patch600:       0000-Revert-clockevents-Stop-unused-clockevent-devices.patch

%if 0%{?kat_build:1}
Patch1000:        %{kat_build}.patch
%endif

Patch1500:        i40e-xdp-remove-XDP_QUERY_PROG-and-XDP_QUERY_PROG_HW-XDP-.patch
Patch1501:        i40e-Remove-read_barrier_depends-in-favor-of-READ_ON.patch
Patch1502:        i40e-Fix-minor-compilation-error.patch

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
%setup -D -b 3 -n linux-%{version}
%setup -D -b 6 -n linux-%{version}
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

#VMW
%patch55 -p1
%patch56 -p1

# CVE
%patch100 -p1
%patch101 -p1

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

%patch600 -p1


%if 0%{?kat_build:1}
%patch1000 -p1
%endif

pushd ../i40e-%{i40e_version}
%patch1500 -p1
%patch1501 -p1
%patch1502 -p1
popd

%build
make mrproper

%ifarch x86_64
cp %{SOURCE1} .config
arch="x86_64"
%endif

sed -i 's/CONFIG_LOCALVERSION="-rt"/CONFIG_LOCALVERSION="-%{release}-rt"/' .config

%include %{SOURCE5}

make VERBOSE=1 KBUILD_BUILD_VERSION="1-photon" KBUILD_BUILD_HOST="photon" ARCH=${arch} %{?_smp_mflags}

%ifarch x86_64
# build XR module
bldroot=`pwd`
pushd ../xr_usb_serial_common_lnx-3.6-and-newer-pak
make KERNELDIR=$bldroot %{?_smp_mflags} all
popd

# build i40e module
bldroot=`pwd`
pushd ../i40e-%{i40e_version}
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

# install XR module
bldroot=`pwd`
pushd ../xr_usb_serial_common_lnx-3.6-and-newer-pak
make KERNELDIR=$bldroot INSTALL_MOD_PATH=%{buildroot} modules_install
popd

# install i40e module
bldroot=`pwd`
pushd ../i40e-%{i40e_version}
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

%files docs
%defattr(-,root,root)
%{_defaultdocdir}/%{name}-%{uname_r}/*
%{_mandir}/*

%files devel
%defattr(-,root,root)
/lib/modules/%{uname_r}/build
%{_usrsrc}/%{name}-headers-%{uname_r}

%changelog
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
