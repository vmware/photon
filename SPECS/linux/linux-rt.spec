%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%global security_hardening none

%ifarch x86_64
%define arch x86_64
%define archdir x86
%endif

Summary:        Kernel
Name:           linux-rt
Version:        5.9.0
# Keep rt_version matched up with localversion.patch
%define rt_version rt16
Release:        4%{?kat_build:.kat}%{?dist}
License:    	GPLv2
URL:        	http://www.kernel.org/
Group:        	System Environment/Kernel
Vendor:         VMware, Inc.
Distribution: 	Photon

%define uname_r %{version}-%{rt_version}-%{release}-rt

Source0:        http://www.kernel.org/pub/linux/kernel/v5.x/linux-%{version}.tar.xz
%define sha1 linux=26fefa389c711da70543092fbb121a023f1b0fb8
Source1:	config-rt
Source2:	initramfs.trigger
Source3:	xr_usb_serial_common_lnx-3.6-and-newer-pak.tar.xz
%define sha1 xr=74df7143a86dd1519fa0ccf5276ed2225665a9db
Source4:        pre-preun-postun-tasks.inc
Source5:        check_for_config_applicability.inc
%define i40e_version 2.12.6
Source6:	https://sourceforge.net/projects/e1000/files/i40e%20stable/%{i40e_version}/i40e-%{i40e_version}.tar.gz
%define sha1 i40e=e1a28cdf7c122f177ed75b7615a0a0e221d21ff4
Source7:        i40e-xdp-remove-XDP_QUERY_PROG-and-XDP_QUERY_PROG_HW-XDP-.patch
Source8:        i40e-Remove-read_barrier_depends-in-favor-of-READ_ON.patch
Source9:        i40e-Fix-minor-compilation-error.patch


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
Patch55:        x86-vmware-Use-Efficient-and-Correct-ALTERNATIVEs-fo.patch
Patch56:        x86-vmware-Log-kmsg-dump-on-panic.patch

# CVE:
Patch100:       apparmor-fix-use-after-free-in-sk_peer_label.patch
# Fix for CVE-2019-12379
Patch101:       consolemap-Fix-a-memory-leaking-bug-in-drivers-tty-v.patch
#Fix for CVE-2020-25704
Patch102:       perf-core-Fix-a-leak-in-perf-event-parse-addr-filter.patch
#Fix for CVE-2020-8694
Patch103:        powercap-restrict-energy-meter-to-root-access.patch

# Real-Time kernel (PREEMPT_RT patches)
Patch301:       0001-printk-rb-add-printk-ring-buffer-documentation.patch
Patch302:       0002-printk-rb-add-prb-locking-functions.patch
Patch303:       0003-printk-rb-define-ring-buffer-struct-and-initializer.patch
Patch304:       0004-printk-rb-add-writer-interface.patch
Patch305:       0005-printk-rb-add-basic-non-blocking-reading-interface.patch
Patch306:       0006-printk-rb-add-blocking-reader-support.patch
Patch307:       0007-printk-rb-add-functionality-required-by-printk.patch
Patch308:       0008-printk-add-ring-buffer-and-kthread.patch
Patch309:       0009-printk-remove-exclusive-console-hack.patch
Patch310:       printk-console-must-not-schedule-for-drivers.patch
Patch311:       0010-printk-redirect-emit-store-to-new-ringbuffer.patch
Patch312:       0011-printk_safe-remove-printk-safe-code.patch
Patch313:       0012-printk-minimize-console-locking-implementation.patch
Patch314:       0013-printk-track-seq-per-console.patch
Patch315:       0014-printk-do-boot_delay_msec-inside-printk_delay.patch
Patch316:       0015-printk-print-history-for-new-consoles.patch
Patch317:       0016-printk-implement-CON_PRINTBUFFER.patch
Patch318:       0017-printk-add-processor-number-to-output.patch
Patch319:       0018-console-add-write_atomic-interface.patch
Patch320:       0019-printk-introduce-emergency-messages.patch
Patch321:       0020-serial-8250-implement-write_atomic.patch
Patch322:       0021-printk-implement-KERN_CONT.patch
Patch323:       0022-printk-implement-dev-kmsg.patch
Patch324:       0023-printk-implement-syslog.patch
Patch325:       0024-printk-implement-kmsg_dump.patch
Patch326:       0025-printk-remove-unused-code.patch
Patch327:       printk-set-deferred-to-default-loglevel-enforce-mask.patch
Patch328:       serial-8250-remove-that-trylock-in-serial8250_consol.patch
Patch329:       serial-8250-export-symbols-which-are-used-by-symbols.patch
Patch330:       arm-remove-printk_nmi_.patch
Patch331:       powerpc-remove-printk_nmi_.patch
Patch332:       printk-only-allow-kernel-to-emergency-message.patch
Patch333:       printk-devkmsg-llseek-reset-clear-if-it-is-lost.patch
Patch334:       printk-print-rate-limitted-message-as-info.patch
Patch335:       printk-kmsg_dump-remove-mutex-usage.patch
Patch336:       printk-devkmsg-read-Return-EPIPE-when-the-first-mess.patch
Patch337:       printk-handle-iterating-while-buffer-changing.patch
Patch338:       printk-hack-out-emergency-loglevel-usage.patch
Patch339:       printk-Force-a-line-break-on-pr_cont-n.patch
Patch340:       serial-8250-only-atomic-lock-for-console.patch
Patch341:       serial-8250-fsl-ingenic-mtk-fix-atomic-console.patch
Patch342:       printk-fix-ifnullfree.cocci-warnings.patch
Patch343:       mm-fix-exec-activate_mm-vs-TLB-shootdown-and-lazy-tl.patch
Patch344:       0001-stop_machine-Add-function-and-caller-debug-info.patch
Patch345:       0002-sched-Fix-balance_callback.patch
Patch346:       0003-sched-hotplug-Ensure-only-per-cpu-kthreads-run-durin.patch
Patch347:       0004-sched-core-Wait-for-tasks-being-pushed-away-on-hotpl.patch
Patch348:       0005-workqueue-Manually-break-affinity-on-hotplug.patch
Patch349:       0006-sched-hotplug-Consolidate-task-migration-on-CPU-unpl.patch
Patch350:       0007-sched-Fix-hotplug-vs-CPU-bandwidth-control.patch
Patch351:       0008-sched-Massage-set_cpus_allowed.patch
Patch352:       0009-sched-Add-migrate_disable.patch
Patch353:       0010-sched-Fix-migrate_disable-vs-set_cpus_allowed_ptr.patch
Patch354:       0011-sched-core-Make-migrate-disable-and-CPU-hotplug-coop.patch
Patch355:       0012-sched-rt-Use-cpumask_any-_distribute.patch
Patch356:       0013-sched-rt-Use-the-full-cpumask-for-balancing.patch
Patch357:       0014-sched-lockdep-Annotate-pi_lock-recursion.patch
Patch358:       0015-sched-Fix-migrate_disable-vs-rt-dl-balancing.patch
Patch359:       0016-sched-proc-Print-accurate-cpumask-vs-migrate_disable.patch
Patch360:       0017-sched-Add-migrate_disable-tracepoints.patch
Patch361:       Use-CONFIG_PREEMPTION.patch
Patch362:       x86-entry-Use-should_resched-in-idtentry_exit_cond_r.patch
Patch363:       io_wq-Make-io_wqe-lock-a-raw_spinlock_t.patch
Patch364:       bus-mhi-Remove-include-of-rwlock_types.h.patch
Patch365:       cgroup-use-irqsave-in-cgroup_rstat_flush_locked.patch
Patch366:       mm-workingset-replace-IRQ-off-check-with-a-lockdep-a.patch
Patch367:       tpm-remove-tpm_dev_wq_lock.patch
Patch368:       shmem-Use-raw_spinlock_t-for-stat_lock.patch
Patch369:       net--Move-lockdep-where-it-belongs.patch
Patch370:       tcp-Remove-superfluous-BH-disable-around-listening_h.patch
Patch371:       x86-fpu--Do-not-disable-BH-on-RT.patch
Patch372:       softirq--Add-RT-variant.patch
Patch373:       tick-sched--Prevent-false-positive-softirq-pending-warnings-on-RT.patch
Patch374:       rcu--Prevent-false-positive-softirq-warning-on-RT.patch
Patch375:       softirq--Replace-barrier---with-cpu_relax---in-tasklet_unlock_wait--.patch
Patch376:       tasklets--Avoid-cancel-kill-deadlock-on-RT.patch
Patch377:       tasklets-Use-static-line-for-functions.patch
Patch378:       0001-locking-rtmutex-Remove-cruft.patch
Patch379:       0002-locking-rtmutex-Remove-output-from-deadlock-detector.patch
Patch380:       0003-locking-rtmutex-Move-rt_mutex_init-outside-of-CONFIG.patch
Patch381:       0004-locking-rtmutex-Remove-rt_mutex_timed_lock.patch
Patch382:       0005-locking-rtmutex-Handle-the-various-new-futex-race-co.patch
Patch383:       0006-futex-Fix-bug-on-when-a-requeued-RT-task-times-out.patch
Patch384:       0007-locking-rtmutex-Add-rtmutex_lock_killable.patch
Patch385:       0008-locking-rtmutex-Make-lock_killable-work.patch
Patch386:       0009-locking-spinlock-Split-the-lock-types-header.patch
Patch387:       0010-locking-rtmutex-Avoid-include-hell.patch
Patch388:       0011-lockdep-Reduce-header-files-in-debug_locks.h.patch
Patch389:       0012-locking-split-out-the-rbtree-definition.patch
Patch390:       0013-locking-rtmutex-Provide-rt_mutex_slowlock_locked.patch
Patch391:       0014-locking-rtmutex-export-lockdep-less-version-of-rt_mu.patch
Patch392:       0015-sched-Add-saved_state-for-tasks-blocked-on-sleeping-.patch
Patch393:       0016-locking-rtmutex-add-sleeping-lock-implementation.patch
Patch394:       0017-locking-rtmutex-Allow-rt_mutex_trylock-on-PREEMPT_RT.patch
Patch395:       0018-locking-rtmutex-add-mutex-implementation-based-on-rt.patch
Patch396:       0019-locking-rtmutex-add-rwsem-implementation-based-on-rt.patch
Patch397:       0020-locking-rtmutex-add-rwlock-implementation-based-on-r.patch
Patch398:       0021-locking-rtmutex-wire-up-RT-s-locking.patch
Patch399:       0022-locking-rtmutex-add-ww_mutex-addon-for-mutex-rt.patch
Patch400:       0023-locking-rtmutex-Use-custom-scheduling-function-for-s.patch
Patch401:       signal-revert-ptrace-preempt-magic.patch
Patch402:       preempt-nort-rt-variants.patch
Patch403:       mm-make-vmstat-rt-aware.patch
Patch404:       seqlock-Fix-multiple-kernel-doc-warnings.patch
Patch405:       0001-time-sched_clock-Use-raw_read_seqcount_latch-during-.patch
Patch406:       0002-mm-swap-Do-not-abuse-the-seqcount_t-latching-API.patch
Patch407:       0003-seqlock-Introduce-seqcount_latch_t.patch
Patch408:       0004-time-sched_clock-Use-seqcount_latch_t.patch
Patch409:       0005-timekeeping-Use-seqcount_latch_t.patch
Patch410:       0006-x86-tsc-Use-seqcount_latch_t.patch
Patch411:       0007-rbtree_latch-Use-seqcount_latch_t.patch
Patch412:       0008-seqlock-seqcount-latch-APIs-Only-allow-seqcount_latc.patch
Patch413:       0009-seqlock-seqcount_LOCKNAME_t-Standardize-naming-conve.patch
Patch414:       0010-seqlock-Use-unique-prefix-for-seqcount_t-property-ac.patch
Patch415:       0011-seqlock-seqcount_t-Implement-all-read-APIs-as-statem.patch
Patch416:       0012-seqlock-seqcount_LOCKNAME_t-Introduce-PREEMPT_RT-sup.patch
Patch417:       0013-seqlock-PREEMPT_RT-Do-not-starve-seqlock_t-writers.patch
Patch418:       0024-xfrm-Use-sequence-counter-with-associated-spinlock.patch
Patch419:       u64_stats-Disable-preemption-on-32bit-UP-SMP-with-RT.patch
Patch420:       fs-dcache-use-swait_queue-instead-of-waitqueue.patch
Patch421:       fs-dcache-disable-preemption-on-i_dir_seq-s-write-si.patch
Patch422:       net-Qdisc-use-a-seqlock-instead-seqcount.patch
Patch423:       net-Properly-annotate-the-try-lock-for-the-seqlock.patch
Patch424:       kconfig-disable-a-few-options-rt.patch
Patch425:       mm-disable-sloub-rt.patch
Patch426:       rcu-make-RCU_BOOST-default-on-RT.patch
Patch427:       sched-disable-rt-group-sched-on-rt.patch
Patch428:       net_disable_NET_RX_BUSY_POLL.patch
Patch429:       efi-Disable-runtime-services-on-RT.patch
Patch430:       efi-Allow-efi-runtime.patch
Patch431:       rt-local-irq-lock.patch
Patch432:       oleg-signal-rt-fix.patch
Patch433:       0001-Split-IRQ-off-and-zone-lock-while-freeing-pages-from.patch
Patch434:       0002-Split-IRQ-off-and-zone-lock-while-freeing-pages-from.patch
Patch435:       0003-mm-SLxB-change-list_lock-to-raw_spinlock_t.patch
Patch436:       0004-mm-SLUB-delay-giving-back-empty-slubs-to-IRQ-enabled.patch
Patch437:       mm-slub-Always-flush-the-delayed-empty-slubs-in-flus.patch
Patch438:       mm-page_alloc-Use-migrate_disable-in-drain_local_pag.patch
Patch439:       mm-page_alloc-rt-friendly-per-cpu-pages.patch
Patch440:       mm-slub-Make-object_map_lock-a-raw_spinlock_t.patch
Patch441:       slub-enable-irqs-for-no-wait.patch
Patch442:       slub-disable-SLUB_CPU_PARTIAL.patch
Patch443:       mm-memcontrol-Provide-a-local_lock-for-per-CPU-memcg.patch
Patch444:       mm-memcontrol-Don-t-call-schedule_work_on-in-preempt.patch
Patch445:       mm-memcontrol-do_not_disable_irq.patch
Patch446:       mm_zsmalloc_copy_with_get_cpu_var_and_locking.patch
Patch447:       mm-zswap-Use-local-lock-to-protect-per-CPU-data.patch
Patch448:       x86-kvm-require-const-tsc-for-rt.patch
Patch449:       wait.h-include-atomic.h.patch
Patch450:       hrtimer-Allow-raw-wakeups-during-boot.patch
Patch451:       sched-limit-nr-migrate.patch
Patch452:       sched-mmdrop-delayed.patch
Patch453:       kernel-sched-move-stack-kprobe-clean-up-to-__put_tas.patch
Patch454:       sched-might-sleep-do-not-account-rcu-depth.patch
Patch455:       sched-disable-ttwu-queue.patch
Patch456:       softirq-preempt-fix-3-re.patch
Patch457:       softirq-disable-softirq-stacks-for-rt.patch
Patch458:       net-core-use-local_bh_disable-in-netif_rx_ni.patch
Patch459:       pid.h-include-atomic.h.patch
Patch460:       ptrace-fix-ptrace-vs-tasklist_lock-race.patch
Patch461:       add_cpu_light.patch
Patch462:       ftrace-migrate-disable-tracing.patch
Patch463:       locking-don-t-check-for-__LINUX_SPINLOCK_TYPES_H-on-.patch
Patch464:       locking-Make-spinlock_t-and-rwlock_t-a-RCU-section-o.patch
Patch465:       rcu-Use-rcuc-threads-on-PREEMPT_RT-as-we-did.patch
Patch466:       rcu-enable-rcu_normal_after_boot-by-default-for-RT.patch
Patch467:       rcutorture-Avoid-problematic-critical-section-nestin.patch
Patch468:       mm-vmalloc-use-get-cpu-light.patch
Patch469:       block-mq-drop-preempt-disable.patch
Patch470:       md-raid5-percpu-handling-rt-aware.patch
Patch471:       scsi-fcoe-rt-aware.patch
Patch472:       sunrpc-make-svc_xprt_do_enqueue-use-get_cpu_light.patch
Patch473:       rt-introduce-cpu-chill.patch
Patch474:       fs-namespace-use-cpu-chill-in-trylock-loops.patch
Patch475:       debugobjects-rt.patch
Patch476:       skbufhead-raw-lock.patch
Patch477:       net-Dequeue-in-dev_cpu_dead-without-the-lock.patch
Patch478:       net-dev-always-take-qdisc-s-busylock-in-__dev_xmit_s.patch
Patch479:       irqwork-push_most_work_into_softirq_context.patch
Patch480:       x86-crypto-reduce-preempt-disabled-regions.patch
Patch481:       crypto-Reduce-preempt-disabled-regions-more-algos.patch
Patch482:       crypto-limit-more-FPU-enabled-sections.patch
Patch483:       crypto-cryptd-add-a-lock-instead-preempt_disable-loc.patch
Patch484:       panic-disable-random-on-rt.patch
Patch485:       x86-stackprot-no-random-on-rt.patch
Patch486:       random-make-it-work-on-rt.patch
Patch487:       upstream-net-rt-remove-preemption-disabling-in-netif_rx.patch
Patch488:       lockdep-no-softirq-accounting-on-rt.patch
Patch489:       lockdep-selftest-only-do-hardirq-context-test-for-raw-spinlock.patch
Patch490:       lockdep-selftest-fix-warnings-due-to-missing-PREEMPT.patch
Patch491:       lockdep-disable-self-test.patch
Patch492:       drmradeoni915_Use_preempt_disableenable_rt_where_recommended.patch
Patch493:       drm-i915-Don-t-disable-interrupts-on-PREEMPT_RT-duri.patch
Patch494:       drm-i915-disable-tracing-on-RT.patch
Patch495:       drm-i915-skip-DRM_I915_LOW_LEVEL_TRACEPOINTS-with-NO.patch
Patch496:       drm-i915-gt-Only-disable-interrupts-for-the-timeline.patch
Patch497:       cpuset-Convert-callback_lock-to-raw_spinlock_t.patch
Patch498:       x86-Enable-RT.patch
Patch499:       mm-rt-kmap-atomic-scheduling.patch
Patch500:       x86-highmem-add-a-already-used-pte-check.patch
Patch501:       arm-highmem-flush-tlb-on-unmap.patch
Patch502:       arm-enable-highmem-for-rt.patch
Patch503:       mm-scatterlist-dont-disable-irqs-on-RT.patch
Patch504:       preempt-lazy-support.patch
Patch505:       x86-preempt-lazy.patch
Patch506:       arm-preempt-lazy-support.patch
Patch507:       powerpc-preempt-lazy-support.patch
Patch508:       arch-arm64-Add-lazy-preempt-support.patch
Patch509:       jump-label-rt.patch
Patch510:       leds-trigger-disable-CPU-trigger-on-RT.patch
Patch511:       drivers-tty-fix-omap-lock-crap.patch
Patch512:       drivers-tty-pl011-irq-disable-madness.patch
Patch513:       ARM-enable-irq-in-translation-section-permission-fau.patch
Patch514:       genirq-update-irq_set_irqchip_state-documentation.patch
Patch515:       KVM-arm-arm64-downgrade-preempt_disable-d-region-to-.patch
Patch516:       arm64-fpsimd-use-preemp_disable-in-addition-to-local.patch
Patch517:       x86-Enable-RT-also-on-32bit.patch
Patch518:       ARM-Allow-to-enable-RT.patch
Patch519:       ARM64-Allow-to-enable-RT.patch
Patch520:       powerpc-pseries-iommu-Use-a-locallock-instead-local_ir.patch
Patch521:       powerpc-kvm-Disable-in-kernel-MPIC-emulation-for-PRE.patch
Patch522:       power-disable-highmem-on-rt.patch
Patch523:       powerpc-stackprotector-work-around-stack-guard-init-.patch
Patch524:       POWERPC-Allow-to-enable-RT.patch
Patch525:       mips-disable-highmem-on-rt.patch
Patch526:       drivers-block-zram-Replace-bit-spinlocks-with-rtmute.patch
Patch527:       drivers-zram-Don-t-disable-preemption-in-zcomp_strea.patch
Patch528:       tpm_tis-fix-stall-after-iowrite-s.patch
Patch529:       signals-allow-rt-tasks-to-cache-one-sigqueue-struct.patch
Patch530:       signal-Prevent-double-free-of-user-struct.patch
Patch531:       genirq-disable-irqpoll-on-rt.patch
Patch532:       sysfs-realtime-entry.patch
# Keep rt_version matched up with this patch.
Patch533:       localversion.patch

Patch600:       0000-Revert-clockevents-Stop-unused-clockevent-devices.patch

%if 0%{?kat_build:1}
Patch1000:        %{kat_build}.patch
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
%patch102 -p1
%patch103 -p1

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
%patch600 -p1


%if 0%{?kat_build:1}
%patch1000 -p1
%endif

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
patch -p1 < %{SOURCE7}
patch -p1 < %{SOURCE8}
patch -p1 < %{SOURCE9}
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
