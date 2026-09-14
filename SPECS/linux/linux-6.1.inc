# linux.spec preamble for kernel 6.1 (photon_subrelease <= 90), included from linux.spec

# If 'security_hardening none' is removed,
# ensure kpatch-build in kpatch is updated accordingly.
%global security_hardening none
%global __cmake_in_source_build 0
%global lkcm_version 5.0.0

# SBAT generation of "linux.photon" component
%define linux_photon_generation 1

# Do not add unique suffix to *.ko.debug files
# If _unique_debug_names defined, then __debug_install_post expands
# *.ko to *.ko-<version>-<release>.<arch>.debug.
# Undefining this option keeps filenames simple: *.ko.debug.
# This is what crash utility is looking for.
%undefine _unique_debug_names

# __debug_install_post extracts debug-info from modules. We need to
# specify option for any customizations.
%define _find_debuginfo_opts --keep-section '.BTF'

%ifarch x86_64
%define arch x86_64
%define archdir x86

# Set this flag to 0 to build without canister
%global fips 1
%endif

# Disable canister_build always
%if 0%{?canister_build}
%global canister_build 0
%endif

%if 0%{?acvp_build}
%global fips 1
%if 0%{?canister_build}
%global fips 0
%endif
%endif

%ifarch aarch64
%define arch arm64
%define archdir arm64
%global fips 0
%endif

Release:        3%{?acvp_build:.acvp}%{?kat_build:.kat}%{?dist}

%define uname_r %{version}-%{release}
%define _modulesdir /lib/modules/%{uname_r}

Source1:        config_%{_arch}-6.1
Source2:        initramfs.trigger

%define ena_version 2.17.0
Source3:        https://github.com/amzn/amzn-drivers/archive/refs/tags/ena_linux_%{ena_version}.tar.gz

%define efa_version 3.1.0
Source4:        https://github.com/amzn/amzn-drivers/archive/refs/tags/efa_linux_%{efa_version}.tar.gz

# contains pre, postun, filetriggerun tasks
Source6:        scriptlets.inc
Source7:        check_for_config_applicability-6.1.inc

%if 0%{?fips}
%define struct_comparator struct-comparator
%define struct_comp_dir struct-comp-dir
Source9:        struct-comparator.c

%define fips_canister_version 5.0.0-6.1.75-2%{?dist}-secure
Source16:       fips-canister-%{fips_canister_version}.tar.bz2
%endif

Source18:       spec_install_post-6.1.inc
Source19:       %{name}-dracut-%{_arch}.conf
Source20:       photon_sb2020.pem
Source21:       photon_km_2025.pem

%ifarch x86_64
# Secure Boot
Source25:       linux-sbat.csv.in

%define jent_major_version 3.4.1
%define jent_ph_version 4
Source32: jitterentropy-%{jent_major_version}-%{jent_ph_version}.tar.bz2
Source33: jitterentropy_canister_wrapper-6.1.c
Source34: jitterentropy_canister_wrapper-6.1.h
Source35: jitterentropy_canister_wrapper_asm-6.1.S

Source36: fips_canister_wrapper-6.1.c
Source37: fips_canister_wrapper-6.1.h
Source38: fips_canister_wrapper_asm.S
Source39: fips_canister_wrapper_common-6.1.h
# fips_canister_wrapper_internal{.c,.h} is the latest released
# wrapper files. These files may differ between 2 canister versions.
# During canister binary update, rename
# %%{fips_canister_version}-fips_canister_wrapper_internal{.c,.h}
# files to fips_canister_wrapper_internal{.c,.h}
%if 0%{?fips}
Source40: fips_canister_wrapper_internal-6.1.h
Source41: fips_canister_wrapper_internal-6.1.c
%endif

%if 0%{?canister_build}
Source43: fips_canister_wrapper_internal-6.1.h
Source44: fips_canister_wrapper_internal-6.1.c
Source45: fips_integrity-6.1.c
Source46: fips_integrity-6.1.h
Source47: update_canister_hmac-6.1.sh
Source48: canister_combine.lds
Source49: gen_canister_relocs-6.1.c
Source50: check_kernel_struct_in_canister.inc
%endif

Source51: jitterentropy_rng_proxy-6.1.c
%endif

Source52: license-6.1.txt
%include %{SOURCE52}

%if 0%{?fips}
# known vmlinux struct definitions
%define vmlinux_definition_loc canister_known_struct_def_vmlinux
Source75: crypto_alg.txt
Source76: crypto_template.txt
Source77: skcipher_walk.txt
Source78: swait_queue_head.txt
Source79: x86_cpu_id.txt
%endif

%if 0%{?acvp_build}
Source53: config_x86_64_acvp
Source54: check_for_acvp_config_applicability.inc
%endif

Source100: Makefile.viomem
Source101: viomem-6.1.c
Source102: kernel_cve_patches-6.1.inc

# common [0..49]
Patch0: confdata-format-change-for-split-script-6.1.patch
Patch1: net-Double-tcp_mem-limits.patch
Patch2: SUNRPC-xs_bind-uses-ip_local_reserved_ports.patch
Patch3: 6.0-9p-transport-for-9p.patch
Patch4: 9p-trans_fd-extend-port-variable-to-u32.patch
Patch5: vsock-delay-detach-of-QP-with-outgoing-data-59.patch
# RDRAND-based RNG driver to enhance the kernel's entropy pool:
Patch6: 6.0-0001-hwrng-rdrand-Add-RNG-driver-based-on-x86-rdrand-inst.patch
Patch7: 0001-cgroup-v1-cgroup_stat-support-6.1.patch
Patch8: 6.0-Discard-.note.gnu.property-sections-in-generic-NOTES.patch

# Expose Photon kernel macros to identify kernel flavor and version
Patch9:  0001-kbuild-Makefile-Introduce-macros-to-distinguish-Phot-6.1.patch
Patch10: 0002-linux-Makefile-Add-kernel-flavor-info-to-the-generat-6.1.patch

#HyperV patches
Patch12: vmbus-Don-t-spam-the-logs-with-unknown-GUIDs.patch

# TODO: Is CONFIG_HYPERV_VSOCKETS the same?
#Patchx: 0014-hv_sock-introduce-Hyper-V-Sockets.patch
Patch13: 6.1-0001-fork-add-sysctl-to-disallow-unprivileged-CLONE_NEWUS.patch
# Out-of-tree patches from AppArmor:
Patch14: 6.0-0001-apparmor-patch-to-provide-compatibility-with-v2.x-ne.patch
Patch15: 6.0-0002-apparmor-af_unix-mediation.patch

Patch16: Performance-over-security-model-6.1.patch
# Disable md5 algorithm for sctp if fips is enabled.
Patch18: 6.0-0001-disable-md5-algorithm-for-sctp-if-fips-is-enabled.patch

# VMware-specific patch to enable turbostat to work on ESXi
Patch19: 0001-tools-power-turbostat-Skip-some-CPUID-checks-if-runn-6.1.patch

# Allow PCI resets to be disabled from vfio_pci_core module
Patch21: 6.1-0001-drivers-vfio-pci-Add-kernel-parameter-to-allow-disab.patch
# Add PCI quirk to allow multiple devices under the same virtual PCI bridge
# to be put into separate IOMMU groups on ESXi.
Patch22: 0001-Add-PCI-quirk-for-VMware-PCIe-Root-Port.patch

Patch25: 0001-vmgenid-expose-vmgenid-via-sysfs-6.1.patch

# glibc-2.43 build error fixes
Patch26: 0001-libbpf-Fix-Wdiscarded-qualifiers-under-C23.patch

%ifarch x86_64
Patch49: 0001-x86-pti-Fix-kernel-warnings-for-pti-and-nopti-cmdlin.patch
%endif

# VMW: [50..59]
%ifarch x86_64
Patch55: 6.0-x86-vmware-Use-Efficient-and-Correct-ALTERNATIVEs-fo.patch
Patch56: 6.0-x86-vmware-Log-kmsg-dump-on-panic.patch
Patch57: 6.0-x86-vmware-Fix-steal-time-clock-under-SEV.patch

# Secure Boot and Kernel Lockdown
Patch58: 0001-kernel-lockdown-when-UEFI-secure-boot-enabled-6.1.patch
Patch59: 0002-Add-.sbat-section-6.1.patch
Patch60: 0003-Verify-SBAT-on-kexec-6.1.patch
%endif

#Secure:
Patch61: gcc-rap-plugin-with-kcfi.patch
Patch62: 0004-Fix-PAX-function-pointer-overwritten-for-tasklet-cal.patch
Patch63: fix-warn-definition.patch

Patch100: 6.0-0003-apparmor-fix-use-after-free-in-sk_peer_label.patch

# Fix BPF JIT memory (bpf_jit_limit) leak: seccomp filters held by
# unreaped zombies were not released until release_task(); release
# them at task exit instead. Upstream commit bfafe5efa975 (v6.11).
Patch101: seccomp-release-task-filters-when-the-task-exits.patch

# CVE patches — see kernel_cve_patches.inc (range 3000–3999)
%include %{SOURCE102}

# perf: off-cpu sample [221..223]
Patch221: 0001-perf-core-add-logic-to-collect-off-cpu-sample-6.1.patch
Patch222: 0002-perf-record-add-options-to-off-cpu-6.1.patch
Patch223: 0003-perf-display-off-cpu-samples-6.1.patch

%ifarch aarch64
# aarch specific patches [250..269]
# Rpi of_configfs patches
Patch250: 0001-OF-DT-Overlay-configfs-interface-6.1.patch
Patch251: 0002-of-configfs-Use-of_overlay_fdt_apply-API-call.patch
Patch252: 0003-of-overlay-Correct-symbol-path-fixups.patch
# arm64 hypervisor detection and kmsg dumper
Patch253: 6.0-0001-x86-hyper-generalize-hypervisor-type-detection.patch
Patch254: 6.0-0002-arm64-Generic-hypervisor-type-detection-for-arm64.patch
Patch255: 6.0-0003-arm64-VMware-hypervisor-detection.patch
Patch256: 6.0-0004-arm64-kmsg-dumper-for-VMware-hypervisor.patch
Patch257: 6.0-0005-scsi-vmw_pvscsi-add-arm64-support.patch
Patch258: 6.0-0006-vmxnet3-build-only-for-x86-and-arm64.patch
Patch259: 6.0-0005-vmw_balloon-add-arm64-support.patch
Patch260: 6.0-0001-vmw_vmci-arm64-support-memory-ordering.patch
%endif

%ifarch x86_64
# AWS: [300..339]
Patch301: 6.0-0001-scsi-sd_revalidate_disk-prevent-NULL-ptr-deref.patch
Patch302: 6.0-0007-xen-manage-keep-track-of-the-on-going-suspend-mode.patch
Patch303: 6.0-0008-xen-manage-introduce-helper-function-to-know-the-on-.patch
Patch304: 6.0-0009-xenbus-add-freeze-thaw-restore-callbacks-support.patch
Patch305: 6.0-0010-x86-xen-Introduce-new-function-to-map-HYPERVISOR_sha.patch
Patch306: 6.0-0011-x86-xen-add-system-core-suspend-and-resume-callbacks.patch
Patch307: 6.0-0012-xen-blkfront-add-callbacks-for-PM-suspend-and-hibern.patch
Patch308: 6.0-0013-xen-netfront-add-callbacks-for-PM-suspend-and-hibern.patch
Patch309: 6.0-0014-xen-time-introduce-xen_-save-restore-_steal_clock.patch
Patch310: 6.0-0015-x86-xen-save-and-restore-steal-clock.patch
Patch311: 6.0-0016-xen-events-add-xen_shutdown_pirqs-helper-function.patch
Patch312: 6.0-0017-x86-xen-close-event-channels-for-PIRQs-in-system-cor.patch
Patch313: 6.0-0018-PM-hibernate-update-the-resume-offset-on-SNAPSHOT_SE.patch
Patch314: 6.0-0020-xen-blkfront-Fixed-blkfront_restore-to-remove-a-call.patch
Patch315: 6.0-0021-x86-tsc-avoid-system-instability-in-hibernation.patch
Patch316: 6.0-0022-block-xen-blkfront-consider-new-dom0-features-on-res.patch
Patch317: 6.0-0023-xen-restore-pirqs-on-resume-from-hibernation.patch
Patch318: 6.0-0024-xen-Only-restore-the-ACPI-SCI-interrupt-in-xen_resto.patch
Patch319: 6.0-0026-xen-netfront-call-netif_device_attach-on-resume.patch
Patch320: 6.0-0054-xen-Restore-xen-pirqs-on-resume-from-hibernation.patch
Patch321: 6.0-0055-block-xen-blkfront-bump-the-maximum-number-of-indire.patch
Patch322: 6.0-0185-Introduce-page-touching-DMA-ops-binding.patch
Patch323: 6.0-0444-drivers-base-memory-use-MHP_MEMMAP_ON_MEMORY-from-th.patch
Patch324: 6.0-0490-Correct-read-overflow-in-page-touching-DMA-ops-bindi.patch
%endif

# Crypto: [500..529]
# Patch to invoke crypto self-tests and add missing test vectors to testmgr
Patch500: 0002-FIPS-crypto-self-tests.patch
# Patch to call drbg and dh crypto tests from tcrypt
Patch501: tcrypt-disable-tests-that-are-not-enabled-in-photon.patch
Patch502: 0001-Initialize-jitterentropy-before-ecdh.patch
# Patch to remove urandom usage in rng module
Patch503: 0001-FIPS-crypto-rng-Jitterentropy-RNG-as-the-only-RND-source-6.1.patch
# Patch to remove urandom usage in drbg and ecc modules
Patch504: 0003-FIPS-crypto-drbg-Jitterentropy-RNG-as-the-only-RND.patch

%ifarch x86_64
Patch505: 0001-changes-to-build-with-jitterentropy-v3.4.1.patch
Patch506: 0001-compile-jitterentropy-rng-proxy-6.1.patch
Patch507: 0001-change-jitterentropy_rng-driver-name-6.1.patch
%endif

%if 0%{?fips}
# FIPS canister usage patch
Patch508: 0001-FIPS-canister-binary-usage-6.1.patch
Patch509: 0001-scripts-kallsyms-Extra-kallsyms-parsing.patch
Patch510: 0001-LKCM-5.0-binary-patching-to-fix-struct-aesni_cpu_id-.patch
Patch511: 0001-canister-Change-spinlock_t-lock-to-void-reserved.patch
# commit e470d42 (crypto: api - Add crypto_tfm_get) introduced an api
# which adds a new member in struct crypto_tfm, causing build issues
# with fips canister, since, crypto_tfm_get() api is not being used
# in v6.1.x so reverting upstream commit.
Patch512: 0001-Revert-crypto-api-Add-crypto_tfm_get.patch
%endif

%if 0%{?acvp_build:1}
#ACVP test harness patches.
#Need to be applied on top of FIPS canister usage patch to avoid HUNK failure
Patch513: 0001-crypto-AF_ALG-add-sign-verify-API-6.1.patch
Patch514: 0002-crypto-AF_ALG-add-setpubkey-setsockopt-call-6.1.patch
Patch515: 0003-crypto-AF_ALG-add-asymmetric-cipher-6.1.patch
Patch516: 0004-crypto-AF_ALG-add-DH-keygen-ssgen-API.patch
Patch517: 0005-crypto-AF_ALG-add-DH-param-ECDH-curve-setsockopt-6.1.patch
Patch518: 0006-crypto-AF_ALG-eliminate-code-duplication-6.1.patch
Patch519: 0007-crypto-AF_ALG-add-KPP-support-6.1.patch
Patch520: 0008-crypto-AF_ALG-add-ECC-support-6.1.patch
Patch521: 0009-kernels-net-Export-sock_getsockopt.patch
Patch522: 0010-DRBG-Fix-issues-with-DRBG.patch
Patch523: 0011-Added-jitterentropy-implementation-of-SHA3-256.patch
Patch524: 0012-jitterentropy-Support-for-sample-collection.patch
%if 0%{?kat_build:1}
Patch525: 0013-crypto-api-return-status-prints-for-LKCM5-demo.patch
%endif
%endif

%ifarch x86_64
# SEV on VMware: [600..609]
Patch600: 0079-x86-sev-es-Disable-BIOS-ACPI-RSDP-probing-if-SEV-ES-.patch
Patch601: 0080-x86-boot-Enable-vmw-serial-port-via-Super-I-O.patch
Patch602: 0001-x86-boot-unconditional-preserve-CR4.MCE-6.1.patch
# TODO: Review: Patch602: 0081-x86-sev-es-Disable-use-of-WP-via-PAT-for-__sme_early.patch

# SEV-SNP:
Patch605: 0001-sev-snp-parse-MP-tables.patch
%endif

#HCX-Patches
Patch701: 0001-Active-probing-of-dst-mac-of-unknown-unicast-6.1.patch
Patch702: 0002-Skip-IP_ECN_decapsulate-for-gretap-devices-6.1.patch
Patch703: 0003-Handle-ipsec-in-ipip-more-correctly-6.1.patch
Patch704: 0004-De-cap-fou-traffic-into-correct-tunnel-device-s-6.1.patch
Patch705: 0005-Add-unknown-fou-tracking-to-kernel-6.1.patch
Patch706: 0006-Add-initial-support-for-vxlan-trunk-to-cgw-kernel-wi.patch
Patch707: 0007-Changes-for-bridge-vlan-arp-filtering-to-work-right.patch
Patch708: 0008-Add-support-for-mac-flapping-and-long-mac-flapping-p.patch
Patch709: 0009-vmxnet3-Avoid-fragmentation-by-giving-each-vmxnet3-d.patch
Patch710: 0010-RPS-flow-balance.patch
Patch711: 0011-add-mss-clamp-support-to-gretap-baseimage.patch
Patch712: 0012-set-max_mtu-as-IP_MAX_MTU.patch
Patch713: 0013-set-max_mtu-as-IP_MAX_MTU_for_vlan.patch
Patch714: 0014-iptunnel-mark-xfrm-multi-parts.patch
Patch715: 0015-disable-pskb_inet_may_pull-in-tunnel.patch
Patch716: 0016-gre_tap-interface-mss_clamp-support.patch
Patch717: 0017-rps_cpus-skip-receive-packets-queuing-to-only-housek.patch
# RCU callbacks invocation max batch limit control for HCX usecase
Patch718: 0001-rcutree-Adding-rcu_max_blimit-rcutree-param.patch
Patch719: 0018-Introduce-xfrm_dst-cache-mechanism-to-reuse-xfrm_dst.patch

# Report guest crash to vmware hypervisor
%ifarch aarch64
Patch1000: 0001-arm64-report-guest-crash-to-vmware-hypervisor.patch
%endif

%ifarch x86_64
Patch1000: 0001-x86-vmware-mark-hypercalls-as-volatile.patch
Patch1001: 0002-x86-report-guest-crash-to-vmware-hypervisor.patch
%endif

# Patches for efa [1400..1409]
Patch1400: Fix-efa-cmake-to-build-from-local-directory.patch

%if 0%{?canister_build}
# Below patches are common for fips and canister_build flags
# 0001-FIPS-canister-binary-usage.patch is renamed as <ver-rel>-0001-FIPS-canister-binary-usage.patch
# in both places until final canister binary is released
Patch10000: 0001-FIPS-canister-binary-usage-6.1.patch
Patch10001: 0001-scripts-kallsyms-Extra-kallsyms-parsing.patch
# Below patches are specific to canister_build flag
Patch10003: 0002-FIPS-canister-creation.patch
Patch10004: 0003-aesni_intel-Remove-static-call.patch
Patch10005: 0004-Disable-retpoline_sites-and-return_sites-section-in-.patch
Patch10006: 0005-Move-__bug_table-section-to-fips_canister_wrapper.patch
Patch10007: 0006-crypto-Add-prandom-module_kthread_exit-to-canister-w.patch
Patch10008: 0007-crypto-Remove-EXPORT_SYMBOL-EXPORT_SYMBOL_GPL-from-c.patch
Patch10009: 0008-Move-kernel-structures-usage.patch
Patch10010: 0009-ecc-Add-pairwise-consistency-test-for-every-generate.patch
Patch10011: 0001-List-canister-objs-in-a-file.patch
# Patch for RSA FIPS 186-5 compliance
Patch10012: 0001-crypto-rsa-allow-only-odd-e-and-restrict-value-in-FI.patch
Patch10013: 0001-Handle-approved-and-non-approved-services.patch

%if 0%{?kat_build}
Patch10014: 0001-Crypto-Tamper-KAT-PCT-and-Integrity-Test-6.1.patch
%endif
%endif

%if 0%{?photon_subrelease} >= 91
BuildRequires: mpc-devel
%endif

BuildRequires:  flex
BuildRequires:  perl
BuildRequires:  which

%ifarch x86_64
BuildRequires:  pciutils-devel
BuildRequires:  libcap-devel
# Requirements for signing artifacts
%if "%{?signing_script}" != ""
%define network_required 1
BuildRequires:  ca-certificates-pki
BuildRequires:  python3-requests
%endif
%endif

%if 0%{?fips}
BuildRequires:  gdb
%endif

Requires(pre):    (coreutils or coreutils-selinux)
Requires(preun):  (coreutils or coreutils-selinux)
Requires(post):   (coreutils or coreutils-selinux)
Requires(postun): (coreutils or coreutils-selinux)
