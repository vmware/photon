# CVE patches shared across all Linux kernel flavours
# Patch range reserved: 3000–3999
# DO NOT add non-CVE patches to this file.

# Fix CVE-2017-1000252
Patch3000: KVM-Don-t-accept-obviously-wrong-gsi-values-via-KVM_.patch

# Fix CVE-2023-0597
Patch3001: 0001-x86-mm-Randomize-per-cpu-entry-area.patch
Patch3002: 0002-x86-mm-Do-not-shuffle-CPU-entry-areas-without-KASLR.patch

# Fix CVE-2024-38557
Patch3003: 0003-net-mlx5-Reload-only-IB-representors-upon-lag-disabl.patch

# Fix CVE-2024-56729
Patch3004: 0004-smb-Initialize-cfid-tcon-before-performing-network-o.patch

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

# Fix CVE-2023-52452
Patch3024: 0001-bpf-Fix-accesses-to-uninit-stack-slots.patch

# Fix CVE-2024-46813
Patch3025: 0001-drm-amd-display-Check-link_index-before-accessing-dc.patch

# Fix CVE-2024-50029
Patch3026: 0001-Bluetooth-hci_conn-Fix-UAF-in-hci_enhanced_setup_syn.patch

# Fix CVE-2025-39901
Patch3027: 0001-i40e-remove-read-access-to-debugfs-files.patch

# Fix CVE-2024-41045
Patch3028: 0001-bpf-Defer-work-in-bpf_timer_cancel_and_free.patch

# Fix CVE-2024-46811
Patch3029: 0001-drm-amd-display-Fix-index-may-exceed-array-range-wit.patch

# Fix CVE-2024-35949
Patch3030: 0001-btrfs-make-sure-that-WRITTEN-is-set-on-all-metadata-.patch

# Fix CVE-2024-46834
Patch3031: 0001-ethtool-Fail-number-of-channels-change-when-it-confl.patch
Patch3032: 0002-ethtool-fail-closed-if-we-can-t-get-max-channel-used.patch

# Fix CVE-2024-56611
Patch3033: 0001-mm-mempolicy-fix-migrate_to_node-assuming-there-is-a.patch

# Fix CVE-2024-38564
Patch3034: 0001-bpf-Add-attach_type-checks-under-bpf_prog_attach_che.patch
Patch3035: 0002-bpf-Add-BPF_PROG_TYPE_CGROUP_SKB-attach-type-enforce.patch

# Fix CVE-2025-38636
Patch3036: 0001-rv-Use-strings-in-da-monitors-tracepoints.patch

# Fix CVE-2024-50018
Patch3037: 0001-net-napi-Prevent-overflow-of-napi_defer_hard_irqs.patch

# Fix CVE-2025-21759
Patch3038: 0001-ipv6-mcast-extend-RCU-protection-in-igmp6_send.patch

# Fix CVE-2025-21714
Patch3039: 0001-RDMA-mlx5-Fix-implicit-ODP-use-after-free.patch
Patch3040: 0001-RDMA-mlx5-Fix-implicit-ODP-hang-on-parent-deregistra.patch

# Fix CVE-2024-53179
Patch3041: 0001-smb-client-fix-use-after-free-of-signing-key.patch

# Fix CVE-2024-53168
Patch3042: 0001-sunrpc-fix-one-UAF-issue-caused-by-sunrpc-kernel-tcp.patch

# Fix CVE-2025-21969
Patch3043: 0001-Bluetooth-L2CAP-Fix-slab-use-after-free-Read-in-l2ca.patch

# Fix CVE-2024-27042
Patch3044: 0001-drm-amdgpu-Fix-potential-out-of-bounds-access-in-amd.patch

# Fix CVE-2024-26669
Patch3045: 0001-net-sched-flower-Fix-chain-template-offload.patch

# Fix CVE-2024-57982
Patch3046: 0001-xfrm-state-fix-out-of-bounds-read-during-lookup.patch

# Fix CVE-2023-52653
Patch3047: 0001-SUNRPC-fix-a-memleak-in-gss_import_v2_context.patch

# Fix CVE-2024-26661
Patch3048: 0001-drm-amd-display-Add-NULL-test-for-timing-generator-i.patch

# Fix CVE-2024-26662
Patch3049: 0001-drm-amd-display-Fix-panel_cntl-could-be-null-in-dcn2.patch

# Fix CVE-2024-26944
Patch3050: 0001-btrfs-zoned-fix-use-after-free-in-do_zone_finish.patch

# Fix CVE-2024-57795
Patch3051: 0001-RDMA-rxe-Remove-the-direct-link-to-net_device.patch
Patch3052: 0001-RDMA-rxe-Fix-the-failure-of-ibv_query_device-and-ibv.patch

# Fix CVE-2025-39705
Patch3053: 0001-drm-amd-display-fix-a-Null-pointer-dereference-vulne.patch

# Fix CVE-2025-38705
Patch3054: 0001-drm-amd-pm-fix-null-pointer-access.patch

# Fix CVE-2024-49922
Patch3055: 0001-drm-amd-display-Check-null-pointers-before-using-the.patch

# Fix CVE-2024-49988
Patch3056: 0001-ksmbd-add-refcnt-to-ksmbd_conn-struct.patch
Patch3057: 0002-ksmbd-fix-use-after-free-in-SMB-request-handling.patch

# Fix CVE-2025-38039
Patch3058: 0001-net-mlx5e-Avoid-WARN_ON-when-configuring-MQPRIO-with.patch

# Fix CVE-2025-38064
Patch3059: 0001-virtio-break-and-reset-virtio-devices-on-device_shut.patch

# Fix CVE-2025-38045
Patch3060: 0001-wifi-iwlwifi-fix-debug-actions-order.patch

# Fix CVE-2025-39990
Patch3061: 0001-bpf-Check-the-helper-function-is-valid-in-get_helper.patch

# Fix CVE-2025-37750
Patch3062: 0001-smb-client-fix-UAF-in-decryption-with-multichannel.patch

# Fix CVE-2025-2312
Patch3063: 0001-CIFS-New-mount-option-for-cifs.upcall-namespace-reso.patch

# Fix CVE-2025-39744
Patch3064: 0001-rcu-Fix-rcu_read_unlock-deadloop-due-to-IRQ-work.patch
Patch3065: 0002-rcu-Fix-racy-re-initialization-of-irq_work-causing-h.patch

# Fix CVE-2025-38248
Patch3066: 0001-bridge-mcast-fix-use-after-free-during-router-port-configuration.patch

# Fix CVE-2025-39797
Patch3067: 0001-xfrm-Duplicate-SPI-Handling.patch
Patch3068: 0001-xfrm-xfrm_alloc_spi-shouldn-t-use-0-as-SPI.patch

# Fix CVE-2025-38616
Patch3069: 0001-tls-handle-data-disappearing-from-under-the-TLS-ULP.patch

# Fix CVE-2025-39810
Patch3070: 0001-bnxt_en-Fix-possible-crash-after-creating-sw-mqprio-.patch
Patch3071: 0002-bnxt_en-Fix-memory-corruption-when-FW-resources-chan.patch

# CVE-2024-53177
Patch3072: 0001-smb-client-prevent-new-fids-from-being-removed-by-la.patch
Patch3073: 0002-smb-client-fix-use-after-free-in-smb2_query_info_com.patch
Patch3074: 0003-smb-Don-t-leak-cfid-when-reconnect-races-with-open_c.patch
Patch3075: 0004-smb-prevent-use-after-free-due-to-open_cached_dir-er.patch

# CVE-2025-40362
Patch3076: 0001-ceph-pass-the-mdsc-to-several-helpers.patch
Patch3077: 0002-ceph-fix-multifs-mds-auth-caps-issue.patch

# CVE-2025-39905
Patch3078: 0001-net-phylink-add-lock-for-serializing-concurrent-pl-p.patch

# CVE-2024-53095
Patch3079: 0001-smb-client-Fix-use-after-free-of-network-namespace.patch

# CVE-2025-68188
Patch3080: 0001-tcp-use-dst_dev_rcu-in-tcp_fastopen_active_disable_o.patch

# CVE-2025-68379
Patch3081: 0001-RDMA-rxe-Fix-null-deref-on-srq-rq.queue-after-resize.patch

# CVE-2025-40328
Patch3082: 0001-smb-client-fix-potential-UAF-in-smb2_close_cached_fi.patch

# CVE-2025-68219
Patch3083: 0001-cifs-fix-memory-leak-in-smb3_fs_context_parse_param-.patch

# CVE-2025-71068
Patch3084: 0001-svcrdma-bound-check-rq_pages-index-in-inline-path.patch

# Fix CVE-2025-68353
Patch3085: 0001-net-vxlan-prevent-NULL-deref-in-vxlan_xmit_one.patch

# CVE-2023-54271
Patch3086: 0001-blk-cgroup-Fix-NULL-deref-caused-by-blkg_policy_data.patch

# Fix CVE-2025-68190
Patch3087: 0001-drm-amdgpu-atom-Check-kcalloc-for-WS-buffer-in-amdgp.patch

# Fix CVE-2024-25742 and CVE-2024-25743
Patch3088: 0001-x86-sev-Harden-VC-instruction-emulation-somewhat.patch

# Fix CVE-2025-71184
Patch3089: 0001-btrfs-fix-NULL-dereference-on-root-when-tracing-inod.patch

# Fix CVE-2024-53068
Patch3090: 0001-firmware-arm_scmi-Fix-slab-use-after-free-in-scmi_bu.patch

# Fix CVE-2025-38081
Patch3091: 0001-spi-rockchip-Fix-register-out-of-bounds-access.patch

# CVE-2026-23171
Patch3092: 0001-bonding-fix-use-after-free-due-to-enslave-fail-after-slave-array-update.patch

# Fix CVE-2026-23447
Patch3093: 0001-net-usb-cdc_ncm-add-ndpoffset-to-NDP32-nframes-bound.patch

# Fix CVE-2026-31648
Patch3094: 0001-mm-filemap-fix-nr_pages-calculation-overflow-in-file.patch

# Prerequisite for CVE-2026-31663
Patch3095: 0001-xfrm-hold-device-only-for-asynchronous-decryption.patch

# Fix CVE-2026-31663
Patch3096: 0001-xfrm-hold-dev-ref-until-after-transport_finish-NF_HO.patch

# Fixes Patch3048 (CVE-2024-26661) and Patch3049 (CVE-2024-26662)
Patch3097: 0001-drm-amd-display-Fix-vs-typos.patch

# Fix CVE-2026-43414
Patch3098: 0001-scsi-qla2xxx-Completely-fix-fcport-double-free.patch

# Fix CVE-2026-23272
Patch3099: 0001-netfilter-nf_tables-always-increment-set-element-cou.patch
Patch3100: 0002-netfilter-nf_tables-fix-set-size-with-rbtree-backend.patch
Patch3101: 0003-netfilter-nf_tables-unconditionally-bump-set-nelems-.patch

# Fix CVE-2026-23239
Patch3102: 0001-espintcp-Fix-race-condition-in-espintcp_close.patch

# Fix CVE-2026-31527
Patch3103: 0001-driver-core-generalize-driver_override-in-struct-dev.patch
Patch3104: 0001-driver-core-platform-use-generic-driver_override-inf.patch

# Fix CVE-2026-31516
Patch3105: 0001-xfrm-prevent-policy_hthresh.work-from-racing-with-ne.patch

# Fix CVE-2026-43239
Patch3106: 0001-smb-client-prevent-races-in-query_interfaces.patch

# Fix CVE-2026-43215
Patch3107: 0001-cifs-Fix-locking-usage-for-tcon-fields.patch

# Fix CVE-2026-43125
Patch3108: 0001-dlm-validate-length-in-dlm_search_rsb_tree.patch

# Fix CVE-2026-31709
Patch3109: 0001-smb-client-validate-dacloffset-before-building-DACL-.patch
Patch3110: 0002-smb-client-validate-the-whole-DACL-before-rewriting-.patch

# Fix CVE-2026-43249
Patch3111: 0001-9p-xen-protect-xen_9pfs_front_free-against-concurren.patch

# Fix CVE-2026-23278
Patch3112: 0001-netfilter-nf_tables-always-walk-all-pending-catchall.patch

# Fix CVE-2026-31505
Patch3113: 0001-iavf-fix-out-of-bounds-writes-in-iavf_get_ethtool_st.patch
# Fix CVE-2026-31502
Patch3114: 0001-team-fix-header_ops-type-confusion-with-non-Ethernet.patch

# Fix CVE-2026-31557
Patch3115: 0001-nvmet-move-async-event-work-off-nvmet-wq.patch

# Fix CVE-2026-23383
Patch3116: 0001-bpf-arm64-Force-8-byte-alignment-for-JIT-buffer.patch

# Fix CVE-2026-31419
Patch3117: 0001-net-bonding-fix-use-after-free-in-bond_xmit_broadcas.patch

# Fix CVE-2026-3118
Patch3118: 0001-net-ioam6-fix-OOB-and-missing-lock.patch
