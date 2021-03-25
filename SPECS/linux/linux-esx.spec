%global security_hardening none
Summary:       Kernel
Name:          linux-esx
Version:       4.4.263
Release:       1%{?dist}
License:       GPLv2
URL:           http://www.kernel.org/
Group:         System Environment/Kernel
Vendor:        VMware, Inc.
Distribution:  Photon

%define uname_r %{version}-%{release}-esx

Source0:       http://www.kernel.org/pub/linux/kernel/v4.x/linux-%{version}.tar.xz
%define sha1 linux=e006aedf7c52e17d1c5d7d206b34c4f40c726acc
Source1:       config-esx
Source2:       pre-preun-postun-tasks.inc

Patch0:        double-tcp_mem-limits.patch
Patch1:        linux-4.4-sysctl-sched_weighted_cpuload_uses_rla.patch
Patch2:        linux-4.4-watchdog-Disable-watchdog-on-virtual-machines.patch
Patch3:        SUNRPC-Do-not-reuse-srcport-for-TIME_WAIT-socket.patch
Patch4:        vmxnet3-1.4.6.0-update-rx-ring2-max-size.patch
Patch5:        clear-linux.patch
Patch6:        pci-probe.patch
Patch7:        quiet-boot.patch
Patch8:        pv-ops.patch
Patch9:        poweroff.patch
Patch10:       sunrpc-xs_bind-uses-ip_local_reserved_ports.patch
Patch11:       vmxnet3-1.4.6.0-avoid-calling-pskb_may_pull-with-interrupts-disabled.patch
Patch13:       REVERT-sched-fair-Beef-up-wake_wide.patch
Patch14:       e1000e-prevent-div-by-zero-if-TIMINCA-is-zero.patch

Patch16:       vmxnet3-1.4.6.0-fix-lock-imbalance-in-vmxnet3_tq_xmit.patch
Patch17:       vmxnet3-1.4.7.0-set-CHECKSUM_UNNECESSARY-for-IPv6-packets.patch
Patch18:       vmxnet3-1.4.8.0-segCnt-can-be-1-for-LRO-packets.patch
Patch19:       serial-8250-do-not-probe-U6-16550A-fifo-size.patch
Patch20:       vmci-1.1.4.0-use-32bit-atomics-for-queue-headers.patch
Patch21:       vmci-1.1.5.0-doorbell-create-and-destroy-fixes.patch
Patch22:       vsock-transport-for-9p.patch
Patch23:       Implement-the-f-xattrat-family-of-functions.patch
Patch24:       init-do_mounts-recreate-dev-root.patch

# 9p patches for VDFS
Patch25:       p9fs_dir_readdir-offset-support.patch
Patch26:       net-9p-vdfs-zerocopy.patch
Patch27:       0001-fs-9p-Add-opt_metaonly-option.patch
Patch28:       0001-Enable-cache-loose-for-vdfs-9p.patch
Patch29:       0001-Calculate-zerocopy-pages-with-considering-buffer-ali.patch
Patch30:       0001-9p-Transport-error-uninitialized.patch
Patch31:       0001-9p-Ensure-seekdir-take-effect-when-entries-in-readdi.patch
Patch32:       0001-9p-fscache-Don-t-use-writeback-fid-for-cache-when-en.patch
# Fix for CVE-2018-5995
Patch33:        0001-percpu-stop-printing-kernel-addresses.patch

Patch35:       0001-hwrng-rdrand-Add-RNG-driver-based-on-x86-rdrand-inst.patch
# Fix for CVE-2017-18232
Patch36:       0001-scsi-libsas-direct-call-probe-and-destruct.patch
# Fix for CVE-2019-19922
Patch37:       0001-sched-fair-Fix-bandwidth-timer-clock-drift-condition.patch
Patch38:       0002-sched-fair-Fix-low-cpu-usage-with-high-throttling-by.patch
Patch39:       0003-sched-fair-Fix-Wunused-but-set-variable-warnings.patch
# Fix for CVE-2019-20811
Patch40:        0001-net-sysfs-call-dev_hold-if-kobject_init_and_add-succ.patch
# Fix for CVE-2018-10322 (following 8 patches)
Patch41:        0001-xfs-add-missing-include-dependencies-to-xfs_dir2.h.patch
Patch42:        0002-xfs-replace-xfs_mode_to_ftype-table-with-switch-stat.patch
Patch43:        0003-xfs-fix-xfs_mode_to_ftype-prototype.patch
Patch44:        0004-xfs-sanity-check-directory-inode-di_size.patch
Patch45:        0005-xfs-sanity-check-inode-di_mode.patch
Patch46:        0006-xfs-verify-dinode-header-first.patch
Patch47:        0007-xfs-move-inode-fork-verifiers-to-xfs_dinode_verify.patch
Patch48:        0008-xfs-enhance-dinode-verifier.patch
#9p uninitialized fid->iounit
Patch49:        0001-Initialize-fid-iounit-during-creation-of-p9_fid.patch
#Fix CVE-2019-8912
Patch50:        fix_use_after_free_in_sockfs_setattr.patch
# Fix for CVE-2019-12456
Patch51:        0001-scsi-mpt3sas_ctl-fix-double-fetch-bug-in-_ctl_ioctl_.patch
# Fix for CVE-2020-14386
Patch52:        0001-net-packet-make-tp_drops-atomic.patch
Patch53:        0001-net-packet-fix-overflow-in-tpacket_rcv.patch
# Fix for CVE-2019-12379
Patch54:        0001-consolemap-Fix-a-memory-leaking-bug-in-drivers-tty-v.patch
# Fix for CVE-2019-12381
Patch55:        0001-ip_sockglue-Fix-missing-check-bug-in-ip_ra_control.patch
# Fix for CVE-2019-12382
Patch56:        0001-drm-edid-Fix-a-missing-check-bug-in-drm_load_edid_fi.patch
# Fix for CVE-2019-12378
Patch57:        0001-ipv6_sockglue-Fix-a-missing-check-bug-in-ip6_ra_cont.patch
# Fix CVE-2019-18885
Patch59:        0001-btrfs-merge-btrfs_find_device-and-find_device.patch
Patch60:        0002-btrfs-Detect-unbalanced-tree-with-empty-leaf-before-.patch
#Fix for CVE-2020-12888
Patch61:        0001-vfio-type1-Support-faulting-PFNMAP-vmas.patch
Patch62:        0002-vfio-pci-Fault-mmaps-to-enable-vma-tracking.patch
Patch63:        0003-vfio-pci-Invalidate-mmaps-and-block-MMIO-access-on-d.patch
# Fix for CVE-2019-19377
Patch68:        0001-btrfs-Don-t-submit-any-btree-write-bio-if-the-fs-has.patch

# For Spectre
Patch70:        0169-x86-syscall-Clear-unused-extra-registers-on-syscall-.patch

#Fix CVE-2019-19813 and CVE-2019-19816
Patch71:        0001-btrfs-Move-btrfs_check_chunk_valid-to-tree-check.-ch.patch
Patch72:        0002-btrfs-tree-checker-Make-chunk-item-checker-messages-.patch
Patch73:        0003-btrfs-tree-checker-Make-btrfs_check_chunk_valid-retu.patch
Patch74:        0004-btrfs-tree-checker-Check-chunk-item-at-tree-block-re.patch
Patch75:        0005-btrfs-tree-checker-Verify-dev-item.patch
Patch76:        0006-btrfs-tree-checker-Enhance-chunk-checker-to-validate.patch
Patch77:        0007-btrfs-tree-checker-Verify-inode-item.patch

# Fix for CVE-2020-16119
Patch79:        0001-timer-Prepare-to-change-timer-callback-argument-type.patch
Patch80:        0002-net-dccp-Convert-timers-to-use-timer_setup.patch
Patch81:        0003-dccp-ccid-move-timers-to-struct-dccp_sock.patch
Patch82:        0004-Revert-dccp-don-t-free-ccid2_hc_tx_sock-struct-in-dc.patch

#Fix for CVE-2020-16120
Patch83:        0001-ovl-pass-correct-flags-for-opening-real-directory.patch
Patch84:        0002-ovl-switch-to-mounter-creds-in-readdir.patch
Patch85:        0003-ovl-verify-permissions-in-ovl_path_open.patch

#Fix for CVE-2019-19338
Patch86:        0001-KVM-vmx-implement-MSR_IA32_TSX_CTRL-disable-RTM-func.patch
Patch87:        0001-KVM-vmx-use-MSR_IA32_TSX_CTRL-to-hard-disable-TSX-on.patch

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
Requires(pre): coreutils
Requires(preun): coreutils
Requires(post): coreutils
Requires(postun): coreutils

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
%patch25 -p1
%patch26 -p1
%patch27 -p1
%patch28 -p1
%patch29 -p1
%patch30 -p1
%patch31 -p1
%patch32 -p1
%patch33 -p1
%patch35 -p1
%patch36 -p1
%patch37 -p1
%patch38 -p1
%patch39 -p1
%patch40 -p1
%patch41 -p1
%patch42 -p1
%patch43 -p1
%patch44 -p1
%patch45 -p1
%patch46 -p1
%patch47 -p1
%patch48 -p1
%patch49 -p1
%patch50 -p1
%patch51 -p1
%patch52 -p1
%patch53 -p1
%patch54 -p1
%patch55 -p1
%patch56 -p1
%patch57 -p1
%patch59 -p1
%patch60 -p1
%patch61 -p1
%patch62 -p1
%patch63 -p1
%patch68 -p1

%patch70 -p1
%patch71 -p1
%patch72 -p1
%patch73 -p1
%patch74 -p1
%patch75 -p1
%patch76 -p1
%patch77 -p1
%patch79 -p1
%patch80 -p1
%patch81 -p1
%patch82 -p1
%patch83 -p1
%patch84 -p1
%patch85 -p1
%patch86 -p1
%patch87 -p1

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

%include %{SOURCE2}

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
*   Wed Mar 24 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.4.263-1
-   Update to version 4.4.263
*   Fri Feb 26 2021 Sharan Turlapati <sturlapati@vmware.com> 4.4.258-1
-   Update to version 4.4.258
*   Tue Feb 23 2021 Sharan Turlapati <sturlapati@vmware.com> 4.4.257-2
-   Part of the fix for CVE-2021-3347
*   Tue Feb 23 2021 Sharan Turlapati <sturlapati@vmware.com> 4.4.257-1
-   Update to version 4.4.257
*   Mon Jan 11 2021 Ankit Jain <ankitja@vmware.com> 4.4.250-1
-   Update to version 4.4.250
*   Mon Jan 04 2021 Ankit Jain <ankitja@vmware.com> 4.4.249-1
-   Update to version 4.4.249
*   Mon Dec 14 2020 Vikash Bansal <bvikas@vmware.com> 4.4.248-1
-   Update to version 4.4.248
*   Sun Nov 29 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.4.246-1
-   Update to version 4.4.246
-   Fix CVE-2019-19338
*   Wed Nov 18 2020 Vikash Bansal <bvikas@vmware.com> 4.4.243-2
-   Mark BAR0 (at offset 0x10) for PCI device 15ad:07b0 (VMXNET3) as variable
*   Wed Nov 11 2020 Keerthana K <keerthanak@vmware.com> 4.4.243-1
-   Update to version 4.4.243
*   Tue Nov 10 2020 Keerthana K <keerthanak@vmware.com> 4.4.241-4
-   Fix slab-out-of-bounds read in fbcon
*   Tue Nov 10 2020 Keerthana K <keerthanak@vmware.com> 4.4.241-3
-   Fix for CVE-2020-8694
*   Tue Nov 03 2020 Sharan Turlapati <sturlapati@vmware.com> 4.4.241-2
-   Fix for CVE-2020-25645
*   Mon Nov 02 2020 Keerthana K <keerthanak@vmware.com> 4.4.241-1
-   Update to version 4.4.241
*   Mon Oct 19 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.4.240-1
-   Update to version 4.4.240
*   Thu Oct 15 2020 Srinidhi Rao <srinidhir@vmware.com> 4.4.237-5
-   Fix for CVE-2019-19377
*   Mon Oct 12 2020 Ajay Kaher <akaher@vmware.com> 4.4.237-4
-   Fix for CVE-2020-16120
*   Mon Oct 12 2020 Ankit Jain <ankitja@vmware.com> 4.4.237-3
-   Fix for CVE-2020-16119
*   Tue Sep 29 2020 Amod Mishra <mamod@vmware.com> 4.4.237-2
-   9p: Don't use writeback fid for cache when enabled for VDFS
*   Mon Sep 28 2020 Ajay Kaher <akaher@vmware.com> 4.4.237-1
-   Update to version 4.4.237
*   Wed Sep 23 2020 Ajay Kaher <akaher@vmware.com> 4.4.234-5
-   Fix for CVE-2020-14390
*   Wed Sep 23 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.4.234-4
-   Fix for CVE-2019-19813 and CVE-2019-19816
*   Tue Sep 22 2020 Ajay Kaher <akaher@vmware.com> 4.4.234-3
-   Fix for CVE-2020-25211
*   Mon Sep 07 2020 Vikash Bansal <bvikas@vmware.com> 4.4.234-2
-   Fix for CVE-2020-14386
*   Tue Sep 01 2020 Vikash Bansal <bvikas@vmware.com> 4.4.234-1
-   Update to version 4.4.234
*   Tue Aug 18 2020 Ajay Kaher <akaher@vmware.com> 4.4.232-2
-   9p: Add opt_metaonly cache option
*   Fri Aug 14 2020 ashwin-h <ashwinh@vmware.com> 4.4.232-1
-   Update to version 4.4.232
*   Thu Aug 13 2020 Ashwin H <ashwinh@vmware.com> 4.4.230-4
-   Fix CVE-2020-16166
*   Wed Aug 12 2020 Shreenidhi Shedi <sshedi@vmware.com> 4.4.230-3
-   Keep modules of running kernel till next boot
*   Sun Jul 26 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.4.230-2
-   Fix CVE-2020-14331
*   Tue Jul 21 2020 Sharan Turlapati <sturlapati@vmware.com> 4.4.230-1
-   Update to version 4.4.230
*   Thu Jul 09 2020 Ajay Kaher <akaher@vmware.com> 4.4.228-3
-   Fix for CVE-2020-12888
*   Fri Jul 03 2020 Mounesh Badiger <badigerm@vmware.com> 4.4.228-2
-   9p: Initialize fid->iounit during creation of p9_fid
*   Wed Jun 24 2020 Keerthana K <keerthanak@vmware.com> 4.4.228-1
-   Update to version 4.4.228
*   Mon Jun 22 2020 Vikash Bansal <bvikas@vmware.com> 4.4.227-2
-   Add patch to fix CVE-2019-19922 & CVE-2019-20811
*   Thu Jun 18 2020 Keerthana K <keerthanak@vmware.com> 4.4.227-1
-   Update to version 4.4.227
*   Tue Jun 02 2020 Ajay Kaher <akaher@vmware.com> 4.4.224-3
-   Fix for CVE-2018-5995
*   Tue May 26 2020 Albert Guo <aguo@vmware.com> 4.4.224-2
-   9p: Ensure seekdir take effect
*   Fri May 22 2020 Ajay Kaher <akaher@vmware.com> 4.4.224-1
-   Update to version 4.4.224
*   Tue May 19 2020 Vikash Bansal <bvikas@vmware.com> 4.4.221-4
-   Fix for CVE-2019-18885
*   Tue May 12 2020 Siddharth Chandrasekaran <csiddharth@vmware.com> 4.4.221-3
-   Add patch to fix CVE-2020-10711
*   Fri May 08 2020 Vikash Bansal <bvikas@vmware.com> 4.4.221-2
-   PCI Probe Refactored - Backported from dev
*   Tue May 05 2020 ashwin-h <ashwinh@vmware.com> 4.4.221-1
-   Update to version 4.4.221
*   Thu Apr 30 2020 ashwin-h <ashwinh@vmware.com> 4.4.220-1
-   Update to version 4.4.220
*   Tue Apr 14 2020 Alexey Makhalov <amakhalov@vmware.com> 4.4.219-2
-   Improve hardcodded poweroff (03-poweroff.patch)
*   Mon Apr 13 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.4.219-1
-   Update to version 4.4.219
*   Mon Mar 30 2020 Vikash Bansal <bvikas@vmware.com> 4.4.217-2
-   Fix for CVE-2018-13094
*   Mon Mar 23 2020 Keerthana K <keerthanak@vmware.com> 4.4.217-1
-   Update to version 4.4.217
*   Tue Mar 17 2020 Ajay Kaher <akaher@vmware.com> 4.4.216-1
-   Update to version 4.4.216
*   Thu Feb 13 2020 Ajay Kaher <akaher@vmware.com> 4.4.213-2
-   Fix CVE-2019-16233
*   Wed Feb 12 2020 ashwin-h <ashwinh@vmware.com> 4.4.213-1
-   Update to version 4.4.213
*   Tue Feb 11 2020 Mounesh Badiger <badigerm@vmware.com> 4.4.210-3
-   9p: Transport error uninitialized
*   Wed Feb 05 2020 Mounesh Badiger <badigerm@vmware.com> 4.4.210-2
-   9p:Calculate zerocopy pages with considering buffer alignment
*   Fri Jan 17 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.4.210-1
-   Update to version 4.4.210
*   Fri Dec 06 2019 Ajay Kaher <akaher@vmware.com> 4.4.206-1
-   Update to version 4.4.206
*   Tue Nov 26 2019 Ajay Kaher <akaher@vmware.com> 4.4.202-2
-   Fix CVE-2019-19066
*   Tue Nov 19 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.4.202-1
-   Update to version 4.4.202
*   Tue Nov 12 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.4.201-1
-   Update to version 4.4.201
*   Thu Nov 07 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.4.199-1
-   Update to version 4.4.199
*   Fri Oct 11 2019 Ajay Kaher <akaher@vmware.com> 4.4.196-1
-   Update to version 4.4.196
*   Wed Sep 18 2019 bvikas <bvikas@vmware.com> 4.4.193-1
-   Update to version 4.4.193
*   Mon Sep 09 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.4.191-1
-   Update to version 4.4.191
*   Mon Sep 02 2019  Mounesh Badiger <badigerm@vmware.com> 4.4.189-2
-   9p: use loose cache only for metadata
*   Mon Aug 12 2019 Alexey Makhalov <amakhalov@vmware.com> 4.4.189-1
-   Update to version 4.4.189 to fix CVE-2019-1125
*   Thu Jul 25 2019 Keerthana K <keerthanak@vmware.com> 4.4.185-3
-   Fix postun scriplet.
*   Thu Jul 25 2019 Ajay Kaher <akaher@vmware.com> 4.4.185-2
-   Fix CVE-2019-11487
*   Wed Jul 10 2019 VIKASH BANSAL <bvikas@vmware.com> 4.4.185-1
-   Update to version 4.4.185
*   Mon Jun 17 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.4.182-1
-   Update to version 4.4.182
-   Fix CVE-2019-12456, CVE-2018-16597, CVE-2018-19407, CVE-2019-12379,
-   CVE-2019-12381, CVE-2019-12382, CVE-2019-12378
*   Tue Jun 11 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.4.181-1
-   Update to version 4.4.181
*   Tue May 28 2019 Keerthana K <keerthanak@vmware.com> 4.4.180-2
-   Fix to parse through /boot folder and update symlink (/boot/photon.cfg) if
-   mulitple kernels are installed and current linux kernel is removed.
*   Fri May 17 2019 Ajay Kaher <akaher@vmware.com> 4.4.180-1
-   Update to version 4.4.180
*   Tue May 14 2019 Ajay Kaher <akaher@vmware.com> 4.4.178-2
-   Fix CVE-2019-11599
*   Fri Apr 05 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.4.178-1
-   Update to version 4.4.178
*   Wed Mar 27 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.4.177-1
-   Update to version 4.4.177
*   Fri Feb 22 2019 Srinidhi Rao<srinidhir@vmware.com> 4.4.174-1
-   Update to version 4.4.174
*   Thu Feb 21 2019 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.4.171-2
-   Fix CVE-2019-8912
*   Thu Jan 24 2019 Ajay Kaher <akaher@vmware.com> 4.4.171-1
-   Update to version 4.4.171
*   Wed Dec 12 2018 Kamal Charan <kcharan@vmware.com> 4.4.164-2
-   Add 9p zero copy data path using crossfd
*   Mon Nov 26 2018 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.4.164-1
-   Update to version 4.4.164
*   Wed Nov 14 2018 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.4.163-1
-   Update to version 4.4.163
*   Mon Oct 15 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.4.161-1
-   Update to version 4.4.161
*   Mon Sep 24 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.4.157-1
-   Update to version 4.4.157 and fix CVE-2018-10879
*   Tue Sep 18 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.4.153-3
-   Improve error-handling of rdrand-rng kernel driver.
*   Fri Sep 07 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.4.153-2
-   Fix CVE-2018-13053
*   Tue Sep 04 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.4.153-1
-   Update to version 4.4.153
*   Fri Aug 24 2018 Bo Gan <ganb@vmware.com> 4.4.152-1
-   Update to version 4.4.152
*   Fri Aug 17 2018 Bo Gan <ganb@vmware.com> 4.4.148-1
-   Update to version 4.4.148 (l1tf fixes)
*   Thu Aug 09 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.4.147-1
-   Update to version 4.4.147 to fix CVE-2018-12233.
*   Tue Aug 07 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.4.146-1
-   Update to version 4.4.146
*   Mon Jul 30 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.4.145-1
-   Update to version 4.4.145 and clear stack on fork.
*   Thu Jul 26 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.4.144-1
-   Update to version 4.4.144 and fix CVE-2018-10322
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
-   Initial commit. Use patchset from Clear Linux.
