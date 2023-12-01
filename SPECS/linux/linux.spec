%global security_hardening none
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

Summary:        Kernel
Name:           linux
Version:        5.10.198
Release:        9%{?acvp_build:.acvp}%{?kat_build:.kat}%{?dist}
License:        GPLv2
URL:            http://www.kernel.org/
Group:          System Environment/Kernel
Vendor:         VMware, Inc.
Distribution:   Photon

%define uname_r %{version}-%{release}
%define _modulesdir /lib/modules/%{uname_r}

Source0:        http://www.kernel.org/pub/linux/kernel/v5.x/linux-%{version}.tar.xz
%define sha512 linux=3ccfbaff9b45d3239024e6c29e3a33af05460997971d767293e45f22c4db66f99595285d5dac1071f19926f35cdd90d323bd6e57809b57954f4988152ebe6342
Source1:        config_%{_arch}
Source2:        initramfs.trigger

%ifarch x86_64
%define ena_version 2.4.0
Source3:    https://github.com/amzn/amzn-drivers/archive/ena_linux_%{ena_version}.tar.gz
%define sha512 ena_linux=e14b706d06444dcc832d73150a08bbdc0fc53b291d2fd233aef62d8f989f529b4aabc7865526fe27a895d43d5f8ba5993752a920601be8a1d3ed9ea973e9c6ef

%define sgx_version 1.8
Source5:    https://github.com/intel/SGXDataCenterAttestationPrimitives/archive/DCAP_%{sgx_version}.tar.gz
%define sha512 DCAP=79d0b4aba102559bed9baf9fe20917e9781a22d742fa52b49b2c1a00c452a452796e6ce1a92bad80d6e6fc92ad71fa72ee02c1b65a59bddbb562aaaad4b2d8b2
%endif

# contains pre, postun, filetriggerun tasks
Source6:        scriptlets.inc
Source7:        check_for_config_applicability.inc

%ifarch x86_64
%define i40e_version 2.22.18
Source10:       https://sourceforge.net/projects/e1000/files/i40e%20stable/%{i40e_version}/i40e-%{i40e_version}.tar.gz
%define sha512 i40e=042fd064528cb807894dc1f211dcb34ff28b319aea48fc6dede928c93ef4bbbb109bdfc903c27bae98b2a41ba01b7b1dffc3acac100610e3c6e95427162a26ac

%define iavf_version 4.8.2
Source11:       https://sourceforge.net/projects/e1000/files/iavf%20stable/%{iavf_version}/iavf-%{iavf_version}.tar.gz
%define sha512 iavf=5406b86e61f6528adfd7bc3a5f330cec8bb3b4d6c67395961cc6ab78ec3bd325c3a8655b8f42bf56fb47c62a85fb7dbb0c1aa3ecb6fa069b21acb682f6f578cf

Source12:       ena-Use-new-API-interface-after-napi_hash_del-.patch

%define ice_version 1.11.14
Source13:       https://sourceforge.net/projects/e1000/files/ice%20stable/%{ice_version}/ice-%{ice_version}.tar.gz
%define sha512 ice=a2a6a498e553d41e4e6959a19cdb74f0ceff3a7dbcbf302818ad514fdc18e3d3b515242c88d55ef8a00c9d16925f0cd8579cb41b3b1c27ea6716ccd7e70fd847
%endif

%if 0%{?fips}
Source9:        check_fips_canister_struct_compatibility.inc

%define fips_canister_version 5.0.0-6.1.62-7.ph5-secure
Source16:       fips-canister-%{fips_canister_version}.tar.bz2
%define sha512 fips-canister=e63f5200a669cc40952fc1cfea499d4bc029999098f8252d2c5ffac08392aefe3d57aa68226079dffa4e0f5ddd26c83f85fcebcb21bfd0935aecc8a02f1714a9
%endif

Source21:       spec_install_post.inc
Source22:       %{name}-dracut-%{_arch}.conf

%ifarch x86_64
%define jent_major_version 3.4.1
%define jent_ph_version 4
Source32: jitterentropy-%{jent_major_version}-%{jent_ph_version}.tar.bz2
%define sha512 jitterentropy=37a9380b14d5e56eb3a16b8e46649bc5182813aadb5ec627c31910e4cc622269dfd29359789cb4c13112182f4f8d3c084a6b9c576df06dae9689da44e4735dd2
Source33: jitterentropy_canister_wrapper.c
Source34: jitterentropy_canister_wrapper.h
Source35: jitterentropy_canister_wrapper_asm.S
%endif

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
#HyperV patches
Patch11: vmbus-Don-t-spam-the-logs-with-unknown-GUIDs.patch

# TODO: Is CONFIG_HYPERV_VSOCKETS the same?
#Patchx: 0014-hv_sock-introduce-Hyper-V-Sockets.patch
Patch12: fork-add-sysctl-to-disallow-unprivileged-CLONE_NEWUSER-by.patch
# Out-of-tree patches from AppArmor:
Patch13: apparmor-patch-to-provide-compatibility-with-v2.x-ne.patch
Patch14: apparmor-af_unix-mediation.patch
# floppy:
Patch15: 0001-floppy-lower-printk-message-priority.patch

# Disable md5 algorithm for sctp if fips is enabled.
Patch16: 0001-disable-md5-algorithm-for-sctp-if-fips-is-enabled.patch

# VMware-specific patch to enable turbostat to work on ESXi
Patch17: 0001-tools-power-turbostat-Skip-some-CPUID-checks-if-runn.patch
# Backports of upstream patches to add Ice Lake support to turbostat
Patch18: 0002-tools-power-turbostat-Remove-Package-C6-Retention-on.patch
Patch19: 0003-tools-power-turbostat-Fix-DRAM-Energy-Unit-on-SKX.patch

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
Patch46: 0004-linux-Makefile-Add-kernel-flavor-info-to-the-generat.patch

%ifarch x86_64
# VMW:
Patch55: x86-vmware-Use-Efficient-and-Correct-ALTERNATIVEs-fo-510.patch
Patch56: x86-vmware-Log-kmsg-dump-on-panic-510.patch
Patch57: x86-vmware-Fix-steal-time-clock-under-SEV.patch
Patch58: 0001-x86-vmware-avoid-TSC-recalibration.patch
%endif

# CVE:
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

# Fix for CVE-2022-3524 and CVE-2022-3567
Patch122: 0001-ipv6-annotate-some-data-races-around-sk-sk_prot.patch
Patch126: 0005-ipv6-Fix-data-races-around-sk-sk_prot.patch
Patch127: 0006-tcp-Fix-data-races-around-icsk-icsk_af_ops.patch

#Fix for CVE-2022-43945
Patch130: 0001-NFSD-Cap-rsize_bop-result-based-on-send-buffer-size.patch
Patch131: 0002-NFSD-Protect-against-send-buffer-overflow-in-NFSv3-R.patch
Patch132: 0003-NFSD-Protect-against-send-buffer-overflow-in-NFSv2-R.patch
Patch133: 0004-NFSD-Protect-against-send-buffer-overflow-in-NFSv3-R.patch

#Fix for CVE-2021-3699
Patch135: ipc-replace-costly-bailout-check-in-sysvipc_find_ipc.patch

# Allow PCI resets to be disabled from vfio_pci module
Patch150: 0001-drivers-vfio-pci-Add-kernel-parameter-to-allow-disab.patch
# Add PCI quirk to allow multiple devices under the same virtual PCI bridge
# to be put into separate IOMMU groups on ESXi.
Patch151: 0001-Add-PCI-quirk-for-VMware-PCIe-Root-Port.patch

# Enable CONFIG_DEBUG_INFO_BTF=y
Patch152: 0001-tools-resolve_btfids-Warn-when-having-multiple-IDs-f.patch

%ifarch aarch64
# Rpi of_configfs patches
Patch201: 0001-OF-DT-Overlay-configfs-interface.patch
Patch202: 0002-of-configfs-Use-of_overlay_fdt_apply-API-call.patch
Patch203: 0003-of-overlay-Correct-symbol-path-fixups.patch

# Rpi fan driver
Patch204: 0001-Add-rpi-poe-fan-driver.patch
%endif

# Crypto:
# Patch to invoke crypto self-tests and add missing test vectors to testmgr
Patch500: 0002-FIPS-crypto-self-tests.patch
# Patch to call drbg and dh crypto tests from tcrypt
Patch501: tcrypt-disable-tests-that-are-not-enabled-in-photon.patch
Patch502: 0001-Initialize-jitterentropy-before-ecdh.patch
# Patch to remove urandom usage in rng module
Patch503: 0001-FIPS-crypto-rng-Jitterentropy-RNG-as-the-only-RND-source.patch
# Patch to remove urandom usage in drbg and ecc modules
Patch504: 0003-FIPS-crypto-drbg-Jitterentropy-RNG-as-the-only-RND.patch

%ifarch x86_64
Patch506: 0001-changes-to-build-with-jitterentropy-v3.4.1.patch
%endif

%if 0%{?fips}
# FIPS canister usage patch
Patch508: 0001-FIPS-canister-binary-usage.patch
Patch509: 0001-scripts-kallsyms-Extra-kallsyms-parsing.patch
Patch510: FIPS-do-not-allow-not-certified-algos-in-fips-2.patch
%endif

%ifarch x86_64
# SEV on VMware:
Patch600: 0079-x86-sev-es-Disable-BIOS-ACPI-RSDP-probing-if-SEV-ES-.patch
Patch601: 0080-x86-boot-Enable-vmw-serial-port-via-Super-I-O.patch
Patch602: 0081-x86-sev-es-Disable-use-of-WP-via-PAT-for-__sme_early.patch
Patch603: x86-sev-es-load-idt-before-entering-long-mode-to-han-510.patch
Patch604: x86-swiotlb-Adjust-SWIOTLB-bounce-buffer-size-for-SE.patch
Patch605: x86-sev-es-Do-not-unroll-string-IO-for-SEV-ES-guests.patch

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

%if 0%{?acvp_build:1} && 0%{?fips}
#ACVP test harness patches.
#Need to be applied on top of FIPS canister usage patch to avoid HUNK failure
Patch10100:       0001-crypto-AF_ALG-add-sign-verify-API.patch
Patch10101:       0002-crypto-AF_ALG-add-setpubkey-setsockopt-call.patch
Patch10102:       0003-crypto-AF_ALG-add-asymmetric-cipher.patch
Patch10103:       0004-crypto-AF_ALG-add-DH-keygen-ssgen-API.patch
Patch10104:       0005-crypto-AF_ALG-add-DH-param-ECDH-curve-setsockopt.patch
Patch10105:       0006-crypto-AF_ALG-eliminate-code-duplication.patch
Patch10106:       0007-crypto-AF_ALG-add-KPP-support.patch
Patch10107:       0008-crypto-AF_ALG-add-ECC-support.patch
Patch10108:       0009-kernels-net-Export-sock_getsockopt.patch
Patch10109:       0010-DRBG-Fix-issues-with-DRBG.patch
Patch10110:       0011-Added-jitterentropy-implementation-of-SHA3-256.patch
Patch10111:       0012-jitterentropy-Support-for-sample-collection.patch
%if 0%{?kat_build:1}
Patch10112:       0013-crypto-api-return-status-prints-for-LKCM5-demo.patch
%endif
%endif

BuildRequires:  bc
BuildRequires:  kmod-devel
BuildRequires:  glib-devel
BuildRequires:  elfutils-devel
BuildRequires:  openssl-devel
BuildRequires:  procps-ng-devel
BuildRequires:  audit-devel
BuildRequires:  elfutils-libelf-devel
BuildRequires:  binutils-devel
BuildRequires:  xz-devel
BuildRequires:  slang-devel
BuildRequires:  python3-devel
BuildRequires:  bison
BuildRequires:  dwarves-devel

%ifarch x86_64
BuildRequires:  pciutils-devel
BuildRequires:  libcap-devel
%endif

%if 0%{?fips}
BuildRequires:  gdb
%endif

Requires: filesystem
Requires: kmod
Requires(pre): (coreutils or coreutils-selinux)
Requires(preun): (coreutils or coreutils-selinux)
Requires(post): (coreutils or coreutils-selinux)
Requires(postun): (coreutils or coreutils-selinux)

%description
The Linux package contains the Linux kernel.
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

%package drivers-gpu
Summary:        Kernel GPU Drivers
Group:          System Environment/Kernel
Requires:       %{name} = %{version}-%{release}
%description drivers-gpu
The Linux package contains the Linux kernel drivers for GPU

%package drivers-sound
Summary:        Kernel Sound modules
Group:          System Environment/Kernel
Requires:       %{name} = %{version}-%{release}
%description drivers-sound
The Linux package contains the Linux kernel sound support

%package docs
Summary:        Kernel docs
Group:          System Environment/Kernel
Requires:       python3
%description docs
The Linux package contains the Linux kernel doc files

%ifarch x86_64
%package drivers-intel-sgx
Summary:    Intel SGX driver
Group:      System Environment/Kernel
Requires:   %{name} = %{version}-%{release}
Requires(post): /usr/sbin/groupadd
%description drivers-intel-sgx
This Linux package contains Intel SGX kernel module.

%package oprofile
Summary:        Kernel driver for oprofile, a statistical profiler for Linux systems
Group:          System Environment/Kernel
Requires:       %{name} = %{version}-%{release}
%description oprofile
Kernel driver for oprofile, a statistical profiler for Linux systems
%endif

%package tools
Summary:        This package contains the 'perf' performance analysis tools for Linux kernel
Group:          System/Tools
Requires:       (%{name} = %{version} or linux-esx = %{version} or linux-aws = %{version} or linux-rt = %{version})
Requires:       audit elfutils-libelf binutils-libs
Requires:       xz-libs slang
Requires:       python3 traceevent-plugins
%ifarch x86_64
Requires:       pciutils
%endif
Obsoletes:      linux-aws-tools <= 4.19.52-1
Provides:       linux-aws-tools
%description tools
This package contains kernel tools like perf, turbostat and cpupower.

%package python3-perf
Summary:        Python bindings for applications that will manipulate perf events.
Group:          Development/Libraries
Requires:       linux-tools = %{version}-%{release}
Requires:       python3

%description python3-perf
This package provides a module that permits applications written in the
Python programming language to use the interface to manipulate perf events.

%package -n bpftool
Summary:    Inspection and simple manipulation of eBPF programs and maps
Group:      Development/Libraries
Requires:   linux-tools = %{version}-%{release}

%description -n bpftool
This package contains the bpftool, which allows inspection and simple
manipulation of eBPF programs and maps.

%prep
#TODO: remove rcN after 5.9 goes out of rc
# Using autosetup is not feasible
%setup -q -n linux-%{version}
%ifarch x86_64
# Using autosetup is not feasible
%setup -q -T -D -b 3 -n linux-%{version}
# Using autosetup is not feasible
%setup -q -T -D -b 5 -n linux-%{version}
# Using autosetup is not feasible
%setup -q -T -D -b 10 -n linux-%{version}
# Using autosetup is not feasible
%setup -q -T -D -b 11 -n linux-%{version}
# Using autosetup is not feasible
%setup -q -T -D -b 13 -n linux-%{version}
%endif

%if 0%{?fips}
# Using autosetup is not feasible
%setup -q -T -D -b 16 -n linux-%{version}
%endif

%ifarch x86_64
# Using autosetup is not feasible
%setup -q -T -D -b 32 -n linux-%{version}
%endif

%autopatch -p1 -m0 -M46

%ifarch x86_64
# VMW x86
%autopatch -p1 -m55 -M58
%endif

# CVE
%autopatch -p1 -m100 -M135

# Allow PCI resets to be disabled from vfio_pci module
%autopatch -p1 -m150 -M151

%autopatch -p1 -m152 -M152

%ifarch aarch64
# Rpi of_configfs patches
# Rpi fan driver
%autopatch -p1 -m201 -M204
%endif

# crypto
%autopatch -p1 -m500 -M504

%ifarch x86_64
%autopatch -p1 -m506 -M506
%endif

%if 0%{?fips}
%autopatch -p1 -m508 -M510
%endif

%ifarch x86_64
# SEV on VMware
%autopatch -p1 -m600 -M605

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

%endif

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

%if 0%{?acvp_build:1} && 0%{?fips}
#ACVP test harness patches.
#Need to be applied on top of FIPS canister usage patch to avoid HUNK failure
%autopatch -p1 -m10100 -M10111
%if 0%{?kat_build:1}
%autopatch -p1 -m10112 -M10112
%endif
%endif

%build
%ifarch x86_64
cp -r ../jitterentropy-%{jent_major_version}-%{jent_ph_version}/ \
      crypto/jitterentropy-%{jent_major_version}/
cp %{SOURCE33} crypto/jitterentropy-%{jent_major_version}/
cp %{SOURCE34} crypto/jitterentropy-%{jent_major_version}/
cp %{SOURCE35} crypto/jitterentropy-%{jent_major_version}/
%endif

make %{?_smp_mflags} mrproper
cp %{SOURCE1} .config

%if 0%{?acvp_build:1} && 0%{?fips}
#ACVP test harness changes in kernel configs.
sed -i 's/# CONFIG_CRYPTO_USER is not set/CONFIG_CRYPTO_USER=y/' .config
sed -i 's/# CONFIG_CRYPTO_DH is not set/CONFIG_CRYPTO_DH=y/' .config
sed -i 's/CONFIG_CRYPTO_USER_API=m/CONFIG_CRYPTO_USER_API=y/' .config
sed -i 's/CONFIG_CRYPTO_USER_API_HASH=m/CONFIG_CRYPTO_USER_API_HASH=y/' .config
sed -i 's/CONFIG_CRYPTO_USER_API_SKCIPHER=m/CONFIG_CRYPTO_USER_API_SKCIPHER=y/' .config
sed -i 's/CONFIG_CRYPTO_USER_API_RNG=m/CONFIG_CRYPTO_USER_API_RNG=y/' .config
sed -i 's/# CONFIG_CRYPTO_USER_API_RNG_CAVP is not set/CONFIG_CRYPTO_USER_API_RNG_CAVP=y/' .config
sed -i '/CONFIG_CRYPTO_USER_API_ENABLE_OBSOLETE/ a # CONFIG_CRYPTO_STATS is not set' .config
sed -i '/CONFIG_CRYPTO_STATS/ a CONFIG_CRYPTO_USER_API_AKCIPHER=y' .config
sed -i '/CONFIG_CRYPTO_USER_API_AKCIPHER/ a CONFIG_CRYPTO_USER_API_KPP=y' .config
sed -i '/CONFIG_CRYPTO_USER_API_KPP=y/ a CONFIG_CRYPTO_USER_API_ECC=y' .config
sed -i 's/# CONFIG_CRYPTO_USER_API_AEAD is not set/CONFIG_CRYPTO_USER_API_AEAD=y/' .config
%endif

%if 0%{?fips}
cp ../fips-canister-%{fips_canister_version}/fips_canister.o \
   ../fips-canister-%{fips_canister_version}/fips_canister_wrapper.c \
   ../fips-canister-%{fips_canister_version}/.fips_canister.o.cmd \
   ../fips-canister-%{fips_canister_version}/fips_canister-kallsyms \
   ../fips-canister-%{fips_canister_version}/fips_canister_wrapper_asm.S \
   ../fips-canister-%{fips_canister_version}/fips_canister_wrapper_internal.h \
   ../fips-canister-%{fips_canister_version}/aesni-intel_glue_fips_canister_wrapper.c \
   ../fips-canister-%{fips_canister_version}/testmgr_fips_canister_wrapper.c \
   crypto/
%endif

sed -i 's/CONFIG_LOCALVERSION=""/CONFIG_LOCALVERSION="-%{release}"/' .config

%include %{SOURCE7}

# Set/add CONFIG_CROSS_COMPILE= if needed
if [ %{_host} != %{_build} ]; then
grep -q CONFIG_CROSS_COMPILE= .config && sed -i '/^CONFIG_CROSS_COMPILE=/c\CONFIG_CROSS_COMPILE="%{_host}-"' .config || \
  echo 'CONFIG_CROSS_COMPILE="%{_host}-"' >> .config
fi

make %{?_smp_mflags} V=1 KBUILD_BUILD_VERSION="1-photon" KBUILD_BUILD_HOST="photon" ARCH=%{arch} %{?_smp_mflags}

%if 0%{?fips}
%include %{SOURCE9}
%endif

%ifarch aarch64
ARCH_FLAGS="EXTRA_CFLAGS=-Wno-error=format-overflow"
%endif

make %{?_smp_mflags} ARCH=%{arch} -C tools perf PYTHON=python3 $ARCH_FLAGS
# verify perf has no dependency on libunwind
tools/perf/perf -vv | grep libunwind | grep OFF
tools/perf/perf -vv | grep dwarf | grep on

%ifarch x86_64
# build turbostat and cpupower
make %{?_smp_mflags} ARCH=%{arch} -C tools turbostat cpupower PYTHON=python3

# build ENA module
bldroot="${PWD}"
pushd ../amzn-drivers-ena_linux_%{ena_version}/kernel/linux/ena
patch -p4 < %{SOURCE12}
make %{?_smp_mflags} -C ${bldroot} M="${PWD}" V=1 modules %{?_smp_mflags}
popd

# build Intel SGX module
pushd ../SGXDataCenterAttestationPrimitives-DCAP_%{sgx_version}/driver/linux
make %{?_smp_mflags} KDIR=${bldroot} ARCH=%{arch} %{?_smp_mflags}
popd

# build i40e module
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
make %{?_smp_mflags} ARCH=%{arch} INSTALL_MOD_PATH=%{buildroot} modules_install

%ifarch x86_64
# install ENA module
bldroot="${PWD}"
pushd ../amzn-drivers-ena_linux_%{ena_version}/kernel/linux/ena
make %{?_smp_mflags} -C ${bldroot} M="${PWD}" INSTALL_MOD_PATH=%{buildroot} modules_install
popd

# install Intel SGX module
pushd ../SGXDataCenterAttestationPrimitives-DCAP_%{sgx_version}/driver/linux
mkdir -p %{buildroot}%{_sysconfdir}/udev/rules.d
install -vm 644 10-sgx.rules %{buildroot}/%{_sysconfdir}/udev/rules.d
mkdir -p %{buildroot}%{_modulesdir}/extra
install -vm 644 intel_sgx.ko %{buildroot}%{_modulesdir}/extra/
popd

# The auxiliary.ko kernel module is a common dependency for iavf, i40e
# and ice drivers.  Install it only once, along with the iavf driver
# and re-use it in the ice and i40e drivers.

# install i40e module
pushd ../i40e-%{i40e_version}
make %{?_smp_mflags} -C src KSRC=${bldroot} INSTALL_MOD_PATH=%{buildroot} \
    INSTALL_MOD_DIR=extra MANDIR=%{_mandir} modules_install_no_aux mandocs_install
popd

# install iavf module (with aux module)
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

%ifarch aarch64
install -vm 644 arch/arm64/boot/Image %{buildroot}/boot/vmlinuz-%{uname_r}
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
photon_cmdline=init=/lib/systemd/systemd ro loglevel=3 quiet
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

%ifarch aarch64
ARCH_FLAGS="EXTRA_CFLAGS=-Wno-error=format-overflow"
%endif

make %{?_smp_mflags} -C tools ARCH=%{arch} DESTDIR=%{buildroot} \
     prefix=%{_prefix} perf_install PYTHON=python3 $ARCH_FLAGS

make %{?_smp_mflags} -C tools/perf ARCH=%{arch} DESTDIR=%{buildroot} \
     prefix=%{_prefix} PYTHON=python3 install-python_ext

%ifarch x86_64
make %{?_smp_mflags} -C tools ARCH=%{arch} DESTDIR=%{buildroot} \
     prefix=%{_prefix} mandir=%{_mandir} turbostat_install cpupower_install PYTHON=python3
%endif

make install %{?_smp_mflags} -C tools/bpf/bpftool prefix=%{_prefix} DESTDIR=%{buildroot}

mkdir -p %{buildroot}%{_modulesdir}/dracut.conf.d/
cp -p %{SOURCE22} %{buildroot}%{_modulesdir}/dracut.conf.d/%{name}.conf

%include %{SOURCE2}
%include %{SOURCE6}
%include %{SOURCE21}

%post
/sbin/depmod -a %{uname_r}
ln -sf linux-%{uname_r}.cfg /boot/photon.cfg

%post drivers-gpu
/sbin/depmod -a %{uname_r}

%post drivers-sound
/sbin/depmod -a %{uname_r}

%ifarch x86_64
%post drivers-intel-sgx
/sbin/depmod -a %{uname_r}
getent group sgx_prv >/dev/null || groupadd -r sgx_prv

%post oprofile
/sbin/depmod -a %{uname_r}
%endif

%files
%defattr(-,root,root)
/boot/System.map-%{uname_r}
/boot/config-%{uname_r}
/boot/vmlinuz-%{uname_r}
%config(noreplace) /boot/linux-%{uname_r}.cfg
%defattr(0644,root,root)
%{_modulesdir}/*
%exclude %{_modulesdir}/build
%exclude %{_modulesdir}/kernel/drivers/gpu
%exclude %{_modulesdir}/kernel/sound
%ifarch aarch64
%exclude %{_modulesdir}/kernel/drivers/staging/vc04_services/bcm2835-audio
%endif
%ifarch x86_64
%exclude %{_modulesdir}/kernel/arch/x86/oprofile/
%exclude %{_modulesdir}/extra/intel_sgx.ko.xz
# iavf.conf is used to just blacklist the deprecated i40evf
# and create alias of i40evf to iavf.
# By default iavf is used for VF driver.
# This file creates conflict with other flavour of linux
# thus excluding this file from packaging
%exclude %{_sysconfdir}/modprobe.d/iavf.conf
# ICE driver firmware files are packaged in linux-firmware
%exclude /lib/firmware/updates/intel/ice
%endif

%config(noreplace) %{_modulesdir}/dracut.conf.d/%{name}.conf

%files docs
%defattr(-,root,root)
%{_docdir}/linux-%{uname_r}/*
# For out-of-tree Intel i40e driver.
%ifarch x86_64
%{_mandir}/*
%endif

%files devel
%defattr(-,root,root)
%{_modulesdir}/build
%{_usrsrc}/linux-headers-%{uname_r}

%files drivers-gpu
%defattr(-,root,root)
%exclude %{_modulesdir}/kernel/drivers/gpu/drm/cirrus/
%{_modulesdir}/kernel/drivers/gpu

%files drivers-sound
%defattr(-,root,root)
%{_modulesdir}/kernel/sound

%ifarch aarch64
%{_modulesdir}/kernel/drivers/staging/vc04_services/bcm2835-audio
%endif

%ifarch x86_64
%files drivers-intel-sgx
%defattr(-,root,root)
%{_modulesdir}/extra/intel_sgx.ko.xz
%config(noreplace) %{_sysconfdir}/udev/rules.d/10-sgx.rules

%files oprofile
%defattr(-,root,root)
%{_modulesdir}/kernel/arch/x86/oprofile/
%endif

%files tools
%defattr(-,root,root)

%ifarch x86_64
%exclude %{_lib64}/traceevent
%endif

%ifarch aarch64
%exclude %{_libdir}/traceevent
%endif

%{_bindir}
%{_sysconfdir}/bash_completion.d/perf
%{_libexecdir}/perf-core
%{_datadir}/perf-core
%{_docdir}/perf-tip
%{_libdir}/perf/examples/bpf/*
%{_libdir}/perf/include/bpf/*

%ifarch x86_64
%{_includedir}/cpufreq.h
%{_includedir}/cpuidle.h
%{_lib64dir}/libcpupower.so*
%{_docdir}/packages/cpupower
%{_datadir}/bash-completion/completions/cpupower
%config(noreplace) %{_sysconfdir}/cpufreq-bench.conf
%{_sbindir}/cpufreq-bench
%{_datadir}/locale/*/LC_MESSAGES/cpupower.mo
%endif

%files python3-perf
%defattr(-,root,root)
%{python3_sitelib}/*

%files -n bpftool
%defattr(-,root,root)
%{_sbindir}/bpftool
%{_datadir}/bash-completion/completions/bpftool

%changelog
* Fri Dec 01 2023 Srish Srinivasan <ssrish@vmware.com> 5.10.198-9
- Fix algif_ecc support patch for ECDSA KeyVerification
* Wed Nov 29 2023 Srish Srinivasan <ssrish@vmware.com> 5.10.198-8
- print kernel crypto API return status for LKCM5 demo
  these prints appear only when both ACVP_BUILD and KAT_BUILD
  are enabled during build
- Handle allocation of cipher inside algif_ecc for curves other than
  nist_p256 and nist_p384
- Move all the ACVP related patches under a dedicated directory called
  acvp_patches
* Mon Nov 27 2023 Srish Srinivasan <ssrish@vmware.com> 5.10.198-7
- Remove kat_build and its associated spec changes
* Sat Nov 25 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 5.10.198-6
- Update canister to 5.0.0-6.1.62-7
* Tue Nov 21 2023 Keerthana K <keerthanak@vmware.com> 5.10.198-5
- Update canister to 5.0.0-6.1.62-2
* Tue Oct 31 2023 Srinidhi Rao <srinidhir@vmware.com> 5.10.198-4
- Jitterentropy sample collection support in ACVP Build.
* Thu Oct 26 2023 Srish Srinivasan <ssrish@vmware.com> 5.10.198-3
- Upgrade canister to 5.0.0-6.1.56-6
* Fri Oct 13 2023 Srish Srinivasan <ssrish@vmware.com> 5.10.198-2
- Ensure all the necessary crypto self-tests are run irrespective
  of whether the canister is used in the kernel build or not
- Fix tcrypt tests
- Apply jitterentropy builder patch before canister binary usage patch
* Fri Oct 13 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 5.10.198-1
- Update to version 5.10.198
- Fix CVE-2023-4244
- Update canister to 5.0.0-6.1.56-3
* Thu Oct 12 2023 Keerthana K <keerthanak@vmware.com> 5.10.197-1
- Update to version 5.10.197
* Wed Oct 11 2023 Srinidhi Rao <srinidhir@vmware.com> 5.10.190-3
- Jitterentropy wrapper changes.
* Tue Oct 03 2023 Srish Srinivasan <ssrish@vmware.com> 5.10.190-2
- Tweak ACVP kernel patches to support LKCM 5.0 canister
- Added jitterentropy implementation of SHA3-256
* Wed Sep 27 2023 Keerthana K <keerthanak@vmware.com> 5.10.190-1
- Update to version 5.10.190
* Fri Sep 15 2023 Srish Srinivasan <ssrish@vmware.com> 5.10.183-6
- Use canister version 5.0.0-6.1.45-7
* Tue Sep 12 2023 Keerthana K <keerthanak@vmware.com> 5.10.183-5
- Build with jitterentropy v3.4.1-1
* Fri Sep 08 2023 Keerthana K <keerthanak@vmware.com> 5.10.183-4
- Use canister version 5.0.0-6.1.45-4
* Mon Jul 17 2023 Keerthana K <keerthanak@vmware.com> 5.10.183-3
- Use canister version 5.0.0-6.1.37-2
* Tue Jul 04 2023 Keerthana K <keerthanak@vmware.com> 5.10.183-2
- Use canister 5.0.0-6.1.10-18
* Thu Jun 08 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 5.10.183-1
- Update to version 5.10.183, fix some CVEs
* Wed May 17 2023 Ankit Jain <ankitja@vmware.com> 5.10.180-1
- Update to version 5.10.180
* Wed May 17 2023 Srish Srinivasan <ssrish@vmware.com> 5.10.175-8
- Added support for ACVP build
* Mon May 08 2023 Srish Srinivasan <ssrish@vmware.com> 5.10.175-7
- Enable CONFIG_DEBUG_INFO_BTF=y
* Wed Apr 26 2023 Shreenidhi Shedi <sshedi@vmware.com> 5.10.175-6
- Fix aarch64 initrd driver list
* Sun Apr 16 2023 Shreenidhi Shedi <sshedi@vmware.com> 5.10.175-5
- Fix initrd generation logic
* Wed Apr 12 2023 Ajay Kaher <akaher@vmware.com> 5.10.175-4
- perf: remove libunwind dependency
* Tue Apr 11 2023 Roye Eshed <eshedr@vmware.com> 5.10.175-3
- Fix for CVE-2022-39189
* Mon Apr 10 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 5.10.175-2
- update to latest ToT vmxnet3 driver pathes
* Tue Apr 04 2023 Roye Eshed <eshedr@vmware.com> 5.10.175-1
- Update to version 5.10.175
* Tue Apr 04 2023 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.168-7
- Fix IRQ affinity of i40e driver
* Thu Mar 30 2023 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.168-6
- Expose Photon kernel macros to simplify building out-of-tree drivers.
* Fri Mar 17 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 5.10.168-5
- Update intel ethernet drivers to:
- i40e: 2.22.18
- iavf: 4.8.2
- ice: 1.11.14
* Tue Feb 28 2023 Ankit Jain <ankitja@vmware.com> 5.10.168-4
- Exclude iavf.conf
* Mon Feb 27 2023 Ajay Kaher <akaher@vmware.com> 5.10.168-3
- exclude man dir from linux-tools
* Fri Feb 17 2023 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.168-2
- Enable turbostat to work in the guest on VMware hypervisor.
- Add support for Intel Ice Lake server CPUs to turbostat.
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
* Mon Oct 31 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.142-5
- Replace rpm macro 'name' with 'linux' to be consistent with other flavors.
* Mon Oct 17 2022 Sharan Turlapati <sturlapati@vmware.com> 5.10.142-4
- Fix for CVE-2022-2602
* Wed Oct 12 2022 Sharan Turlapati <sturlapati@vmware.com> 5.10.142-3
- Fixes for CVEs in the wifi subsystem
* Wed Sep 14 2022 Shreenidhi Shedi <sshedi@vmware.com> 5.10.142-2
- Add bpftool subpackage
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
* Mon Jul 18 2022 Keerthana K <keerthanak@vmware.com> 5.10.118-11
- Update iavf driver to v4.4.2
- Update ice driver to v1.8.3
* Fri Jul 15 2022 Keerthana K <keerthanak@vmware.com> 5.10.118-10
- .config: enable CONFIG_NET_ACT_SIMP
* Fri Jul 15 2022 Keerthana K <keerthanak@vmware.com> 5.10.118-9
- .config: enable CONFIG_X86_CPU_RESCTRL
* Fri Jul 15 2022 Keerthana K <keerthanak@vmware.com> 5.10.118-8
- Enable cgroup v1 stats
- .config: enable PERCPU_STATS
* Fri Jul 15 2022 Keerthana K <keerthanak@vmware.com> 5.10.118-7
- Avoid TSC recalibration
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
- Enabling config_livepatch and related, including ftrace
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
- Enable crypto related configs in aarch64 similar to x86_64
- crypto_self_test and broken kattest module enhancements
* Fri Dec 17 2021 Alexey Makhalov <amakhalov@vmware.com> 5.10.83-5
- mm: fix percpu alloacion for memoryless nodes
- pvscsi: fix disk detection issue
* Fri Dec 17 2021 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 5.10.83-4
- Disable md5 algorithm for sctp if fips is enabled.
* Tue Dec 14 2021 Harinadh D <hdommaraju@vmware.com> 5.10.83-3
- remove tmem,lvm in add-drivers list
- lvm drivers are built as part of dm-mod
- tmem module is no longer exist
* Thu Dec 09 2021 Prashant S Chauhan <psinghchauha@vmware.com> 5.10.83-2
- Bump up to compile with python 3.10
* Mon Dec 06 2021 srinidhira0 <srinidhir@vmware.com> 5.10.83-1
- Update to version 5.10.83
* Mon Nov 29 2021 Srinidhi Rao <srinidhir@vmware.com> 5.10.78-5
- Enable eBPF Net Packet filter support.
* Thu Nov 18 2021 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.78-4
- Add PCI quirk to allow multiple devices under the same virtual
- PCI bridge to be put into separate IOMMU groups.
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
* Tue Jun 22 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.42-3
- Fix for CVE-2021-3609
* Thu Jun 10 2021 Keerthana K <keerthanak@vmware.com> 5.10.42-2
- Added script to check structure compatibility between fips_canister.o and vmlinux.
* Thu Jun 03 2021 Keerthana K <keerthanak@vmware.com> 5.10.42-1
- Update to version 5.10.42
- Remove XR usb driver support
- .config: Enable CONFIG_FANOTIFY_ACCESS_PERMISSIONS
* Wed Jun 02 2021 Keerthana K <keerthanak@vmware.com> 5.10.35-4
- Fix for CVE-2021-3573
* Thu May 20 2021 Ajay Kaher <akaher@vmware.com> 5.10.35-3
- Add Rpi fan driver
* Thu May 20 2021 Ajay Kaher <akaher@vmware.com> 5.10.35-2
- Fix for CVE-2021-3564
* Mon May 17 2021 Ajay Kaher <akaher@vmware.com> 5.10.35-1
- Update to version 5.10.35
* Thu May 13 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.25-10
- Fix for CVE-2021-23133
* Tue May 11 2021 Ankit Jain <ankitja@vmware.com> 5.10.25-9
- .config: Enable MLX5_INFINIBAND
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
- Remove hmac(sha224) test from broken kat test.
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
* Mon Mar 15 2021 Srinidhi Rao <srinidhir@vmware.com> 5.10.21-2
- Use jitterentropy rng instead of urandom in rng module.
* Mon Mar 08 2021 Vikash Bansal <bvikas@vmware.com> 5.10.21-1
- Update to version 5.10.21
* Mon Mar 01 2021 Alexey Makhalov <amakhalov@vmware.com> 5.10.4-17
- FIPS canister update
* Fri Feb 19 2021 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.4-16
- Fix /boot/photon.cfg symlink when /boot is a separate partition.
* Fri Feb 19 2021 Ajay Kaher <akaher@vmware.com> 5.10.4-15
- Added SEV-ES improvement patches
* Thu Feb 18 2021 Ajay Kaher <akaher@vmware.com> 5.10.4-14
- Enable CONFIG_WDAT_WDT
* Thu Feb 18 2021 Ajay Kaher <akaher@vmware.com> 5.10.4-13
- lower the loglevel for floppy driver
* Thu Feb 18 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.4-12
- Enable CONFIG_IFB
* Wed Feb 17 2021 Ankit Jain <ankitja@vmware.com> 5.10.4-11
- Added latest out of tree version of Intel ice driver
* Tue Feb 16 2021 Alexey Makhalov <amakhalov@vmware.com> 5.10.4-10
- Fix perf compilation issue with gcc-10.2.0 for aarch64
* Mon Feb 15 2021 Keerthana K <keerthanak@vmware.com> 5.10.4-9
- Added crypto_self_test and kattest module.
- These patches are applied when kat_build is enabled.
* Wed Feb 03 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 5.10.4-8
- Update i40e driver to v2.13.10
- Add out of tree iavf driver
- Enable CONFIG_NET_TEAM
* Thu Jan 28 2021 Alexey Makhalov <amakhalov@vmware.com> 5.10.4-7
- Use secure FIPS canister.
* Mon Jan 25 2021 Ankit Jain <ankitja@vmware.com> 5.10.4-6
- Enabled CONFIG_WIREGUARD
* Fri Jan 22 2021 Keerthana K <keerthanak@vmware.com> 5.10.4-5
- Build kernel with FIPS canister.
* Wed Jan 20 2021 Alexey Makhalov <amakhalov@vmware.com> 5.10.4-4
- Handle module.lds for aarch64 in the same way as for x86_64
* Wed Jan 13 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.4-3
- Remove traceevent/plugins from linux-tools
* Mon Jan 11 2021 Bo Gan <ganb@vmware.com> 5.10.4-2
- Fix aarch64 build failure
* Mon Jan 04 2021 Bo Gan <ganb@vmware.com> 5.10.4-1
- Update to 5.10.4
- Drop out-of-tree SEV-ES functional patches (already upstreamed).
* Wed Dec 09 2020 Ajay Kaher <akaher@vmware.com> 5.9.0-9
- To dynamic load Overlays adding of_configfs patches v5.9.y.
* Tue Dec 01 2020 Prashant S Chauhan <psinghchauha@vmware.com> 5.9.0-8
- Added ami for arm support in linux generic, added multiple drivers
- in aarch64 to support aws ami
* Thu Nov 12 2020 Ajay Kaher <akaher@vmware.com> 5.9.0-7
- .config: support for floppy disk and ch341 usb to serial
* Wed Nov 11 2020 Tapas Kundu <tkundu@vmware.com> 5.9.0-6
- Fix perf python script for compatibility with python 3.9
* Tue Nov 10 2020 Keerthana K <keerthanak@vmware.com> 5.9.0-5
- Fix CVE-2020-8694
* Fri Nov 06 2020 Keerthana K <keerthanak@vmware.com> 5.9.0-4
- Fix CVE-2020-25704
* Tue Nov 03 2020 Srinidhi Rao <srinidhir@vmware.com> 5.9.0-3
- Remove the support of fipsify and hmacgen
* Tue Oct 27 2020 Piyush Gupta <gpiyush@vmware.com> 5.9.0-2
- Fix aarch64 build failure due to missing CONFIG_FB_ARMLCD
* Mon Oct 19 2020 Bo Gan <ganb@vmware.com> 5.9.0-1
- Update to 5.9.0
* Wed Sep 30 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.9.0-rc7.1
- Update to version 5.9.0-rc7
* Mon Sep 21 2020 Bo Gan <ganb@vmware.com> 5.9.0-rc4.1
- Update to 5.9.0-rc4
- AMD SEV-ES Support
- RPI4 Support
- config_common: Reduce linked-in modules
- Drop NXP LS10XXa board support
* Tue Sep 08 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 4.19.127-6
- Fix build failure with binutils updated to 2.35
* Wed Aug 05 2020 Sharan Turlapati <sturlapati@vmware.com> 4.19.127-5
- Enable CONFIG_TCP_CONG_BBR
* Wed Jul 29 2020 Alexey Makhalov <amakhalov@vmware.com> 4.19.127-4
- .config: add zram module
* Mon Jul 27 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.127-3
- Fix CVE-2020-14331
* Fri Jul 17 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.127-2
- Fix aarch64 build failure due to missing i40e man pages.
* Tue Jun 23 2020 Keerthana K <keerthanak@vmware.com> 4.19.127-1
- Update to version 4.19.127
* Tue Jun 16 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.112-14
- Add latest out of tree version of i40e driver
* Wed Jun 10 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.112-13
- Enable CONFIG_VFIO_NOIOMMU
* Tue Jun 09 2020 Alexey Makhalov <amakhalov@vmware.com> 4.19.112-12
- Add intel_sgx module (-drivers-intel-sgx subpackage)
* Fri Jun 05 2020 Ankit Jain <ankitja@vmware.com> 4.19.112-11
- Enabled CONFIG_BINFMT_MISC
* Tue Jun 02 2020 Vikash Bansal <bvikas@vmware.com> 4.19.112-10
- Add patch to fix CVE-2019-18885
* Mon Jun 1 2020 Shreenidhi Shedi <sshedi@vmware.com> 4.19.112-9
- Keep modules of running kernel till next boot
* Sat May 30 2020 Alexey Makhalov <amakhalov@vmware.com> 4.19.112-8
- .config: add gs_usb module
* Wed May 20 2020 Tapas Kundu <tkundu@vmware.com> 4.19.112-7
- Added linux-python3-perf subpackage.
- Added turbostat and cpupower to tools for x86_64.
- linux-python3-perf replaces python3-perf.
* Fri May 15 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.112-6
- Add uio_pic_generic driver support in config
* Wed May 06 2020 Siddharth Chandrasekaran <csiddharth@vmware.com> 4.19.112-5
- Add patch to fix CVE-2020-10711
* Wed Apr 29 2020 Keerthana K <keerthanak@vmware.com> 4.19.112-4
- Photon-checksum-generator version update to 1.1.
* Wed Apr 29 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.112-3
- Enable additional config options.
* Wed Apr 15 2020 Vikash Bansal <bvikas@vmware.com> 4.19.112-2
- HMAC-SHA256 digest of hmac_generator module moved to hmacgen package
* Wed Apr 08 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.112-1
- Update to version 4.19.112
* Tue Mar 31 2020 Vikash Bansal <bvikas@vmware.com> 4.19.104-2
- hmac generation of crypto modules and initrd generation changes if fips=1
* Wed Mar 25 2020 Vikash Bansal <bvikas@vmware.com> 4.19.104-1
- Update to version 4.19.104
* Mon Mar 23 2020 Alexey Makhalov <amakhalov@vmware.com> 4.19.97-8
- Fix perf compilation issue with binutils >= 2.34.
* Mon Mar 16 2020 Keerthana K <keerthanak@vmware.com> 4.19.97-7
- Adding Enhances depedency to hmacgen.
* Wed Mar 04 2020 Vikash Bansal <bvikas@vmware.com> 4.19.97-6
- Backporting of patch continuous testing of RNG from urandom
* Tue Feb 25 2020 Ajay Kaher <akaher@vmware.com> 4.19.97-5
- Fix CVE-2019-16234
* Tue Feb 11 2020 Keerthana K <keerthanak@vmware.com> 4.19.97-4
- Add photon-checksum-generator source tarball and remove hmacgen patch.
- Exclude hmacgen.ko from base package.
* Fri Jan 31 2020 Ajay Kaher <akaher@vmware.com> 4.19.97-3
- Move snd-bcm2835.ko to linux-drivers-sound rpm
* Wed Jan 29 2020 Keerthana K <keerthanak@vmware.com> 4.19.97-2
- Update tcrypt to test drbg_pr_sha256 and drbg_nopr_sha256.
- Update testmgr to add drbg_pr_ctr_aes256 test vectors.
* Fri Jan 17 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.97-1
- Update to version 4.19.97
* Thu Jan 16 2020 Srinidhi Rao <srinidhir@vmware.com> 4.19.87-6
- Enable DRBG HASH and DRBG CTR support.
* Wed Jan 08 2020 Ajay Kaher <akaher@vmware.com> 4.19.87-5
- Enabled configs RTC_DRV_PL030, RTC_DRV_PL031
* Fri Jan 03 2020 Keerthana K <keerthanak@vmware.com> 4.19.87-4
- Modify tcrypt to remove tests for algorithms that are not supported in photon.
- Added tests for DH, DRBG algorithms.
* Thu Jan 02 2020 Keerthana K <keerthanak@vmware.com> 4.19.87-3
- Update fips Kat tests patch.
* Mon Dec 09 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.87-2
- Cross compilation support
* Fri Dec 06 2019 Ajay Kaher <akaher@vmware.com> 4.19.87-1
- Update to version 4.19.87
* Tue Dec 03 2019 Keerthana K <keerthanak@vmware.com> 4.19.84-4
- Adding hmac sha256/sha512 generator kernel module for fips.
* Tue Nov 26 2019 Ajay Kaher <akaher@vmware.com> 4.19.84-3
- Fix CVE-2019-19062, CVE-2019-19066, CVE-2019-19072,
- CVE-2019-19073, CVE-2019-19074, CVE-2019-19078
* Mon Nov 18 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.84-2
- .config: infiniband support.
* Tue Nov 12 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.84-1
- Update to version 4.19.84
- Fix CVE-2019-18814
* Fri Nov 08 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.82-1
- Update to version 4.19.82
* Thu Nov 07 2019 Jorgen Hansen (VMware) <jhansen@vmware.com> 4.19.79-3
- Fix vsock QP detach with outgoing data
* Thu Oct 24 2019 Ajay Kaher <akaher@vmware.com> 4.19.79-2
- Enabled WiFi and BT config for Dell 5K.
* Tue Oct 15 2019 Ajay Kaher <akaher@vmware.com> 4.19.79-1
- Update to version 4.19.79
- Fix CVE-2019-17133
* Mon Oct 14 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.76-5
- Add megaraid_sas driver to initramfs
* Mon Oct 14 2019 Bo Gan <ganb@vmware.com> 4.19.76-4
- Enable IMA with SHA256 as default hash algorithm
* Thu Oct 10 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.76-3
- Add additional BuildRequires and Requires to fix issues with perf, related to
- interactive UI and C++ symbol demangling. Also update the last few perf python
- scripts in Linux kernel to use python3 syntax.
* Thu Oct 10 2019 Harinadh D <hdommaraju@vmware.com> 4.19.76-2
- Adding lvm and dm-mod modules to support root as lvm
* Wed Oct 02 2019 Ajay Kaher <akaher@vmware.com> 4.19.76-1
- Update to version 4.19.76
- Enable USB_SERIAL_PL2303 for aarch64
* Mon Sep 30 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.72-1
- Update to version 4.19.72
* Thu Sep 05 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.69-3
- Avoid oldconfig which leads to potential build hang
- Fix archdir usage
* Thu Sep 05 2019 Ajay Kaher <akaher@vmware.com> 4.19.69-2
- Adding SPI and Audio interfaces in rpi3 device tree
- Adding spi0 and audio overlays
- Copying rpi dt in /boot/broadcom as u-boot picks from here
* Fri Aug 30 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.69-1
- Update to version 4.19.69
* Fri Aug 23 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.65-4
- NXP ls1046a frwy board support.
- config_aarch64: add fsl_dpaa2 support.
- fix fsl_dpaa_mac initialization issue.
* Wed Aug 14 2019 Raejoon Jung <rjung@vmware.com> 4.19.65-3
- Backport of Secure Boot UEFI certificate import from v5.2
* Mon Aug 12 2019 Ajay Kaher <akaher@vmware.com> 4.19.65-2
- Fix config_aarch64 for v4.19.65
* Tue Aug 06 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.65-1
- Update to version 4.19.65
- Fix CVE-2019-1125 (SWAPGS)
* Tue Jul 30 2019 Ajay Kaher <akaher@vmware.com> 4.19.52-7
- Added of_configfs patches to dynamic load Overlays.
* Thu Jul 25 2019 Keerthana K <keerthanak@vmware.com> 4.19.52-6
- Fix postun scriplet.
* Thu Jul 11 2019 Keerthana K <keerthanak@vmware.com> 4.19.52-5
- Enable kernel configs necessary for BPF Compiler Collection (BCC).
* Wed Jul 10 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.52-4
- Deprecate linux-aws-tools in favor of linux-tools.
* Tue Jul 02 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.52-3
- Fix 9p vsock 16bit port issue.
* Thu Jun 20 2019 Tapas Kundu <tkundu@vmware.com> 4.19.52-2
- Enabled CONFIG_I2C_CHARDEV to support lm-sensors
* Mon Jun 17 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.52-1
- Update to version 4.19.52
- Fix CVE-2019-12456, CVE-2019-12379, CVE-2019-12380, CVE-2019-12381,
- CVE-2019-12382, CVE-2019-12378, CVE-2019-12455
* Tue May 28 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.40-3
- Change default I/O scheduler to 'deadline' to fix performance issue.
* Tue May 14 2019 Keerthana K <keerthanak@vmware.com> 4.19.40-2
- Fix to parse through /boot folder and update symlink (/boot/photon.cfg) if
- mulitple kernels are installed and current linux kernel is removed.
* Tue May 07 2019 Ajay Kaher <akaher@vmware.com> 4.19.40-1
- Update to version 4.19.40
* Thu Apr 11 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.32-3
- Update config_aarch64 to fix ARM64 build.
* Fri Mar 29 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.32-2
- Fix CVE-2019-10125
* Wed Mar 27 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.32-1
- Update to version 4.19.32
* Thu Mar 14 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.29-1
- Update to version 4.19.29
* Tue Mar 05 2019 Ajay Kaher <akaher@vmware.com> 4.19.26-1
- Update to version 4.19.26
* Thu Feb 21 2019 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.15-3
- Fix CVE-2019-8912
* Thu Jan 24 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.15-2
- Add WiFi (ath10k), sensors (i2c,spi), usb support for NXP LS1012A board.
* Tue Jan 15 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.15-1
- Update to version 4.19.15
* Fri Jan 11 2019 Srinidhi Rao <srinidhir@vmware.com> 4.19.6-7
- Add Network support for NXP LS1012A board.
* Wed Jan 09 2019 Ankit Jain <ankitja@vmware.com> 4.19.6-6
- Enable following for x86_64 and aarch64:
-  Enable Kernel Address Space Layout Randomization.
-  Enable CONFIG_SECURITY_NETWORK_XFRM
* Fri Jan 04 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.6-5
- Enable AppArmor by default.
* Wed Jan 02 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.6-4
- .config: added Compulab fitlet2 device drivers
- .config_aarch64: added gpio sysfs support
- renamed -sound to -drivers-sound
* Tue Jan 01 2019 Ajay Kaher <akaher@vmware.com> 4.19.6-3
- .config: Enable CONFIG_PCI_HYPERV driver
* Wed Dec 19 2018 Srinidhi Rao <srinidhir@vmware.com> 4.19.6-2
- Add NXP LS1012A support.
* Mon Dec 10 2018 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.6-1
- Update to version 4.19.6
* Fri Dec 07 2018 Alexey Makhalov <amakhalov@vmware.com> 4.19.1-3
- .config: added qmi wwan module
* Mon Nov 12 2018 Ajay Kaher <akaher@vmware.com> 4.19.1-2
- Fix config_aarch64 for 4.19.1
* Mon Nov 05 2018 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.1-1
- Update to version 4.19.1
* Tue Oct 16 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.18.9-5
- Change in config to enable drivers for zigbee and GPS
* Fri Oct 12 2018 Ajay Kaher <akaher@vmware.com> 4.18.9-4
- Enable LAN78xx for aarch64 rpi3
* Fri Oct 5 2018 Ajay Kaher <akaher@vmware.com> 4.18.9-3
- Fix config_aarch64 for 4.18.9
- Add module.lds for aarch64
* Wed Oct 03 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.18.9-2
- Use updated steal time accounting patch.
- .config: Enable CONFIG_CPU_ISOLATION and a few networking options
- that got accidentally dropped in the last update.
* Mon Oct 1 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.18.9-1
- Update to version 4.18.9
* Tue Sep 25 2018 Ajay Kaher <akaher@vmware.com> 4.14.67-2
- Build hang (at make oldconfig) fix in config_aarch64
* Wed Sep 19 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.14.67-1
- Update to version 4.14.67
* Tue Sep 18 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.14.54-7
- Add rdrand-based RNG driver to enhance kernel entropy.
* Sun Sep 02 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.14.54-6
- Add full retpoline support by building with retpoline-enabled gcc.
* Thu Aug 30 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.14.54-5
- Apply out-of-tree patches needed for AppArmor.
* Wed Aug 22 2018 Alexey Makhalov <amakhalov@vmware.com> 4.14.54-4
- Fix overflow kernel panic in rsi driver.
- .config: enable BT stack, enable GPIO sysfs.
- Add Exar USB serial driver.
* Fri Aug 17 2018 Ajay Kaher <akaher@vmware.com> 4.14.54-3
- Enabled USB PCI in config_aarch64
- Build hang (at make oldconfig) fix in config_aarch64
* Thu Jul 19 2018 Alexey Makhalov <amakhalov@vmware.com> 4.14.54-2
- .config: usb_serial_pl2303=m,wlan=y,can=m,gpio=y,pinctrl=y,iio=m
* Mon Jul 09 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.14.54-1
- Update to version 4.14.54
* Fri Jan 26 2018 Alexey Makhalov <amakhalov@vmware.com> 4.14.8-2
- Added vchiq entry to rpi3 dts
- Added dtb-rpi3 subpackage
* Fri Dec 22 2017 Alexey Makhalov <amakhalov@vmware.com> 4.14.8-1
- Version update
* Wed Dec 13 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.66-4
- KAT build support
* Thu Dec 07 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.66-3
- Aarch64 support
* Tue Dec 05 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.66-2
- Sign and compress modules after stripping. fips=1 requires signed modules
* Mon Dec 04 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.66-1
- Version update
* Tue Nov 21 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.64-1
- Version update
* Mon Nov 06 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.60-1
- Version update
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
* Tue Aug 22 2017 Anish Swaminathan <anishs@vmware.com> 4.9.43-2
- Add missing xen block drivers
* Mon Aug 14 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.43-1
- Version update
- [feature] new sysctl option unprivileged_userns_clone
* Wed Aug 09 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.41-2
- Fix CVE-2017-7542
- [bugfix] Added ccm,gcm,ghash,lzo crypto modules to avoid
    panic on modprobe tcrypt
* Mon Aug 07 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.41-1
- Version update
* Fri Aug 04 2017 Bo Gan <ganb@vmware.com> 4.9.38-6
- Fix initramfs triggers
* Tue Aug 01 2017 Anish Swaminathan <anishs@vmware.com> 4.9.38-5
- Allow some algorithms in FIPS mode
- Reverts 284a0f6e87b0721e1be8bca419893902d9cf577a and backports
- bcf741cb779283081db47853264cc94854e7ad83 in the kernel tree
- Enable additional NF features
* Fri Jul 21 2017 Anish Swaminathan <anishs@vmware.com> 4.9.38-4
- Add patches in Hyperv codebase
* Fri Jul 21 2017 Anish Swaminathan <anishs@vmware.com> 4.9.38-3
- Add missing hyperv drivers
* Thu Jul 20 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.38-2
- Disable scheduler beef up patch
* Tue Jul 18 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.38-1
- Fix CVE-2017-11176 and CVE-2017-10911
* Mon Jul 03 2017 Xiaolin Li <xiaolinl@vmware.com> 4.9.34-3
- Add libdnet-devel, kmod-devel and libmspack-devel to BuildRequires
* Thu Jun 29 2017 Divya Thaluru <dthaluru@vmware.com> 4.9.34-2
- Added obsolete for deprecated linux-dev package
* Wed Jun 28 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.34-1
- [feature] 9P FS security support
- [feature] DM Delay target support
- Fix CVE-2017-1000364 ("stack clash") and CVE-2017-9605
* Thu Jun 8 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.31-1
- Fix CVE-2017-8890, CVE-2017-9074, CVE-2017-9075, CVE-2017-9076
    CVE-2017-9077 and CVE-2017-9242
- [feature] IPV6 netfilter NAT table support
* Fri May 26 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.30-1
- Added ENA driver for AMI
- Fix CVE-2017-7487 and CVE-2017-9059
* Wed May 17 2017 Vinay Kulkarni <kulkarniv@vmware.com> 4.9.28-2
- Enable IPVLAN module.
* Tue May 16 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.28-1
- Version update
* Wed May 10 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.27-1
- Version update
* Sun May 7 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.26-1
- Version update
- Removed version suffix from config file name
* Thu Apr 27 2017 Bo Gan <ganb@vmware.com> 4.9.24-2
- Support dynamic initrd generation
* Tue Apr 25 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.24-1
- Fix CVE-2017-6874 and CVE-2017-7618.
- Fix audit-devel BuildRequires.
- .config: build nvme and nvme-core in kernel.
* Mon Mar 6 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.13-2
- .config: NSX requirements for crypto and netfilter
* Tue Feb 28 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.13-1
- Update to linux-4.9.13 to fix CVE-2017-5986 and CVE-2017-6074
* Thu Feb 09 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.9-1
- Update to linux-4.9.9 to fix CVE-2016-10153, CVE-2017-5546,
    CVE-2017-5547, CVE-2017-5548 and CVE-2017-5576.
- .config: added CRYPTO_FIPS support.
* Tue Jan 10 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.2-1
- Update to linux-4.9.2 to fix CVE-2016-10088
- Move linux-tools.spec to linux.spec as -tools subpackage
* Mon Dec 19 2016 Xiaolin Li <xiaolinl@vmware.com> 4.9.0-2
- BuildRequires Linux-PAM-devel
* Mon Dec 12 2016 Alexey Makhalov <amakhalov@vmware.com> 4.9.0-1
- Update to linux-4.9.0
- Add paravirt stolen time accounting feature (from linux-esx),
    but disable it by default (no-vmw-sta cmdline parameter)
* Thu Dec  8 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.35-3
- net-packet-fix-race-condition-in-packet_set_ring.patch
    to fix CVE-2016-8655
* Wed Nov 30 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.35-2
- Expand `uname -r` with release number
- Check for build-id matching
- Added syscalls tracing support
- Compress modules
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
- .config: add cgrup_hugetlb support
- .config: add netfilter_xt_{set,target_ct} support
- .config: add netfilter_xt_match_{cgroup,ipvs} support
* Thu Nov 10 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.31-1
- Update to linux-4.4.31
* Fri Oct 21 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.26-1
- Update to linux-4.4.26
* Wed Oct 19 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.20-6
- net-add-recursion-limit-to-GRO.patch
- scsi-arcmsr-buffer-overflow-in-arcmsr_iop_message_xfer.patch
* Tue Oct 18 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.20-5
- ipip-properly-mark-ipip-GRO-packets-as-encapsulated.patch
- tunnels-dont-apply-GRO-to-multiple-layers-of-encapsulation.patch
* Mon Oct  3 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.20-4
- Package vmlinux with PROGBITS sections in -debuginfo subpackage
* Tue Sep 27 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.20-3
- .config: CONFIG_IP_SET_HASH_{IPMARK,MAC}=m
* Tue Sep 20 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.20-2
- Add -release number for /boot/* files
- Use initrd.img with version and release number
- Rename -dev subpackage to -devel
* Wed Sep  7 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.20-1
- Update to linux-4.4.20
- apparmor-fix-oops-validate-buffer-size-in-apparmor_setprocattr.patch
- keys-fix-asn.1-indefinite-length-object-parsing.patch
* Thu Aug 25 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-11
- vmxnet3 patches to bumpup a version to 1.4.8.0
* Wed Aug 10 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-10
- Added VSOCK-Detach-QP-check-should-filter-out-non-matching-QPs.patch
- .config: pmem hotplug + ACPI NFIT support
- .config: enable EXPERT mode, disable UID16 syscalls
* Thu Jul 07 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-9
- .config: pmem + fs_dax support
* Fri Jun 17 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-8
- patch: e1000e-prevent-div-by-zero-if-TIMINCA-is-zero.patch
- .config: disable rt group scheduling - not supported by systemd
* Wed Jun 15 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.4.8-7
- fixed the capitalization for - System.map
* Thu May 26 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-6
- patch: REVERT-sched-fair-Beef-up-wake_wide.patch
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.4.8-5
- GA - Bump release of all rpms
* Mon May 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.4.8-4
- Fixed generation of debug symbols for kernel modules & vmlinux.
* Mon May 23 2016 Divya Thaluru <dthaluru@vmware.com> 4.4.8-3
- Added patches to fix CVE-2016-3134, CVE-2016-3135
* Wed May 18 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.4.8-2
- Enabled CONFIG_UPROBES in config as needed by ktap
* Wed May 04 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-1
- Update to linux-4.4.8
- Added net-Drivers-Vmxnet3-set-... patch
* Tue May 03 2016 Vinay Kulkarni <kulkarniv@vmware.com> 4.2.0-27
- Compile Intel GigE and VMXNET3 as part of kernel.
* Thu Apr 28 2016 Nick Shi <nshi@vmware.com> 4.2.0-26
- Compile cramfs.ko to allow mounting cramfs image
* Tue Apr 12 2016 Vinay Kulkarni <kulkarniv@vmware.com> 4.2.0-25
- Revert network interface renaming disable in kernel.
* Tue Mar 29 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-24
- Support kmsg dumping to vmware.log on panic
- sunrpc: xs_bind uses ip_local_reserved_ports
* Mon Mar 28 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.2.0-23
- Enabled Regular stack protection in Linux kernel in config
* Thu Mar 17 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.2.0-22
- Restrict the permissions of the /boot/System.map-X file
* Fri Mar 04 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-21
- Patch: SUNRPC: Do not reuse srcport for TIME_WAIT socket.
* Wed Mar 02 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-20
- Patch: SUNRPC: Ensure that we wait for connections to complete
    before retrying
* Fri Feb 26 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-19
- Disable watchdog under VMware hypervisor.
* Thu Feb 25 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-18
- Added rpcsec_gss_krb5 and nfs_fscache
* Mon Feb 22 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-17
- Added sysctl param to control weighted_cpuload() behavior
* Thu Feb 18 2016 Divya Thaluru <dthaluru@vmware.com> 4.2.0-16
- Disabling network renaming
* Sun Feb 14 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-15
- veth patch: don’t modify ip_summed
* Thu Feb 11 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-14
- Full tickless -> idle tickless + simple CPU time accounting
- SLUB -> SLAB
- Disable NUMA balancing
- Disable stack protector
- No build_forced no-CBs CPUs
- Disable Expert configuration mode
- Disable most of debug features from 'Kernel hacking'
* Mon Feb 08 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-13
- Double tcp_mem limits, patch is added.
* Wed Feb 03 2016 Anish Swaminathan <anishs@vmware.com>  4.2.0-12
- Fixes for CVE-2015-7990/6937 and CVE-2015-8660.
* Tue Jan 26 2016 Anish Swaminathan <anishs@vmware.com> 4.2.0-11
- Revert CONFIG_HZ=250
* Fri Jan 22 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-10
- Fix for CVE-2016-0728
* Wed Jan 13 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-9
- CONFIG_HZ=250
* Tue Jan 12 2016 Mahmoud Bassiouny <mbassiouny@vmware.com> 4.2.0-8
- Remove rootfstype from the kernel parameter.
* Mon Jan 04 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.2.0-7
- Disabled all the tracing options in kernel config.
- Disabled preempt.
- Disabled sched autogroup.
* Thu Dec 17 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.2.0-6
- Enabled kprobe for systemtap & disabled dynamic function tracing in config
* Fri Dec 11 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.2.0-5
- Added oprofile kernel driver sub-package.
* Fri Nov 13 2015 Mahmoud Bassiouny <mbassiouny@vmware.com> 4.2.0-4
- Change the linux image directory.
* Wed Nov 11 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.2.0-3
- Added the build essential files in the dev sub-package.
* Mon Nov 09 2015 Vinay Kulkarni <kulkarniv@vmware.com> 4.2.0-2
- Enable Geneve module support for generic kernel.
* Fri Oct 23 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.2.0-1
- Upgraded the generic linux kernel to version 4.2.0 & and updated timer handling to full tickless mode.
* Tue Sep 22 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.0.9-5
- Added driver support for frame buffer devices and ACPI
* Wed Sep 2 2015 Alexey Makhalov <amakhalov@vmware.com> 4.0.9-4
- Added mouse ps/2 module.
* Fri Aug 14 2015 Alexey Makhalov <amakhalov@vmware.com> 4.0.9-3
- Use photon.cfg as a symlink.
* Thu Aug 13 2015 Alexey Makhalov <amakhalov@vmware.com> 4.0.9-2
- Added environment file(photon.cfg) for grub.
* Wed Aug 12 2015 Sharath George <sharathg@vmware.com> 4.0.9-1
- Upgrading kernel version.
* Wed Aug 12 2015 Alexey Makhalov <amakhalov@vmware.com> 3.19.2-5
- Updated OVT to version 10.0.0.
- Rename -gpu-drivers to -drivers-gpu in accordance to directory structure.
- Added -sound package/
* Tue Aug 11 2015 Anish Swaminathan<anishs@vmware.com> 3.19.2-4
- Removed Requires dependencies.
* Fri Jul 24 2015 Harish Udaiya Kumar <hudaiyakumar@gmail.com> 3.19.2-3
- Updated the config file to include graphics drivers.
* Mon May 18 2015 Touseef Liaqat <tliaqat@vmware.com> 3.13.3-2
- Update according to UsrMove.
* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 3.13.3-1
- Initial build. First version
