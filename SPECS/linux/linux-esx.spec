%global security_hardening none

# Set this flag to 0 to build without canister
%global fips 1

# If kat_build is enabled, canister is not used.
%if 0%{?kat_build}
%global fips 0
%endif

Summary:        Kernel
Name:           linux-esx
Version:        5.10.224
Release:        5%{?kat_build:.kat}%{?dist}
License:        GPLv2
URL:            http://www.kernel.org
Group:          System Environment/Kernel
Vendor:         VMware, Inc.
Distribution:   Photon

%define uname_r %{version}-%{release}-esx
%define _modulesdir /lib/modules/%{uname_r}

Source0:        http://www.kernel.org/pub/linux/kernel/v5.x/linux-%{version}.tar.xz
%define sha512 linux=43c038046601a32100056d67300ce32700d04c081935964b15732e749fce5bd70c54a3a2419f85a60ccad229726698d3e163e3b9959156fd6e0cb653dad27541
Source1:        config-esx
Source2:        initramfs.trigger
# contains pre, postun, filetriggerun tasks
Source3:        scriptlets.inc
Source4:        check_for_config_applicability.inc

%ifarch x86_64
%define i40e_version 2.22.18
Source6:        https://sourceforge.net/projects/e1000/files/i40e%20stable/%{i40e_version}/i40e-%{i40e_version}.tar.gz
%define sha512 i40e=042fd064528cb807894dc1f211dcb34ff28b319aea48fc6dede928c93ef4bbbb109bdfc903c27bae98b2a41ba01b7b1dffc3acac100610e3c6e95427162a26ac

%define iavf_version 4.8.2
Source7:       https://sourceforge.net/projects/e1000/files/iavf%20stable/%{iavf_version}/iavf-%{iavf_version}.tar.gz
%define sha512 iavf=5406b86e61f6528adfd7bc3a5f330cec8bb3b4d6c67395961cc6ab78ec3bd325c3a8655b8f42bf56fb47c62a85fb7dbb0c1aa3ecb6fa069b21acb682f6f578cf

%define ice_version 1.11.14
Source8:       https://sourceforge.net/projects/e1000/files/ice%20stable/%{ice_version}/ice-%{ice_version}.tar.gz
%define sha512 ice=a2a6a498e553d41e4e6959a19cdb74f0ceff3a7dbcbf302818ad514fdc18e3d3b515242c88d55ef8a00c9d16925f0cd8579cb41b3b1c27ea6716ccd7e70fd847
%endif

%if 0%{?fips}
Source9:        check_fips_canister_struct_compatibility.inc

%define fips_canister_version 4.0.1-5.10.21-3-secure
Source16:       fips-canister-%{fips_canister_version}.tar.bz2
%define sha512 fips-canister=1d3b88088a23f7d6e21d14b1e1d29496ea9e38c750d8a01df29e1343034f74b0f3801d1f72c51a3d27e9c51113c808e6a7aa035cb66c5c9b184ef8c4ed06f42a

Source17:       modify_kernel_configs.inc
Source18:       fips_canister-kallsyms
Source19:       FIPS-do-not-allow-not-certified-algos-in-fips-2.patch
Source20:       Add-alg_request_report-cmdline.patch
Source21:       speedup-algos-registration-in-non-fips-mode.patch
Source22:       0001-LKCM-4.0.1-binary-patching-to-fix-jent-on-AMD-EPYC.patch
Source25:       0001-LKCM-4.0.1-binary-patching-to-fix-struct-aesni_cpu_i.patch
%endif

Source23:       spec_install_post.inc
Source24:       %{name}-dracut.conf

# common
Patch0: net-Double-tcp_mem-limits.patch
# TODO: disable this patch, check for regressions
#Patchx: linux-4.9-watchdog-Disable-watchdog-on-virtual-machines.patch
Patch1: SUNRPC-Do-not-reuse-srcport-for-TIME_WAIT-socket.patch
Patch2: SUNRPC-xs_bind-uses-ip_local_reserved_ports.patch
Patch3: 9p-transport-for-9p.patch
Patch4:  9p-trans_fd-extend-port-variable-to-u32.patch
Patch5: vsock-delay-detach-of-QP-with-outgoing-data-59.patch
Patch6: hwrng-rdrand-Add-RNG-driver-based-on-x86-rdrand-inst.patch
Patch7: 9p-file-attributes-caching-support.patch
Patch8: 9p-support-for-local-file-lock.patch
Patch9: fork-add-sysctl-to-disallow-unprivileged-CLONE_NEWUSER-by.patch
Patch10: apparmor-patch-to-provide-compatibility-with-v2.x-ne.patch
Patch11: apparmor-af_unix-mediation.patch
Patch12: Performance-over-security-model.patch
# Revert crypto api workqueue
Patch13: 0001-Revert-crypto-api-Use-work-queue-in-crypto_destroy_i.patch
# floppy:
Patch17: 0001-floppy-lower-printk-message-priority.patch
Patch18: 0001-Control-MEMCG_KMEM-config.patch
Patch19: 0001-cgroup-v1-cgroup_stat-support.patch

#vmxnet3
Patch20: 0001-vmxnet3-Remove-buf_info-from-device-accessible-struc.patch
# Upgrade to version 6
Patch21: 0001-vmxnet3-prepare-for-version-6-changes.patch
Patch22: 0002-vmxnet3-add-support-for-32-Tx-Rx-queues.patch
Patch23: 0003-vmxnet3-remove-power-of-2-limitation-on-the-queues.patch
Patch24: 0004-vmxnet3-add-support-for-ESP-IPv6-RSS.patch
Patch25: 0005-vmxnet3-set-correct-hash-type-based-on-rss-informati.patch
Patch26: 0006-vmxnet3-increase-maximum-configurable-mtu-to-9190.patch
Patch27: 0007-vmxnet3-update-to-version-6.patch
Patch28: 0001-vmxnet3-fix-minimum-vectors-alloc-issue.patch
# Upgrade to version 7
Patch29: 0001-vmxnet3-prepare-for-version-7-changes.patch
Patch30: 0002-vmxnet3-add-support-for-capability-registers.patch
Patch31: 0003-vmxnet3-add-support-for-large-passthrough-BAR-regist.patch
Patch32: 0004-vmxnet3-add-support-for-out-of-order-rx-completion.patch
Patch33: 0005-vmxnet3-add-command-to-set-ring-buffer-sizes.patch
Patch34: 0006-vmxnet3-limit-number-of-TXDs-used-for-TSO-packet.patch
Patch35: 0007-vmxnet3-use-ext1-field-to-indicate-encapsulated-pack.patch
Patch36: 0008-vmxnet3-update-to-version-7.patch
Patch37: 0001-vmxnet3-disable-overlay-offloads-if-UPT-device-does-.patch
Patch38: 0001-vmxnet3-do-not-reschedule-napi-for-rx-processing.patch
Patch40: 0002-vmxnet3-use-correct-intrConf-reference-when-using-ex.patch
Patch41: 0001-vmxnet3-move-rss-code-block-under-eop-descriptor.patch
Patch42: 0001-vmxnet3-use-gro-callback-when-UPT-is-enabled.patch

# Expose Photon kernel macros to identify kernel flavor and version
Patch50: 0001-kbuild-simplify-access-to-the-kernel-s-version.patch
Patch51: 0002-kbuild-replace-if-A-A-B-with-or-A-B.patch
Patch52: 0003-kbuild-Makefile-Introduce-macros-to-distinguish-Phot.patch
Patch53: 0004-linux-esx-Makefile-Add-kernel-flavor-info-to-the-gen.patch

# VMW: [54..59]
Patch54: x86-vmware-Use-Efficient-and-Correct-ALTERNATIVEs-fo.patch
Patch55: x86-vmware-Log-kmsg-dump-on-panic-510.patch
Patch56: x86-vmware-Fix-steal-time-clock-under-SEV.patch
Patch57: x86-probe_roms-Skip-OpROM-probing-if-running-as-VMwa.patch
Patch58: 0001-x86-vmware-avoid-TSC-recalibration.patch

#Kernel lockdown
Patch59: 0001-kernel-lockdown-when-UEFI-secure-boot-enabled.patch

# -esx
Patch60: init-do_mounts-recreate-dev-root.patch
Patch61: serial-8250-do-not-probe-U6-16550A-fifo-size.patch
Patch62: 01-clear-linux.patch
Patch63: 02-pci-probe.patch
Patch64: poweroff-without-firmware.patch
Patch65: 04-quiet-boot.patch
Patch66: 05-pv-ops-clocksource.patch
# TODO: make it working for v5.9+
#Patch67: 06-pv-ops-boot_clock.patch
Patch68: 07-vmware-only.patch
Patch69: 0001-initramfs-support-for-page-aligned-format-newca.patch
Patch70: 0001-Remove-OOM_SCORE_ADJ_MAX-limit-check.patch
Patch71: 0001-fs-VTAR-archive-to-TPMFS-extractor.patch
Patch72: 0001-fs-A-new-VTARFS-file-system-to-mount-VTAR-archive.patch
Patch73: halt-on-panic.patch
Patch77: revert-x86-entry-Align-entry-text-section-to-PMD-boundary.patch

%if 0%{?vmxnet3_sw_timestamp}
Patch78: 0009-esx-vmxnet3-software-timestamping.patch
%endif

#TARFS
Patch80:    0001-fs-TARFS-file-system-to-mount-TAR-archive.patch

# initialize MMCONFIG
Patch81: 0001-initialize-MMCONFIG-if-already-not-initialized.patch
Patch82: 0001-MMIO_should_have_more_priority_then_IO.patch
Patch83: 0001-Avoid-extra-scanning-for-peer-host-bridges.patch

# Disable md5 algorithm for sctp if fips is enabled.
Patch85: 0001-disable-md5-algorithm-for-sctp-if-fips-is-enabled.patch

# Hotplug support without firmware
Patch90: 0001-vmw_extcfg-hotplug-without-firmware-support.patch
Patch91: 0002-vmw_extcfg-hotplug-without-firmware-support.patch
Patch92: 0003-vmw_extcfg-hotplug-without-firmware-support.patch

%ifarch x86_64
# Driver VM patchset
Patch95: 0001-Adding-SBX-kernel-driver.patch
# Required for out of tree Intel i915 support
Patch96: 0001-Add-vmap_pfn-without-enabling-i915.patch
Patch97: linux-esx-Initialize-PAT-even-if-MTRR-is-not-set.patch
%endif

# CVE: [100..300]
Patch100: apparmor-fix-use-after-free-in-sk_peer_label.patch
# Fix CVE-2017-1000252
Patch101: KVM-Don-t-accept-obviously-wrong-gsi-values-via-KVM_.patch
# Fix for CVE-2019-12379
Patch102: consolemap-Fix-a-memory-leaking-bug-in-drivers-tty-v.patch

# Next 2 patches are about to be merged into stable
Patch103: 0001-mm-fix-panic-in-__alloc_pages.patch

# Fix for CVE-2021-4204
Patch104: 0002-bpf-Disallow-unprivileged-bpf-by-default.patch

# Fix for CVE-2022-3522
Patch106: 0001-mm_hugetlb_handle_pte_markers_in_page_faults.patch
Patch107: 0002-mm_hugetlb_fix_race_condition_of_uffd_missing_minor_handling.patch
Patch108: 0003-mm_hugetlb_use_hugetlb_pte_stable_in_migration_race_check.patch

# Fix for CVE-2022-0500
Patch114: 0001-bpf-Introduce-composable-reg-ret-and-arg-types.patch
Patch115: 0002-bpf-Replace-ARG_XXX_OR_NULL-with-ARG_XXX-PTR_MAYBE_N.patch
Patch116: 0003-bpf-Replace-RET_XXX_OR_NULL-with-RET_XXX-PTR_MAYBE_N.patch
Patch117: 0004-bpf-Extract-nullable-reg-type-conversion-into-a-help.patch
Patch118: 0005-bpf-Replace-PTR_TO_XXX_OR_NULL-with-PTR_TO_XXX-PTR_M.patch
Patch119: 0006-bpf-Introduce-MEM_RDONLY-flag.patch
Patch120: 0007-bpf-Make-per_cpu_ptr-return-rdonly-PTR_TO_MEM.patch
Patch121: 0008-bpf-Add-MEM_RDONLY-for-helper-args-that-are-pointers.patch

#Fix for CVE-2021-3699
Patch136: ipc-replace-costly-bailout-check-in-sysvipc_find_ipc.patch

#Fix for CVE-2023-0597
Patch137: 0001-x86-mm-Randomize-per-cpu-entry-area.patch
Patch138: 0002-x86-mm-Do-not-shuffle-CPU-entry-areas-without-KASLR.patch

#Fix CVE-2023-2176
Patch139: 0001-RDMA-core-Refactor-rdma_bind_addr.patch

#Fix CVE-2023-22995
Patch140: 0001-usb-dwc3-dwc3-qcom-Add-missing-platform_device_put-i.patch

# Fix CVE-2024-23307
Patch144: 0001-md-raid5-fix-atomicity-violation-in-raid5_cache_coun.patch

# Fix CVE-2024-26584
Patch146: 0001-tls-rx-simplify-async-wait.patch
Patch147: 0001-net-tls-factor-out-tls_-crypt_async_wait.patch
Patch148: 0001-net-tls-handle-backlogging-of-crypto-requests.patch

# Fix CVE-2024-26583
Patch151: 0001-tls-fix-race-between-async-notify-and-socket-close.patch

# Fix CVE-2024-26585
Patch152: 0001-tls-fix-race-between-tx-work-scheduling-and-socket-c.patch

# Fix CVE-2024-26589
Patch153: 0001-bpf-Reject-variable-offset-alu-on-PTR_TO_FLOW_KEYS.patch

# Fix CVE-2023-1192
Patch154: 0001-cifs-Fix-UAF-in-cifs_demultiplex_thread.patch

# Fix CVE-2024-26904
Patch155: 0001-btrfs-fix-data-race-at-btrfs_use_block_rsv.patch

# Fix CVE-2024-41073
Patch156: 0001-nvme-avoid-double-free-special-payload.patch

# Fix CVE-2024-43853
Patch157: 0001-cgroup-cpuset-Prevent-UAF-in-proc_cpuset_show.patch

# Fix CVE-2024-43854
Patch158: 0001-block-initialize-integrity-buffer-to-zero-before-wri.patch

# Fix CVE-2024-43835
Patch159: 0001-virtio_net-Fix-napi_skb_cache_put-warning.patch

# Fix CVE-2024-38577
Patch160: 0001-rcu-tasks-Fix-show_rcu_tasks_trace_gp_kthread-buffer.patch

# Fix CVE-2024-42228
Patch161: 0001-drm-amdgpu-Using-uninitialized-value-size-when-calli.patch

# Fix CVE-2024-42246
Patch162: 0001-net-sunrpc-Remap-EPERM-in-case-of-connection-failure.patch

# Fix CVE-2024-24855
Patch163: 0001-scsi-lpfc-Fix-a-possible-data-race-in-lpfc_unregiste.patch

#Patches for ptp_vmw
Patch301: 0001-ptp-ptp_vmw-Implement-PTP-clock-adjustments-ops.patch
Patch302: 0002-ptp-ptp_vmw-Add-module-param-to-probe-device-using-h.patch

# GPUs support for DriverVM
Patch400: amdgpu-Add-Missing-Sienna-Cichlid-DID.patch

# Crypto:
# Patch to add drbg_pr_ctr_aes256 test vectors to testmgr
Patch500: crypto-testmgr-Add-drbg_pr_ctr_aes256-test-vectors.patch
# Patch to call drbg and dh crypto tests from tcrypt
Patch501: tcrypt-disable-tests-that-are-not-enabled-in-photon.patch
Patch502: 0001-Initialize-jitterentropy-before-ecdh.patch
Patch503: 0002-FIPS-crypto-self-tests.patch
# Patch to remove urandom usage in rng module
Patch504: 0001-FIPS-crypto-rng-Jitterentropy-RNG-as-the-only-RND-source.patch
# Patch to remove urandom usage in drbg and ecc modules
Patch505: 0003-FIPS-crypto-drbg-Jitterentropy-RNG-as-the-only-RND.patch
#Patch to not make shash_no_setkey static
Patch506: 0001-fips-Continue-to-export-shash_no_setkey.patch
#Patch to introduce wrappers for random callback functions
Patch507: 0001-linux-crypto-Add-random-ready-callbacks-support.patch

%if 0%{?fips}
# FIPS canister usage patch
Patch508: 0001-FIPS-canister-binary-usage.patch
Patch509: 0001-scripts-kallsyms-Extra-kallsyms-parsing.patch
Patch510: 0001-Introduce_module_put_and_exit-function-to-address.patch
%else
%if 0%{?kat_build}
Patch510: 0003-FIPS-broken-kattest.patch
%endif
%endif

%if 0%{?fips}
#retpoline
Patch511: 0001-retpoline-re-introduce-alternative-for-r11.patch
%endif

# SEV:
Patch600: 0079-x86-sev-es-Disable-BIOS-ACPI-RSDP-probing-if-SEV-ES-.patch
Patch601: 0080-x86-boot-Enable-vmw-serial-port-via-Super-I-O.patch
Patch602: 0081-x86-sev-es-Disable-use-of-WP-via-PAT-for-__sme_early.patch
Patch603: x86-sev-es-load-idt-before-entering-long-mode-to-han-510.patch
Patch604: x86-swiotlb-Adjust-SWIOTLB-bounce-buffer-size-for-SE.patch
Patch605: x86-sev-es-Do-not-unroll-string-IO-for-SEV-ES-guests.patch
Patch606: 0001-x86-boot-Avoid-VE-during-boot-for-TDX-platforms.patch

%ifarch x86_64
#Patches for i40e driver
Patch1500: i40e-xdp-remove-XDP_QUERY_PROG-and-XDP_QUERY_PROG_HW-XDP-.patch
Patch1501: 0001-Add-support-for-gettimex64-interface.patch
Patch1502: i40e-don-t-install-auxiliary-module-on.patch
Patch1503: i40e-Make-i40e-driver-honor-default-and-user-defined.patch

#Patches for iavf driver
Patch1512: no-aux-symvers.patch

# Patches for ice driver
Patch1513: ice-don-t-install-auxiliary-module-on-modul.patch
Patch1514: ice-fix-redefinition-of-eth_hw_addr_set.patch
%endif

#Patches for vmci driver
Patch1521:       001-return-correct-error-code.patch
Patch1522:       002-switch-to-kvfree_rcu-API.patch
Patch1523:       003-print-unexpanded-names-of-ioctl.patch
Patch1524:       004-enforce-queuepair-max-size-for-IOCTL_VMCI_QUEUEPAIR_ALLOC.patch
Patch1531:       0001-whitespace-formatting-change-for-vmci-register-defines.patch
Patch1532:       0002-add-MMIO-access-to-registers.patch
Patch1533:       0003-detect-DMA-datagram-capability.patch
Patch1534:       0004-set-OS-page-size.patch
Patch1535:       0005-register-dummy-IRQ-handlers-for-DMA-datagrams.patch
Patch1536:       0006-allocate-send-receive-buffers-for-DMAdatagrams.patch
Patch1537:       0007-add-support-for-DMA-datagrams-send.patch
Patch1538:       0008-add-support-for-DMA-datagrams-receive.patch
Patch1539:       0009-fix-the-description-of-vmci_check_host_caps.patch
Patch1540:       0010-no-need-to-clear-memory-after-dma_alloc_coherent.patch
Patch1541:       0011-fix-error-handling-paths-in-vmci_guest_probe_device.patch
Patch1542:       0012-check-exclusive-vectors-when-freeing-interrupt1.patch
Patch1543:       0013-release-notification-bitmap-inn-error-path.patch
Patch1544:       0014-add-support-for-arm64.patch

BuildArch:     x86_64

BuildRequires: bc
BuildRequires: kbd
BuildRequires: kmod-devel
BuildRequires: glib-devel
BuildRequires: xerces-c-devel
BuildRequires: xml-security-c-devel
BuildRequires: libdnet-devel
BuildRequires: libmspack-devel
BuildRequires: Linux-PAM-devel
BuildRequires: openssl-devel
BuildRequires: procps-ng-devel
BuildRequires: lz4
BuildRequires: elfutils-libelf-devel
BuildRequires: bison

%if 0%{?fips}
BuildRequires: gdb
%endif

Requires: kmod
Requires: filesystem
Requires(pre): (coreutils or coreutils-selinux)
Requires(preun): (coreutils or coreutils-selinux)
Requires(post): (coreutils or coreutils-selinux)
Requires(postun): (coreutils or coreutils-selinux)

%description
The Linux kernel build for GOS for VMware hypervisor.
%if 0%{?fips}
This kernel is FIPS certified.
%endif
%if 0%{?vmxnet3_sw_timestamp}
- vmxnet3 with sotfware timestamping enabled
%endif

%package devel
Summary:       Kernel Dev
Group:         System Environment/Kernel
Requires:      python3
Requires:      gawk
Requires:      %{name} = %{version}-%{release}
%description devel
The Linux package contains the Linux kernel dev files

%package docs
Summary:       Kernel docs
Group:         System Environment/Kernel
Requires:      python3
Requires:      %{name} = %{version}-%{release}
%description docs
The Linux package contains the Linux kernel doc files

%prep
# Using autosetup is not feasible
%setup -q -n linux-%{version}
%ifarch x86_64
# Using autosetup is not feasible
%setup -q -T -D -b 6 -n linux-%{version}
# Using autosetup is not feasible
%setup -q -T -D -b 7 -n linux-%{version}
# Using autosetup is not feasible
%setup -q -T -D -b 8 -n linux-%{version}
%endif
%if 0%{?fips}
# Using autosetup is not feasible
%setup -q -T -D -b 16 -n linux-%{version}
%endif

%autopatch -p1 -m0 -M44

# VMW
%autopatch -p1 -m50 -M59

# -esx
%autopatch -p1 -m60 -M97

# CVE: [100..300]
%autopatch -p1 -m100 -M163

#Patches for ptp_vmw
%autopatch -p1 -m301 -M302

# GPUs support for DriverVM
%autopatch -p1 -m400 -M400

# crypto
%autopatch -p1 -m500 -M507

%if 0%{?fips}
%autopatch -p1 -m508 -M510
%else
%if 0%{?kat_build}
%autopatch -p1 -m510 -M510
%endif
%endif

%if 0%{?fips}
%autopatch -p1 -m511 -M511
%endif

# SEV
%autopatch -p1 -m600 -M606

%ifarch x86_64
# Patches for i40e driver
pushd ../i40e-%{i40e_version}
%autopatch -p1 -m1500 -M1503
popd

#Patches for iavf driver
pushd ../iavf-%{iavf_version}
%autopatch -p1 -m1512 -M1512
popd

#Patches for ice driver
pushd ../ice-%{ice_version}
%autopatch -p1 -m1513 -M1514
popd
%endif

# vmci
%autopatch -p1 -m1521 -M1544

%make_build mrproper
cp %{SOURCE1} .config
%if 0%{?fips}
cp ../fips-canister-%{fips_canister_version}/fips_canister.o crypto/
cp ../fips-canister-%{fips_canister_version}/fips_canister_wrapper.c crypto/
# Change m to y for modules that are in the canister
%include %{SOURCE17}
cp %{SOURCE18} crypto/
# Patch canister wrapper
patch -p1 < %{SOURCE19}
patch -p1 < %{SOURCE20}
patch -p1 < %{SOURCE21}
patch -p1 < %{SOURCE22}
patch -p1 < %{SOURCE25}
%else
%if 0%{?kat_build}
# Change m to y for modules in katbuild
%include %{SOURCE17}
%endif
%endif
sed -i 's/CONFIG_LOCALVERSION="-esx"/CONFIG_LOCALVERSION="-%{release}-esx"/' .config

%if 0%{?kat_build}
sed -i '/CONFIG_CRYPTO_SELF_TEST=y/a CONFIG_CRYPTO_BROKEN_KAT=y' .config
%endif

%include %{SOURCE4}

%build
%make_build KBUILD_BUILD_VERSION="1-photon" KBUILD_BUILD_HOST="photon" ARCH="x86_64"

%if 0%{?fips}
%include %{SOURCE9}
%endif

%ifarch x86_64
# build i40e module
bldroot="${PWD}"
pushd ../i40e-%{i40e_version}
%make_build -C src KSRC=${bldroot} clean
%make_build -C src KSRC=${bldroot}
popd

# build iavf module
pushd ../iavf-%{iavf_version}
%make_build -C src KSRC=${bldroot} clean
%make_build -C src KSRC=${bldroot}
popd

# build ice module
pushd ../ice-%{ice_version}
%make_build -C src KSRC=${bldroot} clean
%make_build -C src KSRC=${bldroot}
popd

%endif

%install
install -vdm 755 %{buildroot}%{_sysconfdir}
install -vdm 755 %{buildroot}/boot
install -vdm 755 %{buildroot}%{_docdir}/linux-%{uname_r}
install -vdm 755 %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}
%make_build INSTALL_MOD_PATH=%{buildroot} modules_install

%ifarch x86_64
# The auxiliary.ko kernel module is a common dependency for i40e, iavf
# and ice drivers.  Install it only once, along with the iavf driver
# and re-use it in the ice and i40e drivers.

# install i40e module
bldroot="${PWD}"
pushd ../i40e-%{i40e_version}
%make_build -C src KSRC=${bldroot} INSTALL_MOD_PATH=%{buildroot} \
    INSTALL_MOD_DIR=extra MANDIR=%{_mandir} modules_install_no_aux mandocs_install
popd

# install iavf module (with aux module)
pushd ../iavf-%{iavf_version}
%make_build -C src KSRC=$bldroot INSTALL_MOD_PATH=%{buildroot} INSTALL_MOD_DIR=extra \
    INSTALL_AUX_DIR=extra/auxiliary MANDIR=%{_mandir} modules_install \
    mandocs_install
install -Dvm 644 src/linux/auxiliary_bus.h \
       %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}/include/linux/auxiliary_bus.h
popd

# install ice module
pushd ../ice-%{ice_version}
%make_build -C src KSRC=${bldroot} MANDIR=%{_mandir} INSTALL_MOD_PATH=%{buildroot} \
            mandocs_install
%make_build -C src KSRC=${bldroot} INSTALL_MOD_PATH=%{buildroot} \
    INSTALL_MOD_DIR=extra modules_install_no_aux
popd
%endif

install -vm 644 arch/x86/boot/bzImage %{buildroot}/boot/vmlinuz-%{uname_r}
install -vm 400 System.map %{buildroot}/boot/System.map-%{uname_r}
install -vm 644 .config %{buildroot}/boot/config-%{uname_r}
cp -r Documentation/* %{buildroot}%{_docdir}/linux-%{uname_r}

%if 0%{?__debug_package}
install -vdm 755 %{buildroot}%{_libdir}/debug/%{_modulesdir}
install -vm 644 vmlinux %{buildroot}%{_libdir}/debug/%{_modulesdir}/vmlinux-%{uname_r}
%endif

# TODO: noacpi acpi=off noapic pci=conf1,nodomains pcie_acpm=off pnpacpi=off
cat > %{buildroot}/boot/linux-%{uname_r}.cfg << "EOF"
# GRUB Environment Block
photon_cmdline=init=/lib/systemd/systemd rcupdate.rcu_expedited=1 rw systemd.show_status=0 quiet noreplace-smp cpu_init_udelay=0
photon_linux=vmlinuz-%{uname_r}
photon_initrd=initrd.img-%{uname_r}
EOF

mkdir -p %{buildroot}%{_modulesdir}/dracut.conf.d/
cp -p %{SOURCE24} %{buildroot}%{_modulesdir}/dracut.conf.d/%{name}.conf

# cleanup dangling symlinks
rm -f %{buildroot}%{_modulesdir}/source \
      %{buildroot}%{_modulesdir}/build

# create /use/src/linux-headers-*/ content
find . -name Makefile* -o -name Kconfig* -o -name *.pl | xargs sh -c 'cp --parents "$@" %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}' copy
find arch/x86/include include scripts -type f | xargs sh -c 'cp --parents "$@" %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}' copy
find $(find arch/x86 -name include -o -name scripts -type d) -type f | xargs sh -c 'cp --parents "$@" %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}' copy
find arch/x86/include Module.symvers include scripts -type f | xargs sh -c 'cp --parents "$@" %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}' copy
%ifarch x86_64
# CONFIG_STACK_VALIDATION=y requires objtool to build external modules
install -vsm 755 tools/objtool/objtool %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}/tools/objtool/
install -vsm 755 tools/objtool/fixdep %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}/tools/objtool/
%endif

# copy .config manually to be where it's expected to be
cp .config %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}
# symling to the build folder
ln -sf "%{_usrsrc}/linux-headers-%{uname_r}" "%{buildroot}%{_modulesdir}/build"
find %{buildroot}/lib/modules -name '*.ko' -print0 | xargs -0 chmod u+x

%include %{SOURCE2}
%include %{SOURCE3}
%include %{SOURCE23}

%post
/sbin/depmod -a %{uname_r}
ln -sf linux-%{uname_r}.cfg /boot/photon.cfg

%files
%defattr(-,root,root)
/boot/System.map-%{uname_r}
/boot/config-%{uname_r}
/boot/vmlinuz-%{uname_r}
%config(noreplace) /boot/linux-%{uname_r}.cfg
/lib/modules/*
%exclude %{_modulesdir}/build
# iavf.conf is used to just blacklist the deprecated i40evf
# and create alias of i40evf to iavf.
# By default iavf is used for VF driver.
# This file creates conflict with other flavour of linux
# thus excluding this file from packaging
%exclude %{_sysconfdir}/modprobe.d/iavf.conf
# ICE driver firmware files are packaged in linux-firmware
%exclude /lib/firmware/updates/intel/ice

%config(noreplace) %{_modulesdir}/dracut.conf.d/%{name}.conf

%files docs
%defattr(-,root,root)
%{_defaultdocdir}/linux-%{uname_r}/*
%{_mandir}/*

%files devel
%defattr(-,root,root)
%{_modulesdir}/build
%{_usrsrc}/linux-headers-%{uname_r}

%changelog
* Tue Sep 10 2024 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 5.10.224-5
- Fix CVE-2024-24855 and CVE-2024-42246
* Sat Aug 31 2024 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 5.10.224-4
- Fix CVE-2024-38577, CVE-2024-42228
* Wed Aug 28 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 5.10.224-3
- Fix CVE-2024-43853, CVE-2024-43854
* Tue Aug 27 2024 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 5.10.224-2
- Fix CVE-2024-41073
* Tue Aug 20 2024 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 5.10.224-1
- Update to version 5.10.224
* Tue Aug 20 2024 Keerthana K <keerthana.kalyanasundaram@broadcom.com> 5.10.223-2
- Binary patch aesni_cpu_id value in canister
* Sun Aug 18 2024 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 5.10.223-1
- Update to version 5.10.223
* Tue Jul 23 2024 Harinadh Dommaraju <Harinadh.Dommaraju@broadcom.com> 5.10.222-2
- Fix CVE-2024-27397
* Fri Jul 19 2024 Ajay Kaher <ajay.kaher@broadcom.com> 5.10.222-1
- Update to version 5.10.222
- Fix for LTP fanotify22
* Tue Jul 09 2024 Ajay Kaher <ajay.kaher@broadcom.com> 5.10.219-3
- Fix for CVE-2022-48666
* Thu Jun 27 2024 Ashwin Dayanand Kamat <ashwin.kamat@broadcom.com> 5.10.219-2
- Fix for CVE-2024-36901
* Wed Jun 19 2024 Ashwin Dayanand Kamat <ashwin.kamat@broadcom.com> 5.10.219-1
- Update to version 5.10.219
* Tue May 07 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 5.10.216-1
- Update to version 5.10.216
* Fri Apr 12 2024 Ankit Jain <ankit-aj.jain@broadcom.com> 5.10.214-3
- Fix for CVE-2023-1192
* Wed Apr 03 2024 Kuntal Nayak <kuntal.nayak@broadcom.com> 5.10.214-2
- Patched CVE-2024-26643
* Wed Apr 03 2024 Keerthana K <keerthana.kalyanasundaram@broadcom.com> 5.10.214-1
- Update to version 5.10.214
- Fix CVE-2024-26642, CVE-2023-52620
* Mon Apr 01 2024 Ajay Kaher <ajay.kaher@broadcom.com> 5.10.212-4
- Fix CVE-2023-52585
* Mon Mar 25 2024 Srish Srinivasan <srish.srinivasan@broadcom.com> 5.10.212-3
- Patched CVE-2024-26583, CVE-2024-26585, and CVE-2024-26589
* Tue Mar 19 2024 Ashwin Dayanand Kamat <ashwin.kamat@broadcom.com> 5.10.212-2
- Fix for CVE-2023-52458/2023-52482
* Mon Mar 11 2024 Srish Srinivasan <srish.srinivasan@broadcom.com> 5.10.212-1
- Update to version 5.10.212, patched CVE-2024-26584
* Mon Mar 11 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com>  5.10.210-4
- Fixes CVE-2024-23307 and CVE-2024-22099
* Thu Mar 07 2024 Alexey Makhalov <alexey.makhalov@broadcom.com> 5.10.210-3
- Remove Intel i915 backported out of tree device driver.
* Wed Feb 28 2024 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 5.10.210-2
- Fix CVE-2024-0841
* Mon Feb 26 2024 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 5.10.210-1
- Update to version 5.10.210
* Tue Feb 13 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 5.10.209-4
- Patch from the same series that resolved CVE-2024-0565
* Tue Feb 13 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 5.10.209-3
- Fix CVE-2024-1086
* Mon Feb 12 2024 Ankit Jain <ankit-aj.jain@broadcom.com> 5.10.209-2
- initramfs: Fix freeing of 'newc' initrd when used in mix with 'newca'
* Sun Jan 28 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 5.10.209-1
- Update to version 5.10.209
* Mon Jan 22 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 5.10.206-5
- Fixes CVE-2024-0565 and CVE-2023-6915
* Mon Jan 22 2024 Ajay Kaher <ajay.kaher@broadcom.com> 5.10.206-4
- Fix CVE-2024-0607
* Tue Jan 16 2024 Ajay Kaher <ajay.kaher@broadcom.com> 5.10.206-3
- Fix CVE-2024-0340
* Mon Jan 15 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 5.10.206-2
- Build with gcc-10.5.0
* Tue Jan 09 2024 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 5.10.206-1
- Update to version 5.10.206
* Fri Dec 22 2023 Keerthana K <keerthanak@vmware.com> 5.10.201-2
- Increase CONFIG_LOG_BUF_SHIFT to 18
- Decrease CONFIG_LOG_CPU_MAX_BUF_SHIFT to 12
* Mon Nov 27 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 5.10.201-1
- Update to version 5.10.201
* Thu Nov 23 2023 Ankit Jain <ankitja@vmware.com> 5.10.200-3
- tarfs: Fixes file permission and buffer overflow issue
* Wed Nov 15 2023 Kuntal Nayak <nkuntal@vmware.com> 5.10.200-2
- Kconfig to lockdown kernel in UEFI Secure Boot
* Thu Nov 09 2023 Ankit Jain <ankitja@vmware.com> 5.10.200-1
- Update to version 5.10.200
* Wed Oct 25 2023 Alexey Makhalov <amakhalov@vmware.com> 5.10.198-2
- newca: fixes and enhancements
* Fri Oct 13 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 5.10.198-1
- Update to version 5.10.198
- Fix CVE-2023-4244
* Thu Oct 12 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 5.10.197-2
- Move kernel prep to %prep
* Tue Oct 03 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 5.10.197-1
- Update to version 5.10.197
- Undo commit 625bf86bf53eb7a8ee60fb9dc45b272b77e5ce1c as it breaks canister usage.
* Mon Oct 02 2023 Alexey Makhalov <amakhalov@vmware.com> 5.10.194-6
- LKCM: jitterentropy fix
* Sun Oct 01 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 5.10.194-5
- Fix for CVE-2023-42754
* Mon Sep 25 2023 Keerthana K <keerthanak@vmware.com> 5.10.194-4
- Fix CVE-2023-42756
* Mon Sep 25 2023 Keerthana K <keerthanak@vmware.com> 5.10.194-3
- Fix CVE-2023-42755
* Wed Sep 20 2023 Keerthana K <keerthanak@vmware.com> 5.10.194-2
- Fix CVE-2023-42753
* Tue Sep 12 2023 Roye Eshed <eshedr@vmware.com> 5.10.194-1
- Update to version 5.10.194
* Tue Sep 05 2023 Ankit Jain <ankitja@vmware.com> 5.10.190-3
- Fixes CVE-2023-22995
* Tue Sep 05 2023 Ankit Jain <ankitja@vmware.com> 5.10.190-2
- Fixes CVE-2023-2176
* Tue Aug 29 2023 Ajay Kaher <akaher@vmware.com> 5.10.190-1
- Update to version 5.10.190
* Fri Aug 25 2023 Srish Srinivasan <ssrish@vmware.com> 5.10.188-2
- Patched CVE-2023-4147, CVE-2023-4128
* Tue Aug 01 2023 Kuntal Nayak <nkuntal@vmware.com> 5.10.188-1
- Update to version 5.10.188
* Fri Jul 28 2023 Ajay Kaher <akaher@vmware.com> 5.10.186-2
- Fix: SEV: Guest should not disabled CR4.MCE
* Thu Jul 20 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 5.10.186-1
- Update to version 5.10.186
* Mon Jul 17 2023 Alexey Makhalov <amakhalov@vmware.com> 5.10.183-4
- Add Intel i915 backport in headless mode.
- Use PAT even if MTRR is not set (CRX case).
* Mon Jul 10 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 5.10.183-3
- Fix for CVE-2023-0597
* Thu Jul 06 2023 Garrett Goble <gobleg@vmware.com> 5.10.183-2
- Adding SBX kernel driver
* Thu Jun 08 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 5.10.183-1
- Update to version 5.10.183, fix some CVEs
* Wed May 17 2023 Ankit Jain <ankitja@vmware.com> 5.10.180-1
- Update to version 5.10.180
* Wed Apr 12 2023 Shreenidhi Shedi <sshedi@vmware.com> 5.10.175-4
- Fix initrd generation logic
* Tue Apr 11 2023 Roye Eshed <eshedr@vmware.com> 5.10.175-3
- Fix for CVE-2022-39189
* Mon Apr 10 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 5.10.175-2
- update to latest ToT vmxnet3 driver pathes
* Tue Apr 04 2023 Roye Eshed <eshedr@vmware.com> 5.10.175-1
- Update to version 5.10.175
* Tue Apr 04 2023 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.168-5
- Fix IRQ affinity of i40e driver
* Thu Mar 30 2023 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.168-4
- Expose Photon kernel macros to simplify building out-of-tree drivers.
* Mon Mar 20 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 5.10.168-3
- Update intel ethernet driver versions:
- iavf: 4.8.2
- i40e: 2.22.18
- ice: 1.11.14
* Fri Feb 24 2023 Ankit Jain <ankitja@vmware.com> 5.10.168-2
- Exclude iavf.conf
* Thu Feb 16 2023 Srish Srinivasan <ssrish@vmware.com> 5.10.168-1
- Update to version 5.10.168
* Tue Feb 14 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 5.10.165-2
- Fix for CVE-2022-2196/CVE-2022-4379
* Wed Feb 08 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 5.10.165-1
- Update to version 5.10.165
* Fri Feb 03 2023 Alexey Makhalov <amakhalov@vmware.com> 5.10.162-4
- Implement performance over security option for RETBleed (pos=1)
* Wed Jan 25 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 5.10.162-3
- initialize MMCONFIG, if already not initialized
* Fri Jan 20 2023 Alexey Makhalov <amakhalov@vmware.com> 5.10.162-2
- Support for missing Sienna Cichlid AMD GPU card.
* Tue Jan 17 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 5.10.162-1
- Update to version 5.10.162
* Thu Jan 12 2023 Alexey Makhalov <amakhalov@vmware.com> 5.10.159-3
- Introduce fips=2 and alg_request_report cmdline parameters
* Thu Jan 05 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 5.10.159-2
- update to latest ToT vmxnet3 driver
- Include patch "vmxnet3: correctly report csum_level for encapsulated packet"
* Mon Dec 19 2022 srinidhira0 <srinidhir@vmware.com> 5.10.159-1
- Update to version 5.10.159
* Wed Dec 14 2022 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 5.10.158-2
- update to latest ToT vmxnet3 driver
* Mon Dec 12 2022 Ankit Jain <ankitja@vmware.com> 5.10.158-1
- Update to version 5.10.158
* Tue Dec 06 2022 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 5.10.152-10
- Fix for CVE-2022-43945
* Mon Dec 05 2022 Srish Srinivasan <ssrish@vmware.com> 5.10.152-9
- Enable CONFIG_NET_CLS_FLOWER=m
* Wed Nov 30 2022 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 5.10.152-8
- Fix for CVE-2022-3564
* Mon Nov 28 2022 Ankit Jain <ankitja@vmware.com> 5.10.152-7
- Fix for CVE-2022-4139
* Mon Nov 28 2022 Ajay Kaher <akaher@vmware.com> 5.10.152-6
- Fix for CVE-2022-3522
* Mon Nov 14 2022 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 5.10.152-5
- vmxnet3 version 6,7 patches
* Wed Nov 09 2022 Ajay Kaher <akaher@vmware.com> 5.10.152-4
- Fix for CVE-2022-3623
* Fri Nov 04 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.152-3
- Fix CVE-2022-3524 and CVE-2022-3567
* Fri Nov 04 2022 Ankit Jain <ankitja@vmware.com> 5.10.152-2
- tarfs: fix readdir incase dir_emit fails
* Mon Oct 31 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.152-1
- Update to version 5.10.152
* Mon Oct 17 2022 Sharan Turlapati <sturlapati@vmware.com> 5.10.142-4
- Fix for CVE-2022-2602
* Thu Oct 13 2022 Sharan Turlapati <sturlapati@vmware.com> 5.10.142-3
- Fixes for CVEs in wifi subsystem
* Tue Oct 04 2022 Ankit Jain <ankitja@vmware.com> 5.10.142-2
- linux-esx: Enabling VFIO,UIO and IOMMU support
* Fri Sep 09 2022 srinidhira0 <srinidhir@vmware.com> 5.10.142-1
- Update to version 5.10.142
* Tue Aug 16 2022 srinidhira0 <srinidhir@vmware.com> 5.10.132-1
- Update to version 5.10.132
* Fri Aug 12 2022 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 5.10.118-14
- Backport fixes for CVE-2022-0500
* Mon Aug 08 2022 Shreenidhi Shedi <sshedi@vmware.com> 5.10.118-13
- Scriptlets fixes and improvements
* Fri Aug 05 2022 Him Kalyan Bordoloi <bordoloih@vmware.com> 5.10.118-12
- Fix for CVE-2022-2585, CVE-2022-2586 and CVE-2022-2588
* Fri Jul 29 2022 Ankit Jain <ankitja@vmware.com> 5.10.118-11
- tarfs: fix error for empty tar archive
* Tue Jul 26 2022 Ankit Jain <ankitja@vmware.com> 5.10.118-10
- Fix multiple issues in tarfs
* Mon Jul 18 2022 Keerthana K <keerthanak@vmware.com> 5.10.118-9
- Update iavf driver to v4.4.2
- Update ice driver to v1.8.3
- .config: Enable CONFIG_NET_DEVLINK=y (ice v1.8.3 needs it)
* Mon Jul 18 2022 Keerthana K <keerthanak@vmware.com> 5.10.118-8
- .config: enable CROSS_MEMORY_ATTACH
- Add elfutils-libelf-devel required to build objtool
- vmxnet3: enable software timestamping
* Fri Jul 15 2022 Keerthana K <keerthanak@vmware.com> 5.10.118-7
- .config: disable kernel accounting for memory cgroups
- Enable cgroup v1 stats
- .config: enable PERCPU_STATS
* Fri Jul 15 2022 Keerthana K <keerthanak@vmware.com> 5.10.118-6
- Avoid TSC recalibration
* Wed Jul 13 2022 Srinidhi Rao <srinidhir@vmware.com> 5.10.118-5
- Fix for CVE-2022-21505
* Tue Jul 12 2022 Keerthana K <keerthanak@vmware.com> 5.10.118-4
- Reduce FIPS canister memory footprint by disabling CONFIG_KALLSYMS_ALL
- Add only fips_canister-kallsyms to vmlinux instead of all symbols
* Fri Jul 01 2022 HarinadhD <hdommaraju@vmware.com> 5.10.118-3
- VMCI patches & configs
* Fri Jun 24 2022 Shreenidhi Shedi <sshedi@vmware.com> 5.10.118-2
- Fix debug_package macro usage while adding vmlinux to debuginfo rpm
* Mon Jun 13 2022 Sharan Turlapati <sturlapati@vmware.com> 5.10.118-1
- Update to version 5.10.118
* Wed Jun 01 2022 Ajay Kaher <akaher@vmware.com> 5.10.109-4
- Fix for CVE-2022-1966, CVE-2022-1972
* Tue May 24 2022 Sharan Turlapati <sturlapati@vmware.com> 5.10.109-3
- Fix for CVE-2022-21499
* Thu May 12 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 5.10.109-2
- Fix for CVE-2022-29582
* Fri Apr 29 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 5.10.109-1
- Update to version 5.10.109
* Mon Apr 18 2022 Alexey Makhalov <amakhalov@vmware.com> 5.10.103-5
- Add objtool to the -devel package.
- .config: increase kernel log buffer size.
* Tue Apr 05 2022 Alexey Makhalov <amakhalov@vmware.com> 5.10.103-4
- .config: enable squashfs module, enable crypto user api rng.
- .config: enable CONFIG_EXT2_FS_XATTR
* Mon Mar 21 2022 Ajay Kaher <akaher@vmware.com> 5.10.103-3
- Fix for CVE-2022-1016
* Mon Mar 14 2022 Bo Gan <ganb@vmware.com> 5.10.103-2
- Fix SEV and Hypercall alternative inst. patches
* Tue Mar 08 2022 srinidhira0 <srinidhir@vmware.com> 5.10.103-1
- Update to version 5.10.103
* Tue Mar 01 2022 Alexey Makhalov <amakhalov@vmware.com> 5.10.93-8
- Reduce kernel .text size by ~40% by removing .entry.text alignment
- Reduce kernel .data section by configuring smaller kernel log buffer
- Speedup algos registration in non-fips mode
* Mon Feb 28 2022 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 5.10.93-7
- Port non-acpi hotplug support patch to 5.10.x
* Mon Feb 14 2022 Ankit Jain <ankitja@vmware.com> 5.10.93-6
- vtarfs: fixes multiple issues
- tarfs: support for hardlink, fixes uid/gid/mode issues
* Wed Feb 09 2022 Sharan Turlapati <sturlapati@vmware.com> 5.10.93-5
- Fix for CVE-2022-0435
* Sat Feb 05 2022 Sharan Turlapati <sturlapati@vmware.com> 5.10.93-4
- Fix for CVE-2022-0492
* Tue Jan 25 2022 Sharan Turlapati <sturlapati@vmware.com> 5.10.93-3
- Fix for CVE-2022-22942
* Tue Jan 25 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.93-2
- Fix CVE-2022-0330
* Fri Jan 21 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.93-1
- Update to version 5.10.93
* Wed Jan 12 2022 Deep Shah <sdeep@vmware.com> 5.10.83-8
- Update ptp_vmw with provider mode support
* Sat Jan 08 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.83-7
- Fix CVE-2021-4155 and CVE-2021-4204
* Mon Dec 20 2021 Keerthana K <keerthanak@vmware.com> 5.10.83-6
- crypto_self_test and broken kattest module enhancements
- FIPS: Add module signing for crypto modules
* Fri Dec 17 2021 Alexey Makhalov <amakhalov@vmware.com> 5.10.83-5
- mm: fix percpu alloacion for memoryless nodes
- pvscsi: fix disk detection issue
* Fri Dec 17 2021 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 5.10.83-4
- Disable md5 algorithm for sctp if fips is enabled.
* Tue Dec 14 2021 Harinadh D <hdommaraju@vmware.com> 5.10.83-3
- remove lvm in add-drivers list
- lvm drivers are built as part of dm-mod
* Wed Dec 08 2021 Ankit Jain <ankitja@vmware.com> 5.10.83-2
- tarfs: Fix binary execution issue
* Mon Dec 06 2021 srinidhira0 <srinidhir@vmware.com> 5.10.83-1
- Update to version 5.10.83
* Fri Nov 12 2021 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 5.10.78-4
- tarfs: A new readonly filesystem to mount tar archive
* Thu Nov 11 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 5.10.78-3
- compile with openssl 3.0.0
* Mon Nov 08 2021 Keerthana K <keerthanak@vmware.com> 5.10.78-2
- Add out-of-tree i40e, iavf and ice drivers.
* Mon Nov 08 2021 Vikash Bansal <bvikas@vmware.com> 5.10.78-1
- Update to version 5.10.78
* Tue Oct 26 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.75-1
- Update to version 5.10.75
* Mon Oct 18 2021 Alexey Makhalov <amakhalov@vmware.com> 5.10.61-5
- initramfs: large files support for newca
* Wed Oct 06 2021 Ankit Jain <ankitja@vmware.com> 5.10.61-4
- vtarfs: Fix memory allocation for entry pages
* Fri Sep 17 2021 Ankit Jain <ankitja@vmware.com> 5.10.61-3
- vtarfs: Added support for LongFilename/LongLink
* Tue Sep 07 2021 Ankit Jain <ankitja@vmware.com> 5.10.61-2
- vtarfs: Fix crash in vtarfs_file_read_iter()
* Fri Aug 27 2021 Ankit Jain <ankitja@vmware.com> 5.10.61-1
- Update to version 5.10.61
* Wed Aug 25 2021 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.52-3
- Enable ptp_vmw module (CONFIG_PTP_1588_CLOCK_VMW) in the config.
* Mon Aug 09 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 5.10.52-2
- Port crx patches
* Thu Aug 05 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 5.10.52-1
- Update to version 5.10.52
* Wed Jul 28 2021 Ankit Jain <ankitja@vmware.com> 5.10.46-3
- vtarfs: Fixed multiple mount executable issue,
- Fixed fault handler
* Thu Jul 15 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 5.10.46-2
- Fix for CVE-2021-33909
* Mon Jun 28 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.46-1
- Update to version 5.10.46
* Tue Jun 22 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.42-3
- Fix for CVE-2021-3609
* Thu Jun 10 2021 Keerthana K <keerthanak@vmware.com> 5.10.42-2
- Added script to check structure compatibility between fips_canister.o and vmlinux.
* Thu Jun 03 2021 Keerthana K <keerthanak@vmware.com> 5.10.42-1
- Update to version 5.10.42
- .config: Enable CONFIG_FANOTIFY_ACCESS_PERMISSIONS
* Mon May 17 2021 Ajay Kaher <akaher@vmware.com> 5.10.35-1
- Update to version 5.10.35
* Thu May 13 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.25-10
- Fix for CVE-2021-23133
* Wed May 12 2021 Ankit Jain <ankitja@vmware.com> 5.10.25-9
- .config: Enable Netfilter modules required for NFT support
- .config: Enable Bonding driver support, NET_TEAM, NET_VRF
* Tue May 11 2021 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.25-8
- Fix CVE-2020-26147, CVE-2020-24587, CVE-2020-24586, CVE-2020-24588,
- CVE-2020-26145, CVE-2020-26141
* Tue May 11 2021 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.25-7
- Fix CVE-2021-3489, CVE-2021-3490, CVE-2021-3491
* Tue May 04 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.25-6
- Remove buf_info from device accessible structures in vmxnet3
* Thu Apr 29 2021 Alexey Makhalov <amakhalov@vmware.com> 5.10.25-5
- Update canister binary.
- use jent by drbg and ecc.
- Enable hmac(sha224) self test and broket KAT test.
* Thu Apr 22 2021 Keerthana K <keerthanak@vmware.com> 5.10.25-4
- Remove hmac(sha224) from broken kat test.
* Thu Apr 15 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.25-3
- Fix for CVE-2021-23133
* Thu Apr 15 2021 Srinidhi Rao <srinidhir@vmware.com> 5.10.25-2
- Fix for CVE-2021-29154
* Mon Mar 22 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 5.10.25-1
- Update to version 5.10.25
* Sun Mar 21 2021 Alexey Makhalov <amakhalov@vmware.com> 5.10.21-3
- Do not execute some tests twice
- Support future disablement of des3
- Do verbose build
- Canister update.
* Mon Mar 15 2021 Srinidhi Rao <srinidhir@vmware.com> 5.10.21-2
- Use jitterentropy rng instead of urandom in rng module.
* Mon Mar 08 2021 Vikash Bansal <bvikas@vmware.com> 5.10.21-1
- Update to version 5.10.21
* Mon Mar 01 2021 Alexey Makhalov <amakhalov@vmware.com> 5.10.4-14
- Enable FIPS canister
* Fri Feb 19 2021 Ankit Jain <ankitja@vmware.com> 5.10.4-13
- Enable CONFIG_ISCSI_TCP support
* Fri Feb 19 2021 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.4-12
- Fix /boot/photon.cfg symlink when /boot is a separate partition.
* Fri Feb 19 2021 Ajay Kaher <akaher@vmware.com> 5.10.4-11
- Added SEV-ES improvement patches
* Thu Feb 18 2021 Keerthana K <keerthanak@vmware.com> 5.10.4-10
- Disable fips canister.
* Thu Feb 18 2021 Ajay Kaher <akaher@vmware.com> 5.10.4-9
- Enable CONFIG_WDAT_WDT
* Thu Feb 18 2021 Ajay Kaher <akaher@vmware.com> 5.10.4-8
- lower the loglevel for floppy driver
* Mon Feb 15 2021 Ankit Jain <ankitja@vmware.com> 5.10.4-7
- Enable CONFIG_NF_TABLES support
* Thu Feb 11 2021 Keerthana K <keerthanak@vmware.com> 5.10.4-6
- Added crypto_self_test and kattest module.
- These patches are applied when kat_build is enabled.
* Wed Feb 03 2021 Ankit Jain <ankitja@vmware.com> 5.10.4-5
- Replaced syscalls routines based on user space address
- Removed set_fs() calls
* Thu Jan 28 2021 Alexey Makhalov <amakhalov@vmware.com> 5.10.4-4
- Use secure FIPS canister.
* Mon Jan 25 2021 Ankit Jain <ankitja@vmware.com> 5.10.4-3
- Enabled CONFIG_WIREGUARD
* Mon Jan 25 2021 Alexey Makhalov <amakhalov@vmware.com> 5.10.4-2
- Build kernel with FIPS canister.
* Wed Jan 06 2021 Bo Gan <ganb@vmware.com> 5.10.4-1
- Update to 5.10.4
- Drop out-of-tree SEV-ES functional patches (already upstreamed).
* Thu Dec 03 2020 Alexey Makhalov <amakhalov@vmware.com> 5.9.0-8
- halt_on_panic kernel cmdline.
- Improve no ACPI poweroff patch to support direct boot.
- .config: enable CONFIG_POWER_RESET_PIIX4_POWEROFF.
* Wed Nov 18 2020 Vikash Bansal <bvikas@vmware.com> 5.9.0-7
- Mark BAR0 (at offset 0x10) for PCI device 15ad:07b0 (VMXNET3) as variable
* Thu Nov 12 2020 Ajay Kaher <akaher@vmware.com> 5.9.0-6
- .config: support for floppy disk and ch341 usb to serial
* Tue Nov 10 2020 Keerthana K <keerthanak@vmware.com> 5.9.0-5
- Fix CVE-2020-8694
* Fri Nov 06 2020 Keerthana K <keerthanak@vmware.com> 5.9.0-4
- Fix CVE-2020-25704
* Tue Nov 03 2020 Srinidhi Rao <srinidhir@vmware.com> 5.9.0-3
- Remove the support of fipsify and hmacgen
* Tue Oct 27 2020 Srinidhi Rao <srinidhir@vmware.com> 5.9.0-2
- Enable vtarfs support as module
* Mon Oct 19 2020 Bo Gan <ganb@vmware.com> 5.9.0-1
- Update to 5.9.0
* Thu Oct 08 2020 Ankit Jain <ankitja@vmware.com> 5.9.0-rc7.2
- Added vtar Support.
- Disabled by default, Enable CONFIG_VTAR as builtin only
* Wed Sep 30 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.9.0-rc7.1
- Update to version 5.9.0-rc7
* Mon Sep 21 2020 Bo Gan <ganb@vmware.com> 5.9.0-rc4.1
- Update to 5.9.0-rc4
- AMD SEV-ES Support
* Tue Sep 8 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.127-4
- Enable sysrq magic in config
* Mon Jul 27 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.127-3
- Fix CVE-2020-14331
* Tue Jun 23 2020 Tapas Kundu <tkundu@vmware.com> 4.19.127-2
- Mass Removal Python2
* Tue Jun 23 2020 Keerthana K <keerthanak@vmware.com> 4.19.127-1
- Update to version 4.19.127
* Fri Jun 05 2020 Ankit Jain <ankitja@vmware.com> 4.19.115-5
- Enabled CONFIG_BINFMT_MISC
* Wed Jun 03 2020 Alexey Makhalov <amakhalov@vmware.com> 4.19.115-4
- fs/9p: local lock support
* Tue Jun 02 2020 Vikash Bansal <bvikas@vmware.com> 4.19.115-3
- Add patch to fix CVE-2019-18885
* Mon Jun 01 2020 Shreenidhi Shedi <sshedi@vmware.com> 4.19.115-2
- Keep modules of running kernel till next boot
* Fri May 29 2020 Alexey Makhalov <amakhalov@vmware.com> 4.19.115-1
- initramfs: zero-copy support
* Wed May 06 2020 Siddharth Chandrasekaran <csiddharth@vmware.com> 4.19.112-9
- Add patch to fix CVE-2020-10711
* Wed May 06 2020 Vikash Bansal <bvikas@vmware.com> 4.19.112-8
- Hardcoded the value of BARs in PCI_Probe for 2 more pci devices
* Wed Apr 29 2020 Keerthana K <keerthanak@vmware.com> 4.19.112-7
- Photon-checksum-generator version update to 1.1.
* Fri Apr 24 2020 Vikash Bansal <bvikas@vmware.com> 4.19.112-6
- Modified PCI Probe patch to store hardcoded values in lookup table
* Thu Apr 23 2020 Keerthana K <keerthanak@vmware.com> 4.19.112-5
- Fix __modules_install_post to skip compression for certain modules.
* Wed Apr 22 2020 Vikash Bansal <bvikas@vmware.com> 4.19.112-4
- Corrected number of bars for "LSI Logic" and typepo in is_known_device call
* Wed Apr 15 2020 Vikash Bansal <bvikas@vmware.com> 4.19.112-3
- HMAC-SHA256 digest of hmac_generator module moved to hmacgen package
* Tue Apr 14 2020 Alexey Makhalov <amakhalov@vmware.com> 4.19.112-2
- Refactor PCI probe patch (03-pci-probe.patch)
* Wed Apr 08 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.112-1
- Update to version 4.19.112
* Wed Apr 08 2020 Alexey Makhalov <amakhalov@vmware.com> 4.19.104-3
- Improve hardcodded poweroff (03-poweroff.patch)
* Tue Mar 31 2020 Vikash Bansal <bvikas@vmware.com> 4.19.104-2
- hmac generation of crypto modules and initrd generation changes if fips=1
* Wed Mar 25 2020 Vikash Bansal <bvikas@vmware.com> 4.19.104-1
- Update to version 4.19.104
* Mon Mar 16 2020 Keerthana K <keerthanak@vmware.com> 4.19.97-8
- Adding Enhances depedency to hmacgen.
* Fri Mar 06 2020 Alexey Makhalov <amakhalov@vmware.com> 4.19.97-7
- 9p: file attributes caching support (cache=stat)
* Wed Mar 04 2020 Vikash Bansal <bvikas@vmware.com> 4.19.97-6
- Backporting of patch continuous testing of RNG from urandom
* Fri Feb 28 2020 Keerthana K <keerthanak@vmware.com> 4.19.97-5
- Enable CONFIG_CRYPT_TEST for FIPS.
* Tue Feb 25 2020 Ajay Kaher <akaher@vmware.com> 4.19.97-4
- Fix CVE-2019-16234
* Tue Feb 11 2020 Keerthana K <keerthanak@vmware.com> 4.19.97-3
- Add photon-checksum-generator source tarball and remove hmacgen patch.
- Exclude hmacgen.ko from base package.
* Wed Jan 29 2020 Keerthana K <keerthanak@vmware.com> 4.19.97-2
- Update tcrypt to test drbg_pr_sha256 and drbg_nopr_sha256.
- Update testmgr to add drbg_pr_ctr_aes256 test vectors.
* Fri Jan 17 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.97-1
- Update to version 4.19.97
* Thu Jan 16 2020 Srinidhi Rao <srinidhir@vmware.com> 4.19.87-5
- Enable DRBG HASH and DRBG CTR support.
* Mon Jan 06 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.87-4
- Enable CONFIG_NF_CONNTRACK_ZONES
* Thu Jan 02 2020 Keerthana K <keerthanak@vmware.com> 4.19.87-3
- Modify tcrypt to remove tests for algorithms that are not supported in photon.
- Added tests for DH, DRBG algorithms.
* Fri Dec 20 2019 Keerthana K <keerthanak@vmware.com> 4.19.87-2
- Update fips Kat tests.
* Fri Dec 06 2019 Ajay Kaher <akaher@vmware.com> 4.19.87-1
- Update to version 4.19.87
* Tue Dec 03 2019 Keerthana K <keerthanak@vmware.com> 4.19.84-3
- Adding hmac sha256/sha512 generator kernel module for fips.
* Tue Nov 26 2019 Ajay Kaher <akaher@vmware.com> 4.19.84-2
- Fix CVE-2019-19062, CVE-2019-19066, CVE-2019-19072,
- CVE-2019-19073, CVE-2019-19074, CVE-2019-19078
* Tue Nov 12 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.84-1
- Update to version 4.19.84
- Fix CVE-2019-18814
* Fri Nov 08 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.82-1
- Update to version 4.19.82
* Thu Nov 07 2019 Jorgen Hansen (VMware) <jhansen@vmware.com> 4.19.79-2
- Fix vsock QP detach with outgoing data
* Tue Oct 15 2019 Ajay Kaher <akaher@vmware.com> 4.19.79-1
- Update to version 4.19.79
- Fix CVE-2019-17133
* Mon Oct 14 2019 Bo Gan <ganb@vmware.com> 4.19.76-4
- Recreate /dev/root in init
* Mon Oct 14 2019 Bo Gan <ganb@vmware.com> 4.19.76-3
- Enable IMA with SHA256 as default hash algorithm
* Thu Oct 10 2019 Harinadh D <hdommaraju@vmware.com> 4.19.76-2
- Adding lvm and dm-mod modules to support root as lvm
* Wed Oct 02 2019 Ajay Kaher <akaher@vmware.com> 4.19.76-1
- Update to version 4.19.76
* Mon Sep 30 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.72-1
- Update to version 4.19.72
* Thu Sep 05 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.69-2
- Avoid oldconfig which leads to potential build hang
* Fri Aug 30 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.69-1
- Update to version 4.19.69
* Fri Aug 23 2019 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.65-3
- .config: Enable CONFIG_IP_VS_WRR, CONFIG_IP_VS_SH, CONFIG_FB_EFI, CONFIG_TCG_TIS_CORE
* Tue Aug 13 2019 Daniel Müller <danielmuller@vmware.com> 4.19.65-2
- Add patch "Remove OOM_SCORE_ADJ_MAX limit check"
* Tue Aug 06 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.65-1
- Update to version 4.19.65
- Fix CVE-2019-1125 (SWAPGS)
* Tue Jul 30 2019 Keerthana K <keerthanak@vmware.com> 4.19.52-4
- Fix postun script.
* Tue Jul 02 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.52-3
- Fix 9p vsock 16bit port issue.
* Fri Jun 21 2019 Srinidhi Rao <srinidhir@vmware.com> 4.19.52-2
- Use LZ4 compression and enable VMXNET3 as built-in for linux-esx
* Mon Jun 17 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.52-1
- Update to version 4.19.52
- Fix CVE-2019-12456, CVE-2019-12379, CVE-2019-12380, CVE-2019-12381,
- CVE-2019-12382, CVE-2019-12378, CVE-2019-12455
* Tue May 14 2019 Keerthana K <keerthanak@vmware.com> 4.19.40-2
- Fix to parse through /boot folder and update symlink (/boot/photon.cfg) if
- mulitple kernels are installed and current linux kernel is removed.
* Tue May 07 2019 Ajay Kaher <akaher@vmware.com> 4.19.40-1
- Update to version 4.19.40
* Fri May 03 2019 Ajay Kaher <akaher@vmware.com> 4.19.32-3
- Enable SELinux kernel config
* Fri Mar 29 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.32-2
- Fix CVE-2019-10125
* Wed Mar 27 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.32-1
- Update to version 4.19.32
* Thu Mar 14 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.29-1
- Update to version 4.19.29
* Tue Mar 05 2019 Ajay Kaher <akaher@vmware.com> 4.19.26-1
- Update to version 4.19.26
* Thu Feb 21 2019 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.15-2
- Fix CVE-2019-8912
* Tue Jan 15 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.15-1
- Update to version 4.19.15
- .config: Enable USB_SERIAL and USB_ACM
* Tue Jan 08 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.6-4
- Additional security hardening options in the config.
* Tue Jan 08 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.6-3
- Fix crash on cpu hot-add.
* Fri Jan 04 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.6-2
- Add out-of-tree patches from AppArmor and enable it by default.
* Mon Dec 10 2018 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.6-1
- Update to version 4.19.6
* Thu Nov 29 2018 Alexey Makhalov <amakhalov@vmware.com> 4.19.1-3
- Fix BAR4 is zero issue for IDE devices
* Thu Nov 15 2018 Ajay Kaher <akaher@vmware.com> 4.19.1-2
- Adding BuildArch
* Thu Nov 08 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.1-1
- Update to version 4.19.1
* Mon Sep 24 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.18.9-1
- Update to version 4.18.9
* Wed Sep 19 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.14.67-1
- Update to version 4.14.67
* Tue Sep 18 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.14.54-3
- Add rdrand-based RNG driver to enhance kernel entropy.
* Sun Sep 02 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.14.54-2
- Add full retpoline support by building with retpoline-enabled gcc.
* Mon Jul 09 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.14.54-1
- Update to version 4.14.54
* Fri Feb 02 2018 Alexey Makhalov <amakhalov@vmware.com> 4.14.8-1
- Version update
* Tue Dec 19 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.66-2
- Enable audit support (CONFIG_AUDIT=y)
* Mon Dec 04 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.66-1
- Version update
* Tue Nov 21 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.64-1
- Version update
* Mon Nov 06 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.60-1
- Version update
* Wed Oct 25 2017 Anish Swaminathan <anishs@vmware.com> 4.9.53-5
- Enable x86 vsyscall emulation
* Tue Oct 17 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.53-4
- Enable vsyscall emulation
- Do not use deprecated -q depmod option
* Wed Oct 11 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.53-3
- Add patch "KVM: Don't accept obviously wrong gsi values via
  KVM_IRQFD" to fix CVE-2017-1000252.
* Tue Oct 10 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.53-2
- Build hang (at make oldconfig) fix.
* Thu Oct 05 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.53-1
- Version update
* Mon Oct 02 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.52-3
- Allow privileged CLONE_NEWUSER from nested user namespaces.
* Mon Oct 02 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.52-2
- Fix CVE-2017-11472 (ACPICA: Namespace: fix operand cache leak)
* Mon Oct 02 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.52-1
- Version update
* Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.47-2
- Requires coreutils or toybox
* Mon Sep 04 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.47-1
- Fix CVE-2017-11600
* Mon Aug 14 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.43-1
- Version update
- [feature] new sysctl option unprivileged_userns_clone
* Wed Aug 09 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.41-2
- [bugfix] Do not fallback to syscall from VDSO on clock_gettime(MONOTONIC)
- Fix CVE-2017-7542
* Mon Aug 07 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.41-1
- Version update
* Wed Jul 26 2017 Bo Gan <ganb@vmware.com> 4.9.38-3
- Fix initramfs triggers
* Thu Jul 20 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.38-2
- Disable scheduler beef up patch
* Tue Jul 18 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.38-1
- [feature] IP tunneling support (CONFIG_NET_IPIP=m)
- Fix CVE-2017-11176 and CVE-2017-10911
* Mon Jul 03 2017 Xiaolin Li <xiaolinl@vmware.com> 4.9.34-2
- Add libdnet-devel, kmod-devel and libmspack-devel to BuildRequires
* Wed Jun 28 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.34-1
- [feature] DM Delay target support
- Fix CVE-2017-1000364 ("stack clash") and CVE-2017-9605
* Thu Jun 8 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.31-1
- Fix CVE-2017-8890, CVE-2017-9074, CVE-2017-9075, CVE-2017-9076
    CVE-2017-9077 and CVE-2017-9242
* Thu Jun 1 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.30-2
- [feature] ACPI NFIT support (for PMEM type 7)
* Fri May 26 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.30-1
- Fix CVE-2017-7487 and CVE-2017-9059
* Wed May 17 2017 Vinay Kulkarni <kulkarniv@vmware.com> 4.9.28-2
- Enable IPVLAN module.
* Tue May 16 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.28-1
- .config: built ATA drivers in a kernel
* Wed May 10 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.27-1
- New pci=scan_all cmdline parameter to verify hardcoded pci-probe values
- pci-probe added more known values
- vmw_balloon late initcall
* Sun May 7 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.26-1
- Version update
- Use ordered rdtsc in clocksource_vmware
- .config: added debug info
- Removed version suffix from config file name
* Thu Apr 27 2017 Bo Gan <ganb@vmware.com> 4.9.24-2
- Support dynamic initrd generation
* Tue Apr 25 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.24-1
- Fix CVE-2017-6874 and CVE-2017-7618.
- .config: build nvme and nvme-core in kernel.
* Tue Feb 28 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.13-1
- Update to linux-4.9.13 to fix CVE-2017-5986 and CVE-2017-6074
- .config: enable PMEM support
- .config: disable vsyscall
* Thu Feb 09 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.9-1
- Update to linux-4.9.9 to fix CVE-2016-10153, CVE-2017-5546,
    CVE-2017-5547, CVE-2017-5548 and CVE-2017-5576.
- .config: added CRYPTO_FIPS and SYN_COOKIES support.
* Tue Jan 10 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.2-1
- Update to linux-4.9.2 to fix CVE-2016-10088
* Wed Dec 21 2016 Alexey Makhalov <amakhalov@vmware.com> 4.9.0-3
- .config: CONFIG_IPV6_MULTIPLE_TABLES=y
* Mon Dec 19 2016 Xiaolin Li <xiaolinl@vmware.com> 4.9.0-2
- BuildRequires Linux-PAM-devel
* Mon Dec 12 2016 Alexey Makhalov <amakhalov@vmware.com> 4.9.0-1
- Update to linux-4.9.0
* Thu Dec  8 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.35-4
- net-packet-fix-race-condition-in-packet_set_ring.patch
    to fix CVE-2016-8655
* Wed Nov 30 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.35-3
- Expand `uname -r` with release number
- Compress modules
* Tue Nov 29 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.35-2
- Added btrfs module
* Mon Nov 28 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.35-1
- Update to linux-4.4.35
- vfio-pci-fix-integer-overflows-bitmask-check.patch
    to fix CVE-2016-9083
* Tue Nov 22 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.31-4
- net-9p-vsock.patch
* Thu Nov 17 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.31-3
- tty-prevent-ldisc-drivers-from-re-using-stale-tty-fields.patch
    to fix CVE-2015-8964
* Tue Nov 15 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.31-2
- .config: add ip set support
- .config: add ipvs_{tcp,udp} support
- .config: add cgrup_{hugetlb,net_prio} support
* Thu Nov 10 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.31-1
- Update to linux-4.4.31
* Thu Nov 10 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.26-2
- .config: add ipvs modules for docker swarm
- .config: serial driver built in kernel
- serial-8250-do-not-probe-U6-16550A-fifo-size.patch - faster boot
* Fri Oct 21 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.26-1
- Update to linux-4.4.26
* Wed Oct 19 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.20-7
- net-add-recursion-limit-to-GRO.patch
* Tue Oct 18 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.20-6
- ipip-properly-mark-ipip-GRO-packets-as-encapsulated.patch
- tunnels-dont-apply-GRO-to-multiple-layers-of-encapsulation.patch
* Thu Oct  6 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.20-5
- .config: added ADM PCnet32 support
- vmci-1.1.4.0-use-32bit-atomics-for-queue-headers.patch
- vmci-1.1.5.0-doorbell-create-and-destroy-fixes.patch
- late_initcall for vmw_balloon driver
- Minor fixed in pv-ops patchset
* Mon Oct  3 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.20-4
- Package vmlinux with PROGBITS sections in -debuginfo subpackage
* Wed Sep 21 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.20-3
- Add PCIE hotplug support
- Switch processor type to generic
* Tue Sep 20 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.20-2
- Add -release number for /boot/* files
- Fixed generation of debug symbols for kernel modules & vmlinux
* Wed Sep  7 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.20-1
- Update to linux-4.4.20
- keys-fix-asn.1-indefinite-length-object-parsing.patch
* Thu Aug 25 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-11
- vmxnet3 patches to bumpup a version to 1.4.8.0
* Wed Aug 24 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-10
- .config: added NVME blk dev support
* Wed Aug 10 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-9
- Added VSOCK-Detach-QP-check-should-filter-out-non-matching-QPs.patch
* Wed Jul 20 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-8
- .config: added cgroups for pids,mem and blkio
* Mon Jul 11 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-7
- .config: added ip multible tables support
* Fri Jun 17 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-6
- patch: e1000e-prevent-div-by-zero-if-TIMINCA-is-zero.patch
- .config: disable rt group scheduling - not supported by systemd
* Fri May 27 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-5
- patch: REVERT-sched-fair-Beef-up-wake_wide.patch
* Wed May 25 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-4
- .config: added net_9p and 9p_fs
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.4.8-3
- GA - Bump release of all rpms
* Mon May 23 2016 Divya Thaluru <dthaluru@vmware.com> 4.4.8-2
- Added patches to fix CVE-2016-3134, CVE-2016-3135
* Fri May 13 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-1
- Update to linux-4.4.8
- Added net-Drivers-Vmxnet3-set-... patch
- Added e1000e module
* Tue Mar 29 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-19
- Support kmsg dumping to vmware.log on panic
- sunrpc: xs_bind uses ip_local_reserved_ports
* Thu Mar 24 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-18
- Apply photon8 config (+stack protector regular)
- pv-ops patch: added STA support
- Added patches from generic kernel
* Wed Mar 09 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.2.0-17
- Enable ACPI hotplug support in kernel config
* Sun Feb 14 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-16
- veth patch: don’t modify ip_summed
* Mon Feb 08 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-15
- Double tcp_mem limits, patch is added.
* Wed Feb 03 2016 Anish Swaminathan <anishs@vmware.com>  4.2.0-14
- Fixes for CVE-2015-7990/6937 and CVE-2015-8660.
* Fri Jan 22 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-13
- Fix for CVE-2016-0728
* Wed Jan 13 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-12
- CONFIG_HZ=250
- Disable sched autogroup.
* Tue Jan 12 2016 Mahmoud Bassiouny <mbassiouny@vmware.com> 4.2.0-11
- Remove rootfstype from the kernel parameter.
* Tue Dec 15 2015 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-10
- Skip rdrand reseed to improve boot time.
- .config changes: jolietfs(m), default THP=always, hotplug_cpu(m)
* Tue Nov 17 2015 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-9
- nordrand cmdline param is removed.
- .config: + serial 8250 driver (M).
* Fri Nov 13 2015 Mahmoud Bassiouny <mbassiouny@vmware.com> 4.2.0-8
- Change the linux image directory.
* Tue Nov 10 2015 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-7
- Get LAPIC timer frequency from HV, skip boot time calibration.
- .config: + dummy net driver (M).
* Mon Nov 09 2015 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-6
- Rename subpackage dev -> devel.
- Added the build essential files in the devel subpackage.
- .config: added genede driver module.
* Wed Oct 28 2015 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-5
- Import patches from kernel2 repo.
- Added pv-ops patch (timekeeping related improvements).
- Removed unnecessary cmdline params.
- .config changes: elevator=noop by default, paravirt clock enable,
    initrd support, openvswitch module, x2apic enable.
* Mon Sep 21 2015 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-4
- CDROM modules are added.
* Thu Sep 17 2015 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-3
- Fix for 05- patch (SVGA mem size)
- Compile out: pci hotplug, sched smt.
- Compile in kernel: vmware balloon & vmci.
- Module for efi vars.
* Fri Sep 4 2015 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-2
- Hardcoded poweroff (direct write to piix4), no ACPI is required.
- sd.c: Lower log level for "Assuming drive cache..." message.
* Tue Sep 1 2015 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-1
- Update to linux-4.2.0. Enable CONFIG_EFI
* Fri Aug 28 2015 Alexey Makhalov <amakhalov@vmware.com> 4.1.3-5
- Added MD/LVM/DM modules.
- Pci probe improvements.
* Fri Aug 14 2015 Alexey Makhalov <amakhalov@vmware.com> 4.1.3-4
- Use photon.cfg as a symlink.
* Thu Aug 13 2015 Alexey Makhalov <amakhalov@vmware.com> 4.1.3-3
- Added environment file(photon.cfg) for a grub.
* Tue Aug 11 2015 Alexey Makhalov <amakhalov@vmware.com> 4.1.3-2
- Added pci-probe-vmware.patch. Removed unused modules. Decreased boot time.
* Tue Jul 28 2015 Alexey Makhalov <amakhalov@vmware.com> 4.1.3-1
- Initial commit. Use patchset from Clear Linux.
