# linux-esx.spec preamble for kernel 6.12 (photon_subrelease >= 91), included from linux-esx.spec

%global security_hardening none
%global __cmake_in_source_build 0

# SBAT generation of "linux.photon" component
%define linux_photon_generation 1

# Do not add unique suffix to *.ko.debug files
# If _unique_debug_names defined, then __debug_install_post expands
# *.ko to *.ko-<version>-<release>.<arch>.debug.
# Undefining this option keeps filenames simple: *.ko.debug.
# This is what crash utility is looking for.
%undefine _unique_debug_names

%ifarch x86_64
%define arch x86_64
%define archdir x86

# Set this flag to 0 to build without canister
%global fips 1
%endif

%ifarch aarch64
%define arch arm64
%define archdir arm64
%global fips 0
%endif

# The esx flavour never builds the canister itself, it always links against the
# prebuilt canister object file. Mirror linux.spec's derived flag model so the
# shared canister_config.inc behaves identically for both flavours.
%if 0%{?fips}
%global canister_build 0
%global canister_usage 1
%else
%global canister_build 0
%global canister_usage 0
%endif

Release:        7%{?dist}

%define uname_r %{version}-%{release}-esx
%define _modulesdir /lib/modules/%{uname_r}

Source1:        config-esx_%{_arch}
Source2:        initramfs.trigger
# contains pre, postun, filetriggerun tasks
Source3:        scriptlets.inc
Source4:        check_for_config_applicability.inc
# shared canister/.config handling, also included by linux.spec
Source5:        canister_config.inc

Source19:       spec_install_post.inc

Source20:       %{name}-dracut.conf

Source21:       photon_km_2025.pem
%ifarch x86_64
# Secure Boot
Source25:       linux-sbat.csv.in
%endif

Source30: Makefile.viomem
Source31: viomem.c

Source42: license-esx.txt
%include %{SOURCE42}

%if 0%{?fips}
%define jent_name photon-jitterentropy-v6.12
%define jent_rel_ver 3
Source10000:       %{jent_name}-%{jent_rel_ver}.tar.gz

Source10001: jitterentropy_canister_wrapper.c
Source10002: jitterentropy_canister_wrapper.h
Source10003: jitterentropy_canister_wrapper_asm.S

%define fips_canister_version 6.12.60-18.2.ph5
%define ExtraBuildRequiresSansSnapshot linux-fips-canister = %{fips_canister_version}
BuildRequires:       linux-fips-canister = %{fips_canister_version}

Source10101: fips_canister_wrapper.c
Source10102: fips_canister_wrapper.h
Source10104: fips_canister_wrapper_common.h
Source10105: fips_canister_wrapper_internal.h
Source10106: fips_canister_wrapper_internal.c

Source10300: jitterentropy_rng_proxy.c
%endif

Source10301: kernel_cve_patches.inc

# common [0..49]
Patch0: confdata-format-change-for-split-script.patch
Patch1: net-Double-tcp_mem-limits.patch
Patch2: SUNRPC-xs_bind-uses-ip_local_reserved_ports.patch
Patch3: 9p-transport-for-9p.patch
Patch4: 9p-trans_fd-extend-port-variable-to-u32.patch
Patch5: vsock-delay-detach-of-QP-with-outgoing-data-59.patch
# RDRAND-based RNG driver to enhance the kernel's entropy pool:
Patch6: 0001-hwrng-rdrand-Add-RNG-driver-based-on-x86-rdrand-inst.patch
Patch7: 0001-cgroup-v1-cgroup_stat-support.patch
# Expose Photon kernel macros to identify kernel flavor and version
Patch9:  0001-kbuild-Makefile-Introduce-macros-to-distinguish-Phot.patch
Patch10: 0002-linux-esx-Makefile-Add-kernel-flavor-info-to-the-gen.patch
Patch12: 9p-support-for-local-file-lock.patch
Patch13: 0001-fork-add-sysctl-to-disallow-unprivileged-CLONE_NEWUS.patch
# Out-of-tree patches from AppArmor:
Patch14: 0001-apparmor-patch-to-provide-compatibility-with-v2.x-ne.patch
Patch15: 0002-apparmor-af_unix-mediation.patch
Patch17: Performance-over-security-model.patch
# Enable AUXILIARY BUS, to make building other out-of-tree intel NIC drivers easier
Patch19: 0001-Enable-AUXILIARY_BUS-by-default.patch

#VTAR/VTARFS
Patch20: 0001-fs-VTAR-archive-to-TPMFS-extractor.patch
Patch21: 0001-fs-A-new-VTARFS-file-system-to-mount-VTAR-archive.patch
#TARFS
Patch22: 0001-fs-TARFS-file-system-to-mount-TAR-archive.patch
#initrd newca
Patch23: 0001-initramfs-support-for-page-aligned-format-newca.patch
Patch24: 0001-NEWCA-make-initrd-pages-immutable.patch

# Upstream fix to properly handle PNP0C01/PNP0C02 device.
Patch25: 0001-ACPI-PNP-Drop-PNP0C01-and-PNP0C02-from-acpi_pnp_devi.patch

Patch29: 0001-randomize_kstack-Unify-random-source-across-arches.patch

# Patches for ptp_vmw
Patch30: 0001-ptp-ptp_vmw-Implement-PTP-clock-adjustments-ops.patch
Patch31: 0002-ptp-ptp_vmw-Add-module-param-to-probe-device-using-h.patch

Patch32: 0001-alloc_tag-avoid-current-alloc_tag-manipulations-when.patch

# sched_info_enqueue: don't update last_queued on delayed migration
Patch33: 0001-sched_info_enqueue-don-t-update-last_queued-on-delay.patch

%ifarch x86_64
# VMW: [50..59]
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
# NOTE: linux-esx does not support kexec, omitting SBAT verify logic.
# CONFIG_SECURITY_SBAT_VERIFY=y
# Patch58: 0003-Verify-SBAT-on-kexec.patch
#external-entropy
Patch59: 0001-external_entropy-Enable-External-Entropy-support.patch
Patch60: 07-vmware-only.patch
%endif

# linux-esx [60..89]
Patch61: init-do_mounts-recreate-dev-root.patch
Patch62: serial-8250-do-not-probe-U6-16550A-fifo-size.patch
Patch63: 01-clear-linux.patch
Patch64: 02-pci-probe.patch
Patch65: poweroff-without-firmware.patch
Patch66: 04-quiet-boot.patch
Patch67: 05-pv-ops-clocksource.patch
Patch68: 0001-Remove-OOM_SCORE_ADJ_MAX-limit-check.patch
Patch69: halt-on-panic.patch
Patch70: x86-probe_roms-Skip-OpROM-probing-if-running-as-VMwa.patch
Patch71: revert-x86-entry-Align-entry-text-section-to-PMD-boundary.patch

%if 0%{?vmxnet3_sw_timestamp}
Patch72: 0009-esx-vmxnet3-software-timestamping.patch
%endif

# vmxnet3
Patch73: 0001-vmxnet3_support_higher_link_speeds_from_vmxnet3_v9.patch

# initialize MMCONFIG
Patch75: 0001-initialize-MMCONFIG-if-already-not-initialized.patch
Patch76: 0001-MMIO_should_have_more_priority_then_IO.patch
Patch77: 0001-Avoid-extra-scanning-for-peer-host-bridges.patch

# Hotplug support without firmware
Patch80: 0001-vmw_extcfg-hotplug-without-firmware-support.patch
Patch81: 0002-vmw_extcfg-hotplug-without-firmware-support.patch
Patch82: 0003-vmw_extcfg-hotplug-without-firmware-support.patch

# Drain per-CPU page caches after boot-time memory frees, so
# /proc/meminfo reports settled numbers from the first read
Patch83: 0001-init-main.c-drain-per-CPU-page-caches-after-boot-tim.patch

# SBX driver
Patch85: 0001-Adding-SBX-kernel-driver.patch

%ifarch x86_64
#SBX DTLS driver
Patch86: 0001-linux-esx-Add-SBX-DTLS-kernel-module.patch
# D-TLS ZERO COPY driver
Patch88: 0001-Adding-DTLS-Zero-Copy-Driver.patch
%endif

# Backward compatibility
%if "%{dist}" == ".ph5"
Patch91: 0001-block-Fix-validation-of-ioprio-level.patch
%endif

# CVE patches — see kernel_cve_patches.inc (range 3000–3999)
%include %{SOURCE10301}

# aarch64 [200..219]
%ifarch aarch64
Patch200: 0001-x86-hyper-generalize-hypervisor-type-detection.patch
Patch201: 0002-arm64-Generic-hypervisor-type-detection-for-arm64.patch
Patch202: 0003-arm64-VMware-hypervisor-detection.patch
Patch203: 0004-arm64-kmsg-dumper-for-VMware-hypervisor.patch
Patch204: 0005-scsi-vmw_pvscsi-add-arm64-support.patch
Patch205: 0006-vmxnet3-build-only-for-x86-and-arm64.patch
Patch206: 0005-vmw_balloon-add-arm64-support.patch
Patch207: 0001-vmw_vmci-arm64-support-memory-ordering.patch
# Report guest crash to vmware hypervisor
Patch208: 0001-arm64-report-guest-crash-to-vmware-hypervisor.patch
%endif

# 9p: [300..350]
Patch300: 0001-fs-9p-Add-opt_metaonly-cache-option.patch
Patch301: 0002-p9fs_dir_readdir-offset-support.patch
Patch303: 0003-Enable-cache-loose-for-vdfs-9p.patch
Patch304: 0004-Ensure-seekdir-take-effect-when-entries-in-readdir-b.patch
Patch305: 0005-Initialize-fid-iounit-during-creation-of-p9_fid.patch
Patch307: 0006-fscache-Only-fetch-attr-from-inode-cache-when-cache-.patch
Patch308: 0007-9p-fscache-Make-dcache-work-with-case-insensitive-vo.patch
Patch309: 0008-9p-fscache-Ensure-consistent-blksize-is-returned-fro.patch

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
Patch10050: 0001-jitterentropy-Defer-jent_mod_init-in-non-fips-boot.patch

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

BuildRequires: mpc-devel
BuildRequires: bison
BuildRequires: libtraceevent-devel
BuildRequires: clang-devel
BuildRequires: readline-devel
%if 0%{?fips}
BuildRequires: gcc >= 12.2.0-6
%endif

# Requirements for signing artifacts
%if "%{?signing_script}" != ""
%ifarch x86_64
%define network_required 1
BuildRequires:  ca-certificates-pki
BuildRequires:  python3-requests
%endif
%endif

Requires(pre):    coreutils
Requires(preun):  coreutils
Requires(post):   coreutils
Requires(postun): coreutils
