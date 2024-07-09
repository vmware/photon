%global security_hardening none

%ifarch x86_64
%define arch x86_64
%define archdir x86
%endif

# Set this flag to 0 to build without canister
%global fips 1

# If kat_build is enabled, canister is not used.
%if 0%{?kat_build}
%global fips 0
%endif

Summary:        Kernel
Name:           linux-aws
Version:        5.10.219
Release:        3%{?dist}
License:        GPLv2
URL:            http://www.kernel.org
Group:          System Environment/Kernel
Vendor:         VMware, Inc.
Distribution:   Photon

%define uname_r %{version}-%{release}-aws
%define _modulesdir /lib/modules/%{uname_r}

Source0:    http://www.kernel.org/pub/linux/kernel/v5.x/linux-%{version}.tar.xz
%define sha512 linux=e62d8262654054c3a05e5e0a62dcedc51499fcfa078a4c19cb52c6dca82a83125152b83aa9bc0fdd448f563fbd71409305402d1a12cc8c7a038b8bed76ac482e
Source1:    config-aws
Source2:    initramfs.trigger
# contains pre, postun, filetriggerun tasks
Source3:    scriptlets.inc
Source4:    check_for_config_applicability.inc

%if 0%{?fips}
Source9:        check_fips_canister_struct_compatibility.inc

%define fips_canister_version 4.0.1-5.10.21-3-secure
Source16:       fips-canister-%{fips_canister_version}.tar.bz2
%define sha512 fips-canister=1d3b88088a23f7d6e21d14b1e1d29496ea9e38c750d8a01df29e1343034f74b0f3801d1f72c51a3d27e9c51113c808e6a7aa035cb66c5c9b184ef8c4ed06f42a

Source18:       fips_canister-kallsyms
Source19:       FIPS-do-not-allow-not-certified-algos-in-fips-2.patch
Source20:       Add-alg_request_report-cmdline.patch
Source21:       0001-LKCM-4.0.1-binary-patching-to-fix-jent-on-AMD-EPYC.patch
%endif

Source22:       spec_install_post.inc
Source23:       %{name}-dracut.conf

# common
Patch0: net-Double-tcp_mem-limits.patch
Patch1: SUNRPC-Do-not-reuse-srcport-for-TIME_WAIT-socket.patch
Patch2: SUNRPC-xs_bind-uses-ip_local_reserved_ports.patch
Patch3: 9p-transport-for-9p.patch
Patch4: vsock-delay-detach-of-QP-with-outgoing-data-59.patch
# RDRAND-based RNG driver to enhance the kernel's entropy pool:
Patch5: hwrng-rdrand-Add-RNG-driver-based-on-x86-rdrand-inst.patch

#HyperV patches
Patch6: vmbus-Don-t-spam-the-logs-with-unknown-GUIDs.patch

# TODO: Is CONFIG_HYPERV_VSOCKETS the same?
#Patchx: 0014-hv_sock-introduce-Hyper-V-Sockets.patch
Patch7: fork-add-sysctl-to-disallow-unprivileged-CLONE_NEWUSER-by.patch
# Out-of-tree patches from AppArmor:
Patch8: apparmor-patch-to-provide-compatibility-with-v2.x-ne.patch
Patch9: apparmor-af_unix-mediation.patch
Patch10: 0001-cgroup-v1-cgroup_stat-support.patch

Patch11: Performance-over-security-model.patch

# Revert crypto api workqueue
Patch12: 0001-Revert-crypto-api-Use-work-queue-in-crypto_destroy_i.patch

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
Patch45: 0001-kbuild-simplify-access-to-the-kernel-s-version.patch
Patch46: 0002-kbuild-replace-if-A-A-B-with-or-A-B.patch
Patch47: 0003-kbuild-Makefile-Introduce-macros-to-distinguish-Phot.patch
Patch48: 0004-linux-aws-Makefile-Add-kernel-flavor-info-to-the-gen.patch

# VMW: [55..65]
Patch55: x86-vmware-Use-Efficient-and-Correct-ALTERNATIVEs-fo-510.patch
Patch56: x86-vmware-Log-kmsg-dump-on-panic-510.patch
Patch57: 0001-x86-vmware-avoid-TSC-recalibration.patch

# Disable md5 algorithm for sctp if fips is enabled.
Patch58: 0001-disable-md5-algorithm-for-sctp-if-fips-is-enabled.patch

#Kernel lockdown
Patch59: 0001-kernel-lockdown-when-UEFI-secure-boot-enabled.patch

# CVE: [100..300]
Patch100: apparmor-fix-use-after-free-in-sk_peer_label.patch
# Fix CVE-2017-1000252
Patch101: KVM-Don-t-accept-obviously-wrong-gsi-values-via-KVM_.patch
# Fix for CVE-2019-12379
Patch102: consolemap-Fix-a-memory-leaking-bug-in-drivers-tty-v.patch

# Fix for CVE-2022-48666
Patch103: 0001-scsi-core-Fix-a-use-after-free.patch

# Fix for CVE-2021-4204
Patch105: 0002-bpf-Disallow-unprivileged-bpf-by-default.patch

# Fix for CVE-2022-3522
Patch107: 0001-mm_hugetlb_handle_pte_markers_in_page_faults.patch
Patch108: 0002-mm_hugetlb_fix_race_condition_of_uffd_missing_minor_handling.patch
Patch109: 0003-mm_hugetlb_use_hugetlb_pte_stable_in_migration_race_check.patch

# Fix for CVE-2022-0500
Patch115: 0001-bpf-Introduce-composable-reg-ret-and-arg-types.patch
Patch116: 0002-bpf-Replace-ARG_XXX_OR_NULL-with-ARG_XXX-PTR_MAYBE_N.patch
Patch117: 0003-bpf-Replace-RET_XXX_OR_NULL-with-RET_XXX-PTR_MAYBE_N.patch
Patch118: 0004-bpf-Extract-nullable-reg-type-conversion-into-a-help.patch
Patch119: 0005-bpf-Replace-PTR_TO_XXX_OR_NULL-with-PTR_TO_XXX-PTR_M.patch
Patch120: 0006-bpf-Introduce-MEM_RDONLY-flag.patch
Patch121: 0007-bpf-Make-per_cpu_ptr-return-rdonly-PTR_TO_MEM.patch
Patch122: 0008-bpf-Add-MEM_RDONLY-for-helper-args-that-are-pointers.patch

# Fix for CVE-2022-3524 and CVE-2022-3567
Patch123: 0001-ipv6-annotate-some-data-races-around-sk-sk_prot.patch
Patch127: 0005-ipv6-Fix-data-races-around-sk-sk_prot.patch
Patch128: 0006-tcp-Fix-data-races-around-icsk-icsk_af_ops.patch

#Fix for CVE-2022-43945
Patch131: 0001-NFSD-Cap-rsize_bop-result-based-on-send-buffer-size.patch
Patch132: 0002-NFSD-Protect-against-send-buffer-overflow-in-NFSv3-R.patch
Patch133: 0003-NFSD-Protect-against-send-buffer-overflow-in-NFSv2-R.patch
Patch134: 0004-NFSD-Protect-against-send-buffer-overflow-in-NFSv3-R.patch

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
Patch142: 0001-md-raid5-fix-atomicity-violation-in-raid5_cache_coun.patch

# Fix CVE-2024-26584
Patch144: 0001-tls-rx-simplify-async-wait.patch
Patch145: 0001-net-tls-factor-out-tls_-crypt_async_wait.patch
Patch146: 0001-net-tls-handle-backlogging-of-crypto-requests.patch

# Fix CVE-2023-1192
Patch151: 0001-cifs-Fix-UAF-in-cifs_demultiplex_thread.patch
# Fix CVE-2024-26583
Patch152: 0001-tls-fix-race-between-async-notify-and-socket-close.patch

# Fix CVE-2024-26585
Patch153: 0001-tls-fix-race-between-tx-work-scheduling-and-socket-c.patch

# Fix CVE-2024-26589
Patch154: 0001-bpf-Reject-variable-offset-alu-on-PTR_TO_FLOW_KEYS.patch

# Fix CVE-2024-26904
Patch155: 0001-btrfs-fix-data-race-at-btrfs_use_block_rsv.patch

# Fix CVE-2024-36901
Patch156: 0001-ipv6-annotate-data-races-around-cnf.disable_ipv6.pat.patch
Patch157: 0001-ipv6-prevent-NULL-dereference-in-ip6_output.patch

#Amazon AWS
Patch301: 0002-bump-the-default-TTL-to-255.patch
Patch302: 0003-bump-default-tcp_wmem-from-16KB-to-20KB.patch
Patch303: 0005-drivers-introduce-AMAZON_DRIVER_UPDATES.patch
Patch304: 0006-drivers-amazon-add-network-device-drivers-support.patch
Patch305: 0007-drivers-amazon-introduce-AMAZON_ENA_ETHERNET.patch
Patch306: 0008-Importing-Amazon-ENA-driver-1.5.0-into-amazon-4.14.y.patch
Patch307: 0009-xen-manage-keep-track-of-the-on-going-suspend-mode.patch
Patch308: 0010-xen-manage-introduce-helper-function-to-know-the-on-.patch
Patch309: 0011-xenbus-add-freeze-thaw-restore-callbacks-support.patch
Patch310: 0012-x86-xen-Introduce-new-function-to-map-HYPERVISOR_sha.patch
Patch311: 0013-x86-xen-add-system-core-suspend-and-resume-callbacks.patch
Patch312: 0014-xen-blkfront-add-callbacks-for-PM-suspend-and-hibern.patch
Patch313: 0015-xen-netfront-add-callbacks-for-PM-suspend-and-hibern.patch
Patch314: 0016-xen-time-introduce-xen_-save-restore-_steal_clock.patch
Patch315: 0017-x86-xen-save-and-restore-steal-clock.patch
Patch316: 0018-xen-events-add-xen_shutdown_pirqs-helper-function.patch
Patch317: 0019-x86-xen-close-event-channels-for-PIRQs-in-system-cor.patch
Patch318: 0020-PM-hibernate-update-the-resume-offset-on-SNAPSHOT_SE.patch
Patch319: 0021-Not-for-upstream-PM-hibernate-Speed-up-hibernation-b.patch
Patch320: 0022-xen-blkfront-add-persistent_grants-parameter.patch
Patch321: 0023-Revert-xen-dont-fiddle-with-event-channel-masking-in.patch
Patch322: 0024-xen-blkfront-Fixed-blkfront_restore-to-remove-a-call.patch
Patch323: 0025-x86-tsc-avoid-system-instability-in-hibernation.patch
Patch324: 0026-block-xen-blkfront-consider-new-dom0-features-on-res.patch
Patch325: 0028-xen-restore-pirqs-on-resume-from-hibernation.patch
Patch326: 0029-xen-Only-restore-the-ACPI-SCI-interrupt-in-xen_resto.patch
Patch327: 0030-net-ena-Import-the-ENA-v2-driver-2.0.2g.patch
Patch328: 0031-xen-netfront-call-netif_device_attach-on-resume.patch
Patch329: 0032-net-ena-replace-dma_zalloc_coherent-with-dma_alloc_c.patch
Patch330: 0060-xen-Restore-xen-pirqs-on-resume-from-hibernation.patch
Patch331: 0061-block-xen-blkfront-bump-the-maximum-number-of-indire.patch
Patch332: 0063-linux-ena-update-ENA-linux-driver-to-version-2.1.1.patch
Patch333: 0064-Update-ena-driver-to-version-2.1.3.patch
Patch334: 0065-Add-Amazon-EFA-driver-version-1.4.patch
Patch335: 0066-libfs-revert-d4f4de5e5ef8efde85febb6876cd3c8ab163199.patch
Patch336: 0070-ena-update-to-2.2.3.patch
Patch337: 0071-ena-update-to-2.2.6.patch
Patch338: 0082-ena-Update-to-2.2.10.patch
Patch339: 0123-drivers-amazon-efa-update-to-1.9.0.patch
Patch340: drivers-amazon-efa-driver-compilation-fix-on-5.10.patch

# Enable CONFIG_DEBUG_INFO_BTF=y
Patch400: 0001-tools-resolve_btfids-Warn-when-having-multiple-IDs-f.patch

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

%else

%if 0%{?kat_build}
Patch510: 0003-FIPS-broken-kattest.patch
%endif

%endif

%if 0%{?fips}
#retpoline
Patch511: 0001-retpoline-re-introduce-alternative-for-r11.patch
%endif

BuildArch:      x86_64

BuildRequires:  bc
BuildRequires:  kmod-devel
BuildRequires:  glib-devel
BuildRequires:  elfutils-devel
BuildRequires:  libunwind-devel
BuildRequires:  openssl-devel
BuildRequires:  procps-ng-devel
BuildRequires:  audit-devel
BuildRequires:  python3-macros
BuildRequires:  bison
BuildRequires:  dwarves-devel
%if 0%{?fips}
BuildRequires:  gdb
%endif

Requires: kmod
Requires: filesystem
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

%package sound
Summary:        Kernel Sound modules
Group:          System Environment/Kernel
Requires:       %{name} = %{version}-%{release}
%description sound
The Linux package contains the Linux kernel sound support

%package docs
Summary:        Kernel docs
Group:          System Environment/Kernel
Requires:       python3
%description docs
The Linux package contains the Linux kernel doc files

%ifarch x86_64
%package oprofile
Summary:        Kernel driver for oprofile, a statistical profiler for Linux systems
Group:          System Environment/Kernel
Requires:       %{name} = %{version}-%{release}
%description oprofile
Kernel driver for oprofile, a statistical profiler for Linux systems
%endif

%prep
# Using autosetup is not feasible
%setup -q -n linux-%{version}
%if 0%{?fips}
# Using autosetup is not feasible
%setup -q -T -D -b 16 -n linux-%{version}
%endif

%autopatch -p1 -m0 -M50

# VMW
%autopatch -p1 -m55 -M65

# CVE: [100..300]
%autopatch -p1 -m100 -M157

#Amazon AWS
%autopatch -p1 -m301 -M340

# Enable CONFIG_DEBUG_INFO_BTF=y
%autopatch -p1 -m400 -M400

# crypto
%autopatch -p1 -m500 -M507

%if 0%{?fips}
%autopatch -p1 -m508 -M509
%else
%if 0%{?kat_build}
%patch510 -p1
%endif
%endif

%if 0%{?fips}
%autopatch -p1 -m511 -M511
%endif

%make_build mrproper
cp %{SOURCE1} .config
%if 0%{?fips}
cp ../fips-canister-%{fips_canister_version}/fips_canister.o crypto/
cp ../fips-canister-%{fips_canister_version}/fips_canister_wrapper.c crypto/
cp %{SOURCE18} crypto/
# Patch canister wrapper
patch -p1 < %{SOURCE19}
patch -p1 < %{SOURCE20}
patch -p1 < %{SOURCE21}
%endif

sed -i 's/CONFIG_LOCALVERSION="-aws"/CONFIG_LOCALVERSION="-%{release}-aws"/' .config

%if 0%{?kat_build}
sed -i '/CONFIG_CRYPTO_SELF_TEST=y/a CONFIG_CRYPTO_BROKEN_KAT=y' .config
%endif

%include %{SOURCE4}

%build
%make_build KBUILD_BUILD_VERSION="1-photon" \
    KBUILD_BUILD_HOST="photon" ARCH=%{arch}

%if 0%{?fips}
%include %{SOURCE9}
%endif

%install
install -vdm 755 %{buildroot}%{_sysconfdir}
install -vdm 755 %{buildroot}/boot
install -vdm 755 %{buildroot}%{_docdir}/linux-%{uname_r}
install -vdm 755 %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}
install -vdm 755 %{buildroot}%{_libdir}/debug/%{_modulesdir}
%make_build INSTALL_MOD_PATH=%{buildroot} modules_install

%ifarch x86_64

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
photon_cmdline=init=/lib/systemd/systemd ro loglevel=3 quiet nvme_core.io_timeout=4294967295
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

# disable (JOBS=1) parallel build to fix this issue:
# fixdep: error opening depfile: ./.plugin_cfg80211.o.d: No such file or directory
# Linux version that was affected is 4.4.26

%include %{SOURCE2}
%include %{SOURCE3}
%include %{SOURCE22}

%post
/sbin/depmod -a %{uname_r}
ln -sf linux-%{uname_r}.cfg /boot/photon.cfg

%post drivers-gpu
/sbin/depmod -a %{uname_r}

%post sound
/sbin/depmod -a %{uname_r}

%ifarch x86_64
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
%ifarch x86_64
%exclude %{_modulesdir}/kernel/arch/x86/oprofile/
%endif

%config(noreplace) %{_modulesdir}/dracut.conf.d/%{name}.conf

%files docs
%defattr(-,root,root)
%{_defaultdocdir}/linux-%{uname_r}/*

%files devel
%defattr(-,root,root)
%{_modulesdir}/build
%{_usrsrc}/linux-headers-%{uname_r}

%files drivers-gpu
%defattr(-,root,root)
%exclude %{_modulesdir}/kernel/drivers/gpu/drm/cirrus/
%{_modulesdir}/kernel/drivers/gpu

%files sound
%defattr(-,root,root)
%{_modulesdir}/kernel/sound

%ifarch x86_64
%files oprofile
%defattr(-,root,root)
%{_modulesdir}/kernel/arch/x86/oprofile/
%endif

%changelog
* Tue Jul 09 2024 Ajay Kaher <ajay.kaher@broadcom.com> 5.10.219-3
- Fix for CVE-2022-48666
* Thu Jun 27 2024 Ashwin Dayanand Kamat <ashwin.kamat@broadcom.com> 5.10.219-2
- Fix for CVE-2024-36901
* Wed Jun 19 2024 Ashwin Dayanand Kamat <ashwin.kamat@broadcom.com> 5.10.219-1
- Update to version 5.10.219
* Tue May 07 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 5.10.216-1
- Update to version 5.10.216
* Wed Apr 17 2024 Keerthana K <keerthana.kalyanasundaram@broadcom.com> 5.10.214-4
- Fix CVE-2024-26587, Disable CONFIG_NETDEVSIM
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
- Fix for CVE-2023-52447/2023-52458/2023-52482
* Mon Mar 11 2024 Srish Srinivasan <srish.srinivasan@broadcom.com> 5.10.212-1
- Update to version 5.10.212, patched CVE-2024-26584
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
- Update to version 5.10.206
* Mon Nov 27 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 5.10.201-1
- Update to version 5.10.201
* Wed Nov 15 2023 Kuntal Nayak <nkuntal@vmware.com> 5.10.200-2
- Kconfig to lockdown kernel in UEFI Secure Boot
* Thu Nov 09 2023 Ankit Jain <ankitja@vmware.com> 5.10.200-1
- Update to version 5.10.200
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
* Wed Sep 13 2023 Roye Eshed <eshedr@vmware.com> 5.10.194-1
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
* Thu Mar 30 2023 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.168-2
- Expose Photon kernel macros to simplify building out-of-tree drivers.
* Thu Feb 16 2023 Srish Srinivasan <ssrish@vmware.com> 5.10.168-1
- Update to version 5.10.168
* Thu Feb 16 2023 Keerthana K <keerthanak@vmware.com> 5.10.165-3
- Add FIPS canister
* Tue Feb 14 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 5.10.165-2
- Fix for CVE-2022-2196/CVE-2022-4379
* Wed Feb 08 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 5.10.165-1
- Update to version 5.10.165
* Fri Feb 03 2023 Alexey Makhalov <amakhalov@vmware.com> 5.10.162-2
- Implement performance over security option for RETBleed (pos=1)
* Tue Jan 17 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 5.10.162-1
- Update to version 5.10.162
* Thu Jan 05 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 5.10.159-2
- update to latest ToT vmxnet3 driver
- Include patch "vmxnet3: correctly report csum_level for encapsulated packet"
* Mon Dec 19 2022 srinidhira0 <srinidhir@vmware.com> 5.10.159-1
- Update to version 5.10.159
* Wed Dec 14 2022 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 5.10.158-2
- update to latest ToT vmxnet3 driver
* Mon Dec 12 2022 Ankit Jain <ankitja@vmware.com> 5.10.158-1
- Update to version 5.10.158
* Tue Dec 06 2022 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 5.10.152-8
- Fix for CVE-2022-43945
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
* Tue Aug 16 2022 srinidhira0 <srinidhir@vmware.com> 5.10.132-1
- Update to version 5.10.132
* Fri Aug 12 2022 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 5.10.118-10
- Backport fixes for CVE-2022-0500
* Mon Aug 08 2022 Shreenidhi Shedi <sshedi@vmware.com> 5.10.118-9
- Scriptlets fixes and improvements
* Fri Aug 05 2022 Him Kalyan Bordoloi <bordoloih@vmware.com> 5.10.118-8
- Fix for CVE-2022-2585, CVE-2022-2586 and CVE-2022-2588
* Thu Jul 28 2022 Keerthana K <keerthanak@vmware.com> 5.10.118-7
- Fix linux headers, doc folder and linux-<uname -r>.cfg names
* Fri Jul 15 2022 Keerthana K <keerthanak@vmware.com> 5.10.118-6
- Enable cgroup v1 stats
- .config: enable PERCPU_STATS
* Fri Jul 15 2022 Keerthana K <keerthanak@vmware.com> 5.10.118-5
- Avoid TSC recalibration
* Wed Jul 13 2022 Srinidhi Rao <srinidhir@vmware.com> 5.10.118-4
- Fix for CVE-2022-21505
* Fri Jun 24 2022 Shreenidhi Shedi <sshedi@vmware.com> 5.10.118-3
- Fix debug_package macro usage while adding vmlinux to debuginfo rpm
* Wed Jun 15 2022 Brennan Lamoreaux <blamoreaux@vmware.com> 5.10.118-2
- Enable config_livepatch
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
* Tue Apr 05 2022 Alexey Makhalov <amakhalov@vmware.com> 5.10.103-4
- .config: enable zstd compression for squashfs.
- .config: enable crypto user api rng.
- .config: make ext2 fs builtin module
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
* Sat Jan 08 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.83-5
- Fix CVE-2021-4155 and CVE-2021-4204
* Fri Dec 17 2021 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 5.10.83-4
- Disable md5 algorithm for sctp if fips is enabled.
* Tue Dec 14 2021 Harinadh D <hdommaraju@vmware.com> 5.10.83-3
- remove tmem from add-drivers list
- tmem module is no longer exist
* Thu Dec 09 2021 Prashant S Chauhan <psinghchauha@vmware.com> 5.10.83-2
- Bump up to compile with python 3.10
* Mon Dec 06 2021 srinidhira0 <srinidhir@vmware.com> 5.10.83-1
- Update to version 5.10.83
* Thu Nov 11 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 5.10.78-2
- compile with openssl 3.0.0
* Mon Nov 08 2021 Vikash Bansal <bvikas@vmware.com> 5.10.78-1
- Update to version 5.10.78
* Tue Oct 26 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.75-1
- Update to version 5.10.75
* Thu Sep 09 2021 Alexey Makhalov <amakhalov@vmware.com> 5.10.61-2
- Remove no-vmw-sta as it is not supported in AWS.
* Fri Aug 27 2021 Ankit Jain <ankitja@vmware.com> 5.10.61-1
- Update to version 5.10.61
* Fri Jul 23 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 5.10.52-1
- Update to version 5.10.52
* Thu Jul 15 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 5.10.46-2
- Fix for CVE-2021-33909
* Mon Jun 28 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.46-1
- Update to version 5.10.46
* Tue Jun 22 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.42-2
- Fix for CVE-2021-3609
* Thu Jun 03 2021 Keerthana K <keerthanak@vmware.com> 5.10.42-1
- Update to version 5.10.42
* Mon May 17 2021 Ajay Kaher <akaher@vmware.com> 5.10.35-1
- Update to version 5.10.35
* Thu May 13 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.25-7
- Fix for CVE-2021-23133
* Tue May 11 2021 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.25-6
- Fix CVE-2020-26147, CVE-2020-24587, CVE-2020-24586, CVE-2020-24588,
- CVE-2020-26145, CVE-2020-26141
* Tue May 11 2021 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.25-5
- Fix CVE-2021-3489, CVE-2021-3490, CVE-2021-3491
* Tue May 04 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.25-4
- Remove buf_info from device accessible structures in vmxnet3
* Mon Apr 19 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.25-3
- Fix for CVE-2021-23133
* Thu Apr 15 2021 Srinidhi Rao <srinidhir@vmware.com> 5.10.25-2
- Fix for CVE-2021-29154
* Mon Mar 22 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 5.10.25-1
- Update to version 5.10.25
* Mon Mar 08 2021 Vikash Bansal <bvikas@vmware.com> 5.10.21-1
- Update to version 5.10.21
* Thu Feb 18 2021 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.4-4
- Fix /boot/photon.cfg symlink when /boot is a separate partition.
* Tue Feb 02 2021 Keerthana K <keerthanak@vmware.com> 5.10.4-3
- Removed katbuild patch.
* Mon Jan 25 2021 Ankit Jain <ankitja@vmware.com> 5.10.4-2
- Enabled CONFIG_WIREGUARD
* Mon Jan 11 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 5.10.4-1
- Update to version 5.10.4
* Tue Nov 10 2020 Keerthana K <keerthanak@vmware.com> 5.9.0-4
- Fix CVE-2020-8694
* Fri Nov 06 2020 Keerthana K <keerthanak@vmware.com> 5.9.0-3
- Fix CVE-2020-25704
* Tue Nov 03 2020 Srinidhi Rao <srinidhir@vmware.com> 5.9.0-2
- Remove the support of fipsify and hmacgen
* Wed Oct 28 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 5.9.0-1
- Update to version 5.9.0
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 4.19.127-3
- openssl 1.1.1
* Mon Jul 27 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.127-2
- Fix CVE-2020-14331
* Tue Jun 23 2020 Keerthana K <keerthanak@vmware.com> 4.19.127-1
- Update to version 4.19.127
* Tue Jun 02 2020 Vikash Bansal <bvikas@vmware.com> 4.19.112-6
- Add patch to fix CVE-2019-18885
* Fri May 29 2020 Shreenidhi Shedi <sshedi@vmware.com> 4.19.112-5
- Keep modules of running kernel till next boot
* Wed May 06 2020 Siddharth Chandrasekaran <csiddharth@vmware.com> 4.19.112-4
- Add patch to fix CVE-2020-10711
* Wed Apr 29 2020 Keerthana K <keerthanak@vmware.com> 4.19.112-3
- Photon-checksum-generator version update to 1.1.
* Wed Apr 15 2020 Vikash Bansal <bvikas@vmware.com> 4.19.112-2
- HMAC-SHA256 digest of hmac_generator module moved to hmacgen package
* Wed Apr 08 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.112-1
- Update to version 4.19.112
* Tue Mar 31 2020 Vikash Bansal <bvikas@vmware.com> 4.19.104-2
- hmac generation of crypto modules and initrd generation changes if fips=1
* Wed Mar 25 2020 Vikash Bansal <bvikas@vmware.com> 4.19.104-1
- Update to version 4.19.104
* Mon Mar 16 2020 Keerthana K <keerthanak@vmware.com> 4.19.97-6
- Adding Enhances depedency to hmacgen.
* Wed Mar 04 2020 Vikash Bansal <bvikas@vmware.com> 4.19.97-5
- Backporting of patch continuous testing of RNG from urandom
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
* Thu Jan 02 2020 Keerthana K <keerthanak@vmware.com> 4.19.87-3
- Modify tcrypt to remove tests for algorithms that are not supported in photon.
- Added tests for DH, DRBG algorithms.
* Fri Dec 20 2019 Keerthana K <keerthanak@vmware.com> 4.19.87-2
- Update fips Kat tests.
* Fri Dec 06 2019 Ajay Kaher <akaher@vmware.com> 4.19.87-1
- Update to version 4.19.87
* Thu Dec 05 2019 Ajay Kaher <akaher@vmware.com> 4.19.84-4
- Adding nvme and nvme-core to initrd list
- Removing unwanted modules from initrd list
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
* Tue Aug 06 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.65-1
- Update to version 4.19.65
- Fix CVE-2019-1125 (SWAPGS)
* Tue Jul 30 2019 Keerthana K <keerthanak@vmware.com> 4.19.52-3
- Fix postun script.
* Wed Jul 10 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.52-2
- Deprecate linux-aws-tools in favor of linux-tools.
* Mon Jun 17 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.52-1
- Update to version 4.19.52
- Fix CVE-2019-12456, CVE-2019-12379, CVE-2019-12380, CVE-2019-12381,
- CVE-2019-12382, CVE-2019-12378, CVE-2019-12455
* Thu May 23 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.40-3
- Fix CVE-2019-11191 by deprecating a.out file format support.
* Tue May 14 2019 Keerthana K <keerthanak@vmware.com> 4.19.40-2
- Fix to parse through /boot folder and update symlink (/boot/photon.cfg) if
- mulitple kernels are installed and current linux kernel is removed.
* Tue May 07 2019 Ajay Kaher <akaher@vmware.com> 4.19.40-1
- Update to version 4.19.40
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
* Mon Jan 07 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.6-2
- Enable additional security hardening options in the config.
* Mon Dec 10 2018 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.6-1
- Update to version 4.19.6
- Enable EFI in config-aws to support kernel signing.
* Mon Dec 10 2018 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.1-3
- Set nvme io_timeout to maximum in kernel cmdline.
* Wed Nov 14 2018 Ajay Kaher <akaher@vmware.com> 4.19.1-2
- Adding BuildArch
* Tue Nov 06 2018 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.1-1
- Update to version 4.19.1
* Mon Oct 22 2018 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.18.9-1
- Update to version 4.18.9
* Mon Oct 08 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.14.67-2
- Add enhancements from Amazon.
* Wed Sep 19 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.14.67-1
- Update to version 4.14.67
* Tue Sep 18 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.14.54-4
- Add rdrand-based RNG driver to enhance kernel entropy.
* Sun Sep 02 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.14.54-3
- Add full retpoline support by building with retpoline-enabled gcc.
* Thu Aug 30 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.14.54-2
- Apply out-of-tree patches needed for AppArmor.
* Mon Jul 09 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.14.54-1
- Update to version 4.14.54
* Thu Feb 22 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.14.8-1
- First build based on linux.spec and config. No AWS-specific patches yet.
