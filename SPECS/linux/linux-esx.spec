%global security_hardening none
Summary:        Kernel
Name:           linux-esx
Version:        4.9.154
Release:        1%{?dist}
License:        GPLv2
URL:            http://www.kernel.org/
Group:          System Environment/Kernel
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://www.kernel.org/pub/linux/kernel/v4.x/linux-%{version}.tar.xz
%define sha1 linux=1a506bd238df9dbdc81e6b74abc0bb751a45eb5b
Source1:        config-esx
Source2:        initramfs.trigger
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
# -esx
Patch13:        serial-8250-do-not-probe-U6-16550A-fifo-size.patch
Patch14:        01-clear-linux.patch
Patch15:        02-pci-probe.patch
Patch16:        03-poweroff.patch
Patch17:        04-quiet-boot.patch
Patch18:        05-pv-ops-clocksource.patch
Patch19:        06-pv-ops-boot_clock.patch
Patch20:        07-vmware-only.patch
Patch22:        add-sysctl-to-disallow-unprivileged-CLONE_NEWUSER-by-default.patch
# Fix CVE-2017-1000252
Patch24:        kvm-dont-accept-wrong-gsi-values.patch
Patch25:        init-do_mounts-recreate-dev-root.patch
Patch30:        vmxnet3-avoid-xmit-reset-due-to-a-race-in-vmxnet3.patch
Patch31:        vmxnet3-use-correct-flag-to-indicate-LRO-feature.patch
Patch32:        netfilter-ipset-pernet-ops-must-be-unregistered-last.patch
Patch33:        vmxnet3-fix-incorrect-dereference-when-rxvlan-is-disabled.patch
# Fixes for CVE-2018-1000026
Patch34:        0001-net-create-skb_gso_validate_mac_len.patch
Patch35:        0002-bnx2x-disable-GSO-where-gso_size-is-too-big-for-hard.patch
# Fix for CVE-2018-8043
Patch38:        0001-net-phy-mdio-bcm-unimac-fix-potential-NULL-dereferen.patch
Patch42:        0001-hwrng-rdrand-Add-RNG-driver-based-on-x86-rdrand-inst.patch
# Fix for CVE-2017-18232
Patch43:        0001-scsi-libsas-direct-call-probe-and-destruct.patch
# Fix for CVE-2018-10323
Patch45:        0001-xfs-set-format-back-to-extents-if-xfs_bmap_extents_t.patch
# Fix for CVE-2018-10322
Patch46:        0001-xfs-move-inode-fork-verifiers-to-xfs-dinode-verify.patch
Patch47:        0002-xfs-verify-dinode-header-first.patch
Patch48:        0003-xfs-enhance-dinode-verifier.patch

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
Requires(post):(coreutils or toybox)
%define uname_r %{version}-%{release}-esx

%description
The Linux kernel build for GOS for VMware hypervisor.

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
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1
%patch22 -p1
%patch24 -p1
%patch25 -p1
%patch30 -p1
%patch31 -p1
%patch32 -p1
%patch33 -p1
%patch34 -p1
%patch35 -p1
%patch38 -p1
%patch42 -p1
%patch43 -p1
%patch45 -p1
%patch46 -p1
%patch47 -p1
%patch48 -p1


%build

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
photon_cmdline=init=/lib/systemd/systemd rcupdate.rcu_expedited=1 rw systemd.show_status=0 quiet noreplace-smp cpu_init_udelay=0
photon_linux=vmlinuz-%{uname_r}
#photon_initrd=initrd.img-%{uname_r}
EOF

# Register myself to initramfs
mkdir -p %{buildroot}/%{_localstatedir}/lib/initramfs/kernel
touch %{buildroot}/%{_localstatedir}/lib/initramfs/kernel/%{uname_r}

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
%config %{_localstatedir}/lib/initramfs/kernel/%{uname_r}
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
*   Mon Feb 04 2019 Ajay Kaher <akaher@vmware.com> 4.9.154-1
-   Update to version 4.9.154
*   Tue Jan 08 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.9.140-3
-   Read TSC only during the startup of the boot-CPU.
*   Mon Dec 03 2018 Alexey Makhalov <amakhalov@vmware.com> 4.9.140-2
-   Fix BAR4 is zero issue for IDE devices
*   Mon Nov 26 2018 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.9.140-1
-   Update to version 4.9.140
*   Fri Nov 16 2018 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.9.137-1
-   Update to version 4.9.137
*   Mon Oct 08 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.130-3
-   Enable SMB2 support in the config.
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
*   Tue Jul 17 2018 Srinidhi Rao <srinidhir@vmware.com> 4.9.111-3
-   Fix CVE-2018-10322
*   Thu Jul 12 2018 Srinidhi Rao <srinidhir@vmware.com> 4.9.111-2
-   Fix CVE-2017-18232, CVE-2017-18249 and CVE-2018-10323
*   Sat Jul 07 2018 Alexey Makhalov <amakhalov@vmware.com> 4.9.111-1
-   Update to version 4.9.111.
-   .config: use =y for vmxnet3 instead of =m, use lz4 for bzImage.
*   Sun Jul 01 2018 Ron Jaegers <ron.jaegers@gmail.com> 4.9.109-4
-   Enable USB_ACM support in the config.
*   Wed Jun 27 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.109-3
-   Add rdrand-based RNG driver to enhance kernel entropy.
*   Mon Jun 25 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.109-2
-   Enable USB_SERIAL support in the config.
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
*   Mon Feb 05 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.80-1
-   Update to version 4.9.80
*   Wed Jan 31 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.79-1
-   Update version to 4.9.79
*   Fri Jan 26 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.78-1
-   Update version to 4.9.78.
*   Wed Jan 10 2018 Bo Gan <ganb@vmware.com> 4.9.76-1
-   Version update
*   Wed Jan 10 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.75-4
-   Enable the 'deadline' and 'cfq' I/O schedulers.
*   Sun Jan 07 2018 Bo Gan <ganb@vmware.com> 4.9.75-3
-   Second Spectre fix, clear user controlled registers upon syscall entry
*   Sun Jan 07 2018 Bo Gan <ganb@vmware.com> 4.9.75-2
-   Initial Spectre fix
*   Fri Jan 05 2018 Anish Swaminathan <anishs@vmware.com> 4.9.75-1
-   Version update to 4.9.75
*   Thu Jan 04 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.74-3
-   Update vsock transport for 9p with newer version.
*   Wed Jan 03 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.74-2
-   Fix SMB3 mount regression.
*   Tue Jan 02 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.74-1
-   Version update
-   Add patches to fix CVE-2017-8824, CVE-2017-17448 and CVE-2017-17450.
*   Thu Dec 21 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.71-1
-   Version update
*   Mon Dec 19 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.66-2
-   Enable audit support (CONFIG_AUDIT=y)
*   Mon Dec 04 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.66-1
-   Version update
*   Mon Nov 27 2017 Bo Gan <ganb@vmware.com> 4.9.64-2
-   Recreate /dev/root in init
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

