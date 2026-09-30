# linux-esx.spec preamble for kernel 6.1 (photon_subrelease <= 90), included from linux-esx.spec

# If 'security_hardening none' is removed,
# ensure kpatch-build in kpatch is updated accordingly.
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

Release:        1%{?dist}

%define uname_r %{version}-%{release}-esx
%define _modulesdir /lib/modules/%{uname_r}

Source1:        config-esx_%{_arch}-6.1
Source2:        initramfs.trigger
# contains pre, postun, filetriggerun tasks
Source3:        scriptlets.inc
Source4:        check_for_config_applicability-6.1.inc

%if 0%{?fips}
%define struct_comparator struct-comparator
%define struct_comp_dir struct-comp-dir
Source9:        struct-comparator.c

%define fips_canister_version 5.0.0-6.1.75-2%{?dist}-secure
Source16:       fips-canister-%{fips_canister_version}.tar.bz2
%endif

Source19:       spec_install_post-6.1.inc

Source20:       %{name}-dracut.conf

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
Source36: jitterentropy_rng_proxy-6.1.c
%endif

%if 0%{?fips}
Source37: fips_canister_wrapper-6.1.c
Source38: fips_canister_wrapper-6.1.h
Source39: fips_canister_wrapper_asm.S
Source40: fips_canister_wrapper_common-6.1.h
Source41: fips_canister_wrapper_internal-6.1.h
Source42: fips_canister_wrapper_internal-6.1.c

# known vmlinux struct definitions
%define vmlinux_definition_loc canister_known_struct_def_vmlinux
Source43: crypto_alg.txt
Source44: crypto_template.txt
Source45: skcipher_walk.txt
Source46: swait_queue_head.txt
Source47: x86_cpu_id.txt
%endif

Source49: license-6.1.txt
%include %{SOURCE49}

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
Patch10: 0002-linux-esx-Makefile-Add-kernel-flavor-info-to-the-gen-6.1.patch
Patch11: 9p-file-attributes-caching-support.patch
Patch12: 9p-support-for-local-file-lock-6.1.patch
Patch13: 6.1-0001-fork-add-sysctl-to-disallow-unprivileged-CLONE_NEWUS.patch
# Out-of-tree patches from AppArmor:
Patch14: 6.0-0001-apparmor-patch-to-provide-compatibility-with-v2.x-ne.patch
Patch15: 6.0-0002-apparmor-af_unix-mediation.patch
Patch16: 0001-Control-MEMCG_KMEM-config.patch
Patch17: Performance-over-security-model-6.1.patch
# Disable md5 algorithm for sctp if fips is enabled.
Patch18: 6.0-0001-disable-md5-algorithm-for-sctp-if-fips-is-enabled.patch
# Enable AUXILIARY BUS, to make building other out-of-tree intel NIC drivers easier
Patch19: 0001-Enable-AUXILIARY_BUS-by-default.patch

#VTAR/VTARFS
Patch20: 0001-fs-VTAR-archive-to-TPMFS-extractor-6.1.patch
Patch21: 0001-fs-A-new-VTARFS-file-system-to-mount-VTAR-archive-6.1.patch
#TARFS
Patch22: 0001-fs-TARFS-file-system-to-mount-TAR-archive-6.1.patch
#initrd newca
Patch23: 0001-initramfs-support-for-page-aligned-format-newca-6.1.patch
Patch24: 0001-NEWCA-make-initrd-pages-immutable-6.1.patch

# Patches for ptp_vmw
Patch30: 0001-ptp-ptp_vmw-Implement-PTP-clock-adjustments-ops-6.1.patch
Patch31: 0002-ptp-ptp_vmw-Add-module-param-to-probe-device-using-h-6.1.patch

%ifarch x86_64
Patch49: 0001-x86-pti-Fix-kernel-warnings-for-pti-and-nopti-cmdlin.patch

# VMW: [50..59]
Patch50: 6.0-x86-vmware-Use-Efficient-and-Correct-ALTERNATIVEs-fo.patch
Patch51: 6.0-x86-vmware-Log-kmsg-dump-on-panic.patch
Patch52: 6.0-x86-vmware-Fix-steal-time-clock-under-SEV.patch
Patch53: 6.0-x86-probe_roms-Skip-OpROM-probing-if-running-as-VMwa.patch
Patch54: 07-vmware-only-6.1.patch
Patch55: revert-x86-entry-Align-entry-text-section-to-PMD-boundary-6.1.patch

# Secure Boot and Kernel Lockdown
Patch56: 0001-kernel-lockdown-when-UEFI-secure-boot-enabled-6.1.patch
Patch57: 0002-Add-.sbat-section-6.1.patch
# NOTE: linux-esx does not support kexec, omitting SBAT verify logic.
# CONFIG_SECURITY_SBAT_VERIFY=y
# Patch58: 0003-Verify-SBAT-on-kexec.patch
#external-entropy
Patch59: 0001-external_entropy-Enable-External-Entropy-support-6.1.patch
%endif

# linux-esx [60..89]
Patch60: init-do_mounts-recreate-dev-root.patch
Patch61: serial-8250-do-not-probe-U6-16550A-fifo-size.patch
Patch62: 01-clear-linux.patch
Patch63: 02-pci-probe-6.1.patch
Patch64: poweroff-without-firmware-6.1.patch
Patch65: 04-quiet-boot.patch
Patch66: 05-pv-ops-clocksource.patch
Patch67: 0001-Remove-OOM_SCORE_ADJ_MAX-limit-check.patch
Patch68: halt-on-panic-6.1.patch

%if 0%{?vmxnet3_sw_timestamp}
Patch71: 0009-esx-vmxnet3-software-timestamping.patch
%endif

# initialize MMCONFIG
Patch75: 0001-initialize-MMCONFIG-if-already-not-initialized-6.1.patch
Patch76: 0001-MMIO_should_have_more_priority_then_IO-6.1.patch
Patch77: 0001-Avoid-extra-scanning-for-peer-host-bridges.patch

# Hotplug support without firmware
Patch80: 0001-vmw_extcfg-hotplug-without-firmware-support-6.1.patch
Patch81: 0002-vmw_extcfg-hotplug-without-firmware-support-6.1.patch
Patch82: 0003-vmw_extcfg-hotplug-without-firmware-support-6.1.patch

# SBX driver
Patch85: 0001-Adding-SBX-kernel-driver-6.1.patch

Patch100: 6.0-0003-apparmor-fix-use-after-free-in-sk_peer_label.patch

# Fix BPF JIT memory (bpf_jit_limit) leak: seccomp filters held by
# unreaped zombies were not released until release_task(); release
# them at task exit instead. Upstream commit bfafe5efa975 (v6.11).
Patch101: seccomp-release-task-filters-when-the-task-exits.patch

# CVE patches — see kernel_cve_patches.inc (range 3000–3999)
%include %{SOURCE102}

# aarch64 [250..260]
%ifarch aarch64
Patch250: 6.0-0001-x86-hyper-generalize-hypervisor-type-detection.patch
Patch251: 6.0-0002-arm64-Generic-hypervisor-type-detection-for-arm64.patch
Patch252: 6.0-0003-arm64-VMware-hypervisor-detection.patch
Patch253: 6.0-0004-arm64-kmsg-dumper-for-VMware-hypervisor.patch
Patch254: 6.0-0005-scsi-vmw_pvscsi-add-arm64-support.patch
Patch255: 6.0-0006-vmxnet3-build-only-for-x86-and-arm64.patch
Patch256: 6.0-0005-vmw_balloon-add-arm64-support.patch
Patch257: 6.0-0001-vmw_vmci-arm64-support-memory-ordering.patch
%endif

# 9p: [300..350]
Patch300: 0001-fs-9p-Add-opt_metaonly-cache-option-6.1.patch
Patch301: 0002-p9fs_dir_readdir-offset-support-6.1.patch
Patch302: 0003-Add-9p-zero-copy-data-path-using-crossfd.patch
Patch303: 0004-Enable-cache-loose-for-vdfs-9p.patch
Patch304: 0005-Ensure-seekdir-take-effect-when-entries-in-readdir-b.patch
Patch305: 0006-Initialize-fid-iounit-during-creation-of-p9_fid.patch
Patch306: 0007-Don-t-use-writeback-fid-for-cache-when-enabled-for-V.patch
Patch307: 0008-fscache-Only-fetch-attr-from-inode-cache-when-cache-.patch
Patch308: 0009-9p-fscache-Make-dcache-work-with-case-insensitive-vo.patch
Patch309: 0010-9p-fscache-Ensure-consistent-blksize-is-returned-fro.patch

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
Patch506: 0001-jitterentropy-kcapi-defer-jent_init.patch
Patch507: 0001-compile-jitterentropy-rng-proxy-6.1.patch
Patch508: 0001-change-jitterentropy_rng-driver-name-6.1.patch
%endif

%if 0%{?fips}
# FIPS canister usage patch
Patch509: 0001-FIPS-canister-binary-usage-6.1.patch
Patch510: 0001-scripts-kallsyms-Extra-kallsyms-parsing.patch
Patch511: 0001-LKCM-5.0-binary-patching-to-fix-struct-aesni_cpu_id-.patch
Patch512: 0001-canister-Change-spinlock_t-lock-to-void-reserved.patch
# commit e470d42 (crypto: api - Add crypto_tfm_get) introduced an api
# which adds a new member in struct crypto_tfm, causing build issues
# with fips canister, since, crypto_tfm_get() api is not being used
# in v6.1.x so reverting upstream commit.
Patch513: 0001-Revert-crypto-api-Add-crypto_tfm_get.patch
Patch514: speedup-algos-registration-in-non-fips-mode.patch
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

# Report guest crash to vmware hypervisor
%ifarch aarch64
Patch1000: 0001-arm64-report-guest-crash-to-vmware-hypervisor.patch
%endif

%ifarch x86_64
Patch1000: 0001-x86-vmware-mark-hypercalls-as-volatile.patch
Patch1001: 0002-x86-esx-report-guest-crash-to-vmware-hypervisor.patch
%endif

%if 0%{?photon_subrelease} >= 91
BuildRequires: mpc-devel
%endif

BuildRequires: bison
BuildRequires: which

# Requirements for signing artifacts
%if "%{?signing_script}" != ""
%ifarch x86_64
%define network_required 1
BuildRequires:  ca-certificates-pki
BuildRequires:  python3-requests
%endif
%endif

%if 0%{?fips}
BuildRequires: gdb
%endif

Requires(pre):    (coreutils or coreutils-selinux)
Requires(preun):  (coreutils or coreutils-selinux)
Requires(post):   (coreutils or coreutils-selinux)
Requires(postun): (coreutils or coreutils-selinux)
