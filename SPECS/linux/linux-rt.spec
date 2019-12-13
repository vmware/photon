%global security_hardening none
Summary:        Kernel
Name:           linux-rt
Version:        4.19.82
# Keep rt_version matched up with REBASE.patch
%define rt_version rt30
Release:        2%{?kat_build:.%kat_build}%{?dist}
License:    	GPLv2
URL:        	http://www.kernel.org/
Group:        	System Environment/Kernel
Vendor:         VMware, Inc.
Distribution: 	Photon
Source0:        http://www.kernel.org/pub/linux/kernel/v4.x/linux-%{version}.tar.xz
%define sha1 linux=358ecd8e4b70a3396e2bbc2a15f29724bafde87c
Source1:	config-rt
Source2:	initramfs.trigger
Source3:	xr_usb_serial_common_lnx-3.6-and-newer-pak.tar.xz
%define sha1 xr=74df7143a86dd1519fa0ccf5276ed2225665a9db
Source4:        update_photon_cfg.postun
Source5:        check_for_config_applicability.inc
# common
Patch0:         linux-4.14-Log-kmsg-dump-on-panic.patch
Patch1:         double-tcp_mem-limits.patch
# TODO: disable this patch, check for regressions
#Patch2:         linux-4.9-watchdog-Disable-watchdog-on-virtual-machines.patch
Patch3:         SUNRPC-Do-not-reuse-srcport-for-TIME_WAIT-socket.patch
Patch4:         SUNRPC-xs_bind-uses-ip_local_reserved_ports_linux_rt.patch
Patch5:         vsock-transport-for-9p.patch
Patch6:         4.18-x86-vmware-STA-support.patch
Patch7:         9p-trans_fd-extend-port-variable-to-u32.patch
Patch8:         vsock-delay-detach-of-QP-with-outgoing-data.patch
# ttyXRUSB support
Patch11:	usb-acm-exclude-exar-usb-serial-ports.patch
#FIPS patches - allow some algorithms
Patch24:        4.18-Allow-some-algo-tests-for-FIPS.patch
Patch26:        4.18-add-sysctl-to-disallow-unprivileged-CLONE_NEWUSER-by-default.patch
# Out-of-tree patches from AppArmor:
Patch29:        4.17-0001-apparmor-patch-to-provide-compatibility-with-v2.x-ne.patch
Patch30:        4.17-0002-apparmor-af_unix-mediation.patch
Patch31:        4.17-0003-apparmor-fix-use-after-free-in-sk_peer_label.patch
# RDRAND-based RNG driver to enhance the kernel's entropy pool:
Patch32:        4.18-0001-hwrng-rdrand-Add-RNG-driver-based-on-x86-rdrand-inst.patch
# Fix for CVE-2019-12456
Patch33:        0001-scsi-mpt3sas_ctl-fix-double-fetch-bug-in-_ctl_ioctl_.patch
# Fix for CVE-2019-12379
Patch34:        0001-consolemap-Fix-a-memory-leaking-bug-in-drivers-tty-v.patch
# Fix for CVE-2019-12380
Patch35:        0001-efi-x86-Add-missing-error-handling-to-old_memmap-1-1.patch
# Fix for CVE-2019-12381
Patch36:        0001-ip_sockglue-Fix-missing-check-bug-in-ip_ra_control.patch
# Fix for CVE-2019-12378
Patch38:        0001-ipv6_sockglue-Fix-a-missing-check-bug-in-ip6_ra_cont.patch
# Fix for CVE-2019-12455
Patch39:        0001-clk-sunxi-fix-a-missing-check-bug-in-sunxi_divs_clk_.patch

# Real-Time kernel (PREEMPT_RT patches)
Patch201:        0001-ARM-at91-add-TCB-registers-definitions.patch
Patch202:        0002-clocksource-drivers-Add-a-new-driver-for-the-Atmel-A.patch
Patch203:        0003-clocksource-drivers-timer-atmel-tcb-add-clockevent-d.patch
Patch204:        0004-clocksource-drivers-atmel-pit-make-option-silent.patch
Patch205:        0005-ARM-at91-Implement-clocksource-selection.patch
Patch206:        0006-ARM-configs-at91-use-new-TCB-timer-driver.patch
Patch207:        0007-ARM-configs-at91-unselect-PIT.patch
Patch208:        0008-irqchip-gic-v3-its-Move-pending-table-allocation-to-.patch
Patch209:        0009-kthread-convert-worker-lock-to-raw-spinlock.patch
Patch210:        0010-crypto-caam-qi-simplify-CGR-allocation-freeing.patch
Patch211:        0011-sched-fair-Robustify-CFS-bandwidth-timer-locking.patch
Patch212:        0012-arm-Convert-arm-boot_lock-to-raw.patch
Patch213:        0013-x86-ioapic-Don-t-let-setaffinity-unmask-threaded-EOI.patch
Patch214:        0014-cgroup-use-irqsave-in-cgroup_rstat_flush_locked.patch
Patch215:        0015-fscache-initialize-cookie-hash-table-raw-spinlocks.patch
Patch216:        0016-Drivers-hv-vmbus-include-header-for-get_irq_regs.patch
Patch217:        0017-percpu-include-irqflags.h-for-raw_local_irq_save.patch
Patch218:        0018-efi-Allow-efi-runtime.patch
Patch219:        0019-x86-efi-drop-task_lock-from-efi_switch_mm.patch
Patch220:        0020-arm64-KVM-compute_layout-before-altenates-are-applie.patch
Patch221:        0021-of-allocate-free-phandle-cache-outside-of-the-devtre.patch
Patch222:        0022-mm-kasan-make-quarantine_lock-a-raw_spinlock_t.patch
Patch223:        0023-EXP-rcu-Revert-expedited-GP-parallelization-cleverne.patch
Patch224:        0024-kmemleak-Turn-kmemleak_lock-to-raw-spinlock-on-RT.patch
Patch225:        0025-NFSv4-replace-seqcount_t-with-a-seqlock_t.patch
Patch226:        0026-kernel-sched-Provide-a-pointer-to-the-valid-CPU-mask.patch
Patch227:        0027-kernel-sched-core-add-migrate_disable.patch
Patch228:        0028-sched-migrate_disable-Add-export_symbol_gpl-for-__mi.patch
Patch229:        0029-arm-at91-do-not-disable-enable-clocks-in-a-row.patch
Patch230:        0030-clocksource-TCLIB-Allow-higher-clock-rates-for-clock.patch
Patch231:        0031-timekeeping-Split-jiffies-seqlock.patch
Patch232:        0032-signal-Revert-ptrace-preempt-magic.patch
Patch233:        0033-net-sched-Use-msleep-instead-of-yield.patch
Patch234:        0034-dm-rq-remove-BUG_ON-irqs_disabled-check.patch
Patch235:        0035-usb-do-no-disable-interrupts-in-giveback.patch
Patch236:        0036-rt-Provide-PREEMPT_RT_BASE-config-switch.patch
Patch237:        0037-cpumask-Disable-CONFIG_CPUMASK_OFFSTACK-for-RT.patch
Patch238:        0038-jump-label-disable-if-stop_machine-is-used.patch
Patch239:        0039-kconfig-Disable-config-options-which-are-not-RT-comp.patch
Patch240:        0040-lockdep-disable-self-test.patch
Patch241:        0041-mm-Allow-only-slub-on-RT.patch
Patch242:        0042-locking-Disable-spin-on-owner-for-RT.patch
Patch243:        0043-rcu-Disable-RCU_FAST_NO_HZ-on-RT.patch
Patch244:        0044-rcu-make-RCU_BOOST-default-on-RT.patch
Patch245:        0045-sched-Disable-CONFIG_RT_GROUP_SCHED-on-RT.patch
Patch246:        0046-net-core-disable-NET_RX_BUSY_POLL.patch
Patch247:        0047-arm-disable-NEON-in-kernel-mode.patch
Patch248:        0048-powerpc-Use-generic-rwsem-on-RT.patch
Patch249:        0049-powerpc-kvm-Disable-in-kernel-MPIC-emulation-for-PRE.patch
Patch250:        0050-powerpc-Disable-highmem-on-RT.patch
Patch251:        0051-mips-Disable-highmem-on-RT.patch
Patch252:        0052-x86-Use-generic-rwsem_spinlocks-on-rt.patch
Patch253:        0053-leds-trigger-disable-CPU-trigger-on-RT.patch
Patch254:        0054-cpufreq-drop-K8-s-driver-from-beeing-selected.patch
Patch255:        0055-md-disable-bcache.patch
Patch256:        0056-efi-Disable-runtime-services-on-RT.patch
Patch257:        0057-printk-Add-a-printk-kill-switch.patch
Patch258:        0058-printk-Add-force_early_printk-boot-param-to-help-wit.patch
Patch259:        0059-preempt-Provide-preempt_-_-no-rt-variants.patch
Patch260:        0060-futex-workaround-migrate_disable-enable-in-different.patch
Patch261:        0061-rt-Add-local-irq-locks.patch
Patch262:        0062-locallock-provide-get-put-_locked_ptr-variants.patch
Patch263:        0063-mm-scatterlist-Do-not-disable-irqs-on-RT.patch
Patch264:        0064-signal-x86-Delay-calling-signals-in-atomic.patch
Patch265:        0065-x86-signal-delay-calling-signals-on-32bit.patch
Patch266:        0066-buffer_head-Replace-bh_uptodate_lock-for-rt.patch
Patch267:        0067-fs-jbd-jbd2-Make-state-lock-and-journal-head-lock-rt.patch
Patch268:        0068-list_bl-Make-list-head-locking-RT-safe.patch
Patch269:        0069-list_bl-fixup-bogus-lockdep-warning.patch
Patch270:        0070-genirq-Disable-irqpoll-on-rt.patch
Patch271:        0071-genirq-Force-interrupt-thread-on-RT.patch
Patch272:        0072-Split-IRQ-off-and-zone-lock-while-freeing-pages-from.patch
Patch273:        0073-Split-IRQ-off-and-zone-lock-while-freeing-pages-from.patch
Patch274:        0074-mm-SLxB-change-list_lock-to-raw_spinlock_t.patch
Patch275:        0075-mm-SLUB-delay-giving-back-empty-slubs-to-IRQ-enabled.patch
Patch276:        0076-mm-page_alloc-rt-friendly-per-cpu-pages.patch
Patch277:        0077-mm-swap-Convert-to-percpu-locked.patch
Patch278:        0078-mm-perform-lru_add_drain_all-remotely.patch
Patch279:        0079-mm-vmstat-Protect-per-cpu-variables-with-preempt-dis.patch
Patch280:        0080-ARM-Initialize-split-page-table-locks-for-vector-pag.patch
Patch281:        0081-mm-Enable-SLUB-for-RT.patch
Patch282:        0082-slub-Enable-irqs-for-__GFP_WAIT.patch
Patch283:        0083-slub-Disable-SLUB_CPU_PARTIAL.patch
Patch284:        0084-mm-memcontrol-Don-t-call-schedule_work_on-in-preempt.patch
Patch285:        0085-mm-memcontrol-Replace-local_irq_disable-with-local-l.patch
Patch286:        0086-mm-zsmalloc-copy-with-get_cpu_var-and-locking.patch
Patch287:        0087-x86-mm-pat-disable-preemption-__split_large_page-aft.patch
Patch288:        0088-radix-tree-use-local-locks.patch
Patch289:        0089-timers-Prepare-for-full-preemption.patch
Patch290:        0090-x86-kvm-Require-const-tsc-for-RT.patch
Patch291:        0091-pci-switchtec-Don-t-use-completion-s-wait-queue.patch
Patch292:        0092-wait.h-include-atomic.h.patch
Patch293:        0093-work-simple-Simple-work-queue-implemenation.patch
Patch294:        0094-work-simple-drop-a-shit-statement-in-SWORK_EVENT_PEN.patch
Patch295:        0095-completion-Use-simple-wait-queues.patch
Patch296:        0096-fs-aio-simple-simple-work.patch
Patch297:        0097-genirq-Do-not-invoke-the-affinity-callback-via-a-wor.patch
Patch298:        0098-time-hrtimer-avoid-schedule_work-with-interrupts-dis.patch
Patch299:        0099-hrtimer-consolidate-hrtimer_init-hrtimer_init_sleepe.patch
Patch300:        0100-hrtimers-Prepare-full-preemption.patch
Patch301:        0101-hrtimer-by-timers-by-default-into-the-softirq-contex.patch
Patch302:        0102-sched-fair-Make-the-hrtimers-non-hard-again.patch
Patch303:        0103-hrtimer-Move-schedule_work-call-to-helper-thread.patch
Patch304:        0104-hrtimer-move-state-change-before-hrtimer_cancel-in-d.patch
Patch305:        0105-posix-timers-Thread-posix-cpu-timers-on-rt.patch
Patch306:        0106-sched-Move-task_struct-cleanup-to-RCU.patch
Patch307:        0107-sched-Limit-the-number-of-task-migrations-per-batch.patch
Patch308:        0108-sched-Move-mmdrop-to-RCU-on-RT.patch
Patch309:        0109-kernel-sched-move-stack-kprobe-clean-up-to-__put_tas.patch
Patch310:        0110-sched-Add-saved_state-for-tasks-blocked-on-sleeping-.patch
Patch311:        0111-sched-Do-not-account-rcu_preempt_depth-on-RT-in-migh.patch
Patch312:        0112-sched-Use-the-proper-LOCK_OFFSET-for-cond_resched.patch
Patch313:        0113-sched-Disable-TTWU_QUEUE-on-RT.patch
Patch314:        0114-sched-workqueue-Only-wake-up-idle-workers-if-not-blo.patch
Patch315:        0115-rt-Increase-decrease-the-nr-of-migratory-tasks-when-.patch
Patch316:        0116-hotplug-Lightweight-get-online-cpus.patch
Patch317:        0117-trace-Add-migrate-disabled-counter-to-tracing-output.patch
Patch318:        0118-lockdep-Make-it-RT-aware.patch
Patch319:        0119-tasklet-Prevent-tasklets-from-going-into-infinite-sp.patch
Patch320:        0120-softirq-Check-preemption-after-reenabling-interrupts.patch
Patch321:        0121-softirq-Disable-softirq-stacks-for-RT.patch
Patch322:        0122-softirq-Split-softirq-locks.patch
Patch323:        0123-net-core-use-local_bh_disable-in-netif_rx_ni.patch
Patch324:        0124-genirq-Allow-disabling-of-softirq-processing-in-irq-.patch
Patch325:        0125-softirq-split-timer-softirqs-out-of-ksoftirqd.patch
Patch326:        0126-softirq-Avoid-local_softirq_pending-messages-if-ksof.patch
Patch327:        0127-softirq-Avoid-local_softirq_pending-messages-if-task.patch
Patch328:        0128-rtmutex-trylock-is-okay-on-RT.patch
Patch329:        0129-fs-nfs-turn-rmdir_sem-into-a-semaphore.patch
Patch330:        0130-rtmutex-Handle-the-various-new-futex-race-conditions.patch
Patch331:        0131-futex-Fix-bug-on-when-a-requeued-RT-task-times-out.patch
Patch332:        0132-futex-Ensure-lock-unlock-symetry-versus-pi_lock-and-.patch
Patch333:        0133-pid.h-include-atomic.h.patch
Patch334:        0134-arm-include-definition-for-cpumask_t.patch
Patch335:        0135-locking-locktorture-Do-NOT-include-rwlock.h-directly.patch
Patch336:        0136-rtmutex-Add-rtmutex_lock_killable.patch
Patch337:        0137-rtmutex-Make-lock_killable-work.patch
Patch338:        0138-spinlock-Split-the-lock-types-header.patch
Patch339:        0139-rtmutex-Avoid-include-hell.patch
Patch340:        0140-rbtree-don-t-include-the-rcu-header.patch
Patch341:        0141-rtmutex-Provide-rt_mutex_slowlock_locked.patch
Patch342:        0142-rtmutex-export-lockdep-less-version-of-rt_mutex-s-lo.patch
Patch343:        0143-rtmutex-add-sleeping-lock-implementation.patch
Patch344:        0144-rtmutex-add-mutex-implementation-based-on-rtmutex.patch
Patch345:        0145-rtmutex-add-rwsem-implementation-based-on-rtmutex.patch
Patch346:        0146-rtmutex-add-rwlock-implementation-based-on-rtmutex.patch
Patch347:        0147-rtmutex-rwlock-preserve-state-like-a-sleeping-lock.patch
Patch348:        0148-rtmutex-wire-up-RT-s-locking.patch
Patch349:        0149-rtmutex-add-ww_mutex-addon-for-mutex-rt.patch
Patch350:        0150-kconfig-Add-PREEMPT_RT_FULL.patch
Patch351:        0151-locking-rt-mutex-fix-deadlock-in-device-mapper-block.patch
Patch352:        0152-locking-rt-mutex-Flush-block-plug-on-__down_read.patch
Patch353:        0153-locking-rtmutex-re-init-the-wait_lock-in-rt_mutex_in.patch
Patch354:        0154-ptrace-fix-ptrace-vs-tasklist_lock-race.patch
Patch355:        0155-rtmutex-annotate-sleeping-lock-context.patch
Patch356:        0156-sched-migrate_disable-fallback-to-preempt_disable-in.patch
Patch357:        0157-locking-don-t-check-for-__LINUX_SPINLOCK_TYPES_H-on-.patch
Patch358:        0158-rcu-Frob-softirq-test.patch
Patch359:        0159-rcu-Merge-RCU-bh-into-RCU-preempt.patch
Patch360:        0160-rcu-Make-ksoftirqd-do-RCU-quiescent-states.patch
Patch361:        0161-rcu-Eliminate-softirq-processing-from-rcutree.patch
Patch362:        0162-srcu-use-cpu_online-instead-custom-check.patch
Patch363:        0163-srcu-replace-local_irqsave-with-a-locallock.patch
Patch364:        0164-rcu-enable-rcu_normal_after_boot-by-default-for-RT.patch
Patch365:        0165-tty-serial-omap-Make-the-locking-RT-aware.patch
Patch366:        0166-tty-serial-pl011-Make-the-locking-work-on-RT.patch
Patch367:        0167-tty-serial-pl011-explicitly-initialize-the-flags-var.patch
Patch368:        0168-rt-Improve-the-serial-console-PASS_LIMIT.patch
Patch369:        0169-tty-serial-8250-don-t-take-the-trylock-during-oops.patch
Patch370:        0170-locking-percpu-rwsem-Remove-preempt_disable-variants.patch
Patch371:        0171-mm-Protect-activate_mm-by-preempt_-disable-enable-_r.patch
Patch372:        0172-fs-dcache-bring-back-explicit-INIT_HLIST_BL_HEAD-ini.patch
Patch373:        0173-fs-dcache-disable-preemption-on-i_dir_seq-s-write-si.patch
Patch374:        0174-squashfs-make-use-of-local-lock-in-multi_cpu-decompr.patch
Patch375:        0175-thermal-Defer-thermal-wakups-to-threads.patch
Patch376:        0176-x86-fpu-Disable-preemption-around-local_bh_disable.patch
Patch377:        0177-fs-epoll-Do-not-disable-preemption-on-RT.patch
Patch378:        0178-mm-vmalloc-Another-preempt-disable-region-which-suck.patch
Patch379:        0179-block-mq-use-cpu_light.patch
Patch380:        0180-block-mq-do-not-invoke-preempt_disable.patch
Patch381:        0181-block-mq-don-t-complete-requests-via-IPI.patch
Patch382:        0182-md-raid5-Make-raid5_percpu-handling-RT-aware.patch
Patch383:        0183-rt-Introduce-cpu_chill.patch
Patch384:        0184-hrtimer-Don-t-lose-state-in-cpu_chill.patch
Patch385:        0185-hrtimer-cpu_chill-save-task-state-in-saved_state.patch
Patch386:        0186-block-blk-mq-move-blk_queue_usage_counter_release-in.patch
Patch387:        0187-block-Use-cpu_chill-for-retry-loops.patch
Patch388:        0188-fs-dcache-Use-cpu_chill-in-trylock-loops.patch
Patch389:        0189-net-Use-cpu_chill-instead-of-cpu_relax.patch
Patch390:        0190-fs-dcache-use-swait_queue-instead-of-waitqueue.patch
Patch391:        0191-workqueue-Use-normal-rcu.patch
Patch392:        0192-workqueue-Use-local-irq-lock-instead-of-irq-disable-.patch
Patch393:        0193-workqueue-Prevent-workqueue-versus-ata-piix-livelock.patch
Patch394:        0194-sched-Distangle-worker-accounting-from-rqlock.patch
Patch395:        0195-debugobjects-Make-RT-aware.patch
Patch396:        0196-seqlock-Prevent-rt-starvation.patch
Patch397:        0197-sunrpc-Make-svc_xprt_do_enqueue-use-get_cpu_light.patch
Patch398:        0198-net-Use-skbufhead-with-raw-lock.patch
Patch399:        0199-net-move-xmit_recursion-to-per-task-variable-on-RT.patch
Patch400:        0200-net-provide-a-way-to-delegate-processing-a-softirq-t.patch
Patch401:        0201-net-dev-always-take-qdisc-s-busylock-in-__dev_xmit_s.patch
Patch402:        0202-net-Qdisc-use-a-seqlock-instead-seqcount.patch
Patch403:        0203-net-add-back-the-missing-serialization-in-ip_send_un.patch
Patch404:        0204-net-add-a-lock-around-icmp_sk.patch
Patch405:        0205-net-Have-__napi_schedule_irqoff-disable-interrupts-o.patch
Patch406:        0206-irqwork-push-most-work-into-softirq-context.patch
Patch407:        0207-printk-Make-rt-aware.patch
Patch408:        0208-kernel-printk-Don-t-try-to-print-from-IRQ-NMI-region.patch
Patch409:        0209-printk-Drop-the-logbuf_lock-more-often.patch
Patch410:        0210-ARM-enable-irq-in-translation-section-permission-fau.patch
Patch411:        0211-genirq-update-irq_set_irqchip_state-documentation.patch
Patch412:        0212-KVM-arm-arm64-downgrade-preempt_disable-d-region-to-.patch
Patch413:        0213-arm64-fpsimd-use-preemp_disable-in-addition-to-local.patch
Patch414:        0214-kgdb-serial-Short-term-workaround.patch
Patch415:        0215-sysfs-Add-sys-kernel-realtime-entry.patch
Patch416:        0216-mm-rt-kmap_atomic-scheduling.patch
Patch417:        0217-x86-highmem-Add-a-already-used-pte-check.patch
Patch418:        0218-arm-highmem-Flush-tlb-on-unmap.patch
Patch419:        0219-arm-Enable-highmem-for-rt.patch
Patch420:        0220-scsi-fcoe-Make-RT-aware.patch
Patch421:        0221-x86-crypto-Reduce-preempt-disabled-regions.patch
Patch422:        0222-crypto-Reduce-preempt-disabled-regions-more-algos.patch
Patch423:        0223-crypto-limit-more-FPU-enabled-sections.patch
Patch424:        0224-crypto-scompress-serialize-RT-percpu-scratch-buffer-.patch
Patch425:        0225-crypto-cryptd-add-a-lock-instead-preempt_disable-loc.patch
Patch426:        0226-panic-skip-get_random_bytes-for-RT_FULL-in-init_oops.patch
Patch427:        0227-x86-stackprotector-Avoid-random-pool-on-rt.patch
Patch428:        0228-random-Make-it-work-on-rt.patch
Patch429:        0229-cpu-hotplug-Implement-CPU-pinning.patch
Patch430:        0230-sched-Allow-pinned-user-tasks-to-be-awakened-to-the-.patch
Patch431:        0231-hotplug-duct-tape-RT-rwlock-usage-for-non-RT.patch
Patch432:        0232-net-Remove-preemption-disabling-in-netif_rx.patch
Patch433:        0233-net-Another-local_irq_disable-kmalloc-headache.patch
Patch434:        0234-net-core-protect-users-of-napi_alloc_cache-against-r.patch
Patch435:        0235-net-netfilter-Serialize-xt_write_recseq-sections-on-.patch
Patch436:        0236-net-Add-a-mutex-around-devnet_rename_seq.patch
Patch437:        0237-lockdep-selftest-Only-do-hardirq-context-test-for-ra.patch
Patch438:        0238-lockdep-selftest-fix-warnings-due-to-missing-PREEMPT.patch
Patch439:        0239-sched-Add-support-for-lazy-preemption.patch
Patch440:        0240-ftrace-Fix-trace-header-alignment.patch
Patch441:        0241-x86-Support-for-lazy-preemption.patch
Patch442:        0242-x86-lazy-preempt-properly-check-against-preempt-mask.patch
Patch443:        0243-x86-lazy-preempt-use-proper-return-label-on-32bit-x8.patch
Patch444:        0244-arm-Add-support-for-lazy-preemption.patch
Patch445:        0245-powerpc-Add-support-for-lazy-preemption.patch
Patch446:        0246-arch-arm64-Add-lazy-preempt-support.patch
Patch447:        0247-connector-cn_proc-Protect-send_msg-with-a-local-lock.patch
Patch448:        0248-drivers-block-zram-Replace-bit-spinlocks-with-rtmute.patch
Patch449:        0249-drivers-zram-Don-t-disable-preemption-in-zcomp_strea.patch
Patch450:        0250-drivers-zram-fix-zcomp_stream_get-smp_processor_id-u.patch
Patch451:        0251-tpm_tis-fix-stall-after-iowrite-s.patch
Patch452:        0252-watchdog-prevent-deferral-of-watchdogd-wakeup-on-RT.patch
Patch453:        0253-drm-radeon-i915-Use-preempt_disable-enable_rt-where-.patch
Patch454:        0254-drm-i915-Use-local_lock-unlock_irq-in-intel_pipe_upd.patch
Patch455:        0255-drm-i915-disable-tracing-on-RT.patch
Patch456:        0256-drm-i915-skip-DRM_I915_LOW_LEVEL_TRACEPOINTS-with-NO.patch
Patch457:        0257-cgroups-use-simple-wait-in-css_release.patch
Patch458:        0258-cpuset-Convert-callback_lock-to-raw_spinlock_t.patch
Patch459:        0259-apparmor-use-a-locallock-instead-preempt_disable.patch
Patch460:        0260-workqueue-Prevent-deadlock-stall-on-RT.patch
Patch461:        0261-signals-Allow-rt-tasks-to-cache-one-sigqueue-struct.patch
Patch462:        0262-Add-localversion-for-RT-release.patch
Patch463:        0263-powerpc-pseries-iommu-Use-a-locallock-instead-local_.patch
Patch464:        0264-powerpc-reshuffle-TIF-bits.patch
Patch465:        0265-tty-sysrq-Convert-show_lock-to-raw_spinlock_t.patch
Patch466:        0266-drm-i915-Don-t-disable-interrupts-independently-of-t.patch
Patch467:        0267-sched-completion-Fix-a-lockup-in-wait_for_completion.patch
Patch468:        0268-kthread-add-a-global-worker-thread.patch
Patch469:        0269-genirq-Do-not-invoke-the-affinity-callback-via-a-wor.patch
Patch470:        0270-genirq-Handle-missing-work_struct-in-irq_set_affinit.patch
Patch471:        0271-arm-imx6-cpuidle-Use-raw_spinlock_t.patch
Patch472:        0272-rcu-Don-t-allow-to-change-rcu_normal_after_boot-on-R.patch
Patch473:        0273-pci-switchtec-fix-stream_open.cocci-warnings.patch
Patch474:        0274-sched-core-Drop-a-preempt_disable_rt-statement.patch
Patch475:        0275-timers-Redo-the-notification-of-canceling-timers-on-.patch
Patch476:        0276-Revert-futex-Ensure-lock-unlock-symetry-versus-pi_lo.patch
Patch477:        0277-Revert-futex-Fix-bug-on-when-a-requeued-RT-task-time.patch
Patch478:        0278-Revert-rtmutex-Handle-the-various-new-futex-race-con.patch
Patch479:        0279-Revert-futex-workaround-migrate_disable-enable-in-di.patch
Patch480:        0280-futex-Make-the-futex_hash_bucket-lock-raw.patch
Patch481:        0281-futex-Delay-deallocation-of-pi_state.patch
Patch482:        0282-mm-zswap-Do-not-disable-preemption-in-zswap_frontswa.patch
Patch483:        0283-revert-aio.patch
Patch484:        0284-fs-aio-simple-simple-work.patch
Patch485:        0285-revert-thermal.patch
Patch486:        0286-thermal-Defer-thermal-wakups-to-threads.patch
Patch487:        0287-revert-block.patch
Patch488:        0288-block-blk-mq-move-blk_queue_usage_counter_release-in.patch
Patch489:        0289-workqueue-rework.patch
# Keep rt_version matched up with this patch.
Patch490:        0290-Linux-4.19.82-rt30-REBASE.patch

%if 0%{?kat_build:1}
Patch1000:	%{kat_build}.patch
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
Requires(post):(coreutils or toybox)
Requires(postun):(coreutils or toybox)

%define uname_r %{version}-%{rt_version}-%{release}-rt

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
%endif
%patch0 -p1
%patch1 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch11 -p1
%patch24 -p1
%patch26 -p1
%patch29 -p1
%patch30 -p1
%patch31 -p1
%patch32 -p1
%patch33 -p1
%patch34 -p1
%patch35 -p1
%patch36 -p1
%patch38 -p1
%patch39 -p1

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
%patch214 -p1
%patch215 -p1
%patch216 -p1
%patch217 -p1
%patch218 -p1
%patch219 -p1
%patch220 -p1
%patch221 -p1
%patch222 -p1
%patch223 -p1
%patch224 -p1
%patch225 -p1
%patch226 -p1
%patch227 -p1
%patch228 -p1
%patch229 -p1
%patch230 -p1
%patch231 -p1
%patch232 -p1
%patch233 -p1
%patch234 -p1
%patch235 -p1
%patch236 -p1
%patch237 -p1
%patch238 -p1
%patch239 -p1
%patch240 -p1
%patch241 -p1
%patch242 -p1
%patch243 -p1
%patch244 -p1
%patch245 -p1
%patch246 -p1
%patch247 -p1
%patch248 -p1
%patch249 -p1
%patch250 -p1
%patch251 -p1
%patch252 -p1
%patch253 -p1
%patch254 -p1
%patch255 -p1
%patch256 -p1
%patch257 -p1
%patch258 -p1
%patch259 -p1
%patch260 -p1
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
%patch271 -p1
%patch272 -p1
%patch273 -p1
%patch274 -p1
%patch275 -p1
%patch276 -p1
%patch277 -p1
%patch278 -p1
%patch279 -p1
%patch280 -p1
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
%patch294 -p1
%patch295 -p1
%patch296 -p1
%patch297 -p1
%patch298 -p1
%patch299 -p1
%patch300 -p1
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

install -vdm 755 %{buildroot}/etc
install -vdm 755 %{buildroot}/boot
install -vdm 755 %{buildroot}%{_defaultdocdir}/%{name}-%{uname_r}
install -vdm 755 %{buildroot}/usr/src/%{name}-headers-%{uname_r}
install -vdm 755 %{buildroot}/usr/lib/debug/lib/modules/%{uname_r}
make INSTALL_MOD_PATH=%{buildroot} modules_install

%ifarch x86_64

# install XR module
bldroot=`pwd`
pushd ../xr_usb_serial_common_lnx-3.6-and-newer-pak
make KERNELDIR=$bldroot INSTALL_MOD_PATH=%{buildroot} modules_install
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
cp -r Documentation/*        %{buildroot}%{_defaultdocdir}/%{name}-%{uname_r}
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

find . -name Makefile* -o -name Kconfig* -o -name *.pl | xargs  sh -c 'cp --parents "$@" %{buildroot}/usr/src/%{name}-headers-%{uname_r}' copy
find arch/${archdir}/include include scripts -type f | xargs  sh -c 'cp --parents "$@" %{buildroot}/usr/src/%{name}-headers-%{uname_r}' copy
find $(find arch/${archdir} -name include -o -name scripts -type d) -type f | xargs  sh -c 'cp --parents "$@" %{buildroot}/usr/src/%{name}-headers-%{uname_r}' copy
find arch/${archdir}/include Module.symvers include scripts -type f | xargs  sh -c 'cp --parents "$@" %{buildroot}/usr/src/%{name}-headers-%{uname_r}' copy
%ifarch x86_64
# CONFIG_STACK_VALIDATION=y requires objtool to build external modules
install -vsm 755 tools/objtool/objtool %{buildroot}/usr/src/%{name}-headers-%{uname_r}/tools/objtool/
install -vsm 755 tools/objtool/fixdep %{buildroot}/usr/src/%{name}-headers-%{uname_r}/tools/objtool/
%endif

cp .config %{buildroot}/usr/src/%{name}-headers-%{uname_r} # copy .config manually to be where it's expected to be
ln -sf "/usr/src/%{name}-headers-%{uname_r}" "%{buildroot}/lib/modules/%{uname_r}/build"
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

%files devel
%defattr(-,root,root)
/lib/modules/%{uname_r}/build
/usr/src/%{name}-headers-%{uname_r}

%changelog
*   Wed Dec 12 2019 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.82-2
-   Fix patch that wont apply on 4.19.82. Revert when upgraded to 4.19.87 or more
*   Tue Nov 12 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.82-1
-   Introduce a new kernel flavor 'linux-rt' supporting real-time (RT) features.
