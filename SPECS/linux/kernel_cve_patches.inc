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
Patch3009: 0001-tcp-Add-preempt_-disable-enable-_nest.patch
Patch3010: 0002-sctp-validate-embedded-INIT-chunk-and.patch
Patch3011: 0003-sctp-add-INIT-verification-after-cookie-unpacking.patch
# Fixes CVE-2026-43197, CVE-2026-43198
Patch3012: 0001-netconsole-avoid-OOB-reads-msg-is-not-nul-terminated.patch
Patch3013: 0001-tcp-fix-potential-race-in-tcp_v6_syn_recv_sock.patch
# Fixes CVE-2025-40074, CVE-2025-68353, CVE-2026-23208, CVE-2026-43009, CVE-2026-43485
Patch3014: 0001-ALSA-usb-audio-Prevent-excessive-number-of-frames.patch
Patch3015: 0001-bpf-Fix-incorrect-pruning-due-to-atomic-fetch-precis.patch
Patch3016: 0001-ipv4-start-using-dst_dev_rcu.patch
Patch3017: 0001-net-vxlan-prevent-NULL-deref-in-vxlan_xmit_one.patch
Patch3018: 0001-nouveau-gsp-drop-WARN_ON-in-ACPI-probes.patch
Patch3019: 0002-ALSA-usb-audio-Use-the-right-limit-for-PCM-OOB-check.patch
