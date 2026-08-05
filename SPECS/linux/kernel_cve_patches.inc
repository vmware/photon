# CVE patches shared across all Linux kernel flavours
# Patch range reserved: 3000–3999
# DO NOT add non-CVE patches to this file.

# Fix CVE-2017-1000252
Patch3000: KVM-Don-t-accept-obviously-wrong-gsi-values-via-KVM_.patch

# Fix CVE-2026-43083
Patch3001: 0001-net-ioam6-fix-OOB-and-missing-lock.patch

# Fix CVE-2025-68359
Patch3002: 0001-btrfs-fix-double-free-of-qgroup-record-after-failure.patch

# Fix CVE-2026-43101
Patch3003: 0001-ipv6-adopt-skb_dst_dev-and-skb_dst_dev_net-_rcu-help.patch
Patch3004: 0002-ipv6-ioam-fix-potential-NULL-dereferences-in-__ioam6.patch
# Fixes CVE-2026-31589, CVE-2026-43414, CVE-2026-43465, CVE-2026-53224, CVE-2026-53246, CVE-2026-53260
Patch3005: 0001-mm-call-free_folio-directly-in-folio_.patch
Patch3006: 0001-net-mlx5e-RX-Fix-XDP-multi-buf-frag-c.patch
Patch3007: 0001-scsi-qla2xxx-Completely-fix-fcport-do.patch
Patch3008: 0001-sctp-validate-cached-peer-INIT-chunk-length-in-COOKI.patch
Patch3010: 0002-sctp-validate-embedded-INIT-chunk-and.patch
Patch3011: 0003-sctp-add-INIT-verification-after-cookie-unpacking.patch
Patch3013: 0001-tcp-fix-potential-race-in-tcp_v6_syn_recv_sock.patch
# Fixes CVE-2025-40074, CVE-2025-68353, CVE-2026-23208, CVE-2026-43009, CVE-2026-43485
Patch3014: 0001-ALSA-usb-audio-Prevent-excessive-number-of-frames.patch
Patch3015: 0001-bpf-Fix-incorrect-pruning-due-to-atomic-fetch-precis.patch
Patch3016: 0001-ipv4-start-using-dst_dev_rcu.patch
Patch3017: 0001-net-vxlan-prevent-NULL-deref-in-vxlan_xmit_one.patch
Patch3018: 0001-nouveau-gsp-drop-WARN_ON-in-ACPI-probes.patch
Patch3019: 0002-ALSA-usb-audio-Use-the-right-limit-for-PCM-OOB-check.patch
# Fixes CVE-2025-40158, CVE-2025-68745, CVE-2026-63872, CVE-2026-64076, CVE-2026-64077
Patch3020: 0001-esp-fix-page-frag-reference-leak-on-skb_to_sgvec-failure.patch
Patch3021: 0001-ipv6-use-RCU-in-ip6_output.patch
Patch3022: 0001-netfilter-bridge-eb_tables-close-module-init-race.patch
Patch3023: 0001-netfilter-ebtables-move-to-two-stage-removal-scheme.patch
Patch3024: 0001-scsi-qla2xxx-Clear-cmds-after-chip-reset.patch
# Fixes CVE-2026-52988, CVE-2026-52991, CVE-2026-53089, CVE-2026-53091
Patch3025: 0001-bpf-Fix-use-after-free-in-offloaded-map-prog-info-fi.patch
Patch3026: 0001-cgroup-psi-Set-of-priv-to-NULL-upon-file-release.patch
Patch3027: 0001-rculist-add-list_splice_rcu-for-private-lists.patch
Patch3028: 0002-netfilter-nf_tables-join-hook-list-via-splice_list_r.patch
Patch3029: 0002-sched-psi-fix-race-between-file-release-and-pressure.patch
Patch3030: 0001-net_sched-make-room-for-struct-qdisc_skb_cb-pkt_segs.patch
Patch3031: 0002-net-init-shinfo-gso_segs-from-qdisc_pkt_len_init.patch
Patch3032: 0003-net_sched-initialize-qdisc_skb_cb-skb-pkt_segs-in-qd.patch
Patch3033: 0004-net-use-qdisc_pkt_len_segs_init-in-sch_handle_ingres.patch
Patch3034: 0005-net-dropreason-add-SKB_DROP_REASON_RECURSION_LIMIT.patch
Patch3035: 0006-net-plumb-drop-reasons-to-__dev_queue_xmit.patch
Patch3036: 0007-net-qdisc_pkt_len_segs_init-cleanup.patch
Patch3037: 0008-net-pull-headers-in-qdisc_pkt_len_segs_init.patch
Patch3038: 0009-xfrm-Do-not-clobber-inner-headers-when-already-set.patch
