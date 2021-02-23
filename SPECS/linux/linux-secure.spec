%global security_hardening none
Summary:        Kernel
Name:           linux-secure
Version:        4.9.258
Release:        1%{?kat_build:.%kat_build}%{?dist}
License:        GPLv2
URL:            http://www.kernel.org/
Group:          System Environment/Kernel
Vendor:         VMware, Inc.
Distribution:   Photon

%define uname_r %{version}-%{release}-secure

Source0:        http://www.kernel.org/pub/linux/kernel/v4.x/linux-%{version}.tar.xz
%define sha1 linux=4cb67679baa0c8dd301245647072477b21aca679
Source1:        config-secure
Source2:        aufs4.9.tar.gz
%define sha1 aufs=ebe716ce4b638a3772c7cd3161abbfe11d584906
Source3:        initramfs.trigger
Source4:        pre-preun-postun-tasks.inc

# common
Patch0:         x86-vmware-read-tsc_khz-only-once-at-boot-time.patch
Patch1:         x86-vmware-use-tsc_khz-value-for-calibrate_cpu.patch
Patch2:         x86-vmware-add-basic-paravirt-ops-support.patch
Patch3:         x86-vmware-add-paravirt-sched-clock.patch
Patch4:         x86-vmware-log-kmsg-dump-on-panic.patch
Patch5:         double-tcp_mem-limits.patch
Patch6:         linux-4.9-sysctl-sched_weighted_cpuload_uses_rla.patch
Patch7:         linux-4.9-watchdog-Disable-watchdog-on-virtual-machines.patch
Patch8:         Implement-the-f-xattrat-family-of-functions.patch
Patch9:         SUNRPC-Do-not-reuse-srcport-for-TIME_WAIT-socket.patch
Patch10:        SUNRPC-xs_bind-uses-ip_local_reserved_ports.patch
Patch11:        vsock-transport-for-9p.patch
Patch12:        x86-vmware-sta.patch
# secure
Patch13:        0001-NOWRITEEXEC-and-PAX-features-MPROTECT-EMUTRAMP.patch
Patch14:        0002-Added-rap_plugin.patch
Patch15:        0003-Added-PAX_RANDKSTACK.patch
# HyperV Patches
Patch16:        0004-vmbus-Don-t-spam-the-logs-with-unknown-GUIDs.patch
Patch17:        0005-Drivers-hv-utils-Fix-the-mapping-between-host-versio.patch
Patch18:        0006-Drivers-hv-vss-Improve-log-messages.patch
Patch19:        0007-Drivers-hv-vss-Operation-timeouts-should-match-host-.patch
Patch20:        0008-Drivers-hv-vmbus-Use-all-supported-IC-versions-to-ne.patch
Patch21:        0009-Drivers-hv-Log-the-negotiated-IC-versions.patch
Patch22:        0010-vmbus-fix-missed-ring-events-on-boot.patch
Patch23:        0011-vmbus-remove-goto-error_clean_msglist-in-vmbus_open.patch
Patch24:        0012-vmbus-dynamically-enqueue-dequeue-the-channel-on-vmb.patch
Patch26:        0014-hv_sock-introduce-Hyper-V-Sockets.patch
#FIPS patches - allow some algorithms
Patch27:        0001-Revert-crypto-testmgr-Disable-fips-allowed-for-authe.patch
Patch28:        0002-allow-also-ecb-cipher_null.patch
Patch29:        add-sysctl-to-disallow-unprivileged-CLONE_NEWUSER-by-default.patch
# Fix CVE-2017-1000252
Patch31:        kvm-dont-accept-wrong-gsi-values.patch
Patch32:        vmxnet3-avoid-xmit-reset-due-to-a-race-in-vmxnet3.patch
Patch33:        vmxnet3-use-correct-flag-to-indicate-LRO-feature.patch
Patch34:        netfilter-ipset-pernet-ops-must-be-unregistered-last.patch
Patch35:        vmxnet3-fix-incorrect-dereference-when-rxvlan-is-disabled.patch
# Fix for CVE-2019-20811
Patch36:        0001-net-sysfs-call-dev_hold-if-kobject_init_and_add-succ.patch
Patch37:        0001-net-sysfs-Call-dev_hold-always-in-netdev_queue_add_k.patch
Patch38:        0002-net-sysfs-Call-dev_hold-always-in-rx_queue_add_kobje.patch
#Fix for CVE-2019-20908
Patch39:        efi-Restrict-efivar_ssdt_load-when-the-kernel-is-locked-down.patch
#Fix for CVE-2019-19338
Patch40:        0001-KVM-vmx-implement-MSR_IA32_TSX_CTRL-disable-RTM-func.patch
Patch41:        0001-KVM-vmx-use-MSR_IA32_TSX_CTRL-to-hard-disable-TSX-on.patch

Patch44:        0001-hwrng-rdrand-Add-RNG-driver-based-on-x86-rdrand-inst.patch
# Fix for CVE-2017-18232
Patch45:        0001-scsi-libsas-direct-call-probe-and-destruct.patch
# Fix for CVE-2018-10322
Patch48:        0001-xfs-move-inode-fork-verifiers-to-xfs-dinode-verify.patch
Patch49:        0002-xfs-verify-dinode-header-first.patch
Patch50:        0003-xfs-enhance-dinode-verifier.patch
#Fix CVE-2019-8912
Patch51:        fix_use_after_free_in_sockfs_setattr.patch
# Fix for CVE-2018-16882
Patch52:        0001-KVM_Fix_UAF_in_nested_posted_interrupt_processing.patch
# Fix for CVE-2019-12456
Patch53:        0001-scsi-mpt3sas_ctl-fix-double-fetch-bug-in-_ctl_ioctl_.patch
# Fix for CVE-2019-12379
Patch54:        0001-consolemap-Fix-a-memory-leaking-bug-in-drivers-tty-v.patch
# Fix for CVE-2019-12381
Patch55:        0001-ip_sockglue-Fix-missing-check-bug-in-ip_ra_control.patch
# Fix for CVE-2019-12382
Patch56:        0001-drm-edid-Fix-a-missing-check-bug-in-drm_load_edid_fi.patch
# Fix for CVE-2019-12378
Patch57:        0001-ipv6_sockglue-Fix-a-missing-check-bug-in-ip6_ra_cont.patch
#Fix for CVE-2019-3900
Patch59: 0001-vhost-vsock-add-weight-support.patch
# Fix CVE-2019-18885
Patch61:        0001-btrfs-merge-btrfs_find_device-and-find_device.patch
Patch62:        0002-btrfs-Detect-unbalanced-tree-with-empty-leaf-before-.patch
# Fix for CVE-2020-16119
Patch63:        0001-timer-Prepare-to-change-timer-callback-argument-type.patch
Patch64:        0002-net-dccp-Convert-timers-to-use-timer_setup.patch
Patch65:        0003-dccp-ccid-move-timers-to-struct-dccp_sock.patch
Patch66:        0004-Revert-dccp-don-t-free-ccid2_hc_tx_sock-struct-in-dc.patch
Patch67:        0001-dccp-ccid-use-setup_timer-instead-of-timer_setup.patch

#Fix for CVE-2020-16120
Patch68:        0001-ovl-pass-correct-flags-for-opening-real-directory.patch
Patch69:        0002-ovl-switch-to-mounter-creds-in-readdir.patch
Patch70:        0003-ovl-verify-permissions-in-ovl_path_open.patch

# Out-of-tree patches from AppArmor:
Patch71: 0001-UBUNTU-SAUCE-AppArmor-basic-networking-rules.patch
Patch72: 0002-apparmor-Fix-quieting-of-audit-messages-for-network-.patch
Patch73: 0003-UBUNTU-SAUCE-apparmor-Add-the-ability-to-mediate-mou.patch

# Fix use-after-free issue in network stack
Patch74: 0001-inet-rename-netns_frags-to-fqdir.patch
Patch75: 0002-net-rename-inet_frags_exit_net-to-fqdir_exit.patch
Patch76: 0003-net-rename-struct-fqdir-fields.patch
Patch77: 0004-ipv4-no-longer-reference-init_net-in.patch
Patch78: 0005-ipv6-no-longer-reference-init_net-in.patch
Patch79: 0006-netfilter-ipv6-nf_defrag-no-longer-reference-init_ne.patch
Patch80: 0007-ieee820154-6lowpan-no-longer-reference-init_net-in.patch
Patch81: 0008-net-rename-inet_frags_init_net-to-fdir_init.patch
Patch82: 0009-net-add-a-net-pointer-to-struct-fqdir.patch
Patch83: 0010-net-dynamically-allocate-fqdir-structures.patch
Patch84: 0011-netns-add-pre_exit-method-to-struct-pernet_operation.patch
Patch85: 0012-inet-frags-uninline-fqdir_init.patch
Patch86: 0013-inet-frags-rework-rhashtable-dismantle.patch
Patch87: 0014-inet-frags-fix-use-after-free-read-in-inet_frag_dest.patch
Patch88: 0015-inet-fix-various-use-after-free-in-defrags-units.patch
Patch89: 0016-netns-restore-ops-before-calling-ops_exit_list.patch

#Fix CVE-2019-19813 and CVE-2019-19816
Patch90: 0001-btrfs-Move-btrfs_check_chunk_valid-to-tree-check.-ch.patch
Patch91: 0002-btrfs-tree-checker-Make-chunk-item-checker-messages-.patch
Patch92: 0003-btrfs-tree-checker-Make-btrfs_check_chunk_valid-retu.patch
Patch93: 0004-btrfs-tree-checker-Check-chunk-item-at-tree-block-re.patch
Patch94: 0005-btrfs-tree-checker-Verify-dev-item.patch
Patch95: 0006-btrfs-tree-checker-Enhance-chunk-checker-to-validate.patch
Patch96: 0007-btrfs-tree-checker-Verify-inode-item.patch


# NSX requirements (should be removed)
Patch99:        LKCM.patch

Patch111:       9p-trans_fd-extend-port-variable-to-u32.patch

%if 0%{?kat_build:1}
Patch1000:	%{kat_build}.patch
%endif
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
Requires:       filesystem kmod
Requires(pre): (coreutils or toybox)
Requires(preun): (coreutils or toybox)
Requires(post):(coreutils or toybox)
Requires(postun):(coreutils or toybox)

%description
Security hardened Linux kernel.

%package lkcm
Summary:       LKCM module
Group:         System Environment/Kernel
Requires:      %{name} = %{version}-%{release}
%description lkcm
The Linux package contains the LKCM driver module

%package devel
Summary:       Kernel Dev
Group:         System Environment/Kernel
Requires:      python2 gawk
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
%setup -D -b 2 -n linux-%{version}

# apply aufs patch
patch -p1 < ../aufs4-standalone-aufs4.9/aufs4-kbuild.patch
patch -p1 < ../aufs4-standalone-aufs4.9/aufs4-base.patch
patch -p1 < ../aufs4-standalone-aufs4.9/aufs4-mmap.patch
patch -p1 < ../aufs4-standalone-aufs4.9/aufs4-standalone.patch
cp -a ../aufs4-standalone-aufs4.9/Documentation/ .
cp -a ../aufs4-standalone-aufs4.9/fs/ .
cp ../aufs4-standalone-aufs4.9/include/uapi/linux/aufs_type.h include/uapi/linux/

cat >> %{SOURCE1} << "EOF"
CONFIG_AUFS_FS=m
CONFIG_AUFS_BRANCH_MAX_127=y
# CONFIG_AUFS_BRANCH_MAX_511 is not set
# CONFIG_AUFS_BRANCH_MAX_1023 is not set
# CONFIG_AUFS_BRANCH_MAX_32767 is not set
CONFIG_AUFS_SBILIST=y
# CONFIG_AUFS_HNOTIFY is not set
# CONFIG_AUFS_EXPORT is not set
# CONFIG_AUFS_XATTR is not set
# CONFIG_AUFS_FHSM is not set
# CONFIG_AUFS_RDU is not set
# CONFIG_AUFS_SHWH is not set
# CONFIG_AUFS_BR_RAMFS is not set
# CONFIG_AUFS_BR_FUSE is not set
CONFIG_AUFS_BDEV_LOOP=y
# CONFIG_AUFS_DEBUG is not set
EOF

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
%patch16 -p1
%patch17 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1
%patch24 -p1
%patch26 -p1
%patch27 -p1
%patch28 -p1
%patch29 -p1
%patch31 -p1
%patch32 -p1
%patch33 -p1
%patch34 -p1
%patch35 -p1
%patch36 -p1
%patch37 -p1
%patch38 -p1
%patch39 -p1
%patch40 -p1
%patch41 -p1
%patch44 -p1
%patch45 -p1
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
%patch61 -p1
%patch62 -p1
%patch63 -p1
%patch64 -p1
%patch65 -p1
%patch66 -p1
%patch67 -p1
%patch68 -p1
%patch69 -p1
%patch70 -p1

%patch71 -p1
%patch72 -p1
%patch73 -p1

%patch74 -p1
%patch75 -p1
%patch76 -p1
%patch77 -p1
%patch78 -p1
%patch79 -p1
%patch80 -p1
%patch81 -p1
%patch82 -p1
%patch83 -p1
%patch84 -p1
%patch85 -p1
%patch86 -p1
%patch87 -p1
%patch88 -p1
%patch89 -p1

%patch90 -p1
%patch91 -p1
%patch92 -p1
%patch93 -p1
%patch94 -p1
%patch95 -p1
%patch96 -p1

# secure
%patch13 -p1
%patch14 -p1
%patch15 -p1

pushd ..
%patch99 -p0
popd

%patch111 -p1

%if 0%{?kat_build:1}
%patch1000 -p1
%endif

%build

make mrproper
cp %{SOURCE1} .config
sed -i 's/CONFIG_LOCALVERSION="-secure"/CONFIG_LOCALVERSION="-%{release}-secure"/' .config
make LC_ALL= oldconfig
make VERBOSE=1 KBUILD_BUILD_VERSION="1-photon" KBUILD_BUILD_HOST="photon" ARCH="x86_64" %{?_smp_mflags}
# build LKCM module
bldroot=`pwd`
pushd ../LKCM
make -C $bldroot M=`pwd` modules
popd

%define __modules_install_post \
for MODULE in `find %{buildroot}/lib/modules/%{uname_r} -name *.ko` ; do \
	./scripts/sign-file sha512 certs/signing_key.pem certs/signing_key.x509 $MODULE \
	rm -f $MODULE.{sig,dig} \
	xz $MODULE \
done \
%{nil}

# __os_install_post strips signature from modules. We need to resign it again
# and then compress. Extra step is added to the default __spec_install_post.
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
# install LKCM module
bldroot=`pwd`
pushd ../LKCM
make -C $bldroot M=`pwd` INSTALL_MOD_PATH=%{buildroot} modules_install
popd
cp -v arch/x86/boot/bzImage    %{buildroot}/boot/vmlinuz-%{uname_r}
cp -v System.map        %{buildroot}/boot/System.map-%{uname_r}
cp -v .config            %{buildroot}/boot/config-%{uname_r}
cp -r Documentation/*        %{buildroot}%{_defaultdocdir}/linux-%{uname_r}
install -vdm 755 %{buildroot}/usr/lib/debug/lib/modules/%{uname_r}
cp -v vmlinux %{buildroot}/usr/lib/debug/lib/modules/%{uname_r}/vmlinux-%{uname_r}

# Since we use compressed modules we cann't use load pinning,
# because .ko files will be loaded from the memory (LoadPin: obj=<unknown>)
cat > %{buildroot}/boot/linux-%{uname_r}.cfg << "EOF"
# GRUB Environment Block
photon_cmdline=init=/lib/systemd/systemd ro loglevel=3 quiet no-vmw-sta loadpin.enabled=0 slub_debug=P page_poison=1 slab_nomerge
photon_linux=vmlinuz-%{uname_r}
photon_initrd=initrd.img-%{uname_r}
EOF

# Register myself to initramfs
mkdir -p %{buildroot}/%{_localstatedir}/lib/initramfs/kernel
cat > %{buildroot}/%{_localstatedir}/lib/initramfs/kernel/%{uname_r} << "EOF"
--add-drivers "tmem xen-scsifront xen-blkfront xen-acpi-processor xen-evtchn xen-gntalloc xen-gntdev xen-privcmd xen-pciback xenfs hv_utils hv_vmbus hv_storvsc hv_netvsc hv_sock hv_balloon cn"
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


%include %{SOURCE3}
%include %{SOURCE4}

%post
/sbin/depmod -a %{uname_r}
ln -sf linux-%{uname_r}.cfg /boot/photon.cfg

%post lkcm
/sbin/depmod -a %{uname_r}

%files
%defattr(-,root,root)
/boot/System.map-%{uname_r}
/boot/config-%{uname_r}
/boot/vmlinuz-%{uname_r}
%config(noreplace) /boot/linux-%{uname_r}.cfg
%config %{_localstatedir}/lib/initramfs/kernel/%{uname_r}
/lib/firmware/*
/lib/modules/*
%exclude /lib/modules/%{uname_r}/build
%exclude /usr/src
%exclude /lib/modules/%{uname_r}/extra/fips_lkcm.ko.xz

%files lkcm
%defattr(-,root,root)
/lib/modules/%{uname_r}/extra/fips_lkcm.ko.xz

%files docs
%defattr(-,root,root)
%{_defaultdocdir}/linux-%{uname_r}/*

%files devel
%defattr(-,root,root)
/lib/modules/%{uname_r}/build
/usr/src/linux-headers-%{uname_r}

%changelog
*   Tue Feb 23 2021 Sharan Turlapati <sturlapati@vmware.com> 4.9.258-1
-   Update to version 4.9.258
*   Wed Jan 20 2021 Keerthana K <keerthanak@vmware.com> 4.9.252-1
-   Update to version 4.9.252
*   Mon Jan 04 2021 Ankit Jain <ankitja@vmware.com> 4.9.249-1
-   Update to version 4.9.249
*   Mon Dec 14 2020 Vikash Bansal <bvikas@vmware.com> 4.9.248-1
-   Update to version 4.9.248
*   Tue Nov 24 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.9.246-1
-   Update to version 4.9.246
-   Fix CVE-2019-19338 and CVE-2019-20908
*   Fri Nov 13 2020 Vikash Bansal <bvikas@vmware.com> 4.9.243-2
-   Fixes on top of CVE-2019-20811 fix
*   Fri Nov 13 2020 Keerthana K <keerthanak@vmware.com> 4.9.243-1
-   Update to version 4.9.243
*   Thu Nov 12 2020 Vikash Bansal <bvikas@vmware.com> 4.9.241-6
-   Add patch to fix CVE-2019-20811
*   Tue Nov 10 2020 Keerthana K <keerthanak@vmware.com> 4.9.241-5
-   Fix slab-out-of-bounds read in fbcon
*   Tue Nov 10 2020 Keerthana K <keerthanak@vmware.com> 4.9.241-4
-   Fix CVE-2020-8694
*   Fri Nov 06 2020 Keerthana K <keerthanak@vmware.com> 4.9.241-3
-   Fix CVE-2020-25704
*   Tue Nov 03 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.9.241-2
-   Fix CVE-2020-25645
*   Mon Nov 02 2020 Keerthana K <keerthanak@vmware.com> 4.9.241-1
-   Update to version 4.9.241
*   Mon Oct 19 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.9.240-1
-   Update to version 4.9.240
*   Mon Oct 12 2020 Ajay Kaher <akaher@vmware.com> 4.9.237-3
-   Fix for CVE-2020-16120
*   Mon Oct 12 2020 Ankit Jain <ankitja@vmware.com> 4.9.237-2
-   Fix for CVE-2020-16119
*   Thu Oct 01 2020 Ankit Jain <ankitja@vmware.com> 4.9.237-1
-   Update to version 4.9.237
*   Wed Sep 23 2020 Ajay Kaher <akaher@vmware.com> 4.9.236-2
-   Fix for CVE-2020-14390
*   Wed Sep 23 2020 Vikash Bansal <bvikas@vmware.com> 4.9.236-1
-   Update to version 4.9.236
*   Wed Sep 23 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.9.228-8
-   Fix for CVE-2019-19813 and CVE-2019-19816
*   Tue Sep 22 2020 Ajay Kaher <akaher@vmware.com> 4.9.228-7
-   Fix for CVE-2020-25211
*   Thu Sep 10 2020 Vikash Bansal <bvikas@vmware.com> 4.9.228-6
-   Fix for CVE-2020-14356
*   Thu Sep 10 2020 Vikash Bansal <bvikas@vmware.com> 4.9.228-5
-   Fix for CVE-2020-14386
*   Thu Aug 13 2020 Vikash Bansal <bvikas@vmware.com> 4.9.228-4
-   Fix network stack for use-after-free issue in case timeout happens
-   on fragment queue and ip_expire is called
*   Thu Aug 06 2020 Ashwin H <ashwinh@vmware.com> 4.9.228-3
-   Fix CVE-2020-16166
*   Sun Jul 26 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.9.228-2
-   Fix CVE-2020-14331
*   Tue Jun 23 2020 Keerthana K <keerthanak@vmware.com> 4.9.228-1
-   Update to version 4.9.228
*   Mon Jun 08 2020 Vikash Bansal <bvikas@vmware.com> 4.9.226-1
-   Update to version 4.9.226
*   Thu Jun 04 2020 Ajay Kaher <akaher@vmware.com> 4.9.224-3
-   Fix for CVE-2020-10757
*   Fri May 29 2020 Shreenidhi Shedi <sshedi@vmware.com> 4.9.224-2
-   Keep modules of running kernel till next boot
*   Fri May 22 2020 Ajay Kaher <akaher@vmware.com> 4.9.224-1
-   Update to version 4.9.224
*   Fri May 15 2020 Vikash Bansal <bvikas@vmware.com> 4.9.221-3
-   Fix for CVE-2019-18885
*   Wed May 06 2020 Siddharth Chandrasekaran <csiddharth@vmware.com> 4.9.221-2
-   Add patch to fix CVE-2020-10711
*   Tue May 05 2020 ashwin-h <ashwinh@vmware.com> 4.9.221-1
-   Update to version 4.9.221
*   Thu Apr 30 2020 ashwin-h <ashwinh@vmware.com> 4.9.220-1
-   Update to version 4.9.220
*   Mon Apr 13 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.9.219-1
-   Update to version 4.9.219
*   Mon Mar 30 2020 Vikash Bansal <bvikas@vmware.com> 4.9.217-2
-   Fix for CVE-2018-13094 & CVE-2019-3900
*   Mon Mar 23 2020 Keerthana K <keerthanak@vmware.com> 4.9.217-1
-   Update to version 4.9.217
*   Tue Mar 17 2020 Ajay Kaher <akaher@vmware.com> 4.9.216-1
-   Update to version 4.9.216
*   Tue Mar 03 2020 Siddharth Chandrasekaran <csiddharth@vmware.com> 4.9.214-1
-   Update to version 4.9.214
*   Tue Feb 25 2020 Ajay Kaher <akaher@vmware.com> 4.9.210-3
-   Fix CVE-2019-16234
*   Fri Jan 31 2020 Ajay Kaher <akaher@vmware.com> 4.9.210-2
-   Fix CVE-2019-16233
*   Fri Jan 17 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.9.210-1
-   Update to version 4.9.210
*   Fri Dec 20 2019 Siddharth Chandrasekran <csiddharth@vmware.com> 4.9.205-2
-   Fix CVE-2019-10220
*   Wed Dec 04 2019 Ajay Kaher <akaher@vmware.com> 4.9.205-1
-   Update to version 4.9.205
*   Tue Nov 26 2019 Ajay Kaher <akaher@vmware.com> 4.9.202-2
-   Fix CVE-2019-19066
*   Tue Nov 19 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.9.202-1
-   Update to version 4.9.202
*   Tue Nov 12 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.9.201-1
-   Update to version 4.9.201
*   Thu Nov 07 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.9.199-1
-   Update to version 4.9.199
*   Mon Oct 21 2019 Ajay Kaher <akaher@vmware.com> 4.9.197-1
-   Update to version 4.9.197, Fix CVE-2019-17133
*   Wed Sep 18 2019 bvikas <bvikas@vmware.com> 4.9.193-1
-   Update to version 4.9.193
*   Mon Aug 12 2019 Alexey Makhalov <amakhalov@vmware.com> 4.9.189-1
-   Update to version 4.9.189 to fix CVE-2019-1125
*   Tue Jul 30 2019 Keerthana K <keerthanak@vmware.com> 4.9.185-2
-   Fix postun script.
*   Thu Jul 11 2019 VIKASH BANSAL <bvikas@vmware.com> 4.9.185-1
-   Update to version 4.9.185
*   Tue Jul 02 2019 Alexey Makhalov <amakhalov@vmware.com> 4.9.182-2
-   Fix 9p vsock 16bit port number issue.
*   Mon Jun 17 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.9.182-1
-   Update to version 4.9.182
-   Fix CVE-2019-12456, CVE-2019-12379, CVE-2019-12381, CVE-2019-12382,
-   CVE-2019-12378
*   Mon Jun 03 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.9.180-1
-   Update to version 4.9.180
*   Thu May 30 2019 Ajay Kaher <akaher@vmware.com> 4.9.178-4
-   Fix CVE-2019-11487
*   Thu May 30 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.9.178-3
-   Change default I/O scheduler to 'deadline' to fix performance issue.
*   Tue May 28 2019 Keerthana K <keerthanak@vmware.com> 4.9.178-2
-   Fix to parse through /boot folder and update symlink (/boot/photon.cfg) if
-   mulitple kernels are installed and current linux kernel is removed.
*   Fri May 24 2019 srinidhira0 <srinidhir@vmware.com> 4.9.178-1
-   Update to version 4.9.178
*   Tue May 14 2019 Ajay Kaher <akaher@vmware.com> 4.9.173-2
-   Fix CVE-2019-11599
*   Wed May 08 2019 Ajay Kaher <akaher@vmware.com> 4.9.173-1
-   Update to version 4.9.173
*   Fri Apr 05 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.9.168-1
-   Update to version 4.9.168
*   Wed Mar 27 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.9.166-1
-   Update to version 4.9.166
*   Thu Mar 14 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.9.163-1
-   Update to version 4.9.163
*   Mon Feb 25 2019 Ajay Kaher <akaher@vmware.com> 4.9.154-3
-   Fix CVE-2018-16882
*   Thu Feb 21 2019 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.9.154-2
-   Fix CVE-2019-8912
*   Mon Feb 04 2019 Ajay Kaher <akaher@vmware.com> 4.9.154-1
-   Update to version 4.9.154
*   Tue Jan 15 2019 Alexey Makhalov <amakhalov@vmware.com> 4.9.140-3
-   .config: disable CONFIG_FANOTIFY_ACCESS_PERMISSIONS
*   Thu Dec 20 2018 Alexey Makhalov <amakhalov@vmware.com> 4.9.140-2
-   .config: CONFIG_FANOTIFY_ACCESS_PERMISSIONS=y
*   Mon Nov 26 2018 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.9.140-1
-   Update to version 4.9.140
*   Fri Nov 16 2018 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.9.137-1
-   Update to version 4.9.137
*   Tue Oct 02 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.130-2
-   Improve error-handling of rdrand-rng kernel driver.
*   Mon Oct 01 2018 srinidhira0 <srinidhir@vmware.com> 4.9.130-1
-   Update to version 4.9.130
*   Mon Sep 10 2018 Srinidhi Rao <srinidhir@vmware.com> 4.9.124-2
-   Fix for CVE-2018-13053
*   Fri Aug 24 2018 Bo Gan <ganb@vmware.com> 4.9.124-1
-   Update to version 4.9.124
*   Fri Aug 17 2018 Bo Gan <ganb@vmware.com> 4.9.120-1
-   Update to version 4.9.120 (l1tf fixes)
*   Thu Aug 09 2018 Srinidhi Rao <srinidhir@vmware.com> 4.9.118-2
-   Fix CVE-2018-12233
*   Tue Aug 07 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.118-1
-   Update to version 4.9.118
*   Mon Jul 30 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.116-1
-   Update to version 4.9.116 and clear stack on fork.
*   Mon Jul 23 2018 srinidhira0 <srinidhir@vmware.com> 4.9.114-1
-   Update to version 4.9.114
*   Thu Jul 19 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.111-4
-   Apply out-of-tree patches needed for AppArmor.
*   Tue Jul 17 2018 Srinidhi Rao <srinidhir@vmware.com> 4.9.111-3
-   Fix CVE-2018-10322
*   Thu Jul 12 2018 Srinidhi Rao <srinidhir@vmware.com> 4.9.111-2
-   Fix CVE-2017-18232, CVE-2017-18249 and CVE-2018-10323
*   Sat Jul 07 2018 Alexey Makhalov <amakhalov@vmware.com> 4.9.111-1
-   Update to version 4.9.111
*   Wed Jun 27 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.109-2
-   Add rdrand-based RNG driver to enhance kernel entropy.
*   Thu Jun 21 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.109-1
-   Update to version 4.9.109
*   Mon May 21 2018 Alexey Makhalov <amakhalov@vmware.com> 4.9.101-2
-   Add the f*xattrat family of syscalls.
*   Mon May 21 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.101-1
-   Update to version 4.9.101 and fix CVE-2018-3639.
*   Wed May 09 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.99-1
-   Update to version 4.9.99
*   Fri May 04 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.98-2
-   Fix CVE-2017-18216, CVE-2018-8043, CVE-2018-8087, CVE-2017-18241,
-   CVE-2017-18224.
*   Fri May 04 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.98-1
-   Update to version 4.9.98
*   Wed May 02 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.97-3
-   Fix CVE-2017-18255.
*   Tue May 01 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.97-2
-   Fix CVE-2018-1000026.
*   Mon Apr 30 2018 Alexey Makhalov <amakhalov@vmware.com> 4.9.97-1
-   Update to version 4.9.97. Apply 3rd vmxnet3 patch.
*   Mon Apr 23 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.94-2
-   Add full retpoline support by building with retpoline-enabled gcc.
*   Wed Apr 18 2018 Alexey Makhalov <amakhalov@vmware.com> 4.9.94-1
-   Update to version 4.9.94. Fix panic in ip_set.
*   Mon Apr 02 2018 Alexey Makhalov <amakhalov@vmware.com> 4.9.92-1
-   Update to version 4.9.92. Apply vmxnet3 patches.
*   Tue Mar 27 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.90-1
-   Update to version 4.9.90
*   Thu Mar 22 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.89-1
-   Update to version 4.9.89
*   Mon Mar 19 2018 Alexey Makhalov <amakhalov@vmware.com> 4.9.80-2
-   Extra hardening: slab_nomerge, disable /proc/kcore
*   Mon Feb 05 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.80-1
-   Update to version 4.9.80
*   Wed Jan 31 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.79-1
-   Update version to 4.9.79
*   Fri Jan 26 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.78-1
-   Update version to 4.9.78.
*   Wed Jan 10 2018 Bo Gan <ganb@vmware.com> 4.9.76-1
-   Version update
*   Sun Jan 07 2018 Bo Gan <ganb@vmware.com> 4.9.75-3
-   Second Spectre fix, clear user controlled registers upon syscall entry
*   Sun Jan 07 2018 Bo Gan <ganb@vmware.com> 4.9.75-2
-   Initial Spectre fix
*   Fri Jan 05 2018 Bo Gan <ganb@vmware.com> 4.9.75-1
-   Verion update (fix Intel Meltdown)
*   Thu Jan 04 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.74-3
-   Update vsock transport for 9p with newer version.
*   Wed Jan 03 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.74-2
-   Fix SMB3 mount regression.
*   Tue Jan 02 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.74-1
-   Version update
-   Add patches to fix CVE-2017-8824, CVE-2017-17448 and CVE-2017-17450.
*   Thu Dec 21 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.71-1
-   Version update
*   Mon Dec 04 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.66-1
-   Version update
*   Tue Nov 21 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.64-1
-   Version update
*   Wed Nov 08 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.60-2
-   Update LKCM module
-   Add -lkcm subpackage
*   Mon Nov 06 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.60-1
-   Version update
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
*   Tue Aug 22 2017 Anish Swaminathan <anishs@vmware.com> 4.9.43-2
-   Add missing xen block drivers
*   Mon Aug 14 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.43-1
-   Version update
-   [feature] new sysctl option unprivileged_userns_clone
*   Wed Aug 09 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.41-2
-   Fix CVE-2017-7542
-   [bugfix] Added ccm,gcm,ghash,lzo crypto modules to avoid
    panic on modprobe tcrypt
*   Mon Aug 07 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.41-1
-   Version update
*   Fri Aug 04 2017 Bo Gan <ganb@vmware.com> 4.9.38-6
-   Fix initramfs triggers
*   Tue Aug 01 2017 Anish Swaminathan <anishs@vmware.com> 4.9.38-5
-   Allow some algorithms in FIPS mode
-   Reverts 284a0f6e87b0721e1be8bca419893902d9cf577a and backports
-   bcf741cb779283081db47853264cc94854e7ad83 in the kernel tree
-   Enable additional NF features
*   Fri Jul 21 2017 Anish Swaminathan <anishs@vmware.com> 4.9.38-4
-   Add patches in Hyperv codebase
*   Fri Jul 21 2017 Anish Swaminathan <anishs@vmware.com> 4.9.38-3
-   Add missing hyperv drivers
*   Thu Jul 20 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.38-2
-   Disable scheduler beef up patch
*   Tue Jul 18 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.38-1
-   Fix CVE-2017-11176 and CVE-2017-10911
*   Fri Jul 14 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.34-3
-   Remove aufs source tarballs from git repo
*   Mon Jul 03 2017 Xiaolin Li <xiaolinl@vmware.com> 4.9.34-2
-   Add libdnet-devel, kmod-devel and libmspack-devel to BuildRequires
*   Wed Jun 28 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.34-1
-   [feature] 9P FS security support
-   [feature] DM Delay target support
-   Fix CVE-2017-1000364 ("stack clash") and CVE-2017-9605
*   Thu Jun 8 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.31-1
-   Fix CVE-2017-8890, CVE-2017-9074, CVE-2017-9075, CVE-2017-9076
    CVE-2017-9077 and CVE-2017-9242
-   [feature] IPV6 netfilter NAT table support
*   Fri May 26 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.30-1
-   Fix CVE-2017-7487 and CVE-2017-9059
*   Wed May 17 2017 Vinay Kulkarni <kulkarniv@vmware.com> 4.9.28-2
-   Enable IPVLAN module.
*   Tue May 16 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.28-1
-   Version update
*   Wed May 10 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.27-1
-   Version update
*   Sun May 7 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.26-1
-   Version update
-   Removed version suffix from config file name
*   Thu Apr 27 2017 Bo Gan <ganb@vmware.com> 4.9.24-2
-   Support dynamic initrd generation
*   Tue Apr 25 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.24-1
-   Fix CVE-2017-6874 and CVE-2017-7618.
-   .config: build nvme and nvme-core in kernel.
*   Tue Mar 21 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.13-3
-   Added LKCM module
*   Mon Mar 6 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.13-2
-   .config: NSX requirements for crypto and netfilter
*   Tue Feb 28 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.13-1
-   Update to linux-4.9.13 to fix CVE-2017-5986 and CVE-2017-6074
-   .config: disable XEN guest (needs rap_plugin verification)
*   Wed Feb 22 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.9-2
-   rap_plugin improvement: throw error on function type casting
    function signatures were cleaned up using this feature.
-   Added RAP_ENTRY for asm functions.
*   Thu Feb 09 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.9-1
-   Update to linux-4.9.9 to fix CVE-2016-10153, CVE-2017-5546,
    CVE-2017-5547, CVE-2017-5548 and CVE-2017-5576.
-   Added aufs support.
-   Added PAX_RANDKSTACK feature.
-   Extra func signatures cleanup to fix 1809717 and 1809722.
-   .config: added CRYPTO_FIPS support.
*   Tue Jan 10 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.2-1
-   Update to linux-4.9.2 to fix CVE-2016-10088
-   Rename package to linux-secure.
-   Added KSPP cmdline params: slub_debug=P page_poison=1
*   Mon Dec 19 2016 Xiaolin Li <xiaolinl@vmware.com> 4.9.0-2
-   BuildRequires Linux-PAM-devel
*   Mon Dec 12 2016 Alexey Makhalov <amakhalov@vmware.com> 4.9.0-1
-   Update to linux-4.9.0
-   Add paravirt stolen time accounting feature (from linux-esx),
    but disable it by default (no-vmw-sta cmdline parameter)
-   Use vmware_io_delay() to keep "void fn(void)" signature
*   Wed Nov 30 2016 Alexey Makhalov <amakhalov@vmware.com> 4.8.0-2
-   Expand `uname -r` with release number
-   Resign and compress modules after stripping
-   .config: add syscalls tracing support
-   .config: add cgrup_hugetlb support
-   .config: add netfilter_xt_{set,target_ct} support
-   .config: add netfilter_xt_match_{cgroup,ipvs} support
-   .config: disable /dev/mem
*   Mon Oct 17 2016 Alexey Makhalov <amakhalov@vmware.com> 4.8.0-1
    Initial commit.
