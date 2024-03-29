%global security_hardening none

%ifarch x86_64
%define arch x86_64
%define archdir x86

# Set this flag to 0 to build without canister
%global fips 1

# If kat_build is enabled, canister is not used.
%if 0%{?kat_build}
%global fips 0
%endif

%endif

Summary:        Kernel
Name:           linux-rt
Version:        5.10.214
Release:        2%{?kat_build:.kat}%{?dist}
License:        GPLv2
URL:            http://www.kernel.org/
Group:          System Environment/Kernel
Vendor:         VMware, Inc.
Distribution:   Photon

# Keep rt_version matched up with localversion.patch
%define rt_version rt105
%define uname_r %{version}-%{release}-rt
%define _modulesdir /lib/modules/%{uname_r}

Source0:        http://www.kernel.org/pub/linux/kernel/v5.x/linux-%{version}.tar.xz
%define sha512 linux=120b5f269b56478791d00ca3af18acd4e16b8fd01af163d9db8b8cdcecf7df4bf6c50cfed9e0ae456e6b1677e4b450b8fcfc376b746344bf1d056f024d2ce1e5
%ifarch x86_64
Source1: config-rt
%endif
Source2: initramfs.trigger
# contains pre, postun, filetriggerun tasks
Source4: scriptlets.inc
Source5: check_for_config_applicability.inc
# Real-Time kernel (PREEMPT_RT patches)
# Source: https://cdn.kernel.org/pub/linux/kernel/projects/rt/5.10/
Source6: preempt_rt.patches

%ifarch x86_64
%define i40e_version 2.22.18
Source7: https://sourceforge.net/projects/e1000/files/i40e%20stable/%{i40e_version}/i40e-%{i40e_version}.tar.gz
%define sha512 i40e=042fd064528cb807894dc1f211dcb34ff28b319aea48fc6dede928c93ef4bbbb109bdfc903c27bae98b2a41ba01b7b1dffc3acac100610e3c6e95427162a26ac

%define iavf_version 4.8.2
Source8: https://sourceforge.net/projects/e1000/files/iavf%20stable/%{iavf_version}/iavf-%{iavf_version}.tar.gz
%define sha512 iavf=5406b86e61f6528adfd7bc3a5f330cec8bb3b4d6c67395961cc6ab78ec3bd325c3a8655b8f42bf56fb47c62a85fb7dbb0c1aa3ecb6fa069b21acb682f6f578cf

%define ice_version 1.11.14
Source9: https://sourceforge.net/projects/e1000/files/ice%20stable/%{ice_version}/ice-%{ice_version}.tar.gz
%define sha512 ice=a2a6a498e553d41e4e6959a19cdb74f0ceff3a7dbcbf302818ad514fdc18e3d3b515242c88d55ef8a00c9d16925f0cd8579cb41b3b1c27ea6716ccd7e70fd847
%endif

%if 0%{?fips}
Source10: check_fips_canister_struct_compatibility.inc

%define fips_canister_version 4.0.1-5.10.21-3-secure
Source16: fips-canister-%{fips_canister_version}.tar.bz2
%define sha512 fips-canister=1d3b88088a23f7d6e21d14b1e1d29496ea9e38c750d8a01df29e1343034f74b0f3801d1f72c51a3d27e9c51113c808e6a7aa035cb66c5c9b184ef8c4ed06f42a
Source17: modify_kernel_configs.inc
Source18: fips_canister-kallsyms
Source19: FIPS-do-not-allow-not-certified-algos-in-fips-2.patch
Source20: Add-alg_request_report-cmdline.patch
Source21: 0001-LKCM-4.0.1-binary-patching-to-fix-jent-on-AMD-EPYC.patch
%endif

Source22: spec_install_post.inc
Source23: %{name}-dracut.conf

# common
Patch0: net-Double-tcp_mem-limits.patch
Patch1: SUNRPC-Do-not-reuse-srcport-for-TIME_WAIT-socket.patch
Patch2: SUNRPC-xs_bind-uses-ip_local_reserved_ports.patch
Patch3: 9p-transport-for-9p.patch
Patch4: 9p-trans_fd-extend-port-variable-to-u32.patch
Patch5: vsock-delay-detach-of-QP-with-outgoing-data-59.patch
# RDRAND-based RNG driver to enhance the kernel's entropy pool:
Patch6: hwrng-rdrand-Add-RNG-driver-based-on-x86-rdrand-inst.patch
Patch7: 0001-cgroup-v1-cgroup_stat-support.patch
Patch8: Performance-over-security-model.patch

# ttyXRUSB support
Patch10: usb-acm-exclude-exar-usb-serial-ports-nxt.patch

Patch12: fork-add-sysctl-to-disallow-unprivileged-CLONE_NEWUSER-by.patch
# Out-of-tree patches from AppArmor:
Patch13: apparmor-patch-to-provide-compatibility-with-v2.x-ne.patch
Patch14: apparmor-af_unix-mediation.patch

# Revert crypto api workqueue
Patch15: 0001-Revert-crypto-api-Use-work-queue-in-crypto_destroy_i.patch

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
Patch43: 0001-kbuild-simplify-access-to-the-kernel-s-version.patch
Patch44: 0002-kbuild-replace-if-A-A-B-with-or-A-B.patch
Patch45: 0003-kbuild-Makefile-Introduce-macros-to-distinguish-Phot.patch
Patch46: 0004-linux-rt-Makefile-Add-kernel-flavor-info-to-the-gene.patch

# VMW: [55..65]
Patch55: x86-vmware-Use-Efficient-and-Correct-ALTERNATIVEs-fo-510.patch
Patch56: x86-vmware-Log-kmsg-dump-on-panic-510.patch
Patch57: 0001-x86-vmware-avoid-TSC-recalibration.patch

#Kernel lockdown
Patch58: 0001-kernel-lockdown-when-UEFI-secure-boot-enabled.patch

# CVE:
Patch100: apparmor-fix-use-after-free-in-sk_peer_label.patch
# Fix for CVE-2019-12379
Patch101: consolemap-Fix-a-memory-leaking-bug-in-drivers-tty-v.patch

# Next 2 patches are about to be merged into stable
Patch102: 0001-mm-fix-panic-in-__alloc_pages.patch

# Fix for CVE-2021-4204
Patch103: 0002-bpf-Disallow-unprivileged-bpf-by-default.patch

# Fix for CVE-2023-52585
Patch105: 0001-drm-amdgpu-Fix-possible-NULL-dereference-in-amdgpu_r.patch

# Fix for CVE-2022-3522
Patch106: 0001-mm_hugetlb_handle_pte_markers_in_page_faults.patch
Patch107: 0002-mm_hugetlb_fix_race_condition_of_uffd_missing_minor_handling.patch
Patch108: 0003-mm_hugetlb_use_hugetlb_pte_stable_in_migration_race_check.patch

# Fix for CVE-2022-0500
Patch113: 0001-bpf-Introduce-composable-reg-ret-and-arg-types.patch
Patch114: 0002-bpf-Replace-ARG_XXX_OR_NULL-with-ARG_XXX-PTR_MAYBE_N.patch
Patch115: 0003-bpf-Replace-RET_XXX_OR_NULL-with-RET_XXX-PTR_MAYBE_N.patch
Patch116: 0004-bpf-Extract-nullable-reg-type-conversion-into-a-help.patch
Patch117: 0005-bpf-Replace-PTR_TO_XXX_OR_NULL-with-PTR_TO_XXX-PTR_M.patch
Patch118: 0006-bpf-Introduce-MEM_RDONLY-flag.patch
Patch119: 0007-bpf-Make-per_cpu_ptr-return-rdonly-PTR_TO_MEM.patch
Patch120: 0008-bpf-Add-MEM_RDONLY-for-helper-args-that-are-pointers.patch

# Fix for CVE-2022-3524 and CVE-2022-3567
Patch121: 0001-ipv6-annotate-some-data-races-around-sk-sk_prot.patch
Patch125: 0005-ipv6-Fix-data-races-around-sk-sk_prot.patch
Patch126: 0006-tcp-Fix-data-races-around-icsk-icsk_af_ops.patch

#Fix for CVE-2022-43945
Patch129: 0001-NFSD-Cap-rsize_bop-result-based-on-send-buffer-size.patch
Patch130: 0002-NFSD-Protect-against-send-buffer-overflow-in-NFSv3-R.patch
Patch131: 0003-NFSD-Protect-against-send-buffer-overflow-in-NFSv2-R.patch
Patch132: 0004-NFSD-Protect-against-send-buffer-overflow-in-NFSv3-R.patch

#Fix for CVE-2021-3699
Patch133: ipc-replace-costly-bailout-check-in-sysvipc_find_ipc.patch

#Fix for CVE-2023-0597
Patch135: 0001-x86-mm-Randomize-per-cpu-entry-area.patch
Patch136: 0002-x86-mm-Do-not-shuffle-CPU-entry-areas-without-KASLR.patch

#Fix CVE-2023-2176
Patch137: 0001-RDMA-core-Refactor-rdma_bind_addr.patch

#Fix CVE-2023-22995
Patch138: 0001-usb-dwc3-dwc3-qcom-Add-missing-platform_device_put-i.patch

# Fix CVE-2024-23307
Patch142: 0001-md-raid5-fix-atomicity-violation-in-raid5_cache_coun.patch

# Fix CVE-2024-26584
Patch144: 0001-tls-rx-simplify-async-wait.patch
Patch145: 0001-net-tls-factor-out-tls_-crypt_async_wait.patch
Patch146: 0001-net-tls-handle-backlogging-of-crypto-requests.patch

# Fix CVE-2023-52458
Patch149: 0001-block-add-check-that-partition-length-needs-to-be-al.patch

# Fix CVE-2023-52482
Patch150: 0001-x86-srso-Add-SRSO-mitigation-for-Hygon-processors.patch

# Fix CVE-2024-26583
Patch151: 0001-tls-fix-race-between-async-notify-and-socket-close.patch

# Fix CVE-2024-26585
Patch152: 0001-tls-fix-race-between-tx-work-scheduling-and-socket-c.patch

# Fix CVE-2024-26589
Patch153: 0001-bpf-Reject-variable-offset-alu-on-PTR_TO_FLOW_KEYS.patch

# Fix CVE-2024-26642
Patch154: 0001-netfilter-nf_tables-disallow-anonymous-set-with-timeout-flag.patch

# Fix CVE-2024-26642
Patch155: 0001-netfilter-nf_tables-disallow-timeout-for-anonymous-sets.patch

# Fix CVE-2024-26643
Patch156: 0001-netfilter-nf_tables-mark-set-as-dead-when-unbinding.patch

# Allow PCI resets to be disabled from vfio_pci module
Patch200: 0001-drivers-vfio-pci-Add-kernel-parameter-to-allow-disab.patch
# Add PCI quirk to allow multiple devices under the same virtual PCI bridge
# to be put into separate IOMMU groups on ESXi.
Patch201: 0001-Add-PCI-quirk-for-VMware-PCIe-Root-Port.patch

# Enable CONFIG_DEBUG_INFO_BTF=y
Patch202: 0001-tools-resolve_btfids-Warn-when-having-multiple-IDs-f.patch

# SEV, TDX
%ifarch x86_64
Patch211: 0001-x86-boot-Avoid-VE-during-boot-for-TDX-platforms.patch
%endif

# Real-Time kernel (PREEMPT_RT patches)
# Source: http://cdn.kernel.org/pub/linux/kernel/projects/rt/5.10/
%include %{SOURCE6}

#Ignore reading localversion-rt
Patch699: 0001-setlocalversion-Skip-reading-localversion-rt-file.patch

#Photon Specific Changes
Patch700: 0000-Revert-clockevents-Stop-unused-clockevent-devices.patch

# RT Runtime Greed
Patch701: 0001-RT-PATCH-sched-rt-RT_RUNTIME_GREED-sched-feature.patch
Patch702: use-kmsg_dump-iterator-for-RT.patch

# Patchset to conditional restart_tick upon idle_exit
# https://lore.kernel.org/lkml/162091184942.29796.4815200413212139734.tip-bot2@tip-bot2/
Patch703: 0001-tick-nohz-Evaluate-the-CPU-expression-after-the-stat.patch
Patch704: 0002-tick-nohz-Conditionally-restart-tick-on-idle-exit.patch
Patch705: 0003-tick-nohz-Remove-superflous-check-for-CONFIG_VIRT_CP.patch
Patch706: 0004-tick-nohz-Update-idle_exittime-on-actual-idle-exit.patch
Patch707: 0005-tick-nohz-Update-nohz_full-Kconfig-help.patch
Patch708: 0006-tick-nohz-Only-wakeup-a-single-target-cpu-when-kicki.patch
Patch709: 0007-tick-nohz-Change-signal-tick-dependency-to-wakeup-CP.patch
Patch710: 0008-tick-nohz-Kick-only-_queued_-task-whose-tick-depende.patch
Patch711: 0009-tick-nohz-Call-tick_nohz_task_switch-with-interrupts.patch
Patch712: 0010-MAINTAINERS-Add-myself-as-context-tracking-maintaine.patch

#Patch to enable nohz with idle=poll
Patch713: 0001-Allow-tick-sched-timer-to-be-turned-off-in-idle-poll.patch

# Disable md5 algorithm for sctp if fips is enabled.
Patch714: 0001-disable-md5-algorithm-for-sctp-if-fips-is-enabled.patch

#Backport hrtick changes
Patch715: 0001-sched-features-Distinguish-between-NORMAL-and-DEADLI.patch

#Patch to add timer padding on guest
Patch716: Guest-timer-Advancement-Feature.patch

# Provide mixed cpusets guarantees for processes placement
Patch717: 0001-Enable-and-enhance-SCHED-isolation.patch

# Crypto:
# Patch to add drbg_pr_ctr_aes256 test vectors to testmgr
Patch1000: crypto-testmgr-Add-drbg_pr_ctr_aes256-test-vectors.patch
# Patch to call drbg and dh crypto tests from tcrypt
Patch1001: tcrypt-disable-tests-that-are-not-enabled-in-photon.patch
Patch1002: 0001-Initialize-jitterentropy-before-ecdh.patch
Patch1003: 0002-FIPS-crypto-self-tests.patch
# Patch to remove urandom usage in rng module
Patch1004: 0001-FIPS-crypto-rng-Jitterentropy-RNG-as-the-only-RND-source.patch
# Patch to remove urandom usage in drbg and ecc modules
Patch1005: 0003-FIPS-crypto-drbg-Jitterentropy-RNG-as-the-only-RND.patch
#Patch to not make shash_no_setkey static
Patch1006: 0001-fips-Continue-to-export-shash_no_setkey.patch
#Patch to introduce wrappers for random callback functions
Patch1007: 0001-linux-crypto-Add-random-ready-callbacks-support.patch

%if 0%{?fips}
# FIPS canister usage patch
Patch1008: 0001-FIPS-canister-binary-usage.patch
Patch1009: 0001-scripts-kallsyms-Extra-kallsyms-parsing.patch
%else
%if 0%{?kat_build}
Patch1010: 0003-FIPS-broken-kattest.patch
%endif
%endif

%if 0%{?fips}
#retpoline
Patch1011: 0001-retpoline-re-introduce-alternative-for-r11.patch
%endif

#Patches for i40e driver
Patch1500: i40e-xdp-remove-XDP_QUERY_PROG-and-XDP_QUERY_PROG_HW-XDP-.patch
Patch1501: 0001-Add-support-for-gettimex64-interface.patch
Patch1502: i40e-don-t-install-auxiliary-module-on.patch
Patch1503: i40e-Make-i40e-driver-honor-default-and-user-defined.patch

#Patches for iavf driver
Patch1512: no-aux-symvers.patch

#Patches for ice driver
Patch1513: ice-don-t-install-auxiliary-module-on-modul.patch
Patch1514: ice-fix-redefinition-of-eth_hw_addr_set.patch

#Patches for vmci driver
Patch1521: 001-return-correct-error-code.patch
Patch1522: 002-switch-to-kvfree_rcu-API.patch
Patch1523: 003-print-unexpanded-names-of-ioctl.patch
Patch1524: 004-enforce-queuepair-max-size-for-IOCTL_VMCI_QUEUEPAIR_ALLOC.patch
Patch1531: 0001-whitespace-formatting-change-for-vmci-register-defines.patch
Patch1532: 0002-add-MMIO-access-to-registers.patch
Patch1533: 0003-detect-DMA-datagram-capability.patch
Patch1534: 0004-set-OS-page-size.patch
Patch1535: 0005-register-dummy-IRQ-handlers-for-DMA-datagrams.patch
Patch1536: 0006-allocate-send-receive-buffers-for-DMAdatagrams.patch
Patch1537: 0007-add-support-for-DMA-datagrams-send.patch
Patch1538: 0008-add-support-for-DMA-datagrams-receive.patch
Patch1539: 0009-fix-the-description-of-vmci_check_host_caps.patch
Patch1540: 0010-no-need-to-clear-memory-after-dma_alloc_coherent.patch
Patch1541: 0011-fix-error-handling-paths-in-vmci_guest_probe_device.patch
Patch1542: 0012-check-exclusive-vectors-when-freeing-interrupt1.patch
Patch1543: 0013-release-notification-bitmap-inn-error-path.patch
Patch1544: 0014-add-support-for-arm64.patch

BuildArch: x86_64

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
BuildRequires: audit-devel
BuildRequires: python3-macros
BuildRequires: elfutils-libelf-devel
BuildRequires: bison
BuildRequires: dwarves-devel
# i40e build scripts require getopt
BuildRequires: util-linux

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
The Linux package contains the Linux kernel with RT (real-time)
features.
Built with rt patchset version %{rt_version}.
%if 0%{?fips}
This kernel is FIPS certified.
%endif

%package devel
Summary:        Kernel Dev
Group:          System Environment/Kernel
Requires:       %{name} = %{version}-%{release}
Requires:       python3
Requires:       gawk
%description devel
The Linux package contains the Linux kernel dev files

%package docs
Summary:        Kernel docs
Group:          System Environment/Kernel
Requires:       python3
%description docs
The Linux package contains the Linux kernel doc files

%prep
# Using autosetup is not feasible
%setup -q -n linux-%{version}
%ifarch x86_64
# Using autosetup is not feasible
%setup -q -T -D -b 7 -n linux-%{version}
# Using autosetup is not feasible
%setup -q -T -D -b 8 -n linux-%{version}
# Using autosetup is not feasible
%setup -q -T -D -b 9 -n linux-%{version}
%endif
%if 0%{?fips}
# Using autosetup is not feasible
%setup -q -T -D -b 16 -n linux-%{version}
%endif

%autopatch -p1 -m0 -M48

#VMW
%autopatch -p1 -m55 -M65

# CVE
%autopatch -p1 -m100 -M156

# Allow PCI resets to be disabled from vfio_pci module
%autopatch -p1 -m200 -M201

%autopatch -p1 -m202 -M202

# SEV, TDX
%ifarch x86_64
%autopatch -p1 -m211 -M211
%endif

# RT
%autopatch -p1 -m301 -M717

%autopatch -p1 -m1000 -M1007

%if 0%{?fips}
%autopatch -p1 -m1008 -M1009
%else
%if 0%{?kat_build}
%patch1010 -p1
%endif
%endif

%if 0%{?fips}
%autopatch -p1 -m1011 -M1011
%endif

#Patches for i40e driver
pushd ../i40e-%{i40e_version}
%autopatch -p1 -m1500 -M1503
popd

#Patches for iavf driver
pushd ../iavf-%{iavf_version}
%patch1512 -p1
popd

#Patches for ice driver
pushd ../ice-%{ice_version}
%patch1513 -p1
%patch1514 -p1
popd

# vmci
%patch1521 -p1
%patch1522 -p1
%patch1523 -p1
%patch1524 -p1
%patch1531 -p1
%patch1532 -p1
%patch1533 -p1
%patch1534 -p1
%patch1535 -p1
%patch1536 -p1
%patch1537 -p1
%patch1538 -p1
%patch1539 -p1
%patch1540 -p1
%patch1541 -p1
%patch1542 -p1
%patch1543 -p1
%patch1544 -p1

make %{?_smp_mflags} mrproper

%ifarch x86_64
cp %{SOURCE1} .config
%endif
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
%else
%if 0%{?kat_build}
# Change m to y for modules in katbuild
%include %{SOURCE17}
%endif
%endif

sed -i 's/CONFIG_LOCALVERSION="-rt"/CONFIG_LOCALVERSION="-%{release}-rt"/' .config

%if 0%{?kat_build}
sed -i '/CONFIG_CRYPTO_SELF_TEST=y/a CONFIG_CRYPTO_BROKEN_KAT=y' .config
%endif

%include %{SOURCE5}

%build
make %{?_smp_mflags} V=1 KBUILD_BUILD_VERSION="1-photon" \
    KBUILD_BUILD_HOST="photon" ARCH=%{?arch} %{?_smp_mflags}

%if 0%{?fips}
%include %{SOURCE10}
%endif

%ifarch x86_64

# build i40e module
bldroot="${PWD}"
pushd ../i40e-%{i40e_version}
make %{?_smp_mflags} -C src KSRC=${bldroot} clean
make -C src KSRC=${bldroot} %{?_smp_mflags}
popd

# build iavf module
pushd ../iavf-%{iavf_version}
make %{?_smp_mflags} -C src KSRC=${bldroot} clean
make -C src KSRC=${bldroot} %{?_smp_mflags}
popd

# build ice module
pushd ../ice-%{ice_version}
make %{?_smp_mflags} -C src KSRC=${bldroot} clean
make -C src KSRC=${bldroot} %{?_smp_mflags}
popd
%endif

%install
install -vdm 755 %{buildroot}%{_sysconfdir}
install -vdm 755 %{buildroot}/boot
install -vdm 755 %{buildroot}%{_docdir}/linux-%{uname_r}
install -vdm 755 %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}
install -vdm 755 %{buildroot}%{_libdir}/debug/%{_modulesdir}
make %{?_smp_mflags} INSTALL_MOD_PATH=%{buildroot} modules_install

%ifarch x86_64

# The auxiliary.ko kernel module is a common dependency for i40e, iavf
# and ice drivers. Install it only once, along with the iavf driver
# and re-use it in the ice and i40e drivers.

# install i40e module
bldroot="${PWD}"
pushd ../i40e-%{i40e_version}
make %{?_smp_mflags} -C src KSRC=${bldroot} INSTALL_MOD_PATH=%{buildroot} \
    INSTALL_MOD_DIR=extra MANDIR=%{_mandir} modules_install_no_aux mandocs_install
popd

# install iavf module
pushd ../iavf-%{iavf_version}
make -C src KSRC=$bldroot INSTALL_MOD_PATH=%{buildroot} INSTALL_MOD_DIR=extra \
    INSTALL_AUX_DIR=extra/auxiliary MANDIR=%{_mandir} modules_install \
    mandocs_install %{?_smp_mflags}
install -Dvm 644 src/linux/auxiliary_bus.h \
    %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}/include/linux/auxiliary_bus.h
popd

# install ice module
pushd ../ice-%{ice_version}
make -C src KSRC=${bldroot} MANDIR=%{_mandir} INSTALL_MOD_PATH=%{buildroot} \
            mandocs_install %{?_smp_mflags}
make %{?_smp_mflags} -C src KSRC=${bldroot} INSTALL_MOD_PATH=%{buildroot} \
    INSTALL_MOD_DIR=extra modules_install_no_aux
popd

# Verify for build-id match
# We observe different IDs sometimes
# TODO: debug it
ID1=$(readelf -n vmlinux | grep "Build ID")
./scripts/extract-vmlinux arch/x86/boot/bzImage > extracted-vmlinux
ID2=$(readelf -n extracted-vmlinux | grep "Build ID")
if [ "$ID1" != "$ID2" ] ; then
  echo "Build IDs do not match"
  echo $ID1
  echo $ID2
  exit 1
fi
install -vm 644 arch/x86/boot/bzImage %{buildroot}/boot/vmlinuz-%{uname_r}
%endif

# Restrict the permission on System.map-X file
install -vm 400 System.map %{buildroot}/boot/System.map-%{uname_r}
install -vm 644 .config %{buildroot}/boot/config-%{uname_r}
cp -r Documentation/* %{buildroot}%{_docdir}/linux-%{uname_r}

%if 0%{?__debug_package}
install -vm 644 vmlinux %{buildroot}%{_libdir}/debug/%{_modulesdir}/vmlinux-%{uname_r}
# `perf test vmlinux` needs it
ln -s vmlinux-%{uname_r} %{buildroot}%{_libdir}/debug/%{_modulesdir}/vmlinux
%endif

cat > %{buildroot}/boot/linux-%{uname_r}.cfg << "EOF"
# GRUB Environment Block
photon_cmdline=init=/lib/systemd/systemd ro loglevel=3 quiet nosoftlockup intel_idle.max_cstate=0 mce=ignore_ce nowatchdog cpuidle.off=1 nmi_watchdog=0 audit=0
photon_linux=vmlinuz-%{uname_r}
photon_initrd=initrd.img-%{uname_r}
EOF

# Cleanup dangling symlinks
rm -rf %{buildroot}%{_modulesdir}/source \
       %{buildroot}%{_modulesdir}/build

find . -name Makefile* -o -name Kconfig* -o -name *.pl | xargs sh -c 'cp --parents "$@" %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}' copy
find arch/%{archdir}/include include scripts -type f | xargs sh -c 'cp --parents "$@" %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}' copy
find $(find arch/%{archdir} -name include -o -name scripts -type d) -type f | xargs sh -c 'cp --parents "$@" %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}' copy
find arch/%{archdir}/include Module.symvers include scripts -type f | xargs sh -c 'cp --parents "$@" %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}' copy
%ifarch x86_64
# CONFIG_STACK_VALIDATION=y requires objtool to build external modules
install -vsm 755 tools/objtool/objtool %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}/tools/objtool/
install -vsm 755 tools/objtool/fixdep %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}/tools/objtool/
%endif

cp .config %{buildroot}%{_usrsrc}/linux-headers-%{uname_r} # copy .config manually to be where it's expected to be
ln -sf "%{_usrsrc}/linux-headers-%{uname_r}" "%{buildroot}%{_modulesdir}/build"
find %{buildroot}/lib/modules -name '*.ko' -print0 | xargs -0 chmod u+x

mkdir -p %{buildroot}%{_modulesdir}/dracut.conf.d/
cp -p %{SOURCE23} %{buildroot}%{_modulesdir}/dracut.conf.d/%{name}.conf

%include %{SOURCE2}
%include %{SOURCE4}
%include %{SOURCE22}

%post
/sbin/depmod -a %{uname_r}
ln -sf linux-%{uname_r}.cfg /boot/photon.cfg

%files
%defattr(-,root,root)
/boot/System.map-%{uname_r}
/boot/config-%{uname_r}
/boot/vmlinuz-%{uname_r}
%config(noreplace) /boot/linux-%{uname_r}.cfg
%defattr(0644,root,root)
%{_modulesdir}/*
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
- Fix for CVE-2023-52447/2023-52458/2023-52482
* Mon Mar 11 2024 Srish Srinivasan <srish.srinivasan@broadcom.com> 5.10.212-1
- Update to version 5.10.212, rt103, patched CVE-2024-26584
* Mon Mar 11 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com>  5.10.210-3
- Fixes CVE-2024-23307 and CVE-2024-22099
* Wed Feb 28 2024 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 5.10.210-2
- Fix CVE-2024-0841
* Mon Feb 26 2024 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 5.10.210-1
- Update to version 5.10.210
* Mon Feb 05 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 5.10.209-3
- Patch from the same series that resolved CVE-2024-0565
* Mon Feb 05 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 5.10.209-2
- Fix CVE-2024-1086
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
- Update to version 5.10.206 and rt version to 5.10.204-rt100
* Mon Nov 27 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 5.10.201-1
- Update to version 5.10.201
* Wed Nov 15 2023 Kuntal Nayak <nkuntal@vmware.com> 5.10.200-2
- Kconfig to lockdown kernel in UEFI Secure Boot
* Thu Nov 09 2023 Ankit Jain <ankitja@vmware.com> 5.10.200-1
- Update to version 5.10.200
* Fri Oct 13 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 5.10.198-1
- Update to version 5.10.198
- Fix CVE-2023-4244
* Thu Oct 12 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 5.10.197-3
- Move kernel prep to %prep
* Mon Oct 09 2023 Him Kalyan Bordoloi <bordoloih@vmware.com> 5.10.197-2
- Fix issues in Guest timer Advancement feature
* Tue Oct 03 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 5.10.197-1
- Update to version 5.10.197
- Undo commit 625bf86bf53eb7a8ee60fb9dc45b272b77e5ce1c as it breaks canister usage.
* Mon Oct 02 2023 Alexey Makhalov <amakhalov@vmware.com> 5.10.194-6
- LKCM: jitterentropy fix.
- Enable and enhance sched isolation.
* Sun Oct 01 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 5.10.194-5
- Fix for CVE-2023-42754
* Mon Sep 25 2023 Keerthana K <keerthanak@vmware.com> 5.10.194-4
- Fix CVE-2023-42756
* Mon Sep 25 2023 Keerthana K <keerthanak@vmware.com> 5.10.194-3
- Fix CVE-2023-42755
* Wed Sep 20 2023 Keerthana K <keerthanak@vmware.com> 5.10.194-2
- Fix CVE-2023-42753
* Mon Sep 11 2023 Roye Eshed <eshedr@vmware.com> 5.10.194-1
- Update to version 5.10.194
* Tue Sep 05 2023 Ankit Jain <ankitja@vmware.com> 5.10.190-4
- Fixes CVE-2023-22995
* Tue Sep 05 2023 Ankit Jain <ankitja@vmware.com> 5.10.190-3
- Fixes CVE-2023-2176
* Wed Aug 30 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 5.10.190-2
- Disable CONFIG_SCSI_DPT_I2O to fix CVE-2023-2007
* Tue Aug 29 2023 Ajay Kaher <akaher@vmware.com> 5.10.190-1
- Update to version 5.10.190
* Fri Aug 25 2023 Srish Srinivasan <ssrish@vmware.com> 5.10.188-2
- Patched CVE-2023-4147, CVE-2023-4128
* Tue Aug 01 2023 Kuntal Nayak <nkuntal@vmware.com> 5.10.188-1
- Update to version 5.10.188
* Fri Jul 28 2023 Ajay Kaher <akaher@vmware.com> 5.10.186-2
- Fix: SEV: Guest should not disabled CR4.MCE
* Fri Jul 14 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 5.10.186-1
- Update to version 5.10.186
* Mon Jul 10 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 5.10.183-2
- Fix for CVE-2023-0597
* Thu Jun 08 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 5.10.183-1
- Update to version 5.10.183, fix some CVEs
* Wed May 17 2023 Ankit Jain <ankitja@vmware.com> 5.10.180-1
- Update to version 5.10.180
* Mon May 08 2023 Srish Srinivasan <ssrish@vmware.com> 5.10.175-5
- Enable CONFIG_DEBUG_INFO_BTF=y
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
- Update intel ethernet drivers
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
* Fri Feb 03 2023 Alexey Makhalov <amakhalov@vmware.com> 5.10.162-2
- Implement performance over security option for RETBleed (pos=1)
* Tue Jan 17 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 5.10.162-1
- Update to version 5.10.162
* Thu Jan 12 2023 Alexey Makhalov <amakhalov@vmware.com> 5.10.159-4
- Introduce fips=2 and alg_request_report cmdline parameters
* Thu Jan 05 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 5.10.159-3
- update to latest ToT vmxnet3 driver
- Include patch "vmxnet3: correctly report csum_level for encapsulated packet"
* Thu Dec 22 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 5.10.159-2
- Enable CONFIG_PCI_PF_STUB
* Mon Dec 19 2022 srinidhira0 <srinidhir@vmware.com> 5.10.159-1
- Update to version 5.10.159
* Wed Dec 14 2022 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 5.10.158-2
- update to latest ToT vmxnet3 driver
* Mon Dec 12 2022 Ankit Jain <ankitja@vmware.com> 5.10.158-1
- Update to version 5.10.158
* Tue Dec 06 2022 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 5.10.152-9
- Fix for CVE-2022-43945
* Mon Dec 05 2022 Srish Srinivasan <ssrish@vmware.com> 5.10.152-8
- Enable CONFIG_NET_CLS_FLOWER=m
* Wed Nov 30 2022 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 5.10.152-7
- Fix for CVE-2022-3564
* Mon Nov 28 2022 Ankit Jain <ankitja@vmware.com> 5.10.152-6
- Fix for CVE-2022-4139
* Mon Nov 28 2022 Ajay Kaher <akaher@vmware.com> 5.10.152-5
- Fix for CVE-2022-3522
* Mon Nov 14 2022 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 5.10.152-4
- vmxnet3 version 6, 7 patches
* Wed Nov 09 2022 Ajay Kaher <akaher@vmware.com> 5.10.152-3
- Fix for CVE-2022-3623
* Fri Nov 04 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.152-2
- Fix CVE-2022-3524 and CVE-2022-3567
* Mon Oct 31 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.152-1
- Update to version 5.10.152
* Mon Oct 17 2022 Sharan Turlapati <sturlapati@vmware.com> 5.10.142-3
- Fix for CVE-2022-2602
* Thu Oct 13 2022 Sharan Turlapati <sturlapati@vmware.com> 5.10.142-2
- Fixes for CVEs in the wifi subsystem
* Fri Sep 09 2022 srinidhira0 <srinidhir@vmware.com> 5.10.142-1
- Update to version 5.10.142
* Tue Aug 23 2022 Shivani Agarwal <shivania2@vmware.com> 5.10.132-2
- .config: Enable MPLS and other routing related options, namely,
- CGROUP_BPF, XFRM_INTERFACE, NFT_XFRM, NETFILTER_XT_TARGET_NOTRACK
- NET_ACT_BPF, MPLS_ROUTING, MPLS_IPTUNNEL, LWTUNNEL, LWTUNNEL_BPF, PPP
* Tue Aug 16 2022 srinidhira0 <srinidhir@vmware.com> 5.10.132-1
- Update to version 5.10.132
* Fri Aug 12 2022 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 5.10.118-19
- Backport fixes for CVE-2022-0500
* Wed Aug 10 2022 Shreenidhi Shedi <sshedi@vmware.com> 5.10.118-18
- Scriptlets fixes and improvements
* Wed Aug 10 2022 Sharan Turlapati <sturlapati@vmware.com> 5.10.118-17
- Correct SPEC file to autopatch vfio_pci patches
* Fri Aug 05 2022 Him Kalyan Bordoloi <bordoloih@vmware.com> 5.10.118-16
- Fix for CVE-2022-2585, CVE-2022-2586 and CVE-2022-2588
* Thu Jul 28 2022 Keerthana K <keerthanak@vmware.com> 5.10.118-15
- Fix linux headers, doc folder and linux-<uname -r>.cfg names
- Drop rt_version from uname_r
- Patch to skip reading localversion-rt
* Mon Jul 18 2022 Keerthana K <keerthanak@vmware.com> 5.10.118-14
- Update iavf driver to v4.4.2
- Update ice driver to v1.8.3
* Mon Jul 18 2022 Keerthana K <keerthanak@vmware.com> 5.10.118-13
- .config: enable CROSS_MEMORY_ATTACH
- Add elfutils-libelf-devel required to build objtool
* Mon Jul 18 2022 Keerthana K <keerthanak@vmware.com> 5.10.118-12
- Patch for timer padding on guest
* Fri Jul 15 2022 Keerthana K <keerthanak@vmware.com> 5.10.118-11
- Backport hrtick changes to fix lost timer wakeups
* Fri Jul 15 2022 Keerthana K <keerthanak@vmware.com> 5.10.118-10
- .config: enable CONFIG_NET_ACT_SIMP
* Fri Jul 15 2022 Keerthana K <keerthanak@vmware.com> 5.10.118-9
- Enable cgroup v1 stats
- .config: enable PERCPU_STATS
* Fri Jul 15 2022 Keerthana K <keerthanak@vmware.com> 5.10.118-8
- Avoid TSC recalibration
* Fri Jul 15 2022 Keerthana K <keerthanak@vmware.com> 5.10.118-7
- Enable config options needed to build N3000 FPGA driver.
* Wed Jul 13 2022 Srinidhi Rao <srinidhir@vmware.com> 5.10.118-6
- Fix for CVE-2022-21505
* Tue Jul 12 2022 Keerthana K <keerthanak@vmware.com> 5.10.118-5
- Reduce FIPS canister memory footprint by disabling CONFIG_KALLSYMS_ALL
- Add only fips_canister-kallsyms to vmlinux instead of all symbols
* Fri Jul 01 2022 Harinadh D <hdommaraju@vmware.com> 5.10.118-4
- VMCI patches & configs
* Fri Jun 24 2022 Shreenidhi Shedi <sshedi@vmware.com> 5.10.118-3
- Fix debug_package macro usage while adding vmlinux to debuginfo rpm
* Wed Jun 15 2022 Brennan Lamoreaux <blamoreaux@vmware.com> 5.10.118-2
- Enable config_livepatch
* Mon Jun 13 2022 Sharan Turlapati <sturlapati@vmware.com> 5.10.118-1
- Update to version 5.10.118
* Wed Jun 01 2022 Ajay Kaher <akaher@vmware.com> 5.10.109-4
- Fix for CVE-2022-1966, CVE-2022-1972
* Mon May 23 2022 Sharan Turlapati <sturlapati@vmware.com> 5.10.109-3
- Fix for CVE-2022-21499
* Thu May 12 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 5.10.109-2
- Fix for CVE-2022-29582
* Fri Apr 29 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 5.10.109-1
- Update to version 5.10.109
* Tue Apr 05 2022 Alexey Makhalov <amakhalov@vmware.com> 5.10.103-4
- .config: enable zstd compression for squashfs.
- .config: enable crypto user api rng.
- .config: enable CONFIG_EXT2_FS_XATTR
* Mon Mar 21 2022 Ajay Kaher <akaher@vmware.com> 5.10.103-3
- Fix for CVE-2022-1016
* Mon Mar 14 2022 Bo Gan <ganb@vmware.com> 5.10.103-2
- Fix SEV and Hypercall alternative inst. patches
* Tue Mar 08 2022 srinidhira0 <srinidhir@vmware.com> 5.10.103-1
- Update to version 5.10.103
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
* Sat Jan 08 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.83-7
- Fix CVE-2021-4155 and CVE-2021-4204
* Mon Dec 20 2021 Keerthana K <keerthanak@vmware.com> 5.10.83-6
- crypto_self_test and broken kattest module enhancements
* Fri Dec 17 2021 Alexey Makhalov <amakhalov@vmware.com> 5.10.83-5
- mm: fix percpu alloacion for memoryless nodes
- pvscsi: fix disk detection issue
* Fri Dec 17 2021 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 5.10.83-4
- Disable md5 algorithm for sctp if fips is enabled.
* Tue Dec 14 2021 Harinadh D <hdommaraju@vmware.com> 5.10.83-3
- remove lvm in add-drivers list
- lvm drivers are built as part of dm-mod
* Thu Dec 09 2021 Prashant S Chauhan <psinghchauha@vmware.com> 5.10.83-2
- Bump up to compile with python 3.10
* Mon Dec 06 2021 srinidhira0 <srinidhir@vmware.com> 5.10.83-1
- Update to version 5.10.83
* Mon Nov 29 2021 Srinidhi Rao <srinidhir@vmware.com> 5.10.78-7
- Enable eBPF Net Packet filter support.
* Thu Nov 18 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 5.10.78-6
- Add vhost and vhost-net drivers in config
* Thu Nov 18 2021 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.78-5
- Add PCI quirk to allow multiple devices under the same virtual
- PCI bridge to be put into separate IOMMU groups.
* Wed Nov 17 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 5.10.78-4
- Enable nohz for idle=poll
* Wed Nov 17 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.78-3
- Allow PCI resets disablement from vfio_pci
* Thu Nov 11 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 5.10.78-2
- compile with openssl 3.0.0
* Mon Nov 08 2021 Vikash Bansal <bvikas@vmware.com> 5.10.78-1
- Update to version 5.10.78
* Tue Oct 26 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.75-1
- Update to version 5.10.75
* Thu Sep 09 2021 Alexey Makhalov <amakhalov@vmware.com> 5.10.61-2
- .config enable CONFIG_MOUSE_PS2_VMMOUSE and CONFIG_INPUT_UINPUT
- Enable sta by default
* Fri Aug 27 2021 Ankit Jain <ankitja@vmware.com> 5.10.61-1
- Update to version 5.10.61
* Wed Aug 18 2021 Keerthana K <keerthanak@vmware.com> 5.10.52-2
- Update ice driver to v1.6.4
- Update i40e driver to v2.15.9
- Update iavf driver to v4.2.7
* Fri Jul 23 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 5.10.52-1
- Update to version 5.10.52
* Thu Jul 15 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 5.10.46-2
- Fix for CVE-2021-33909
* Mon Jun 28 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.46-1
- Update to version 5.10.46
* Thu Jun 24 2021 Ankit Jain <ankitja@vmware.com> 5.10.42-4
- Conditional tick_restart upon idle_exit
* Tue Jun 22 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.42-3
- Fix for CVE-2021-3609
* Thu Jun 10 2021 Keerthana K <keerthanak@vmware.com> 5.10.42-2
- Added script to check structure compatibility between fips_canister.o and vmlinux.
* Thu Jun 03 2021 Keerthana K <keerthanak@vmware.com> 5.10.42-1
- Update to version 5.10.42
- Remove XR usb driver support
- .config: Enable CONFIG_FANOTIFY_ACCESS_PERMISSIONS
* Wed Jun 02 2021 Keerthana K <keerthanak@vmware.com> 5.10.35-3
- Fix for CVE-2021-3573
* Thu May 20 2021 Ajay Kaher <akaher@vmware.com> 5.10.35-2
- Fix for CVE-2021-3564
* Mon May 17 2021 Ajay Kaher <akaher@vmware.com> 5.10.35-1
- Update to version 5.10.35
* Thu May 13 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.25-10
- Fix for CVE-2021-23133
* Tue May 11 2021 Ankit Jain <ankitja@vmware.com> 5.10.25-9
- .config: Enable INFINIBAND, MLX5_INFINIBAND
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
* Mon Apr 19 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.25-3
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
* Wed Mar 17 2021 Srinidhi Rao <srinidhir@vmware.com> 5.10.21-2
- Use jitterentropy rng instead of urandom in rng module.
* Tue Mar 16 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 5.10.21-1
- Update to version 5.10.21
* Mon Mar 01 2021 Alexey Makhalov <amakhalov@vmware.com> 5.10.4-10
- FIPS canister update
* Thu Feb 18 2021 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.4-9
- Fix /boot/photon.cfg symlink when /boot is a separate partition.
* Thu Feb 18 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.4-8
- Enable CONFIG_IFB
* Wed Feb 17 2021 Ankit Jain <ankitja@vmware.com> 5.10.4-7
- Added latest out of tree version of Intel ice driver
* Wed Feb 17 2021 Vikash Bansal <bvikas@vmware.com> 5.10.4-6
- Added support for RT RUNTIME GREED
* Mon Feb 15 2021 Keerthana K <keerthanak@vmware.com> 5.10.4-5
- Added crypto_self_test and kattest module.
- These patches are applied when kat_build is enabled.
* Wed Feb 03 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 5.10.4-4
- Update i40e driver to v2.13.10
- Add out of tree iavf driver
- Enable CONFIG_NET_TEAM
* Wed Jan 27 2021 Alexey Makhalov <amakhalov@vmware.com> 5.10.4-3
- Build kernel with FIPS canister.
* Mon Jan 25 2021 Ankit Jain <ankitja@vmware.com> 5.10.4-2
- Enabled CONFIG_WIREGUARD
* Mon Jan 11 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 5.10.4-1
- Update to version 5.10.4
* Tue Nov 10 2020 Keerthana K <keerthanak@vmware.com> 5.9.0-4
- Fix CVE-2020-8694
* Fri Nov 06 2020 Keerthana K <keerthanak@vmware.com> 5.9.0-3
- Fix CVE-2020-25704
* Tue Oct 27 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.9.0-2
- Revert d254087 (clockevents: Stop unused clockevent devices)
- Solve cyclictest regression introduced in 4.1
* Tue Oct 27 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.9.0-1
- Update to version 5.9.0
* Tue Oct 06 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.9.0-rc7.1
- Update to version 5.9.0-rc7
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 4.19.127-2
- openssl 1.1.1
* Tue Jun 23 2020 Keerthana K <keerthanak@vmware.com> 4.19.127-1
- Update to version 4.19.127
* Tue Jun 16 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.115-10
- Add latest out of tree version of i40e driver
* Wed Jun 10 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.115-9
- Enable CONFIG_VFIO_NOIOMMU
* Fri Jun 05 2020 Ankit Jain <ankitja@vmware.com> 4.19.115-8
- Enabled CONFIG_BINFMT_MISC
* Tue Jun 02 2020 Vikash Bansal <bvikas@vmware.com> 4.19.115-7
- Add patch to fix CVE-2019-18885
* Fri May 29 2020 Shreenidhi Shedi <sshedi@vmware.com> 4.19.115-6
- Keep modules of running kernel till next boot
* Fri May 22 2020 Tapas Kundu <tkundu@vmware.com> 4.19.115-5
- Deprecate linux-rt-tools in favor of linux-tools.
- Deprecate python3-perf in favor of linux-python3-perf.
* Thu May 21 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.115-4
- Add ICE network driver support in config
* Fri May 15 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.115-3
- Add uio_pic_generic driver support in config
* Wed May 06 2020 Siddharth Chandrasekaran <csiddharth@vmware.com> 4.19.115-2
- Add patch to fix CVE-2020-10711
* Wed May 06 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.115-1
- Upgrade to 4.19.115
* Wed Apr 29 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.98-5
- Enable additional config options.
* Mon Mar 23 2020 Alexey Makhalov <amakhalov@vmware.com> 4.19.98-4
- Fix perf compilation issue with binutils >= 2.34.
* Sun Mar 22 2020 Tapas Kundu <tkundu@vmware.com> 4.19.98-3
- Added python3-perf subpackage
* Tue Mar 17 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.98-2
- Add tools subpackage to include perf, turbostat and cpupower.
- Update the last few perf python scripts in Linux kernel to use
- python3 syntax.
* Tue Jan 28 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.98-1
- Upgrade to 4.19.98
* Thu Jan 16 2020 Srinidhi Rao <srinidhir@vmware.com> 4.19.82-4
- Enable DRBG HASH and DRBG CTR support.
* Fri Jan 03 2020 Keerthana K <keerthanak@vmware.com> 4.19.82-3
- Remove FIPS patch that enables fips for algorithms which are not fips allowed.
* Thu Dec 12 2019 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.82-2
- Fix patch that wont apply on 4.19.82. Revert when upgraded to 4.19.87 or more
* Tue Nov 12 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.82-1
- Introduce a new kernel flavor 'linux-rt' supporting real-time (RT) features.
