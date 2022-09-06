%global security_hardening none

Summary:        Kernel
Name:           linux-rt
Version:        4.19.256
Release:        2%{?kat_build:.%kat}%{?dist}
License:        GPLv2
URL:            http://www.kernel.org
Group:          System Environment/Kernel
Vendor:         VMware, Inc.
Distribution:   Photon

# Keep rt_version matched up with REBASE.patch
%define rt_version rt113
%define uname_r %{version}-%{release}-rt
%define _modulesdir /lib/modules/%{uname_r}

Source0: http://www.kernel.org/pub/linux/kernel/v4.x/linux-%{version}.tar.xz
%define sha512 linux=b7fa316b8d4a3874372da50efce932bc174803ddb0a866936b4102eb04626b1a97de4ef12a88fb5daaa70b0fd0498d329a149edf3dca54c2bef26af64ea5789b

Source1: config-rt
Source2: initramfs.trigger
# contains pre, postun, filetriggerun tasks
Source4: scriptlets.inc
Source5: check_for_config_applicability.inc

%define i40e_version 2.16.11
Source6: https://sourceforge.net/projects/e1000/files/i40e%20stable/%{i40e_version}/i40e-%{i40e_version}.tar.gz
%define sha512 i40e=004ec7da665cde30142807c51e4351d041a6df906325ad9e97a01868d1b019e1c9178ea58901e0c2dbbec69a9e00b897a9ecfd116a6d4acf3c7ab87962e2a0aa

%define iavf_version 4.4.2
Source8: https://sourceforge.net/projects/e1000/files/iavf%20stable/%{iavf_version}/iavf-%{iavf_version}.tar.gz
%define sha512 iavf=6eb5123cee389dd4af71a7e151b6a9fd9f8c47d91b9e0e930ef792d2e9bea6efd01d7599fbc9355bb1a3f86e56d17d037307d7759a13c9f1a8f3e007534709e5

%define ice_version 1.8.3
Source9: https://sourceforge.net/projects/e1000/files/ice%20stable/%{ice_version}/ice-%{ice_version}.tar.gz
%define sha512 ice=b5fa544998b72b65c365489ddaf67dbb64e1b5127dace333573fc95a146a13147f13c5593afb4b9b3ce227bbd6757e3f3827fdf19c3cc1ba1f74057309c7d37b

Source10: ApplyPatch.inc

# common
Patch0: linux-4.14-Log-kmsg-dump-on-panic.patch
Patch1: double-tcp_mem-limits.patch
# TODO: disable this patch, check for regressions
#Patch2: linux-4.9-watchdog-Disable-watchdog-on-virtual-machines.patch
Patch3: SUNRPC-Do-not-reuse-srcport-for-TIME_WAIT-socket.patch
Patch4: SUNRPC-xs_bind-uses-ip_local_reserved_ports.patch
Patch5: vsock-transport-for-9p.patch
Patch6: 4.18-x86-vmware-STA-support.patch
Patch7: 9p-trans_fd-extend-port-variable-to-u32.patch
Patch9: vsock-delay-detach-of-QP-with-outgoing-data.patch
Patch10: 0001-cgroup-v1-cgroup_stat-support.patch

Patch26: 4.18-add-sysctl-to-disallow-unprivileged-CLONE_NEWUSER-by-default.patch
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
#Fix for CVE-2019-20908
Patch40: efi-Restrict-efivar_ssdt_load-when-the-kernel-is-locked-down.patch
#Fix for CVE-2019-19338
Patch41: 0001-KVM-vmx-implement-MSR_IA32_TSX_CTRL-disable-RTM-func.patch
Patch42: 0001-KVM-vmx-use-MSR_IA32_TSX_CTRL-to-hard-disable-TSX-on.patch
# Fix for CVE-2020-16119
Patch58: 0001-dccp-ccid-move-timers-to-struct-dccp_sock.patch
Patch59: 0002-Revert-dccp-don-t-free-ccid2_hc_tx_sock-struct-in-dc.patch

#Fix for CVE-2020-16120
Patch60: 0001-ovl-pass-correct-flags-for-opening-real-directory.patch
Patch61: 0002-ovl-switch-to-mounter-creds-in-readdir.patch
Patch62: 0003-ovl-verify-permissions-in-ovl_path_open.patch
Patch63: 0004-ovl-call-secutiry-hook-in-ovl_real_ioctl.patch
Patch64: 0005-ovl-check-permission-to-open-real-file.patch

# Fix for CVE-2019-19770
Patch65: 0001-block-revert-back-to-synchronous-request_queue-remov.patch
Patch66: 0002-block-create-the-request_queue-debugfs_dir-on-regist.patch

#Fix for CVE-2020-36385
Patch67: 0001-RDMA-cma-Add-missing-locking-to-rdma_accept.patch
Patch68: 0001-RDMA-ucma-Rework-ucma_migrate_id-to-avoid-races-with.patch

#Fix for CVE-2022-1055
Patch69: 0001-net-sched-fix-use-after-free-in-tc_new_tfilter.patch

# CVE-2022-1789
Patch70: 0001-KVM-x86-mmu-fix-NULL-pointer-dereference-on-guest-IN.patch

# CVE-2022-2586
Patch72: 0002-netfilter-nf_tables-do-not-allow-RULE_ID-to-refer-to.patch

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

# Support for PTP_SYS_OFFSET_EXTENDED ioctl
Patch91: 0001-ptp-reorder-declarations-in-ptp_ioctl.patch
Patch92: 0002-ptp-add-PTP_SYS_OFFSET_EXTENDED-ioctl.patch
Patch93: 0003-ptp-deprecate-gettime64-in-favor-of-gettimex64.patch
Patch94: 0004-ptp-uapi-change-_IOW-to-IOWR-in-PTP_SYS_OFFSET_EXTEN.patch

# Allow PCI resets to be disabled from vfio_pci module
Patch100: 0001-drivers-vfio-pci-Add-kernel-parameter-to-allow-disab.patch
# Add PCI quirk to allow multiple devices under the same virtual PCI bridge
# to be put into separate IOMMU groups on ESXi.
Patch101: 0001-Add-PCI-quirk-for-VMware-PCIe-Root-Port.patch

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

# Update vmxnet3 driver to version 7
Patch120: 0001-vmxnet3-prepare-for-version-7-changes.patch
Patch121: 0002-vmxnet3-add-support-for-capability-registers.patch
Patch122: 0003-vmxnet3-add-support-for-large-passthrough-BAR-regist.patch
Patch123: 0004-vmxnet3-add-support-for-out-of-order-rx-completion.patch
Patch124: 0005-vmxnet3-add-command-to-set-ring-buffer-sizes.patch
Patch125: 0006-vmxnet3-limit-number-of-TXDs-used-for-TSO-packet.patch
Patch126: 0007-vmxnet3-use-ext1-field-to-indicate-encapsulated-pack.patch
Patch127: 0008-vmxnet3-update-to-version-7.patch
Patch128: 0009-vmxnet3-disable-overlay-offloads-if-UPT-device-does-.patch
Patch129: 0001-vmxnet3-do-not-reschedule-napi-for-rx-processing.patch

# Patchset to fix Panic due to nested priority inheritance in sched_deadline
Patch130: 0001-sched-deadline-Unthrottle-PI-boosted-threads-while-e.patch
Patch131: 0002-sched-deadline-Fix-stale-throttling-on-de-boosted-ta.patch
Patch132: 0003-sched-deadline-Fix-priority-inheritance-with-multipl.patch
Patch133: 0004-kernel-sched-Remove-dl_boosted-flag-comment.patch
Patch134: 0001-sched-deadline-Fix-BUG_ON-condition-for-deboosted-ta.patch

# Backport netfilter patch to allow checking if dst has xfrm attached
Patch141: 0001-netfilter-nf_tables-rt-allow-checking-if-dst-has-xfr.patch

# Real-Time kernel (PREEMPT_RT patches)
# Source: http://cdn.kernel.org/pub/linux/kernel/projects/rt/4.19/
Patch201: 0001-ARM-at91-add-TCB-registers-definitions.patch
Patch202: 0002-clocksource-drivers-Add-a-new-driver-for-the-Atmel-A.patch
Patch203: 0003-clocksource-drivers-timer-atmel-tcb-add-clockevent-d.patch
Patch204: 0004-clocksource-drivers-atmel-pit-make-option-silent.patch
Patch205: 0005-ARM-at91-Implement-clocksource-selection.patch
Patch206: 0006-ARM-configs-at91-use-new-TCB-timer-driver.patch
Patch207: 0007-ARM-configs-at91-unselect-PIT.patch
Patch208: 0008-irqchip-gic-v3-its-Move-pending-table-allocation-to-.patch
Patch209: 0009-kthread-convert-worker-lock-to-raw-spinlock.patch
Patch210: 0010-crypto-caam-qi-simplify-CGR-allocation-freeing.patch
Patch211: 0011-sched-fair-Robustify-CFS-bandwidth-timer-locking.patch
Patch212: 0012-arm-Convert-arm-boot_lock-to-raw.patch
Patch213: 0013-x86-ioapic-Don-t-let-setaffinity-unmask-threaded-EOI.patch
Patch214: 0014-cgroup-use-irqsave-in-cgroup_rstat_flush_locked.patch
Patch215: 0015-fscache-initialize-cookie-hash-table-raw-spinlocks.patch
Patch216: 0016-Drivers-hv-vmbus-include-header-for-get_irq_regs.patch
Patch217: 0017-percpu-include-irqflags.h-for-raw_local_irq_save.patch
Patch218: 0018-efi-Allow-efi-runtime.patch
Patch219: 0019-x86-efi-drop-task_lock-from-efi_switch_mm.patch
Patch220: 0020-arm64-KVM-compute_layout-before-altenates-are-applie.patch
Patch221: 0021-of-allocate-free-phandle-cache-outside-of-the-devtre.patch
Patch222: 0022-mm-kasan-make-quarantine_lock-a-raw_spinlock_t.patch
Patch223: 0023-EXP-rcu-Revert-expedited-GP-parallelization-cleverne.patch
Patch224: 0024-kmemleak-Turn-kmemleak_lock-to-raw-spinlock-on-RT.patch
Patch225: 0025-NFSv4-replace-seqcount_t-with-a-seqlock_t.patch
Patch226: 0026-kernel-sched-Provide-a-pointer-to-the-valid-CPU-mask.patch
Patch227: 0027-kernel-sched-core-add-migrate_disable.patch
Patch228: 0028-sched-migrate_disable-Add-export_symbol_gpl-for-__mi.patch
Patch229: 0029-arm-at91-do-not-disable-enable-clocks-in-a-row.patch
Patch230: 0030-clocksource-TCLIB-Allow-higher-clock-rates-for-clock.patch
Patch231: 0031-timekeeping-Split-jiffies-seqlock.patch
Patch232: 0032-signal-Revert-ptrace-preempt-magic.patch
Patch233: 0033-net-sched-Use-msleep-instead-of-yield.patch
Patch234: 0034-dm-rq-remove-BUG_ON-irqs_disabled-check.patch
Patch235: 0035-usb-do-no-disable-interrupts-in-giveback.patch
Patch236: 0036-rt-Provide-PREEMPT_RT_BASE-config-switch.patch
Patch237: 0037-cpumask-Disable-CONFIG_CPUMASK_OFFSTACK-for-RT.patch
Patch238: 0038-jump-label-disable-if-stop_machine-is-used.patch
Patch239: 0039-kconfig-Disable-config-options-which-are-not-RT-comp.patch
Patch240: 0040-lockdep-disable-self-test.patch
Patch241: 0041-mm-Allow-only-slub-on-RT.patch
Patch242: 0042-locking-Disable-spin-on-owner-for-RT.patch
Patch243: 0043-rcu-Disable-RCU_FAST_NO_HZ-on-RT.patch
Patch244: 0044-rcu-make-RCU_BOOST-default-on-RT.patch
Patch245: 0045-sched-Disable-CONFIG_RT_GROUP_SCHED-on-RT.patch
Patch246: 0046-net-core-disable-NET_RX_BUSY_POLL.patch
Patch247: 0047-arm-disable-NEON-in-kernel-mode.patch
Patch248: 0048-powerpc-Use-generic-rwsem-on-RT.patch
Patch249: 0049-powerpc-kvm-Disable-in-kernel-MPIC-emulation-for-PRE.patch
Patch250: 0050-powerpc-Disable-highmem-on-RT.patch
Patch251: 0051-mips-Disable-highmem-on-RT.patch
Patch252: 0052-x86-Use-generic-rwsem_spinlocks-on-rt.patch
Patch253: 0053-leds-trigger-disable-CPU-trigger-on-RT.patch
Patch254: 0054-cpufreq-drop-K8-s-driver-from-beeing-selected.patch
Patch255: 0055-md-disable-bcache.patch
Patch256: 0056-efi-Disable-runtime-services-on-RT.patch
Patch257: 0057-printk-Add-a-printk-kill-switch.patch
Patch258: 0058-printk-Add-force_early_printk-boot-param-to-help-wit.patch
Patch259: 0059-preempt-Provide-preempt_-_-no-rt-variants.patch
Patch260: 0060-futex-workaround-migrate_disable-enable-in-different.patch
Patch261: 0061-rt-Add-local-irq-locks.patch
Patch262: 0062-locallock-provide-get-put-_locked_ptr-variants.patch
Patch263: 0063-mm-scatterlist-Do-not-disable-irqs-on-RT.patch
Patch264: 0064-signal-x86-Delay-calling-signals-in-atomic.patch
Patch265: 0065-x86-signal-delay-calling-signals-on-32bit.patch
Patch266: 0066-buffer_head-Replace-bh_uptodate_lock-for-rt.patch
Patch267: 0067-fs-jbd-jbd2-Make-state-lock-and-journal-head-lock-rt.patch
Patch268: 0068-list_bl-Make-list-head-locking-RT-safe.patch
Patch269: 0069-list_bl-fixup-bogus-lockdep-warning.patch
Patch270: 0070-genirq-Disable-irqpoll-on-rt.patch
Patch271: 0071-genirq-Force-interrupt-thread-on-RT.patch
Patch272: 0072-Split-IRQ-off-and-zone-lock-while-freeing-pages-from.patch
Patch273: 0073-Split-IRQ-off-and-zone-lock-while-freeing-pages-from.patch
Patch274: 0074-mm-SLxB-change-list_lock-to-raw_spinlock_t.patch
Patch275: 0075-mm-SLUB-delay-giving-back-empty-slubs-to-IRQ-enabled.patch
Patch276: 0076-mm-page_alloc-rt-friendly-per-cpu-pages.patch
Patch277: 0077-mm-swap-Convert-to-percpu-locked.patch
Patch278: 0078-mm-perform-lru_add_drain_all-remotely.patch
Patch279: 0079-mm-vmstat-Protect-per-cpu-variables-with-preempt-dis.patch
Patch280: 0080-ARM-Initialize-split-page-table-locks-for-vector-pag.patch
Patch281: 0081-mm-Enable-SLUB-for-RT.patch
Patch282: 0082-slub-Enable-irqs-for-__GFP_WAIT.patch
Patch283: 0083-slub-Disable-SLUB_CPU_PARTIAL.patch
Patch284: 0084-mm-memcontrol-Don-t-call-schedule_work_on-in-preempt.patch
Patch285: 0085-mm-memcontrol-Replace-local_irq_disable-with-local-l.patch
Patch286: 0086-mm-zsmalloc-copy-with-get_cpu_var-and-locking.patch
Patch287: 0087-x86-mm-pat-disable-preemption-__split_large_page-aft.patch
Patch288: 0088-radix-tree-use-local-locks.patch
Patch289: 0089-timers-Prepare-for-full-preemption.patch
Patch290: 0090-x86-kvm-Require-const-tsc-for-RT.patch
Patch291: 0091-pci-switchtec-Don-t-use-completion-s-wait-queue.patch
Patch292: 0092-wait.h-include-atomic.h.patch
Patch293: 0093-work-simple-Simple-work-queue-implemenation.patch
Patch294: 0094-work-simple-drop-a-shit-statement-in-SWORK_EVENT_PEN.patch
Patch295: 0095-completion-Use-simple-wait-queues.patch
Patch296: 0096-fs-aio-simple-simple-work.patch
Patch297: 0097-time-hrtimer-avoid-schedule_work-with-interrupts-dis.patch
Patch298: 0098-hrtimer-consolidate-hrtimer_init-hrtimer_init_sleepe.patch
Patch299: 0099-hrtimers-Prepare-full-preemption.patch
Patch300: 0100-hrtimer-by-timers-by-default-into-the-softirq-contex.patch
Patch301: 0101-sched-fair-Make-the-hrtimers-non-hard-again.patch
Patch302: 0102-hrtimer-Move-schedule_work-call-to-helper-thread.patch
Patch303: 0103-hrtimer-move-state-change-before-hrtimer_cancel-in-d.patch
Patch304: 0104-posix-timers-Thread-posix-cpu-timers-on-rt.patch
Patch305: 0105-sched-Move-task_struct-cleanup-to-RCU.patch
Patch306: 0106-sched-Limit-the-number-of-task-migrations-per-batch.patch
Patch307: 0107-sched-Move-mmdrop-to-RCU-on-RT.patch
Patch308: 0108-kernel-sched-move-stack-kprobe-clean-up-to-__put_tas.patch
Patch309: 0109-sched-Add-saved_state-for-tasks-blocked-on-sleeping-.patch
Patch310: 0110-sched-Do-not-account-rcu_preempt_depth-on-RT-in-migh.patch
Patch311: 0111-sched-Use-the-proper-LOCK_OFFSET-for-cond_resched.patch
Patch312: 0112-sched-Disable-TTWU_QUEUE-on-RT.patch
Patch313: 0113-sched-workqueue-Only-wake-up-idle-workers-if-not-blo.patch
Patch314: 0114-rt-Increase-decrease-the-nr-of-migratory-tasks-when-.patch
Patch315: 0115-hotplug-Lightweight-get-online-cpus.patch
Patch316: 0116-trace-Add-migrate-disabled-counter-to-tracing-output.patch
Patch317: 0117-lockdep-Make-it-RT-aware.patch
Patch318: 0118-tasklet-Prevent-tasklets-from-going-into-infinite-sp.patch
Patch319: 0119-softirq-Check-preemption-after-reenabling-interrupts.patch
Patch320: 0120-softirq-Disable-softirq-stacks-for-RT.patch
Patch321: 0121-softirq-Split-softirq-locks.patch
Patch322: 0122-net-core-use-local_bh_disable-in-netif_rx_ni.patch
Patch323: 0123-genirq-Allow-disabling-of-softirq-processing-in-irq-.patch
Patch324: 0124-softirq-split-timer-softirqs-out-of-ksoftirqd.patch
Patch325: 0125-softirq-Avoid-local_softirq_pending-messages-if-ksof.patch
Patch326: 0126-softirq-Avoid-local_softirq_pending-messages-if-task.patch
Patch327: 0127-rtmutex-trylock-is-okay-on-RT.patch
Patch328: 0128-fs-nfs-turn-rmdir_sem-into-a-semaphore.patch
Patch329: 0129-rtmutex-Handle-the-various-new-futex-race-conditions.patch
Patch330: 0130-futex-Fix-bug-on-when-a-requeued-RT-task-times-out.patch
Patch331: 0131-futex-Ensure-lock-unlock-symetry-versus-pi_lock-and-.patch
Patch332: 0132-pid.h-include-atomic.h.patch
Patch333: 0133-arm-include-definition-for-cpumask_t.patch
Patch334: 0134-locking-locktorture-Do-NOT-include-rwlock.h-directly.patch
Patch335: 0135-rtmutex-Add-rtmutex_lock_killable.patch
Patch336: 0136-rtmutex-Make-lock_killable-work.patch
Patch337: 0137-spinlock-Split-the-lock-types-header.patch
Patch338: 0138-rtmutex-Avoid-include-hell.patch
Patch339: 0139-rbtree-don-t-include-the-rcu-header.patch
Patch340: 0140-rtmutex-Provide-rt_mutex_slowlock_locked.patch
Patch341: 0141-rtmutex-export-lockdep-less-version-of-rt_mutex-s-lo.patch
Patch342: 0142-rtmutex-add-sleeping-lock-implementation.patch
Patch343: 0143-rtmutex-add-mutex-implementation-based-on-rtmutex.patch
Patch344: 0144-rtmutex-add-rwsem-implementation-based-on-rtmutex.patch
Patch345: 0145-rtmutex-add-rwlock-implementation-based-on-rtmutex.patch
Patch346: 0146-rtmutex-rwlock-preserve-state-like-a-sleeping-lock.patch
Patch347: 0147-rtmutex-wire-up-RT-s-locking.patch
Patch348: 0148-rtmutex-add-ww_mutex-addon-for-mutex-rt.patch
Patch349: 0149-kconfig-Add-PREEMPT_RT_FULL.patch
Patch350: 0150-locking-rt-mutex-fix-deadlock-in-device-mapper-block.patch
Patch351: 0151-locking-rt-mutex-Flush-block-plug-on-__down_read.patch
Patch352: 0152-locking-rtmutex-re-init-the-wait_lock-in-rt_mutex_in.patch
Patch353: 0153-ptrace-fix-ptrace-vs-tasklist_lock-race.patch
Patch354: 0154-rtmutex-annotate-sleeping-lock-context.patch
Patch355: 0155-sched-migrate_disable-fallback-to-preempt_disable-in.patch
Patch356: 0156-locking-don-t-check-for-__LINUX_SPINLOCK_TYPES_H-on-.patch
Patch357: 0157-rcu-Frob-softirq-test.patch
Patch358: 0158-rcu-Merge-RCU-bh-into-RCU-preempt.patch
Patch359: 0159-rcu-Make-ksoftirqd-do-RCU-quiescent-states.patch
Patch360: 0160-rcu-Eliminate-softirq-processing-from-rcutree.patch
Patch361: 0161-srcu-use-cpu_online-instead-custom-check.patch
Patch362: 0162-srcu-replace-local_irqsave-with-a-locallock.patch
Patch363: 0163-rcu-enable-rcu_normal_after_boot-by-default-for-RT.patch
Patch364: 0164-tty-serial-omap-Make-the-locking-RT-aware.patch
Patch365: 0165-tty-serial-pl011-Make-the-locking-work-on-RT.patch
Patch366: 0166-tty-serial-pl011-explicitly-initialize-the-flags-var.patch
Patch367: 0167-rt-Improve-the-serial-console-PASS_LIMIT.patch
Patch368: 0168-tty-serial-8250-don-t-take-the-trylock-during-oops.patch
Patch369: 0169-locking-percpu-rwsem-Remove-preempt_disable-variants.patch
Patch370: 0170-mm-Protect-activate_mm-by-preempt_-disable-enable-_r.patch
Patch371: 0171-fs-dcache-bring-back-explicit-INIT_HLIST_BL_HEAD-ini.patch
Patch372: 0172-fs-dcache-disable-preemption-on-i_dir_seq-s-write-si.patch
Patch373: 0173-squashfs-make-use-of-local-lock-in-multi_cpu-decompr.patch
Patch374: 0174-thermal-Defer-thermal-wakups-to-threads.patch
Patch375: 0175-x86-fpu-Disable-preemption-around-local_bh_disable.patch
Patch376: 0176-fs-epoll-Do-not-disable-preemption-on-RT.patch
Patch377: 0177-mm-vmalloc-Another-preempt-disable-region-which-suck.patch
Patch378: 0178-block-mq-use-cpu_light.patch
Patch379: 0179-block-mq-do-not-invoke-preempt_disable.patch
Patch380: 0180-block-mq-don-t-complete-requests-via-IPI.patch
Patch381: 0181-md-raid5-Make-raid5_percpu-handling-RT-aware.patch
Patch382: 0182-rt-Introduce-cpu_chill.patch
Patch383: 0183-hrtimer-Don-t-lose-state-in-cpu_chill.patch
Patch384: 0184-hrtimer-cpu_chill-save-task-state-in-saved_state.patch
Patch385: 0185-block-blk-mq-move-blk_queue_usage_counter_release-in.patch
Patch386: 0186-block-Use-cpu_chill-for-retry-loops.patch
Patch387: 0187-fs-dcache-Use-cpu_chill-in-trylock-loops.patch
Patch388: 0188-net-Use-cpu_chill-instead-of-cpu_relax.patch
Patch389: 0189-fs-dcache-use-swait_queue-instead-of-waitqueue.patch
Patch390: 0190-workqueue-Use-normal-rcu.patch
Patch391: 0191-workqueue-Use-local-irq-lock-instead-of-irq-disable-.patch
Patch392: 0192-workqueue-Prevent-workqueue-versus-ata-piix-livelock.patch
Patch393: 0193-sched-Distangle-worker-accounting-from-rqlock.patch
Patch394: 0194-debugobjects-Make-RT-aware.patch
Patch395: 0195-seqlock-Prevent-rt-starvation.patch
Patch396: 0196-sunrpc-Make-svc_xprt_do_enqueue-use-get_cpu_light.patch
Patch397: 0197-net-Use-skbufhead-with-raw-lock.patch
Patch398: 0198-net-move-xmit_recursion-to-per-task-variable-on-RT.patch
Patch399: 0199-net-provide-a-way-to-delegate-processing-a-softirq-t.patch
Patch400: 0200-net-dev-always-take-qdisc-s-busylock-in-__dev_xmit_s.patch
Patch401: 0201-net-Qdisc-use-a-seqlock-instead-seqcount.patch
Patch402: 0202-net-add-back-the-missing-serialization-in-ip_send_un.patch
Patch403: 0203-net-add-a-lock-around-icmp_sk.patch
Patch404: 0204-net-Have-__napi_schedule_irqoff-disable-interrupts-o.patch
Patch405: 0205-irqwork-push-most-work-into-softirq-context.patch
Patch406: 0206-printk-Make-rt-aware.patch
Patch407: 0207-kernel-printk-Don-t-try-to-print-from-IRQ-NMI-region.patch
Patch408: 0208-printk-Drop-the-logbuf_lock-more-often.patch
Patch409: 0209-ARM-enable-irq-in-translation-section-permission-fau.patch
Patch410: 0210-genirq-update-irq_set_irqchip_state-documentation.patch
Patch411: 0211-KVM-arm-arm64-downgrade-preempt_disable-d-region-to-.patch
Patch412: 0212-arm64-fpsimd-use-preemp_disable-in-addition-to-local.patch
Patch413: 0213-kgdb-serial-Short-term-workaround.patch
Patch414: 0214-sysfs-Add-sys-kernel-realtime-entry.patch
Patch415: 0215-mm-rt-kmap_atomic-scheduling.patch
Patch416: 0216-x86-highmem-Add-a-already-used-pte-check.patch
Patch417: 0217-arm-highmem-Flush-tlb-on-unmap.patch
Patch418: 0218-arm-Enable-highmem-for-rt.patch
Patch419: 0219-scsi-fcoe-Make-RT-aware.patch
Patch420: 0220-x86-crypto-Reduce-preempt-disabled-regions.patch
Patch421: 0221-crypto-Reduce-preempt-disabled-regions-more-algos.patch
Patch422: 0222-crypto-limit-more-FPU-enabled-sections.patch
Patch423: 0223-crypto-scompress-serialize-RT-percpu-scratch-buffer-.patch
Patch424: 0224-crypto-cryptd-add-a-lock-instead-preempt_disable-loc.patch
Patch425: 0225-panic-skip-get_random_bytes-for-RT_FULL-in-init_oops.patch
Patch426: 0226-x86-stackprotector-Avoid-random-pool-on-rt.patch
Patch427: 0227-cpu-hotplug-Implement-CPU-pinning.patch
Patch428: 0228-sched-Allow-pinned-user-tasks-to-be-awakened-to-the-.patch
Patch429: 0229-hotplug-duct-tape-RT-rwlock-usage-for-non-RT.patch
Patch430: 0230-net-Remove-preemption-disabling-in-netif_rx.patch
Patch431: 0231-net-Another-local_irq_disable-kmalloc-headache.patch
Patch432: 0232-net-core-protect-users-of-napi_alloc_cache-against-r.patch
Patch433: 0233-net-netfilter-Serialize-xt_write_recseq-sections-on-.patch
Patch434: 0234-lockdep-selftest-Only-do-hardirq-context-test-for-ra.patch
Patch435: 0235-lockdep-selftest-fix-warnings-due-to-missing-PREEMPT.patch
Patch436: 0236-sched-Add-support-for-lazy-preemption.patch
Patch437: 0237-ftrace-Fix-trace-header-alignment.patch
Patch438: 0238-x86-Support-for-lazy-preemption.patch
Patch439: 0239-x86-lazy-preempt-properly-check-against-preempt-mask.patch
Patch440: 0240-x86-lazy-preempt-use-proper-return-label-on-32bit-x8.patch
Patch441: 0241-arm-Add-support-for-lazy-preemption.patch
Patch442: 0242-powerpc-Add-support-for-lazy-preemption.patch
Patch443: 0243-arch-arm64-Add-lazy-preempt-support.patch
Patch444: 0244-connector-cn_proc-Protect-send_msg-with-a-local-lock.patch
Patch445: 0245-drivers-block-zram-Replace-bit-spinlocks-with-rtmute.patch
Patch446: 0246-drivers-zram-Don-t-disable-preemption-in-zcomp_strea.patch
Patch447: 0247-drivers-zram-fix-zcomp_stream_get-smp_processor_id-u.patch
Patch448: 0248-tpm_tis-fix-stall-after-iowrite-s.patch
Patch449: 0249-watchdog-prevent-deferral-of-watchdogd-wakeup-on-RT.patch
Patch450: 0250-drm-radeon-i915-Use-preempt_disable-enable_rt-where-.patch
Patch451: 0251-drm-i915-Use-local_lock-unlock_irq-in-intel_pipe_upd.patch
Patch452: 0252-drm-i915-disable-tracing-on-RT.patch
Patch453: 0253-drm-i915-skip-DRM_I915_LOW_LEVEL_TRACEPOINTS-with-NO.patch
Patch454: 0254-cgroups-use-simple-wait-in-css_release.patch
Patch455: 0255-cpuset-Convert-callback_lock-to-raw_spinlock_t.patch
Patch456: 0256-apparmor-use-a-locallock-instead-preempt_disable.patch
Patch457: 0257-workqueue-Prevent-deadlock-stall-on-RT.patch
Patch458: 0258-signals-Allow-rt-tasks-to-cache-one-sigqueue-struct.patch
Patch459: 0259-Add-localversion-for-RT-release.patch
Patch460: 0260-powerpc-pseries-iommu-Use-a-locallock-instead-local_.patch
Patch461: 0261-powerpc-reshuffle-TIF-bits.patch
Patch462: 0262-tty-sysrq-Convert-show_lock-to-raw_spinlock_t.patch
Patch463: 0263-drm-i915-Don-t-disable-interrupts-independently-of-t.patch
Patch464: 0264-sched-completion-Fix-a-lockup-in-wait_for_completion.patch
Patch465: 0265-kthread-add-a-global-worker-thread.patch
Patch466: 0266-arm-imx6-cpuidle-Use-raw_spinlock_t.patch
Patch467: 0267-rcu-Don-t-allow-to-change-rcu_normal_after_boot-on-R.patch
Patch468: 0268-pci-switchtec-fix-stream_open.cocci-warnings.patch
Patch469: 0269-sched-core-Drop-a-preempt_disable_rt-statement.patch
Patch470: 0270-timers-Redo-the-notification-of-canceling-timers-on-.patch
Patch471: 0271-Revert-futex-Ensure-lock-unlock-symetry-versus-pi_lo.patch
Patch472: 0272-Revert-futex-Fix-bug-on-when-a-requeued-RT-task-time.patch
Patch473: 0273-Revert-rtmutex-Handle-the-various-new-futex-race-con.patch
Patch474: 0274-Revert-futex-workaround-migrate_disable-enable-in-di.patch
Patch475: 0275-futex-Make-the-futex_hash_bucket-lock-raw.patch
Patch476: 0276-futex-Delay-deallocation-of-pi_state.patch
Patch477: 0277-mm-zswap-Do-not-disable-preemption-in-zswap_frontswa.patch
Patch478: 0278-revert-aio.patch
Patch479: 0279-fs-aio-simple-simple-work.patch
Patch480: 0280-revert-thermal.patch
Patch481: 0281-thermal-Defer-thermal-wakups-to-threads.patch
Patch482: 0282-revert-block.patch
Patch483: 0283-block-blk-mq-move-blk_queue_usage_counter_release-in.patch
Patch484: 0284-workqueue-rework.patch
Patch485: 0285-i2c-exynos5-Remove-IRQF_ONESHOT.patch
Patch486: 0286-i2c-hix5hd2-Remove-IRQF_ONESHOT.patch
Patch487: 0287-sched-deadline-Ensure-inactive_timer-runs-in-hardirq.patch
Patch488: 0288-thermal-x86_pkg_temp-make-pkg_temp_lock-a-raw-spinlo.patch
Patch489: 0289-dma-buf-Use-seqlock_t-instread-disabling-preemption.patch
Patch490: 0290-KVM-arm-arm64-Let-the-timer-expire-in-hardirq-contex.patch
Patch491: 0291-x86-preempt-Check-preemption-level-before-looking-at.patch
Patch492: 0292-hrtimer-Use-READ_ONCE-to-access-timer-base-in-hrimer.patch
Patch493: 0293-hrtimer-Don-t-grab-the-expiry-lock-for-non-soft-hrti.patch
Patch494: 0294-hrtimer-Prevent-using-hrtimer_grab_expiry_lock-on-mi.patch
Patch495: 0295-hrtimer-Add-a-missing-bracket-and-hide-migration_bas.patch
Patch496: 0296-posix-timers-Unlock-expiry-lock-in-the-early-return.patch
Patch497: 0297-sched-migrate_dis-enable-Use-sleeping_lock-to-annota.patch
Patch498: 0298-sched-__set_cpus_allowed_ptr-Check-cpus_mask-not-cpu.patch
Patch499: 0299-sched-Remove-dead-__migrate_disabled-check.patch
Patch500: 0300-sched-migrate-disable-Protect-cpus_ptr-with-lock.patch
Patch501: 0301-lib-smp_processor_id-Don-t-use-cpumask_equal.patch
Patch502: 0302-futex-Make-the-futex_hash_bucket-spinlock_t-again-an.patch
Patch503: 0303-locking-rtmutex-Clean-pi_blocked_on-in-the-error-cas.patch
Patch504: 0304-lib-ubsan-Don-t-seralize-UBSAN-report.patch
Patch505: 0305-kmemleak-Change-the-lock-of-kmemleak_object-to-raw_s.patch
Patch506: 0306-sched-migrate_enable-Use-select_fallback_rq.patch
Patch507: 0307-sched-Lazy-migrate_disable-processing.patch
Patch508: 0308-sched-migrate_enable-Use-stop_one_cpu_nowait.patch
Patch509: 0309-Revert-ARM-Initialize-split-page-table-locks-for-vec.patch
Patch510: 0310-locking-Make-spinlock_t-and-rwlock_t-a-RCU-section-o.patch
Patch511: 0311-sched-core-migrate_enable-must-access-takedown_cpu_t.patch
Patch512: 0312-lib-smp_processor_id-Adjust-check_preemption_disable.patch
Patch513: 0313-sched-migrate_enable-Busy-loop-until-the-migration-r.patch
Patch514: 0314-userfaultfd-Use-a-seqlock-instead-of-seqcount.patch
Patch515: 0315-sched-migrate_enable-Use-per-cpu-cpu_stop_work.patch
Patch516: 0316-sched-migrate_enable-Remove-__schedule-call.patch
Patch517: 0317-mm-memcontrol-Move-misplaced-local_unlock_irqrestore.patch
Patch518: 0318-locallock-Include-header-for-the-current-macro.patch
Patch519: 0319-drm-vmwgfx-Drop-preempt_disable-in-vmw_fifo_ping_hos.patch
Patch520: 0320-tracing-make-preempt_lazy-and-migrate_disable-counte.patch
Patch521: 0321-lib-ubsan-Remove-flags-parameter-from-calls-to-ubsan.patch
Patch522: 0322-irq_work-Fix-checking-of-IRQ_WORK_LAZY-flag-set-on-n.patch
Patch523: 0323-tasklet-Address-a-race-resulting-in-double-enqueue.patch
Patch524: 0324-hrtimer-fix-logic-for-when-grabbing-softirq_expiry_l.patch
Patch525: 0325-fs-dcache-Include-swait.h-header.patch
Patch526: 0326-mm-slub-Always-flush-the-delayed-empty-slubs-in-flus.patch
Patch527: 0327-tasklet-Fix-UP-case-for-tasklet-CHAINED-state.patch
Patch528: 0328-signal-Prevent-double-free-of-user-struct.patch
Patch529: 0329-Bluetooth-Acquire-sk_lock.slock-without-disabling-in.patch
Patch530: 0330-net-phy-fixed_phy-Remove-unused-seqcount.patch
Patch531: 0331-net-xfrm-fix-compress-vs-decompress-serialization.patch
Patch532: 0332-mm-memcontrol-Disable-preemption-in-__mod_memcg_lruv.patch
Patch533: 0333-ptrace-fix-ptrace_unfreeze_traced-race-with-rt-lock.patch
Patch534: 0334-mm-slub-Don-t-resize-the-location-tracking-cache-on-.patch
Patch535: 0335-locking-rwsem_rt-Add-__down_read_interruptible.patch
Patch536: 0336-locking-rwsem-rt-Remove-might_sleep-in-__up_read.patch
Patch537: 0337-fscache-fix-initialisation-of-cookie-hash-table-raw-.patch
Patch538: 0338-rt-PREEMPT_RT-safety-net-for-backported-patches.patch
Patch539: 0339-net-Add-missing-xmit_lock_owner-hunks.patch
Patch540: 0340-genirq-Add-lost-hunk-to-irq_forced_thread_fn.patch
Patch541: 0341-random-Use-local-locks-for-crng-context-access.patch
# Keep rt_version matched up with this patch.
Patch542: 0342-Linux-4.19.255-rt113-REBASE.patch

#Ignore reading localversion-rt
Patch599: 0001-setlocalversion-Skip-reading-localversion-rt-file.patch

#Photon Specific Changes
Patch600: 0000-Revert-clockevents-Stop-unused-clockevent-devices.patch
#RT Runtine Greed changes
Patch601: 0001-sched-rt-Disable-RT_RUNTIME_SHARE-by-default.patch
Patch602: 0002-RT-PATCH-sched-rt-RT_RUNTIME_GREED-sched-feature.patch
#Patchset to reduce timer softirqs
#https://lore.kernel.org/lkml/20200717140551.29076-1-frederic@kernel.org/
Patch603: 0001-timers-Preserve-higher-bits-of-expiration-on-index-c.patch
Patch604: 0002-timers-Use-only-bucket-expiry-for-base-next_expiry-v.patch
Patch605: 0003-timers-Move-trigger_dyntick_cpu-to-enqueue_timer.patch
Patch606: 0004-timers-Add-comments-about-calc_index-ceiling-work.patch
Patch607: 0005-timers-Optimize-_next_timer_interrupt-level-iteratio.patch
Patch608: 0006-timers-Always-keep-track-of-next-expiry.patch
Patch609: 0007-timers-Reuse-next-expiry-cache-after-nohz-exit.patch
Patch610: 0008-timers-Expand-clk-forward-logic-beyond-nohz.patch
Patch611: 0009-timers-Spare-timer-softirq-until-next-expiry.patch
Patch612: 0010-timers-Remove-must_forward_clk.patch
Patch613: 0011-timers-Lower-base-clock-forwarding-threshold.patch

# Patchset to conditional restart_tick upon idle_exit
# https://lore.kernel.org/lkml/162091184942.29796.4815200413212139734.tip-bot2@tip-bot2/
Patch615: 0001-tick-nohz-Evaluate-the-CPU-expression-after-the-stat.patch
Patch616: 0002-tick-nohz-Conditionally-restart-tick-on-idle-exit.patch
Patch617: 0003-tick-nohz-Remove-superflous-check-for-CONFIG_VIRT_CP.patch
Patch618: 0004-tick-nohz-Update-idle_exittime-on-actual-idle-exit.patch
Patch619: 0005-tick-nohz-Update-nohz_full-Kconfig-help.patch
Patch620: 0006-tick-nohz-Only-wakeup-a-single-target-cpu-when-kicki.patch
Patch621: 0007-tick-nohz-Change-signal-tick-dependency-to-wakeup-CP.patch
Patch622: 0008-tick-nohz-Kick-only-_queued_-task-whose-tick-depende.patch
Patch623: 0009-tick-nohz-Call-tick_nohz_task_switch-with-interrupts.patch
Patch624: 0010-MAINTAINERS-Add-myself-as-context-tracking-maintaine.patch

#Patch to enable nohz with idle=poll
Patch625: 0001-Allow-tick-sched-timer-to-be-turned-off-in-idle-poll.patch

#Patch to add timer padding on guest
Patch626: 0001-timer-padding-on-guest.patch

# Disable md5 algorithm for sctp if fips is enabled.
Patch630: 0001-disable-md5-algorithm-for-sctp-if-fips-is-enabled.patch

# Fix for CVE-2021-4204
Patch633: 0002-bpf-Disallow-unprivileged-bpf-by-default.patch

# Backport hrtick changes
Patch634: 0001-sched-Mark-hrtimers-to-expire-in-hard-interrupt-cont.patch
Patch635: 0002-sched-features-Fix-hrtick-reprogramming.patch
Patch636: 0003-sched-features-Distinguish-between-NORMAL-and-DEADLI.patch

%if 0%{?kat_build}
Patch1000: fips-kat-tests.patch
%endif

#Patches for i40e driver
Patch1500: 0001-Add-support-for-gettimex64-interface.patch

#Patches for iavf driver
Patch1511: 0001-iavf-Use-PTP_SYS_OFFSET_EXTENDED_IOCTL-support.patch
Patch1512: no-aux-symvers.patch

#Patches for ice driver
Patch1521: 0001-ice-Use-PTP_SYS_OFFSET_EXTENDED_IOCTL-support.patch
Patch1522: no-aux-bus.patch

BuildArch: x86_64

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

Requires:       filesystem
Requires:       kmod
Requires(pre): (coreutils or toybox)
Requires(preun): (coreutils or toybox)
Requires(post): (coreutils or toybox)
Requires(postun): (coreutils or toybox)

%description
The Linux package contains the Linux kernel with RT (real-time)
features.
Built with rt patchset version %{rt_version}.

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
%setup -q -T -D -b 8 -n linux-%{version}
# Using autosetup is not feasible
%setup -q -T -D -b 9 -n linux-%{version}
%endif

# ApplyPatch.inc
%include %{SOURCE10}

ApplyPatch "0" "636"

%if 0%{?kat_build}
%patch1000 -p1
%endif

#Patches for i40e driver
pushd ../i40e-%{i40e_version}
%patch1500 -p1
popd

#Patches for iavf driver
pushd ../iavf-%{iavf_version}
ApplyPatch "1511" "1512"
popd

#Patches for ice driver
pushd ../ice-%{ice_version}
ApplyPatch "1521" "1522"
popd

%build
make mrproper %{?_smp_mflags}

%ifarch x86_64
cp %{SOURCE1} .config
arch="x86_64"
%endif

sed -i 's/CONFIG_LOCALVERSION="-rt"/CONFIG_LOCALVERSION="-%{release}-rt"/' .config

%include %{SOURCE5}

make VERBOSE=1 KBUILD_BUILD_VERSION="1-photon" \
        KBUILD_BUILD_HOST="photon" ARCH=${arch} %{?_smp_mflags}

bldroot="${PWD}"

%ifarch x86_64

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

%define __modules_install_post \
for MODULE in $(find %{buildroot}%{_modulesdir} -name *.ko); do \
  ./scripts/sign-file sha512 certs/signing_key.pem certs/signing_key.x509 $MODULE \
  rm -f $MODULE.{sig,dig} \
  xz $MODULE \
  done \
%{nil}

# We want to compress modules after stripping. Extra step is added to
# the default __spec_install_post.
%define __spec_install_post \
  %{?__debug_package:%{__debug_install_post}} \
  %{__arch_install_post} \
  %{__os_install_post} \
  %{__modules_install_post} \
%{nil}

%install
%ifarch x86_64
archdir="x86"
%endif

install -vdm 755 %{buildroot}%{_sysconfdir}
install -vdm 755 %{buildroot}/boot
install -vdm 755 %{buildroot}%{_defaultdocdir}/linux-%{uname_r}
install -vdm 755 %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}
install -vdm 755 %{buildroot}%{_libdir}/debug/%{_modulesdir}
make INSTALL_MOD_PATH=%{buildroot} modules_install %{?_smp_mflags}

bldroot="${PWD}"

%ifarch x86_64

# install i40e module
pushd ../i40e-%{i40e_version}
make -C src KSRC=${bldroot} INSTALL_MOD_PATH=%{buildroot} \
        INSTALL_MOD_DIR=extra MANDIR=%{_mandir} \
        modules_install mandocs_install %{?_smp_mflags}
popd

# install iavf module
pushd ../iavf-%{iavf_version}
# The auxiliary.ko kernel module is a common dependency for both iavf
# and ice drivers.  Install it only once, along with the iavf driver
# and re-use it in the ice driver.
make -C src KSRC=${bldroot} INSTALL_MOD_PATH=%{buildroot} \
                 INSTALL_MOD_DIR=extra INSTALL_AUX_DIR=extra \
                 MANDIR=%{_mandir} modules_install \
                 mandocs_install %{?_smp_mflags}

install -Dvm 644 src/linux/auxiliary_bus.h \
        %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}/include/linux/auxiliary_bus.h
popd

# install ice module
pushd ../ice-%{ice_version}
# The auxiliary.ko kernel module is a common dependency for both iavf
# and ice drivers.  Install it only once, along with the iavf driver
# and re-use it in the ice driver.
make -C src KSRC=${bldroot} INSTALL_MOD_PATH=%{buildroot} \
                INSTALL_MOD_DIR=extra MANDIR=%{_mandir} \
                modules_install mandocs_install %{?_smp_mflags}
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

cp -r Documentation/* %{buildroot}%{_defaultdocdir}/linux-%{uname_r}

%if 0%{?__debug_package}
install -vm 644 vmlinux %{buildroot}%{_libdir}/debug/%{_modulesdir}/vmlinux-%{uname_r}
# `perf test vmlinux` needs it
ln -s vmlinux-%{uname_r} %{buildroot}%{_libdir}/debug/%{_modulesdir}/vmlinux
%endif

cat > %{buildroot}/boot/linux-%{uname_r}.cfg << "EOF"
# GRUB Environment Block
photon_cmdline=init=/lib/systemd/systemd ro loglevel=3 quiet no-vmw-sta nosoftlockup intel_idle.max_cstate=0 mce=ignore_ce nowatchdog cpuidle.off=1 nmi_watchdog=0 audit=0 cgroup.memory=nokmem
photon_linux=vmlinuz-%{uname_r}
photon_initrd=initrd.img-%{uname_r}
EOF

# Register myself to initramfs
mkdir -p %{buildroot}%{_sharedstatedir}/initramfs/kernel
cat > %{buildroot}%{_sharedstatedir}/initramfs/kernel/%{uname_r} << "EOF"
--add-drivers "cn dm-mod megaraid_sas"
EOF

# Cleanup dangling symlinks
rm -rf %{buildroot}%{_modulesdir}/source \
       %{buildroot}%{_modulesdir}/build

find . -name Makefile* -o -name Kconfig* -o -name *.pl | xargs sh -c 'cp --parents "$@" %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}' copy

find arch/${archdir}/include include scripts -type f | xargs sh -c 'cp --parents "$@" %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}' copy

find $(find arch/${archdir} -name include -o -name scripts -type d) -type f | xargs sh -c 'cp --parents "$@" %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}' copy

find arch/${archdir}/include Module.symvers include scripts -type f | xargs sh -c 'cp --parents "$@" %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}' copy

%ifarch x86_64
# CONFIG_STACK_VALIDATION=y requires objtool to build external modules
install -vsm 755 tools/objtool/objtool %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}/tools/objtool/
install -vsm 755 tools/objtool/fixdep %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}/tools/objtool/
%endif

# copy .config manually to be where it's expected to be
cp .config %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}

ln -sf "%{_usrsrc}/linux-headers-%{uname_r}" "%{buildroot}%{_modulesdir}/build"
find %{buildroot}/lib/modules -name '*.ko' -print0 | xargs -0 chmod u+x

%include %{SOURCE2}
%include %{SOURCE4}

%post
/sbin/depmod -a %{uname_r}
ln -sf linux-%{uname_r}.cfg /boot/photon.cfg

%files
%defattr(-,root,root)
/boot/System.map-%{uname_r}
/boot/config-%{uname_r}
/boot/vmlinuz-%{uname_r}
%config(noreplace) /boot/linux-%{uname_r}.cfg
%config %{_sharedstatedir}/initramfs/kernel/%{uname_r}
%defattr(0644,root,root)
%{_modulesdir}/*
%exclude %{_modulesdir}/build
%{_sysconfdir}/modprobe.d/iavf.conf
# ICE driver firmware files are packaged in linux-firmware
%exclude /lib/firmware/updates/intel/ice

%files docs
%defattr(-,root,root)
%{_defaultdocdir}/linux-%{uname_r}/*
%{_mandir}/*

%files devel
%defattr(-,root,root)
%{_modulesdir}/build
%{_usrsrc}/linux-headers-%{uname_r}

%changelog
* Tue Sep 06 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.256-2
- Backport netfilter patch to allow checking if dst has xfrm attached.
* Tue Aug 30 2022 Brennan Lamoreaux <blamoreaux@vmware.com> 4.19.256-1
- Update to version 4.19.256
* Tue Aug 16 2022 Shivani Agarwal <shivania2@vmware.com> 4.19.247-14
- .config: Enable MPLS and other routing related options, namely,
- CGROUP_BPF, XFRM_INTERFACE, NETFILTER_XT_TARGET_NOTRACK
- NET_ACT_BPF, MPLS_ROUTING, MPLS_IPTUNNEL, LWTUNNEL, LWTUNNEL_BPF, PPP
* Fri Aug 05 2022 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.247-13
- Fix for CVE-2022-2586 and CVE-2022-2588
* Wed Aug 03 2022 Shreenidhi Shedi <sshedi@vmware.com> 4.19.247-12
- Scriptlets fixes and improvements
* Wed Aug 03 2022 Keerthana K <keerthanak@vmware.com> 4.19.247-11
- Fix linux headers, doc folder and linux-<uname -r>.cfg names
- Drop rt_version from uname_r
- Patch to skip reading localversion-rt
* Tue Aug 02 2022 Sharan Turlapati <sturlapati@vmware.com> 4.19.247-10
- Revert napi reschedule on rx in vmxnet3 driver
* Tue Aug 02 2022 Ankit Jain <ankitja@vmware.com> 4.19.247-9
- Fix BUG_ON for deboosted tasks
* Tue Jul 12 2022 Ankit Jain <ankitja@vmware.com> 4.19.247-8
- Backported the fix for CVE-2022-1789
* Wed Jul 06 2022 Shreenidhi Shedi <sshedi@vmware.com> 4.19.247-7
- Spec improvements
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
- Enable config_livepatch
* Tue Jun 14 2022 Ajay Kaher <akaher@vmware.com> 4.19.247-1
- Update to version 4.19.247
* Fri Jun 10 2022 Alexey Makhalov <amakhalov@vmware.com> 4.19.245-3
- .config: enable CROSS_MEMORY_ATTACH
- Add elfutils-libelf-devel required to build objtool
* Tue May 31 2022 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.245-2
- Patch for timer padding on guest
* Thu May 26 2022 Sharan Turlapati <sturlapati@vmware.com> 4.19.245-1
- Update to version 4.19.245
* Mon May 16 2022 Brennan Lamoreaux <blamoreaux@vmware.com> 4.19.241-4
- Fix for CVE-2022-1048
* Mon May 16 2022 Sharan Turlapati <sturlapati@vmware.com> 4.19.241-3
- Backport hrtick changes to fix lost timer wakeups
* Thu May 12 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.241-2
- .config: Enable CONFIG_NFT_CHAIN_ROUTE_IPV4, CONFIG_NFT_CHAIN_NAT_IPV4,
- CONFIG_NFT_MASQ_IPV4 and CONFIG_NFT_REDIR_IPV4
* Wed May 11 2022 Brennan Lamoreaux <blamoreaux@vmware.com> 4.19.241-1
- Update to version 4.19.241
* Wed May 11 2022 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.240-2
- Add vhost and vhost-net drivers in config
* Fri Apr 29 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 4.19.240-1
- Update to version 4.19.240
- Fix CVE-2022-1055
* Mon Mar 21 2022 Ajay Kaher <akaher@vmware.com> 4.19.232-2
- Fix for CVE-2022-1016
* Mon Mar 07 2022 srinidhira0 <srinidhir@vmware.com> 4.19.232-1
- Update to version 4.19.232
* Tue Feb 15 2022 Alexey Makhalov <amakhalov@vmware.com> 4.19.229-2
- .config: enable zstd compression for squashfs.
- .config: enable crypto user api rng.
* Sat Feb 12 2022 Sharan Turlapati <sturlapati@vmware.com> 4.19.229-1
- Update to version 4.19.229
* Fri Feb 11 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.225-7
- Add support for eBPF packet filter.
* Fri Feb 11 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.225-6
- .config: Enable CONFIG_NET_ACT_SIMP and CONFIG_NET_ACT_BPF
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
* Mon Dec 20 2021 Harinadh D <hdommaraju@vmware.com> 4.19.219-4
- remove lvm in add-drivers list
- lvm drivers are built as part of dm-mod
* Wed Dec 15 2021 Alexey Makhalov <amakhalov@vmware.com> 4.19.219-3
- mm: fix percpu alloacion for memoryless nodes
- pvscsi: fix disk detection issue
* Tue Dec 14 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.219-2
- Fix for CVE-2020-36385
* Wed Dec 08 2021 srinidhira0 <srinidhir@vmware.com> 4.19.219-1
- Update to version 4.19.219
* Wed Nov 24 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.217-1
- Update to version 4.19.217
* Thu Nov 11 2021 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.214-3
- .config: Enable CONFIG_INTEL_RDT
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
* Wed Jul 21 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.191-5
- Revert patch that is causing regression in cyclictest
* Thu Jul 15 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.191-4
- Fix for CVE-2021-33909
* Tue Jun 22 2021 Sharan Turlapati <sturlapati@vmware.com> 4.19.191-3
- Fix for CVE-2021-3609
* Wed Jun 09 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.191-2
- Enable nohz for idle=poll
* Thu Jun 03 2021 Keerthana K <keerthanak@vmware.com> 4.19.191-1
- Update to version 4.19.191
- Remove XR usb driver support
- .config: Enable CONFIG_FANOTIFY_ACCESS_PERMISSIONS
* Wed Jun 02 2021 Keerthana K <keerthanak@vmware.com> 4.19.190-5
- Fix for CVE-2021-3573
* Wed May 26 2021 Ankit Jain <ankitja@vmware.com> 4.19.190-4
- Conditional tick_restart upon idle_exit
* Wed May 26 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.190-3
- Backport patchset to to reduce timer softirqs
* Thu May 20 2021 Ajay Kaher <akaher@vmware.com> 4.19.190-2
- Fix for CVE-2021-3564
* Mon May 17 2021 Ajay Kaher <akaher@vmware.com> 4.19.190-1
- Update to version 4.19.190
* Wed May 12 2021 Sharan Turlapati <sturlapati@vmware.com> 4.19.189-4
- Fix for CVE-2021-23133
* Fri May 07 2021 Ankit Jain <ankitja@vmware.com> 4.19.189-3
- .config: Enable INFINIBAND, MLX5_INFINIBAND
* Tue May 04 2021 Sharan Turlapati <sturlapati@vmware.com> 4.19.189-2
- Remove buf_info from device accessible structures in vmxnet3
* Thu Apr 29 2021 Ankit Jain <ankitja@vmware.com> 4.19.189-1
- Update to version 4.19.189
* Tue Apr 20 2021 Ankit Jain <ankitja@vmware.com> 4.19.186-3
- Fix for CVE-2021-3444
* Mon Apr 19 2021 Sharan Turlapati <sturlapati@vmware.com> 4.19.186-2
- Fix for CVE-2021-23133
* Tue Apr 13 2021 srinidhira0 <srinidhir@vmware.com> 4.19.186-1
- Update to version 4.19.186
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
* Fri Feb 19 2021 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.174-4
- Fix /boot/photon.cfg symlink when /boot is a separate partition.
* Thu Feb 11 2021 Ankit Jain <ankitja@vmware.com> 4.19.174-3
- Added latest out of tree version of Intel ice driver
* Thu Feb 11 2021 Vikash Bansal <bvikas@vmware.com> 4.19.174-2
- Added support for RT RUNTIME GREED
* Tue Feb 09 2021 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.174-1
- Update to version 4.19.174
* Mon Jan 04 2021 Ankit Jain <ankitja@vmware.com> 4.19.164-1
- Update to version 4.19.164
* Tue Dec 15 2020 Vikash Bansal <bvikas@vmware.com> 4.19.163-1
- Update to version 4.19.163
* Thu Dec 10 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.160-4
- Add latest out of tree version of iavf driver
- Enable CONFIG_NET_TEAM
* Wed Dec 09 2020 Srinidhi Rao <srinidhir@vmware.com> 4.19.160-3
- Fix for CVE-2019-19770
* Tue Dec 08 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.160-2
- Change PTP_SYS_OFFSET_EXTENDED IOCTL to _IOWR
* Tue Nov 24 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.160-1
- Update to version 4.19.160
- Fix CVE-2019-19338 and CVE-2019-20908
* Fri Nov 13 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.154-8
- Fix CVE-2020-25668
* Fri Nov 13 2020 Sharan Turlapati <sturlapati@vmware.com> 4.19.154-7
- Upgrade RT patchset version to -rt65
* Thu Nov 12 2020 Sharan Turlapati <sturlapati@vmware.com> 4.19.154-6
- Enable CONFIG_IFB
* Tue Nov 10 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.154-5
- Add support for PTP_SYS_OFFSET_EXTENDED ioctl
- Update i40e out-of-tree driver to version 2.13.10
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
* Tue Oct 06 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.148-3
- Fix IPIP encapsulation issue in vmxnet3 driver.
* Thu Oct 01 2020 Bo Gan <ganb@vmware.com> 4.19.148-2
- Revert d254087 (clockevents: Stop unused clockevent devices)
- Solve cyclictest regression introduced in 4.1
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
* Mon Sep 07 2020 Vikash Bansal <bvikas@vmware.com> 4.19.138-2
- Fix for CVE-2020-14386
* Thu Aug 13 2020 ashwin-h <ashwinh@vmware.com> 4.19.138-1
- Update to version 4.19.138
* Wed Aug 12 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.132-5
- Increment release number to enable kernel signing (for secure boot).
* Wed Aug 05 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.132-4
- Enable config options needed to build N3000 FPGA driver.
* Tue Aug 04 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.132-3
- Ugrade vmxnet3 driver to version 4
* Sun Jul 26 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.132-2
- Fix CVE-2020-14331
* Thu Jul 16 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.132-1
- Introduce a new kernel flavor 'linux-rt' supporting real-time (RT) features.
