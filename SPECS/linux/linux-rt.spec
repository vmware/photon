%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%global security_hardening none
Summary:        Kernel
Name:           linux-rt
Version:        5.9.0
# Keep rt_version matched up with REBASE.patch
%define rt_version rt10
Release:        rc7.1%{?kat_build:.%kat}%{?dist}
License:    	GPLv2
URL:        	http://www.kernel.org/
Group:        	System Environment/Kernel
Vendor:         VMware, Inc.
Distribution: 	Photon

#TODO: Use rt_version in uname_r after 5.9 goes out of rc
%define uname_r %{version}-%{release}-rt

#TODO: remove rcN after 5.9 goes out of rc
%define lnx_rc_ver 5.9.0-rc7
%define lnx_rc_local_ver .1%{?kat_build:.kat}%{?dist}

Source0:        http://www.kernel.org/pub/linux/kernel/v5.x/linux-%{lnx_rc_ver}.tar.xz
%define sha1 linux=b8809bb16a9591303ac2bb84e19a597e26b69c4c
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
Patch331:       printk-only-allow-kernel-to-emergency-message.patch
Patch332:       printk-devkmsg-llseek-reset-clear-if-it-is-lost.patch
Patch333:       printk-print-rate-limitted-message-as-info.patch
Patch334:       printk-kmsg_dump-remove-mutex-usage.patch
Patch335:       printk-devkmsg-read-Return-EPIPE-when-the-first-mess.patch
Patch336:       printk-handle-iterating-while-buffer-changing.patch
Patch337:       printk-hack-out-emergency-loglevel-usage.patch
Patch338:       printk-Force-a-line-break-on-pr_cont-n.patch
Patch339:       serial-8250-only-atomic-lock-for-console.patch
Patch340:       serial-8250-fsl-ingenic-mtk-fix-atomic-console.patch
Patch341:       printk-fix-ifnullfree.cocci-warnings.patch
Patch342:       mm-fix-exec-activate_mm-vs-TLB-shootdown-and-lazy-tl.patch
Patch343:       Use-CONFIG_PREEMPTION.patch
Patch344:       x86-entry-Use-should_resched-in-idtentry_exit_cond_r.patch
Patch345:       io_wq-Make-io_wqe-lock-a-raw_spinlock_t.patch
Patch346:       bus-mhi-Remove-include-of-rwlock_types.h.patch
Patch347:       cgroup-use-irqsave-in-cgroup_rstat_flush_locked.patch
Patch348:       mm-workingset-replace-IRQ-off-check-with-a-lockdep-a.patch
Patch349:       tpm-remove-tpm_dev_wq_lock.patch
Patch350:       shmem-Use-raw_spinlock_t-for-stat_lock.patch
Patch351:       net--Move-lockdep-where-it-belongs.patch
Patch352:       x86-fpu--Do-not-disable-BH-on-RT.patch
Patch353:       softirq--Add-RT-variant.patch
Patch354:       tick-sched--Prevent-false-positive-softirq-pending-warnings-on-RT.patch
Patch355:       rcu--Prevent-false-positive-softirq-warning-on-RT.patch
Patch356:       softirq--Replace-barrier---with-cpu_relax---in-tasklet_unlock_wait--.patch
Patch357:       tasklets--Avoid-cancel-kill-deadlock-on-RT.patch
Patch358:       tasklets-Use-static-line-for-functions.patch
Patch359:       signal-revert-ptrace-preempt-magic.patch
Patch360:       preempt-nort-rt-variants.patch
Patch361:       mm-make-vmstat-rt-aware.patch
Patch362:       seqlock-Fix-multiple-kernel-doc-warnings.patch
Patch363:       0001-time-sched_clock-Use-raw_read_seqcount_latch-during-.patch
Patch364:       0002-mm-swap-Do-not-abuse-the-seqcount_t-latching-API.patch
Patch365:       0003-seqlock-Introduce-seqcount_latch_t.patch
Patch366:       0004-time-sched_clock-Use-seqcount_latch_t.patch
Patch367:       0005-timekeeping-Use-seqcount_latch_t.patch
Patch368:       0006-x86-tsc-Use-seqcount_latch_t.patch
Patch369:       0007-rbtree_latch-Use-seqcount_latch_t.patch
Patch370:       0008-seqlock-seqcount-latch-APIs-Only-allow-seqcount_latc.patch
Patch371:       0009-seqlock-seqcount_LOCKNAME_t-Standardize-naming-conve.patch
Patch372:       0010-seqlock-Use-unique-prefix-for-seqcount_t-property-ac.patch
Patch373:       0011-seqlock-seqcount_t-Implement-all-read-APIs-as-statem.patch
Patch374:       0012-seqlock-seqcount_LOCKNAME_t-Introduce-PREEMPT_RT-sup.patch
Patch375:       0013-seqlock-PREEMPT_RT-Do-not-starve-seqlock_t-writers.patch
Patch376:       0024-xfrm-Use-sequence-counter-with-associated-spinlock.patch
Patch377:       u64_stats-Disable-preemption-on-32bit-UP-SMP-with-RT.patch
Patch378:       fs-dcache-use-swait_queue-instead-of-waitqueue.patch
Patch379:       fs-dcache-disable-preemption-on-i_dir_seq-s-write-si.patch
Patch380:       net-Qdisc-use-a-seqlock-instead-seqcount.patch
Patch381:       net-Properly-annotate-the-try-lock-for-the-seqlock.patch
Patch382:       kconfig-disable-a-few-options-rt.patch
Patch383:       mm-disable-sloub-rt.patch
Patch384:       rcu-make-RCU_BOOST-default-on-RT.patch
Patch385:       sched-disable-rt-group-sched-on-rt.patch
Patch386:       net_disable_NET_RX_BUSY_POLL.patch
Patch387:       efi-Disable-runtime-services-on-RT.patch
Patch388:       efi-Allow-efi-runtime.patch
Patch389:       rt-local-irq-lock.patch
Patch390:       oleg-signal-rt-fix.patch
Patch391:       0001-Split-IRQ-off-and-zone-lock-while-freeing-pages-from.patch
Patch392:       0002-Split-IRQ-off-and-zone-lock-while-freeing-pages-from.patch
Patch393:       0003-mm-SLxB-change-list_lock-to-raw_spinlock_t.patch
Patch394:       0004-mm-SLUB-delay-giving-back-empty-slubs-to-IRQ-enabled.patch
Patch395:       mm-slub-Always-flush-the-delayed-empty-slubs-in-flus.patch
Patch396:       mm-page_alloc-Use-migrate_disable-in-drain_local_pag.patch
Patch397:       mm-page_alloc-rt-friendly-per-cpu-pages.patch
Patch398:       mm-slub-Make-object_map_lock-a-raw_spinlock_t.patch
Patch399:       slub-enable-irqs-for-no-wait.patch
Patch400:       slub-disable-SLUB_CPU_PARTIAL.patch
Patch401:       mm-memcontrol-Provide-a-local_lock-for-per-CPU-memcg.patch
Patch402:       mm-memcontrol-Don-t-call-schedule_work_on-in-preempt.patch
Patch403:       mm-memcontrol-do_not_disable_irq.patch
Patch404:       mm_zsmalloc_copy_with_get_cpu_var_and_locking.patch
Patch405:       mm-zswap-Use-local-lock-to-protect-per-CPU-data.patch
Patch406:       x86-kvm-require-const-tsc-for-rt.patch
Patch407:       wait.h-include-atomic.h.patch
Patch408:       hrtimer-Allow-raw-wakeups-during-boot.patch
Patch409:       sched-limit-nr-migrate.patch
Patch410:       sched-mmdrop-delayed.patch
Patch411:       kernel-sched-move-stack-kprobe-clean-up-to-__put_tas.patch
Patch412:       sched-rt-mutex-wakeup.patch
Patch413:       sched-might-sleep-do-not-account-rcu-depth.patch
Patch414:       sched-disable-ttwu-queue.patch
Patch415:       softirq-preempt-fix-3-re.patch
Patch416:       softirq-disable-softirq-stacks-for-rt.patch
Patch417:       net-core-use-local_bh_disable-in-netif_rx_ni.patch
Patch418:       rtmutex-futex-prepare-rt.patch
Patch419:       futex-requeue-pi-fix.patch
Patch420:       futex-Ensure-lock-unlock-symetry-versus-pi_lock-and-.patch
Patch421:       pid.h-include-atomic.h.patch
Patch422:       rtmutex-lock-killable.patch
Patch423:       rtmutex-Make-lock_killable-work.patch
Patch424:       spinlock-types-separate-raw.patch
Patch425:       rtmutex-avoid-include-hell.patch
Patch426:       locking-split-out-the-rbtree-definition.patch
Patch427:       rtmutex-Provide-rt_mutex_slowlock_locked.patch
Patch428:       rtmutex-export-lockdep-less-version-of-rt_mutex-s-lo.patch
Patch429:       rtmutex-add-sleeping-lock-implementation.patch
Patch430:       cond-resched-lock-rt-tweak.patch
Patch431:       locking-rtmutex-Clean-pi_blocked_on-in-the-error-cas.patch
Patch432:       rtmutex-trylock-is-okay-on-RT.patch
Patch433:       rtmutex-add-mutex-implementation-based-on-rtmutex.patch
Patch434:       rtmutex-add-rwsem-implementation-based-on-rtmutex.patch
Patch435:       rtmutex-add-rwlock-implementation-based-on-rtmutex.patch
Patch436:       rtmutex-wire-up-RT-s-locking.patch
Patch437:       rwsem-Provide-down_read_non_owner-and-up_read_non_ow.patch
Patch438:       rtmutex-add-ww_mutex-addon-for-mutex-rt.patch
Patch439:       mutex-Move-the-ww_mutext-definition-back-to-ww_mutex.patch
Patch440:       locking-rt-mutex-fix-deadlock-in-device-mapper-block.patch
Patch441:       locking-rt-mutex-Flush-block-plug-on-__down_read.patch
Patch442:       ptrace-fix-ptrace-vs-tasklist_lock-race.patch
Patch443:       add_migrate_disable.patch
Patch444:       sched-migrate_enable-Use-stop_one_cpu_nowait.patch
Patch445:       sched-migrate_enable-Use-per-cpu-cpu_stop_work.patch
Patch446:       sched-migrate_enable-Remove-__schedule-call.patch
Patch447:       ftrace-migrate-disable-tracing.patch
Patch448:       futex-workaround-migrate_disable-enable-in-different.patch
Patch449:       locking-don-t-check-for-__LINUX_SPINLOCK_TYPES_H-on-.patch
Patch450:       locking-Make-spinlock_t-and-rwlock_t-a-RCU-section-o.patch
Patch451:       rcu-Use-rcuc-threads-on-PREEMPT_RT-as-we-did.patch
Patch452:       rcu-enable-rcu_normal_after_boot-by-default-for-RT.patch
Patch453:       rcutorture-Avoid-problematic-critical-section-nestin.patch
Patch454:       mm-vmalloc-use-get-cpu-light.patch
Patch455:       block-mq-drop-preempt-disable.patch
Patch456:       md-raid5-percpu-handling-rt-aware.patch
Patch457:       scsi-fcoe-rt-aware.patch
Patch458:       sunrpc-make-svc_xprt_do_enqueue-use-get_cpu_light.patch
Patch459:       rt-introduce-cpu-chill.patch
Patch460:       fs-namespace-use-cpu-chill-in-trylock-loops.patch
Patch461:       debugobjects-rt.patch
Patch462:       skbufhead-raw-lock.patch
Patch463:       net-Dequeue-in-dev_cpu_dead-without-the-lock.patch
Patch464:       net-dev-always-take-qdisc-s-busylock-in-__dev_xmit_s.patch
Patch465:       irqwork-push_most_work_into_softirq_context.patch
Patch466:       x86-crypto-reduce-preempt-disabled-regions.patch
Patch467:       crypto-Reduce-preempt-disabled-regions-more-algos.patch
Patch468:       crypto-limit-more-FPU-enabled-sections.patch
Patch469:       crypto-cryptd-add-a-lock-instead-preempt_disable-loc.patch
Patch470:       panic-disable-random-on-rt.patch
Patch471:       x86-stackprot-no-random-on-rt.patch
Patch472:       random-make-it-work-on-rt.patch
Patch473:       upstream-net-rt-remove-preemption-disabling-in-netif_rx.patch
Patch474:       lockdep-no-softirq-accounting-on-rt.patch
Patch475:       lockdep-selftest-only-do-hardirq-context-test-for-raw-spinlock.patch
Patch476:       lockdep-selftest-fix-warnings-due-to-missing-PREEMPT.patch
Patch477:       lockdep-Reduce-header-files-in-debug_locks.h.patch
Patch478:       lockdep-disable-self-test.patch
Patch479:       drmradeoni915_Use_preempt_disableenable_rt_where_recommended.patch
Patch480:       drm-i915-Don-t-disable-interrupts-on-PREEMPT_RT-duri.patch
Patch481:       drm-i915-disable-tracing-on-RT.patch
Patch482:       drm-i915-skip-DRM_I915_LOW_LEVEL_TRACEPOINTS-with-NO.patch
Patch483:       drm-i915-gt-Only-disable-interrupts-for-the-timeline.patch
Patch484:       cpuset-Convert-callback_lock-to-raw_spinlock_t.patch
Patch485:       x86-Enable-RT.patch
Patch486:       mm-rt-kmap-atomic-scheduling.patch
Patch487:       x86-highmem-add-a-already-used-pte-check.patch
Patch488:       arm-highmem-flush-tlb-on-unmap.patch
Patch489:       arm-enable-highmem-for-rt.patch
Patch490:       mm-scatterlist-dont-disable-irqs-on-RT.patch
Patch491:       preempt-lazy-support.patch
Patch492:       x86-preempt-lazy.patch
Patch493:       arm-preempt-lazy-support.patch
Patch494:       powerpc-preempt-lazy-support.patch
Patch495:       arch-arm64-Add-lazy-preempt-support.patch
Patch496:       jump-label-rt.patch
Patch497:       leds-trigger-disable-CPU-trigger-on-RT.patch
Patch498:       drivers-tty-fix-omap-lock-crap.patch
Patch499:       drivers-tty-pl011-irq-disable-madness.patch
Patch500:       ARM-enable-irq-in-translation-section-permission-fau.patch
Patch501:       genirq-update-irq_set_irqchip_state-documentation.patch
Patch502:       KVM-arm-arm64-downgrade-preempt_disable-d-region-to-.patch
Patch503:       arm64-fpsimd-use-preemp_disable-in-addition-to-local.patch
Patch504:       x86-Enable-RT-also-on-32bit.patch
Patch505:       ARM-Allow-to-enable-RT.patch
Patch506:       ARM64-Allow-to-enable-RT.patch
Patch507:       powerpc-pseries-iommu-Use-a-locallock-instead-local_ir.patch
Patch508:       powerpc-kvm-Disable-in-kernel-MPIC-emulation-for-PRE.patch
Patch509:       power-disable-highmem-on-rt.patch
Patch510:       powerpc-stackprotector-work-around-stack-guard-init-.patch
Patch511:       POWERPC-Allow-to-enable-RT.patch
Patch512:       mips-disable-highmem-on-rt.patch
Patch513:       drivers-block-zram-Replace-bit-spinlocks-with-rtmute.patch
Patch514:       drivers-zram-Don-t-disable-preemption-in-zcomp_strea.patch
Patch515:       tpm_tis-fix-stall-after-iowrite-s.patch
Patch516:       signals-allow-rt-tasks-to-cache-one-sigqueue-struct.patch
Patch517:       signal-Prevent-double-free-of-user-struct.patch
Patch518:       genirq-disable-irqpoll-on-rt.patch
Patch519:       sysfs-realtime-entry.patch
# Keep rt_version matched up with this patch.
# TODO: Enable this patch after 5.9 GA
# Patch520:       localversion.patch

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
#TODO: remove rcN after 5.9 goes out of rc
%setup -q -n linux-%{lnx_rc_ver}
%ifarch x86_64
%setup -D -b 3 -n linux-%{lnx_rc_ver}
%setup -D -b 6 -n linux-%{lnx_rc_ver}
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
# TODO: Enable this patch after 5.9 GA.
#%patch520 -p1


%if 0%{?kat_build:1}
%patch1000 -p1
%endif

%build
make mrproper

%ifarch x86_64
cp %{SOURCE1} .config
arch="x86_64"
%endif

sed -i 's/CONFIG_LOCALVERSION="-rt"/CONFIG_LOCALVERSION="%{lnx_rc_local_ver}-rt"/' .config

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
%ifarch x86_64
archdir="x86"
%endif

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
find arch/${archdir}/include include scripts -type f | xargs  sh -c 'cp --parents "$@" %{buildroot}%{_usrsrc}/%{name}-headers-%{uname_r}' copy
find $(find arch/${archdir} -name include -o -name scripts -type d) -type f | xargs  sh -c 'cp --parents "$@" %{buildroot}%{_usrsrc}/%{name}-headers-%{uname_r}' copy
find arch/${archdir}/include Module.symvers include scripts -type f | xargs  sh -c 'cp --parents "$@" %{buildroot}%{_usrsrc}/%{name}-headers-%{uname_r}' copy
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
