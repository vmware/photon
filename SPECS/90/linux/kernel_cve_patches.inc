# CVE patches shared across all Linux kernel flavours
# Patch range reserved: 3000–3999
# DO NOT add non-CVE patches to this file.

# Fix CVE-2017-1000252
Patch3000: KVM-Don-t-accept-obviously-wrong-gsi-values-via-KVM_.patch

# Fix CVE-2023-0597
Patch3001: 0001-x86-mm-Randomize-per-cpu-entry-area.patch
Patch3002: 0002-x86-mm-Do-not-shuffle-CPU-entry-areas-without-KASLR.patch

# Fix CVE-2023-39191 [3005..3023]
Patch3005: 0001-bpf-Refactor-ARG_PTR_TO_DYNPTR-checks-into-process_d.patch
Patch3006: 0002-bpf-Rework-process_dynptr_func.patch
Patch3007: 0003-bpf-Rename-RET_PTR_TO_ALLOC_MEM.patch
Patch3008: 0004-bpf-Rework-check_func_arg_reg_off.patch
Patch3009: 0005-bpf-Use-memmove-for-bpf_dynptr_-read-write.patch
Patch3010: 0006-bpf-Propagate-errors-from-process_-checks-in-check_f.patch
Patch3011: 0007-bpf-Move-PTR_TO_STACK-alignment-check-to-process_dyn.patch
Patch3012: 0008-bpf-Fix-state-pruning-for-STACK_DYNPTR-stack-slots.patch
Patch3013: 0009-bpf-Fix-missing-var_off-check-for-ARG_PTR_TO_DYNPTR.patch
Patch3014: 0010-bpf-Fix-partial-dynptr-stack-slot-reads-writes.patch
Patch3015: 0011-bpf-Invalidate-slices-on-destruction-of-dynptrs-on-s.patch
Patch3016: 0012-bpf-Allow-reinitializing-unreferenced-dynptr-stack-s.patch
Patch3017: 0013-bpf-Combine-dynptr_get_spi-and-is_spi_bounds_valid.patch
Patch3018: 0014-selftests-bpf-convenience-macro-for-use-with-asm-vol.patch
Patch3019: 0015-selftests-bpf-Add-test-for-dynptr-reinit-in-user_rin.patch
Patch3020: 0016-selftests-bpf-Add-dynptr-pruning-tests.patch
Patch3021: 0017-selftests-bpf-Add-dynptr-var_off-tests.patch
Patch3022: 0018-selftests-bpf-Add-dynptr-partial-slot-overwrite-test.patch
Patch3023: 0019-selftests-bpf-Add-dynptr-helper-tests.patch

# Fix CVE-2024-46811

# Fix CVE-2024-35949
Patch3030: 0001-btrfs-make-sure-that-WRITTEN-is-set-on-all-metadata-.patch

# Fix CVE-2024-46834
Patch3031: 0001-ethtool-Fail-number-of-channels-change-when-it-confl.patch
# Fix CVE-2024-38564
Patch3034: 0001-bpf-Add-attach_type-checks-under-bpf_prog_attach_che.patch
# Fix CVE-2024-50018
Patch3037: 0001-net-napi-Prevent-overflow-of-napi_defer_hard_irqs.patch

# Fix CVE-2024-27042
Patch3044: 0001-drm-amdgpu-Fix-potential-out-of-bounds-access-in-amd.patch

# Fix CVE-2024-26944
Patch3050: 0001-btrfs-zoned-fix-use-after-free-in-do_zone_finish.patch

# Fix CVE-2024-57795
Patch3051: 0001-RDMA-rxe-Remove-the-direct-link-to-net_device.patch
Patch3052: 0001-RDMA-rxe-Fix-the-failure-of-ibv_query_device-and-ibv.patch

# Fix CVE-2024-49988

# Fix CVE-2025-38039
Patch3058: 0001-net-mlx5e-Avoid-WARN_ON-when-configuring-MQPRIO-with.patch

# Fix CVE-2025-39990
Patch3061: 0001-bpf-Check-the-helper-function-is-valid-in-get_helper.patch

# Fix CVE-2025-2312
Patch3063: 0001-CIFS-New-mount-option-for-cifs.upcall-namespace-reso.patch

Patch3065: 0002-rcu-Fix-racy-re-initialization-of-irq_work-causing-h.patch

Patch3068: 0001-xfrm-xfrm_alloc_spi-shouldn-t-use-0-as-SPI.patch

# Fix CVE-2025-39810
Patch3070: 0001-bnxt_en-Fix-possible-crash-after-creating-sw-mqprio-.patch

# CVE-2024-53177
Patch3071: 0004-smb-prevent-use-after-free-due-to-open_cached_dir-er.patch
Patch3072: 0001-smb-client-prevent-new-fids-from-being-removed-by-la.patch

Patch3077: 0002-ceph-fix-multifs-mds-auth-caps-issue.patch

# CVE-2025-39905
Patch3078: 0001-net-phylink-add-lock-for-serializing-concurrent-pl-p.patch

# Fix CVE-2025-68353
Patch3085: 0001-net-vxlan-prevent-NULL-deref-in-vxlan_xmit_one.patch

# Fix CVE-2024-25742 and CVE-2024-25743
Patch3088: 0001-x86-sev-Harden-VC-instruction-emulation-somewhat.patch

# Fix CVE-2026-31648
Patch3094: 0001-mm-filemap-fix-nr_pages-calculation-overflow-in-file.patch
Patch3095: 0001-xfrm-hold-device-only-for-asynchronous-decryption.patch
Patch3096: 0001-xfrm-Fix-dev-use-after-free-in-xfrm-async-resumption.patch

# Prerequisite for CVE-2026-31663

# Fixes Patch3048 (CVE-2024-26661) and Patch3049 (CVE-2024-26662)

# Fix CVE-2026-31527
Patch3103: 0001-driver-core-generalize-driver_override-in-struct-dev.patch
Patch3104: 0001-driver-core-platform-use-generic-driver_override-inf.patch

# Fix CVE-2026-31516

Patch3122: 0002-net-sched-netem-handle-multi-segment-skb-in-corrupti.patch
Patch3124: 0001-netfilter-conntrack-check-NULL-when-retrieving-ct-ex.patch
Patch3128: 0004-netfilter-nf_conntrack_expect-add-and-use-nf_ct_expe.patch
Patch3129: 0005-netfilter-nf_conntrack_expect-bail-out-on-insert-dea.patch
Patch3130: 0006-netfilter-nf_conntrack_expect-consolidate-check-for-.patch
# Fixes CVE-2026-53091, CVE-2026-53120, CVE-2026-98034, CVE-2026-98103
Patch3131: 0001-PCI-use-generic-driver_override-infrastructure.patch
Patch3132: 0001-bpf-Mark-NULL-kptr-stores-precise.patch
Patch3133: 0001-igmp-convert-struct-ip_sf_list-to-RCU.patch
Patch3134: 0001-net-do-not-use-skb_mac_header-in-qdisc_pkt_len_init.patch
Patch3135: 0002-net-pull-headers-in-qdisc_pkt_len_segs_init.patch
Patch3136: 0003-net-reject-a-negative-TCP-header-offset-in-qdisc_pkt.patch
