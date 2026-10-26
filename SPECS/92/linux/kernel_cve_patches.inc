# CVE patches shared across all Linux kernel flavours
# Patch range reserved: 3000–3999
# DO NOT add non-CVE patches to this file.

# Fix CVE-2017-1000252
Patch3000: KVM-Don-t-accept-obviously-wrong-gsi-values-via-KVM_.patch

# Fixes CVE-2026-31589, CVE-2026-43414, CVE-2026-43465, CVE-2026-53224, CVE-2026-53246, CVE-2026-53260
Patch3005: 0001-mm-call-free_folio-directly-in-folio_.patch
Patch3019: 0002-ALSA-usb-audio-Use-the-right-limit-for-PCM-OOB-check.patch
# Fixes CVE-2025-40158, CVE-2025-68745, CVE-2026-63872, CVE-2026-64076, CVE-2026-64077
Patch3020: 0001-esp-fix-page-frag-reference-leak-on-skb_to_sgvec-failure.patch
# Fixes CVE-2026-52988, CVE-2026-52991, CVE-2026-53089, CVE-2026-53091
Patch3026: 0001-cgroup-psi-Set-of-priv-to-NULL-upon-file-release.patch
Patch3030: 0001-net_sched-make-room-for-struct-qdisc_skb_cb-pkt_segs.patch
Patch3031: 0002-net-init-shinfo-gso_segs-from-qdisc_pkt_len_init.patch
Patch3032: 0003-net_sched-initialize-qdisc_skb_cb-skb-pkt_segs-in-qd.patch
Patch3033: 0004-net-use-qdisc_pkt_len_segs_init-in-sch_handle_ingres.patch
Patch3034: 0005-net-dropreason-add-SKB_DROP_REASON_RECURSION_LIMIT.patch
Patch3035: 0006-net-plumb-drop-reasons-to-__dev_queue_xmit.patch
Patch3038: 0009-xfrm-Do-not-clobber-inner-headers-when-already-set.patch
Patch3040: 0001-netfs-Fix-missing-barriers-when-accessing-stream-sub.patch
Patch3042: 0001-netfs-Fix-netfs_read_to_pagecache-to-pause-on-subreq.patch
Patch3046: 0001-netfs-Fix-barriering-when-walking-subrequest-list.patch
Patch3055: 0002-filemap-Add-folio_next_pos.patch
Patch3056: 0003-netfs-Fix-potential-for-tearing-in-remote_i_size-and.patch
Patch3057: 0004-cifs-Fix-undefined-variables.patch
Patch3061: 0001-netfilter-x_tables-add-and-use-xt_unregister_table_p.patch
Patch3063: 0002-netfilter-x_tables-add-and-use-xtables_unregister_ta.patch
Patch3065: 0001-fbdev-bound-mode-sysfs-output-to-the-sysfs-buffer.patch
Patch3074: 0002-fbdev-serialize-mode-sysfs-access-with-lock_fb_info.patch
# Fixes CVE-2026-63858
Patch3093: 0001-netfilter-nf_tables-avoid-false-positive-lockdep-flowtables.patch
Patch3094: 0002-netfilter-nf_tables-avoid-false-positive-lockdep-basechain.patch
Patch3095: 0003-netfilter-nf_tables-use-list_del_rcu-for-netlink-hoo.patch
Patch3096: 0004-netfilter-nf_tables-add-hook-transactions-for-device.patch
Patch3100: 0001-ext4-validate-readdir-offset-before-accessing-dirent.patch
Patch3102: 0001-net-mlx5-LAG-Fix-off-by-one-in-single-FDB-error-rol.patch
Patch3106: 0002-nfsd-use-test_and_clear_bit-for-somebody_reclaimed-to.patch
# Fixes CVE-2026-72355, CVE-2026-80670, CVE-2026-89637
Patch3107: 0001-perf-stat-Bounds-check-CPU-index-in-topology-aggrega.patch
Patch3108: 0001-smb-client-fix-UAF-and-buffer-leak-in-cifs_check_tra.patch
Patch3109: 0002-perf-stat-Introduce-perf_env__get_cpu_topology-to-gu.patch
Patch3110: 0003-perf-tools-Use-perf_env__get_cpu_topology-in-machine.patch
Patch3113: 0002-ceph-fix-use-after-free-in-check_new_map-after-early.patch
# Fixes CVE-2026-80668
Patch3116: 0001-netfilter-conntrack-check-NULL-when-retrieving-ct-ex.patch
Patch3119: 0004-netfilter-nf_conntrack_expect-add-and-use-nf_ct_expe.patch
Patch3120: 0005-netfilter-nf_conntrack_expect-bail-out-on-insert-dea.patch
Patch3121: 0006-netfilter-nf_conntrack_expect-consolidate-check-for-.patch
