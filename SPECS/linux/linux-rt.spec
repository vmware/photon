%global security_hardening none
Summary:        Kernel
Name:           linux-rt
Version:        4.14.54
Release:        1%{?dist}
License:        GPLv2
URL:            http://www.kernel.org/
Group:          System Environment/Kernel
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://www.kernel.org/pub/linux/kernel/v4.x/linux-%{version}.tar.xz
%define sha1 linux=434080e874f7b78c3234f22784427d4a189fb54d
Source1:        config-rt
Source2:        initramfs.trigger
%define ena_version 1.5.0
Source3:       https://github.com/amzn/amzn-drivers/archive/ena_linux_%{ena_version}.tar.gz
%define sha1 ena_linux=cbbbe8a3bbab6d01a4e38417cb0ead2f7cb8b2ee
Source4:	config_aarch64
# -rt
Patch0000:	  ./rt/0001-rtmutex-Make-rt_mutex_futex_unlock-safe-for-irq-off-.patch
Patch0001:	  ./rt/0002-rcu-Suppress-lockdep-false-positive-boost_mtx-compla.patch
Patch0002:	  ./rt/0003-brd-remove-unused-brd_mutex.patch
Patch0003:	  ./rt/0004-KVM-arm-arm64-Remove-redundant-preemptible-checks.patch
Patch0004:	  ./rt/0005-iommu-amd-Use-raw-locks-on-atomic-context-paths.patch
Patch0005:	  ./rt/0006-iommu-amd-Don-t-use-dev_data-in-irte_ga_set_affinity.patch
Patch0006:	  ./rt/0007-iommu-amd-Avoid-locking-get_irq_table-from-atomic-co.patch
Patch0007:	  ./rt/0008-iommu-amd-Turn-dev_data_list-into-a-lock-less-list.patch
Patch0008:	  ./rt/0009-iommu-amd-Split-domain-id-out-of-amd_iommu_devtable_.patch
Patch0009:	  ./rt/0010-iommu-amd-Split-irq_lookup_table-out-of-the-amd_iomm.patch
Patch0010:	  ./rt/0011-iommu-amd-Remove-the-special-case-from-alloc_irq_tab.patch
Patch0011:	  ./rt/0012-iommu-amd-Use-table-instead-irt-as-variable-name-in-.patch
Patch0012:	  ./rt/0013-iommu-amd-Factor-out-setting-the-remap-table-for-a-d.patch
Patch0013:	  ./rt/0014-iommu-amd-Drop-the-lock-while-allocating-new-irq-rem.patch
Patch0014:	  ./rt/0015-iommu-amd-Make-amd_iommu_devtable_lock-a-spin_lock.patch
Patch0015:	  ./rt/0016-iommu-amd-Return-proper-error-code-in-irq_remapping_.patch
Patch0016:	  ./rt/0017-timers-Use-static-keys-for-migrate_enable-nohz_activ.patch
Patch0017:	  ./rt/0018-hrtimer-Correct-blantanly-wrong-comment.patch
Patch0018:	  ./rt/0019-hrtimer-Fix-kerneldoc-for-struct-hrtimer_cpu_base.patch
Patch0019:	  ./rt/0020-hrtimer-Cleanup-clock-argument-in-schedule_hrtimeout.patch
Patch0020:	  ./rt/0021-hrtimer-Fix-hrtimer-function-description.patch
Patch0021:	  ./rt/0022-hrtimer-Cleanup-hrtimer_mode-enum.patch
Patch0022:	  ./rt/0023-tracing-hrtimer-Print-hrtimer-mode-in-hrtimer_start-.patch
Patch0023:	  ./rt/0024-hrtimer-Switch-for-loop-to-_ffs-evaluation.patch
Patch0024:	  ./rt/0025-hrtimer-Store-running-timer-in-hrtimer_clock_base.patch
Patch0025:	  ./rt/0026-hrtimer-Make-room-in-struct-hrtimer_cpu_base.patch
Patch0026:	  ./rt/0027-hrtimer-Reduce-conditional-code-hres_active.patch
Patch0027:	  ./rt/0028-hrtimer-Use-accesor-functions-instead-of-direct-acce.patch
Patch0028:	  ./rt/0029-hrtimer-Make-the-remote-enqueue-check-unconditional.patch
Patch0029:	  ./rt/0030-hrtimer-Make-hrtimer_cpu_base.next_timer-handling-un.patch
Patch0030:	  ./rt/0031-hrtimer-Make-hrtimer_reprogramm-unconditional.patch
Patch0031:	  ./rt/0032-hrtimer-Make-hrtimer_force_reprogramm-unconditionall.patch
Patch0032:	  ./rt/0033-hrtimer-Unify-handling-of-hrtimer-remove.patch
Patch0033:	  ./rt/0034-hrtimer-Unify-handling-of-remote-enqueue.patch
Patch0034:	  ./rt/0035-hrtimer-Make-remote-enqueue-decision-less-restrictiv.patch
Patch0035:	  ./rt/0036-hrtimer-Remove-base-argument-from-hrtimer_reprogram.patch
Patch0036:	  ./rt/0037-hrtimer-Split-hrtimer_start_range_ns.patch
Patch0037:	  ./rt/0038-hrtimer-Split-__hrtimer_get_next_event.patch
Patch0038:	  ./rt/0039-hrtimer-Use-irqsave-irqrestore-around-__run_hrtimer.patch
Patch0039:	  ./rt/0040-hrtimer-Add-clock-bases-and-hrtimer-mode-for-soft-ir.patch
Patch0040:	  ./rt/0041-hrtimer-Prepare-handling-of-hard-and-softirq-based-h.patch
Patch0041:	  ./rt/0042-hrtimer-Implement-support-for-softirq-based-hrtimers.patch
Patch0042:	  ./rt/0043-hrtimer-Implement-SOFT-HARD-clock-base-selection.patch
Patch0043:	  ./rt/0044-can-bcm-Replace-hrtimer_tasklet-with-softirq-based-h.patch
Patch0044:	  ./rt/0045-mac80211_hwsim-Replace-hrtimer-tasklet-with-softirq-.patch
Patch0045:	  ./rt/0046-xfrm-Replace-hrtimer-tasklet-with-softirq-hrtimer.patch
Patch0046:	  ./rt/0047-softirq-Remove-tasklet_hrtimer.patch
Patch0047:	  ./rt/0048-ALSA-dummy-Replace-tasklet-with-softirq-hrtimer.patch
Patch0048:	  ./rt/0049-usb-gadget-NCM-Replace-tasklet-with-softirq-hrtimer.patch
Patch0049:	  ./rt/0050-net-mvpp2-Replace-tasklet-with-softirq-hrtimer.patch
Patch0050:	  ./rt/0051-arm-at91-do-not-disable-enable-clocks-in-a-row.patch
Patch0051:	  ./rt/0052-ARM-smp-Move-clear_tasks_mm_cpumask-call-to-__cpu_di.patch
Patch0052:	  ./rt/0053-rtmutex-Handle-non-enqueued-waiters-gracefully.patch
Patch0053:	  ./rt/0054-rbtree-include-rcu.h-because-we-use-it.patch
Patch0054:	  ./rt/0055-rxrpc-remove-unused-static-variables.patch
Patch0055:	  ./rt/0056-mfd-syscon-atmel-smc-include-string.h.patch
Patch0056:	  ./rt/0057-sched-swait-include-wait.h.patch
Patch0057:	  ./rt/0058-NFSv4-replace-seqcount_t-with-a-seqlock_t.patch
Patch0058:	  ./rt/0059-Bluetooth-avoid-recursive-locking-in-hci_send_to_cha.patch
Patch0059:	  ./rt/0060-iommu-iova-Use-raw_cpu_ptr-instead-of-get_cpu_ptr-fo.patch
Patch0060:	  ./rt/0061-greybus-audio-don-t-inclide-rwlock.h-directly.patch
Patch0061:	  ./rt/0062-xen-9pfs-don-t-inclide-rwlock.h-directly.patch
Patch0062:	  ./rt/0063-drm-i915-properly-init-lockdep-class.patch
Patch0063:	  ./rt/0064-timerqueue-Document-return-values-of-timerqueue_add-.patch
Patch0064:	  ./rt/0065-sparc64-use-generic-rwsem-spinlocks-rt.patch
Patch0065:	  ./rt/0066-kernel-SRCU-provide-a-static-initializer.patch
Patch0066:	  ./rt/0067-target-drop-spin_lock_assert-irqs_disabled-combo-che.patch
Patch0067:	  ./rt/0068-kernel-sched-Provide-a-pointer-to-the-valid-CPU-mask.patch
Patch0068:	  ./rt/0069-kernel-sched-core-add-migrate_disable.patch
Patch0069:	  ./rt/0070-tracing-Reverse-the-order-of-trace_types_lock-and-ev.patch
Patch0070:	  ./rt/0071-ring-buffer-Rewrite-trace_recursive_-un-lock-to-be-s.patch
Patch0071:	  ./rt/0072-tracing-Remove-lookups-from-tracing_map-hitcount.patch
Patch0072:	  ./rt/0073-tracing-Increase-tracing-map-KEYS_MAX-size.patch
Patch0073:	  ./rt/0074-tracing-Make-traceprobe-parsing-code-reusable.patch
Patch0074:	  ./rt/0075-tracing-Clean-up-hist_field_flags-enum.patch
Patch0075:	  ./rt/0076-tracing-Add-hist_field_name-accessor.patch
Patch0076:	  ./rt/0077-tracing-Reimplement-log2.patch
Patch0077:	  ./rt/0078-tracing-Move-hist-trigger-Documentation-to-histogram.patch
Patch0078:	  ./rt/0079-tracing-Add-Documentation-for-log2-modifier.patch
Patch0079:	  ./rt/0080-tracing-Add-support-to-detect-and-avoid-duplicates.patch
Patch0080:	  ./rt/0081-tracing-Remove-code-which-merges-duplicates.patch
Patch0081:	  ./rt/0082-ring-buffer-Add-interface-for-setting-absolute-time-.patch
Patch0082:	  ./rt/0083-ring-buffer-Redefine-the-unimplemented-RINGBUF_TYPE_.patch
Patch0083:	  ./rt/0084-tracing-Add-timestamp_mode-trace-file.patch
Patch0084:	  ./rt/0085-tracing-Give-event-triggers-access-to-ring_buffer_ev.patch
Patch0085:	  ./rt/0086-tracing-Add-ring-buffer-event-param-to-hist-field-fu.patch
Patch0086:	  ./rt/0087-tracing-Break-out-hist-trigger-assignment-parsing.patch
Patch0087:	  ./rt/0088-tracing-Add-hist-trigger-timestamp-support.patch
Patch0088:	  ./rt/0089-tracing-Add-per-element-variable-support-to-tracing_.patch
Patch0089:	  ./rt/0090-tracing-Add-hist_data-member-to-hist_field.patch
Patch0090:	  ./rt/0091-tracing-Add-usecs-modifier-for-hist-trigger-timestam.patch
Patch0091:	  ./rt/0092-tracing-Add-variable-support-to-hist-triggers.patch
Patch0092:	  ./rt/0093-tracing-Account-for-variables-in-named-trigger-compa.patch
Patch0093:	  ./rt/0094-tracing-Move-get_hist_field_flags.patch
Patch0094:	  ./rt/0095-tracing-Add-simple-expression-support-to-hist-trigge.patch
Patch0095:	  ./rt/0096-tracing-Generalize-per-element-hist-trigger-data.patch
Patch0096:	  ./rt/0097-tracing-Pass-tracing_map_elt-to-hist_field-accessor-.patch
Patch0097:	  ./rt/0098-tracing-Add-hist_field-type-field.patch
Patch0098:	  ./rt/0099-tracing-Add-variable-reference-handling-to-hist-trig.patch
Patch0099:	  ./rt/0100-tracing-Add-hist-trigger-action-hook.patch
Patch0100:	  ./rt/0101-tracing-Add-support-for-synthetic-events.patch
Patch0101:	  ./rt/0102-tracing-Add-support-for-field-variables.patch
Patch0102:	  ./rt/0103-tracing-Add-onmatch-hist-trigger-action-support.patch
Patch0103:	  ./rt/0104-tracing-Add-onmax-hist-trigger-action-support.patch
Patch0104:	  ./rt/0105-tracing-Allow-whitespace-to-surround-hist-trigger-fi.patch
Patch0105:	  ./rt/0106-tracing-Add-cpu-field-for-hist-triggers.patch
Patch0106:	  ./rt/0107-tracing-Add-hist-trigger-support-for-variable-refere.patch
Patch0107:	  ./rt/0108-tracing-Add-last-error-error-facility-for-hist-trigg.patch
Patch0108:	  ./rt/0109-tracing-Add-inter-event-hist-trigger-Documentation.patch
Patch0109:	  ./rt/0110-tracing-Make-tracing_set_clock-non-static.patch
Patch0110:	  ./rt/0111-tracing-Add-a-clock-attribute-for-hist-triggers.patch
Patch0111:	  ./rt/0112-ring-buffer-Bring-back-context-level-recursive-check.patch
Patch0112:	  ./rt/0113-ring-buffer-Fix-duplicate-results-in-mapping-context.patch
Patch0113:	  ./rt/0114-ring-buffer-Add-nesting-for-adding-events-within-eve.patch
Patch0114:	  ./rt/0115-tracing-Use-the-ring-buffer-nesting-to-allow-synthet.patch
Patch0115:	  ./rt/0116-tracing-Add-inter-event-blurb-to-HIST_TRIGGERS-confi.patch
Patch0116:	  ./rt/0117-selftests-ftrace-Add-inter-event-hist-triggers-testc.patch
Patch0117:	  ./rt/0118-tracing-Fix-display-of-hist-trigger-expressions-cont.patch
Patch0118:	  ./rt/0119-tracing-Don-t-add-flag-strings-when-displaying-varia.patch
Patch0119:	  ./rt/0120-tracing-Add-action-comparisons-when-testing-matching.patch
Patch0120:	  ./rt/0121-tracing-Make-sure-variable-string-fields-are-NULL-te.patch
Patch0121:	  ./rt/0122-block-Shorten-interrupt-disabled-regions.patch
Patch0122:	  ./rt/0123-timekeeping-Split-jiffies-seqlock.patch
Patch0123:	  ./rt/0124-tracing-Account-for-preempt-off-in-preempt_schedule.patch
Patch0124:	  ./rt/0125-signal-Revert-ptrace-preempt-magic.patch
Patch0125:	  ./rt/0126-arm-Convert-arm-boot_lock-to-raw.patch
Patch0126:	  ./rt/0127-arm-kprobe-replace-patch_lock-to-raw-lock.patch
Patch0127:	  ./rt/0128-posix-timers-Prevent-broadcast-signals.patch
Patch0128:	  ./rt/0129-signals-Allow-rt-tasks-to-cache-one-sigqueue-struct.patch
Patch0129:	  ./rt/0130-drivers-random-Reduce-preempt-disabled-region.patch
Patch0130:	  ./rt/0131-ARM-AT91-PIT-Remove-irq-handler-when-clock-event-is-.patch
Patch0131:	  ./rt/0132-clockevents-drivers-timer-atmel-pit-fix-double-free_.patch
Patch0132:	  ./rt/0133-clocksource-TCLIB-Allow-higher-clock-rates-for-clock.patch
Patch0133:	  ./rt/0134-suspend-Prevent-might-sleep-splats.patch
Patch0134:	  ./rt/0135-net-flip-lock-dep-thingy.patch.patch
Patch0135:	  ./rt/0136-net-sched-Use-msleep-instead-of-yield.patch
Patch0136:	  ./rt/0137-net-core-disable-NET_RX_BUSY_POLL.patch
Patch0137:	  ./rt/0138-x86-ioapic-Do-not-unmask-io_apic-when-interrupt-is-i.patch
Patch0138:	  ./rt/0139-rcu-segcblist-include-rcupdate.h.patch
Patch0139:	  ./rt/0140-printk-Add-a-printk-kill-switch.patch
Patch0140:	  ./rt/0141-printk-Add-force_early_printk-boot-param-to-help-wit.patch
Patch0141:	  ./rt/0142-rt-Provide-PREEMPT_RT_BASE-config-switch.patch
Patch0142:	  ./rt/0143-kconfig-Disable-config-options-which-are-not-RT-comp.patch
Patch0143:	  ./rt/0144-kconfig-Add-PREEMPT_RT_FULL.patch
Patch0144:	  ./rt/0145-bug-BUG_ON-WARN_ON-variants-dependend-on-RT-RT.patch
Patch0145:	  ./rt/0146-iommu-amd-Use-WARN_ON_NORT-in-__attach_device.patch
Patch0146:	  ./rt/0147-rt-local_irq_-variants-depending-on-RT-RT.patch
Patch0147:	  ./rt/0148-preempt-Provide-preempt_-_-no-rt-variants.patch
Patch0148:	  ./rt/0149-futex-workaround-migrate_disable-enable-in-different.patch
Patch0149:	  ./rt/0150-rt-Add-local-irq-locks.patch
Patch0150:	  ./rt/0151-ata-Do-not-disable-interrupts-in-ide-code-for-preemp.patch
Patch0151:	  ./rt/0152-ide-Do-not-disable-interrupts-for-PREEMPT-RT.patch
Patch0152:	  ./rt/0153-infiniband-Mellanox-IB-driver-patch-use-_nort-primit.patch
Patch0153:	  ./rt/0154-input-gameport-Do-not-disable-interrupts-on-PREEMPT_.patch
Patch0154:	  ./rt/0155-core-Do-not-disable-interrupts-on-RT-in-kernel-users.patch
Patch0155:	  ./rt/0156-usb-Use-_nort-in-giveback-function.patch
Patch0156:	  ./rt/0157-mm-scatterlist-Do-not-disable-irqs-on-RT.patch
Patch0157:	  ./rt/0158-mm-workingset-Do-not-protect-workingset_shadow_nodes.patch
Patch0158:	  ./rt/0159-signal-Make-__lock_task_sighand-RT-aware.patch
Patch0159:	  ./rt/0160-signal-x86-Delay-calling-signals-in-atomic.patch
Patch0160:	  ./rt/0161-x86-signal-delay-calling-signals-on-32bit.patch
Patch0161:	  ./rt/0162-net-wireless-Use-WARN_ON_NORT.patch
Patch0162:	  ./rt/0163-buffer_head-Replace-bh_uptodate_lock-for-rt.patch
Patch0163:	  ./rt/0164-fs-jbd-jbd2-Make-state-lock-and-journal-head-lock-rt.patch
Patch0164:	  ./rt/0165-list_bl-Make-list-head-locking-RT-safe.patch
Patch0165:	  ./rt/0166-list_bl-fixup-bogus-lockdep-warning.patch
Patch0166:	  ./rt/0167-genirq-Disable-irqpoll-on-rt.patch
Patch0167:	  ./rt/0168-genirq-Force-interrupt-thread-on-RT.patch
Patch0168:	  ./rt/0169-drivers-net-vortex-fix-locking-issues.patch
Patch0169:	  ./rt/0170-delayacct-use-raw_spinlocks.patch
Patch0170:	  ./rt/0171-mm-page_alloc-rt-friendly-per-cpu-pages.patch
Patch0171:	  ./rt/0172-mm-page_alloc-Reduce-lock-sections-further.patch
Patch0172:	  ./rt/0173-mm-swap-Convert-to-percpu-locked.patch
Patch0173:	  ./rt/0174-mm-perform-lru_add_drain_all-remotely.patch
Patch0174:	  ./rt/0175-mm-vmstat-Protect-per-cpu-variables-with-preempt-dis.patch
Patch0175:	  ./rt/0176-ARM-Initialize-split-page-table-locks-for-vector-pag.patch
Patch0176:	  ./rt/0177-mm-bounce-Use-local_irq_save_nort.patch
Patch0177:	  ./rt/0178-mm-Allow-only-slub-on-RT.patch
Patch0178:	  ./rt/0179-mm-Enable-SLUB-for-RT.patch
Patch0179:	  ./rt/0180-mm-slub-close-possible-memory-leak-in-kmem_cache_all.patch
Patch0180:	  ./rt/0181-slub-Enable-irqs-for-__GFP_WAIT.patch
Patch0181:	  ./rt/0182-slub-Disable-SLUB_CPU_PARTIAL.patch
Patch0182:	  ./rt/0183-mm-page_alloc-Use-local_lock_on-instead-of-plain-spi.patch
Patch0183:	  ./rt/0184-mm-memcontrol-Don-t-call-schedule_work_on-in-preempt.patch
Patch0184:	  ./rt/0185-mm-memcontrol-Replace-local_irq_disable-with-local-l.patch
Patch0185:	  ./rt/0186-mm-backing-dev-don-t-disable-IRQs-in-wb_congested_pu.patch
Patch0186:	  ./rt/0187-mm-zsmalloc-copy-with-get_cpu_var-and-locking.patch
Patch0187:	  ./rt/0188-radix-tree-use-local-locks.patch
Patch0188:	  ./rt/0189-panic-skip-get_random_bytes-for-RT_FULL-in-init_oops.patch
Patch0189:	  ./rt/0190-timers-Prepare-for-full-preemption.patch
Patch0190:	  ./rt/0191-timer-delay-waking-softirqs-from-the-jiffy-tick.patch
Patch0191:	  ./rt/0192-nohz-Prevent-erroneous-tick-stop-invocations.patch
Patch0192:	  ./rt/0193-x86-kvm-Require-const-tsc-for-RT.patch
Patch0193:	  ./rt/0194-wait.h-include-atomic.h.patch
Patch0194:	  ./rt/0195-work-simple-Simple-work-queue-implemenation.patch
Patch0195:	  ./rt/0196-completion-Use-simple-wait-queues.patch
Patch0196:	  ./rt/0197-fs-aio-simple-simple-work.patch
Patch0197:	  ./rt/0198-genirq-Do-not-invoke-the-affinity-callback-via-a-wor.patch
Patch0198:	  ./rt/0199-time-hrtimer-avoid-schedule_work-with-interrupts-dis.patch
Patch0199:	  ./rt/0200-hrtimer-consolidate-hrtimer_init-hrtimer_init_sleepe.patch
Patch0200:	  ./rt/0201-hrtimers-Prepare-full-preemption.patch
Patch0201:	  ./rt/0202-hrtimer-by-timers-by-default-into-the-softirq-contex.patch
Patch0202:	  ./rt/0203-alarmtimer-Prevent-live-lock-in-alarm_cancel.patch
Patch0203:	  ./rt/0204-posix-timers-user-proper-timer-while-waiting-for-ala.patch
Patch0204:	  ./rt/0205-posix-timers-move-the-rcu-head-out-of-the-union.patch
Patch0205:	  ./rt/0206-hrtimer-Move-schedule_work-call-to-helper-thread.patch
Patch0206:	  ./rt/0207-timer-fd-Prevent-live-lock.patch
Patch0207:	  ./rt/0208-posix-timers-Thread-posix-cpu-timers-on-rt.patch
Patch0208:	  ./rt/0209-sched-Move-task_struct-cleanup-to-RCU.patch
Patch0209:	  ./rt/0210-sched-Limit-the-number-of-task-migrations-per-batch.patch
Patch0210:	  ./rt/0211-sched-Move-mmdrop-to-RCU-on-RT.patch
Patch0211:	  ./rt/0212-kernel-sched-move-stack-kprobe-clean-up-to-__put_tas.patch
Patch0212:	  ./rt/0213-sched-Add-saved_state-for-tasks-blocked-on-sleeping-.patch
Patch0213:	  ./rt/0214-sched-Prevent-task-state-corruption-by-spurious-lock.patch
Patch0214:	  ./rt/0215-sched-Remove-TASK_ALL.patch
Patch0215:	  ./rt/0216-sched-Do-not-account-rcu_preempt_depth-on-RT-in-migh.patch
Patch0216:	  ./rt/0217-sched-Take-RT-softirq-semantics-into-account-in-cond.patch
Patch0217:	  ./rt/0218-sched-Use-the-proper-LOCK_OFFSET-for-cond_resched.patch
Patch0218:	  ./rt/0219-sched-Disable-TTWU_QUEUE-on-RT.patch
Patch0219:	  ./rt/0220-sched-Disable-CONFIG_RT_GROUP_SCHED-on-RT.patch
Patch0220:	  ./rt/0221-sched-ttwu-Return-success-when-only-changing-the-sav.patch
Patch0221:	  ./rt/0222-sched-workqueue-Only-wake-up-idle-workers-if-not-blo.patch
Patch0222:	  ./rt/0223-rt-Increase-decrease-the-nr-of-migratory-tasks-when-.patch
Patch0223:	  ./rt/0224-stop_machine-convert-stop_machine_run-to-PREEMPT_RT.patch
Patch0224:	  ./rt/0225-stop_machine-Use-raw-spinlocks.patch
Patch0225:	  ./rt/0226-hotplug-Lightweight-get-online-cpus.patch
Patch0226:	  ./rt/0227-trace-Add-migrate-disabled-counter-to-tracing-output.patch
Patch0227:	  ./rt/0228-lockdep-Make-it-RT-aware.patch
Patch0228:	  ./rt/0229-lockdep-disable-self-test.patch
Patch0229:	  ./rt/0230-locking-Disable-spin-on-owner-for-RT.patch
Patch0230:	  ./rt/0231-tasklet-Prevent-tasklets-from-going-into-infinite-sp.patch
Patch0231:	  ./rt/0232-softirq-Check-preemption-after-reenabling-interrupts.patch
Patch0232:	  ./rt/0233-softirq-Disable-softirq-stacks-for-RT.patch
Patch0233:	  ./rt/0234-softirq-Split-softirq-locks.patch
Patch0234:	  ./rt/0235-kernel-softirq-unlock-with-irqs-on.patch
Patch0235:	  ./rt/0236-genirq-Allow-disabling-of-softirq-processing-in-irq-.patch
Patch0236:	  ./rt/0237-softirq-split-timer-softirqs-out-of-ksoftirqd.patch
Patch0237:	  ./rt/0238-softirq-wake-the-timer-softirq-if-needed.patch
Patch0238:	  ./rt/0239-rtmutex-trylock-is-okay-on-RT.patch
Patch0239:	  ./rt/0240-fs-nfs-turn-rmdir_sem-into-a-semaphore.patch
Patch0240:	  ./rt/0241-rtmutex-Handle-the-various-new-futex-race-conditions.patch
Patch0241:	  ./rt/0242-futex-Fix-bug-on-when-a-requeued-RT-task-times-out.patch
Patch0242:	  ./rt/0243-locking-rtmutex-don-t-drop-the-wait_lock-twice.patch
Patch0243:	  ./rt/0244-futex-Ensure-lock-unlock-symetry-versus-pi_lock-and-.patch
Patch0244:	  ./rt/0245-pid.h-include-atomic.h.patch
Patch0245:	  ./rt/0246-arm-include-definition-for-cpumask_t.patch
Patch0246:	  ./rt/0247-locking-locktorture-Do-NOT-include-rwlock.h-directly.patch
Patch0247:	  ./rt/0248-rtmutex-Add-rtmutex_lock_killable.patch
Patch0248:	  ./rt/0249-rtmutex-Make-lock_killable-work.patch
Patch0249:	  ./rt/0250-spinlock-Split-the-lock-types-header.patch
Patch0250:	  ./rt/0251-rtmutex-Avoid-include-hell.patch
Patch0251:	  ./rt/0252-rbtree-don-t-include-the-rcu-header.patch
Patch0252:	  ./rt/0253-rtmutex-Provide-rt_mutex_slowlock_locked.patch
Patch0253:	  ./rt/0254-rtmutex-export-lockdep-less-version-of-rt_mutex-s-lo.patch
Patch0254:	  ./rt/0255-rtmutex-add-sleeping-lock-implementation.patch
Patch0255:	  ./rt/0256-rtmutex-add-mutex-implementation-based-on-rtmutex.patch
Patch0256:	  ./rt/0257-rtmutex-add-rwsem-implementation-based-on-rtmutex.patch
Patch0257:	  ./rt/0258-rtmutex-add-rwlock-implementation-based-on-rtmutex.patch
Patch0258:	  ./rt/0259-rtmutex-wire-up-RT-s-locking.patch
Patch0259:	  ./rt/0260-rtmutex-add-ww_mutex-addon-for-mutex-rt.patch
Patch0260:	  ./rt/0261-locking-rt-mutex-fix-deadlock-in-device-mapper-block.patch
Patch0261:	  ./rt/0262-locking-rtmutex-re-init-the-wait_lock-in-rt_mutex_in.patch
Patch0262:	  ./rt/0263-ptrace-fix-ptrace-vs-tasklist_lock-race.patch
Patch0263:	  ./rt/0264-RCU-we-need-to-skip-that-warning-but-only-on-sleepin.patch
Patch0264:	  ./rt/0265-RCU-skip-the-schedule-in-RCU-section-warning-on-UP-t.patch
Patch0265:	  ./rt/0266-locking-don-t-check-for-__LINUX_SPINLOCK_TYPES_H-on-.patch
Patch0266:	  ./rt/0267-rcu-Frob-softirq-test.patch
Patch0267:	  ./rt/0268-rcu-Merge-RCU-bh-into-RCU-preempt.patch
Patch0268:	  ./rt/0269-rcu-Make-ksoftirqd-do-RCU-quiescent-states.patch
Patch0269:	  ./rt/0270-rcutree-rcu_bh_qs-Disable-irq-while-calling-rcu_pree.patch
Patch0270:	  ./rt/0271-tty-serial-omap-Make-the-locking-RT-aware.patch
Patch0271:	  ./rt/0272-tty-serial-pl011-Make-the-locking-work-on-RT.patch
Patch0272:	  ./rt/0273-rt-Improve-the-serial-console-PASS_LIMIT.patch
Patch0273:	  ./rt/0274-tty-serial-8250-don-t-take-the-trylock-during-oops.patch
Patch0274:	  ./rt/0275-locking-percpu-rwsem-Remove-preempt_disable-variants.patch
Patch0275:	  ./rt/0276-fs-namespace-preemption-fix.patch
Patch0276:	  ./rt/0277-mm-Protect-activate_mm-by-preempt_-disable-enable-_r.patch
Patch0277:	  ./rt/0278-block-Turn-off-warning-which-is-bogus-on-RT.patch
Patch0278:	  ./rt/0279-fs-ntfs-disable-interrupt-only-on-RT.patch
Patch0279:	  ./rt/0280-fs-jbd2-pull-your-plug-when-waiting-for-space.patch
Patch0280:	  ./rt/0281-Revert-fs-jbd2-pull-your-plug-when-waiting-for-space.patch
Patch0281:	  ./rt/0282-fs-dcache-bringt-back-explicit-INIT_HLIST_BL_HEAD-in.patch
Patch0282:	  ./rt/0283-fs-dcache-disable-preemption-on-i_dir_seq-s-write-si.patch
Patch0283:	  ./rt/0284-x86-Convert-mce-timer-to-hrtimer.patch
Patch0284:	  ./rt/0285-x86-mce-use-swait-queue-for-mce-wakeups.patch
Patch0285:	  ./rt/0286-x86-stackprotector-Avoid-random-pool-on-rt.patch
Patch0286:	  ./rt/0287-x86-Use-generic-rwsem_spinlocks-on-rt.patch
Patch0287:	  ./rt/0288-x86-UV-raw_spinlock-conversion.patch
Patch0288:	  ./rt/0289-thermal-Defer-thermal-wakups-to-threads.patch
Patch0289:	  ./rt/0290-fs-epoll-Do-not-disable-preemption-on-RT.patch
Patch0290:	  ./rt/0291-mm-vmalloc-Another-preempt-disable-region-which-suck.patch
Patch0291:	  ./rt/0292-block-mq-use-cpu_light.patch
Patch0292:	  ./rt/0293-block-mq-do-not-invoke-preempt_disable.patch
Patch0293:	  ./rt/0294-block-mq-don-t-complete-requests-via-IPI.patch
Patch0294:	  ./rt/0295-md-raid5-Make-raid5_percpu-handling-RT-aware.patch
Patch0295:	  ./rt/0296-md-raid5-do-not-disable-interrupts.patch
Patch0296:	  ./rt/0297-rt-Introduce-cpu_chill.patch
Patch0297:	  ./rt/0298-cpu_chill-Add-a-UNINTERRUPTIBLE-hrtimer_nanosleep.patch
Patch0298:	  ./rt/0299-kernel-cpu_chill-use-schedule_hrtimeout.patch
Patch0299:	  ./rt/0300-Revert-cpu_chill-Add-a-UNINTERRUPTIBLE-hrtimer_nanos.patch
Patch0300:	  ./rt/0301-rtmutex-annotate-sleeping-lock-context.patch
Patch0301:	  ./rt/0302-block-blk-mq-move-blk_queue_usage_counter_release-in.patch
Patch0302:	  ./rt/0303-block-Use-cpu_chill-for-retry-loops.patch
Patch0303:	  ./rt/0304-fs-dcache-Use-cpu_chill-in-trylock-loops.patch
Patch0304:	  ./rt/0305-net-Use-cpu_chill-instead-of-cpu_relax.patch
Patch0305:	  ./rt/0306-fs-dcache-use-swait_queue-instead-of-waitqueue.patch
Patch0306:	  ./rt/0307-workqueue-Use-normal-rcu.patch
Patch0307:	  ./rt/0308-workqueue-Use-local-irq-lock-instead-of-irq-disable-.patch
Patch0308:	  ./rt/0309-workqueue-Prevent-workqueue-versus-ata-piix-livelock.patch
Patch0309:	  ./rt/0310-sched-Distangle-worker-accounting-from-rqlock.patch
Patch0310:	  ./rt/0311-percpu_ida-Use-local-locks.patch
Patch0311:	  ./rt/0312-debugobjects-Make-RT-aware.patch
Patch0312:	  ./rt/0313-jump-label-disable-if-stop_machine-is-used.patch
Patch0313:	  ./rt/0314-seqlock-Prevent-rt-starvation.patch
Patch0314:	  ./rt/0315-sunrpc-Make-svc_xprt_do_enqueue-use-get_cpu_light.patch
Patch0315:	  ./rt/0316-net-Use-skbufhead-with-raw-lock.patch
Patch0316:	  ./rt/0317-net-core-cpuhotplug-Drain-input_pkt_queue-lockless.patch
Patch0317:	  ./rt/0318-net-move-xmit_recursion-to-per-task-variable-on-RT.patch
Patch0318:	  ./rt/0319-net-use-task_struct-instead-of-CPU-number-as-the-que.patch
Patch0319:	  ./rt/0320-net-provide-a-way-to-delegate-processing-a-softirq-t.patch
Patch0320:	  ./rt/0321-net-dev-always-take-qdisc-s-busylock-in-__dev_xmit_s.patch
Patch0321:	  ./rt/0322-net-Qdisc-use-a-seqlock-instead-seqcount.patch
Patch0322:	  ./rt/0323-net-add-back-the-missing-serialization-in-ip_send_un.patch
Patch0323:	  ./rt/0324-net-take-the-tcp_sk_lock-lock-with-BH-disabled.patch
Patch0324:	  ./rt/0325-net-add-a-lock-around-icmp_sk.patch
Patch0325:	  ./rt/0326-net-use-trylock-in-icmp_sk.patch
Patch0326:	  ./rt/0327-net-Have-__napi_schedule_irqoff-disable-interrupts-o.patch
Patch0327:	  ./rt/0328-irqwork-push-most-work-into-softirq-context.patch
Patch0328:	  ./rt/0329-irqwork-Move-irq-safe-work-to-irq-context.patch
Patch0329:	  ./rt/0330-snd-pcm-fix-snd_pcm_stream_lock-irqs_disabled-splats.patch
Patch0330:	  ./rt/0331-printk-Make-rt-aware.patch
Patch0331:	  ./rt/0332-kernel-printk-Don-t-try-to-print-from-IRQ-NMI-region.patch
Patch0332:	  ./rt/0333-printk-Drop-the-logbuf_lock-more-often.patch
Patch0333:	  ./rt/0334-powerpc-Use-generic-rwsem-on-RT.patch
Patch0334:	  ./rt/0335-powerpc-kvm-Disable-in-kernel-MPIC-emulation-for-PRE.patch
Patch0335:	  ./rt/0336-powerpc-ps3-device-init.c-adapt-to-completions-using.patch
Patch0336:	  ./rt/0337-ARM-at91-tclib-Default-to-tclib-timer-for-RT.patch
Patch0337:	  ./rt/0338-arm-unwind-use-a-raw_spin_lock.patch
Patch0338:	  ./rt/0339-ARM-enable-irq-in-translation-section-permission-fau.patch
Patch0339:	  ./rt/0340-genirq-update-irq_set_irqchip_state-documentation.patch
Patch0340:	  ./rt/0341-KVM-arm-arm64-downgrade-preempt_disable-d-region-to-.patch
Patch0341:	  ./rt/0342-arm64-xen-Make-XEN-depend-on-RT.patch
Patch0342:	  ./rt/0343-kgdb-serial-Short-term-workaround.patch
Patch0343:	  ./rt/0344-sysfs-Add-sys-kernel-realtime-entry.patch
Patch0344:	  ./rt/0345-powerpc-Disable-highmem-on-RT.patch
Patch0345:	  ./rt/0346-mips-Disable-highmem-on-RT.patch
Patch0346:	  ./rt/0347-mm-rt-kmap_atomic-scheduling.patch
Patch0347:	  ./rt/0348-mm-rt-Fix-generic-kmap_atomic-for-RT.patch
Patch0348:	  ./rt/0349-x86-highmem-Add-a-already-used-pte-check.patch
Patch0349:	  ./rt/0350-arm-highmem-Flush-tlb-on-unmap.patch
Patch0350:	  ./rt/0351-arm-Enable-highmem-for-rt.patch
Patch0351:	  ./rt/0352-scsi-fcoe-Make-RT-aware.patch
Patch0352:	  ./rt/0353-sas-ata-isci-dont-t-disable-interrupts-in-qc_issue-h.patch
Patch0353:	  ./rt/0354-x86-crypto-Reduce-preempt-disabled-regions.patch
Patch0354:	  ./rt/0355-crypto-Reduce-preempt-disabled-regions-more-algos.patch
Patch0355:	  ./rt/0356-crypto-limit-more-FPU-enabled-sections.patch
Patch0356:	  ./rt/0357-arm-disable-NEON-in-kernel-mode.patch
Patch0357:	  ./rt/0358-dm-Make-rt-aware.patch
Patch0358:	  ./rt/0359-acpi-rt-Convert-acpi_gbl_hardware-lock-back-to-a-raw.patch
Patch0359:	  ./rt/0360-cpumask-Disable-CONFIG_CPUMASK_OFFSTACK-for-RT.patch
Patch0360:	  ./rt/0361-random-Make-it-work-on-rt.patch
Patch0361:	  ./rt/0362-random-avoid-preempt_disable-ed-section.patch
Patch0362:	  ./rt/0363-char-random-don-t-print-that-the-init-is-done.patch
Patch0363:	  ./rt/0364-cpu-hotplug-Implement-CPU-pinning.patch
Patch0364:	  ./rt/0365-hotplug-duct-tape-RT-rwlock-usage-for-non-RT.patch
Patch0365:	  ./rt/0366-scsi-qla2xxx-Use-local_irq_save_nort-in-qla2x00_poll.patch
Patch0366:	  ./rt/0367-net-Remove-preemption-disabling-in-netif_rx.patch
Patch0367:	  ./rt/0368-net-Another-local_irq_disable-kmalloc-headache.patch
Patch0368:	  ./rt/0369-net-core-protect-users-of-napi_alloc_cache-against-r.patch
Patch0369:	  ./rt/0370-net-netfilter-Serialize-xt_write_recseq-sections-on-.patch
Patch0370:	  ./rt/0371-net-Add-a-mutex-around-devnet_rename_seq.patch
Patch0371:	  ./rt/0372-crypto-Convert-crypto-notifier-chain-to-SRCU.patch
Patch0372:	  ./rt/0373-lockdep-selftest-Only-do-hardirq-context-test-for-ra.patch
Patch0373:	  ./rt/0374-lockdep-selftest-fix-warnings-due-to-missing-PREEMPT.patch
Patch0374:	  ./rt/0375-srcu-use-cpu_online-instead-custom-check.patch
Patch0375:	  ./rt/0376-srcu-Prohibit-call_srcu-use-under-raw-spinlocks.patch
Patch0376:	  ./rt/0377-srcu-replace-local_irqsave-with-a-locallock.patch
Patch0377:	  ./rt/0378-rcu-Disable-RCU_FAST_NO_HZ-on-RT.patch
Patch0378:	  ./rt/0379-rcu-Eliminate-softirq-processing-from-rcutree.patch
Patch0379:	  ./rt/0380-rcu-make-RCU_BOOST-default-on-RT.patch
Patch0380:	  ./rt/0381-rcu-enable-rcu_normal_after_boot-by-default-for-RT.patch
Patch0381:	  ./rt/0382-sched-Add-support-for-lazy-preemption.patch
Patch0382:	  ./rt/0383-ftrace-Fix-trace-header-alignment.patch
Patch0383:	  ./rt/0384-x86-Support-for-lazy-preemption.patch
Patch0384:	  ./rt/0385-arm-Add-support-for-lazy-preemption.patch
Patch0385:	  ./rt/0386-powerpc-Add-support-for-lazy-preemption.patch
Patch0386:	  ./rt/0387-arch-arm64-Add-lazy-preempt-support.patch
Patch0387:	  ./rt/0388-leds-trigger-disable-CPU-trigger-on-RT.patch
Patch0388:	  ./rt/0389-mmci-Remove-bogus-local_irq_save.patch
Patch0389:	  ./rt/0390-cpufreq-drop-K8-s-driver-from-beeing-selected.patch
Patch0390:	  ./rt/0391-connector-cn_proc-Protect-send_msg-with-a-local-lock.patch
Patch0391:	  ./rt/0392-drivers-block-zram-Replace-bit-spinlocks-with-rtmute.patch
Patch0392:	  ./rt/0393-drivers-zram-Don-t-disable-preemption-in-zcomp_strea.patch
Patch0393:	  ./rt/0394-drivers-zram-fix-zcomp_stream_get-smp_processor_id-u.patch
Patch0394:	  ./rt/0395-tpm_tis-fix-stall-after-iowrite-s.patch
Patch0395:	  ./rt/0396-pci-switchtec-Don-t-use-completion-s-wait-queue.patch
Patch0396:	  ./rt/0397-drm-radeon-i915-Use-preempt_disable-enable_rt-where-.patch
Patch0397:	  ./rt/0398-drm-i915-Use-local_lock-unlock_irq-in-intel_pipe_upd.patch
Patch0398:	  ./rt/0399-cgroups-use-simple-wait-in-css_release.patch
Patch0399:	  ./rt/0400-memcontrol-Prevent-scheduling-while-atomic-in-cgroup.patch
Patch0400:	  ./rt/0401-Revert-memcontrol-Prevent-scheduling-while-atomic-in.patch
Patch0401:	  ./rt/0402-cpuset-Convert-callback_lock-to-raw_spinlock_t.patch
Patch0402:	  ./rt/0403-rt-ntp-Move-call-to-schedule_delayed_work-to-helper-.patch
Patch0403:	  ./rt/0404-Revert-rt-ntp-Move-call-to-schedule_delayed_work-to-.patch
Patch0404:	  ./rt/0405-md-disable-bcache.patch
Patch0405:	  ./rt/0406-apparmor-use-a-locallock-instead-preempt_disable.patch
Patch0406:	  ./rt/0407-workqueue-Prevent-deadlock-stall-on-RT.patch
# We will set localversion at our own convenience.
#Patch0407:	  ./rt/0408-Add-localversion-for-RT-release.patch
Patch0408:	  ./rt/0409-tracing-Add-field-modifier-parsing-hist-error-for-hi.patch
Patch0409:	  ./rt/0410-tracing-Add-field-parsing-hist-error-for-hist-trigge.patch
Patch0410:	  ./rt/0411-tracing-Restore-proper-field-flag-printing-when-disp.patch
Patch0411:	  ./rt/0412-tracing-Uninitialized-variable-in-create_tracing_map.patch
Patch0412:	  ./rt/0413-tracing-Fix-a-potential-NULL-dereference.patch
# Ditto
#Patch0413:	  ./rt/0414-Linux-4.14.59-rt37-REBASE.patch

# common
Patch0414:        linux-4.14-Log-kmsg-dump-on-panic.patch
Patch0415:        double-tcp_mem-limits.patch
# TODO: disable this patch, check for regressions
#Patch0416:        linux-4.9-watchdog-Disable-watchdog-on-virtual-machines.patch
Patch0417:        SUNRPC-Do-not-reuse-srcport-for-TIME_WAIT-socket.patch
Patch0418:        SUNRPC-xs_bind-uses-ip_local_reserved_ports.patch
Patch0419:        vsock-transport-for-9p.patch
Patch0420:        x86-vmware-STA-support.patch
# rpi3 dts
Patch0421:	arm-dts-add-vchiq-entry.patch
#HyperV patches
Patch0422:        0004-vmbus-Don-t-spam-the-logs-with-unknown-GUIDs.patch
# TODO: Is CONFIG_HYPERV_VSOCKETS the same?
#Patch0423:        0014-hv_sock-introduce-Hyper-V-Sockets.patch
#FIPS patches - allow some algorithms
Patch0424:        Allow-some-algo-tests-for-FIPS.patch
Patch0425:        add-sysctl-to-disallow-unprivileged-CLONE_NEWUSER-by-default.patch
# Fix CVE-2017-1000252
Patch0426:        kvm-dont-accept-wrong-gsi-values.patch

%if 0%{?kat_build:1}
Patch1000:	%{kat_build}.patch
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
BuildRequires:	audit-devel
Requires:       filesystem kmod
Requires(post):(coreutils or toybox)
%define localversion_rt rt37
%define uname_r %{version}-%{release}-%{localversion_rt}

%description
The Linux package contains the Preeempt-RT Linux kernel.

%package devel
Summary:        Kernel Dev
Group:          System Environment/Kernel
Obsoletes:      linux-dev
Requires:       %{name} = %{version}-%{release}
Requires:       python2 gawk
%description devel
The Linux package contains the Linux kernel dev files

%package drivers-gpu
Summary:        Kernel GPU Drivers
Group:          System Environment/Kernel
Requires:       %{name} = %{version}-%{release}
%description drivers-gpu
The Linux package contains the Linux kernel drivers for GPU

%package sound
Summary:        Kernel Sound modules
Group:          System Environment/Kernel
Requires:       %{name} = %{version}-%{release}
%description sound
The Linux package contains the Linux kernel sound support

%package docs
Summary:        Kernel docs
Group:          System Environment/Kernel
Requires:       python2
%description docs
The Linux package contains the Linux kernel doc files

%package tools
Summary:        This package contains the 'perf' performance analysis tools for Linux kernel
Group:          System/Tools
Requires:       %{name} = %{version}-%{release}
Requires:       audit
%description tools
This package contains the 'perf' performance analysis tools for Linux kernel.

%ifarch aarch64
%package dtb-rpi3
Summary:        Kernel Device Tree Blob files for Raspberry Pi3
Group:          System Environment/Kernel
Requires:       %{name} = %{version}-%{release}
%description dtb-rpi3
Kernel Device Tree Blob files for Raspberry Pi3
%endif


%prep
%setup -q -n linux-%{version}
%ifarch x86_64
%setup -D -b 3 -n linux-%{version}
%endif
%patch0000 -p1
%patch0001 -p1
%patch0002 -p1
%patch0003 -p1
%patch0004 -p1
%patch0005 -p1
%patch0006 -p1
%patch0007 -p1
%patch0008 -p1
%patch0009 -p1
%patch0010 -p1
%patch0011 -p1
%patch0012 -p1
%patch0013 -p1
%patch0014 -p1
%patch0015 -p1
%patch0016 -p1
%patch0017 -p1
%patch0018 -p1
%patch0019 -p1
%patch0020 -p1
%patch0021 -p1
%patch0022 -p1
%patch0023 -p1
%patch0024 -p1
%patch0025 -p1
%patch0026 -p1
%patch0027 -p1
%patch0028 -p1
%patch0029 -p1
%patch0030 -p1
%patch0031 -p1
%patch0032 -p1
%patch0033 -p1
%patch0034 -p1
%patch0035 -p1
%patch0036 -p1
%patch0037 -p1
%patch0038 -p1
%patch0039 -p1
%patch0040 -p1
%patch0041 -p1
%patch0042 -p1
%patch0043 -p1
%patch0044 -p1
%patch0045 -p1
%patch0046 -p1
%patch0047 -p1
%patch0048 -p1
%patch0049 -p1
%patch0050 -p1
%patch0051 -p1
%patch0052 -p1
%patch0053 -p1
%patch0054 -p1
%patch0055 -p1
%patch0056 -p1
%patch0057 -p1
%patch0058 -p1
%patch0059 -p1
%patch0060 -p1
%patch0061 -p1
%patch0062 -p1
%patch0063 -p1
%patch0064 -p1
%patch0065 -p1
%patch0066 -p1
%patch0067 -p1
%patch0068 -p1
%patch0069 -p1
%patch0070 -p1
%patch0071 -p1
%patch0072 -p1
%patch0073 -p1
%patch0074 -p1
%patch0075 -p1
%patch0076 -p1
%patch0077 -p1
%patch0078 -p1
%patch0079 -p1
%patch0080 -p1
%patch0081 -p1
%patch0082 -p1
%patch0083 -p1
%patch0084 -p1
%patch0085 -p1
%patch0086 -p1
%patch0087 -p1
%patch0088 -p1
%patch0089 -p1
%patch0090 -p1
%patch0091 -p1
%patch0092 -p1
%patch0093 -p1
%patch0094 -p1
%patch0095 -p1
%patch0096 -p1
%patch0097 -p1
%patch0098 -p1
%patch0099 -p1
%patch0100 -p1
%patch0101 -p1
%patch0102 -p1
%patch0103 -p1
%patch0104 -p1
%patch0105 -p1
%patch0106 -p1
%patch0107 -p1
%patch0108 -p1
%patch0109 -p1
%patch0110 -p1
%patch0111 -p1
%patch0112 -p1
%patch0113 -p1
%patch0114 -p1
%patch0115 -p1
%patch0116 -p1
%patch0117 -p1
%patch0118 -p1
%patch0119 -p1
%patch0120 -p1
%patch0121 -p1
%patch0122 -p1
%patch0123 -p1
%patch0124 -p1
%patch0125 -p1
%patch0126 -p1
%patch0127 -p1
%patch0128 -p1
%patch0129 -p1
%patch0130 -p1
%patch0131 -p1
%patch0132 -p1
%patch0133 -p1
%patch0134 -p1
%patch0135 -p1
%patch0136 -p1
%patch0137 -p1
%patch0138 -p1
%patch0139 -p1
%patch0140 -p1
%patch0141 -p1
%patch0142 -p1
%patch0143 -p1
%patch0144 -p1
%patch0145 -p1
%patch0146 -p1
%patch0147 -p1
%patch0148 -p1
%patch0149 -p1
%patch0150 -p1
%patch0151 -p1
%patch0152 -p1
%patch0153 -p1
%patch0154 -p1
%patch0155 -p1
%patch0156 -p1
%patch0157 -p1
%patch0158 -p1
%patch0159 -p1
%patch0160 -p1
%patch0161 -p1
%patch0162 -p1
%patch0163 -p1
%patch0164 -p1
%patch0165 -p1
%patch0166 -p1
%patch0167 -p1
%patch0168 -p1
%patch0169 -p1
%patch0170 -p1
%patch0171 -p1
%patch0172 -p1
%patch0173 -p1
%patch0174 -p1
%patch0175 -p1
%patch0176 -p1
%patch0177 -p1
%patch0178 -p1
%patch0179 -p1
%patch0180 -p1
%patch0181 -p1
%patch0182 -p1
%patch0183 -p1
%patch0184 -p1
%patch0185 -p1
%patch0186 -p1
%patch0187 -p1
%patch0188 -p1
%patch0189 -p1
%patch0190 -p1
%patch0191 -p1
%patch0192 -p1
%patch0193 -p1
%patch0194 -p1
%patch0195 -p1
%patch0196 -p1
%patch0197 -p1
%patch0198 -p1
%patch0199 -p1
%patch0200 -p1
%patch0201 -p1
%patch0202 -p1
%patch0203 -p1
%patch0204 -p1
%patch0205 -p1
%patch0206 -p1
%patch0207 -p1
%patch0208 -p1
%patch0209 -p1
%patch0210 -p1
%patch0211 -p1
%patch0212 -p1
%patch0213 -p1
%patch0214 -p1
%patch0215 -p1
%patch0216 -p1
%patch0217 -p1
%patch0218 -p1
%patch0219 -p1
%patch0220 -p1
%patch0221 -p1
%patch0222 -p1
%patch0223 -p1
%patch0224 -p1
%patch0225 -p1
%patch0226 -p1
%patch0227 -p1
%patch0228 -p1
%patch0229 -p1
%patch0230 -p1
%patch0231 -p1
%patch0232 -p1
%patch0233 -p1
%patch0234 -p1
%patch0235 -p1
%patch0236 -p1
%patch0237 -p1
%patch0238 -p1
%patch0239 -p1
%patch0240 -p1
%patch0241 -p1
%patch0242 -p1
%patch0243 -p1
%patch0244 -p1
%patch0245 -p1
%patch0246 -p1
%patch0247 -p1
%patch0248 -p1
%patch0249 -p1
%patch0250 -p1
%patch0251 -p1
%patch0252 -p1
%patch0253 -p1
%patch0254 -p1
%patch0255 -p1
%patch0256 -p1
%patch0257 -p1
%patch0258 -p1
%patch0259 -p1
%patch0260 -p1
%patch0261 -p1
%patch0262 -p1
%patch0263 -p1
%patch0264 -p1
%patch0265 -p1
%patch0266 -p1
%patch0267 -p1
%patch0268 -p1
%patch0269 -p1
%patch0270 -p1
%patch0271 -p1
%patch0272 -p1
%patch0273 -p1
%patch0274 -p1
%patch0275 -p1
%patch0276 -p1
%patch0277 -p1
%patch0278 -p1
%patch0279 -p1
%patch0280 -p1
%patch0281 -p1
%patch0282 -p1
%patch0283 -p1
%patch0284 -p1
%patch0285 -p1
%patch0286 -p1
%patch0287 -p1
%patch0288 -p1
%patch0289 -p1
%patch0290 -p1
%patch0291 -p1
%patch0292 -p1
%patch0293 -p1
%patch0294 -p1
%patch0295 -p1
%patch0296 -p1
%patch0297 -p1
%patch0298 -p1
%patch0299 -p1
%patch0300 -p1
%patch0301 -p1
%patch0302 -p1
%patch0303 -p1
%patch0304 -p1
%patch0305 -p1
%patch0306 -p1
%patch0307 -p1
%patch0308 -p1
%patch0309 -p1
%patch0310 -p1
%patch0311 -p1
%patch0312 -p1
%patch0313 -p1
%patch0314 -p1
%patch0315 -p1
%patch0316 -p1
%patch0317 -p1
%patch0318 -p1
%patch0319 -p1
%patch0320 -p1
%patch0321 -p1
%patch0322 -p1
%patch0323 -p1
%patch0324 -p1
%patch0325 -p1
%patch0326 -p1
%patch0327 -p1
%patch0328 -p1
%patch0329 -p1
%patch0330 -p1
%patch0331 -p1
%patch0332 -p1
%patch0333 -p1
%patch0334 -p1
%patch0335 -p1
%patch0336 -p1
%patch0337 -p1
%patch0338 -p1
%patch0339 -p1
%patch0340 -p1
%patch0341 -p1
%patch0342 -p1
%patch0343 -p1
%patch0344 -p1
%patch0345 -p1
%patch0346 -p1
%patch0347 -p1
%patch0348 -p1
%patch0349 -p1
%patch0350 -p1
%patch0351 -p1
%patch0352 -p1
%patch0353 -p1
%patch0354 -p1
%patch0355 -p1
%patch0356 -p1
%patch0357 -p1
%patch0358 -p1
%patch0359 -p1
%patch0360 -p1
%patch0361 -p1
%patch0362 -p1
%patch0363 -p1
%patch0364 -p1
%patch0365 -p1
%patch0366 -p1
%patch0367 -p1
%patch0368 -p1
%patch0369 -p1
%patch0370 -p1
%patch0371 -p1
%patch0372 -p1
%patch0373 -p1
%patch0374 -p1
%patch0375 -p1
%patch0376 -p1
%patch0377 -p1
%patch0378 -p1
%patch0379 -p1
%patch0380 -p1
%patch0381 -p1
%patch0382 -p1
%patch0383 -p1
%patch0384 -p1
%patch0385 -p1
%patch0386 -p1
%patch0387 -p1
%patch0388 -p1
%patch0389 -p1
%patch0390 -p1
%patch0391 -p1
%patch0392 -p1
%patch0393 -p1
%patch0394 -p1
%patch0395 -p1
%patch0396 -p1
%patch0397 -p1
%patch0398 -p1
%patch0399 -p1
%patch0400 -p1
%patch0401 -p1
%patch0402 -p1
%patch0403 -p1
%patch0404 -p1
%patch0405 -p1
%patch0406 -p1
#%patch0407 -p1
%patch0408 -p1
%patch0409 -p1
%patch0410 -p1
%patch0411 -p1
%patch0412 -p1
#%patch0413 -p1
%patch0414 -p1
%patch0415 -p1
%patch0417 -p1
%patch0418 -p1
%patch0419 -p1
%patch0420 -p1
%patch0421 -p1
%patch0422 -p1
#%patch0423 -p1
%patch0424 -p1
%patch0425 -p1
%patch0426 -p1
%if 0%{?kat_build:1}
%patch1000 -p1
%endif

%build
make mrproper

%ifarch x86_64
cp %{SOURCE1} .config
arch="x86_64"
archdir="x86"
%endif

%ifarch aarch64
error 
cp %{SOURCE4} .config
arch="arm64"
archdir="arm64"
%endif

sed -i 's/CONFIG_LOCALVERSION="-rt"/CONFIG_LOCALVERSION="-%{release}-%{localversion_rt}"/' .config
make LC_ALL= oldconfig
make VERBOSE=1 KBUILD_BUILD_VERSION="1-photon" KBUILD_BUILD_HOST="photon" ARCH=${arch} %{?_smp_mflags}
make -C tools perf

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
install -vdm 755 %{buildroot}/etc
install -vdm 755 %{buildroot}/boot
install -vdm 755 %{buildroot}%{_defaultdocdir}/%{name}-%{uname_r}
install -vdm 755 %{buildroot}/usr/src/%{name}-headers-%{uname_r}
install -vdm 755 %{buildroot}/usr/lib/debug/lib/modules/%{uname_r}
make INSTALL_MOD_PATH=%{buildroot} modules_install

%ifarch x86_64
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

%ifarch aarch64
install -vm 644 arch/arm64/boot/Image %{buildroot}/boot/vmlinuz-%{uname_r}
# Install DTB files
install -vdm 755 %{buildroot}/boot/dtb
install -vm 640 arch/arm64/boot/dts/broadcom/bcm2837-rpi-3-b.dtb %{buildroot}/boot/dtb/
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
photon_cmdline=init=/lib/systemd/systemd ro loglevel=3 quiet no-vmw-sta
photon_linux=vmlinuz-%{uname_r}
photon_initrd=initrd.img-%{uname_r}
EOF

# Register myself to initramfs
mkdir -p %{buildroot}/%{_localstatedir}/lib/initramfs/kernel
cat > %{buildroot}/%{_localstatedir}/lib/initramfs/kernel/%{uname_r} << "EOF"
--add-drivers "tmem xen-scsifront xen-blkfront xen-acpi-processor xen-evtchn xen-gntalloc xen-gntdev xen-privcmd xen-pciback xenfs hv_utils hv_vmbus hv_storvsc hv_netvsc hv_sock hv_balloon cn"
EOF

#    Cleanup dangling symlinks
rm -rf %{buildroot}/lib/modules/%{uname_r}/source
rm -rf %{buildroot}/lib/modules/%{uname_r}/build

find . -name Makefile* -o -name Kconfig* -o -name *.pl | xargs  sh -c 'cp --parents "$@" %{buildroot}/usr/src/%{name}-headers-%{uname_r}' copy
find "arch/${archdir}/include" include scripts -type f | xargs  sh -c 'cp --parents "$@" %{buildroot}/usr/src/%{name}-headers-%{uname_r}' copy
find $(find "arch/${archdir}" -name include -o -name scripts -type d) -type f | xargs  sh -c 'cp --parents "$@" %{buildroot}/usr/src/%{name}-headers-%{uname_r}' copy
find "arch/${archdir}/include" Module.symvers include scripts -type f | xargs  sh -c 'cp --parents "$@" %{buildroot}/usr/src/%{name}-headers-%{uname_r}' copy
%ifarch x86_64
# CONFIG_STACK_VALIDATION=y requires objtool to build external modules
install -vsm 755 tools/objtool/objtool %{buildroot}/usr/src/%{name}-headers-%{uname_r}/tools/objtool/
install -vsm 755 tools/objtool/fixdep %{buildroot}/usr/src/%{name}-headers-%{uname_r}/tools/objtool/
%endif

cp .config %{buildroot}/usr/src/%{name}-headers-%{uname_r} # copy .config manually to be where it's expected to be
ln -sf "/usr/src/%{name}-headers-%{uname_r}" "%{buildroot}/lib/modules/%{uname_r}/build"
find %{buildroot}/lib/modules -name '*.ko' -print0 | xargs -0 chmod u+x

# disable (JOBS=1) parallel build to fix this issue:
# fixdep: error opening depfile: ./.plugin_cfg80211.o.d: No such file or directory
# Linux version that was affected is 4.4.26
make -C tools JOBS=1 DESTDIR=%{buildroot} prefix=%{_prefix} perf_install

%include %{SOURCE2}

%post
/sbin/depmod -aq %{uname_r}
ln -sf %{name}-%{uname_r}.cfg /boot/photon.cfg

%post drivers-gpu
/sbin/depmod -aq %{uname_r}

%post sound
/sbin/depmod -aq %{uname_r}

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
%exclude /lib/modules/%{uname_r}/kernel/drivers/gpu
%exclude /lib/modules/%{uname_r}/kernel/sound

%files docs
%defattr(-,root,root)
%{_defaultdocdir}/%{name}-%{uname_r}/*

%files devel
%defattr(-,root,root)
/lib/modules/%{uname_r}/build
/usr/src/%{name}-headers-%{uname_r}

%files drivers-gpu
%defattr(-,root,root)
%exclude /lib/modules/%{uname_r}/kernel/drivers/gpu/drm/cirrus/
/lib/modules/%{uname_r}/kernel/drivers/gpu

%files sound
%defattr(-,root,root)
/lib/modules/%{uname_r}/kernel/sound

%files tools
%defattr(-,root,root)
/usr/libexec
%exclude %{_libdir}/debug
%ifarch x86_64
/usr/lib64/traceevent
%endif
%ifarch aarch64
/usr/lib/traceevent
%endif
%{_bindir}
/etc/bash_completion.d/*
/usr/share/perf-core/strace/groups/file
/usr/share/doc/*

%ifarch aarch64
%files dtb-rpi3
%defattr(-,root,root)
/boot/dtb/bcm2837-rpi-3-b.dtb
%endif

%changelog
*   Mon Aug 06 2018 Tiejun Chen <tiejunc@vmware.com> 4.14.54-1
-   Enable Preempt-RT Linux version 4.14.54

