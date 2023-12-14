%global security_hardening none

# Set this flag to 0 to build without canister
%global fips 1

%if 0%{?kat_build} == 1
%global fips 1
%endif

Summary:        Kernel
Name:           linux-secure
Version:        5.10.201
Release:        1%{?kat_build:.kat}%{?dist}
License:        GPLv2
URL:            http://www.kernel.org
Group:          System Environment/Kernel
Vendor:         VMware, Inc.
Distribution:   Photon

%define uname_r %{version}-%{release}-secure
%define _modulesdir /lib/modules/%{uname_r}

Source0:        http://www.kernel.org/pub/linux/kernel/v5.x/linux-%{version}.tar.xz
%define sha512 linux=6335fb4f13400f8c61f34de221b4d2807619e2b555ef0884e5ab12e0243be34f6802d46a4df7460b7960e4bf1474a29f8b5ccbb8535120b2b1c9aac1935545d7
Source1:        config-secure
Source2:        initramfs.trigger
# contains pre, postun, filetriggerun tasks
Source3:        scriptlets.inc
Source4:        check_for_config_applicability.inc

%if 0%{?fips}
Source9:        check_fips_canister_struct_compatibility.inc
%if 0%{?kat_build} == 1
%define fips_canister_version 5.0.0-6.1.62-8.kat.ph5-secure
Source16:       fips-canister-%{fips_canister_version}.tar.bz2
%define sha512 fips-canister=7c1dd0d82db0773613c8e227f7a3d27c8ae92638694e30682e4705ee1ec1aac0d37d8d1a289e2d43a98ac71a8503106dbf9cf983f01071892c40bc52de5fac96
%endif
%if 0%{?kat_build} == 0
%define fips_canister_version 5.0.0-6.1.62-13.ph5-secure
Source16:       fips-canister-%{fips_canister_version}.tar.bz2
%define sha512 fips-canister=51f09934bf41186f5e6a6dd06df84ffc9718f5aaea59eaeb887b639c8f0e8f98caac1339ce51139ab8064c1797631024b10fd92f2c65c35d38b88a17857b96b3
%endif
Source17:       fips_canister_wrapper.c
Source18:       fips_canister_wrapper.h
Source19:       fips_canister_wrapper_asm.S
Source20:       fips_canister_wrapper_common.h
Source21:       fips_canister_wrapper_internal.h
Source22:       fips_canister_wrapper_internal.c
%endif

Source23:       spec_install_post.inc
Source24:       %{name}-dracut.conf

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

#HyperV patches
Patch11: vmbus-Don-t-spam-the-logs-with-unknown-GUIDs.patch
Patch12: fork-add-sysctl-to-disallow-unprivileged-CLONE_NEWUSER-by.patch

# Out-of-tree patches from AppArmor:
Patch13: apparmor-patch-to-provide-compatibility-with-v2.x-ne.patch
Patch14: apparmor-af_unix-mediation.patch

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
Patch39: 0002-vmxnet3-use-correct-intrConf-reference-when-using-ex.patch
Patch40: 0001-vmxnet3-move-rss-code-block-under-eop-descriptor.patch
Patch41: 0001-vmxnet3-use-gro-callback-when-UPT-is-enabled.patch

# Disable md5 algorithm for sctp if fips is enabled.
Patch42: 0001-disable-md5-algorithm-for-sctp-if-fips-is-enabled.patch

# Expose Photon kernel macros to identify kernel flavor and version
Patch43: 0001-kbuild-simplify-access-to-the-kernel-s-version.patch
Patch44: 0002-kbuild-replace-if-A-A-B-with-or-A-B.patch
Patch45: 0003-kbuild-Makefile-Introduce-macros-to-distinguish-Phot.patch
Patch46: 0004-linux-secure-Makefile-Add-kernel-flavor-info-to-the-.patch

# VMW:
%ifarch x86_64
Patch55: x86-vmware-Use-Efficient-and-Correct-ALTERNATIVEs-fo.patch
Patch56: x86-vmware-Log-kmsg-dump-on-panic-510.patch
Patch57: 0001-x86-vmware-avoid-TSC-recalibration.patch
%endif

#Secure:
Patch90: 0001-bpf-ext4-bonding-Fix-compilation-errors.patch
Patch91: 0001-NOWRITEEXEC-and-PAX-features-MPROTECT-EMUTRAMP.patch
Patch92: 0002-Added-PAX_RANDKSTACK.patch
Patch93: 0003-Added-rap_plugin.patch
Patch94: 0004-Fix-PAX-function-pointer-overwritten-for-tasklet-cal.patch

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
Patch136: ipc-replace-costly-bailout-check-in-sysvipc_find_ipc.patch

# Crypto:
# Patch to add drbg_pr_ctr_aes256 test vectors to testmgr
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
Patch510: 0001-crypto-api-allow-algs.patch
%endif

%if 0%{?fips} == 0
Patch513: 0001-Skip-rap-plugin-for-aesni-intel-modules.patch
%endif

%if 0%{?kat_build}
Patch514: 0001-fail-canister-integrity-check-for-cmvp-demo.patch
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

BuildArch:      x86_64

BuildRequires:  bc
BuildRequires:  kbd
BuildRequires:  kmod-devel
BuildRequires:  glib-devel
BuildRequires:  xerces-c-devel
BuildRequires:  xml-security-c-devel
BuildRequires:  libdnet-devel
BuildRequires:  libmspack-devel
BuildRequires:  Linux-PAM-devel
BuildRequires:  openssl-devel
BuildRequires:  procps-ng-devel
BuildRequires:  bison

%if 0%{?fips}
BuildRequires: gdb
%endif

Requires: kmod
Requires: filesystem
Requires(pre): (coreutils or coreutils-selinux)
Requires(preun): (coreutils or coreutils-selinux)
Requires(post): (coreutils or coreutils-selinux)
Requires(postun): (coreutils or coreutils-selinux)
# Linux-secure handles user.pax.flags extended attribute
# User must have setfattr/getfattr tools available
Requires: attr

%description
Security hardened Linux kernel.
%if 0%{?fips}
This kernel is FIPS certified.
%endif

%package devel
Summary:       Kernel Dev
Group:         System Environment/Kernel
Requires:      python3 gawk
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
%autopatch -p1 -m55 -M57
%endif

#Secure
%autopatch -p1 -m90 -M94

# CVE
%autopatch -p1 -m100 -M136

# crypto
%autopatch -p1 -m500 -M504

%ifarch x86_64
%autopatch -p1 -m506 -M506
%endif

%if 0%{?fips}
%autopatch -p1 -m508 -M510
%endif

%if 0%{?fips} == 0
%autopatch -p1 -m513 -M513
%endif

%if 0%{?kat_build}
%autopatch -p1 -m514 -M514
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

%if 0%{?fips}
cp ../fips-canister-%{fips_canister_version}/fips_canister.o \
   ../fips-canister-%{fips_canister_version}/.fips_canister.o.cmd \
   ../fips-canister-%{fips_canister_version}/fips_canister-kallsyms \
   crypto/
cp %{SOURCE17} crypto/
cp %{SOURCE18} crypto/
cp %{SOURCE19} crypto/
cp %{SOURCE20} crypto/
cp %{SOURCE21} crypto/
cp %{SOURCE22} crypto/
%endif

sed -i 's/CONFIG_LOCALVERSION="-secure"/CONFIG_LOCALVERSION="-%{release}-secure"/' .config

%include %{SOURCE4}

make V=1 KBUILD_BUILD_VERSION="1-photon" \
    KBUILD_BUILD_HOST="photon" ARCH="x86_64" %{?_smp_mflags}

%if 0%{?fips}
%include %{SOURCE9}
%endif

%install
install -vdm 755 %{buildroot}/%{_sysconfdir}
install -vdm 755 %{buildroot}/boot
install -vdm 755 %{buildroot}%{_docdir}/linux-%{uname_r}
install -vdm 755 %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}
make %{?_smp_mflags} INSTALL_MOD_PATH=%{buildroot} modules_install

install -vm 644 arch/x86/boot/bzImage %{buildroot}/boot/vmlinuz-%{uname_r}
install -vm 400 System.map %{buildroot}/boot/System.map-%{uname_r}
install -vm 644 .config %{buildroot}/boot/config-%{uname_r}
cp -r Documentation/* %{buildroot}%{_docdir}/linux-%{uname_r}

%if 0%{?__debug_package}
install -vdm 755 %{buildroot}%{_libdir}/debug/%{_modulesdir}
install -vm 644 vmlinux %{buildroot}%{_libdir}/debug/%{_modulesdir}/vmlinux-%{uname_r}
%endif

# Since we use compressed modules we cann't use load pinning,
# because .ko files will be loaded from the memory (LoadPin: obj=<unknown>)
cat > %{buildroot}/boot/linux-%{uname_r}.cfg << "EOF"
# GRUB Environment Block
photon_cmdline=init=/lib/systemd/systemd ro loglevel=3 quiet loadpin.enabled=0 audit=1 slub_debug=P page_poison=1 slab_nomerge pti=on
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
ln -sf %{_usrsrc}/linux-headers-%{uname_r} %{buildroot}%{_modulesdir}/build

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
%exclude %{_usrsrc}

%config(noreplace) %{_modulesdir}/dracut.conf.d/%{name}.conf

%files docs
%defattr(-,root,root)
%{_defaultdocdir}/linux-%{uname_r}/*

%files devel
%defattr(-,root,root)
%{_modulesdir}/build
%{_usrsrc}/linux-headers-%{uname_r}

%changelog
* Thu Dec 14 2023 Keerthana K <keerthanak@vmware.com> 5.10.201-1
- Update to version 5.10.201
- Update canister version to 5.0.0-6.1.62-13
* Mon Nov 27 2023 Srish Srinivasan <ssrish@vmware.com> 5.10.198-7
- When kat_build is enabled, make use of a non-production canister
  to build the kernel for performing Broken-KAT
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
- Apply skip rap plugins patch when the kernel is built without
  the canister
* Fri Oct 13 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 5.10.198-1
- Update to version 5.10.198
- Fix CVE-2023-4244
- Update canister to 5.0.0-6.1.56-3
* Tue Oct 03 2023 Keerthana K <keerthanak@vmware.com> 5.10.197-1
- Update to version 5.10.197
* Fri Sep 29 2023 Srinidhi Rao <srinidhir@vmware.com> 5.10.190-2
- Jitterentropy wrapper changes.
* Wed Sep 27 2023 Keerthana K <keerthanak@vmware.com> 5.10.190-1
- Update to version 5.10.190
* Fri Sep 15 2023 Srish Srinivasan <ssrish@vmware.com> 5.10.183-7
- Use canister version 5.0.0-6.1.45-7
* Tue Sep 12 2023 Keerthana K <keerthanak@vmware.com> 5.10.183-6
- Build with jitterentropy v3.4.1-1
* Fri Sep 08 2023 Keerthana K <keerthanak@vmware.com> 5.10.183-5
- Use canister version 5.0.0-6.1.45-4
* Wed Jul 19 2023 Keerthana K <keerthanak@vmware.com> 5.10.183-4
- Fix rap-plugin patch
* Mon Jul 17 2023 Keerthana K <keerthanak@vmware.com> 5.10.183-3
- Use canister version 5.0.0-6.1.37-2
* Tue Jul 04 2023 Keerthana K <keerthanak@vmware.com> 5.10.183-2
- Use canister 5.0.0-6.1.10-18
- Match rap_plugin implementation with 5.0 kernel with KCFI
* Thu Jun 08 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 5.10.183-1
- Update to version 5.10.183, fix some CVEs
* Wed May 31 2023 Ankit Jain <ankitja@vmware.com> 5.10.180-1
- Update to version 5.10.180
* Wed May 24 2023 Alexey Makhalov <amakhalov@vmware.com> 5.10.175-6
- PaX: Support xattr 'em' file markings
* Tue Apr 25 2023 Keerthana K <keerthanak@vmware.com> 5.10.175-5
- Disable strcture randomization
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
* Tue Feb 14 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 5.10.165-2
- Fix for CVE-2022-2196/CVE-2022-4379
* Wed Feb 08 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 5.10.165-1
- Update to version 5.10.165
* Fri Feb 03 2023 Alexey Makhalov <amakhalov@vmware.com> 5.10.162-2
- Implement performance over security option for RETBleed (pos=1)
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
* Tue Aug 16 2022 srinidhira0 <srinidhir@vmware.com> 5.10.132-1
- Update to version 5.10.132
* Fri Aug 12 2022 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 5.10.118-10
- Backport fixes for CVE-2022-0500
* Mon Aug 08 2022 Shreenidhi Shedi <sshedi@vmware.com> 5.10.118-9
- Scriptlets fixes and improvements
* Fri Aug 05 2022 Him Kalyan Bordoloi <bordoloih@vmware.com> 5.10.118-8
- Fix for CVE-2022-2585, CVE-2022-2586 and CVE-2022-2588
* Fri Jul 15 2022 Keerthana K <keerthanak@vmware.com> 5.10.118-7
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
* Sat Jan 08 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.83-6
- Fix CVE-2021-4155 and CVE-2021-4204
* Mon Dec 20 2021 Keerthana K <keerthanak@vmware.com> 5.10.83-5
- crypto_self_test and broken kattest module enhancements
* Fri Dec 17 2021 Alexey Makhalov <amakhalov@vmware.com> 5.10.83-4
- mm: fix percpu alloacion for memoryless nodes
- pvscsi: fix disk detection issue
* Fri Dec 17 2021 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 5.10.83-3
- Disable md5 algorithm for sctp if fips is enabled.
* Tue Dec 14 2021 Harinadh D <hdommaraju@vmware.com> 5.10.83-2
- remove lvm, tmem in add-drivers list
- lvm drivers are built as part of dm-mod
- tmem module is no longer exist
* Mon Dec 06 2021 srinidhira0 <srinidhir@vmware.com> 5.10.83-1
- Update to version 5.10.83
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
* Fri Jul 23 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 5.10.52-1
- Update to version 5.10.52
* Thu Jul 15 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 5.10.46-2
- Fix for CVE-2021-33909
* Mon Jun 28 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.46-1
- Update to version 5.10.46
* Thu Jun 24 2021 Loïc <4661917+HacKurx@users.noreply.github.com> 5.10.42-4
- EMUTRAMP: use the prefix X86_ for error codes
* Tue Jun 22 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.42-3
- Fix for CVE-2021-3609
* Thu Jun 10 2021 Keerthana K <keerthanak@vmware.com> 5.10.42-2
- Added script to check structure compatibility between fips_canister.o and vmlinux.
* Thu Jun 03 2021 Keerthana K <keerthanak@vmware.com> 5.10.42-1
- Update to version 5.10.42
- .config: Enable CONFIG_FANOTIFY_ACCESS_PERMISSIONS
* Mon May 17 2021 Ajay Kaher <akaher@vmware.com> 5.10.35-1
- Update to version 5.10.35
* Thu May 13 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.25-9
- Fix for CVE-2021-23133
* Tue May 11 2021 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.25-8
- Fix CVE-2020-26147, CVE-2020-24587, CVE-2020-24586, CVE-2020-24588,
- CVE-2020-26145, CVE-2020-26141
* Tue May 11 2021 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.25-7
- Fix CVE-2021-3489, CVE-2021-3490, CVE-2021-3491
* Thu Apr 29 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.25-6
- Remove buf_info from device accessible structures in vmxnet3
* Thu Apr 29 2021 Alexey Makhalov <amakhalov@vmware.com> 5.10.25-5
- Update canister binary.
- use jent by drbg and ecc.
- Enable hmac(sha224) self test and broket KAT test.
* Thu Apr 22 2021 Keerthana K <keerthanak@vmware.com> 5.10.25-4
- Update 0001-Skip-rap-plugin-for-aesni-intel-modules.patch for 5.10.25 kernel.
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
* Mon Mar 15 2021 Srinidhi Rao <srinidhir@vmware.com> 5.10.21-2
- Use jitterentropy rng instead of urandom in rng module.
* Mon Mar 08 2021 Vikash Bansal <bvikas@vmware.com> 5.10.21-1
- Update to version 5.10.21
* Mon Mar 01 2021 Alexey Makhalov <amakhalov@vmware.com> 5.10.4-8
- FIPS canister update
* Thu Feb 18 2021 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.4-7
- Fix /boot/photon.cfg symlink when /boot is a separate partition.
* Tue Feb 02 2021 Keerthana K <keerthanak@vmware.com> 5.10.4-6
- Added crypto_self_test and kattest module.
- These patches are applied when kat_build is enabled.
* Thu Jan 28 2021 Alexey Makhalov <amakhalov@vmware.com> 5.10.4-5
- Build with secure FIPS canister.
* Thu Jan 28 2021 Ankit Jain <ankitja@vmware.com> 5.10.4-4
- Enabled CONFIG_WIREGUARD
* Wed Jan 27 2021 Keerthana K <keerthanak@vmware.com> 5.10.4-3
- Fix rap_plugin code to generate rap_hashes when abs-finish is enabled.
* Wed Jan 13 2021 Keerthana K <keerthanak@vmware.com> 5.10.4-2
- Fix build failure.
* Wed Jan 06 2021 Keerthana K <keerthanak@vmware.com> 5.10.4-1
- Update to 5.10.4.
* Tue Nov 10 2020 Keerthana K <keerthanak@vmware.com> 5.9.0-4
- Fix CVE-2020-8694
* Fri Nov 06 2020 Keerthana K <keerthanak@vmware.com> 5.9.0-3
- Fix CVE-2020-25704
* Tue Nov 03 2020 Srinidhi Rao <srinidhir@vmware.com> 5.9.0-2
- Remove the support of fipsify and hmacgen
* Thu Oct 22 2020 Keerthana K <keerthanak@vmware.com> 5.9.0-1
- Update to 5.9.0
* Wed Oct 14 2020 Keerthana K <keerthanak@vmware.com> 5.9.0-rc7.1
- Update to 5.9.0-rc7
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 4.19.127-4
- openssl 1.1.1
* Mon Jul 27 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.127-3
- Fix CVE-2020-14331
* Tue Jun 23 2020 Tapas Kundu <tkundu@vmware.com> 4.19.127-2
- Require python3
* Tue Jun 23 2020 Keerthana K <keerthanak@vmware.com> 4.19.127-1
- Update to version 4.19.127
* Fri Jun 05 2020 Ankit Jain <ankitja@vmware.com> 4.19.112-8
- Enabled CONFIG_BINFMT_MISC
* Tue Jun 02 2020 Vikash Bansal <bvikas@vmware.com> 4.19.112-7
- Add patch to fix CVE-2019-18885
* Fri May 29 2020 Shreenidhi Shedi <sshedi@vmware.com> 4.19.112-6
- Keep modules of running kernel till next boot
* Wed May 06 2020 Siddharth Chandrasekaran <csiddharth@vmware.com> 4.19.112-5
- Add patch to fix CVE-2020-10711
* Mon May 04 2020 Alexey Makhalov <amakhalov@vmware.com> 4.19.112-4
- Updated pax_rap patch to support gcc-8.4.0
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
* Thu Jan 16 2020 Srinidhi Rao <srinidhir@vmware.com> 4.19.87-4
- Enable DRBG HASH and DRBG CTR support.
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
* Tue Jul 02 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.52-2
- Fix 9p vsock 16bit port issue.
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
* Thu Jan 10 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.6-4
- cmdline: added audit=1 pti=on
- config: PANIC_TIMEOUT=-1, DEBUG_RODATA_TEST=y
* Wed Jan 09 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.6-3
- Additional security hardening options in the config.
* Fri Jan 04 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.6-2
- Enable AppArmor by default.
* Mon Dec 10 2018 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.6-1
- Update to version 4.19.6
* Thu Nov 15 2018 Ajay Kaher <akaher@vmware.com> 4.19.1-2
- Adding BuildArch
* Thu Nov 08 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.1-1
- Update to version 4.19.1
* Tue Oct 30 2018 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.18.9-3
- Fix PAX randkstack and RAP plugin patches to avoid boot panic.
* Mon Oct 22 2018 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.18.9-2
- Use updated steal time accounting patch.
* Tue Sep 25 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.18.9-1
- Update to version 4.18.9
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
* Mon Mar 19 2018 Alexey Makhalov <amakhalov@vmware.com> 4.14.8-2
- Extra hardening: slab_nomerge and some .config changes
* Fri Feb 16 2018 Alexey Makhalov <amakhalov@vmware.com> 4.14.8-1
- Version update to v4.14 LTS. Drop aufs support.
* Mon Dec 04 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.66-1
- Version update
* Tue Nov 21 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.64-1
- Version update
* Wed Nov 08 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.60-2
- Update LKCM module
- Add -lkcm subpackage
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
* Fri Jul 14 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.34-3
- Remove aufs source tarballs from git repo
* Mon Jul 03 2017 Xiaolin Li <xiaolinl@vmware.com> 4.9.34-2
- Add libdnet-devel, kmod-devel and libmspack-devel to BuildRequires
* Wed Jun 28 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.34-1
- [feature] 9P FS security support
- [feature] DM Delay target support
- Fix CVE-2017-1000364 ("stack clash") and CVE-2017-9605
* Thu Jun 8 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.31-1
- Fix CVE-2017-8890, CVE-2017-9074, CVE-2017-9075, CVE-2017-9076
    CVE-2017-9077 and CVE-2017-9242
- [feature] IPV6 netfilter NAT table support
* Fri May 26 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.30-1
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
- .config: build nvme and nvme-core in kernel.
* Tue Mar 21 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.13-3
- Added LKCM module
* Mon Mar 6 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.13-2
- .config: NSX requirements for crypto and netfilter
* Tue Feb 28 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.13-1
- Update to linux-4.9.13 to fix CVE-2017-5986 and CVE-2017-6074
- .config: disable XEN guest (needs rap_plugin verification)
* Wed Feb 22 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.9-2
- rap_plugin improvement: throw error on function type casting
    function signatures were cleaned up using this feature.
- Added RAP_ENTRY for asm functions.
* Thu Feb 09 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.9-1
- Update to linux-4.9.9 to fix CVE-2016-10153, CVE-2017-5546,
    CVE-2017-5547, CVE-2017-5548 and CVE-2017-5576.
- Added aufs support.
- Added PAX_RANDKSTACK feature.
- Extra func signatures cleanup to fix 1809717 and 1809722.
- .config: added CRYPTO_FIPS support.
* Tue Jan 10 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.2-1
- Update to linux-4.9.2 to fix CVE-2016-10088
- Rename package to linux-secure.
- Added KSPP cmdline params: slub_debug=P page_poison=1
* Mon Dec 19 2016 Xiaolin Li <xiaolinl@vmware.com> 4.9.0-2
- BuildRequires Linux-PAM-devel
* Mon Dec 12 2016 Alexey Makhalov <amakhalov@vmware.com> 4.9.0-1
- Update to linux-4.9.0
- Add paravirt stolen time accounting feature (from linux-esx),
    but disable it by default (no-vmw-sta cmdline parameter)
- Use vmware_io_delay() to keep "void fn(void)" signature
* Wed Nov 30 2016 Alexey Makhalov <amakhalov@vmware.com> 4.8.0-2
- Expand `uname -r` with release number
- Resign and compress modules after stripping
- .config: add syscalls tracing support
- .config: add cgrup_hugetlb support
- .config: add netfilter_xt_{set,target_ct} support
- .config: add netfilter_xt_match_{cgroup,ipvs} support
- .config: disable /dev/mem
* Mon Oct 17 2016 Alexey Makhalov <amakhalov@vmware.com> 4.8.0-1
- Initial commit.
