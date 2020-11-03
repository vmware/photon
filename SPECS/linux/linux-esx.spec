%global security_hardening none
Summary:        Kernel
Name:           linux-esx
Version:        5.9.0
Release:        3%{?kat_build:.kat}%{?dist}
License:        GPLv2
URL:            http://www.kernel.org/
Group:          System Environment/Kernel
Vendor:         VMware, Inc.
Distribution:   Photon

%define uname_r %{version}-%{release}-esx

Source0:        http://www.kernel.org/pub/linux/kernel/v5.x/linux-%{version}.tar.xz
%define sha1 linux=26fefa389c711da70543092fbb121a023f1b0fb8
Source1:        config-esx
Source2:        initramfs.trigger
Source3:        pre-preun-postun-tasks.inc
Source4:        check_for_config_applicability.inc
# common
Patch0:         net-Double-tcp_mem-limits.patch
# TODO: disable this patch, check for regressions
#Patchx:         linux-4.9-watchdog-Disable-watchdog-on-virtual-machines.patch
Patch1:         SUNRPC-Do-not-reuse-srcport-for-TIME_WAIT-socket.patch
Patch2:         SUNRPC-xs_bind-uses-ip_local_reserved_ports.patch
Patch3:         9p-transport-for-9p.patch
Patch4:	        9p-trans_fd-extend-port-variable-to-u32.patch
Patch5:         vsock-delay-detach-of-QP-with-outgoing-data-59.patch
Patch6:         hwrng-rdrand-Add-RNG-driver-based-on-x86-rdrand-inst.patch
Patch7:         9p-file-attributes-caching-support.patch
Patch8:         9p-support-for-local-file-lock.patch
Patch9:         fork-add-sysctl-to-disallow-unprivileged-CLONE_NEWUSER-by.patch
Patch10:        apparmor-patch-to-provide-compatibility-with-v2.x-ne.patch
Patch11:        apparmor-af_unix-mediation.patch

# VMW:
Patch30:        x86-vmware-Use-Efficient-and-Correct-ALTERNATIVEs-fo.patch
Patch31:        x86-vmware-Log-kmsg-dump-on-panic.patch
Patch32:        x86-vmware-Fix-steal-time-clock-under-SEV.patch

# -esx
Patch50:        init-do_mounts-recreate-dev-root.patch
Patch51:        serial-8250-do-not-probe-U6-16550A-fifo-size.patch
Patch52:        01-clear-linux.patch
Patch53:        02-pci-probe.patch
Patch54:        03-poweroff.patch
Patch55:        04-quiet-boot.patch
Patch56:        05-pv-ops-clocksource.patch
# TODO: make it working for v5.9+
#Patch57:        06-pv-ops-boot_clock.patch
Patch58:        07-vmware-only.patch
Patch59:        initramfs-support-for-page-aligned-format-newca.patch
Patch60:        0001-Remove-OOM_SCORE_ADJ_MAX-limit-check.patch
Patch61:        0001-fs-VTAR-archive-to-TPMFS-extractor.patch
Patch62:        0001-fs-A-new-VTARFS-file-system-to-mount-VTAR-archive.patch

# CVE:
Patch100:       apparmor-fix-use-after-free-in-sk_peer_label.patch
# Fix CVE-2017-1000252
Patch101:       KVM-Don-t-accept-obviously-wrong-gsi-values-via-KVM_.patch
# Fix for CVE-2019-12379
Patch102:       consolemap-Fix-a-memory-leaking-bug-in-drivers-tty-v.patch

# Crypto:
# Patch to add drbg_pr_ctr_aes256 test vectors to testmgr
Patch500:       crypto-testmgr-Add-drbg_pr_ctr_aes256-test-vectors.patch
# Patch to call drbg and dh crypto tests from tcrypt
Patch501:       tcrypt-disable-tests-that-are-not-enabled-in-photon.patch

%if 0%{?kat_build:1}
Patch510:       crypto-testmgr-break-KAT-fips-intentionally.patch
%endif

# SEV:
Patch600:       0001-KVM-SVM-nested-Don-t-allocate-VMCB-structures-on-sta.patch
Patch601:       0002-KVM-SVM-Add-GHCB-definitions.patch
Patch602:       0003-KVM-SVM-Add-GHCB-Accessor-functions.patch
Patch603:       0004-KVM-SVM-Use-__packed-shorthand.patch
Patch604:       0005-x86-cpufeatures-Add-SEV-ES-CPU-feature.patch
Patch605:       0006-x86-traps-Move-pf-error-codes-to-asm-trap_pf.h.patch
Patch606:       0007-x86-insn-Make-inat-tables.c-suitable-for-pre-decompr.patch
Patch607:       0008-x86-umip-Factor-out-instruction-fetch.patch
Patch608:       0009-x86-umip-Factor-out-instruction-decoding.patch
Patch609:       0010-x86-insn-Add-insn_get_modrm_reg_off.patch
Patch610:       0011-x86-insn-Add-insn_has_rep_prefix-helper.patch
Patch611:       0012-x86-boot-compressed-64-Disable-red-zone-usage.patch
Patch612:       0013-x86-boot-compressed-64-Add-IDT-Infrastructure.patch
Patch613:       0014-x86-boot-compressed-64-Rename-kaslr_64.c-to-ident_ma.patch
Patch614:       0015-x86-boot-compressed-64-Add-page-fault-handler.patch
Patch615:       0016-x86-boot-compressed-64-Always-switch-to-own-page-tab.patch
Patch616:       0017-x86-boot-compressed-64-Don-t-pre-map-memory-in-KASLR.patch
Patch617:       0018-x86-boot-compressed-64-Change-add_identity_map-to-ta.patch
Patch618:       0019-x86-boot-compressed-64-Add-stage1-VC-handler.patch
Patch619:       0020-x86-boot-compressed-64-Call-set_sev_encryption_mask-.patch
Patch620:       0021-x86-boot-compressed-64-Check-return-value-of-kernel_.patch
Patch621:       0022-x86-boot-compressed-64-Add-set_page_en-decrypted-hel.patch
Patch622:       0023-x86-boot-compressed-64-Setup-GHCB-Based-VC-Exception.patch
Patch623:       0024-x86-boot-compressed-64-Unmap-GHCB-page-before-bootin.patch
Patch624:       0025-x86-sev-es-Add-support-for-handling-IOIO-exceptions.patch
Patch625:       0026-x86-fpu-Move-xgetbv-xsetbv-into-separate-header.patch
Patch626:       0027-x86-sev-es-Add-CPUID-handling-to-VC-handler.patch
Patch627:       0028-x86-idt-Move-IDT-to-data-segment.patch
Patch628:       0029-x86-idt-Split-idt_data-setup-out-of-set_intr_gate.patch
Patch629:       0030-x86-head-64-Install-startup-GDT.patch
Patch630:       0031-x86-head-64-Setup-MSR_GS_BASE-before-calling-into-C-.patch
Patch631:       0032-x86-head-64-Load-GDT-after-switch-to-virtual-address.patch
Patch632:       0033-x86-head-64-Load-segment-registers-earlier.patch
Patch633:       0034-x86-head-64-Switch-to-initial-stack-earlier.patch
Patch634:       0035-x86-head-64-Make-fixup_pointer-static-inline.patch
Patch635:       0036-x86-head-64-Load-IDT-earlier.patch
Patch636:       0037-x86-head-64-Move-early-exception-dispatch-to-C-code.patch
Patch637:       0038-x86-head-64-Set-CR4.FSGSBASE-early.patch
Patch638:       0039-x86-sev-es-Add-SEV-ES-Feature-Detection.patch
Patch639:       0040-x86-sev-es-Print-SEV-ES-info-into-kernel-log.patch
Patch640:       0041-x86-sev-es-Compile-early-handler-code-into-kernel-im.patch
Patch641:       0042-x86-sev-es-Setup-early-VC-handler.patch
Patch642:       0043-x86-sev-es-Setup-GHCB-based-boot-VC-handler.patch
Patch643:       0044-x86-sev-es-Setup-per-cpu-GHCBs-for-the-runtime-handl.patch
Patch644:       0045-x86-sev-es-Allocate-and-Map-IST-stack-for-VC-handler.patch
Patch645:       0046-x86-sev-es-Adjust-VC-IST-Stack-on-entering-NMI-handl.patch
Patch646:       0047-x86-dumpstack-64-Add-noinstr-version-of-get_stack_in.patch
Patch647:       0048-x86-entry-64-Add-entry-code-for-VC-handler.patch
Patch648:       0049-x86-sev-es-Add-Runtime-VC-Exception-Handler.patch
Patch649:       0050-x86-sev-es-Wire-up-existing-VC-exit-code-handlers.patch
Patch650:       0051-x86-sev-es-Handle-instruction-fetches-from-user-spac.patch
Patch651:       0052-x86-sev-es-Handle-MMIO-events.patch
Patch652:       0053-x86-sev-es-Handle-MMIO-String-Instructions.patch
Patch653:       0054-x86-sev-es-Handle-MSR-events.patch
Patch654:       0055-x86-sev-es-Handle-DR7-read-write-events.patch
Patch655:       0056-x86-sev-es-Handle-WBINVD-Events.patch
Patch656:       0057-x86-sev-es-Handle-RDTSC-P-Events.patch
Patch657:       0058-x86-sev-es-Handle-RDPMC-Events.patch
Patch658:       0059-x86-sev-es-Handle-INVD-Events.patch
Patch659:       0060-x86-sev-es-Handle-MONITOR-MONITORX-Events.patch
Patch660:       0061-x86-sev-es-Handle-MWAIT-MWAITX-Events.patch
Patch661:       0062-x86-sev-es-Handle-VMMCALL-Events.patch
Patch662:       0063-x86-sev-es-Handle-AC-Events.patch
Patch663:       0064-x86-sev-es-Handle-DB-Events.patch
Patch664:       0065-x86-paravirt-Allow-hypervisor-specific-VMMCALL-handl.patch
Patch665:       0066-x86-kvm-Add-KVM-specific-VMMCALL-handling-under-SEV-.patch
Patch666:       0067-x86-vmware-Add-VMware-specific-handling-for-VMMCALL-.patch
Patch667:       0068-x86-realmode-Add-SEV-ES-specific-trampoline-entry-po.patch
Patch668:       0069-x86-realmode-Setup-AP-jump-table.patch
Patch669:       0070-x86-smpboot-Setup-TSS-for-starting-AP.patch
Patch670:       0071-x86-head-64-Don-t-call-verify_cpu-on-starting-APs.patch
Patch671:       0072-x86-head-64-Rename-start_cpu0.patch
Patch672:       0073-x86-sev-es-Support-CPU-offline-online.patch
Patch673:       0074-x86-sev-es-Handle-NMI-State.patch
Patch674:       0075-x86-efi-Add-GHCB-mappings-when-SEV-ES-is-active.patch
Patch675:       0076-x86-sev-es-Check-required-CPU-features-for-SEV-ES.patch
Patch676:       0079-x86-sev-es-Disable-BIOS-ACPI-RSDP-probing-if-SEV-ES-.patch
Patch677:       0080-x86-boot-Enable-vmw-serial-port-via-Super-I-O.patch
Patch678:       0081-x86-sev-es-Disable-use-of-WP-via-PAT-for-__sme_early.patch
Patch679:       0082-x86-sev-es-load-idt-before-entering-long-mode-to-han.patch

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
Requires:      filesystem kmod
Requires(pre): (coreutils or toybox)
Requires(preun): (coreutils or toybox)
Requires(post):(coreutils or toybox)
Requires(postun):(coreutils or toybox)

%description
The Linux kernel build for GOS for VMware hypervisor.

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
%setup -q -n linux-%{version}

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1

# VMW
%patch30 -p1
%patch31 -p1
%patch32 -p1

# -esx
%patch50 -p1
%patch51 -p1
%patch52 -p1
%patch53 -p1
%patch54 -p1
%patch55 -p1
%patch56 -p1
#%patch57 -p1
%patch58 -p1
%patch59 -p1
%patch60 -p1
%patch61 -p1
%patch62 -p1

# CVE
%patch100 -p1
%patch101 -p1
%patch102 -p1

# crypto
%patch500 -p1
%patch501 -p1

%if 0%{?kat_build:1}
%patch510 -p1
%endif

# SEV
%patch600 -p1
%patch601 -p1
%patch602 -p1
%patch603 -p1
%patch604 -p1
%patch605 -p1
%patch606 -p1
%patch607 -p1
%patch608 -p1
%patch609 -p1
%patch610 -p1
%patch611 -p1
%patch612 -p1
%patch613 -p1
%patch614 -p1
%patch615 -p1
%patch616 -p1
%patch617 -p1
%patch618 -p1
%patch619 -p1
%patch620 -p1
%patch621 -p1
%patch622 -p1
%patch623 -p1
%patch624 -p1
%patch625 -p1
%patch626 -p1
%patch627 -p1
%patch628 -p1
%patch629 -p1
%patch630 -p1
%patch631 -p1
%patch632 -p1
%patch633 -p1
%patch634 -p1
%patch635 -p1
%patch636 -p1
%patch637 -p1
%patch638 -p1
%patch639 -p1
%patch640 -p1
%patch641 -p1
%patch642 -p1
%patch643 -p1
%patch644 -p1
%patch645 -p1
%patch646 -p1
%patch647 -p1
%patch648 -p1
%patch649 -p1
%patch650 -p1
%patch651 -p1
%patch652 -p1
%patch653 -p1
%patch654 -p1
%patch655 -p1
%patch656 -p1
%patch657 -p1
%patch658 -p1
%patch659 -p1
%patch660 -p1
%patch661 -p1
%patch662 -p1
%patch663 -p1
%patch664 -p1
%patch665 -p1
%patch666 -p1
%patch667 -p1
%patch668 -p1
%patch669 -p1
%patch670 -p1
%patch671 -p1
%patch672 -p1
%patch673 -p1
%patch674 -p1
%patch675 -p1
%patch676 -p1
%patch677 -p1
%patch678 -p1
%patch679 -p1

%build
make mrproper
cp %{SOURCE1} .config
sed -i 's/CONFIG_LOCALVERSION="-esx"/CONFIG_LOCALVERSION="-%{release}-esx"/' .config

%include %{SOURCE4}

make VERBOSE=1 KBUILD_BUILD_VERSION="1-photon" KBUILD_BUILD_HOST="photon" ARCH="x86_64" %{?_smp_mflags}

# Do not compress modules which will be loaded at boot time
# to speed up boot process
%define __modules_install_post \
    find %{buildroot}/lib/modules/%{uname_r} -name "*.ko" \! \"(" -name "*evdev*" -o -name "*mousedev*" -o -name "*sr_mod*"  -o -name "*cdrom*" -o -name "*vmwgfx*" -o -name "*drm_kms_helper*" -o -name "*ttm*" -o -name "*psmouse*" -o -name "*drm*" -o -name "*apa_piix*" -o -name "*vmxnet3*" -o -name "*i2c_core*" -o -name "*libata*" -o -name "*processor*" -o -path "*ipv6*" \")" | xargs xz \
%{nil}

# We want to compress modules after stripping. Extra step is added to
# the default __spec_install_post.
%define __spec_install_post\
    %{?__debug_package:%{__debug_install_post}}\
    %{__arch_install_post}\
    %{__os_install_post}\
    %{__modules_install_post}\
%{nil}

%install
install -vdm 755 %{buildroot}%{_sysconfdir}
install -vdm 755 %{buildroot}/boot
install -vdm 755 %{buildroot}%{_docdir}/linux-%{uname_r}
install -vdm 755 %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}
make INSTALL_MOD_PATH=%{buildroot} modules_install

install -vm 644 arch/x86/boot/bzImage %{buildroot}/boot/vmlinuz-%{uname_r}
install -vm 400 System.map %{buildroot}/boot/System.map-%{uname_r}
install -vm 644 .config %{buildroot}/boot/config-%{uname_r}
cp -r Documentation/*        %{buildroot}%{_docdir}/linux-%{uname_r}
install -vdm 755 %{buildroot}/usr/lib/debug/lib/modules/%{uname_r}
install -vm 644 vmlinux %{buildroot}/usr/lib/debug/lib/modules/%{uname_r}/vmlinux-%{uname_r}

# TODO: noacpi acpi=off noapic pci=conf1,nodomains pcie_acpm=off pnpacpi=off
cat > %{buildroot}/boot/linux-%{uname_r}.cfg << "EOF"
# GRUB Environment Block
photon_cmdline=init=/lib/systemd/systemd rcupdate.rcu_expedited=1 rw systemd.show_status=0 quiet noreplace-smp cpu_init_udelay=0
photon_linux=vmlinuz-%{uname_r}
photon_initrd=initrd.img-%{uname_r}
EOF

# Register myself to initramfs
mkdir -p %{buildroot}/%{_localstatedir}/lib/initramfs/kernel
cat > %{buildroot}/%{_localstatedir}/lib/initramfs/kernel/%{uname_r} << "EOF"
--add-drivers "lvm dm-mod"
EOF

# cleanup dangling symlinks
rm -f %{buildroot}/lib/modules/%{uname_r}/source
rm -f %{buildroot}/lib/modules/%{uname_r}/build

# create /use/src/linux-headers-*/ content
find . -name Makefile* -o -name Kconfig* -o -name *.pl | xargs  sh -c 'cp --parents "$@" %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}' copy
find arch/x86/include include scripts -type f | xargs  sh -c 'cp --parents "$@" %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}' copy
find $(find arch/x86 -name include -o -name scripts -type d) -type f | xargs  sh -c 'cp --parents "$@" %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}' copy
find arch/x86/include Module.symvers include scripts -type f | xargs  sh -c 'cp --parents "$@" %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}' copy

# copy .config manually to be where it's expected to be
cp .config %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}
# symling to the build folder
ln -sf "%{_usrsrc}/linux-headers-%{uname_r}" "%{buildroot}/lib/modules/%{uname_r}/build"
find %{buildroot}/lib/modules -name '*.ko' -print0 | xargs -0 chmod u+x

%include %{SOURCE2}
%include %{SOURCE3}

%post
/sbin/depmod -a %{uname_r}
ln -sf linux-%{uname_r}.cfg /boot/photon.cfg

%files
%defattr(-,root,root)
/boot/System.map-%{uname_r}
/boot/config-%{uname_r}
/boot/vmlinuz-%{uname_r}
%config(noreplace) /boot/linux-%{uname_r}.cfg
%config %{_localstatedir}/lib/initramfs/kernel/%{uname_r}
/lib/modules/*
%exclude /lib/modules/%{uname_r}/build

%files docs
%defattr(-,root,root)
%{_defaultdocdir}/linux-%{uname_r}/*

%files devel
%defattr(-,root,root)
/lib/modules/%{uname_r}/build
%{_usrsrc}/linux-headers-%{uname_r}

%changelog
*   Tue Nov 03 2020 Srinidhi Rao <srinidhir@vmware.com> 5.9.0-3
-   Remove the support of fipsify and hmacgen
*   Tue Oct 27 2020 Srinidhi Rao <srinidhir@vmware.com> 5.9.0-2
-   Enable vtarfs support as module
*   Mon Oct 19 2020 Bo Gan <ganb@vmware.com> 5.9.0-1
-   Update to 5.9.0
*   Thu Oct 08 2020 Ankit Jain <ankitja@vmware.com> 5.9.0-rc7.2
-   Added vtar Support.
-   Disabled by default, Enable CONFIG_VTAR as builtin only
*   Wed Sep 30 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.9.0-rc7.1
-   Update to version 5.9.0-rc7
*   Mon Sep 21 2020 Bo Gan <ganb@vmware.com> 5.9.0-rc4.1
-   Update to 5.9.0-rc4
-   AMD SEV-ES Support
*   Tue Sep 8 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.127-4
-   Enable sysrq magic in config
*   Mon Jul 27 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.127-3
-   Fix CVE-2020-14331
*   Tue Jun 23 2020 Tapas Kundu <tkundu@vmware.com> 4.19.127-2
-   Mass Removal Python2
*   Tue Jun 23 2020 Keerthana K <keerthanak@vmware.com> 4.19.127-1
-   Update to version 4.19.127
*   Fri Jun 05 2020 Ankit Jain <ankitja@vmware.com> 4.19.115-5
-   Enabled CONFIG_BINFMT_MISC
*   Wed Jun 03 2020 Alexey Makhalov <amakhalov@vmware.com> 4.19.115-4
-   fs/9p: local lock support
*   Tue Jun 02 2020 Vikash Bansal <bvikas@vmware.com> 4.19.115-3
-   Add patch to fix CVE-2019-18885
*   Mon Jun 01 2020 Shreenidhi Shedi <sshedi@vmware.com> 4.19.115-2
-   Keep modules of running kernel till next boot
*   Fri May 29 2020 Alexey Makhalov <amakhalov@vmware.com> 4.19.115-1
-   initramfs: zero-copy support
*   Wed May 06 2020 Siddharth Chandrasekaran <csiddharth@vmware.com> 4.19.112-9
-   Add patch to fix CVE-2020-10711
*   Wed May 06 2020 Vikash Bansal <bvikas@vmware.com> 4.19.112-8
-   Hardcoded the value of BARs in PCI_Probe for 2 more pci devices
*   Wed Apr 29 2020 Keerthana K <keerthanak@vmware.com> 4.19.112-7
-   Photon-checksum-generator version update to 1.1.
*   Fri Apr 24 2020 Vikash Bansal <bvikas@vmware.com> 4.19.112-6
-   Modified PCI Probe patch to store hardcoded values in lookup table
*   Thu Apr 23 2020 Keerthana K <keerthanak@vmware.com> 4.19.112-5
-   Fix __modules_install_post to skip compression for certain modules.
*   Wed Apr 22 2020 Vikash Bansal <bvikas@vmware.com> 4.19.112-4
-   Corrected number of bars for "LSI Logic" and typepo in is_known_device call
*   Wed Apr 15 2020 Vikash Bansal <bvikas@vmware.com> 4.19.112-3
-   HMAC-SHA256 digest of hmac_generator module moved to hmacgen package
*   Tue Apr 14 2020 Alexey Makhalov <amakhalov@vmware.com> 4.19.112-2
-   Refactor PCI probe patch (03-pci-probe.patch)
*   Wed Apr 08 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.112-1
-   Update to version 4.19.112
*   Wed Apr 08 2020 Alexey Makhalov <amakhalov@vmware.com> 4.19.104-3
-   Improve hardcodded poweroff (03-poweroff.patch)
*   Tue Mar 31 2020 Vikash Bansal <bvikas@vmware.com> 4.19.104-2
-   hmac generation of crypto modules and initrd generation changes if fips=1
*   Wed Mar 25 2020 Vikash Bansal <bvikas@vmware.com> 4.19.104-1
-   Update to version 4.19.104
*   Mon Mar 16 2020 Keerthana K <keerthanak@vmware.com> 4.19.97-8
-   Adding Enhances depedency to hmacgen.
*   Fri Mar 06 2020 Alexey Makhalov <amakhalov@vmware.com> 4.19.97-7
-   9p: file attributes caching support (cache=stat)
*   Wed Mar 04 2020 Vikash Bansal <bvikas@vmware.com> 4.19.97-6
-   Backporting of patch continuous testing of RNG from urandom
*   Fri Feb 28 2020 Keerthana K <keerthanak@vmware.com> 4.19.97-5
-   Enable CONFIG_CRYPT_TEST for FIPS.
*   Tue Feb 25 2020 Ajay Kaher <akaher@vmware.com> 4.19.97-4
-   Fix CVE-2019-16234
*   Tue Feb 11 2020 Keerthana K <keerthanak@vmware.com> 4.19.97-3
-   Add photon-checksum-generator source tarball and remove hmacgen patch.
-   Exclude hmacgen.ko from base package.
*   Wed Jan 29 2020 Keerthana K <keerthanak@vmware.com> 4.19.97-2
-   Update tcrypt to test drbg_pr_sha256 and drbg_nopr_sha256.
-   Update testmgr to add drbg_pr_ctr_aes256 test vectors.
*   Fri Jan 17 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.97-1
-   Update to version 4.19.97
*   Thu Jan 16 2020 Srinidhi Rao <srinidhir@vmware.com> 4.19.87-5
-   Enable DRBG HASH and DRBG CTR support.
*   Mon Jan 06 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.87-4
-   Enable CONFIG_NF_CONNTRACK_ZONES
*   Thu Jan 02 2020 Keerthana K <keerthanak@vmware.com> 4.19.87-3
-   Modify tcrypt to remove tests for algorithms that are not supported in photon.
-   Added tests for DH, DRBG algorithms.
*   Fri Dec 20 2019 Keerthana K <keerthanak@vmware.com> 4.19.87-2
-   Update fips Kat tests.
*   Fri Dec 06 2019 Ajay Kaher <akaher@vmware.com> 4.19.87-1
-   Update to version 4.19.87
*   Tue Dec 03 2019 Keerthana K <keerthanak@vmware.com> 4.19.84-3
-   Adding hmac sha256/sha512 generator kernel module for fips.
*   Tue Nov 26 2019 Ajay Kaher <akaher@vmware.com> 4.19.84-2
-   Fix CVE-2019-19062, CVE-2019-19066, CVE-2019-19072,
-   CVE-2019-19073, CVE-2019-19074, CVE-2019-19078
*   Tue Nov 12 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.84-1
-   Update to version 4.19.84
-   Fix CVE-2019-18814
*   Fri Nov 08 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.82-1
-   Update to version 4.19.82
*   Thu Nov 07 2019 Jorgen Hansen (VMware) <jhansen@vmware.com> 4.19.79-2
-   Fix vsock QP detach with outgoing data
*   Tue Oct 15 2019 Ajay Kaher <akaher@vmware.com> 4.19.79-1
-   Update to version 4.19.79
-   Fix CVE-2019-17133
*   Mon Oct 14 2019 Bo Gan <ganb@vmware.com> 4.19.76-4
-   Recreate /dev/root in init
*   Mon Oct 14 2019 Bo Gan <ganb@vmware.com> 4.19.76-3
-   Enable IMA with SHA256 as default hash algorithm
*   Thu Oct 10 2019 Harinadh D <hdommaraju@vmware.com> 4.19.76-2
-   Adding lvm and dm-mod modules to support root as lvm
*   Wed Oct 02 2019 Ajay Kaher <akaher@vmware.com> 4.19.76-1
-   Update to version 4.19.76
*   Mon Sep 30 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.72-1
-   Update to version 4.19.72
*   Thu Sep 05 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.69-2
-   Avoid oldconfig which leads to potential build hang
*   Fri Aug 30 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.69-1
-   Update to version 4.19.69
*   Fri Aug 23 2019 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.65-3
-   .config: Enable CONFIG_IP_VS_WRR, CONFIG_IP_VS_SH, CONFIG_FB_EFI, CONFIG_TCG_TIS_CORE
*   Tue Aug 13 2019 Daniel Müller <danielmuller@vmware.com> 4.19.65-2
-   Add patch "Remove OOM_SCORE_ADJ_MAX limit check"
*   Tue Aug 06 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.65-1
-   Update to version 4.19.65
-   Fix CVE-2019-1125 (SWAPGS)
*   Tue Jul 30 2019 Keerthana K <keerthanak@vmware.com> 4.19.52-4
-   Fix postun script.
*   Tue Jul 02 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.52-3
-   Fix 9p vsock 16bit port issue.
*   Fri Jun 21 2019 Srinidhi Rao <srinidhir@vmware.com> 4.19.52-2
-   Use LZ4 compression and enable VMXNET3 as built-in for linux-esx
*   Mon Jun 17 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.52-1
-   Update to version 4.19.52
-   Fix CVE-2019-12456, CVE-2019-12379, CVE-2019-12380, CVE-2019-12381,
-   CVE-2019-12382, CVE-2019-12378, CVE-2019-12455
*   Tue May 14 2019 Keerthana K <keerthanak@vmware.com> 4.19.40-2
-   Fix to parse through /boot folder and update symlink (/boot/photon.cfg) if
-   mulitple kernels are installed and current linux kernel is removed.
*   Tue May 07 2019 Ajay Kaher <akaher@vmware.com> 4.19.40-1
-   Update to version 4.19.40
*   Fri May 03 2019 Ajay Kaher <akaher@vmware.com> 4.19.32-3
-   Enable SELinux kernel config
*   Fri Mar 29 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.32-2
-   Fix CVE-2019-10125
*   Wed Mar 27 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.32-1
-   Update to version 4.19.32
*   Thu Mar 14 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.29-1
-   Update to version 4.19.29
*   Tue Mar 05 2019 Ajay Kaher <akaher@vmware.com> 4.19.26-1
-   Update to version 4.19.26
*   Thu Feb 21 2019 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.15-2
-   Fix CVE-2019-8912
*   Tue Jan 15 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.15-1
-   Update to version 4.19.15
-   .config: Enable USB_SERIAL and USB_ACM
*   Tue Jan 08 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.6-4
-   Additional security hardening options in the config.
*   Tue Jan 08 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.6-3
-   Fix crash on cpu hot-add.
*   Fri Jan 04 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.6-2
-   Add out-of-tree patches from AppArmor and enable it by default.
*   Mon Dec 10 2018 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.6-1
-   Update to version 4.19.6
*   Thu Nov 29 2018 Alexey Makhalov <amakhalov@vmware.com> 4.19.1-3
-   Fix BAR4 is zero issue for IDE devices
*   Thu Nov 15 2018 Ajay Kaher <akaher@vmware.com> 4.19.1-2
-   Adding BuildArch
*   Thu Nov 08 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.1-1
-   Update to version 4.19.1
*   Mon Sep 24 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.18.9-1
-   Update to version 4.18.9
*   Wed Sep 19 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.14.67-1
-   Update to version 4.14.67
*   Tue Sep 18 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.14.54-3
-   Add rdrand-based RNG driver to enhance kernel entropy.
*   Sun Sep 02 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.14.54-2
-   Add full retpoline support by building with retpoline-enabled gcc.
*   Mon Jul 09 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.14.54-1
-   Update to version 4.14.54
*   Fri Feb 02 2018 Alexey Makhalov <amakhalov@vmware.com> 4.14.8-1
-   Version update
*   Tue Dec 19 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.66-2
-   Enable audit support (CONFIG_AUDIT=y)
*   Mon Dec 04 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.66-1
-   Version update
*   Tue Nov 21 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.64-1
-   Version update
*   Mon Nov 06 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.60-1
-   Version update
*   Wed Oct 25 2017 Anish Swaminathan <anishs@vmware.com> 4.9.53-5
-   Enable x86 vsyscall emulation
*   Tue Oct 17 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.53-4
-   Enable vsyscall emulation
-   Do not use deprecated -q depmod option
*   Wed Oct 11 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.53-3
-   Add patch "KVM: Don't accept obviously wrong gsi values via
    KVM_IRQFD" to fix CVE-2017-1000252.
*   Tue Oct 10 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.53-2
-   Build hang (at make oldconfig) fix.
*   Thu Oct 05 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.53-1
-   Version update
*   Mon Oct 02 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.52-3
-   Allow privileged CLONE_NEWUSER from nested user namespaces.
*   Mon Oct 02 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.52-2
-   Fix CVE-2017-11472 (ACPICA: Namespace: fix operand cache leak)
*   Mon Oct 02 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.52-1
-   Version update
*   Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.47-2
-   Requires coreutils or toybox
*   Mon Sep 04 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.47-1
-   Fix CVE-2017-11600
*   Mon Aug 14 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.43-1
-   Version update
-   [feature] new sysctl option unprivileged_userns_clone
*   Wed Aug 09 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.41-2
-   [bugfix] Do not fallback to syscall from VDSO on clock_gettime(MONOTONIC)
-   Fix CVE-2017-7542
*   Mon Aug 07 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.41-1
-   Version update
*   Wed Jul 26 2017 Bo Gan <ganb@vmware.com> 4.9.38-3
-   Fix initramfs triggers
*   Thu Jul 20 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.38-2
-   Disable scheduler beef up patch
*   Tue Jul 18 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.38-1
-   [feature] IP tunneling support (CONFIG_NET_IPIP=m)
-   Fix CVE-2017-11176 and CVE-2017-10911
*   Mon Jul 03 2017 Xiaolin Li <xiaolinl@vmware.com> 4.9.34-2
-   Add libdnet-devel, kmod-devel and libmspack-devel to BuildRequires
*   Wed Jun 28 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.34-1
-   [feature] DM Delay target support
-   Fix CVE-2017-1000364 ("stack clash") and CVE-2017-9605
*   Thu Jun 8 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.31-1
-   Fix CVE-2017-8890, CVE-2017-9074, CVE-2017-9075, CVE-2017-9076
    CVE-2017-9077 and CVE-2017-9242
*   Thu Jun 1 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.30-2
-   [feature] ACPI NFIT support (for PMEM type 7)
*   Fri May 26 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.30-1
-   Fix CVE-2017-7487 and CVE-2017-9059
*   Wed May 17 2017 Vinay Kulkarni <kulkarniv@vmware.com> 4.9.28-2
-   Enable IPVLAN module.
*   Tue May 16 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.28-1
-   .config: built ATA drivers in a kernel
*   Wed May 10 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.27-1
-   New pci=scan_all cmdline parameter to verify hardcoded pci-probe values
-   pci-probe added more known values
-   vmw_balloon late initcall
*   Sun May 7 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.26-1
-   Version update
-   Use ordered rdtsc in clocksource_vmware
-   .config: added debug info
-   Removed version suffix from config file name
*   Thu Apr 27 2017 Bo Gan <ganb@vmware.com> 4.9.24-2
-   Support dynamic initrd generation
*   Tue Apr 25 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.24-1
-   Fix CVE-2017-6874 and CVE-2017-7618.
-   .config: build nvme and nvme-core in kernel.
*   Tue Feb 28 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.13-1
-   Update to linux-4.9.13 to fix CVE-2017-5986 and CVE-2017-6074
-   .config: enable PMEM support
-   .config: disable vsyscall
*   Thu Feb 09 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.9-1
-   Update to linux-4.9.9 to fix CVE-2016-10153, CVE-2017-5546,
    CVE-2017-5547, CVE-2017-5548 and CVE-2017-5576.
-   .config: added CRYPTO_FIPS and SYN_COOKIES support.
*   Tue Jan 10 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.2-1
-   Update to linux-4.9.2 to fix CVE-2016-10088
*   Wed Dec 21 2016 Alexey Makhalov <amakhalov@vmware.com> 4.9.0-3
-   .config: CONFIG_IPV6_MULTIPLE_TABLES=y
*   Mon Dec 19 2016 Xiaolin Li <xiaolinl@vmware.com> 4.9.0-2
-   BuildRequires Linux-PAM-devel
*   Mon Dec 12 2016 Alexey Makhalov <amakhalov@vmware.com> 4.9.0-1
-   Update to linux-4.9.0
*   Thu Dec  8 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.35-4
-   net-packet-fix-race-condition-in-packet_set_ring.patch
    to fix CVE-2016-8655
*   Wed Nov 30 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.35-3
-   Expand `uname -r` with release number
-   Compress modules
*   Tue Nov 29 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.35-2
-   Added btrfs module
*   Mon Nov 28 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.35-1
-   Update to linux-4.4.35
-   vfio-pci-fix-integer-overflows-bitmask-check.patch
    to fix CVE-2016-9083
*   Tue Nov 22 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.31-4
-   net-9p-vsock.patch
*   Thu Nov 17 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.31-3
-   tty-prevent-ldisc-drivers-from-re-using-stale-tty-fields.patch
    to fix CVE-2015-8964
*   Tue Nov 15 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.31-2
-   .config: add ip set support
-   .config: add ipvs_{tcp,udp} support
-   .config: add cgrup_{hugetlb,net_prio} support
*   Thu Nov 10 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.31-1
-   Update to linux-4.4.31
*   Thu Nov 10 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.26-2
-   .config: add ipvs modules for docker swarm
-   .config: serial driver built in kernel
-   serial-8250-do-not-probe-U6-16550A-fifo-size.patch - faster boot
*   Fri Oct 21 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.26-1
-   Update to linux-4.4.26
*   Wed Oct 19 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.20-7
-   net-add-recursion-limit-to-GRO.patch
*   Tue Oct 18 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.20-6
-   ipip-properly-mark-ipip-GRO-packets-as-encapsulated.patch
-   tunnels-dont-apply-GRO-to-multiple-layers-of-encapsulation.patch
*   Thu Oct  6 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.20-5
-   .config: added ADM PCnet32 support
-   vmci-1.1.4.0-use-32bit-atomics-for-queue-headers.patch
-   vmci-1.1.5.0-doorbell-create-and-destroy-fixes.patch
-   late_initcall for vmw_balloon driver
-   Minor fixed in pv-ops patchset
*   Mon Oct  3 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.20-4
-   Package vmlinux with PROGBITS sections in -debuginfo subpackage
*   Wed Sep 21 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.20-3
-   Add PCIE hotplug support
-   Switch processor type to generic
*   Tue Sep 20 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.20-2
-   Add -release number for /boot/* files
-   Fixed generation of debug symbols for kernel modules & vmlinux
*   Wed Sep  7 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.20-1
-   Update to linux-4.4.20
-   keys-fix-asn.1-indefinite-length-object-parsing.patch
*   Thu Aug 25 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-11
-   vmxnet3 patches to bumpup a version to 1.4.8.0
*   Wed Aug 24 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-10
-   .config: added NVME blk dev support
*   Wed Aug 10 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-9
-   Added VSOCK-Detach-QP-check-should-filter-out-non-matching-QPs.patch
*   Wed Jul 20 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-8
-   .config: added cgroups for pids,mem and blkio
*   Mon Jul 11 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-7
-   .config: added ip multible tables support
*   Fri Jun 17 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-6
-   patch: e1000e-prevent-div-by-zero-if-TIMINCA-is-zero.patch
-   .config: disable rt group scheduling - not supported by systemd
*   Fri May 27 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-5
-   patch: REVERT-sched-fair-Beef-up-wake_wide.patch
*   Wed May 25 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-4
-   .config: added net_9p and 9p_fs
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.4.8-3
-   GA - Bump release of all rpms
*   Mon May 23 2016 Divya Thaluru <dthaluru@vmware.com> 4.4.8-2
-   Added patches to fix CVE-2016-3134, CVE-2016-3135
*   Fri May 13 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-1
-   Update to linux-4.4.8
-   Added net-Drivers-Vmxnet3-set-... patch
-   Added e1000e module
*   Tue Mar 29 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-19
-   Support kmsg dumping to vmware.log on panic
-   sunrpc: xs_bind uses ip_local_reserved_ports
*   Thu Mar 24 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-18
-   Apply photon8 config (+stack protector regular)
-   pv-ops patch: added STA support
-   Added patches from generic kernel
*   Wed Mar 09 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.2.0-17
-   Enable ACPI hotplug support in kernel config
*   Sun Feb 14 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-16
-   veth patch: don’t modify ip_summed
*   Mon Feb 08 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-15
-   Double tcp_mem limits, patch is added.
*   Wed Feb 03 2016 Anish Swaminathan <anishs@vmware.com>  4.2.0-14
-   Fixes for CVE-2015-7990/6937 and CVE-2015-8660.
*   Fri Jan 22 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-13
-   Fix for CVE-2016-0728
*   Wed Jan 13 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-12
-   CONFIG_HZ=250
-   Disable sched autogroup.
*   Tue Jan 12 2016 Mahmoud Bassiouny <mbassiouny@vmware.com> 4.2.0-11
-   Remove rootfstype from the kernel parameter.
*   Tue Dec 15 2015 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-10
-   Skip rdrand reseed to improve boot time.
-   .config changes: jolietfs(m), default THP=always, hotplug_cpu(m)
*   Tue Nov 17 2015 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-9
-   nordrand cmdline param is removed.
-   .config: + serial 8250 driver (M).
*   Fri Nov 13 2015 Mahmoud Bassiouny <mbassiouny@vmware.com> 4.2.0-8
-   Change the linux image directory.
*   Tue Nov 10 2015 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-7
-   Get LAPIC timer frequency from HV, skip boot time calibration.
-   .config: + dummy net driver (M).
*   Mon Nov 09 2015 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-6
-   Rename subpackage dev -> devel.
-   Added the build essential files in the devel subpackage.
-   .config: added genede driver module.
*   Wed Oct 28 2015 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-5
-   Import patches from kernel2 repo.
-   Added pv-ops patch (timekeeping related improvements).
-   Removed unnecessary cmdline params.
-   .config changes: elevator=noop by default, paravirt clock enable,
    initrd support, openvswitch module, x2apic enable.
*   Mon Sep 21 2015 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-4
-   CDROM modules are added.
*   Thu Sep 17 2015 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-3
-   Fix for 05- patch (SVGA mem size)
-   Compile out: pci hotplug, sched smt.
-   Compile in kernel: vmware balloon & vmci.
-   Module for efi vars.
*   Fri Sep 4 2015 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-2
-   Hardcoded poweroff (direct write to piix4), no ACPI is required.
-   sd.c: Lower log level for "Assuming drive cache..." message.
*   Tue Sep 1 2015 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-1
-   Update to linux-4.2.0. Enable CONFIG_EFI
*   Fri Aug 28 2015 Alexey Makhalov <amakhalov@vmware.com> 4.1.3-5
-   Added MD/LVM/DM modules.
-   Pci probe improvements.
*   Fri Aug 14 2015 Alexey Makhalov <amakhalov@vmware.com> 4.1.3-4
-   Use photon.cfg as a symlink.
*   Thu Aug 13 2015 Alexey Makhalov <amakhalov@vmware.com> 4.1.3-3
-   Added environment file(photon.cfg) for a grub.
*   Tue Aug 11 2015 Alexey Makhalov <amakhalov@vmware.com> 4.1.3-2
    Added pci-probe-vmware.patch. Removed unused modules. Decreased boot time.
*   Tue Jul 28 2015 Alexey Makhalov <amakhalov@vmware.com> 4.1.3-1
    Initial commit. Use patchset from Clear Linux.

