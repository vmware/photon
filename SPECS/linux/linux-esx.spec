%global security_hardening none
Summary:       Kernel
Name:          linux-esx
Version:       4.4.140
Release:       1%{?dist}
License:       GPLv2
URL:           http://www.kernel.org/
Group:         System Environment/Kernel
Vendor:        VMware, Inc.
Distribution:  Photon
Source0:       http://www.kernel.org/pub/linux/kernel/v4.x/linux-%{version}.tar.xz
%define sha1 linux=55dc1299e981cb4ef8ef0c92a4df52c2f4df4835
Source1:       config-esx
Patch0:        double-tcp_mem-limits.patch
Patch1:        linux-4.4-sysctl-sched_weighted_cpuload_uses_rla.patch
Patch2:        linux-4.4-watchdog-Disable-watchdog-on-virtual-machines.patch
Patch3:        SUNRPC-Do-not-reuse-srcport-for-TIME_WAIT-socket.patch
Patch4:        vmxnet3-1.4.6.0-update-rx-ring2-max-size.patch
Patch5:        01-clear-linux.patch
Patch6:        02-pci-probe.patch
Patch7:        03-poweroff.patch
Patch8:        04-quiet-boot.patch
Patch9:        05-pv-ops.patch
Patch10:       06-sunrpc.patch
Patch11:       vmxnet3-1.4.6.0-avoid-calling-pskb_may_pull-with-interrupts-disabled.patch
Patch12:       kprobes-x86-Do-not-modify-singlestep-buffer-while-re.patch
Patch13:       REVERT-sched-fair-Beef-up-wake_wide.patch
Patch14:       e1000e-prevent-div-by-zero-if-TIMINCA-is-zero.patch

Patch16:       vmxnet3-1.4.6.0-fix-lock-imbalance-in-vmxnet3_tq_xmit.patch
Patch17:       vmxnet3-1.4.7.0-set-CHECKSUM_UNNECESSARY-for-IPv6-packets.patch
Patch18:       vmxnet3-1.4.8.0-segCnt-can-be-1-for-LRO-packets.patch
Patch19:       serial-8250-do-not-probe-U6-16550A-fifo-size.patch
Patch20:       vmci-1.1.4.0-use-32bit-atomics-for-queue-headers.patch
Patch21:       vmci-1.1.5.0-doorbell-create-and-destroy-fixes.patch
Patch22:       vsock-transport-for-9p.patch
Patch23:       p9fs_dir_readdir-offset-support.patch
Patch24:       Implement-the-f-xattrat-family-of-functions.patch
Patch26:       init-do_mounts-recreate-dev-root.patch
# Fixes for CVE-2018-1000026
Patch27:       0001-net-create-skb_gso_validate_mac_len.patch
Patch28:       0002-bnx2x-disable-GSO-where-gso_size-is-too-big-for-hard.patch
# Fix for CVE-2018-8043
Patch30:       0001-net-phy-mdio-bcm-unimac-fix-potential-NULL-dereferen.patch
# Fix for CVE-2017-18216
Patch31:       0001-ocfs2-subsystem.su_mutex-is-required-while-accessing.patch
# Fix for CVE-2017-18241
Patch33:       0001-f2fs-fix-a-panic-caused-by-NULL-flush_cmd_control.patch
Patch34:       0001-hwrng-rdrand-Add-RNG-driver-based-on-x86-rdrand-inst.patch
# Fix for CVE-2017-18232
Patch35:       0001-scsi-libsas-direct-call-probe-and-destruct.patch
# Fix for CVE-2018-10323
Patch36:       0001-xfs-set-format-back-to-extents-if-xfs_bmap_extents_t.patch
# Fix for CVE-2017-18249 (following 4 patches)
Patch37:       0001-f2fs-cover-more-area-with-nat_tree_lock.patch
Patch38:       0002-Revert-f2fs-check-the-node-block-address-of-newly-al.patch
Patch39:       0003-f2fs-remove-an-obsolete-variable.patch
Patch40:       0004-f2fs-fix-race-condition-in-between-free-nid-allocato.patch

# For Spectre
Patch52: 0141-locking-barriers-introduce-new-observable-speculatio.patch
Patch55: 0144-uvcvideo-prevent-speculative-execution.patch
Patch56: 0145-carl9170-prevent-speculative-execution.patch
Patch57: 0146-p54-prevent-speculative-execution.patch
Patch58: 0147-qla2xxx-prevent-speculative-execution.patch
Patch59: 0148-cw1200-prevent-speculative-execution.patch
Patch60: 0149-Thermal-int340x-prevent-speculative-execution.patch
Patch61: 0150-ipv4-prevent-speculative-execution.patch
Patch62: 0151-ipv6-prevent-speculative-execution.patch
Patch64: 0153-net-mpls-prevent-speculative-execution.patch
Patch65: 0154-udf-prevent-speculative-execution.patch
Patch66: 0155-userns-prevent-speculative-execution.patch
Patch67: 0169-x86-syscall-Clear-unused-extra-registers-on-syscall-.patch

# Add more Spectre-v2 mitigations (IBPB/IBRS)
Patch201: 0001-x86-cpufeature-Move-some-of-the-scattered-feature-bi.patch
Patch202: 0002-x86-cpufeature-Cleanup-get_cpu_cap.patch
Patch205: 0005-x86-cpu-Provide-a-config-option-to-disable-static_cp.patch
Patch206: 0006-x86-fpu-Add-an-XSTATE_OP-macro.patch
Patch207: 0007-x86-fpu-Get-rid-of-xstate_fault.patch
Patch208: 0008-x86-headers-Don-t-include-asm-processor.h-in-asm-ato.patch
Patch209: 0009-x86-cpufeature-Carve-out-X86_FEATURE_.patch
Patch210: 0010-x86-cpufeature-Replace-the-old-static_cpu_has-with-s.patch
Patch211: 0011-x86-cpufeature-Get-rid-of-the-non-asm-goto-variant.patch
Patch212: 0012-x86-alternatives-Add-an-auxilary-section.patch
Patch213: 0013-x86-alternatives-Discard-dynamic-check-after-init.patch
Patch214: 0014-x86-vdso-Use-static_cpu_has.patch
Patch215: 0015-x86-boot-Simplify-kernel-load-address-alignment-chec.patch
Patch216: 0016-x86-cpufeature-Speed-up-cpu_feature_enabled.patch
Patch217: 0017-x86-cpufeature-x86-mm-pkeys-Add-protection-keys-rela.patch
Patch218: 0018-x86-mm-pkeys-Fix-mismerge-of-protection-keys-CPUID-b.patch
Patch219: 0019-x86-cpu-Add-detection-of-AMD-RAS-Capabilities.patch
Patch220: 0020-x86-cpufeature-x86-mm-pkeys-Fix-broken-compile-time-.patch
Patch221: 0021-x86-cpufeature-Update-cpufeaure-macros.patch
Patch222: 0022-x86-cpufeature-Make-sure-DISABLED-REQUIRED-macros-ar.patch
Patch223: 0023-x86-cpufeature-Add-helper-macro-for-mask-check-macro.patch
Patch224: 0024-x86-cpu-Probe-CPUID-leaf-6-even-when-cpuid_level-6.patch
Patch225: 0025-x86-cpufeatures-Add-CPUID_7_EDX-CPUID-leaf.patch
Patch226: 0026-x86-cpufeatures-Add-Intel-feature-bits-for-Speculati.patch
Patch227: 0027-x86-cpufeatures-Add-AMD-feature-bits-for-Speculation.patch
Patch228: 0028-x86-msr-Add-definitions-for-new-speculation-control-.patch
Patch229: 0029-x86-pti-Do-not-enable-PTI-on-CPUs-which-are-not-vuln.patch
Patch230: 0030-x86-cpufeature-Blacklist-SPEC_CTRL-PRED_CMD-on-early.patch
Patch231: 0031-x86-speculation-Add-basic-IBPB-Indirect-Branch-Predi.patch
Patch232: 0032-x86-cpufeatures-Clean-up-Spectre-v2-related-CPUID-fl.patch
Patch233: 0033-x86-cpuid-Fix-up-virtual-IBRS-IBPB-STIBP-feature-bit.patch
Patch234: 0034-x86-pti-Mark-constant-arrays-as-__initconst.patch
Patch235: 0035-x86-asm-entry-32-Simplify-pushes-of-zeroed-pt_regs-R.patch
Patch236: 0036-x86-entry-64-compat-Clear-registers-for-compat-sysca.patch
Patch237: 0037-x86-speculation-Update-Speculation-Control-microcode.patch
Patch238: 0038-x86-speculation-Correct-Speculation-Control-microcod.patch
Patch239: 0039-x86-speculation-Clean-up-various-Spectre-related-det.patch
Patch240: 0040-x86-speculation-Fix-up-array_index_nospec_mask-asm-c.patch
Patch241: 0041-x86-speculation-Add-asm-msr-index.h-dependency.patch
Patch242: 0042-x86-xen-Zero-MSR_IA32_SPEC_CTRL-before-suspend.patch
Patch243: 0043-x86-mm-Factor-out-LDT-init-from-context-init.patch
Patch244: 0044-x86-mm-Give-each-mm-TLB-flush-generation-a-unique-ID.patch
Patch245: 0045-x86-speculation-Use-Indirect-Branch-Prediction-Barri.patch
Patch246: 0046-x86-spectre_v2-Don-t-check-microcode-versions-when-r.patch
Patch247: 0047-x86-speculation-Use-IBRS-if-available-before-calling.patch
Patch248: 0048-x86-speculation-Move-firmware_restrict_branch_specul.patch
Patch249: 0049-x86-speculation-Remove-Skylake-C2-from-Speculation-C.patch
Patch250: 0050-selftest-seccomp-Fix-the-flag-name-SECCOMP_FILTER_FL.patch
Patch251: 0051-selftest-seccomp-Fix-the-seccomp-2-signature.patch
Patch252: 0052-xen-set-cpu-capabilities-from-xen_start_kernel.patch
Patch253: 0053-x86-amd-don-t-set-X86_BUG_SYSRET_SS_ATTRS-when-runni.patch

# Fix CVE-2018-3639 (Speculative Store Bypass)
Patch254: 0054-x86-nospec-Simplify-alternative_msr_write.patch
Patch255: 0055-x86-bugs-Concentrate-bug-detection-into-a-separate-f.patch
Patch256: 0056-x86-bugs-Concentrate-bug-reporting-into-a-separate-f.patch
Patch257: 0057-x86-bugs-Read-SPEC_CTRL-MSR-during-boot-and-re-use-r.patch
Patch258: 0058-x86-bugs-KVM-Support-the-combination-of-guest-and-ho.patch
Patch259: 0059-x86-cpu-Rename-Merrifield2-to-Moorefield.patch
Patch260: 0060-x86-cpu-intel-Add-Knights-Mill-to-Intel-family.patch
Patch261: 0061-x86-bugs-Expose-sys-.-spec_store_bypass.patch
Patch262: 0062-x86-cpufeatures-Add-X86_FEATURE_RDS.patch
Patch263: 0063-x86-bugs-Provide-boot-parameters-for-the-spec_store_.patch
Patch264: 0064-x86-bugs-intel-Set-proper-CPU-features-and-setup-RDS.patch
Patch265: 0065-x86-bugs-Whitelist-allowed-SPEC_CTRL-MSR-values.patch
Patch266: 0066-x86-bugs-AMD-Add-support-to-disable-RDS-on-Fam-15-16.patch
Patch267: 0067-x86-speculation-Create-spec-ctrl.h-to-avoid-include-.patch
Patch268: 0068-prctl-Add-speculation-control-prctls.patch
Patch269: 0069-x86-process-Optimize-TIF-checks-in-__switch_to_xtra.patch
Patch270: 0070-x86-process-Correct-and-optimize-TIF_BLOCKSTEP-switc.patch
Patch271: 0071-x86-process-Optimize-TIF_NOTSC-switch.patch
Patch272: 0072-x86-process-Allow-runtime-control-of-Speculative-Sto.patch
Patch273: 0073-x86-speculation-Add-prctl-for-Speculative-Store-Bypa.patch
Patch274: 0074-nospec-Allow-getting-setting-on-non-current-task.patch
Patch275: 0075-proc-Provide-details-on-speculation-flaw-mitigations.patch
Patch276: 0076-seccomp-Enable-speculation-flaw-mitigations.patch
Patch277: 0077-prctl-Add-force-disable-speculation.patch
Patch278: 0078-seccomp-Use-PR_SPEC_FORCE_DISABLE.patch
Patch279: 0079-seccomp-Add-filter-flag-to-opt-out-of-SSB-mitigation.patch
Patch280: 0080-seccomp-Move-speculation-migitation-control-to-arch-.patch
Patch281: 0081-x86-speculation-Make-seccomp-the-default-mode-for-Sp.patch
Patch282: 0082-x86-bugs-Rename-_RDS-to-_SSBD.patch
Patch283: 0083-proc-Use-underscores-for-SSBD-in-status.patch
Patch284: 0084-Documentation-spec_ctrl-Do-some-minor-cleanups.patch
Patch285: 0085-x86-bugs-Fix-__ssb_select_mitigation-return-type.patch
Patch286: 0086-x86-bugs-Make-cpu_show_common-static.patch
Patch287: 0087-x86-bugs-Fix-the-parameters-alignment-and-missing-vo.patch
Patch288: 0088-x86-cpu-Make-alternative_msr_write-work-for-32-bit-c.patch
Patch289: 0089-x86-speculation-Use-synthetic-bits-for-IBRS-IBPB-STI.patch
Patch290: 0090-x86-cpufeatures-Disentangle-MSR_SPEC_CTRL-enumeratio.patch
Patch291: 0091-x86-cpufeatures-Disentangle-SSBD-enumeration.patch
Patch292: 0092-x86-cpu-AMD-Fix-erratum-1076-CPB-bit.patch
Patch293: 0093-x86-cpufeatures-Add-FEATURE_ZEN.patch
Patch294: 0094-x86-speculation-Handle-HT-correctly-on-AMD.patch
Patch295: 0095-x86-bugs-KVM-Extend-speculation-control-for-VIRT_SPE.patch
Patch296: 0096-x86-speculation-Add-virtualized-speculative-store-by.patch
Patch297: 0097-x86-speculation-Rework-speculative_store_bypass_upda.patch
Patch298: 0098-x86-bugs-Unify-x86_spec_ctrl_-set_guest-restore_host.patch
Patch299: 0099-x86-bugs-Expose-x86_spec_ctrl_base-directly.patch
Patch300: 0100-x86-bugs-Remove-x86_spec_ctrl_set.patch
Patch301: 0101-x86-bugs-Rework-spec_ctrl-base-and-mask-logic.patch
Patch302: 0102-x86-speculation-KVM-Implement-support-for-VIRT_SPEC_.patch
Patch303: 0103-x86-bugs-Rename-SSBD_NO-to-SSB_NO.patch


BuildRequires: bc
BuildRequires: kbd
BuildRequires: kmod
BuildRequires: glib-devel
BuildRequires: xerces-c-devel
BuildRequires: xml-security-c-devel
BuildRequires: libdnet
BuildRequires: libmspack
BuildRequires: Linux-PAM
BuildRequires: openssl-devel
BuildRequires: procps-ng-devel
Requires:      filesystem kmod coreutils
%define uname_r %{version}-%{release}-esx

%description
The Linux kernel build for GOS for VMware hypervisor.

%package devel
Summary:       Kernel Dev
Group:         System Environment/Kernel
Requires:      python2
Requires:      %{name} = %{version}-%{release}
%description devel
The Linux package contains the Linux kernel dev files

%package docs
Summary:       Kernel docs
Group:         System Environment/Kernel
Requires:      python2
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
%patch12 -p1
%patch13 -p1
%patch14 -p1

%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1
%patch24 -p1
%patch26 -p1
%patch27 -p1
%patch28 -p1
%patch30 -p1
%patch31 -p1
%patch33 -p1
%patch34 -p1
%patch35 -p1
%patch36 -p1
%patch37 -p1
%patch38 -p1
%patch39 -p1
%patch40 -p1

%patch52 -p1
%patch55 -p1
%patch56 -p1
%patch57 -p1
%patch58 -p1
%patch59 -p1
%patch60 -p1
%patch61 -p1
%patch62 -p1
%patch64 -p1
%patch65 -p1
%patch66 -p1
%patch67 -p1

%patch201 -p1
%patch202 -p1
%patch205 -p1
%patch206 -p1
%patch207 -p1
%patch208 -p1
%patch209 -p1
%patch210 -p1
%patch211 -p1
%patch212 -p1
%patch213 -p1
%patch214 -p1
%patch215 -p1
%patch216 -p1
%patch217 -p1
%patch218 -p1
%patch219 -p1
%patch220 -p1
%patch221 -p1
%patch222 -p1
%patch223 -p1
%patch224 -p1
%patch225 -p1
%patch226 -p1
%patch227 -p1
%patch228 -p1
%patch229 -p1
%patch230 -p1
%patch231 -p1
%patch232 -p1
%patch233 -p1
%patch234 -p1
%patch235 -p1
%patch236 -p1
%patch237 -p1
%patch238 -p1
%patch239 -p1
%patch240 -p1
%patch241 -p1
%patch242 -p1
%patch243 -p1
%patch244 -p1
%patch245 -p1
%patch246 -p1
%patch247 -p1
%patch248 -p1
%patch249 -p1
%patch250 -p1
%patch251 -p1
%patch252 -p1
%patch253 -p1
%patch254 -p1
%patch255 -p1
%patch256 -p1
%patch257 -p1
%patch258 -p1
%patch259 -p1
%patch260 -p1
%patch261 -p1
%patch262 -p1
%patch263 -p1
%patch264 -p1
%patch265 -p1
%patch266 -p1
%patch267 -p1
%patch268 -p1
%patch269 -p1
%patch270 -p1
%patch271 -p1
%patch272 -p1
%patch273 -p1
%patch274 -p1
%patch275 -p1
%patch276 -p1
%patch277 -p1
%patch278 -p1
%patch279 -p1
%patch280 -p1
%patch281 -p1
%patch282 -p1
%patch283 -p1
%patch284 -p1
%patch285 -p1
%patch286 -p1
%patch287 -p1
%patch288 -p1
%patch289 -p1
%patch290 -p1
%patch291 -p1
%patch292 -p1
%patch293 -p1
%patch294 -p1
%patch295 -p1
%patch296 -p1
%patch297 -p1
%patch298 -p1
%patch299 -p1
%patch300 -p1
%patch301 -p1
%patch302 -p1
%patch303 -p1


%build
# patch vmw_balloon driver
sed -i 's/module_init/late_initcall/' drivers/misc/vmw_balloon.c

make mrproper
cp %{SOURCE1} .config
sed -i 's/CONFIG_LOCALVERSION="-esx"/CONFIG_LOCALVERSION="-%{release}-esx"/' .config
make LC_ALL= oldconfig
make VERBOSE=1 KBUILD_BUILD_VERSION="1-photon" KBUILD_BUILD_HOST="photon" ARCH="x86_64" %{?_smp_mflags}

# Do not compress modules which will be loaded at boot time
# to speed up boot process
%define __modules_install_post \
    find %{buildroot}/lib/modules/%{uname_r} -name *.ko | \
        grep -v "evdev\|mousedev\|sr_mod\|cdrom\|vmwgfx\|drm_kms_helper\|ttm\|psmouse\|drm\|apa_piix\|vmxnet3\|i2c_core\|libata\|processor\|ipv6" | xargs xz \
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
install -vdm 755 %{buildroot}/etc
install -vdm 755 %{buildroot}/boot
install -vdm 755 %{buildroot}%{_defaultdocdir}/linux-%{uname_r}
install -vdm 755 %{buildroot}/etc/modprobe.d
install -vdm 755 %{buildroot}/usr/src/linux-headers-%{uname_r}
make INSTALL_MOD_PATH=%{buildroot} modules_install
cp -v arch/x86/boot/bzImage    %{buildroot}/boot/vmlinuz-%{uname_r}
cp -v System.map        %{buildroot}/boot/System.map-%{uname_r}
cp -v .config            %{buildroot}/boot/config-%{uname_r}
cp -r Documentation/*        %{buildroot}%{_defaultdocdir}/linux-%{uname_r}
install -vdm 755 %{buildroot}/usr/lib/debug/lib/modules/%{uname_r}
cp -v vmlinux %{buildroot}/usr/lib/debug/lib/modules/%{uname_r}/vmlinux-%{uname_r}

# TODO: noacpi acpi=off noapic pci=conf1,nodomains pcie_acpm=off pnpacpi=off
cat > %{buildroot}/boot/linux-%{uname_r}.cfg << "EOF"
# GRUB Environment Block
photon_cmdline=init=/lib/systemd/systemd rcupdate.rcu_expedited=1 rw systemd.show_status=0 quiet noreplace-smp cpu_init_udelay=0 plymouth.enable=0
photon_linux=vmlinuz-%{uname_r}
EOF

# cleanup dangling symlinks
rm -f %{buildroot}/lib/modules/%{uname_r}/source
rm -f %{buildroot}/lib/modules/%{uname_r}/build

# create /use/src/linux-headers-*/ content
find . -name Makefile* -o -name Kconfig* -o -name *.pl | xargs  sh -c 'cp --parents "$@" %{buildroot}/usr/src/linux-headers-%{uname_r}' copy
find arch/x86/include include scripts -type f | xargs  sh -c 'cp --parents "$@" %{buildroot}/usr/src/linux-headers-%{uname_r}' copy
find $(find arch/x86 -name include -o -name scripts -type d) -type f | xargs  sh -c 'cp --parents "$@" %{buildroot}/usr/src/linux-headers-%{uname_r}' copy
find arch/x86/include Module.symvers include scripts -type f | xargs  sh -c 'cp --parents "$@" %{buildroot}/usr/src/linux-headers-%{uname_r}' copy

# copy .config manually to be where it's expected to be
cp .config %{buildroot}/usr/src/linux-headers-%{uname_r}
# symling to the build folder
ln -sf /usr/src/linux-headers-%{uname_r} %{buildroot}/lib/modules/%{uname_r}/build
find %{buildroot}/lib/modules -name '*.ko' -print0 | xargs -0 chmod u+x

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
%exclude /lib/modules/%{uname_r}/build
%exclude /usr/src

%files docs
%defattr(-,root,root)
%{_defaultdocdir}/linux-%{uname_r}/*

%files devel
%defattr(-,root,root)
/lib/modules/%{uname_r}/build
/usr/src/linux-headers-%{uname_r}

%changelog
*   Mon Jul 16 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.4.140-1
-   Update to version 4.4.140 and fix CVE-2017-18249
*   Tue Jul 10 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.4.139-2
-   Fix CVE-2017-18232 and CVE-2018-10323.
*   Tue Jul 03 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.4.139-1
-   Update to version 4.4.139
*   Thu Jun 28 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.4.138-2
-   Add rdrand-based RNG driver to enhance kernel entropy.
*   Mon Jun 25 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.4.138-1
-   Update to version 4.4.138
*   Thu Jun 14 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.4.137-2
-   Add more spectre mitigations (IBPB/IBRS) and support for SSBD.
*   Wed Jun 13 2018 Alexey Makhalov <amakhalov@vmware.com> 4.4.137-1
-   Update to version 4.4.137. Fix panic in kprobe.
*   Fri May 18 2018 Bo Gan <ganb@vmware.com> 4.4.131-3
-   rebase fXxattrat syscall number to avoid conflict with new syscalls
*   Fri May 04 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.4.131-2
-   Fix CVE-2018-8043, CVE-2017-18216, CVE-2018-8087, CVE-2017-18241.
*   Fri May 04 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.4.131-1
-   Update to version 4.4.131
*   Wed May 02 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.4.130-2
-   Fix CVE-2017-18255.
*   Mon Apr 30 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.4.130-1
-   Update to version 4.4.130 and fix CVE-2018-1000026.
*   Thu Apr 19 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.4.124-2
-   Add full retpoline support by building with retpoline-enabled gcc.
*   Tue Mar 27 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.4.124-1
-   Update to version 4.4.124
*   Mon Feb 05 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.4.115-1
-   Update to version 4.4.115
*   Wed Jan 31 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.4.114-1
-   Update version to 4.4.114
*   Fri Jan 26 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.4.113-1
-   Update version to 4.4.113.
*   Fri Jan 19 2018 Bo Gan <ganb@vmware.com> 4.4.112-1
-   Version update to 4.4.112
*   Thu Jan 11 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.4.111-2
-   Enable the 'deadline' and 'cfq' I/O schedulers.
*   Wed Jan 10 2018 Bo Gan <ganb@vmware.com> 4.4.111-1
-   Version update to 4.4.111
*   Mon Jan 08 2018 Bo Gan <ganb@vmware.com> 4.4.110-2
-   Initial Spectre fix
-   Add Observable speculation barrier
-   Clear unused register upon syscall entry
*   Fri Jan 05 2018 Anish Swaminathan <anishs@vmware.com> 4.4.110-1
-   Version update to 4.4.110
*   Thu Jan 04 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.4.109-3
-   Update vsock transport for 9p with newer version.
*   Wed Jan 03 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.4.109-2
-   Fix SMB3 mount regression.
*   Tue Jan 02 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.4.109-1
-   Version update
-   Add patches to fix CVE-2017-8824, CVE-2017-17448 and CVE-2017-17450.
*   Tue Dec 19 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.4.106-1
-   Version update
*   Fri Dec 08 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.4.104-1
-   Version update
*   Mon Dec 04 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.4.103-1
-   Version update
*   Mon Nov 20 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.4.99-1
-   Version update
*   Tue Nov 07 2017 Alexey Makhalov <amakhalov@vmware.com> 4.4.96-1
-   Version update
*   Mon Oct 30 2017 Bo Gan <ganb@vmware.com> 4.4.92-3
-   Recreate /dev/root in init
*   Tue Oct 17 2017 Alexey Makhalov <amakhalov@vmware.com> 4.4.92-2
-   Enable vsyscall emulation
-   Do not use deprecated -q depmod option
*   Mon Oct 16 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.4.92-1
-   Version update
*   Mon Oct 16 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.4.88-2
-   Fix CVE-2017-11472 (ACPICA: Namespace: fix operand cache leak)
*   Fri Sep 22 2017 Alexey Makhalov <amakhalov@vmware.com> 4.4.88-1
-   Enable kprobes
*   Mon Sep 04 2017 Alexey Makhalov <amakhalov@vmware.com> 4.4.86-1
-   Fix CVE-2017-11600
*   Wed Aug 16 2017 Alexey Makhalov <amakhalov@vmware.com> 4.4.82-2
-   Implement the f*xattrat family of syscalls
*   Tue Aug 15 2017 Alexey Makhalov <amakhalov@vmware.com> 4.4.82-1
-   Version update
*   Fri Aug 11 2017 Alexey Makhalov <amakhalov@vmware.com> 4.4.81-1
-   Version update
*   Tue Aug 08 2017 Alexey Makhalov <amakhalov@vmware.com> 4.4.79-2
-   [bugfix] Do not fallback to syscall from VDSO on clock_gettime(MONOTONIC)
-   Fix CVE-2017-7542
*   Fri Jul 28 2017 Alexey Makhalov <amakhalov@vmware.com> 4.4.79-1
-   [feature] p9fs_dir_readdir() offset support
-   Fix CVE-2017-11473
*   Mon Jul 17 2017 Alexey Makhalov <amakhalov@vmware.com> 4.4.77-1
-   [feature] IP tunneling support (CONFIG_NET_IPIP=m)
-   Fix CVE-2017-11176
*   Wed Jun 28 2017 Alexey Makhalov <amakhalov@vmware.com> 4.4.74-1
-   [feature] DM Delay target support
-   Fix CVE-2017-1000364 ("stack clash") and CVE-2017-9605
*   Wed Jun 7 2017 Alexey Makhalov <amakhalov@vmware.com> 4.4.71-1
-   Fix CVE-2017-8890, CVE-2017-9074, CVE-2017-9075, CVE-2017-9076
    CVE-2017-9077 and CVE-2017-9242
*   Thu Jun 1 2017 Alexey Makhalov <amakhalov@vmware.com> 4.4.70-3
-   [feature] ACPI NFIT support (for PMEM type 7)
*   Wed May 31 2017 Alexey Makhalov <amakhalov@vmware.com> 4.4.70-2
-   .config: added aesni_intel and aes_x86_64 modules
*   Thu May 25 2017 Alexey Makhalov <amakhalov@vmware.com> 4.4.70-1
-   Fix CVE-2017-7487 and CVE-2017-9059
*   Tue May 9 2017 Alexey Makhalov <amakhalov@vmware.com> 4.4.67-1
-   Version update
-   pci-probe: set bar count to 4 for class 0x010000
-   Removed version suffix from config file name
*   Tue May 2 2017 Alexey Makhalov <amakhalov@vmware.com> 4.4.65-1
-   Version update, remove upstreamed patches
*   Thu Apr 27 2017 Alexey Makhalov <amakhalov@vmware.com> 4.4.64-1
-   Fix CVE-2017-7889
-   Fix Bug #1852790
*   Thu Apr 20 2017 Alexey Makhalov <amakhalov@vmware.com> 4.4.62-1
-   Fix CVE-2017-2671 and CVE-2017-7618
-   Add debug info
*   Mon Apr 10 2017 Alexey Makhalov <amakhalov@vmware.com> 4.4.60-1
-   Fix CVE-2017-7184, CVE-2017-7187, CVE-2017-7294,
    CVE-2017-7308 and CVE-2017-7346
*   Wed Mar 15 2017 Alexey Makhalov <amakhalov@vmware.com> 4.4.54-1
-   Update to linux-4.4.54 to fix CVE-2017-6346 and CVE-2017-6347
*   Tue Feb 28 2017 Alexey Makhalov <amakhalov@vmware.com> 4.4.51-2
-   .config: enable 32-bit vDSO back
*   Thu Feb 23 2017 Alexey Makhalov <amakhalov@vmware.com> 4.4.51-1
-   Update to linux-4.4.51 and apply a patch to fix
    CVE-2017-5986 and CVE-2017-6074
-   .config: enable PMEM support
-   .config: disable vsyscall and 32-bit vDSO
*   Wed Feb 1 2017 Alexey Makhalov <amakhalov@vmware.com> 4.4.41-2
-   .config: added MODULES_SIG, CRYPTO_FIPS, SYN_COOKIES support.
*   Mon Jan 9 2017 Alexey Makhalov <amakhalov@vmware.com> 4.4.41-1
-   Update to linux-4.4.41
    to fix CVE-2016-10088, CVE-2016-9793 and CVE-2016-9576
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

