# CVE patches shared across all Linux kernel flavours (5.10.x)
# Patch range reserved: 3000-3999
# DO NOT add non-CVE patches to this file.

# Fix CVE-2017-1000252
Patch3000: KVM-Don-t-accept-obviously-wrong-gsi-values-via-KVM_.patch

# Fix for CVE-2019-12379
Patch3001: consolemap-Fix-a-memory-leaking-bug-in-drivers-tty-v.patch

# Next 2 patches are about to be merged into stable
Patch3002: 0001-mm-fix-panic-in-__alloc_pages.patch

# Fix for CVE-2021-4204
Patch3003: 0002-bpf-Disallow-unprivileged-bpf-by-default.patch

# Fix CVE-2025-38685
Patch3004: 0001-fbdev-Fix-vmalloc-out-of-bounds-write-in-fast_imageb.patch

# Fix for CVE-2022-3522
Patch3005: 0001-mm_hugetlb_handle_pte_markers_in_page_faults.patch
Patch3006: 0002-mm_hugetlb_fix_race_condition_of_uffd_missing_minor_handling.patch
Patch3007: 0003-mm_hugetlb_use_hugetlb_pte_stable_in_migration_race_check.patch

# Fix for CVE-2024-50256
Patch3008: 0001-netfilter-nf_reject_ipv6-fix-potential-crash-in-nf_s.patch

# Fix for CVE-2021-47265
Patch3009: 0001-IB-mlx4-Use-port-iterator-and-validation-APIs.patch
Patch3010: 0002-RDMA-Verify-port-when-creating-flow-rule.patch

# Fix for CVE-2024-26830
Patch3011: 0001-i40e-Do-not-allow-untrusted-VF-to-remove-administrat.patch

# Fix for CVE-2022-0500
Patch3012: 0001-bpf-Introduce-composable-reg-ret-and-arg-types.patch
Patch3013: 0002-bpf-Replace-ARG_XXX_OR_NULL-with-ARG_XXX-PTR_MAYBE_N.patch
Patch3014: 0003-bpf-Replace-RET_XXX_OR_NULL-with-RET_XXX-PTR_MAYBE_N.patch
Patch3015: 0004-bpf-Extract-nullable-reg-type-conversion-into-a-help.patch
Patch3016: 0005-bpf-Replace-PTR_TO_XXX_OR_NULL-with-PTR_TO_XXX-PTR_M.patch
Patch3017: 0006-bpf-Introduce-MEM_RDONLY-flag.patch
Patch3018: 0007-bpf-Make-per_cpu_ptr-return-rdonly-PTR_TO_MEM.patch
Patch3019: 0008-bpf-Add-MEM_RDONLY-for-helper-args-that-are-pointers.patch

#Fix for CVE-2024-50125
Patch3020: 0001-Bluetooth-call-sock_hold-earlier-in-sco_conn_del.patch
Patch3021: 0002-Bluetooth-SCO-Fix-UAF-on-sco_sock_timeout.patch

# Fix CVE-2025-21863
Patch3022: 0001-io_uring-prevent-opcode-speculation.patch

# Fix CVE-2024-35937
Patch3023: 0001-wifi-cfg80211-check-A-MSDU-format-more-carefully.patch

# Fix CVE-2025-38512
Patch3024: 0001-wifi-prevent-A-MSDU-attacks-in-mesh-networks.patch

# Fix CVE-2026-31392
Patch3025: 0001-smb-client-fix-krb5-mount-with-username-option.patch

# Fix CVE-2024-26718
Patch3026: 0001-dm-crypt-dm-verity-disable-tasklets.patch

# Fix CVE-2024-26669
Patch3027: 0001-net-sched-flower-Fix-chain-template-offload.patch

# Fix CVE-2024-26668
Patch3028: 0001-netfilter-nft_limit-reject-configurations-that-cause.patch

#Fix for CVE-2023-0597
Patch3029: 0001-x86-mm-Randomize-per-cpu-entry-area.patch
Patch3030: 0002-x86-mm-Do-not-shuffle-CPU-entry-areas-without-KASLR.patch

#Fix CVE-2023-2176
Patch3031: 0001-RDMA-core-Refactor-rdma_bind_addr.patch

#Fix CVE-2023-22995
Patch3032: 0001-usb-dwc3-dwc3-qcom-Add-missing-platform_device_put-i.patch

#Fix CVE-2024-56604
Patch3033: 0001-Bluetooth-RFCOMM-avoid-leaving-dangling-sk-pointer-i.patch

# Fix CVE-2024-26584
Patch3034: 0001-tls-rx-simplify-async-wait.patch
Patch3035: 0001-net-tls-factor-out-tls_-crypt_async_wait.patch
Patch3036: 0001-net-tls-handle-backlogging-of-crypto-requests.patch

# Fix CVE-2024-26583
Patch3037: 0001-tls-fix-race-between-async-notify-and-socket-close.patch

# Fix CVE-2024-26585
Patch3038: 0001-tls-fix-race-between-tx-work-scheduling-and-socket-c.patch

# Fix CVE-2024-26589
Patch3039: 0001-bpf-Reject-variable-offset-alu-on-PTR_TO_FLOW_KEYS.patch

# Fix CVE-2022-49444
Patch3040: 0001-module-fix-e_shstrndx-.sh_size-0-OOB-access.patch

# Fix CVE-2024-58240
Patch3041: 0001-tls-separate-no-async-decryption-request-handling-fr.patch

# Fix CVE-2024-41071
Patch3042: 0001-wifi-mac80211-Avoid-address-calculations-via-out-of-.patch

# Fix CVE-2024-42080
Patch3043: 0001-RDMA-restrack-Fix-potential-invalid-address-access.patch

# Fix CVE-2021-47188
Patch3044: 0001-scsi-ufs-core-Improve-SCSI-abort-handling.patch

# Fix CVE-2024-44934
Patch3045: 0001-net-bridge-mcast-wait-for-previous-gc-cycles-when-re.patch

# Fix CVE-2025-21690
Patch3046: 0001-scsi-storvsc-Ratelimit-warning-logs-to-prevent-VM-de.patch

# Fix CVE-2024-27415
Patch3047: 0001-netfilter-bridge-confirm-multicast-packets-before-pa.patch

# Fix CVE-2024-27018
Patch3048: 0001-netfilter-br_netfilter-skip-conntrack-input-hook-for.patch

# Fix CVE-2023-52760
Patch3049: 0001-gfs2-make-function-gfs2_make_fs_ro-to-void-type.patch
Patch3050: 0002-gfs2-Fix-slab-use-after-free-in-gfs2_qd_dealloc.patch

# Fix CVE-2024-46834
Patch3051: 0001-ethtool-Fail-number-of-channels-change-when-it-confl.patch
Patch3052: 0002-ethtool-fail-closed-if-we-can-t-get-max-channel-used.patch

# Fix CVE-2024-41013
Patch3053: 0001-xfs-No-need-for-inode-number-error-injection-in-__xf.patch
Patch3054: 0002-xfs-don-t-walk-off-the-end-of-a-directory-data-block.patch

# Fix CVE-2024-41014
Patch3055: 0001-xfs-add-bounds-checking-to-xlog_recover_process_data.patch

# Fix CVE-2024-47673
Patch3056: 0001-wifi-iwlwifi-mvm-pause-TCM-when-the-firmware-is-stop.patch

# Fix CVE-2024-46848
Patch3057: 0001-perf-x86-intel-Limit-the-period-on-Haswell.patch

# Fix CVE-2024-46802
Patch3058: 0001-drm-amd-display-added-NULL-check-at-start-of-dc_vali.patch

# Fix CVE-2024-46816
Patch3059: 0001-drm-amd-display-handle-invalid-connector-indices.patch

# Fix CVE-2024-50014
Patch3060: 0001-ext4-fix-access-to-uninitialised-lock-in-fc-replay-p.patch

# Fix CVE-2024-50018
Patch3061: 0001-net-napi-Prevent-overflow-of-napi_defer_hard_irqs.patch

# Fix CVE-2024-50038
Patch3062: 0001-netfilter-xtables-avoid-NFPROTO_UNSPEC-where-needed.patch
Patch3063: 0002-netfilter-xtables-fix-typo-causing-some-targets-not-.patch

# Fixes CVE-2024-26661 and CVE-2024-26662
Patch3064: 0001-drm-amd-display-Fix-panel_cntl-could-be-null-in-dcn2.patch
Patch3065: 0002-drm-amd-display-Add-NULL-test-for-timing-generator-i.patch
Patch3066: 0003-drm-amd-display-Fix-vs-typos.patch

# Fix CVE-2024-26656
Patch3067: 0001-drm-amdgpu-fix-use-after-free-bug.patch

# Fix CVE-2024-26828
Patch3068: 0001-cifs-fix-underflow-in-parse_server_interfaces.patch

# Fix CVE-2024-35817
Patch3069: 0001-drm-amdgpu-amdgpu_ttm_gart_bind-set-gtt-bound-flag.patch

# Fix CVE-2024-27062
Patch3070: 0001-nouveau-lock-the-client-object-tree.patch

# Fix CVE-2024-26915
Patch3071: 0001-drm-amdgpu-Reset-IH-OVERFLOW_CLEAR-bit.patch

# Fix CVE-2024-35863
Patch3072: smb-client-fix-potential-UAF-in-is_valid_oplock_brea.patch

# Fix CVE-2024-35864
Patch3073: smb-client-fix-potential-UAF-in-smb2_is_valid_lease_.patch

# Fix CVE-2024-35865
Patch3074: smb-client-fix-potential-UAF-in-smb2_is_valid_oplock.patch

# Fix CVE-2026-43071
Patch3075: 0001-dcache-Limit-the-minimal-number-of-bucket-to-two.patch

# Fix CVE-2024-35868
Patch3076: smb-client-fix-potential-UAF-in-cifs_stats_proc_writ.patch

# Fix CVE-2024-35878
Patch3077: 0001-of-Update-of_device_get_modalias.patch
Patch3078: 0002-of-module-prevent-NULL-pointer-dereference-in-vsnpri.patch

# Fix CVE-2021-47200
Patch3079: 0001-drm-prime-Fix-use-after-free-in-mmap-with-drm_gem_tt.patch

# Fix CVE-2021-47101
Patch3080: 0001-net-asix-fix-uninit-value-bugs.patch
Patch3081: 0002-asix-fix-uninit-value-in-asix_mdio_read.patch

# Fix CVE-2023-52531
Patch3082: 0001-wifi-iwlwifi-mvm-Fix-a-memory-corruption-issue.patch

# Fix CVE-2024-49991
Patch3083: 0002-drm-amdkfd-amdkfd_free_gtt_mem-clear-the-correct-poi.patch

# Fix CVE-2026-43125
Patch3084: 0001-dlm-validate-length-in-dlm_search_rsb_tree.patch

# Fix CVE-2026-43198
Patch3085: 0001-tcp-fix-potential-race-in-tcp_v6_syn_recv_sock.patch

# Fix CVE-2023-52621
Patch3086: 0005-bpf-Allow-RCU-protected-lookups-to-happen-from-bh-co.patch

# Fix CVE-2024-35839
Patch3087: 0001-netfilter-nfnetlink_log-use-proper-helper-for-fetchi.patch
Patch3088: 0002-netfilter-nf_queue-remove-excess-nf_bridge-variable.patch
Patch3089: 0003-netfilter-propagate-net-to-nf_bridge_get_physindev.patch
Patch3090: 0004-netfilter-bridge-replace-physindev-with-physinif-in-.patch

# Fix CVE-2022-49651
Patch3091: 0001-srcu-Tighten-cleanup_srcu_struct-GP-checks.patch

# Fix CVE-2024-57795
Patch3092: 0001-RDMA-rxe-Remove-the-direct-link-to-net_device.patch
Patch3093: 0002-RDMA-rxe-Fix-the-failure-of-ibv_query_device-and-ibv.patch

# Fix CVE-2024-27056
Patch3094: 0001-iwlwifi-mvm-don-t-check-system_pm_mode-without-mutex.patch
Patch3095: 0002-wifi-iwlwifi-mvm-fix-mvmtxq-stopped-handling.patch
Patch3096: 0003-wifi-iwlwifi-mvm-fix-double-list_add-at-iwl_mvm_mac_.patch
Patch3097: 0004-wifi-iwlwifi-mvm-protect-TXQ-list-manipulation.patch
Patch3098: 0005-wifi-iwlwifi-mvm-ensure-offloading-TID-queue-exists.patch

# Fix CVE-2025-21759
Patch3099: 0001-ipv6-mcast-extend-RCU-protection-in-igmp6_send.patch

# Fix CVE-2021-47432
Patch3100: 0001-lib-generic-radix-tree.c-Don-t-overflow-in-peek.patch

# Fix CVE-2021-47182
Patch3101: 0001-scsi-core-Fix-scsi_mode_sense-buffer-length-handling.patch

# Fix CVE-2024-57982
Patch3102: 0001-xfrm-state-fix-out-of-bounds-read-during-lookup.patch

# Fix CVE-2022-49226
Patch3103: 0001-net-asix-add-proper-error-handling-of-usb-read-error.patch

# Fix CVE-2024-40999
Patch3104: 0001-net-ena-Add-validation-for-completion-descriptors-co.patch
Patch3105: 0001-net-ena-add-device-distinct-log-prefix-to-files.patch

# CVE-2022-48816
Patch3106: 0001-SUNRPC-lock-against-sock-changing-during-sysfs-read.patch

# Fix CVE-2025-38728
Patch3107: 0001-smb3-fix-for-slab-out-of-bounds-on-mount-to-ksmbd.patch

# CVE-2025-68190
Patch3108: 0001-drm-amdgpu-atom-Check-kcalloc-for-WS-buffer-in-amdgp.patch

# Fix CVE-2024-42321
Patch3109: 0001-net-flow_dissector-use-DEBUG_NET_WARN_ON_ONCE.patch

# Fix CVE-2024-38608
Patch3110: 0001-net-mlx5e-Fix-netif-state-handling.patch

# Fix CVE-2024-57798
Patch3111: 0001-drm-dp_mst-Skip-CSN-if-topology-probing-is-not-done-.patch
Patch3112: 0001-drm-dp_mst-Ensure-mst_primary-pointer-is-valid-in-dr.patch

# Fix CVE-2024-36898
Patch3113: 0001-gpiolib-cdev-fix-uninitialised-kfifo.patch

# Fix CVE-2024-35932
Patch3114: 0001-drm-vc4-don-t-check-if-plane-state-fb-state-fb.patch

# Fix CVE-2024-38564
Patch3115: 0001-bpf-Add-BPF_PROG_TYPE_CGROUP_SKB-attach-type-enforce.patch

# Fix CVE-2024-38556
Patch3116: 0001-net-mlx5-Add-a-timeout-to-acquire-the-command-queue-.patch

# Fix CVE-2024-26792
Patch3117: 0001-btrfs-fix-double-free-of-anonymous-device-after-snap.patch

# Fix CVE-2024-57876
Patch3118: 0001-drm-dp_mst-Fix-resetting-msg-rx-state-after-topology.patch

# Fix CVE-2024-56551
Patch3119: 0001-drm-amdgpu-fix-usage-slab-after-free.patch

# Fix CVE-2024-53168
Patch3120: 0001-sunrpc-fix-one-UAF-issue-caused-by-sunrpc-kernel-tcp.patch

# Fix CVE-2023-53597
Patch3121: 0001-cifs-fix-mid-leak-during-reconnection-after-timeout-.patch

# Fix CVE-2025-39990
Patch3122: 0001-bpf-Check-the-helper-function-is-valid-in-get_helper.patch

# Fix CVE-2022-49635
Patch3123: 0001-drm-i915-selftests-fix-subtraction-overflow-bug.patch

# Fix CVE-2025-40099
Patch3124: 0001-cifs-parse_dfs_referrals-prevent-oob-on-malformed-in.patch

# Fix CVE-2022-50406
Patch3125: 0001-iomap-iomap-fix-memory-corruption-when-recording-err.patch

# Fix CVE-2025-39838
Patch3126: 0001-cifs-prevent-NULL-pointer-dereference-in-UTF16-conve.patch

# Fix CVE-2025-38068
Patch3127: 0001-lib-lzo-lzo1x_compress.c-make-lzogeneric1x_1_compres.patch
Patch3128: 0002-lib-lzo-lzo1x_compress.c-replace-ternary-operator-wi.patch
Patch3129: 0003-crypto-lzo-Fix-compression-buffer-overrun.patch

# CVE-2023-53111
Patch3130: 0001-loop-Fix-use-after-free-issues.patch

# CVE-2025-68379
Patch3131: 0001-RDMA-rxe-Fix-null-deref-on-srq-rq.queue-after-resize.patch

# Fix CVE-2024-35939
Patch3132: 0001-dma-direct-Leak-pages-on-dma_set_decrypted-failure.patch

# Fix CVE-2023-53401
Patch3133: 0001-mm-kmem-fix-a-NULL-pointer-dereference-in-obj_stock_.patch
Patch3134: 0002-mm-memcg-use-READ_ONCE-WRITE_ONCE-to-access-stock-ca.patch

# Fix CVE-2022-49935
Patch3135: 0001-dma-buf-dma-resv-check-if-the-new-fence-is-really-la.patch
Patch3136: 0002-dma-buf-fix-check-in-dma_resv_add_fence.patch

# Fix CVE-2022-49961
Patch3137: 0001-bpf-Do-mark_chain_precision-for-ARG_CONST_ALLOC_SIZE.patch

# Fix CVE-2025-38527
Patch3138: 0001-smb-client-fix-use-after-free-in-cifs_oplock_break.patch

# Fix CVE-2025-40149
Patch3139: 0001-net-Add-locking-to-protect-skb-dev-access-in-ip_outp.patch
Patch3140: 0002-net-netdevice-Add-operation-ndo_sk_get_lower_dev.patch
Patch3141: 0003-tls-Use-__sk_dst_get-and-dst_dev_rcu-in-get_netdev_f.patch

# Fix CVE-2025-40135
Patch3142: 0001-ipv6-use-RCU-in-ip6_xmit.patch

# Fix CVE-2025-39797
Patch3143: 0001-xfrm-Duplicate-SPI-Handling.patch
Patch3144: 0001-xfrm-xfrm_alloc_spi-shouldn-t-use-0-as-SPI.patch

# CVE-2025-39810
Patch3145: 0001-bnxt_en-Fix-possible-crash-after-creating-sw-mqprio-.patch
Patch3146: 0002-bnxt_en-Fix-memory-corruption-when-FW-resources-chan.patch

# CVE-2023-53282
Patch3147: 0001-scsi-lpfc-Fix-use-after-free-KFENCE-violation-during.patch

# CVE-2025-38129
Patch3148: 0001-page_pool-fix-inconsistency-for-page_pool_ring_-un-l.patch
Patch3149: 0002-page_pool-Fix-use-after-free-in-page_pool_recycle_in.patch

# CVE-2022-49622
Patch3150: 0001-netfilter-nf_tables-avoid-skb-access-on-nf_stolen.patch
Patch3151: 0002-netfilter-nf_tables-fix-crash-when-nf_trace-is-enabl.patch

# CVE-2025-68188
Patch3152: 0001-tcp-use-dst_dev_rcu-in-tcp_fastopen_active_disable_o.patch

# CVE-2025-68283
Patch3153: 0001-libceph-replace-BUG_ON-with-bounds-check-for-map-max.patch

# CVE-2023-53510
Patch3154: 0001-scsi-ufs-core-Fix-handling-of-lrbp-cmd.patch

# CVE-2025-39901
Patch3155: 0001-i40e-replace-snprintf-with-scnprintf-in-debugfs.patch

#CVE-2023-54202
Patch3156: 0001-drm-i915-fix-race-condition-UAF-in-i915_perf_add_con.patch

#CVE-2023-53794
Patch3157: 0001-cifs-fix-session-state-check-in-reconnect-to-avoid-u.patch

# Fix CVE-2023-53441
Patch3158: 0001-bpf-cpumap-Fix-memory-leak-in-cpu_map_update_elem.patch

# Fix CVE-2023-53577
Patch3159: 0001-bpf-cpumap-Make-sure-kthread-is-running-before-map-u.patch

# CVE-2023-53867
Patch3160: 0001-ceph-drop-private-list-from-remove_session_caps_cb.patch
Patch3161: 0002-ceph-fix-auth-cap-handling-logic-in-remove_session_c.patch
Patch3162: 0003-ceph-fix-potential-use-after-free-bug-when-trimming-.patch

# CVE-2024-47745
Patch3163: 0001-i915_vma-Rename-vma_lookup-to-i915_vma_lookup.patch
Patch3164: 0001-mm-add-vma_lookup-update-find_vma_intersection-comme.patch
Patch3165: 0001-mm-mmap.c-don-t-unlock-VMAs-in-remap_file_pages.patch
Patch3166: 0002-mm-call-the-security_mmap_file-LSM-hook-in-remap_fil.patch
Patch3167: 0003-mm-split-critical-region-in-remap_file_pages-and-inv.patch

# CVE-2026-23069
Patch3168: 0001-vsock-virtio-fix-potential-underflow-in-virtio_trans.patch

# CVE-2026-23086
Patch3169: 0002-vsock-virtio-cap-TX-credit-to-local-buffer-size.patch

# CVE-2025-39738
Patch3170: 0001-btrfs-do-not-allow-relocation-of-partially-dropped-s.patch

# CVE-2025-40362
Patch3171: 0001-ceph-fix-multifs-mds-auth-caps-issue.patch

# CVE-2026-23189
Patch3172: 0001-ceph-fix-NULL-pointer-dereference-in-ceph_mds_auth_m.patch

# CVE-2026-23231
Patch3173: 0001-netfilter-nf_tables-register-hooks-last-when-adding-.patch
Patch3174: 0002-netfilter-nf_tables-fix-use-after-free-in-nf_tables_.patch

# Fix CVE-2026-45850
Patch3175: 0001-ipvs-skip-ipv6-extension-headers-for-csum-checks.patch

# Fix CVE-2026-46191
Patch3176: 0001-fbcon-Avoid-OOB-font-access-if-console-rotation-fails.patch

# Fix CVE-2026-43304
Patch3177: 0001-libceph-define-and-enforce-CEPH_MAX_KEY_LEN.patch

# Fix CVE-2026-43456
Patch3178: 0001-bonding-fix-type-confusion-in-bond_setup_by_slave.patch
Patch3179: 0001-bonding-prevent-potential-infinite-loop-in-bond_head.patch

# Fix CVE-2026-43091
Patch3180: 0001-xfrm-Wait-for-RCU-readers-during-policy-netns-exit.patch

# Fix CVE-2026-46119
Patch3181: 0001-libceph-Fix-slab-out-of-bounds-access-in-auth-messag.patch

# Fix CVE-2024-26904
Patch3182: 0001-btrfs-fix-data-race-at-btrfs_use_block_rsv.patch

# Fix CVE-2026-23099
Patch3183: 0001-bonding-limit-BOND_MODE_8023AD-to-Ethernet-devices.patch

# Fix CVE-2026-23204
Patch3184: 0001-net-add-skb_header_pointer_careful-helper.patch
Patch3185: 0002-net-sched-cls_u32-use-skb_header_pointer_careful.patch

# CVE-2026-23221
Patch3186: 0001-bus-fsl-mc-Replace-snprintf-and-sprintf-with-sysfs_e.patch
Patch3187: 0002-fsl-mc-Use-driver_set_override-instead-of-open-codin.patch
Patch3188: 0003-bus-fsl-mc-fix-use-after-free-in-driver_override_sho.patch

# CVE-2026-31527
Patch3189: 0001-driver-core-generalize-driver_override-in-struct-dev.patch
Patch3190: 0002-driver-core-platform-use-generic-driver_override-inf.patch

# Fix CVE-2026-31516
Patch3191: 0001-xfrm-prevent-policy_hthresh.work-from-racing-with-ne.patch

# Fix CVE-2026-31419
Patch3192: 0001-net-bonding-fix-use-after-free-in-bond_xmit_broadcas.patch
