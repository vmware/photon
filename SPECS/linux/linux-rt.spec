%global security_hardening none

%ifarch x86_64
%define arch x86_64
%define archdir x86
%endif

Summary:        Kernel
Name:           linux-rt
Version:        4.19.305
Release:        5%{?kat_build:.%kat}%{?dist}
License:        GPLv2
URL:            http://www.kernel.org
Group:          System Environment/Kernel
Vendor:         VMware, Inc.
Distribution:   Photon

# Keep rt_version matched up with REBASE.patch
%define rt_version rt131
%define uname_r %{version}-%{release}-rt
%define _modulesdir /lib/modules/%{uname_r}

Source0: http://www.kernel.org/pub/linux/kernel/v4.x/linux-%{version}.tar.xz
%define sha512 linux=2e9b2f90ff5f6fbc3a0b32dd57620e917b6b004bbefe319e72ffe1ac9ede95fcf87d03bfed73114327a71cfcec6612888d4947922f4ec8d88deea4554b4b579c

%ifarch x86_64
Source1: config-rt
%endif
Source2: initramfs.trigger
# contains pre, postun, filetriggerun tasks
Source4: scriptlets.inc
Source5: check_for_config_applicability.inc
# Real-Time kernel (PREEMPT_RT patches)
# Source: https://cdn.kernel.org/pub/linux/kernel/projects/rt/4.19/
Source6: preempt_rt.patches

%ifarch x86_64
# Specific versions of Intel's i40e, iavf and ice drivers.

%define i40e_version_2_23_17 2.23.17
Source7: https://sourceforge.net/projects/e1000/files/i40e%20stable/%{i40e_version_2_23_17}/i40e-%{i40e_version_2_23_17}.tar.gz
%define sha512 i40e-2.23.17=5dbe5186f23d14aac185f74283377d9bfc0837ab16b145a107f735d5439a207e27db871e278656cd06ba595f426d7095a294d39110df5ad6b30ea9f6d3a2a3a7

%define i40e_version_2_22_18 2.22.18
Source8: https://sourceforge.net/projects/e1000/files/i40e%20stable/%{i40e_version_2_22_18}/i40e-%{i40e_version_2_22_18}.tar.gz
%define sha512 i40e-2.22.18=042fd064528cb807894dc1f211dcb34ff28b319aea48fc6dede928c93ef4bbbb109bdfc903c27bae98b2a41ba01b7b1dffc3acac100610e3c6e95427162a26ac

%define i40e_version_2_16_11 2.16.11
Source9: https://sourceforge.net/projects/e1000/files/i40e%20stable/%{i40e_version_2_16_11}/i40e-%{i40e_version_2_16_11}.tar.gz
%define sha512 i40e-2.16.11=004ec7da665cde30142807c51e4351d041a6df906325ad9e97a01868d1b019e1c9178ea58901e0c2dbbec69a9e00b897a9ecfd116a6d4acf3c7ab87962e2a0aa

%define i40e_version_2_15_9 2.15.9
Source10: https://sourceforge.net/projects/e1000/files/i40e%20stable/%{i40e_version_2_15_9}/i40e-%{i40e_version_2_15_9}.tar.gz
%define sha512 i40e-2.15.9=891723116fca72c51851d7edab0add28c2a0b4c4768a7646794c8b3bc4d44a1786115e67f05cfa5bb3bc484a4e07145fc4640a621f3bc755cc07257b1b531dd5

%define iavf_version_4_9_5 4.9.5
Source11: https://sourceforge.net/projects/e1000/files/iavf%20stable/%{iavf_version_4_9_5}/iavf-%{iavf_version_4_9_5}.tar.gz
%define sha512 iavf-4.9.5=2e97671d1fd51b5b0017b49dcfa62854ef55a85182fcd4990d2d7faea0c3dc9532fe3896c81eabff3c30fb3b2b9573c22416adfec3a1e0f0107c44a9216fbf3a

%define iavf_version_4_9_1 4.9.1
Source12: https://sourceforge.net/projects/e1000/files/iavf%20stable/%{iavf_version_4_9_1}/iavf-%{iavf_version_4_9_1}.tar.gz
%define sha512 iavf-4.9.1=6a52b06373eda09824fc2674ce5a5ff488dc86331c9022faf2857c38a3002a969c6bb039271fc31e70310589701ac65d57d310d08459aa3402acbec9af1f7683

%define iavf_version_4_8_2 4.8.2
Source13: https://sourceforge.net/projects/e1000/files/iavf%20stable/%{iavf_version_4_8_2}/iavf-%{iavf_version_4_8_2}.tar.gz
%define sha512 iavf-4.8.2=5406b86e61f6528adfd7bc3a5f330cec8bb3b4d6c67395961cc6ab78ec3bd325c3a8655b8f42bf56fb47c62a85fb7dbb0c1aa3ecb6fa069b21acb682f6f578cf

%define iavf_version_4_5_3 4.5.3
Source14: https://sourceforge.net/projects/e1000/files/iavf%20stable/%{iavf_version_4_5_3}/iavf-%{iavf_version_4_5_3}.tar.gz
%define sha512 iavf-4.5.3=573b6b92ff7d8ee94d1ec01c56b990063c98c6f785a5fb96db30cf9c3fac4ff64277500b8468210464df343831818f576dd97cd172193491e3d47fec146c43fa

%define iavf_version_4_4_2 4.4.2
Source15: https://sourceforge.net/projects/e1000/files/iavf%20stable/%{iavf_version_4_4_2}/iavf-%{iavf_version_4_4_2}.tar.gz
%define sha512 iavf-4.4.2=6eb5123cee389dd4af71a7e151b6a9fd9f8c47d91b9e0e930ef792d2e9bea6efd01d7599fbc9355bb1a3f86e56d17d037307d7759a13c9f1a8f3e007534709e5

%define iavf_version_4_2_7 4.2.7
Source16: https://sourceforge.net/projects/e1000/files/iavf%20stable/%{iavf_version_4_2_7}/iavf-%{iavf_version_4_2_7}.tar.gz
%define sha512 iavf-4.2.7=1f491d9ab76444db1d5f0edbd9477eb3b15fa75f73785715ff8af31288b0490c01b54cc50b6bac3fc36d9caf25bae94fb4ef4a7e73d4360c7031ece32d725e70

%define ice_version_1_13_7 1.13.7
Source17: https://sourceforge.net/projects/e1000/files/ice%20stable/%{ice_version_1_13_7}/ice-%{ice_version_1_13_7}.tar.gz
%define sha512 ice-1.13.7=6167a0240624915ee6dce8f2186d6980c224baab8bcccee2b1d991d5cc15510b95b7b2a309cc60e57eae7dfffc4e2186730650ba104a231e54711c3b01f20f7b

%define ice_version_1_12_7 1.12.7
Source18: https://sourceforge.net/projects/e1000/files/ice%20stable/%{ice_version_1_12_7}/ice-%{ice_version_1_12_7}.tar.gz
%define sha512 ice-1.12.7=71b08c90ee6c03242b0b11eef2425ec55fe089fa7735cc5ae9bae7469e14768b67505315a456e98b0b09ce0be71ffd35f119f2df211b927265f4d4eb8cbdf60b

%define ice_version_1_11_14 1.11.14
Source19: https://sourceforge.net/projects/e1000/files/ice%20stable/%{ice_version_1_11_14}/ice-%{ice_version_1_11_14}.tar.gz
%define sha512 ice-1.11.14=a2a6a498e553d41e4e6959a19cdb74f0ceff3a7dbcbf302818ad514fdc18e3d3b515242c88d55ef8a00c9d16925f0cd8579cb41b3b1c27ea6716ccd7e70fd847

%define ice_version_1_9_11 1.9.11
Source20: https://sourceforge.net/projects/e1000/files/ice%20stable/%{ice_version_1_9_11}/ice-%{ice_version_1_9_11}.tar.gz
%define sha512 ice-1.9.11=4ca301ea7d190d74f2eebf148483db5e2482ca19ff0eaf1c3061c9550ab215d1b0ab12e1f6466fe6bccc889d2ddae47058043b3d8622fd90c2b29c545bbcd3fc

%define ice_version_1_8_3 1.8.3
Source21: https://sourceforge.net/projects/e1000/files/ice%20stable/%{ice_version_1_8_3}/ice-%{ice_version_1_8_3}.tar.gz
%define sha512 ice-1.8.3=b5fa544998b72b65c365489ddaf67dbb64e1b5127dace333573fc95a146a13147f13c5593afb4b9b3ce227bbd6757e3f3827fdf19c3cc1ba1f74057309c7d37b

%define ice_version_1_6_4 1.6.4
Source22: https://sourceforge.net/projects/e1000/files/ice%20stable/%{ice_version_1_6_4}/ice-%{ice_version_1_6_4}.tar.gz
%define sha512 ice-1.6.4=e88be3b416184d5c157aecda79b2580403b67c68286221ae154a92fa1d46cacd23aa55365994fa53f266d6df4ca2046cc2fcb35620345fd23e80b90a45ec173c
%endif

# common
Patch0: linux-4.14-Log-kmsg-dump-on-panic.patch
Patch1: double-tcp_mem-limits.patch
Patch3: SUNRPC-Do-not-reuse-srcport-for-TIME_WAIT-socket.patch
Patch4: SUNRPC-xs_bind-uses-ip_local_reserved_ports.patch
Patch5: vsock-transport-for-9p.patch
Patch6: 4.18-x86-vmware-STA-support.patch
Patch7: 9p-trans_fd-extend-port-variable-to-u32.patch
Patch9: vsock-delay-detach-of-QP-with-outgoing-data.patch
Patch10: 0001-cgroup-v1-cgroup_stat-support.patch
Patch11: Performance-over-security-model.patch

# Expose Photon kernel macros to identify kernel flavor and version
Patch12: 0001-kbuild-simplify-access-to-the-kernel-s-version.patch
Patch13: 0002-kbuild-Fix-linux-version.h-for-empty-SUBLEVEL-or-PAT.patch
Patch14: 0003-kbuild-replace-if-A-A-B-with-or-A-B.patch
Patch15: 0004-kbuild-Makefile-Introduce-macros-to-distinguish-Phot.patch
Patch16: 0005-linux-rt-Makefile-Add-kernel-flavor-info-to-the-gene.patch

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
# Fix for CVE-2024-0607
Patch37: 0001-netfilter-nf_tables-fix-pointer-math-issue-in.patch
# Fix for CVE-2019-12378
Patch38: 0001-ipv6_sockglue-Fix-a-missing-check-bug-in-ip6_ra_cont.patch
# Fix for CVE-2019-12455
Patch39: 0001-clk-sunxi-fix-a-missing-check-bug-in-sunxi_divs_clk_.patch
#Fix for CVE-2019-20908
Patch40: efi-Restrict-efivar_ssdt_load-when-the-kernel-is-locked-down.patch
#Fix for CVE-2019-19338
Patch41: 0001-KVM-vmx-implement-MSR_IA32_TSX_CTRL-disable-RTM-func.patch
Patch42: 0001-KVM-vmx-use-MSR_IA32_TSX_CTRL-to-hard-disable-TSX-on.patch
# Fix CVE-2024-0340
Patch43: 0001-vhost_use_kzalloc_instead_of_kmalloc.patch
#Fix for CVE-2024-0565
Patch44: 0001-smb-client-fix-OOB-in-receive_encrypted_standard.patch

# Fix for CVE-2022-3524 and CVE-2022-3567
Patch51: 0001-ipv6-annotate-some-data-races-around-sk-sk_prot.patch
Patch55: 0005-ipv6-Fix-data-races-around-sk-sk_prot.patch
Patch56: 0006-tcp-Fix-data-races-around-icsk-icsk_af_ops.patch

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

# Fix for CVE-2022-39189
Patch73: 0001-KVM-x86-do-not-report-a-vCPU-as-preempted-outside-in.patch

# Fix for CVE-2022-36123
Patch74: 0001-x86-xen-Use-clear_bss-for-Xen-PV-guests.patch

# Fix for CVE-2021-4037
Patch76: 0001-xfs-ensure-that-the-inode-uid-gid-match-values-match.patch
Patch77: 0002-xfs-remove-the-icdinode-di_uid-di_gid-members.patch
Patch78: 0003-xfs-fix-up-non-directory-creation-in-SGID-directorie.patch

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
# Remove unnecessary io/memory decoding disabling/enabling.
# Toggling decoding settings (command register/bar) could introduce latency
# spikes across all vcpus due to nested pagetable synchronization
Patch102: 0001-vfio-Only-set-INTX_DISABLE-bit-during-disable.patch

# Next 2 patches are about to be merged into stable
Patch103: 0001-mm-fix-panic-in-__alloc_pages.patch

# TSC calibration optimization
Patch108: Avoid-TSC-recalibration-when-frequency-is-known.patch

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
Patch130: 0001-vmxnet3-correctly-report-encapsulated-LRO-packet.patch
Patch131: 0002-vmxnet3-use-correct-intrConf-reference-when-using-ex.patch
Patch132: 0001-vmxnet3-correctly-report-csum_level-for-encapsulated.patch
Patch133: 0001-vmxnet3-move-rss-code-block-under-eop-descriptor.patch
Patch134: 0001-vmxnet3-use-gro-callback-when-UPT-is-enabled.patch

# Patch to fix Panic due to nested priority inheritance in sched_deadline
Patch135: 0001-sched-deadline-Fix-BUG_ON-condition-for-deboosted-ta.patch

# Backport netfilter patch to allow checking if dst has xfrm attached
Patch141: 0001-netfilter-nf_tables-rt-allow-checking-if-dst-has-xfr.patch

# CVE-2022-43945
Patch151: 0001-NFSD-Cap-rsize_bop-result-based-on-send-buffer-size.patch
Patch152: 0002-NFSD-Protect-against-send-buffer-overflow-in-NFSv3-R.patch
Patch153: 0003-NFSD-Protect-against-send-buffer-overflow-in-NFSv2-R.patch
Patch154: 0004-NFSD-Protect-against-send-buffer-overflow-in-NFSv3-R.patch

#Fix for CVE-2022-0480
Patch156: 0001-memcg-enable-accounting-for-file-lock-caches.patch

#Fix for CVE-2022-3061
Patch157: 0001-video-fbdev-i740fb-Error-out-if-pixclock-equals-zero.patch

#Fix for CVE-2022-3303
Patch158: 0001-ALSA-pcm-oss-Fix-race-at-SNDCTL_DSP_SYNC.patch

#SEV, TDX
Patch161: 0001-x86-boot-Avoid-VE-during-boot-for-TDX-platforms.patch

# Real-Time kernel (PREEMPT_RT patches)
# Source: http://cdn.kernel.org/pub/linux/kernel/projects/rt/4.19/
%include %{SOURCE6}

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

#Patch to add timer advancement feature on guest
Patch626: Guest-timer-Advancement-Feature.patch

# Disable md5 algorithm for sctp if fips is enabled.
Patch630: 0001-disable-md5-algorithm-for-sctp-if-fips-is-enabled.patch

# Backport hrtick changes
Patch634: 0001-sched-Mark-hrtimers-to-expire-in-hard-interrupt-cont.patch
Patch635: 0002-sched-features-Fix-hrtick-reprogramming.patch
Patch636: 0003-sched-features-Distinguish-between-NORMAL-and-DEADLI.patch

# Patch to distribute the tasks within affined cpus
Patch637: linux-rt-sched-core-Distribute-tasks-within-affinity-masks.patch
Patch638: 0001-sched-rt-Use-cpumask_any-_distribute.patch
Patch639: 0001-sched_core-Disable-tasks-distribution-within-cpumask.patch

# Allow cpuidle subsystem to use acpi_idle driver when only one C-state is available
Patch640: 0001-ACPI-processor-idle-Allow-probing-on-platforms-with-.patch

# Provide mixed cpusets guarantees for processes placement
Patch641: 0001-Enable-and-enhance-SCHED-isolation.patch

# Fix for CVE-2021-4204
Patch700: 0002-bpf-Disallow-unprivileged-bpf-by-default.patch

# Fix for CVE-2023-1611
Patch701: 0001-btrfs-fix-race-between-quota-disable-and-quota-assig.patch

#Fix for CVE-2023-1076
Patch702: 0001-net-add-sock_init_data_uid.patch
Patch703: 0001-tap-tap_open-correctly-initialize-socket-uid.patch
Patch704: 0001-tun-tun_chr_open-correctly-initialize-socket-uid.patch

#Fix for CVE-2021-3759
Patch706: 0001-memcg-enable-accounting-of-ipc-resources.patch

#Fix for CVE-2023-2124
Patch707: 0001-xfs-verify-buffer-contents-when-we-skip-log-replay.patch

#Fix for CVE-2023-39197
Patch708: 0001-netfilter-conntrack-dccp-copy-entire-header-to-stack.patch

%if 0%{?kat_build}
Patch1000: fips-kat-tests.patch
%endif

# Patches for i40e v2.23.17 driver
Patch1497: i40e-v2.23.17-Add-support-for-gettimex64-interface.patch
Patch1498: i40e-v2.23.17-i40e-Make-i40e-driver-honor-default-and-user-defined.patch
Patch1499: i40e-v2.23.17-don-t-install-auxiliary-module-on.patch

# Patches for i40e v2.22.18 driver
Patch1500: i40e-v2.22.18-i40e-kcompat.h-Add-support-for-Photon-OS-3.0.patch
Patch1501: i40e-v2.22.18-Add-support-for-gettimex64-interface.patch
Patch1502: i40e-v2.22.18-i40e-Make-i40e-driver-honor-default-and-user-defined.patch
Patch1503: i40e-v2.22.18-don-t-install-auxiliary-module-on.patch

# Patches for i40e v2.16.11 driver
Patch1504: i40e-v2.16.11-i40e-Fix-skb_frag_off-usage-for-kernel-versions-4.19.patch
Patch1505: i40e-v2.16.11-i40e-kcompat.h-Add-support-for-Photon-OS-3.0.patch
Patch1506: i40e-v2.16.11-Add-support-for-gettimex64-interface.patch
Patch1507: i40e-v2.16.11-i40e-Make-i40e-driver-honor-default-and-user-defined.patch
Patch1508: i40e-v2.16.11-add-alias-to-modules_install_no_aux.patch

# Patches for i40e v2.15.9 driver
Patch1509: i40e-v2.15.9-i40e-Fix-skb_frag_off-usage-for-kernel-versions-4.19.patch
Patch1510: i40e-v2.15.9-i40e-kcompat.h-Add-support-for-Photon-OS-3.0.patch
Patch1511: i40e-v2.15.9-Add-support-for-gettimex64-interface.patch
Patch1512: i40e-v2.15.9-i40e-Make-i40e-driver-honor-default-and-user-defined.patch
Patch1513: i40e-v2.15.9-add-alias-for-modules_install_no_aux.patch

# Patches for iavf v4.9.5 driver
Patch1514: iavf-v4.9.5-no-aux-symvers.patch
Patch1515: iavf-v4.9.5-iavf-Makefile-added-alias-for-i40evf.patch

# Patches for iavf v4.9.1 driver
Patch1516: iavf-v4.9.1-no-aux-symvers.patch
Patch1517: iavf-v4.9.1-iavf-Makefile-added-alias-for-i40evf.patch

# Patches for iavf v4.8.2 driver
Patch1518: iavf-v4.8.2-iavf-kcompat.h-Add-support-for-Photon-OS-3.0.patch
Patch1519: iavf-v4.8.2-no-aux-symvers.patch
Patch1520: iavf-v4.8.2-iavf-Makefile-added-alias-for-i40evf.patch

# Patches for iavf v4.5.3 driver
Patch1521: iavf-v4.5.3-iavf-kcompat.h-Add-support-for-Photon-OS-3.0.patch
Patch1522: iavf-v4.5.3-no-aux-symvers.patch
Patch1523: iavf-v4.5.3-iavf-Make-iavf-driver-honor-default-and-user-defined.patch
Patch1524: iavf-v4.5.3-iavf-Makefile-added-alias-for-i40evf.patch
Patch1525: iavf-fix-redefinition-of-eth_hw_addr_set.patch

# Patches for iavf v4.4.2 driver
Patch1526: iavf-v4.4.2-iavf-kcompat.h-Add-support-for-Photon-OS-3.0.patch
Patch1527: iavf-v4.4.2-iavf-Make-iavf-driver-honor-default-and-user-defined.patch
Patch1528: iavf-v4.4.2-introduce-modules-install-no-aux.patch

# Patches for iavf v4.2.7 driver
Patch1529: iavf-v4.2.7-iavf-Fix-skb_frag_off-usage-for-kernel-versions-4.19.patch
Patch1530: iavf-v4.2.7-iavf-kcompat.h-Add-support-for-Photon-OS-3.0.patch
Patch1531: iavf-v4.2.7-iavf-Make-iavf-driver-honor-default-and-user-defined.patch
Patch1532: iavf-v4.2.7-add-alias-to-modules_install_no_aux.patch

# Patch for ice v1.13.7 driver
Patch1533: ice-v1.13.7-don-t-install-auxiliary-module-on-modul.patch

# Patch for ice v1.12.7 driver
Patch1534: ice-v1.12.7-Remove-inline-from-ethtool_sprintf.patch
Patch1535: ice-v1.12.7-don-t-install-auxiliary-module-on-modul.patch

# Patch for ice v1.11.14 driver
Patch1536: ice-v1.11.14-ice-kcompat.h-Add-support-for-Photon-OS-3.0.patch
Patch1537: ice-v1.11.14-don-t-install-auxiliary-module-on-modul.patch
Patch1538: ice-fix-redefinition-of-eth_hw_addr_set.patch

# Patches for ice v1.9.11 driver
Patch1539: ice-v1.9.11-ice-kcompat.h-Add-support-for-Photon-OS-3.0.patch
Patch1540: ice-v1.9.11-ice-Make-ice-driver-honor-default-and-user-defined-I.patch
Patch1541: ice-v1.9.11-don-t-install-auxiliary-module-on-module.patch
Patch1542: ice-fix-redefinition-of-eth_hw_addr_set.patch

# Patches for ice v1.8.3 driver
Patch1543: ice-v1.8.3-ice-kcompat.h-Add-support-for-Photon-OS-3.0.patch
Patch1544: ice-v1.8.3-ice-Make-ice-driver-honor-default-and-user-defined-I.patch
Patch1545: ice-v1.8.3-introduce-modules_install_no_aux.patch

# Patches for ice v1.6.4 driver
Patch1546: ice-v1.6.4-ice-Fix-skb_frag_off-usage-for-kernel-versions-4.19..patch
Patch1547: ice-v1.6.4-ice-kcompat.h-Add-support-for-Photon-OS-3.0.patch
Patch1548: ice-v1.6.4-ice-Make-ice-driver-honor-default-and-user-defined-I.patch
Patch1549: ice-v1.6.4-add-alias-to-modules_install_no_aux.patch

# Usermode helper patches
Patch1550: 0001-umh-Add-command-line-to-user-mode-helpers.patch
Patch1551: 0002-umh-add-exit-routine-for-UMH-process-rt.patch

# bpfilter patches
Patch1552: 0001-net-bpfilter-use-cleanup-callback-to-release-umh_inf.patch
Patch1553: 0002-net-bpfilter-restart-bpfilter_umh-when-error-occurre.patch
Patch1554: 0003-net-bpfilter-disallow-to-remove-bpfilter-module-whil.patch
Patch1555: 0004-net-bpfilter-dont-use-module_init-in-non-modular-cod.patch
Patch1556: 0005-net-bpfilter-fallback-to-netfilter-if-failed-to-load.patch

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
BuildRequires:  bison
BuildRequires:  gettext
# i40e build scripts require getopt
BuildRequires:  util-linux
BuildRequires:  which

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

%package drivers-intel-i40e-2.23.17
Summary:        Intel i40e driver v2.23.17
Group:          System Environment/Kernel
# Add an alias so that the latest version of the i40e driver can be
# installed without having to know its specific version.
Provides:       %{name}-drivers-intel-i40e
Requires:       %{name} = %{version}-%{release}
Conflicts:      %{name}-drivers-intel-i40e-2.22.18 = %{version}-%{release}
Conflicts:      %{name}-drivers-intel-i40e-2.16.11 = %{version}-%{release}
Conflicts:      %{name}-drivers-intel-i40e-2.15.9 = %{version}-%{release}
%description drivers-intel-i40e-2.23.17
This Linux package contains the Intel i40e v2.23.17 driver.

%package drivers-intel-i40e-2.22.18
Summary:        Intel i40e driver v2.22.18
Group:          System Environment/Kernel
Requires:       %{name} = %{version}-%{release}
Conflicts:      %{name}-drivers-intel-i40e-2.23.17 = %{version}-%{release}
Conflicts:      %{name}-drivers-intel-i40e-2.16.11 = %{version}-%{release}
Conflicts:      %{name}-drivers-intel-i40e-2.15.9 = %{version}-%{release}
%description drivers-intel-i40e-2.22.18
This Linux package contains the Intel i40e v2.22.18 driver.

%package drivers-intel-i40e-2.16.11
Summary:        Intel i40e driver v2.16.11
Group:          System Environment/Kernel
Requires:       %{name} = %{version}-%{release}
Conflicts:      %{name}-drivers-intel-i40e-2.23.17 = %{version}-%{release}
Conflicts:      %{name}-drivers-intel-i40e-2.22.18 = %{version}-%{release}
Conflicts:      %{name}-drivers-intel-i40e-2.15.9 = %{version}-%{release}
%description drivers-intel-i40e-2.16.11
This Linux package contains the Intel i40e v2.16.11 driver.

%package drivers-intel-i40e-2.15.9
Summary:        Intel i40e driver v2.15.9
Group:          System Environment/Kernel
Requires:       %{name} = %{version}-%{release}
Conflicts:      %{name}-drivers-intel-i40e-2.23.17 = %{version}-%{release}
Conflicts:      %{name}-drivers-intel-i40e-2.22.18 = %{version}-%{release}
Conflicts:      %{name}-drivers-intel-i40e-2.16.11 = %{version}-%{release}
%description drivers-intel-i40e-2.15.9
This Linux package contains the Intel i40e v2.15.9 driver.

%package drivers-intel-iavf-4.9.5
Summary:        Intel iavf driver v4.9.5
Group:          System Environment/Kernel
# Add an alias so that the latest version of the iavf driver can be
# installed without having to know its specific version.
Provides:       %{name}-drivers-intel-iavf
Requires:       %{name} = %{version}-%{release}
Conflicts:      %{name}-drivers-intel-iavf-4.9.1 = %{version}-%{release}
Conflicts:      %{name}-drivers-intel-iavf-4.8.2 = %{version}-%{release}
Conflicts:      %{name}-drivers-intel-iavf-4.5.3 = %{version}-%{release}
Conflicts:      %{name}-drivers-intel-iavf-4.4.2 = %{version}-%{release}
Conflicts:      %{name}-drivers-intel-iavf-4.2.7 = %{version}-%{release}
%description drivers-intel-iavf-4.9.5
This Linux package contains the Intel iavf v4.9.5 driver.

%package drivers-intel-iavf-4.9.1
Summary:        Intel iavf driver v4.9.1
Group:          System Environment/Kernel
Requires:       %{name} = %{version}-%{release}
Conflicts:      %{name}-drivers-intel-iavf-4.9.5 = %{version}-%{release}
Conflicts:      %{name}-drivers-intel-iavf-4.8.2 = %{version}-%{release}
Conflicts:      %{name}-drivers-intel-iavf-4.5.3 = %{version}-%{release}
Conflicts:      %{name}-drivers-intel-iavf-4.4.2 = %{version}-%{release}
Conflicts:      %{name}-drivers-intel-iavf-4.2.7 = %{version}-%{release}
%description drivers-intel-iavf-4.9.1
This Linux package contains the Intel iavf v4.9.1 driver.

%package drivers-intel-iavf-4.8.2
Summary:        Intel iavf driver v4.8.2
Group:          System Environment/Kernel
Requires:       %{name} = %{version}-%{release}
Conflicts:      %{name}-drivers-intel-iavf-4.9.5 = %{version}-%{release}
Conflicts:      %{name}-drivers-intel-iavf-4.9.1 = %{version}-%{release}
Conflicts:      %{name}-drivers-intel-iavf-4.5.3 = %{version}-%{release}
Conflicts:      %{name}-drivers-intel-iavf-4.4.2 = %{version}-%{release}
Conflicts:      %{name}-drivers-intel-iavf-4.2.7 = %{version}-%{release}
%description drivers-intel-iavf-4.8.2
This Linux package contains the Intel iavf v4.8.2 driver.

%package drivers-intel-iavf-4.5.3
Summary:        Intel iavf driver v4.5.3
Group:          System Environment/Kernel
Requires:       %{name} = %{version}-%{release}
Conflicts:      %{name}-drivers-intel-iavf-4.9.5 = %{version}-%{release}
Conflicts:      %{name}-drivers-intel-iavf-4.9.1 = %{version}-%{release}
Conflicts:      %{name}-drivers-intel-iavf-4.8.2 = %{version}-%{release}
Conflicts:      %{name}-drivers-intel-iavf-4.4.2 = %{version}-%{release}
Conflicts:      %{name}-drivers-intel-iavf-4.2.7 = %{version}-%{release}
%description drivers-intel-iavf-4.5.3
This Linux package contains the Intel iavf v4.5.3 driver.

%package drivers-intel-iavf-4.4.2
Summary:        Intel iavf driver v4.4.2
Group:          System Environment/Kernel
Requires:       %{name} = %{version}-%{release}
Conflicts:      %{name}-drivers-intel-iavf-4.9.5 = %{version}-%{release}
Conflicts:      %{name}-drivers-intel-iavf-4.9.1 = %{version}-%{release}
Conflicts:      %{name}-drivers-intel-iavf-4.8.2 = %{version}-%{release}
Conflicts:      %{name}-drivers-intel-iavf-4.5.3 = %{version}-%{release}
Conflicts:      %{name}-drivers-intel-iavf-4.2.7 = %{version}-%{release}
%description drivers-intel-iavf-4.4.2
This Linux package contains the Intel iavf v4.4.2 driver.

%package drivers-intel-iavf-4.2.7
Summary:        Intel iavf driver v4.2.7
Group:          System Environment/Kernel
Requires:       %{name} = %{version}-%{release}
Conflicts:      %{name}-drivers-intel-iavf-4.9.5 = %{version}-%{release}
Conflicts:      %{name}-drivers-intel-iavf-4.9.1 = %{version}-%{release}
Conflicts:      %{name}-drivers-intel-iavf-4.8.2 = %{version}-%{release}
Conflicts:      %{name}-drivers-intel-iavf-4.5.3 = %{version}-%{release}
Conflicts:      %{name}-drivers-intel-iavf-4.4.2 = %{version}-%{release}
%description drivers-intel-iavf-4.2.7
This Linux package contains the Intel iavf v4.2.7 driver.

%package drivers-intel-ice-1.13.7
Summary:        Intel ice driver v1.13.7
Group:          System Environment/Kernel
# Add an alias so that the latest version of the ice driver can be
# installed without having to know its specific version.
Provides:       %{name}-drivers-intel-ice
Requires:       %{name} = %{version}-%{release}
Conflicts:      %{name}-drivers-intel-ice-1.12.7 = %{version}-%{release}
Conflicts:      %{name}-drivers-intel-ice-1.11.14 = %{version}-%{release}
Conflicts:      %{name}-drivers-intel-ice-1.9.11 = %{version}-%{release}
Conflicts:      %{name}-drivers-intel-ice-1.8.3 = %{version}-%{release}
Conflicts:      %{name}-drivers-intel-ice-1.6.4 = %{version}-%{release}
%description drivers-intel-ice-1.13.7
This Linux package contains the Intel ice v1.13.7 driver.

%package drivers-intel-ice-1.12.7
Summary:        Intel ice driver v1.12.7
Group:          System Environment/Kernel
Requires:       %{name} = %{version}-%{release}
Conflicts:      %{name}-drivers-intel-ice-1.13.7 = %{version}-%{release}
Conflicts:      %{name}-drivers-intel-ice-1.11.14 = %{version}-%{release}
Conflicts:      %{name}-drivers-intel-ice-1.9.11 = %{version}-%{release}
Conflicts:      %{name}-drivers-intel-ice-1.8.3 = %{version}-%{release}
Conflicts:      %{name}-drivers-intel-ice-1.6.4 = %{version}-%{release}
%description drivers-intel-ice-1.12.7
This Linux package contains the Intel ice v1.12.7 driver.

%package drivers-intel-ice-1.11.14
Summary:        Intel ice driver v1.11.14
Group:          System Environment/Kernel
Requires:       %{name} = %{version}-%{release}
Conflicts:      %{name}-drivers-intel-ice-1.13.7 = %{version}-%{release}
Conflicts:      %{name}-drivers-intel-ice-1.12.7 = %{version}-%{release}
Conflicts:      %{name}-drivers-intel-ice-1.9.11 = %{version}-%{release}
Conflicts:      %{name}-drivers-intel-ice-1.8.3 = %{version}-%{release}
Conflicts:      %{name}-drivers-intel-ice-1.6.4 = %{version}-%{release}
%description drivers-intel-ice-1.11.14
This Linux package contains the Intel ice v1.11.14 driver.

%package drivers-intel-ice-1.9.11
Summary:        Intel ice driver v1.9.11
Group:          System Environment/Kernel
Requires:       %{name} = %{version}-%{release}
Conflicts:      %{name}-drivers-intel-ice-1.13.7 = %{version}-%{release}
Conflicts:      %{name}-drivers-intel-ice-1.12.7 = %{version}-%{release}
Conflicts:      %{name}-drivers-intel-ice-1.11.14 = %{version}-%{release}
Conflicts:      %{name}-drivers-intel-ice-1.8.3 = %{version}-%{release}
Conflicts:      %{name}-drivers-intel-ice-1.6.4 = %{version}-%{release}
%description drivers-intel-ice-1.9.11
This Linux package contains the Intel ice v1.9.11 driver.

%package drivers-intel-ice-1.8.3
Summary:        Intel ice driver v1.8.3
Group:          System Environment/Kernel
Requires:       %{name} = %{version}-%{release}
Conflicts:      %{name}-drivers-intel-ice-1.13.7 = %{version}-%{release}
Conflicts:      %{name}-drivers-intel-ice-1.12.7 = %{version}-%{release}
Conflicts:      %{name}-drivers-intel-ice-1.11.14 = %{version}-%{release}
Conflicts:      %{name}-drivers-intel-ice-1.9.11 = %{version}-%{release}
Conflicts:      %{name}-drivers-intel-ice-1.6.4 = %{version}-%{release}
%description drivers-intel-ice-1.8.3
This Linux package contains the Intel ice v1.8.3 driver.

%package drivers-intel-ice-1.6.4
Summary:        Intel ice driver v1.6.4
Group:          System Environment/Kernel
Requires:       %{name} = %{version}-%{release}
Conflicts:      %{name}-drivers-intel-ice-1.13.7 = %{version}-%{release}
Conflicts:      %{name}-drivers-intel-ice-1.12.7 = %{version}-%{release}
Conflicts:      %{name}-drivers-intel-ice-1.11.14 = %{version}-%{release}
Conflicts:      %{name}-drivers-intel-ice-1.9.11 = %{version}-%{release}
Conflicts:      %{name}-drivers-intel-ice-1.8.3 = %{version}-%{release}
%description drivers-intel-ice-1.6.4
This Linux package contains the Intel ice v1.6.4 driver.

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
%setup -q -T -D -b 7 -n linux-%{version}
# Using autosetup is not feasible
%setup -q -T -D -b 8 -n linux-%{version}
# Using autosetup is not feasible
%setup -q -T -D -b 9 -n linux-%{version}
# Using autosetup is not feasible
%setup -q -T -D -b 10 -n linux-%{version}
# Using autosetup is not feasible
%setup -q -T -D -b 11 -n linux-%{version}
# Using autosetup is not feasible
%setup -q -T -D -b 12 -n linux-%{version}
# Using autosetup is not feasible
%setup -q -T -D -b 13 -n linux-%{version}
# Using autosetup is not feasible
%setup -q -T -D -b 14 -n linux-%{version}
# Using autosetup is not feasible
%setup -q -T -D -b 15 -n linux-%{version}
# Using autosetup is not feasible
%setup -q -T -D -b 16 -n linux-%{version}
# Using autosetup is not feasible
%setup -q -T -D -b 17 -n linux-%{version}
# Using autosetup is not feasible
%setup -q -T -D -b 18 -n linux-%{version}
# Using autosetup is not feasible
%setup -q -T -D -b 19 -n linux-%{version}
# Using autosetup is not feasible
%setup -q -T -D -b 20 -n linux-%{version}
# Using autosetup is not feasible
%setup -q -T -D -b 21 -n linux-%{version}
# Using autosetup is not feasible
%setup -q -T -D -b 22 -n linux-%{version}
%endif

%autopatch -p1 -m0 -M641

# CVE Fixes
%autopatch -p1 -m700 -M708

%if 0%{?kat_build}
%patch1000 -p1
%endif

# Patches for i40e v2.23.17 driver
pushd ../i40e-%{i40e_version_2_23_17}
%autopatch -p1 -m1497 -M1499
popd

# Patches for i40e v2.22.18 driver
pushd ../i40e-%{i40e_version_2_22_18}
%autopatch -p1 -m1500 -M1503
popd

# Patches for i40e v2.16.11 driver
pushd ../i40e-%{i40e_version_2_16_11}
%autopatch -p1 -m1504 -M1508
popd

# Patches for i40e v2.15.9 driver
pushd ../i40e-%{i40e_version_2_15_9}
%autopatch -p1 -m1509 -M1513
popd

# Patches for iavf v4.9.5 driver
pushd ../iavf-%{iavf_version_4_9_5}
%autopatch -p1 -m1514 -M1515
popd

# Patches for iavf v4.9.1 driver
pushd ../iavf-%{iavf_version_4_9_1}
%autopatch -p1 -m1516 -M1517
popd

# Patches for iavf v4.8.2 driver
pushd ../iavf-%{iavf_version_4_8_2}
%autopatch -p1 -m1518 -M1520
popd

# Patches for iavf v4.5.3 driver
pushd ../iavf-%{iavf_version_4_5_3}
%autopatch -p1 -m1521 -M1525
popd

# Patches for iavf v4.4.2 driver
pushd ../iavf-%{iavf_version_4_4_2}
%autopatch -p1 -m1526 -M1528
popd

# Patches for iavf v4.2.7 driver
pushd ../iavf-%{iavf_version_4_2_7}
%autopatch -p1 -m1529 -M1532
popd

# Patches for ice v1.13.7 driver
pushd ../ice-%{ice_version_1_13_7}
%autopatch -p1 -m1533 -M1533
popd

# Patches for ice v1.12.7 driver
pushd ../ice-%{ice_version_1_12_7}
%autopatch -p1 -m1534 -M1535
popd

# Patches for ice v1.11.14 driver
pushd ../ice-%{ice_version_1_11_14}
%autopatch -p1 -m1536 -M1538
popd

# Patches for ice v1.9.11 driver
pushd ../ice-%{ice_version_1_9_11}
%autopatch -p1 -m1539 -M1542
popd

# Patches for ice v1.8.3 driver
pushd ../ice-%{ice_version_1_8_3}
%autopatch -p1 -m1543 -M1545
popd

# Patches for ice v1.6.4 driver
pushd ../ice-%{ice_version_1_6_4}
%autopatch -p1 -m1546 -M1549
popd

# Usermode helper patches
%autopatch -p1 -m1550 -M1551

# bpfilter patches
%autopatch -p1 -m1552 -M1556

make mrproper %{?_smp_mflags}

%ifarch x86_64
cp %{SOURCE1} .config
%endif

sed -i 's/CONFIG_LOCALVERSION="-rt"/CONFIG_LOCALVERSION="-%{release}-rt"/' .config

%include %{SOURCE5}

%build
make VERBOSE=1 KBUILD_BUILD_VERSION="1-photon" \
        KBUILD_BUILD_HOST="photon" ARCH=%{?arch} %{?_smp_mflags}

bldroot="${PWD}"

%ifarch x86_64

build_drivers=(
    # i40e driver versions
    i40e-%{i40e_version_2_23_17} \
    i40e-%{i40e_version_2_22_18} \
    i40e-%{i40e_version_2_16_11} \
    i40e-%{i40e_version_2_15_9} \
    # iavf driver versions
    iavf-%{iavf_version_4_9_5} \
    iavf-%{iavf_version_4_9_1} \
    iavf-%{iavf_version_4_8_2} \
    iavf-%{iavf_version_4_5_3} \
    iavf-%{iavf_version_4_4_2} \
    iavf-%{iavf_version_4_2_7} \
    # ice driver versions
    ice-%{ice_version_1_13_7} \
    ice-%{ice_version_1_12_7} \
    ice-%{ice_version_1_11_14} \
    ice-%{ice_version_1_9_11} \
    ice-%{ice_version_1_8_3} \
    ice-%{ice_version_1_6_4} \
)

for driver in "${build_drivers[@]}"; do
    pushd ../$driver
    # make doesn't support _smp_mflags
    make -C src KSRC=${bldroot} clean
    make -C src KSRC=${bldroot} %{?_smp_mflags}
    popd
done

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
install -vdm 755 %{buildroot}%{_sysconfdir}
install -vdm 755 %{buildroot}/boot
install -vdm 755 %{buildroot}%{_defaultdocdir}/linux-%{uname_r}
install -vdm 755 %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}
install -vdm 755 %{buildroot}%{_libdir}/debug/%{_modulesdir}
make INSTALL_MOD_PATH=%{buildroot} modules_install %{?_smp_mflags}

bldroot="${PWD}"

%ifarch x86_64

# ___________________________________________________________
# |         Dependency map for auxiliary module             |
# |_________________________________________________________|
# |  auxiliary.ko   | intel_auxiliary.ko | Not needed       |
# |_________________|____________________|__________________|
# |     iavf-4.5.3  |   i40e-2.23.17     |  ice-1.6.4       |
# |     iavf-4.4.2  |   i40e-2.22.18     |  iavf-4.2.7      |
# |     ice-1.9.11  |   iavf-4.8.2       |  i40e-2.16.11    |
# |     ice-1.8.3   |   iavf-4.9.1       |  i40e-2.15.9     |
# |                 |   iavf-4.9.5       |                  |
# |                 |   ice-1.11.14      |                  |
# |                 |   ice-1.12.7       |                  |
# |                 |   ice-1.13.7       |                  |
# |_________________|____________________|__________________|
#
# auxiliary.ko/intel_auxiliary.ko are common dependencies, so
# install with iavf-4.9.5 and iavf-4.5.3 only. Skip installation
# in all other driver versions with "modules_install_no_aux".

# install i40e drivers
i40e_versions=( \
    %{i40e_version_2_23_17} \
    %{i40e_version_2_22_18} \
    %{i40e_version_2_16_11} \
    %{i40e_version_2_15_9} \
)

for i40e_version in "${i40e_versions[@]}"; do
    # install i40e $i40e_version module
    pushd ../i40e-$i40e_version
    make -C src KSRC=${bldroot} INSTALL_MOD_PATH=%{buildroot} \
        INSTALL_MOD_DIR=extra/i40e-$i40e_version/ \
        MANDIR=%{_mandir} modules_install_no_aux mandocs_install \
        %{?_smp_mflags}
    popd
done

# install iavf drivers
iavf_versions=( \
    %{iavf_version_4_9_5} \
    %{iavf_version_4_9_1} \
    %{iavf_version_4_8_2} \
    %{iavf_version_4_5_3} \
    %{iavf_version_4_4_2} \
    %{iavf_version_4_2_7} \
)

for iavf_version in "${iavf_versions[@]}"; do
    # only install intel_auxiliary.ko/auxiliary.ko with the most up to date iavf driver (v4.9.5)
    if [[ "$iavf_version" == "%{iavf_version_4_9_5}" ]] || [[ "$iavf_version" == "%{iavf_version_4_5_3}" ]]; then
        pushd ../iavf-$iavf_version
        # Install intel_auxiliary.ko only once with iavf 4.9.5 and auxiliary.ko only once with iavf 4.5.3.
        # However, since it is a common dependency, install the intel_auxiliary.ko/auxiliary.ko
        # module under the extra/auxiliary/ directory, so that it gets included in the
        # linux-rt main package, rather than getting bundled with the
        # subpackage of a specific driver/version.
        make -C src KSRC=${bldroot} INSTALL_MOD_PATH=%{buildroot} \
                INSTALL_MOD_DIR=extra/iavf-$iavf_version/ \
                INSTALL_AUX_DIR=extra/auxiliary MANDIR=%{_mandir} \
                modules_install mandocs_install %{?_smp_mflags}

        # only install this once, with iavf 4.9.5
        if [[ "$iavf_version" == "%{iavf_version_4_9_5}" ]]; then
            # keep this updated in line with AUX_BUS_HEADERS in iavf-<version>/src/common.mk
            aux_bus_headers=("linux/auxiliary_bus.h" "auxiliary_compat.h" "kcompat_generated_defs.h")
            for header in "${aux_bus_headers[@]}"; do
                install -Dvm 644 "src/$header" \
                        %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}/include/linux/"${header##*/}"
            done
        fi
        popd
    else
        pushd ../iavf-$iavf_version
        make -C src KSRC=${bldroot} INSTALL_MOD_PATH=%{buildroot} \
            INSTALL_MOD_DIR=extra/iavf-$iavf_version/ \
            MANDIR=%{_mandir} modules_install_no_aux mandocs_install \
            %{?_smp_mflags}
        popd
    fi
done

# install ice drivers
ice_versions=( \
    %{ice_version_1_13_7} \
    %{ice_version_1_12_7} \
    %{ice_version_1_11_14} \
    %{ice_version_1_9_11} \
    %{ice_version_1_8_3} \
    %{ice_version_1_6_4} \
)

for ice_version in "${ice_versions[@]}"; do
    pushd ../ice-$ice_version
    make -C src KSRC=${bldroot} INSTALL_MOD_PATH=%{buildroot} \
        INSTALL_MOD_DIR=extra/ice-$ice_version/ modules_install_no_aux \
        %{?_smp_mflags}
    make -C src KSRC=${bldroot} INSTALL_MOD_PATH=%{buildroot} \
        MANDIR=%{_mandir} mandocs_install %{?_smp_mflags}
    popd
done

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

find arch/%{?archdir}/include include scripts -type f | xargs sh -c 'cp --parents "$@" %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}' copy

find $(find arch/%{?archdir} -name include -o -name scripts -type d) -type f | xargs sh -c 'cp --parents "$@" %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}' copy

find arch/%{?archdir}/include Module.symvers include scripts -type f | xargs sh -c 'cp --parents "$@" %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}' copy

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

%post drivers-intel-i40e-2.23.17
/sbin/depmod -a %{uname_r}

%post drivers-intel-i40e-2.22.18
/sbin/depmod -a %{uname_r}

%post drivers-intel-i40e-2.16.11
/sbin/depmod -a %{uname_r}

%post drivers-intel-i40e-2.15.9
/sbin/depmod -a %{uname_r}

%post drivers-intel-iavf-4.9.5
/sbin/depmod -a %{uname_r}

%post drivers-intel-iavf-4.9.1
/sbin/depmod -a %{uname_r}

%post drivers-intel-iavf-4.8.2
/sbin/depmod -a %{uname_r}

%post drivers-intel-iavf-4.5.3
/sbin/depmod -a %{uname_r}

%post drivers-intel-iavf-4.4.2
/sbin/depmod -a %{uname_r}

%post drivers-intel-iavf-4.2.7
/sbin/depmod -a %{uname_r}

%post drivers-intel-ice-1.13.7
/sbin/depmod -a %{uname_r}

%post drivers-intel-ice-1.12.7
/sbin/depmod -a %{uname_r}

%post drivers-intel-ice-1.11.14
/sbin/depmod -a %{uname_r}

%post drivers-intel-ice-1.9.11
/sbin/depmod -a %{uname_r}

%post drivers-intel-ice-1.8.3
/sbin/depmod -a %{uname_r}

%post drivers-intel-ice-1.6.4
/sbin/depmod -a %{uname_r}

%files
%defattr(-,root,root)
/boot/System.map-%{uname_r}
/boot/config-%{uname_r}
/boot/vmlinuz-%{uname_r}
%config(noreplace) /boot/linux-%{uname_r}.cfg
%config %{_sharedstatedir}/initramfs/kernel/%{uname_r}
%defattr(0644,root,root)
%{_modulesdir}/*
%dir %{_modulesdir}/extra/
%{_modulesdir}/extra/auxiliary/intel_auxiliary.ko.xz
%{_modulesdir}/extra/auxiliary/auxiliary.ko.xz
%exclude %{_modulesdir}/build
%{_sysconfdir}/modprobe.d/iavf.conf
# ICE driver firmware files are packaged in linux-firmware
%exclude /lib/firmware/updates/intel/ice
# Intel i40e driver modules are included in sub-packages
%exclude %{_modulesdir}/extra/i40e-*
# Intel iavf driver modules are included in sub-packages
%exclude %{_modulesdir}/extra/iavf-*
# Intel ice driver modules are included in sub-packages
%exclude %{_modulesdir}/extra/ice-*

%files devel
%defattr(-,root,root)
%{_modulesdir}/build
%{_usrsrc}/linux-headers-%{uname_r}

%files drivers-intel-i40e-2.23.17
%defattr(-,root,root)
%dir %{_modulesdir}/extra/i40e-2.23.17
%{_modulesdir}/extra/i40e-2.23.17/i40e.ko.xz

%files drivers-intel-i40e-2.22.18
%defattr(-,root,root)
%dir %{_modulesdir}/extra/i40e-2.22.18
%{_modulesdir}/extra/i40e-2.22.18/i40e.ko.xz

%files drivers-intel-i40e-2.16.11
%defattr(-,root,root)
%dir %{_modulesdir}/extra/i40e-2.16.11
%{_modulesdir}/extra/i40e-2.16.11/i40e.ko.xz

%files drivers-intel-i40e-2.15.9
%defattr(-,root,root)
%dir %{_modulesdir}/extra/i40e-2.15.9
%{_modulesdir}/extra/i40e-2.15.9/i40e.ko.xz

%files drivers-intel-iavf-4.9.5
%defattr(-,root,root)
%dir %{_modulesdir}/extra/iavf-%{iavf_version_4_9_5}
%{_modulesdir}/extra/iavf-%{iavf_version_4_9_5}/iavf.ko.xz

%files drivers-intel-iavf-4.9.1
%defattr(-,root,root)
%dir %{_modulesdir}/extra/iavf-%{iavf_version_4_9_1}
%{_modulesdir}/extra/iavf-%{iavf_version_4_9_1}/iavf.ko.xz

%files drivers-intel-iavf-4.8.2
%defattr(-,root,root)
%dir %{_modulesdir}/extra/iavf-4.8.2
%{_modulesdir}/extra/iavf-4.8.2/iavf.ko.xz

%files drivers-intel-iavf-4.5.3
%defattr(-,root,root)
%dir %{_modulesdir}/extra/iavf-4.5.3
%{_modulesdir}/extra/iavf-4.5.3/iavf.ko.xz

%files drivers-intel-iavf-4.4.2
%defattr(-,root,root)
%dir %{_modulesdir}/extra/iavf-4.4.2
%{_modulesdir}/extra/iavf-4.4.2/iavf.ko.xz

%files drivers-intel-iavf-4.2.7
%defattr(-,root,root)
%dir %{_modulesdir}/extra/iavf-4.2.7
%{_modulesdir}/extra/iavf-4.2.7/iavf.ko.xz

%files drivers-intel-ice-1.13.7
%defattr(-,root,root)
%dir %{_modulesdir}/extra/ice-1.13.7
%{_modulesdir}/extra/ice-1.13.7/ice.ko.xz

%files drivers-intel-ice-1.12.7
%defattr(-,root,root)
%dir %{_modulesdir}/extra/ice-1.12.7
%{_modulesdir}/extra/ice-1.12.7/ice.ko.xz

%files drivers-intel-ice-1.11.14
%defattr(-,root,root)
%dir %{_modulesdir}/extra/ice-1.11.14
%{_modulesdir}/extra/ice-1.11.14/ice.ko.xz

%files drivers-intel-ice-1.9.11
%defattr(-,root,root)
%dir %{_modulesdir}/extra/ice-1.9.11
%{_modulesdir}/extra/ice-1.9.11/ice.ko.xz

%files drivers-intel-ice-1.8.3
%defattr(-,root,root)
%dir %{_modulesdir}/extra/ice-1.8.3
%{_modulesdir}/extra/ice-1.8.3/ice.ko.xz

%files drivers-intel-ice-1.6.4
%defattr(-,root,root)
%dir %{_modulesdir}/extra/ice-1.6.4
%{_modulesdir}/extra/ice-1.6.4/ice.ko.xz

%files docs
%defattr(-,root,root)
%{_defaultdocdir}/linux-%{uname_r}/*
%{_mandir}/*

%changelog
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
* Wed Sep 20 2023 Roye Eshed <eshedr@vmware.com> 4.19.292-4
- Fix for CVE-2023-42753
* Wed Sep 06 2023 Kuntal Nayak <nkuntal@vmware.com> 4.19.292-3
- Avoid TSC recalibration
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
* Mon Aug 07 2023 Alexey Makhalov <amakhalov@vmware.com> 4.19.288-5
- Enable and enhance sched isolation.
* Mon Jul 31 2023 Ajay Kaher <akaher@vmware.com> 4.19.288-4
- Fix: SEV: Guest should not disabled CR4.MCE
* Mon Jul 31 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 4.19.288-3
- Fix for CVE-2023-2124
* Mon Jul 24 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 4.19.288-2
- Fix for CVE-2021-3759
* Fri Jul 21 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 4.19.288-1
- Update to version 4.19.288
* Wed Jul 19 2023 Ankit Jain <ankitja@vmware.com> 4.19.285-3
- Kernel cmdline param to disable tasks distribution within
- cpumask feature
* Tue Jul 18 2023 Naadir Jeewa <jeewan@vmware.com> 4.19.285-2
- Fixes for bpfilter and usermode helpers
- Add additional build dependencies for container builds
* Wed Jun 14 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 4.19.285-1
- Update to version 4.19.285
* Wed Jun 14 2023 Srish Srinivasan <ssrish@vmware.com> 4.19.283-5
- Fix for CVE-2023-1076 and CVE-2023-1077
* Fri Jun 09 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 4.19.283-4
- Fix for CVE-2023-1611
* Fri Jun 09 2023 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.283-3
- Fix issues in Guest timer Advancement feature
* Wed May 31 2023 Ankit Jain <ankitja@vmware.com> 4.19.283-2
- Allow cpuidle subsystem to use acpi_idle driver
- when only one C-state is available
* Wed May 17 2023 Ankit Jain <ankitja@vmware.com> 4.19.283-1
- Update to version 4.19.283
* Tue Apr 18 2023 Keerthana K <keerthanak@vmware.com> 4.19.280-1
- Update to version 4.19.280
* Mon Apr 17 2023 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.277-5
- Cleanup commented patch files
* Wed Mar 29 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 4.19.277-4
- update to latest ToT vmxnet3 driver pathes
* Thu Mar 23 2023 Ankit Jain <ankitja@vmware.com> 4.19.277-3
- Use cpumask_any_distribute() instead of cpumask_any()
- This will help in distributing the RT tasks on affined cpus
* Thu Mar 16 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 4.19.277-2
- Patch drivers to not install aux module on modules_install_no_aux
- Clean up driver installation code
* Tue Mar 14 2023 Roye Eshed <eshedr@vmware.com> 4.19.277-1
- Update to version 4.19.277
* Thu Mar 02 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 4.19.272-4
- Update ice driver to 1.11.14, iavf driver to 4.8.2 and i40e to 2.22.18
* Thu Mar 02 2023 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.272-3
- Use Photon kernel macros to simplify building i40e, iavf and ice drivers
* Tue Feb 28 2023 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.272-2
- Expose Photon kernel macros to simplify building out-of-tree drivers.
* Thu Feb 16 2023 Srish Srinivasan <ssrish@vmware.com> 4.19.272-1
- Update to version 4.19.272
* Tue Feb 14 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 4.19.271-4
- Fix for CVE-2021-44879/2022-0480/CVE-2022-3061/CVE-2022-3303/CVE-2023-23454
* Thu Feb 09 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 4.19.271-3
- Fix regression in RT patchset that leads to a deadlock/hang.
* Mon Feb 06 2023 Alexey Makhalov <amakhalov@vmware.com> 4.19.271-2
- Implement performance over security option for RETBleed (pos=1)
* Wed Feb 01 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 4.19.271-1
- Update to version 4.19.271
* Thu Jan 05 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 4.19.269-2
- update to latest ToT vmxnet3 driver
- Include patch "vmxnet3: correctly report csum_level for encapsulated packet"
* Mon Dec 19 2022 srinidhira0 <srinidhir@vmware.com> 4.19.269-1
- Update to version 4.19.269
* Thu Dec 15 2022 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 4.19.268-2
- update to latest ToT vmxnet3 driver
* Fri Dec 09 2022 Ankit Jain <ankitja@vmware.com> 4.19.268-1
- Update to version 4.19.268
* Fri Dec 09 2022 Ankit Jain <ankitja@vmware.com> 4.19.264-8
- Distribute the tasks across affined cpus
* Tue Dec 06 2022 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 4.19.264-7
- Fix for CVE-2022-43945
* Mon Nov 21 2022 Ankit Jain <ankitja@vmware.com> 4.19.264-6
- Added ice driver v1.9.11 as sub-package
- Added iavf driver v4.5.3 as sub-package
* Thu Nov 17 2022 Bo Gan <ganb@vmware.com> 4.19.264-5
- Reduce latency spikes when process using vfio-pci terminates,
- by avoiding vfio-pci toggling io/memory decoding.
* Wed Nov 16 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.264-4
- Fix IRQ affinities of i40e, iavf and ice drivers
* Wed Nov 16 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.264-3
- Package Intel i40e, iavf and ice drivers as sub-packages, and provide
- multiple versions of these drivers, namely, i40e-v2.16.11, i40e-v2.15.9,
- iavf-v4.4.2, iavf-v4.2.7, ice-v1.8.3 and ice-v1.6.4
* Mon Nov 07 2022 Ajay Kaher <akaher@vmware.com> 4.19.264-2
- Fix CVE-2022-3524 and CVE-2022-3567
* Thu Nov 03 2022 Ajay Kaher <akaher@vmware.com> 4.19.264-1
- Update to version 4.19.264
* Wed Oct 19 2022 Sharan Turlapati <sturlapati@vmware.com> 4.19.261-1
- Update to version 4.19.261
* Tue Sep 27 2022 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.256-5
- Fix for CVE-2022-34918
* Mon Sep 19 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 4.19.256-4
- Fix for CVE-2022-3028/2021-4037
* Tue Sep 13 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 4.19.256-3
- Fix for CVE-2022-39189/2022-36123
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
