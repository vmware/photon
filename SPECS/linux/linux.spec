%global security_hardening none
%global __cmake_in_source_build 0

# SBAT generation of "linux.photon" component
%define linux_photon_generation 1

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

%if 0%{?acvp_build}
%global fips 1
%endif

%ifarch aarch64
%define arch arm64
%define archdir arm64
%global fips 0
%endif

Summary:        Kernel
Name:           linux
Version:        6.1.60
Release:        2%{?acvp_build:.acvp}%{?kat_build:.kat}%{?dist}
License:        GPLv2
URL:            http://www.kernel.org/
Group:          System Environment/Kernel
Vendor:         VMware, Inc.
Distribution:   Photon

%define uname_r %{version}-%{release}
%define _modulesdir /lib/modules/%{uname_r}

Source0:        http://www.kernel.org/pub/linux/kernel/v6.x/linux-%{version}.tar.xz
%define sha512 linux=cef40235428a09e5f7807a8be83af9a5ab90e841049a04f9f851e69e602aeab5a50f523cae5d5928d345c11b728608eba7754b173be0c023c7ee564cfaf4b20a

Source1:        config_%{_arch}
Source2:        initramfs.trigger

%define ena_version 2.8.3
Source3:        https://github.com/amzn/amzn-drivers/archive/refs/tags/ena_linux_%{ena_version}.tar.gz
%define sha512 ena_linux=173435137b6fe47d110db376c4c3eff8da7a10803dde5f41f694d04e74319861c16398f257a1c917a4fc05477c86e6e7b42e6a63e2f42de7ea9166f77ba9b01d

%define efa_version 2.1.1
Source4:        https://github.com/amzn/amzn-drivers/archive/refs/tags/efa_linux_%{efa_version}.tar.gz
%define sha512 efa_linux=2ceb5a4011a6b5f69d0a389e3d6f188d29cb87373202b42fe6c1f29ac2a310d1180a9ffad3e362680b675edc8007850b541e477b918781ef406afc55ca0d1c6e

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

%define ice_version 1.11.14
Source13:       https://sourceforge.net/projects/e1000/files/ice%20stable/%{ice_version}/ice-%{ice_version}.tar.gz
%define sha512 ice=a2a6a498e553d41e4e6959a19cdb74f0ceff3a7dbcbf302818ad514fdc18e3d3b515242c88d55ef8a00c9d16925f0cd8579cb41b3b1c27ea6716ccd7e70fd847
%endif

%if 0%{?fips}
Source9:        check_fips_canister_struct_compatibility.inc

%define fips_canister_version 5.0.0-6.1.56-6%{?dist}-secure
Source16:       fips-canister-%{fips_canister_version}.tar.bz2
%define sha512 fips-canister=7e1dc80c5eecf2a8cf5e5fc964b5fa56dbcaff9d11a97393d0d57ab8f63ea343f0d164a4354d011c2dc946abd3fd6f772905f1a8e355b22ee318adcdd2fe6b26
%endif

Source18:       spec_install_post.inc
Source19:       %{name}-dracut-%{_arch}.conf
Source20:       photon_sb2020.pem

%ifarch x86_64
# Secure Boot
Source25:       linux-sbat.csv.in

%define jent_major_version 3.4.1
%define jent_ph_version 4
Source32: jitterentropy-%{jent_major_version}-%{jent_ph_version}.tar.bz2
%define sha512 jitterentropy=37a9380b14d5e56eb3a16b8e46649bc5182813aadb5ec627c31910e4cc622269dfd29359789cb4c13112182f4f8d3c084a6b9c576df06dae9689da44e4735dd2
Source33: jitterentropy_canister_wrapper.c
Source34: jitterentropy_canister_wrapper.h
Source35: jitterentropy_canister_wrapper_asm.S
%endif

# common [0..49]
Patch0: confdata-format-change-for-split-script.patch
Patch1: net-Double-tcp_mem-limits.patch
Patch2: SUNRPC-xs_bind-uses-ip_local_reserved_ports.patch
Patch3: 6.0-9p-transport-for-9p.patch
Patch4: 9p-trans_fd-extend-port-variable-to-u32.patch
Patch5: vsock-delay-detach-of-QP-with-outgoing-data-59.patch
# RDRAND-based RNG driver to enhance the kernel's entropy pool:
Patch6: 6.0-0001-hwrng-rdrand-Add-RNG-driver-based-on-x86-rdrand-inst.patch
Patch7: 0001-cgroup-v1-cgroup_stat-support.patch
Patch8: 6.0-Discard-.note.gnu.property-sections-in-generic-NOTES.patch

# Expose Photon kernel macros to identify kernel flavor and version
Patch9:  0001-kbuild-Makefile-Introduce-macros-to-distinguish-Phot.patch
Patch10: 0002-linux-Makefile-Add-kernel-flavor-info-to-the-generat.patch

# ttyXRUSB support
Patch11: usb-acm-exclude-exar-usb-serial-ports-nxt.patch
#HyperV patches
Patch12: vmbus-Don-t-spam-the-logs-with-unknown-GUIDs.patch

# TODO: Is CONFIG_HYPERV_VSOCKETS the same?
#Patchx: 0014-hv_sock-introduce-Hyper-V-Sockets.patch
Patch13: 6.1-0001-fork-add-sysctl-to-disallow-unprivileged-CLONE_NEWUS.patch
# Out-of-tree patches from AppArmor:
Patch14: 6.0-0001-apparmor-patch-to-provide-compatibility-with-v2.x-ne.patch
Patch15: 6.0-0002-apparmor-af_unix-mediation.patch

Patch16: Performance-over-security-model.patch
# Disable md5 algorithm for sctp if fips is enabled.
Patch18: 6.0-0001-disable-md5-algorithm-for-sctp-if-fips-is-enabled.patch

# VMware-specific patch to enable turbostat to work on ESXi
Patch19: 0001-tools-power-turbostat-Skip-some-CPUID-checks-if-runn.patch

# Allow PCI resets to be disabled from vfio_pci_core module
Patch21: 6.1-0001-drivers-vfio-pci-Add-kernel-parameter-to-allow-disab.patch
# Add PCI quirk to allow multiple devices under the same virtual PCI bridge
# to be put into separate IOMMU groups on ESXi.
Patch22: 0001-Add-PCI-quirk-for-VMware-PCIe-Root-Port.patch

%ifarch x86_64
# VMW: [50..59]
Patch55: 6.0-x86-vmware-Use-Efficient-and-Correct-ALTERNATIVEs-fo.patch
Patch56: 6.0-x86-vmware-Log-kmsg-dump-on-panic.patch
Patch57: 6.0-x86-vmware-Fix-steal-time-clock-under-SEV.patch

# Secure Boot and Kernel Lockdown
Patch58: 0001-kernel-lockdown-when-UEFI-secure-boot-enabled.patch
Patch59: 0002-Add-.sbat-section.patch
Patch60: 0003-Verify-SBAT-on-kexec.patch
%endif

# CVE: [100..129]
Patch100: 6.0-0003-apparmor-fix-use-after-free-in-sk_peer_label.patch
# Fix CVE-2017-1000252
Patch101: KVM-Don-t-accept-obviously-wrong-gsi-values-via-KVM_.patch
#Fix CVE-2023-28464
Patch102: 0001-Bluetooth-Fix-double-free-in-hci_conn_cleanup.patch

%ifarch aarch64
# aarch specific patches [200..219]
# Rpi of_configfs patches
Patch201: 0001-OF-DT-Overlay-configfs-interface.patch
Patch202: 0002-of-configfs-Use-of_overlay_fdt_apply-API-call.patch
Patch203: 0003-of-overlay-Correct-symbol-path-fixups.patch
# arm64 hypervisor detection and kmsg dumper
Patch205: 6.0-0001-x86-hyper-generalize-hypervisor-type-detection.patch
Patch206: 6.0-0002-arm64-Generic-hypervisor-type-detection-for-arm64.patch
Patch207: 6.0-0003-arm64-VMware-hypervisor-detection.patch
Patch208: 6.0-0004-arm64-kmsg-dumper-for-VMware-hypervisor.patch
Patch209: 6.0-0005-scsi-vmw_pvscsi-add-arm64-support.patch
Patch210: 6.0-0006-vmxnet3-build-only-for-x86-and-arm64.patch
Patch211: 6.0-0005-vmw_balloon-add-arm64-support.patch
Patch212: 6.0-0001-vmw_vmci-arm64-support-memory-ordering.patch
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
Patch503: 0001-FIPS-crypto-rng-Jitterentropy-RNG-as-the-only-RND-source.patch
# Patch to remove urandom usage in drbg and ecc modules
Patch504: 0003-FIPS-crypto-drbg-Jitterentropy-RNG-as-the-only-RND.patch

%ifarch x86_64
Patch505: 0001-changes-to-build-with-jitterentropy-v3.4.1.patch
%endif

%if 0%{?fips}
# FIPS canister usage patch
Patch508: 6.1.56-3-0001-FIPS-canister-binary-usage.patch
Patch509: 0001-scripts-kallsyms-Extra-kallsyms-parsing.patch
Patch510: FIPS-do-not-allow-not-certified-algos-in-fips-2.patch
%else
%if 0%{?kat_build}
Patch511: 0003-FIPS-broken-kattest.patch
%endif
%endif

%if 0%{?acvp_build:1}
#ACVP test harness patches.
#Need to be applied on top of FIPS canister usage patch to avoid HUNK failure
Patch512:       0001-crypto-AF_ALG-add-sign-verify-API.patch
Patch513:       0002-crypto-AF_ALG-add-setpubkey-setsockopt-call.patch
Patch514:       0003-crypto-AF_ALG-add-asymmetric-cipher.patch
Patch515:       0004-crypto-AF_ALG-add-DH-keygen-ssgen-API.patch
Patch516:       0005-crypto-AF_ALG-add-DH-param-ECDH-curve-setsockopt.patch
Patch517:       0006-crypto-AF_ALG-eliminate-code-duplication.patch
Patch518:       0007-crypto-AF_ALG-add-KPP-support.patch
Patch519:       0008-crypto-AF_ALG-add-ECC-support.patch
Patch520:       0009-kernels-net-Export-sock_getsockopt.patch
Patch521:       0010-DRBG-Fix-issues-with-DRBG.patch
Patch522:       0011-Added-jitterentropy-implementation-of-SHA3-256.patch
Patch523:       0012-jitterentropy-Support-for-sample-collection.patch
%endif

%ifarch x86_64
# SEV on VMware: [600..609]
Patch600: 0079-x86-sev-es-Disable-BIOS-ACPI-RSDP-probing-if-SEV-ES-.patch
Patch601: 0080-x86-boot-Enable-vmw-serial-port-via-Super-I-O.patch
Patch602: 0001-x86-boot-unconditional-preserve-CR4.MCE.patch
# TODO: Review: Patch602: 0081-x86-sev-es-Disable-use-of-WP-via-PAT-for-__sme_early.patch
%endif

# Patches for efa [1400..1409]
Patch1400: Fix-efa-cmake-to-build-from-local-directory.patch

%ifarch x86_64
# Patches for i40e v2.22.18 driver [1500..1509]
Patch1500: i40e-v2.22.18-Add-support-for-gettimex64-interface.patch
Patch1501: i40e-v2.22.18-i40e-Make-i40e-driver-honor-default-and-user-defined.patch

# Patches for iavf v4.8.2 driver [1510..1519]
Patch1511: iavf-Makefile-added-alias-for-i40evf.patch

# Patches for ice v1.11.14 driver [1520..1529]
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
BuildRequires:  python3-setuptools
BuildRequires:  cmake
BuildRequires:  bison
BuildRequires:  dwarves-devel

%ifarch x86_64
BuildRequires:  pciutils-devel
BuildRequires:  libcap-devel
%endif

%if 0%{?fips}
BuildRequires:  gdb
%endif

Requires: kmod
Requires: filesystem
Requires(pre):    (coreutils or coreutils-selinux)
Requires(preun):  (coreutils or coreutils-selinux)
Requires(post):   (coreutils or coreutils-selinux)
Requires(postun): (coreutils or coreutils-selinux)

Obsoletes:  linux-aws

%description
The Linux package contains the Linux kernel.
# Enable post FIPS certification
%if 0
This kernel is FIPS certified.
%endif

%package devel
Summary:        Kernel Dev
Group:          System Environment/Kernel
Requires:       %{name} = %{version}-%{release}
Requires:       python3 gawk
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

%package tools
Summary:        This package contains the 'perf' performance analysis tools for Linux kernel
Group:          System/Tools
Requires:       (%{name} = %{version} or linux-esx = %{version} or linux-rt = %{version})
Requires:       audit elfutils-libelf binutils-libs
Requires:       xz-libs
Requires:       slang
Requires:       python3
Requires:       traceevent-plugins
%ifarch x86_64
Requires:       pciutils
%endif
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
# Using autosetup is not feasible
%setup -q -n linux-%{version}
# Using autosetup is not feasible
%setup -q -T -D -b 3 -n linux-%{version}
# Using autosetup is not feasible
%setup -q -T -D -b 4 -n linux-%{version}
%ifarch x86_64
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

# common
%autopatch -p1 -m0 -M49

%ifarch x86_64
# VMW x86
%autopatch -p1 -m50 -M60
%endif

# CVE
%autopatch -p1 -m100 -M129

%ifarch aarch64
# aarch64 patches
%autopatch -p1 -m200 -M219
%endif

%ifarch x86_64
# AWS x86
%autopatch -p1 -m300 -M339
%endif

# crypto
%autopatch -p1 -m500 -M504

%ifarch x86_64
%autopatch -p1 -m505 -M505
%endif

%if 0%{?fips}
%autopatch -p1 -m508 -M510
%endif
%if 0%{?kat_build}
%autopatch -p1 -m511 -M511
%endif

%if 0%{?acvp_build:1}
#ACVP test harness patches.
#Need to be applied on top of FIPS canister usage patch to avoid HUNK failure
%autopatch -p1 -m512 -M523
%endif

%ifarch x86_64
# SEV on VMware
%autopatch -p1 -m600 -M609
%endif

# Patches for efa driver
pushd ../amzn-drivers-efa_linux_%{efa_version}
%autopatch -p1 -m1400 -M1409
popd

%ifarch x86_64
# Patches for i40e driver
pushd ../i40e-%{i40e_version}
%autopatch -p1 -m1500 -M1509
popd

# Patches for iavf driver
pushd ../iavf-%{iavf_version}
%autopatch -p1 -m1510 -M1519
popd

# Patches for ice driver
pushd ../ice-%{ice_version}
%autopatch -p1 -m1520 -M1529
popd
%endif

%ifarch x86_64
cp -r ../jitterentropy-%{jent_major_version}-%{jent_ph_version}/ \
      crypto/jitterentropy-%{jent_major_version}/
cp %{SOURCE33} crypto/jitterentropy-%{jent_major_version}/
cp %{SOURCE34} crypto/jitterentropy-%{jent_major_version}/
cp %{SOURCE35} crypto/jitterentropy-%{jent_major_version}/
%endif

make %{?_smp_mflags} mrproper
cp %{SOURCE1} .config

%if 0%{?acvp_build:1}
#ACVP test harness changes in kernel configs.
sed -i 's/# CONFIG_CRYPTO_USER is not set/CONFIG_CRYPTO_USER=y/' .config
sed -i 's/# CONFIG_CRYPTO_DH is not set/CONFIG_CRYPTO_DH=y/' .config
sed -i 's/CONFIG_CRYPTO_USER_API=m/CONFIG_CRYPTO_USER_API=y/' .config
sed -i 's/CONFIG_CRYPTO_USER_API_HASH=m/CONFIG_CRYPTO_USER_API_HASH=y/' .config
sed -i 's/CONFIG_CRYPTO_USER_API_SKCIPHER=m/CONFIG_CRYPTO_USER_API_SKCIPHER=y/' .config
sed -i 's/CONFIG_CRYPTO_USER_API_RNG=m/CONFIG_CRYPTO_USER_API_RNG=y/' .config
sed -i 's/# CONFIG_CRYPTO_USER_API_RNG_CAVP is not set/CONFIG_CRYPTO_USER_API_RNG_CAVP=y/' .config
sed -i 's/# CONFIG_CRYPTO_USER_API_AEAD is not set/CONFIG_CRYPTO_USER_API_AEAD=y/' .config
sed -i '/CONFIG_CRYPTO_USER_API_ENABLE_OBSOLETE/ a # CONFIG_CRYPTO_STATS is not set' .config
sed -i '/CONFIG_CRYPTO_STATS/ a CONFIG_CRYPTO_USER_API_AKCIPHER=y' .config
sed -i '/CONFIG_CRYPTO_USER_API_AKCIPHER/ a CONFIG_CRYPTO_USER_API_KPP=y' .config
sed -i '/CONFIG_CRYPTO_USER_API_KPP=y/ a CONFIG_CRYPTO_USER_API_ECC=y' .config
sed -i '/CONFIG_CRYPTO_DH=y/ a # CONFIG_CRYPTO_DH_RFC7919_GROUPS is not set' .config
sed -i '/# end of Userspace interface/ { N; d; }' .config
sed -i '/# CONFIG_CRYPTO_STATS is not set/ a # end of Userspace interface' .config
sed -i '/# end of Userspace interface/{G;}' .config
%endif

cp %{SOURCE20} photon_sb2020.pem
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

%if 0%{?kat_build}
sed -i '/CONFIG_CRYPTO_SELF_TEST=y/a CONFIG_CRYPTO_BROKEN_KAT=y' .config
%endif

%ifarch x86_64
sed -e "s,@@NAME@@,%{name},g" \
    -e "s,@@VERSION_RELEASE@@,%{version}-%{release},g" \
    -e "s,@@LINUX_PH_GEN@@,%{linux_photon_generation},g" \
    %{SOURCE25} > linux-sbat.csv
%endif

%include %{SOURCE7}

# Set/add CONFIG_CROSS_COMPILE= if needed
if [ %{_host} != %{_build} ]; then
grep -q CONFIG_CROSS_COMPILE= .config && sed -i '/^CONFIG_CROSS_COMPILE=/c\CONFIG_CROSS_COMPILE="%{_host}-"' .config || \
  echo 'CONFIG_CROSS_COMPILE="%{_host}-"' >> .config
fi

%build
make %{?_smp_mflags} V=1 KBUILD_BUILD_VERSION="1-photon" \
    KBUILD_BUILD_HOST="photon" ARCH=%{arch} %{?_smp_mflags}

%if 0%{?fips}
%include %{SOURCE9}
%endif

%ifarch aarch64
ARCH_FLAGS="EXTRA_CFLAGS=-Wno-error=format-overflow"
%endif
ARCH_FLAGS="EXTRA_CFLAGS=-Wno-error=deprecated-declarations"
make %{?_smp_mflags} ARCH=%{arch} -C tools perf PYTHON=python3 $ARCH_FLAGS
# verify perf has no dependency on libunwind
tools/perf/perf -vv | grep libunwind | grep OFF
tools/perf/perf -vv | grep dwarf | grep on

%ifarch x86_64
#build turbostat and cpupower
make %{?_smp_mflags} ARCH=%{arch} -C tools turbostat cpupower PYTHON=python3
%endif

# build ENA module
bldroot="${PWD}"
pushd ../amzn-drivers-ena_linux_%{ena_version}/kernel/linux/ena
make %{?_smp_mflags} -C ${bldroot} M="${PWD}" V=1 modules %{?_smp_mflags}
popd

# build EFA module
bldroot="${PWD}"
pushd ../amzn-drivers-efa_linux_%{efa_version}/kernel/linux/efa
mkdir build
cd build
%cmake -DKERNEL_DIR=${bldroot} ..
%cmake_build
popd

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
make %{?_smp_mflags} ARCH=%{arch} INSTALL_MOD_PATH=%{buildroot} modules_install

# install ENA module
bldroot="${PWD}"
pushd ../amzn-drivers-ena_linux_%{ena_version}/kernel/linux/ena
make %{?_smp_mflags} -C ${bldroot} M="${PWD}" INSTALL_MOD_PATH=%{buildroot} modules_install
popd

# install EFA module
bldroot="${PWD}"
pushd ../amzn-drivers-efa_linux_%{efa_version}/kernel/linux/efa/build/src
make %{?_smp_mflags} -C ${bldroot} M="${PWD}" INSTALL_MOD_PATH=%{buildroot} modules_install
popd

%ifarch x86_64
# install i40e module
pushd ../i40e-%{i40e_version}
make %{?_smp_mflags} -C src KSRC=${bldroot} INSTALL_MOD_PATH=%{buildroot} \
    INSTALL_MOD_DIR=extra MANDIR=%{_mandir} modules_install mandocs_install
popd

# install iavf module
pushd ../iavf-%{iavf_version}
make %{?_smp_mflags} -C src KSRC=${bldroot} INSTALL_MOD_PATH=%{buildroot} \
    INSTALL_MOD_DIR=extra MANDIR=%{_mandir} modules_install mandocs_install
popd

# install ice module
pushd ../ice-%{ice_version}
make %{?_smp_mflags} -C src KSRC=${bldroot} INSTALL_MOD_PATH=%{buildroot} \
    INSTALL_MOD_DIR=extra MANDIR=%{_mandir} modules_install mandocs_install
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

# Register myself to initramfs
mkdir -p %{buildroot}%{_localstatedir}/lib/initramfs/kernel

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
cp -p %{SOURCE19} %{buildroot}%{_modulesdir}/dracut.conf.d/%{name}.conf

%include %{SOURCE2}
%include %{SOURCE6}
%include %{SOURCE18}

%post
/sbin/depmod -a %{uname_r}
ln -sf linux-%{uname_r}.cfg /boot/photon.cfg

%post drivers-gpu
/sbin/depmod -a %{uname_r}

%post drivers-sound
/sbin/depmod -a %{uname_r}

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
%{_modulesdir}/kernel/drivers/gpu

%files drivers-sound
%defattr(-,root,root)
%{_modulesdir}/kernel/sound
%ifarch aarch64
%{_modulesdir}/kernel/drivers/staging/vc04_services/bcm2835-audio
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
%{_includedir}/perf/*
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
* Fri Oct 27 2023 Srinidhi Rao <srinidhir@vmware.com> 6.1.60-2
- Jitterentropy sample collection support in ACVP Build.
* Fri Oct 27 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 6.1.60-1
- Upgrade to 6.1.60
* Thu Oct 26 2023 Alexey Makhalov <amakhalov@vmware.com> 6.1.56-9
- Add .sbat section for bzImage
- Introduce SBAT verificaion in addition to signature on kexec
* Thu Oct 26 2023 Srish Srinivasan <ssrish@vmware.com> 6.1.56-8
- Upgrade canister to 5.0.0-6.1.56-6
* Tue Oct 24 2023 Srish Srinivasan <ssrish@vmware.com> 6.1.56-7
- Added cts to crypto self-tests
- Removed rsa(pkcs1pad, sha256), rsa(pkcs1pad, sha512),
  cbc, and ctr from crypto self-tests
- Added ECC pubkey generation and verification success messages
* Wed Oct 18 2023 Keerthana K <keerthanak@vmware.com> 6.1.56-6
- Modified ecdh-nist-p384 vector to generate ECC keypair
* Tue Oct 17 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 6.1.56-5
- Upgrade canister to 5.0.0-6.1.56-3
* Fri Oct 13 2023 Srish Srinivasan <ssrish@vmware.com> 6.1.56-4
- Adding support for ACVP build
- Added jitterentropy implementation of SHA3-256
* Tue Oct 10 2023 Srish Srinivasan <ssrish@vmware.com> 6.1.56-3
- Add missing self-test vector for ecdh-nist-p384 with genkey
* Mon Oct 09 2023 Srinidhi Rao <srinidhir@vmware.com> 6.1.56-2
- Jitterentropy wrapper changes.
* Fri Oct 06 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 6.1.56-1
- Upgrade to 6.1.56
* Tue Oct 03 2023 Kuntal Nayak <nkunal@vmware.com> 6.1.53-7
- Kconfig to lockdown kernel in UEFI Secure Boot
* Sun Oct 01 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 6.1.53-6
- Fix for CVE-2023-42754
* Fri Sep 29 2023 Keerthana K <keerthanak@vmware.com> 6.1.53-5
- Enable fips and update canister binary version 5.0.0-6.1.53-4
- Removed jent_lock struct from ignore list of check_fips_canister
* Tue Sep 26 2023 Keerthana K <keerthanak@vmware.com> 6.1.53-4
- Add pkcs1pad test vectors in crytpo_self_test module
* Mon Sep 25 2023 Keerthana K <keerthanak@vmware.com> 6.1.53-3
- Fix CVE-2023-42756
* Mon Sep 25 2023 Keerthana K <keerthanak@vmware.com> 6.1.53-2
- Fix for CVE-2023-42755
* Mon Sep 18 2023 Roye Eshed <eshedr@vmware.com> 6.1.53-1
- Update to version 6.1.53
* Fri Sep 15 2023 Ajay Kaher <akaher@vmware.com> 6.1.45-8
- Fix: net: roundup issue in kmalloc_reserve()
* Mon Sep 11 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 6.1.45-7
- Move all prep to %prep section
* Mon Sep 11 2023 Srish Srinivasan <ssrish@vmware.com> 6.1.45-6
- LKCM 5.0 specific changes to crypto self-tests and tcrypt
* Fri Sep 08 2023 Keerthana K <keerthanak@vmware.com> 6.1.45-5
- Build with jitterentropy v3.4.1
* Fri Sep 08 2023 Keerthana K <keerthanak@vmware.com> 6.1.45-4
- Update fips_canister version 6.1.45-4
* Tue Sep 05 2023 Ankit Jain <ankitja@vmware.com> 6.1.45-3
- Fix for CVE-2023-28464
* Sat Sep 02 2023 Guruswamy Basavaiah <bguruswamy@vmware.com> 6.1.45-2
- Cherry pick performance over security option for RETBleed (pos=1)
- patch from Photon 4.0
* Mon Aug 14 2023 Ajay Kaher <akaher@vmware.com> 6.1.45-1
- Update to version 6.1.45
* Wed Aug 09 2023 Srish Srinivasan <ssrish@vmware.com> 6.1.41-4
- Enable CONFIG_DEBUG_INFO_BTF=y
* Wed Aug 02 2023 Kuntal Nayak <nkuntal@vmware.com> 6.1.41-3
- Enable Kconfig CONFIG_KEXEC_FILE for kexec signature verify
* Mon Jul 31 2023 Ajay Kaher <akaher@vmware.com> 6.1.41-2
- Fix: unconditional preserve CR4.MCE
* Thu Jul 20 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 6.1.41-1
- Update to version 6.1.41
* Mon Jul 17 2023 Keerthana K <keerthanak@vmware.com> 6.1.37-2
- Use canister version 5.0.0-6.1.37-2
* Tue Jul 04 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 6.1.37-1
- Update to version 6.1.37
* Tue Jun 06 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 6.1.32-1
- Update to version 6.1.32
* Tue May 23 2023 Guruswamy Basavaiah <bguruswamy@vmware.com> 6.1.28-2
- disable kconfig CONFIG_RAID6_PQ_BENCHMARK
* Tue May 16 2023 Ankit Jain <ankitja@vmware.com> 6.1.28-1
- Update to version 6.1.28
* Fri May 12 2023 Ajay Kaher <akaher@vmware.com> 6.1.10-13
- perf: remove libunwind dependency
- Remove rpi fan driver patch
* Tue Apr 25 2023 Shreenidhi Shedi <sshedi@vmware.com> 6.1.10-12
- Remove dracut & initramfs from requires
* Thu Apr 13 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 6.1.10-11
- Use canister version 5.0.0-6.1.10-10
* Thu Apr 06 2023 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 6.1.10-10
- Expose Photon kernel macros to simplify building out-of-tree drivers.
* Thu Mar 30 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 6.1.10-9
- Update drivers
- iavf: 4.8.2
- ice: 1.11.14
- i40e: 2.22.18
* Fri Mar 24 2023 Keerthana K <keerthanak@vmware.com> 6.1.10-8
- Disable FIPS canister binary usage
* Tue Mar 21 2023 Shreenidhi Shedi <sshedi@vmware.com> 6.1.10-7
- Fix initramfs trigger
* Thu Mar 16 2023 Keerthana K <keerthanak@vmware.com> 6.1.10-6
- Enable FIPS canister binary usage
* Tue Mar 07 2023 Him Kalyan Bordoloi <bordoloih@vmware.com> 6.1.10-5
- Add ENA and EFA drivers to ARM build
* Tue Mar 07 2023 Shreenidhi Shedi <sshedi@vmware.com> 6.1.10-4
- Fix initrd driver list for aarch64
* Thu Mar 02 2023 Shreenidhi Shedi <sshedi@vmware.com> 6.1.10-3
- Fix initrd generation logic
- Add dracut, initramfs to requires
* Fri Feb 24 2023 Ankit Jain <ankitja@vmware.com> 6.1.10-2
- Exclude iavf.conf
* Wed Feb 22 2023 Bo Gan <ganb@vmware.com> 6.1.10-1
- Update to 6.1.10
* Tue Feb 21 2023 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 6.0.7-11
- Enable turbostat to work in the guest on VMware hypervisor.
* Tue Feb 21 2023 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 6.0.7-10
- Update i40e driver to v2.19.3 to prevent kernel warnings
* Mon Feb 20 2023 Ajay Kaher <akaher@vmware.com> 6.0.7-9
- exclude man dir from linux-tools
* Thu Feb 02 2023 Shreenidhi Shedi <sshedi@vmware.com> 6.0.7-8
- Fix requires
* Wed Jan 25 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 6.0.7-7
- Enable CONFIG_PCI_PF_STUB
* Tue Jan 17 2023 Him Kalyan Bordoloi <bordoloih@vmware.com> 6.0.7-6
- Depricate linux-aws kernel flavor
* Fri Jan 13 2023 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 6.0.7-5
- Fix IRQ affinities of i40e, iavf and ice drivers
* Mon Jan 09 2023 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 6.0.7-4
- Update Intel drivers i40e to v2.16.11, iavf to v4.5.3 and ice to v1.9.11
* Fri Jan 06 2023 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 6.0.7-3
- Port patch to allow disabling PCI resets from vfio_pci driver to 6.0
- Move the module parameter disable_resets from vfio_pci to
- vfio_pci_core module, to make it work with kernel 6.0.
* Fri Jan 06 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 6.0.7-2
- Bump up due to change in elfutils
* Tue Dec 20 2022 Bo Gan <ganb@vmware.com> 6.0.7-1
- Update to 6.0.7
- Enable PREEMPT_DYNAMIC
- Enable extra Dell platform drivers.
- Enable security configs, RANDOMIZE_KSTACK_OFFSET and others.
- Change from SLAB to SLUB
- aarch64/config: match x86 on non-arch specific setting.
- aarch64/config: don't set CAVIUM_ERRATUM_23154 and wait for ESX support
* Mon Dec 19 2022 Dweep Advani <dadvani@vmware.com> 5.10.142-5
- Ignore warnings to keep building tools
* Mon Oct 31 2022 Prashant S Chauhan <psinghchauha@vmware.com> 5.10.142-4
- Dont throw error for supported deprecated modules of py311
* Thu Oct 20 2022 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 5.10.142-3
- Fix build with latest toolchain
* Wed Sep 28 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.142-2
- Replace rpm macro 'name' with 'linux' to be consistent with other flavors.
* Wed Sep 28 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.142-1
- Update to version 5.10.142
* Tue Sep 27 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.132-1
- Update to version 5.10.132
* Tue Sep 27 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.118-10
- Backport fixes for CVE-2022-0500
* Tue Sep 27 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.118-9
- Fix for CVE-2022-2585, CVE-2022-2586 and CVE-2022-2588
* Tue Sep 27 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.118-8
- Update iavf driver to v4.4.2
- Update ice driver to v1.8.3
* Mon Sep 26 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.118-7
- .config: enable CONFIG_NET_ACT_SIMP
* Mon Sep 26 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.118-6
- .config: enable CONFIG_X86_CPU_RESCTRL
* Fri Sep 23 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.118-5
- Enable cgroup v1 stats
- .config: enable PERCPU_STATS
* Fri Sep 23 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.118-4
- Avoid TSC recalibration
* Fri Sep 23 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.118-3
- Fix for CVE-2022-21505
* Fri Sep 23 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.118-2
- VMCI patches & configs
* Fri Sep 23 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.118-1
- Update to version 5.10.118
* Fri Sep 23 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.109-4
- Fix for CVE-2022-1966, CVE-2022-1972
* Thu Sep 22 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.109-3
- Fix for CVE-2022-21499
* Thu Sep 22 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.109-2
- Fix for CVE-2022-29582
* Wed Sep 21 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.109-1
- Update to version 5.10.109
* Tue Sep 20 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.103-4
- Fix for CVE-2022-1016
* Tue Sep 20 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.103-3
- Fix SEV and Hypercall alternative inst. patches
* Tue Sep 20 2022 Shreenidhi Shedi <sshedi@vmware.com> 5.10.103-2
- Add bpftool subpackage
* Thu Sep 15 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.103-1
- Update to version 5.10.103
* Wed Sep 14 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.93-5
- Fix for CVE-2022-0435
* Wed Sep 14 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.93-4
- Fix for CVE-2022-0492
* Wed Sep 14 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.93-3
- Fix for CVE-2022-22942
* Wed Sep 14 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.93-2
- Fix CVE-2022-0330
* Wed Sep 14 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.93-1
- Update to version 5.10.93
* Wed Sep 14 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.83-5
- Fix CVE-2021-4155 and CVE-2021-4204
* Wed Sep 14 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.83-4
- Enable crypto related configs in aarch64 similar to x86_64
- crypto_self_test and broken kattest module enhancements
* Tue Sep 13 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.83-3
- mm: fix percpu allocation for memoryless nodes
- pvscsi: fix disk detection issue
* Tue Sep 13 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.83-2
- remove tmem, lvm in add-drivers list
- lvm drivers are built as part of dm-mod
- tmem module no longer exists
* Mon Sep 12 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.83-1
- Update to version 5.10.83
* Mon Sep 12 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.78-14
- .config: Enable eBPF net packet filtering support.
* Mon Aug 08 2022 Shreenidhi Shedi <sshedi@vmware.com> 5.10.78-13
- Scriptlets fixes and improvements
* Wed Jul 20 2022 Tejaswini Jayaramaiah <jtejaswini@vmware.com> 5.10.78-12
- Enable CONFIG_CGROUP_BPF in config to run containers with cgroup v2
* Wed Jul 13 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.78-11
- Add PCI quirk to allow multiple devices under the same virtual
- PCI bridge to be put into separate IOMMU groups.
* Tue Jul 12 2022 Sharan Turlapati <sturlpati@vmware.com> 5.10.78-10
- Allow PCI resets to be disabled from vfio_pci
* Wed Jun 29 2022 Keerthana K <keerthanak@vmware.com> 5.10.78-9
- Reduce FIPS canister memory footprint by disabling CONFIG_KALLSYMS_ALL
- Add only fips_canister-kallsyms to vmlinux instead of all symbols
* Fri Jun 24 2022 Shreenidhi Shedi <sshedi@vmware.com> 5.10.78-8
- Fix debug_package macro usage while adding vmlinux to debuginfo rpm
* Tue Jun 14 2022 Brennan Lamoreaux <blamoreaux@vmware.com> 5.10.78-7
- Enable CONFIG_LIVEPATCH, which requires enabling ftrace, and related.
* Tue Apr 05 2022 Shreenidhi Shedi <sshedi@vmware.com> 5.10.78-6
- Enable CONFIG_EXT2_FS_XATTR & related parameters
* Tue Jan 25 2022 Alexey Makhalov <amakhalov@vmware.com> 5.10.78-5
- .config: enable squashfs module, enable crypto user api rng.
* Thu Nov 25 2021 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 5.10.78-4
- Disable md5 algorithm for sctp if fips is enabled.
* Fri Nov 19 2021 Keerthana K <keerthanak@vmware.com> 5.10.78-3
- Add arm64 hypervisor detection and kmsg dumper
* Thu Nov 11 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 5.10.78-2
- compile with openssl 3.0.0
* Mon Nov 08 2021 Vikash Bansal <bvikas@vmware.com> 5.10.78-1
- Update to version 5.10.78
* Thu Oct 28 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.75-1
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
