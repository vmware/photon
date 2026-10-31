# CVE patches shared across all Linux kernel flavours
# Patch range reserved: 3000–3999
# DO NOT add non-CVE patches to this file.

# Fix CVE-2017-1000252
Patch3000: KVM-Don-t-accept-obviously-wrong-gsi-values-via-KVM_.patch

# Fix CVE-2026-43083
%if 0%{?photon_subrelease} == 91
Patch3001: 0001-net-ioam6-fix-OOB-and-missing-lock.patch
%endif

# Fix CVE-2025-68359
%if 0%{?photon_subrelease} == 91
Patch3002: 0001-btrfs-fix-double-free-of-qgroup-record-after-failure.patch
%endif

# Fix CVE-2026-43101
%if 0%{?photon_subrelease} == 91
Patch3004: 0002-ipv6-ioam-fix-potential-NULL-dereferences-in-__ioam6.patch
%endif
# Fixes CVE-2026-31589, CVE-2026-43414, CVE-2026-43465, CVE-2026-53224, CVE-2026-53246, CVE-2026-53260
Patch3005: 0001-mm-call-free_folio-directly-in-folio_.patch
%if 0%{?photon_subrelease} == 91
Patch3006: 0001-net-mlx5e-RX-Fix-XDP-multi-buf-frag-c-6.12.111.patch
%endif
%if 0%{?photon_subrelease} == 91
Patch3007: 0001-scsi-qla2xxx-Completely-fix-fcport-do.patch
%endif
%if 0%{?photon_subrelease} == 91
Patch3008: 0001-sctp-validate-cached-peer-INIT-chunk-length-in-COOKI.patch
%endif
%if 0%{?photon_subrelease} == 91
Patch3010: 0002-sctp-validate-embedded-INIT-chunk-and.patch
%endif
%if 0%{?photon_subrelease} == 91
Patch3011: 0003-sctp-add-INIT-verification-after-cookie-unpacking.patch
%endif
# Fixes CVE-2025-40074, CVE-2025-68353, CVE-2026-23208, CVE-2026-43009, CVE-2026-43485
%if 0%{?photon_subrelease} == 91
Patch3014: 0001-ALSA-usb-audio-Prevent-excessive-number-of-frames.patch
%endif
%if 0%{?photon_subrelease} == 91
Patch3015: 0001-bpf-Fix-incorrect-pruning-due-to-atomic-fetch-precis.patch
%endif
%if 0%{?photon_subrelease} == 91
Patch3017: 0001-net-vxlan-prevent-NULL-deref-in-vxlan_xmit_one.patch
%endif
%if 0%{?photon_subrelease} == 91
Patch3018: 0001-nouveau-gsp-drop-WARN_ON-in-ACPI-probes.patch
%endif
Patch3019: 0002-ALSA-usb-audio-Use-the-right-limit-for-PCM-OOB-check.patch
# Fixes CVE-2025-40158, CVE-2025-68745, CVE-2026-63872, CVE-2026-64076, CVE-2026-64077
Patch3020: 0001-esp-fix-page-frag-reference-leak-on-skb_to_sgvec-failure.patch
%if 0%{?photon_subrelease} == 91
Patch3021: 0001-ipv6-use-RCU-in-ip6_output.patch
%endif
%if 0%{?photon_subrelease} == 91
Patch3022: 0001-netfilter-bridge-eb_tables-close-module-init-race.patch
%endif
%if 0%{?photon_subrelease} == 91
Patch3023: 0001-netfilter-ebtables-move-to-two-stage-removal-scheme.patch
%endif
%if 0%{?photon_subrelease} == 91
Patch3024: 0001-scsi-qla2xxx-Clear-cmds-after-chip-reset.patch
%endif
# Fixes CVE-2026-52988, CVE-2026-52991, CVE-2026-53089, CVE-2026-53091
Patch3026: 0001-cgroup-psi-Set-of-priv-to-NULL-upon-file-release.patch
%if 0%{?photon_subrelease} == 91
Patch3027: 0001-rculist-add-list_splice_rcu-for-private-lists.patch
Patch3028: 0002-netfilter-nf_tables-join-hook-list-via-splice_list_r.patch
%endif
%if 0%{?photon_subrelease} == 91
Patch3029: 0002-sched-psi-fix-race-between-file-release-and-pressure.patch
%endif
Patch3030: 0001-net_sched-make-room-for-struct-qdisc_skb_cb-pkt_segs.patch
%if 0%{?photon_subrelease} == 91
Patch3031: 0002-net-init-shinfo-gso_segs-from-qdisc_pkt_len_init-6.12.111.patch
%else
Patch3031: 0002-net-init-shinfo-gso_segs-from-qdisc_pkt_len_init.patch
%endif
%if 0%{?photon_subrelease} == 91
Patch3032: 0003-net_sched-initialize-qdisc_skb_cb-skb-pkt_segs-in-qd-6.12.111.patch
%else
Patch3032: 0003-net_sched-initialize-qdisc_skb_cb-skb-pkt_segs-in-qd.patch
%endif
Patch3033: 0004-net-use-qdisc_pkt_len_segs_init-in-sch_handle_ingres.patch
Patch3034: 0005-net-dropreason-add-SKB_DROP_REASON_RECURSION_LIMIT.patch
%if 0%{?photon_subrelease} == 91
Patch3035: 0006-net-plumb-drop-reasons-to-__dev_queue_xmit-6.12.111.patch
%else
Patch3035: 0006-net-plumb-drop-reasons-to-__dev_queue_xmit.patch
%endif
%if 0%{?photon_subrelease} == 91
Patch3036: 0007-net-qdisc_pkt_len_segs_init-cleanup.patch
%endif
%if 0%{?photon_subrelease} == 91
Patch3037: 0008-net-pull-headers-in-qdisc_pkt_len_segs_init.patch
%endif
Patch3038: 0009-xfrm-Do-not-clobber-inner-headers-when-already-set.patch
# Fixes CVE-2026-63979, CVE-2026-64024, CVE-2026-64066, CVE-2026-64067, CVE-2026-64068
%if 0%{?photon_subrelease} == 91
Patch3039: 0001-net-handshake-hand-off-the-pinned-file-reference-to-.patch
%endif
Patch3040: 0001-netfs-Fix-missing-barriers-when-accessing-stream-sub.patch
%if 0%{?photon_subrelease} == 91
Patch3041: 0001-netfs-Fix-missing-locking-around-retry-adding-new-su.patch
%endif
Patch3042: 0001-netfs-Fix-netfs_read_to_pagecache-to-pause-on-subreq.patch
%if 0%{?photon_subrelease} == 91
Patch3043: 0001-tcp-fix-stale-per-CPU-tcp_tw_isn-leak-enabling-ISN-p.patch
%endif
# Fixes CVE-2026-72288, CVE-2026-72355
%if 0%{?photon_subrelease} == 91
Patch3045: 0001-KVM-arm64-vgic-Handle-race-between-interrupt-affini.patch
%endif
Patch3046: 0001-netfs-Fix-barriering-when-walking-subrequest-list.patch
# Fixes CVE-2026-72413, CVE-2026-72423
%if 0%{?photon_subrelease} == 91
Patch3047: 0001-bpf-Guard-conntrack-opts-error-writes.patch
%endif
# Fixes CVE-2026-72366, CVE-2026-72463, CVE-2026-72493, CVE-2026-74268, CVE-2026-74269
%if 0%{?photon_subrelease} == 91
Patch3049: 0001-bnxt-fix-head-underflow-on-XDP-head-grow-6.12.111.patch
%endif
%if 0%{?photon_subrelease} == 91
Patch3050: 0001-net-serialize-netif_running-check-in-enqueue_to_backlog.patch
%endif
%if 0%{?photon_subrelease} == 91
Patch3051: 0001-netfs-Fix-netfs_create_write_req-to-handle-async-cac.patch
%endif
%if 0%{?photon_subrelease} == 91
Patch3053: 0001-xfrm-Fix-dev-use-after-free-in-xfrm-async-resumption.patch
# Fixes CVE-2026-64160
Patch3054: 0001-cifs-Fix-handling-of-a-beyond-EOF-DIO-unbuffered-rea.patch
%endif
Patch3055: 0002-filemap-Add-folio_next_pos.patch
%if 0%{?photon_subrelease} == 91
Patch3056: 0003-netfs-Fix-potential-for-tearing-in-remote_i_size-and-6.12.111.patch
%else
Patch3056: 0003-netfs-Fix-potential-for-tearing-in-remote_i_size-and.patch
%endif
Patch3057: 0004-cifs-Fix-undefined-variables.patch
# Fixes CVE-2026-63853, CVE-2026-63879, CVE-2026-64036, CVE-2026-64058, CVE-2026-64078
%if 0%{?photon_subrelease} == 91
Patch3058: 0001-cgroup-rstat-validate-cpu-before-css_rstat_cpu-acce.patch
%endif
%if 0%{?photon_subrelease} == 91
Patch3059: 0001-drm-amdgpu-fix-amdgpu_hmm_range_get_pages.patch
%endif
%if 0%{?photon_subrelease} == 91
Patch3060: 0001-drm-amdgpu-vcn-set-no_user_fence-for-VCN-v4.0-enc-r.patch
%endif
Patch3061: 0001-netfilter-x_tables-add-and-use-xt_unregister_table_p.patch
%if 0%{?photon_subrelease} == 91
Patch3063: 0002-netfilter-x_tables-add-and-use-xtables_unregister_ta-6.12.111.patch
%else
Patch3063: 0002-netfilter-x_tables-add-and-use-xtables_unregister_ta.patch
%endif
# Fixes CVE-2026-74571, CVE-2026-80580
%if 0%{?photon_subrelease} == 91
Patch3064: 0001-btrfs-skip-global-block-reserve-accounting-for-res.patch
%endif
Patch3065: 0001-fbdev-bound-mode-sysfs-output-to-the-sysfs-buffer.patch
# Fixes CVE-2026-68399, CVE-2026-68404, CVE-2026-68409, CVE-2026-68441, CVE-2026-68447, CVE-2026-74571
%if 0%{?photon_subrelease} == 91
Patch3066: 0001-CVE-2026-68399-bpf-Fix-UAF-in-sock-clone-early-bailo.patch
%endif
%if 0%{?photon_subrelease} == 91
Patch3067: 0001-CVE-2026-68404-wifi-cfg80211-use-wiphy-work-for-sock.patch
%endif
%if 0%{?photon_subrelease} == 91
Patch3068: 0001-CVE-2026-68409-wifi-mac80211-defer-link-RX-stats-per.patch
%endif
%if 0%{?photon_subrelease} == 91
Patch3069: 0001-CVE-2026-68441-net-sched-Handle-TC_ACT_REDIRECT-from-6.12.111.patch
%endif
%if 0%{?photon_subrelease} == 91
Patch3070: 0001-CVE-2026-68447-drm-amdkfd-clamp-v9-CRIU-control-stac.patch
%endif
# Fixes CVE-2026-74605, CVE-2026-74611
%if 0%{?photon_subrelease} == 91
Patch3071: 0001-eventfs-Use-children-field-for-rcu-head-and-add-memo.patch
%endif
%if 0%{?photon_subrelease} == 91
Patch3072: 0002-tls-rx-restore-msg_iter-before-TLS-1.3-optimistic-re.patch
%endif
# Fixes CVE-2026-80785
%if 0%{?photon_subrelease} == 91
Patch3073: 0001-fbdev-Wrap-user-invoked-calls-to-fb_set_var-in-helpe.patch
%endif
Patch3074: 0002-fbdev-serialize-mode-sysfs-access-with-lock_fb_info.patch
# Fixes CVE-2026-43464, CVE-2026-45932, CVE-2026-46324, CVE-2026-52956
%if 0%{?photon_subrelease} == 91
Patch3075: 0001-bpf-Fix-tcx-netkit-detach-permissions-when-prog-fd-i.patch
%endif
%if 0%{?photon_subrelease} == 91
Patch3076: 0001-libceph-Fix-potential-out-of-bounds-access-in-__ceph.patch
%endif
%if 0%{?photon_subrelease} == 91
Patch3077: 0001-net-mlx5e-RX-Fix-XDP-multi-buf-frag-counting-for-leg.patch
%endif
%if 0%{?photon_subrelease} == 91
Patch3078: 0001-netfilter-nf_tables-use-list_del_rcu-for-netlink-hoo.patch
%endif
# Fixes CVE-2026-64388, CVE-2026-72031, CVE-2026-72341, CVE-2026-72439
%if 0%{?photon_subrelease} == 91
Patch3080: 0001-ata-libata-core-Add-NOLPM-quirk-for-PNY-CS900-1TB-SS.patch
%endif
%if 0%{?photon_subrelease} == 91
Patch3081: 0001-md-raid10-fix-writes_pending-leak-on-write-request-f.patch
%endif
%if 0%{?photon_subrelease} == 91
Patch3082: 0001-net-mlx5e-Fix-publication-race-for-priv-channel_stat.patch
%endif
%if 0%{?photon_subrelease} == 91
Patch3083: 0001-smb-client-fix-chown-chgrp-with-SMB3-POSIX-Extension.patch
%endif
# Fixes CVE-2026-68426
%if 0%{?photon_subrelease} == 91
Patch3084: 0001-xfrm-fix-stale-skb-prev-after-async-crypto-steals-a-.patch
%endif
# Fixes CVE-2026-46325, CVE-2026-68242, CVE-2026-68258
%if 0%{?photon_subrelease} == 91
Patch3085: 0001-RDMA-rxe-Fix-iova-to-va-conversion-for-MR-page-sizes.patch
%endif
%if 0%{?photon_subrelease} == 91
Patch3086: 0001-drm-amdkfd-Check-bounds-on-CRIU-restore-queue-type-a.patch
%endif
%if 0%{?photon_subrelease} == 91
Patch3087: 0001-drm-i915-gt-Fix-NULL-deref-on-sched_engine-alloc-fai.patch
%endif
%if 0%{?photon_subrelease} >= 92
# Fixes CVE-2026-74752
# Fixes CVE-2026-90104
# Fixes CVE-2026-74723, CVE-2026-89537
# Fixes CVE-2026-80634
# Fixes CVE-2026-63858
Patch3093: 0001-netfilter-nf_tables-avoid-false-positive-lockdep-flowtables.patch
Patch3094: 0002-netfilter-nf_tables-avoid-false-positive-lockdep-basechain.patch
Patch3095: 0003-netfilter-nf_tables-use-list_del_rcu-for-netlink-hoo.patch
Patch3096: 0004-netfilter-nf_tables-add-hook-transactions-for-device.patch
# Fixes CVE-2026-72345, CVE-2026-89682, CVE-2026-90149, CVE-2026-90217, CVE-2026-90231, CVE-2026-90240, CVE-2026-90343, CVE-2026-92499, CVE-2026-93221
Patch3100: 0001-ext4-validate-readdir-offset-before-accessing-dirent.patch
Patch3102: 0001-net-mlx5-LAG-Fix-off-by-one-in-single-FDB-error-rol.patch
Patch3106: 0002-nfsd-use-test_and_clear_bit-for-somebody_reclaimed-to.patch
# Fixes CVE-2026-72355, CVE-2026-80670, CVE-2026-89637
Patch3107: 0001-perf-stat-Bounds-check-CPU-index-in-topology-aggrega.patch
Patch3108: 0001-smb-client-fix-UAF-and-buffer-leak-in-cifs_check_tra.patch
Patch3109: 0002-perf-stat-Introduce-perf_env__get_cpu_topology-to-gu.patch
Patch3110: 0003-perf-tools-Use-perf_env__get_cpu_topology-in-machine.patch
# Fixes CVE-2026-80738, CVE-2026-89654
Patch3113: 0002-ceph-fix-use-after-free-in-check_new_map-after-early.patch
# Fixes CVE-2026-80631, CVE-2026-80668, CVE-2026-80705
Patch3116: 0001-netfilter-conntrack-check-NULL-when-retrieving-ct-ex.patch
Patch3119: 0004-netfilter-nf_conntrack_expect-add-and-use-nf_ct_expe.patch
Patch3120: 0005-netfilter-nf_conntrack_expect-bail-out-on-insert-dea.patch
Patch3121: 0006-netfilter-nf_conntrack_expect-consolidate-check-for-.patch
%endif
