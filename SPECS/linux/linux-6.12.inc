# linux.spec preamble for kernel 6.12 (photon_subrelease >= 91), included from linux.spec

%global security_hardening none
%global __cmake_in_source_build 0
%global lkcm_version 6.12

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

# FIPS flags: fips, canister_build, canister_usage, acvp_build.
# "fips" - declaring whether or not to build FIPS compliant kernel with crypto
# canister. When fips=0, it is a regular kernel build without the canister,
# canister_* values are ignored in this case. When fips=1 there are 2 possible
# build types:
# 1. canister_build=1 - build the canister and use it.
# 2. canister_build=0 - link with prebuilt canister object file.
#
# In both cases when fips=1, we use out of tree jent tarball.
#
# acvp_build=1 defines a special build of the canister for FIPS certification.
# It enforces fips=1 and works with canister_build(dev) or canister_usage (prod)
#
# kat_build=1 defines a non-production canister build used for CMVP_DEMO during FIPS certification.
# It includes additional debug prints in the cryptographic algorithm paths to display API flow
# and return statuses during ACVP testing.
# It also intentionally tampers the self-tests to simulate the broken KAT scenario required
# during the FIPS certification process.
# It enforces acvp_build=1 and canister_build=1.
#
# canister_usage is derived variable and can not be directly set.
# canister_usage=!canister_build, iff fips=1

%ifarch x86_64
%define arch x86_64
%define archdir x86
%global fips 1
%endif

%ifarch aarch64
%define arch arm64
%define archdir arm64
%global fips 0
%endif

%if 0%{?kat_build}
%global acvp_build 1
%global canister_build 1
%endif

%ifarch x86_64
%if 0%{?acvp_build}
%global fips 1
%endif
%endif

# Set default FIPS flags
%if 0%{?fips}
%global fips_plugins 1
%if 0%{?canister_build}
%global canister_usage 0
# This is the last certified canister version
# Remove below line when building a new canister
%define fips_certified_kernel_version 6.12.60-18.ph5
%else
%global canister_usage 1
%endif
%else
%global canister_usage 0
%global canister_build 0
%endif

Release:        7%{?acvp_build:.acvp}%{?kat_build:.kat}%{?dist}

%define uname_r %{version}-%{release}
%define _modulesdir /lib/modules/%{uname_r}

Source1:        config_%{_arch}
Source2:        initramfs.trigger

%define ena_version 2.17.0
Source3:        https://github.com/amzn/amzn-drivers/archive/refs/tags/ena_linux_%{ena_version}.tar.gz

%define efa_version 3.1.0
Source4:        https://github.com/amzn/amzn-drivers/archive/refs/tags/efa_linux_%{efa_version}.tar.gz

# shared canister/.config handling, also included by linux-esx.spec
Source5:        canister_config.inc
# contains pre, postun, filetriggerun tasks
Source6:        scriptlets.inc
Source7:        check_for_config_applicability.inc

Source18:       spec_install_post.inc
Source19:       %{name}-dracut-%{_arch}.conf
Source20:       photon_sb2020.pem
Source21:       photon_km_2025.pem

%ifarch x86_64
# Secure Boot
Source25:       linux-sbat.csv.in
%endif

Source30: Makefile.viomem
Source31: viomem.c
Source56: kernel_cve_patches.inc

Source55: license.txt
%include %{SOURCE55}

%if 0%{?fips}
%define jent_name photon-jitterentropy-v6.12
%define jent_rel_ver 3
Source10000:       %{jent_name}-%{jent_rel_ver}.tar.gz

Source10001: jitterentropy_canister_wrapper.c
Source10002: jitterentropy_canister_wrapper.h
Source10003: jitterentropy_canister_wrapper_asm.S

%if 0%{?canister_usage}
%define fips_canister_version 6.12.60-18.2.ph5
%define ExtraBuildRequiresSansSnapshot linux-fips-canister = %{fips_canister_version}
BuildRequires:       linux-fips-canister = %{fips_canister_version}
%endif

Source10101: fips_canister_wrapper.c
Source10102: fips_canister_wrapper.h
Source10104: fips_canister_wrapper_common.h
Source10105: fips_canister_wrapper_internal.h
Source10106: fips_canister_wrapper_internal.c

Source10300: jitterentropy_rng_proxy.c
%endif

%if 0%{?canister_build}
Source11000: partial_reloc.c
Source11001: fips_integrity.c
Source11002: fips_integrity.h
Source11003: update_canister_hmac.sh
Source11004: canister_combine.lds
Source11005: gen_canister_relocs.c
Source11500: check_kernel_struct_in_canister.inc
%endif

%if 0%{?acvp_build}
Source12000: config_x86_64_acvp
Source12001: check_for_acvp_config_applicability.inc
%endif

# common [0..49]
Patch0: confdata-format-change-for-split-script.patch
Patch1: net-Double-tcp_mem-limits.patch
Patch2: SUNRPC-xs_bind-uses-ip_local_reserved_ports.patch
Patch3: 9p-transport-for-9p.patch
Patch4: 9p-trans_fd-extend-port-variable-to-u32.patch
Patch5: vsock-delay-detach-of-QP-with-outgoing-data-59.patch
# RDRAND-based RNG driver to enhance the kernel's entropy pool:
Patch6: 0001-hwrng-rdrand-Add-RNG-driver-based-on-x86-rdrand-inst.patch
# Enable CGROUP Stat show for V1
Patch7: 0001-cgroup-v1-cgroup_stat-support.patch

# Expose Photon kernel macros to identify kernel flavor and version
Patch9:  0001-kbuild-Makefile-Introduce-macros-to-distinguish-Phot.patch
Patch10: 0002-linux-Makefile-Add-kernel-flavor-info-to-the-generat.patch

# ttyXRUSB support
Patch11: usb-acm-exclude-exar-usb-serial-ports-nxt.patch
#HyperV patches
Patch12: vmbus-Don-t-spam-the-logs-with-unknown-GUIDs.patch

# TODO: Is CONFIG_HYPERV_VSOCKETS the same?
#Patchx: 0014-hv_sock-introduce-Hyper-V-Sockets.patch
Patch13: 0001-fork-add-sysctl-to-disallow-unprivileged-CLONE_NEWUS.patch
# Out-of-tree patches from AppArmor:
Patch14: 0001-apparmor-patch-to-provide-compatibility-with-v2.x-ne.patch
Patch15: 0002-apparmor-af_unix-mediation.patch

Patch16: Performance-over-security-model.patch

Patch17: 0001-mm-add-provision-to-disable-CONFIG_PER_VMA_LOCK.patch

# VMware-specific patch to enable turbostat to work on ESXi
Patch19: 0001-tools-power-turbostat-Skip-some-CPUID-checks-if-runn.patch

# Allow PCI resets to be disabled from vfio_pci_core module
Patch21: 0001-drivers-vfio-pci-Add-kernel-parameter-to-allow-disab.patch
# Add PCI quirk to allow multiple devices under the same virtual PCI bridge
# to be put into separate IOMMU groups on ESXi.
Patch22: 0001-Add-PCI-quirk-for-VMware-PCIe-Root-Port.patch

# Upstream fix to properly handle PNP0C01/PNP0C02 device.
Patch23: 0001-ACPI-PNP-Drop-PNP0C01-and-PNP0C02-from-acpi_pnp_devi.patch

Patch26: 0001-alloc_tag-avoid-current-alloc_tag-manipulations-when.patch

Patch28: 0001-vmgenid-expose-vmgenid-via-sysfs.patch

Patch29: 0001-randomize_kstack-Unify-random-source-across-arches.patch

Patch30: 0001-sched_info_enqueue-don-t-update-last_queued-on-delay.patch

%ifarch x86_64
# VMW: [50..60]
Patch50: x86-vmware-Log-kmsg-dump-on-panic.patch
Patch51: x86-vmware-Support-steal-time-clock-for-encrypted-gu.patch
# Report guest crash to vmware hypervisor
Patch52: 0001-x86-report-guest-crash-to-vmware-hypervisor.patch

# SEV on VMware
Patch53: 0079-x86-sev-es-Disable-BIOS-ACPI-RSDP-probing-if-SEV-ES-.patch
Patch54: 0080-x86-boot-Enable-vmw-serial-port-via-Super-I-O.patch
Patch55: 0001-x86-boot-unconditional-preserve-CR4.MCE.patch
# TODO: Review: Patch602: 0081-x86-sev-es-Disable-use-of-WP-via-PAT-for-__sme_early.patch
Patch56: 0001-x86-vmware-Redefine-the-macro-of-CPUID_VMWARE.patch

# Secure Boot and Kernel Lockdown
Patch57: 0001-kernel-lockdown-when-UEFI-secure-boot-enabled.patch
Patch58: 0002-Add-.sbat-section.patch
Patch59: 0003-Verify-SBAT-on-kexec.patch
%endif

#Secure:
Patch61: 0001-gcc-rap-plugin-with-kcfi.patch
Patch62: 0002-objtool-Return-error-in-case-of-failures.patch
Patch63: 0004-Fix-PAX-function-pointer-overwritten-for-tasklet-cal.patch

# vmxnet3
Patch65: 0001-vmxnet3_support_higher_link_speeds_from_vmxnet3_v9.patch

# Backward compatibility
%if "%{dist}" == ".ph5"
Patch71: 0001-block-Fix-validation-of-ioprio-level.patch
%endif

# CVE patches — see kernel_cve_patches.inc (range 3000–3999)
%include %{SOURCE56}

%ifarch aarch64
# aarch specific patches [200..219]
# Rpi of_configfs patches
Patch201: 0001-OF-DT-Overlay-configfs-interface.patch
Patch203: 0003-of-overlay-Correct-symbol-path-fixups.patch
# Rpi fan driver
# arm64 hypervisor detection and kmsg dumper
Patch205: 0001-x86-hyper-generalize-hypervisor-type-detection.patch
Patch206: 0002-arm64-Generic-hypervisor-type-detection-for-arm64.patch
Patch207: 0003-arm64-VMware-hypervisor-detection.patch
Patch208: 0004-arm64-kmsg-dumper-for-VMware-hypervisor.patch
Patch209: 0005-scsi-vmw_pvscsi-add-arm64-support.patch
Patch210: 0006-vmxnet3-build-only-for-x86-and-arm64.patch
Patch211: 0005-vmw_balloon-add-arm64-support.patch
Patch212: 0001-vmw_vmci-arm64-support-memory-ordering.patch
# Report guest crash to vmware hypervisor
Patch213: 0001-arm64-report-guest-crash-to-vmware-hypervisor.patch
%endif

# perf: off-cpu sample
Patch221: 0001-perf-core-add-logic-to-collect-off-cpu-sample.patch
Patch222: 0002-perf-record-add-options-to-off-cpu.patch
Patch223: 0003-perf-display-off-cpu-samples.patch

# tools: fix for new glibc
Patch230: 0001-perf-disasm-Constify-variables-storing-the-result-of.patch
Patch231: 0002-perf-metricgroup-Constify-variables-storing-the-resu.patch
Patch232: 0003-perf-strlist-Don-t-write-to-const-memory.patch
Patch233: 0004-perf-session-Don-t-write-to-memory-pointed-to-a-cons.patch
Patch234: 0005-perf-trace-event-Constify-variables-storing-the-resu.patch
Patch235: 0006-perf-units-Constify-variables-storing-the-result-of-.patch
Patch236: 0007-perf-time-utils-Constify-variables-storing-the-resul.patch
Patch237: 0008-perf-demangle-java-Constify-variables-storing-the-re.patch
Patch238: 0009-perf-bpf-event-Constify-variables-storing-the-result.patch
Patch239: 0010-perf-jitdump-Constify-variables-storing-the-result-o.patch
Patch240: 0011-perf-list-Remove-unused-sep-variable.patch
Patch241: 0012-perf-diff-Constify-strchr-return-variables.patch
Patch242: 0013-perf-tools-Use-const-for-variables-receiving-str-str.patch
Patch243: 0014-perf-trace-Don-t-change-const-char-strings.patch
Patch244: 0015-perf-list-Don-t-write-to-const-memory.patch
Patch245: 0016-perf-trace-Deal-with-compiler-const-checks.patch
Patch246: 0017-perf-print-events-Fix-compiler-issues-with-newer-gil.patch
Patch247: 0018-perf-list-Signal-changing-const-memory-is-ok.patch
Patch248: 0019-perf-tools-Remove-unused-color_fwrite_lines.patch

%ifarch x86_64
# AWS: [300..339]
Patch301: 0001-scsi-sd_revalidate_disk-prevent-NULL-ptr-deref.patch
Patch302: 0007-xen-manage-keep-track-of-the-on-going-suspend-mode.patch
Patch303: 0008-xen-manage-introduce-helper-function-to-know-the-on-.patch
Patch304: 0009-xenbus-add-freeze-thaw-restore-callbacks-support.patch
Patch305: 0010-x86-xen-Introduce-new-function-to-map-HYPERVISOR_sha.patch
Patch306: 0011-x86-xen-add-system-core-suspend-and-resume-callbacks.patch
Patch307: 0012-xen-blkfront-add-callbacks-for-PM-suspend-and-hibern.patch
Patch308: 0013-xen-netfront-add-callbacks-for-PM-suspend-and-hibern.patch
Patch309: 0014-xen-time-introduce-xen_-save-restore-_steal_clock.patch
Patch310: 0015-x86-xen-save-and-restore-steal-clock.patch
Patch311: 0016-xen-events-add-xen_shutdown_pirqs-helper-function.patch
Patch312: 0017-x86-xen-close-event-channels-for-PIRQs-in-system-cor.patch
Patch313: 0018-PM-hibernate-update-the-resume-offset-on-SNAPSHOT_SE.patch
Patch314: 0020-xen-blkfront-Fixed-blkfront_restore-to-remove-a-call.patch
Patch315: 0021-x86-tsc-avoid-system-instability-in-hibernation.patch
Patch316: 0022-block-xen-blkfront-consider-new-dom0-features-on-res.patch
Patch317: 0023-xen-restore-pirqs-on-resume-from-hibernation.patch
Patch318: 0024-xen-Only-restore-the-ACPI-SCI-interrupt-in-xen_resto.patch
Patch319: 0026-xen-netfront-call-netif_device_attach-on-resume.patch
Patch320: 0054-xen-Restore-xen-pirqs-on-resume-from-hibernation.patch
Patch321: 0055-block-xen-blkfront-bump-the-maximum-number-of-indire.patch
Patch322: 0185-Introduce-page-touching-DMA-ops-binding.patch
Patch323: 0444-drivers-base-memory-use-MHP_MEMMAP_ON_MEMORY-from-th.patch
Patch324: 0490-Correct-read-overflow-in-page-touching-DMA-ops-bindi.patch

%endif

#HCX-Patches
Patch701: 0001-Active-probing-of-dst-mac-of-unknown-unicast.patch
Patch702: 0002-Skip-IP_ECN_decapsulate-for-gretap-devices.patch
Patch703: 0003-Handle-ipsec-in-ipip-more-correctly.patch
Patch704: 0004-De-cap-fou-traffic-into-correct-tunnel-device-s.patch
Patch705: 0005-Add-unknown-fou-tracking-to-kernel.patch
Patch706: 0006-Add-support-for-mac-flapping-and-long-mac-flapping-p.patch
Patch707: 0007-vmxnet3-Avoid-fragmentation-by-giving-each-vmxnet3-d.patch
Patch708: 0008-RPS-flow-balance.patch
Patch709: 0009-add-mss-clamp-support-to-gretap-baseimage.patch
Patch710: 0010-iptunnel-mark-xfrm-multi-parts.patch
Patch711: 0011-disable-pskb_inet_may_pull-in-tunnel.patch
Patch712: 0012-gre_tap-interface-mss_clamp-support.patch
Patch713: 0013-rps_cpus-skip-receive-packets-queuing-to-only-housek.patch
Patch714: 0014-Introduce-xfrm_dst-cache-mechanism-to-reuse-xfrm_dst.patch
Patch715: 0015-rcutree-Adding-rcu_max_blimit-rcutree-param.patch

# Patches for efa [1400..1409]
Patch1400: Fix-efa-cmake-to-build-from-local-directory.patch

# Only LKCM/JENT related patches below
# Jitterentropy support and FIPS compliance
Patch10000: 0001-New-memsize-options-for-jent.patch
%if 0%{?fips}
Patch10001: 0001-jitterentropy-Makefile-changes.patch
# Patch to remove urandom usage in rng module
Patch10002: 0001-FIPS-crypto-rng-Jitterentropy-RNG-as-the-only-RND-source.patch
# Disable md5 algorithm for sctp if fips is enabled.
Patch10003: 0001-disable-md5-and-sha1-algorithms-for-sctp-if-fips-is-enabled.patch
# Mark ECB as Internal algorithm if fips is enabled.
Patch10004: 0001-crypto-ecb-Set-ecb-alg-flag-as-Internal.patch

# Below patches are common for canister_usage and canister_build flags
Patch10101: 0001-FIPS-canister-binary-usage.patch
Patch10102: 0002-algapi.c-honor-fcw_skip_tests.patch
Patch10103: 0003-tcrypt-align-to-LKCM.patch
Patch10104: 0004-scripts-kallsyms-Extra-kallsyms-parsing.patch
# Move rsa-pkcs1pad encrypt and decrypt functions outside canister
Patch10106: 0006-crypto-Disable-rsa-pkcs1pad-encrypt-decrypt-in-FIPS-.patch
# Add internal_iv field for aead_request
Patch10107: 0007-aead-add-internal_iv-field.patch
Patch10108: 0008-FIPS-Mark-structure-field-differences-between-kernel.patch
Patch10109: 0009-aead_geniv_ctx-drop-lock-field.patch
Patch10110: 0010-Move-crypto_inc-to-lib-crypto-utils.c.patch
Patch10111: 0001-crypto-Moving-rfc4543-out-of-canister-boundry.patch
# Make lib/digsig to use lib SHA1 instead of crypto shash API
# [10112..10116]
Patch10112: 0001-crypto-x86-sha1-Rename-conflicting-symbol.patch
Patch10113: 0002-lib-crypto-sha1-Rename-sha1_init-to-sha1_init_raw.patch
Patch10114: 0003-lib-crypto-sha1-Add-SHA-1-library-functions.patch
Patch10115: 0001-lib-digsig-Use-SHA-1-library-instead-of-crypto_shash.patch
Patch10116: 0001-crypto-sha1_generic-Renaming-sha1_final.patch
# Track internal/external jitterentropy rng requests
Patch10117: 0001-crypto-track-external-requests-to-jitterentropy_rng.patch
# make ima to use lib SHA1 instead of crypto shash API
Patch10118: 0001-linux-ima-Use-lib-sha1-instead-of-crypto-shash.patch

# FIPS canister plugins
Patch10200: 0001-Compile-GCC-plugins-for-FIPS-canister.patch
Patch10201: 0002-Build-with-FIPS-Canister-GCC-plugins.patch
Patch10202: 0003-Introduce-FIPS-canister-plugins.patch
Patch10203: 0004-FIPS-Canister-Plugins-Add-self-tests.patch
Patch10204: 0001-Canister-GCC-Plugins-Implement-type-check.patch

# Compile and inject jitterentropy rng proxy
Patch10300: 0001-compile-jitterentropy-rng-proxy.patch
Patch10301: 0001-change-jitterentropy_rng-driver-name.patch
%endif

# Canister build patches
%if 0%{?canister_build}
# Below patches are specific to canister_build flag
Patch11000: 1000-FIPS-canister-creation.patch
Patch11001: 1001-aesni_intel-Remove-static-call.patch
Patch11002: 1002-Disable-retpoline_sites-and-return_sites-sections-in.patch
# Patch to remove urandom usage in drbg and ecc modules
Patch11003: 1003-FIPS-crypto-drbg-Jitterentropy-RNG-as-the-only-RND.patch
Patch11004: 1004-Move-__bug_table-section-to-fips_canister_wrapper.patch
Patch11005: 1005-crypto-Remove-EXPORT_SYMBOL-EXPORT_SYMBOL_GPL-from-c.patch
Patch11006: 1006-Move-kernel-structures-usage-from-canister-to-wrappe.patch
Patch11007: 1007-ecc-Add-pairwise-consistency-test-for-every-generate.patch
Patch11008: 1008-Add-ghash-accelerator.patch
Patch11009: 1009-Handle-approved-and-non-approved-services.patch
Patch11010: 1010-rsa-pkcs1pad-Add-invalid_hash_len-check-in-sign-veri.patch
Patch11011: 1011-sha1-Do-not-register-sha1-to-crypto-backend-when-fip.patch
Patch11012: 1012-Add-shasums-accelerators.patch
Patch11013: 1013-Disable-ret-sites-section-in-x86-shasum-object-files.patch
# Patch to invoke crypto self-tests and add missing test vectors to testmgr
Patch11015: 1015-FIPS-crypto-self-tests.patch
# Disable alloc_hook_tags if MEM_PROFILING is disabled
Patch11016: 1016-linux-canister-Eliminate-codetag-and-other-taggings-.patch
# CVE-2026-64313 fix was applied on canister v6.12.60-18.1.
# Below entry is kept for future reference
# 0001-crypto-ecc-Fix-carry-overflow-in-vli-multiplication.patch
%endif

# ACVP special builds
%if 0%{?acvp_build:1}
#ACVP test harness patches.
Patch12000:       0001-crypto-AF_ALG-add-sign-verify-API.patch
Patch12001:       0002-crypto-AF_ALG-add-setpubkey-setsockopt-call.patch
Patch12002:       0003-crypto-AF_ALG-add-asymmetric-cipher.patch
Patch12003:       0004-crypto-AF_ALG-add-DH-keygen-ssgen-API.patch
Patch12004:       0005-crypto-AF_ALG-add-DH-param-ECDH-curve-setsockopt.patch
Patch12005:       0006-crypto-AF_ALG-eliminate-code-duplication.patch
Patch12006:       0007-crypto-AF_ALG-add-KPP-support.patch
Patch12007:       0008-crypto-AF_ALG-add-ECC-support.patch
Patch12008:       0009-DRBG-Fix-issues-with-DRBG.patch
Patch12009:       0011-sock-Remove-sendpage-in-favour-of-sendmsg-MSG_SPLICE.patch
Patch12010:       0012-jitterentropy-kcapi-Support-for-sample-collection.patch
Patch12011:       0013-Jitterentropy-Add-char-dev-interface-for-jent-osr.patch
Patch12012:       0014-jitterentropy-Add-prototype-for-sample-collection.patch
%endif

# KAT special builds
%if 0%{?kat_build}
Patch12013:       0001-Crypto-Tamper-KAT-PCT-and-Integrity-Test.patch
Patch12014:       0015-crypto-api-return-status-prints-for-LKCM6-demo.patch
%endif

BuildRequires:  mpc-devel
BuildRequires:  libtraceevent-devel
BuildRequires:  clang-devel
BuildRequires:  readline-devel
%if 0%{?fips_plugins}
BuildRequires:  gcc >= 12.2.0-6
%endif

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

BuildRequires:  gdb

Requires(pre):    coreutils
Requires(preun):  coreutils
Requires(post):   coreutils
Requires(postun): coreutils
