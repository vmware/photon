%global security_hardening none
%global __cmake_in_source_build 0

# SBAT generation of "linux.photon" component
%define linux_photon_generation 1

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
Name:           linux-esx
Version:        6.1.111
Release:        3%{?dist}
License:        GPLv2
URL:            http://www.kernel.org
Group:          System Environment/Kernel
Vendor:         VMware, Inc.
Distribution:   Photon

%define uname_r %{version}-%{release}-esx
%define _modulesdir /lib/modules/%{uname_r}

Source0:        http://www.kernel.org/pub/linux/kernel/v6.x/linux-%{version}.tar.xz
%define sha512 linux=239a37cc75c6f19d9f8480cc1fed27e885a60b1d68b127848d3e00ed6e2ffe3fe5d9bea0ada95dad1e39c6e829446f10722b2d8ab062f85aab189ee74512ca9a

Source1:        config-esx_%{_arch}
Source2:        initramfs.trigger
# contains pre, postun, filetriggerun tasks
Source3:        scriptlets.inc
Source4:        check_for_config_applicability.inc

%if 0%{?fips}
Source9:        check_fips_canister_struct_compatibility.inc

%define fips_canister_version 5.0.0-6.1.75-2%{?dist}-secure
Source16:       fips-canister-%{fips_canister_version}.tar.bz2
%define sha512 fips-canister=ddbe5d163f9313209434bf5b2adf711d4b23546012ad08ad869b96c40c94e781bcd13ec1839efc95060038a1d18b2f298e6d7c10584c0335dda445ea1363473b

Source18:       speedup-algos-registration-in-non-fips-mode.patch
%endif

Source19:       spec_install_post.inc

Source20:       %{name}-dracut.conf

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

%if 0%{?fips}
Source36: fips_canister_wrapper.c
Source37: fips_canister_wrapper.h
Source38: fips_canister_wrapper_asm.S
Source39: fips_canister_wrapper_common.h
Source40: fips_canister_wrapper_internal.h
Source41: fips_canister_wrapper_internal.c
%endif

# CVE
Source42: CVE-2023-39191.patches
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
Patch10: 0002-linux-esx-Makefile-Add-kernel-flavor-info-to-the-gen.patch
Patch11: 9p-file-attributes-caching-support.patch
Patch12: 9p-support-for-local-file-lock.patch
Patch13: 6.1-0001-fork-add-sysctl-to-disallow-unprivileged-CLONE_NEWUS.patch
# Out-of-tree patches from AppArmor:
Patch14: 6.0-0001-apparmor-patch-to-provide-compatibility-with-v2.x-ne.patch
Patch15: 6.0-0002-apparmor-af_unix-mediation.patch
Patch16: 0001-Control-MEMCG_KMEM-config.patch
Patch17: Performance-over-security-model.patch
# Disable md5 algorithm for sctp if fips is enabled.
Patch18: 6.0-0001-disable-md5-algorithm-for-sctp-if-fips-is-enabled.patch
# Enable AUXILIARY BUS, to make building other out-of-tree intel NIC drivers easier
Patch19: 0001-Enable-AUXILIARY_BUS-by-default.patch

#VTAR/VTARFS
Patch20: 0001-fs-VTAR-archive-to-TPMFS-extractor.patch
Patch21: 0001-fs-A-new-VTARFS-file-system-to-mount-VTAR-archive.patch
#TARFS
Patch22: 0001-fs-TARFS-file-system-to-mount-TAR-archive.patch
#initrd newca
Patch23: 0001-initramfs-support-for-page-aligned-format-newca.patch

#VMCI/VSOCK
Patch24: 0001-vmw_vsock-vmci_transport-Report-error-when-receiving.patch

# Patches for ptp_vmw
Patch30: 0001-ptp-ptp_vmw-Implement-PTP-clock-adjustments-ops.patch
Patch31: 0002-ptp-ptp_vmw-Add-module-param-to-probe-device-using-h.patch

%ifarch x86_64
# VMW: [50..59]
Patch50: 6.0-x86-vmware-Use-Efficient-and-Correct-ALTERNATIVEs-fo.patch
Patch51: 6.0-x86-vmware-Log-kmsg-dump-on-panic.patch
Patch52: 6.0-x86-vmware-Fix-steal-time-clock-under-SEV.patch
Patch53: 6.0-x86-probe_roms-Skip-OpROM-probing-if-running-as-VMwa.patch
Patch54: 07-vmware-only.patch
Patch55: revert-x86-entry-Align-entry-text-section-to-PMD-boundary.patch

# Secure Boot and Kernel Lockdown
Patch56: 0001-kernel-lockdown-when-UEFI-secure-boot-enabled.patch
Patch57: 0002-Add-.sbat-section.patch
# NOTE: linux-esx does not support kexec, omitting SBAT verify logic.
# CONFIG_SECURITY_SBAT_VERIFY=y
# Patch58: 0003-Verify-SBAT-on-kexec.patch
#external-entropy
Patch59: 0001-external_entropy-Enable-External-Entropy-support.patch
%endif

# linux-esx [60..89]
Patch60: init-do_mounts-recreate-dev-root.patch
Patch61: serial-8250-do-not-probe-U6-16550A-fifo-size.patch
Patch62: 01-clear-linux.patch
Patch63: 02-pci-probe.patch
Patch64: poweroff-without-firmware.patch
Patch65: 04-quiet-boot.patch
Patch66: 05-pv-ops-clocksource.patch
Patch67: 0001-Remove-OOM_SCORE_ADJ_MAX-limit-check.patch
Patch68: halt-on-panic.patch

%if 0%{?vmxnet3_sw_timestamp}
Patch71: 0009-esx-vmxnet3-software-timestamping.patch
%endif

# initialize MMCONFIG
Patch75: 0001-initialize-MMCONFIG-if-already-not-initialized.patch
Patch76: 0001-MMIO_should_have_more_priority_then_IO.patch
Patch77: 0001-Avoid-extra-scanning-for-peer-host-bridges.patch

# Hotplug support without firmware
Patch80: 0001-vmw_extcfg-hotplug-without-firmware-support.patch
Patch81: 0002-vmw_extcfg-hotplug-without-firmware-support.patch
Patch82: 0003-vmw_extcfg-hotplug-without-firmware-support.patch

# SBX driver
Patch85: 0001-Adding-SBX-kernel-driver.patch

# CVE: [100..199]
Patch100: 6.0-0003-apparmor-fix-use-after-free-in-sk_peer_label.patch
# Fix CVE-2017-1000252
Patch101: KVM-Don-t-accept-obviously-wrong-gsi-values-via-KVM_.patch
# Fix CVE-2023-0597
Patch103: 0001-x86-mm-Randomize-per-cpu-entry-area.patch
Patch104: 0002-x86-mm-Do-not-shuffle-CPU-entry-areas-without-KASLR.patch
# Fix CVE-2023-39191 [110..128]
%include %{SOURCE42}

# Fix CVE-2023-52452
Patch133: 0001-bpf-Fix-accesses-to-uninit-stack-slots.patch

# Fix CVE-2024-42322
Patch134: 0001-ipvs-properly-dereference-pe-in-ip_vs_add_service.patch

# aarch64 [200..219]
%ifarch aarch64
Patch200: 6.0-0001-x86-hyper-generalize-hypervisor-type-detection.patch
Patch201: 6.0-0002-arm64-Generic-hypervisor-type-detection-for-arm64.patch
Patch202: 6.0-0003-arm64-VMware-hypervisor-detection.patch
Patch203: 6.0-0004-arm64-kmsg-dumper-for-VMware-hypervisor.patch
Patch204: 6.0-0005-scsi-vmw_pvscsi-add-arm64-support.patch
Patch205: 6.0-0006-vmxnet3-build-only-for-x86-and-arm64.patch
Patch206: 6.0-0005-vmw_balloon-add-arm64-support.patch
Patch207: 6.0-0001-vmw_vmci-arm64-support-memory-ordering.patch
%endif

# 9p: [300..350]
Patch300: 0001-fs-9p-Add-opt_metaonly-cache-option.patch
Patch301: 0002-p9fs_dir_readdir-offset-support.patch
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
Patch503: 0001-FIPS-crypto-rng-Jitterentropy-RNG-as-the-only-RND-source.patch
# Patch to remove urandom usage in drbg and ecc modules
Patch504: 0003-FIPS-crypto-drbg-Jitterentropy-RNG-as-the-only-RND.patch

%ifarch x86_64
Patch505: 0001-changes-to-build-with-jitterentropy-v3.4.1.patch
Patch506: 0001-jitterentropy-kcapi-defer-jent_init.patch
%endif

%if 0%{?fips}
# FIPS canister usage patch
Patch508: 0001-FIPS-canister-binary-usage.patch
Patch509: 0001-scripts-kallsyms-Extra-kallsyms-parsing.patch
Patch510: 0001-LKCM-5.0-binary-patching-to-fix-struct-aesni_cpu_id-.patch
%endif

%ifarch x86_64
# SEV on VMware: [600..609]
Patch600: 0079-x86-sev-es-Disable-BIOS-ACPI-RSDP-probing-if-SEV-ES-.patch
Patch601: 0080-x86-boot-Enable-vmw-serial-port-via-Super-I-O.patch
Patch602: 0001-x86-boot-unconditional-preserve-CR4.MCE.patch
# TODO: Review: Patch602: 0081-x86-sev-es-Disable-use-of-WP-via-PAT-for-__sme_early.patch
%endif

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
BuildRequires: which

%if 0%{?fips}
BuildRequires: gdb
%endif

Requires: kmod
Requires: filesystem
Requires(pre):    (coreutils or coreutils-selinux)
Requires(preun):  (coreutils or coreutils-selinux)
Requires(post):   (coreutils or coreutils-selinux)
Requires(postun): (coreutils or coreutils-selinux)

%description
The Linux kernel build for GOS for VMware hypervisor.
# Enable post FIPS certification
%if 0
This kernel is FIPS certified.
%endif
%if 0%{?vmxnet3_sw_timestamp}
- vmxnet3 with software timestamping enabled
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

# common
%autopatch -p1 -m0 -M49

%ifarch x86_64
# VMW x86
%autopatch -p1 -m50 -M59
%endif

# linux-esx
%autopatch -p1 -m60 -M89

# CVE
%autopatch -p1 -m100 -M137

%ifarch aarch64
# aarch64 patches
%autopatch -p1 -m200 -M219
%endif

# 9P
%autopatch -p1 -m300 -M309

# crypto
%autopatch -p1 -m500 -M504

%ifarch x86_64
%autopatch -p1 -m505 -M506
%endif

%if 0%{?fips}
%autopatch -p1 -m508 -M510
%endif

%ifarch x86_64
# SEV on VMware
%autopatch -p1 -m600 -M609
%endif

%ifarch x86_64
cp -r ../jitterentropy-%{jent_major_version}-%{jent_ph_version}/ \
      crypto/jitterentropy-%{jent_major_version}/
cp %{SOURCE33} crypto/jitterentropy-%{jent_major_version}/
cp %{SOURCE34} crypto/jitterentropy-%{jent_major_version}/
cp %{SOURCE35} crypto/jitterentropy-%{jent_major_version}/
%endif

%make_build mrproper
cp %{SOURCE1} .config
%if 0%{?fips}
cp %{SOURCE36} crypto/
cp %{SOURCE37} crypto/
cp %{SOURCE38} crypto/
cp %{SOURCE39} crypto/
cp %{SOURCE40} crypto/
cp %{SOURCE41} crypto/
cp ../fips-canister-%{fips_canister_version}/fips_canister.o \
   ../fips-canister-%{fips_canister_version}/.fips_canister.o.cmd \
   ../fips-canister-%{fips_canister_version}/fips_canister-kallsyms \
   crypto/
# Patch canister wrapper
patch -p1 < %{SOURCE18}
%endif
sed -i 's/CONFIG_LOCALVERSION="-esx"/CONFIG_LOCALVERSION="-%{release}-esx"/' .config

%ifarch x86_64
sed -e "s,@@NAME@@,%{name},g" \
    -e "s,@@VERSION_RELEASE@@,%{version}-%{release},g" \
    -e "s,@@LINUX_PH_GEN@@,%{linux_photon_generation},g" \
    %{SOURCE25} > linux-sbat.csv
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
%make_build ARCH=%{arch} INSTALL_MOD_PATH=%{buildroot} modules_install

%ifarch x86_64
install -vm 644 arch/%{archdir}/boot/bzImage %{buildroot}/boot/vmlinuz-%{uname_r}
%endif

%ifarch aarch64
install -vm 644 arch/%{archdir}/boot/Image %{buildroot}/boot/vmlinuz-%{uname_r}
%endif

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

# cleanup dangling symlinks
rm -f %{buildroot}%{_modulesdir}/source \
      %{buildroot}%{_modulesdir}/build

# create /use/src/linux-headers-*/ content
find . -name Makefile* -o -name Kconfig* -o -name *.pl | xargs sh -c 'cp --parents "$@" %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}' copy
find arch/%{archdir}/include include scripts -type f | xargs sh -c 'cp --parents "$@" %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}' copy
find $(find arch/%{archdir} -name include -o -name scripts -type d) -type f | xargs sh -c 'cp --parents "$@" %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}' copy
find arch/%{archdir}/include Module.symvers include scripts -type f | xargs sh -c 'cp --parents "$@" %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}' copy
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

mkdir -p %{buildroot}%{_modulesdir}/dracut.conf.d/
cp -p %{SOURCE20} %{buildroot}%{_modulesdir}/dracut.conf.d/%{name}.conf

%include %{SOURCE2}
%include %{SOURCE3}
%include %{SOURCE19}

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

%config(noreplace) %{_modulesdir}/dracut.conf.d/%{name}.conf

%files docs
%defattr(-,root,root)
%{_docdir}/linux-%{uname_r}/*

%files devel
%defattr(-,root,root)
%{_modulesdir}/build
%{_usrsrc}/linux-headers-%{uname_r}

%changelog
* Tue Oct 08 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 6.1.111-3
- Fix CVE-2024-42322
* Thu Oct 03 2024 Srinidhi Rao <srinidhi.rao@broadcom.com> 6.1.111-2
- In jitterentropy, use vzalloc instead of kzalloc.
* Fri Sep 20 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 6.1.111-1
- Update to version 6.1.111
* Tue Sep 10 2024 Ankit Jain <ankit-aj.jain@broadcom.com> 6.1.109-1
- Update to version 6.1.109
* Tue Sep 10 2024 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 6.1.106-6
- Fix CVE-2024-42228
* Wed Sep 04 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 6.1.106-5
- Fix CVE-2024-43859, CVE-2024-43835
* Wed Sep 04 2024 Ankit Jain <ankit-aj.jain@broadcom.com> 6.1.106-4
- Enable CONFIG_NFT_OBJREF, so that we can refer counter by name
* Tue Sep 03 2024 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 6.1.106-3
- Enable CONFIG_ARM64_ERRATUM_3194386
* Tue Aug 27 2024 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 6.1.106-2
- Fix CVE-2024-42314
* Tue Aug 20 2024 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 6.1.106-1
- Update to version 6.1.106
* Tue Aug 20 2024 Keerthana K <keerthana.kalyanasundaram@broadcom.com> 6.1.102-2
- Binary patch aesni_cpu_id value in canister
* Mon Aug 05 2024 Harinadh Dommaraju <Harinadh.Dommaraju@broadcom.com> 6.1.102-1
- Update to version 6.1.102
* Wed Jul 10 2024 Ajay Kaher <ajay.kaher@broadcom.com> 6.1.97-1
- Update to version 6.1.97
* Wed Jun 19 2024 Ashwin Dayanand Kamat <ashwin.kamat@broadcom.com> 6.1.94-1
- Update to version 6.1.94
* Tue Jun 11 2024 Srinidhi Rao <srinidhi.rao@broadcom.com> 6.1.90-4
- Include External Entropy support only for X86_64.
* Mon Jun 03 2024 Srinidhi Rao <srinidhi.rao@broadcom.com> 6.1.90-3
- External entropy support.
* Mon May 20 2024 Keerthana K <keerthana.kalyanasundaram@broadcom.com> 6.1.90-2
- Optimize gdb commands in check_fips_canister_compatibility script
* Mon May 13 2024 Ankit Jain <ankit-aj.jain@broadcom.com> 6.1.90-1
- Update to version 6.1.90
* Thu May 09 2024 Keerthana K <keerthana.kalyanasundaram@broadcom.com> 6.1.83-4
- Enable CONFIG_X86_SGX
* Wed May 08 2024 Keerthana K <keerthana.kalyanasundaram@broadcom.com> 6.1.83-3
- Add SEV patches back in spec file
* Sun Apr 14 2024 Kuntal Nayak <kuntal.nayak@broadcom.com> 6.1.83-2
- Patched CVE-2024-26643
* Thu Apr 11 2024 Keerthana K <keerthana.kalyanasundaram@broadcom.com> 6.1.83-1
- Update to version 6.1.83
- Fix CVE-2024-26642
* Wed Apr 10 2024  Kuntal Nayak <kuntal.nayak@broadcom.com> 6.1.81-6
- Update SBAT verification
* Wed Apr 10 2024 Srinidhi Rao <srinidhi.rao@broadcom.com> 6.1.81-5
- Defer the initialization of jitterentropy.
* Wed Mar 27 2024 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 6.1.81-4
- Fix CVE-2024-52452
* Wed Mar 27 2024 Ajay Kaher <ajay.kaher@broadcom.com> 6.1.81-3
- Fix CVE-2023-52585
* Mon Mar 25 2024 Srish Srinivasan <srish.srinivasan@broadcom.com> 6.1.81-2
- Patched CVE-2024-26585
* Wed Mar 06 2024 Srish Srinivasan <srish.srinivasan@broadcom.com> 6.1.81-1
- Update to version 6.1.81, patched CVE-2024-26584
* Wed Mar 06 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 6.1.79-2
- Fixes CVE-2024-23307 and CVE-2024-22099
* Mon Feb 26 2024 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 6.1.79-1
- Update to version 6.1.79
* Tue Feb 13 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 6.1.77-1
- Update to version 6.1.77
* Mon Feb 12 2024 Keerthana K <keerthana.kalyanasundaram@broadcom.com> 6.1.75-3
- Update canister version to 5.0.0-6.1.75-2
* Wed Jan 31 2024 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 6.1.75-2
- Upgrade iavf to v4.9.5 and ice to 1.13.7
* Tue Jan 23 2024 Ajay Kaher <ajay.kaher@broadcom.com> 6.1.75-1
- Update to version 6.1.75
* Tue Jan 23 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 6.1.70-4
- Fix CVE-2023-6915
* Wed Jan 17 2024 Bryan Tan <bryan-bt.tan@broadcom.com> 6.1.70-3
- Fix refcount underflow in vsock
* Tue Jan 16 2024 Ajay Kaher <ajay.kaher@broadcom.com> 6.1.70-2
- Fix CVE-2024-0340
* Mon Jan 01 2024 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 6.1.70-1
- Update to version 6.1.70
* Wed Dec 20 2023 Keerthana K <keerthanak@vmware.com> 6.1.62-14
- Increase CONFIG_LOG_BUF_SHIFT to 18
- Decrease CONFIG_LOG_CPU_MAX_BUF_SHIFT to 12
* Thu Dec 14 2023 Keerthana K <keerthanak@vmware.com> 6.1.62-13
- Update canister to 5.0.0-6.1.62-13
* Thu Dec 14 2023 Keerthana K <keerthanak@vmware.com> 6.1.62-12
- FIPS: Add log messages for approved and non-approved services
- Remove fips=2 logic
* Tue Dec 12 2023 Kuntal Nayak <nkuntal@vmware.com> 6.1.62-11
- Fix CVE-2023-39191
* Fri Dec 08 2023 Srish Srinivasan <ssrish@vmware.com> 6.1.62-10
- Added self-tests for rsa-pkcs1pad in combination with sha1, sha224, sha384 and sha512
* Tue Dec 5 2023 Albert Guo <aguo@vmware.com> 6.1.62-9
- Fix race condition in v9fs_dentry_release
* Mon Nov 27 2023 Kuntal Nayak <nkuntal@vmware.com> 6.1.62-8
- Fix CVE-2023-5633
* Sat Nov 25 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 6.1.62-7
- Update canister to 5.0.0-6.1.62-7
* Thu Nov 23 2023 Ankit Jain <ankitja@vmware.com> 6.1.62-6
- tarfs: Fixes file permission
* Wed Nov 22 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 6.1.62-5
- Fix for CVE-2023-2176
* Tue Nov 21 2023 Keerthana K <keerthanak@vmware.com> 6.1.62-4
- Update canister to 5.0.0-6.1.62-2
* Mon Nov 20 2023 Ajay Kaher <akaher@vmware.com> 6.1.62-3
- Enabling VFIO, UIO and IOMMU support
* Sat Nov 18 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 6.1.62-2
- Fix RSA self tests
* Tue Nov 14 2023 Ankit Jain <ankitja@vmware.com> 6.1.62-1
- Update to version 6.1.62
* Mon Nov 6 2023 Albert Guo <aguo@vmware.com> 6.1.60-5
- Use iov_iter_revert() to fix offset of iov.
* Fri Oct 27 2023 Ankit Jain <ankitja@vmware.com> 6.1.60-4
- Fix for CVE-2023-0597
* Fri Oct 27 2023 Srish Srinivasan <ssrish@vmware.com> 6.1.60-3
- Remove kat_build and its associated spec changes
* Fri Oct 27 2023 Srinidhi Rao <srinidhir@vmware.com> 6.1.60-2
- Jitterentropy sample collection support in ACVP Build.
* Fri Oct 27 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 6.1.60-1
- Upgrade to 6.1.60
* Thu Oct 26 2023 Alexey Makhalov <amakhalov@vmware.com> 6.1.56-9
- Add .sbat section for bzImage
- newca: fixes and enhancements
* Thu Oct 26 2023 Srish Srinivasan <ssrish@vmware.com> 6.1.56-8
- Upgrade canister to 5.0.0-6.1.56-6
* Tue Oct 24 2023 Srish Srinivasan <ssrish@vmware.com> 6.1.56-7
- Added cts to crypto self-tests
- Removed rsa(pkcs1pad, sha256), rsa(pkcs1pad, sha512),
  cbc, and ctr from crypto self-tests
- Added ECC pubkey generation and verification success messages
* Fri Oct 20 2023 Albert Guo <aguo@vmware.com> 6.1.56-6
- Ported 11 9P patches (combined 2 of them) for VDFS from 4.19.y(photon3) to 6.1.y(photon5).
* Wed Oct 18 2023 Keerthana K <keerthanak@vmware.com> 6.1.56-5
- Modified ecdh-nist-p384 vector to generate ECC keypair
* Tue Oct 17 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 6.1.56-4
- Upgrade canister to 5.0.0-6.1.56-3
* Tue Oct 10 2023 Srish Srinivasan <ssrish@vmware.com> 6.1.56-3
- Add missing self-test vector for ecdh-nist-p384 with genkey
* Mon Oct 09 2023 Srinidhi Rao <srinidhir@vmware.com> 6.1.56-2
- Jitterentropy wrapper changes.
* Fri Oct 06 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 6.1.56-1
- Upgrade to 6.1.56
* Tue Oct 03 2023 Kuntal Nayak <nkunal@vmware.com> 6.1.53-8
- Kconfig to lockdown kernel in UEFI Secure Boot
* Sun Oct 01 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 6.1.53-7
- Fix for CVE-2023-42754
* Sat Sep 30 2023 Keerthana K <keerthanak@vmware.com> 6.1.53-6
- Revert crypto_test (tcrypt) config to 'm'
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
* Mon Jul 31 2023 Ajay Kaher <akaher@vmware.com> 6.1.41-2
- Fix: unconditional preserve CR4.MCE
* Thu Jul 20 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 6.1.41-1
- Update to version 6.1.41
* Mon Jul 17 2023 Keerthana K <keerthanak@vmware.com> 6.1.37-3
- Use canister version 5.0.0-6.1.37-2
* Thu Jul 06 2023 Garrett Goble <gobleg@vmware.com> 6.1.37-2
- Adding SBX kernel driver
* Tue Jul 04 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 6.1.37-1
- Update to version 6.1.37
* Tue Jun 06 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 6.1.32-1
- Update to version 6.1.32
* Wed May 31 2023 Guruswamy Basavaiah <bguruswamy@vmware.com> 6.1.28-2
- disable kconfig CONFIG_RAID6_PQ_BENCHMARK
* Tue May 16 2023 Ankit Jain <ankitja@vmware.com> 6.1.28-1
- Update to version 6.1.28
* Tue Apr 25 2023 Shreenidhi Shedi <sshedi@vmware.com> 6.1.10-12
- Remove dracut & initramfs from requires
* Tue Apr 25 2023 Shreenidhi Shedi <sshedi@vmware.com> 6.1.10-11
- Remove dracut & initramfs from requires
* Wed Apr 19 2023 Ankit Jain <ankitja@vmware.com> 6.1.10-10
- tarfs: fixes buffer overflow
* Thu Apr 13 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 6.1.10-9
- Use canister version 5.0.0-6.1.10-10
* Thu Apr 06 2023 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 6.1.10-8
- Expose Photon kernel macros to simplify building out-of-tree drivers.
* Thu Mar 30 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 6.1.10-7
- Update drivers
- iavf: 4.8.2
- ice: 1.11.14
- i40e: 2.22.18
* Fri Mar 24 2023 Keerthana K <keerthanak@vmware.com> 6.1.10-6
- Disable FIPS canister binary usage
* Tue Mar 21 2023 Shreenidhi Shedi <sshedi@vmware.com> 6.1.10-5
- Fix initramfs trigger
* Thu Mar 16 2023 Keerthana K <keerthanak@vmware.com> 6.1.10-4
- Enable FIPS canister binary usage
* Thu Mar 02 2023 Shreenidhi Shedi <sshedi@vmware.com> 6.1.10-3
- Fix initrd generation logic
- Add dracut, initramfs to requires
* Fri Feb 24 2023 Ankit Jain <ankitja@vmware.com> 6.1.10-2
- Exclude iavf.conf
* Wed Feb 22 2023 Bo Gan <ganb@vmware.com> 6.1.10-1
- Update to 6.1.10
* Thu Feb 16 2023 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 6.0.7-8
- Update i40e driver to v2.19.3 to prevent kernel warnings
* Thu Feb 02 2023 Shreenidhi Shedi <sshedi@vmware.com> 6.0.7-7
- Fix requires
* Mon Jan 30 2023 Keerthana K <keerthanak@vmware.com> 6.0.7-6
- Enable CONFIG_E1000E & CONFIG_E1000 for arm64
* Fri Jan 27 2023 Shivani Agarwal <shivania2@vmware.com> 6.0.7-5
- Enable CONFIG_DRM_I915
* Wed Jan 18 2023 Ajay Kaher <akaher@vmware.com> 6.0.7-4
- Fix aarch64 rpm build issue
* Fri Jan 13 2023 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 6.0.7-3
- Fix IRQ affinities of i40e, iavf and ice drivers
* Mon Jan 09 2023 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 6.0.7-2
- Update Intel drivers i40e to v2.16.11, iavf to v4.5.3 and ice to v1.9.11
* Mon Jan 09 2023 Bo Gan <ganb@vmware.com> 6.0.7-1
- Update to 6.0.7
- common: Change from SLAB to SLUB
- common: Enable BPF/JIT
- aarch64: match configs with x86 for arch independent features.
- aarch64: disable unused platform/drivers for VM.
* Fri Jan 06 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 5.10.142-4
- Bump up due to change in elfutils
* Mon Nov 21 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 5.10.142-3
- Avoid extra scanning for peer host bridges when mmconfig is initialized.
* Thu Oct 20 2022 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 5.10.142-2
- Fix build with latest toolchain
* Wed Sep 28 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.142-1
- Update to version 5.10.142
* Tue Sep 27 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.132-1
- Update to version 5.10.132
* Tue Sep 27 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.118-11
- Backport fixes for CVE-2022-0500
* Tue Sep 27 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.118-10
- Fix for CVE-2022-2585, CVE-2022-2586 and CVE-2022-2588
* Tue Sep 27 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.118-9
- tarfs: fix error for empty tar archive
* Tue Sep 27 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.118-8
- Fix multiple issues in tarfs
* Tue Sep 27 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.118-7
- Update iavf driver to v4.4.2
- Update ice driver to v1.8.3
- .config: Enable CONFIG_NET_DEVLINK=y (ice v1.8.3 needs it)
* Mon Sep 26 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.118-6
- .config: enable CROSS_MEMORY_ATTACH
- Add elfutils-libelf-devel required to build objtool
- vmxnet3: enable software timestamping
* Fri Sep 23 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.118-5
- .config: disable kernel accounting for memory cgroups
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
* Wed Sep 21 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.103-4
- .config: Increase kernel log buffer size to fix regression.
* Tue Sep 20 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.103-3
- Fix for CVE-2022-1016
* Mon Sep 19 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.103-2
- Fix SEV and Hypercall alternative inst. patches
* Thu Sep 15 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.103-1
- Update to version 5.10.103
* Thu Sep 15 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.93-7
- Reduce kernel .data section by configuring smaller kernel log buffer (16)
- Speedup algos registration in non-fips mode
* Wed Sep 14 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.93-6
- vtarfs: fix multiple issues
- tarfs: support for hardlink, fix uid/gid/mode issues
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
* Wed Sep 14 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.83-7
- Update ptp_vmw with provider mode support
* Wed Sep 14 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.83-6
- Fix CVE-2021-4155 and CVE-2021-4204
* Wed Sep 14 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.83-5
- crypto_self_test and broken kattest module enhancements
- FIPS: Add module signing for crypto modules
* Tue Sep 13 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.83-4
- mm: fix percpu allocation for memoryless nodes
- pvscsi: fix disk detection issue
* Tue Sep 13 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.83-3
- remove lvm in add-drivers list
- lvm drivers are built as part of dm-mod
* Tue Sep 13 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.83-2
- tarfs: Fix binary execution issue
* Mon Sep 12 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.83-1
- Update to version 5.10.83
* Mon Aug 08 2022 Shreenidhi Shedi <sshedi@vmware.com> 5.10.78-17
- Scriptlets fixes and improvements
* Fri Jul 29 2022 Tejaswini Jayaramaiah <jtejaswini@vmware.com> 5.10.78-16
- Enable CONFIG_CGROUP_BPF in config to run containers with cgroup v2
* Wed Jun 29 2022 Keerthana K <keerthanak@vmware.com> 5.10.78-15
- Reduce FIPS canister memory footprint by disabling CONFIG_KALLSYMS_ALL
- Add only fips_canister-kallsyms to vmlinux instead of all symbols
* Fri Jun 24 2022 Shreenidhi Shedi <sshedi@vmware.com> 5.10.78-14
- Fix debug_package macro usage while adding vmlinux to debuginfo rpm
* Tue May 31 2022 Ajay Kaher <akaher@vmware.com> 5.10.78-13
- initialize MMCONFIG, if already not initialized
* Mon Apr 18 2022 Alexey Makhalov <amakhalov@vmware.com> 5.10.78-12
- Add objtool to the -devel package.
- Reduce kernel .data section by configuring smaller kernel log buffer
- .config(x86_64): enable amdgpu driver as a module
* Tue Apr 05 2022 Shreenidhi Shedi <sshedi@vmware.com> 5.10.78-11
- Enable CONFIG_EXT2_FS_XATTR & related parameters
* Mon Feb 28 2022 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 5.10.78-10
- Port non-acpi hotplug support patch to 5.10.x
* Tue Feb 01 2022 Alexey Makhalov <amakhalov@vmware.com> 5.10.78-9
- Reduce kernel .text size by ~40% by removing .entry.text alignment.
* Tue Jan 25 2022 Alexey Makhalov <amakhalov@vmware.com> 5.10.78-8
- .config: enable squashfs module, enable crypto user api rng.
* Wed Dec 01 2021 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 5.10.78-7
- Disable md5 algorithm for sctp if fips is enabled.
* Tue Nov 30 2021 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 5.10.78-6
- Correct the config file for linux-esx on arm machine
* Tue Nov 23 2021 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 5.10.78-5
- tarfs: A new readonly filesystem to mount tar archive
* Fri Nov 19 2021 Keerthana K <keerthanak@vmware.com> 5.10.78-4
- Remove vmci and vmw_balloon patches
- Update Hypervisor detection patch with review comments addressed
* Thu Nov 11 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 5.10.78-3
- compile with openssl 3.0.0
* Mon Nov 08 2021 Keerthana K <keerthanak@vmware.com> 5.10.78-2
- Add out-of-tree i40e, iavf and ice drivers.
* Mon Nov 08 2021 Vikash Bansal <bvikas@vmware.com> 5.10.78-1
- Update to version 5.10.78
* Thu Oct 28 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.75-1
- Update to version 5.10.75
* Thu Oct 21 2021 Keerthana K <keerthanak@vmware.com> 5.10.61-7
- Arm64 VMware Hypervisor features
- Arm64 support for vmw_pvscsi, vmw_vmci and vmw_balloon
- vmxnet3: build only for x86 and arm64
* Thu Oct 21 2021 Keerthana K <keerthanak@vmware.com> 5.10.61-6
- Add arm64 support
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
-         Fixed fault handler
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
