%global security_hardening none

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

Summary:        Kernel
Name:           linux-rt
Version:        6.1.10
Release:        9%{?kat_build:.kat}%{?dist}
License:        GPLv2
URL:            http://www.kernel.org
Group:          System Environment/Kernel
Vendor:         VMware, Inc.
Distribution:   Photon

# Keep rt_version matched up with localversion.patch
%define rt_version rt5
%define uname_r %{version}-%{release}-rt
%define _modulesdir /lib/modules/%{uname_r}

Source0:        http://www.kernel.org/pub/linux/kernel/v6.x/linux-%{version}.tar.xz
%define sha512 linux=7bec1d76ecafd89fdb13bc7c9c69b4f378e41b29aed33c302b235540f40f1d5e6b3c653d2dea83c2d03408e324ffa73ff3dcc7c47c685572719d62bc66a06a1d

%ifarch x86_64
Source1:    config-rt
%endif

Source2:    initramfs.trigger
# contains pre, postun, filetriggerun tasks
Source4:    scriptlets.inc
Source5:    check_for_config_applicability.inc

%ifarch x86_64
%define i40e_version 2.22.18
Source6:    https://sourceforge.net/projects/e1000/files/i40e%20stable/%{i40e_version}/i40e-%{i40e_version}.tar.gz
%define sha512 i40e=042fd064528cb807894dc1f211dcb34ff28b319aea48fc6dede928c93ef4bbbb109bdfc903c27bae98b2a41ba01b7b1dffc3acac100610e3c6e95427162a26ac

%define iavf_version 4.8.2
Source7:       https://sourceforge.net/projects/e1000/files/iavf%20stable/%{iavf_version}/iavf-%{iavf_version}.tar.gz
%define sha512 iavf=5406b86e61f6528adfd7bc3a5f330cec8bb3b4d6c67395961cc6ab78ec3bd325c3a8655b8f42bf56fb47c62a85fb7dbb0c1aa3ecb6fa069b21acb682f6f578cf

%define ice_version 1.11.14
Source8:       https://sourceforge.net/projects/e1000/files/ice%20stable/%{ice_version}/ice-%{ice_version}.tar.gz
%define sha512 ice=a2a6a498e553d41e4e6959a19cdb74f0ceff3a7dbcbf302818ad514fdc18e3d3b515242c88d55ef8a00c9d16925f0cd8579cb41b3b1c27ea6716ccd7e70fd847
%endif

%if 0%{?fips}
Source9:        check_fips_canister_struct_compatibility.inc

%define fips_canister_version 5.0.0-6.1.10-8%{?dist}-secure
Source16:       fips-canister-%{fips_canister_version}.tar.bz2
%define sha512 fips-canister=b9d60d93fb86a4ff1cc39d5e3458438ce96b2e18f5773c308b6ea5b02431e5dd9fdd22babb2e2d3860a59af65092b8918e7bd23423645b3c1be7f1c9cf019e23
%endif

Source18:        modify_kernel_configs.inc
Source19:        spec_install_post.inc

Source20:       %{name}-dracut.conf

# common
Patch0: net-Double-tcp_mem-limits.patch
Patch1: SUNRPC-xs_bind-uses-ip_local_reserved_ports.patch
Patch2: 6.0-9p-transport-for-9p.patch
Patch3: 9p-trans_fd-extend-port-variable-to-u32.patch
Patch4: vsock-delay-detach-of-QP-with-outgoing-data-59.patch
Patch5: 6.0-Discard-.note.gnu.property-sections-in-generic-NOTES.patch
# Expose Photon kernel macros to identify kernel flavor and version
Patch6: 0001-kbuild-Makefile-Introduce-macros-to-distinguish-Phot.patch
Patch7: 0002-linux-rt-Makefile-Add-kernel-flavor-info-to-the-gene.patch
# RDRAND-based RNG driver to enhance the kernel's entropy pool:
Patch8: 6.0-0001-hwrng-rdrand-Add-RNG-driver-based-on-x86-rdrand-inst.patch
Patch9: 6.0-0001-cgroup-v1-cgroup_stat-support.patch

# ttyXRUSB support
Patch10: usb-acm-exclude-exar-usb-serial-ports-nxt.patch

Patch12: 6.1-0001-fork-add-sysctl-to-disallow-unprivileged-CLONE_NEWUS.patch
# Out-of-tree patches from AppArmor:
Patch13: 6.0-0001-apparmor-patch-to-provide-compatibility-with-v2.x-ne.patch
Patch14: 6.0-0002-apparmor-af_unix-mediation.patch

# Allow PCI resets to be disabled from vfio_pci_core module
Patch21: 6.1-0001-drivers-vfio-pci-Add-kernel-parameter-to-allow-disab.patch
# Add PCI quirk to allow multiple devices under the same virtual PCI bridge
# to be put into separate IOMMU groups on ESXi.
Patch22: 0001-Add-PCI-quirk-for-VMware-PCIe-Root-Port.patch
# Remove unnecessary io/memory decoding disabling/enabling.
# Toggling decoding settings (command register/bar) could introduce
# latency spikes across all vcpus due to nested pagetable
# synchronization.
Patch23: 6.0-vfio-Only-set-INTX_DISABLE-bit-during-disable.patch

# VMW:
Patch55: 6.0-x86-vmware-Use-Efficient-and-Correct-ALTERNATIVEs-fo.patch
Patch56: 6.0-x86-vmware-Log-kmsg-dump-on-panic.patch

# Disable md5 algorithm for sctp if fips is enabled.
Patch57: 6.0-0001-disable-md5-algorithm-for-sctp-if-fips-is-enabled.patch

# CVE:
Patch100: 6.0-0003-apparmor-fix-use-after-free-in-sk_peer_label.patch

# Real-Time kernel (PREEMPT_RT patches)
# Source: http://cdn.kernel.org/pub/linux/kernel/projects/rt/6.1/
Patch301: vduse-Remove-include-of-rwlock.h.patch
Patch302: signal-Don-t-disable-preemption-in-ptrace_stop-on-PR.patch
Patch303: sched-Consider-task_struct-saved_state-in-wait_task_.patch
Patch304: 0001-spi-Remove-the-obsolte-u64_stats_fetch_-_irq-users.patch
Patch305: 0002-net-Remove-the-obsolte-u64_stats_fetch_-_irq-users-d.patch
Patch306: 0003-net-Remove-the-obsolte-u64_stats_fetch_-_irq-users-n.patch
Patch307: 0004-bpf-Remove-the-obsolte-u64_stats_fetch_-_irq-users.patch
Patch308: u64_stat-Remove-the-obsolete-fetch_irq-variants.patch
Patch309: net-Avoid-the-IPI-to-free-the.patch
Patch310: x86__Allow_to_enable_RT.patch
Patch311: x86__Enable_RT_also_on_32bit.patch
Patch312: softirq-Use-a-dedicated-thread-for-timer-wakeups.patch
Patch313: rcutorture-Also-force-sched-priority-to-timersd-on-b.patch
Patch314: tick-Fix-timer-storm-since-introduction-of-timersd.patch
Patch315: tpm_tis__fix_stall_after_iowrites.patch
Patch316: drivers_block_zram__Replace_bit_spinlocks_with_rtmutex_for_-rt.patch
Patch317: locking-lockdep-Remove-lockdep_init_map_crosslock.patch
Patch318: printk-Bring-back-the-RT-bits.patch
Patch319: 0016-printk-add-infrastucture-for-atomic-consoles.patch
Patch320: 0017-serial-8250-implement-write_atomic.patch
Patch321: 0018-printk-avoid-preempt_disable-for-PREEMPT_RT.patch
Patch322: 0003-drm-i915-Use-preempt_disable-enable_rt-where-recomme.patch
Patch323: 0004-drm-i915-Don-t-disable-interrupts-on-PREEMPT_RT-duri.patch
Patch324: 0005-drm-i915-Don-t-check-for-atomic-context-on-PREEMPT_R.patch
Patch325: 0006-drm-i915-Disable-tracing-points-on-PREEMPT_RT.patch
Patch326: 0007-drm-i915-skip-DRM_I915_LOW_LEVEL_TRACEPOINTS-with-NO.patch
Patch327: 0008-drm-i915-gt-Queue-and-wait-for-the-irq_work-item.patch
Patch328: 0009-drm-i915-gt-Use-spin_lock_irq-instead-of-local_irq_d.patch
Patch329: 0010-drm-i915-Drop-the-irqs_disabled-check.patch
Patch330: Revert-drm-i915-Depend-on-PREEMPT_RT.patch
Patch331: sched__Add_support_for_lazy_preemption.patch
Patch332: x86_entry__Use_should_resched_in_idtentry_exit_cond_resched.patch
Patch333: x86__Support_for_lazy_preemption.patch
Patch334: entry--Fix-the-preempt-lazy-fallout.patch
Patch335: arm__Add_support_for_lazy_preemption.patch
Patch336: powerpc__Add_support_for_lazy_preemption.patch
Patch337: arch_arm64__Add_lazy_preempt_support.patch
Patch338: 0001-arm-Disable-jump-label-on-PREEMPT_RT.patch
Patch339: ARM__enable_irq_in_translation_section_permission_fault_handlers.patch
Patch340: tty_serial_omap__Make_the_locking_RT_aware.patch
Patch341: tty_serial_pl011__Make_the_locking_work_on_RT.patch
Patch342: ARM__Allow_to_enable_RT.patch
Patch343: ARM64__Allow_to_enable_RT.patch
Patch344: powerpc__traps__Use_PREEMPT_RT.patch
Patch345: powerpc_pseries_iommu__Use_a_locallock_instead_local_irq_save.patch
Patch346: powerpc_kvm__Disable_in-kernel_MPIC_emulation_for_PREEMPT_RT.patch
Patch347: powerpc_stackprotector__work_around_stack-guard_init_from_atomic.patch
Patch348: POWERPC__Allow_to_enable_RT.patch
Patch349: sysfs__Add__sys_kernel_realtime_entry.patch
# Keep rt_version matched up with this patch.
Patch350: Add_localversion_for_-RT_release.patch

# Ignore reading localversion-rt
Patch699: 0001-setlocalversion-Skip-reading-localversion-rt-file.patch

# Photon Specific Changes
Patch700: 6.0-0001-Revert-clockevents-Stop-unused-clockevent-devices.patch

# RT Runtime Greed
Patch701: 6.0-sched-rt-RT_RUNTIME_GREED-sched-feature.patch

#Patch to enable nohz with idle=poll
Patch714: 0001-Allow-tick-sched-timer-to-be-turned-off-in-idle-poll.patch

#Patch to add timer padding on guest
Patch716: Guest-timer-Advancement-Feature.patch

# Fix for a latency issue related to ktimer thread wakeup:
Patch717: softirq-wake-up-ktimer-thread-in-softirq-context.patch

# Crypto:
# Patch to add drbg_pr_ctr_aes256 test vectors to testmgr
Patch1000: crypto-testmgr-Add-drbg_pr_ctr_aes256-test-vectors.patch
# Patch to call drbg and dh crypto tests from tcrypt
Patch1001: 6.1-tcrypt-disable-tests-that-are-not-enabled-in-photon.patch
Patch1002: 0001-Initialize-jitterentropy-before-ecdh.patch
Patch1003: 6.0-0002-FIPS-crypto-self-tests.patch
# Patch to remove urandom usage in rng module
Patch1004: 0001-FIPS-crypto-rng-Jitterentropy-RNG-as-the-only-RND-source.patch
# Patch to remove urandom usage in drbg and ecc modules
Patch1005: 6.0-0003-FIPS-crypto-drbg-Jitterentropy-RNG-as-the-only-RND.patch
#Patch to not make shash_no_setkey static
Patch1006: 0001-fips-Continue-to-export-shash_no_setkey.patch

%if 0%{?fips}
# FIPS canister usage patch
Patch1008: 6.1.10-8-0001-FIPS-canister-binary-usage.patch
Patch1009: 0001-scripts-kallsyms-Extra-kallsyms-parsing.patch
Patch1010: FIPS-do-not-allow-not-certified-algos-in-fips-2.patch
%endif
%if 0%{?kat_build}
Patch1011: 0003-FIPS-broken-kattest.patch
%endif

# Patches for i40e v2.22.18 driver [1500..1509]
Patch1500: i40e-v2.22.18-linux-rt-i40e-Fix-build-errors-on-kernel-6.1.y.patch
Patch1501: i40e-v2.22.18-Add-support-for-gettimex64-interface.patch
Patch1502: i40e-v2.22.18-i40e-Make-i40e-driver-honor-default-and-user-defined.patch

# Patches for iavf v4.8.2 driver [1510..1519]
Patch1510: iavf-v4.8.2-linux-rt-iavf-Fix-build-errors-on-kernel-6.1.y.patch
Patch1511: iavf-Makefile-added-alias-for-i40evf.patch

# Patches for ice v1.11.14 driver [1520..1529]
Patch1520: ice-v1.11.14-linux-rt-fix-build-errors-on-6.1.y.patch

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
BuildRequires:  audit-devel
BuildRequires:  elfutils-libelf-devel
BuildRequires:  bison

%if 0%{?fips}
BuildRequires: gdb
%endif

Requires: kmod
Requires: filesystem
Requires: dracut >= 059-3
Requires: initramfs >= 2.0-8
Requires(pre):    (coreutils or coreutils-selinux)
Requires(preun):  (coreutils or coreutils-selinux)
Requires(post):   (coreutils or coreutils-selinux)
Requires(postun): (coreutils or coreutils-selinux)

%description
The Linux package contains the Linux kernel with RT (real-time)
features.
Built with rt patchset version %{rt_version}.
# Enable post FIPS certification
%if 0
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

%package docs
Summary:        Kernel docs
Group:          System Environment/Kernel
Requires:       python3
%description docs
The Linux package contains the Linux kernel doc files

%prep
# Using autosetup is not feasible
%setup -q -n linux-%{version}
%ifarch x86_64
# Using autosetup is not feasible
%setup -q -T -D -b 6 -n linux-%{version}
# Using autosetup is not feasible
%setup -q -T -D -b 7 -n linux-%{version}
# Using autosetup is not feasible
%setup -q -T -D -b 8 -n linux-%{version}
%endif
%if 0%{?fips}
# Using autosetup is not feasible
%setup -q -T -D -b 16 -n linux-%{version}
%endif

%autopatch -p1 -m0 -M23

#VMW
%autopatch -p1 -m55 -M57

# CVE
%autopatch -p1 -m100 -M100

# RT
%autopatch -p1 -m301 -M717

%autopatch -p1 -m1000 -M1006

%if 0%{?fips}
%autopatch -p1 -m1008 -M1010
%endif
%if 0%{?kat_build}
%autopatch -p1 -m1010 -M1011
%endif

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

%build
make %{?_smp_mflags} mrproper

%ifarch x86_64
cp %{SOURCE1} .config
arch="x86_64"
%endif
%if 0%{?fips}
cp ../fips-canister-%{fips_canister_version}/fips_canister.o \
   ../fips-canister-%{fips_canister_version}/fips_canister_wrapper.c \
   ../fips-canister-%{fips_canister_version}/.fips_canister.o.cmd \
   ../fips-canister-%{fips_canister_version}/fips_canister-kallsyms \
   crypto/
# Change m to y for modules that are in the canister
%include %{SOURCE18}
%else
%if 0%{?kat_build}
# Change m to y for modules in katbuild
%include %{SOURCE18}
%endif
%endif

sed -i 's/CONFIG_LOCALVERSION="-rt"/CONFIG_LOCALVERSION="-%{release}-rt"/' .config

%if 0%{?kat_build}
sed -i '/CONFIG_CRYPTO_SELF_TEST=y/a CONFIG_CRYPTO_BROKEN_KAT=y' .config
%endif

%include %{SOURCE5}

make %{?_smp_mflags} V=1 KBUILD_BUILD_VERSION="1-photon" KBUILD_BUILD_HOST="photon" ARCH=${arch} %{?_smp_mflags}

%if 0%{?fips}
%include %{SOURCE9}
%endif

%ifarch x86_64
# build i40e module
bldroot="${PWD}"
pushd ../i40e-%{i40e_version}
make %{?_smp_mflags} -C src KSRC=${bldroot} clean
make %{?_smp_mflags} -C src KSRC=${bldroot} %{?_smp_mflags}
popd

# build iavf module
pushd ../iavf-%{iavf_version}
make %{?_smp_mflags} -C src KSRC=${bldroot} clean
make %{?_smp_mflags} -C src KSRC=${bldroot} %{?_smp_mflags}
popd

# build ice module
pushd ../ice-%{ice_version}
make %{?_smp_mflags} -C src KSRC=${bldroot} clean
make %{?_smp_mflags} -C src KSRC=${bldroot} %{?_smp_mflags}
popd
%endif

%install
install -vdm 755 %{buildroot}%{_sysconfdir}
install -vdm 755 %{buildroot}/boot
install -vdm 755 %{buildroot}%{_docdir}/linux-%{uname_r}
install -vdm 755 %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}
install -vdm 755 %{buildroot}%{_libdir}/debug/%{_modulesdir}
make %{?_smp_mflags} INSTALL_MOD_PATH=%{buildroot} modules_install

%ifarch x86_64

# install i40e module
bldroot="${PWD}"
pushd ../i40e-%{i40e_version}
make %{?_smp_mflags} -C src KSRC=${bldroot} INSTALL_MOD_PATH=%{buildroot} \
    INSTALL_MOD_DIR=extra MANDIR=%{_mandir} modules_install mandocs_install
popd

# install iavf module
pushd ../iavf-%{iavf_version}
make %{?_smp_mflags} -C src KSRC=$bldroot INSTALL_MOD_PATH=%{buildroot} \
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
photon_cmdline=init=/lib/systemd/systemd ro loglevel=3 quiet nosoftlockup intel_idle.max_cstate=0 mce=ignore_ce nowatchdog cpuidle.off=1 nmi_watchdog=0 audit=0
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
cp -p %{SOURCE20} %{buildroot}%{_modulesdir}/dracut.conf.d/%{name}.conf

%include %{SOURCE2}
%include %{SOURCE4}
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
%defattr(0644,root,root)
%{_modulesdir}/*
%exclude %{_modulesdir}/build
# iavf.conf is used to just blacklist the deprecated i40evf
# and create alias of i40evf to iavf.
# By default iavf is used for VF driver.
# This file creates conflict with other flavour of linux
# thus excluding this file from packaging
%exclude %{_sysconfdir}/modprobe.d/iavf.conf
# ICE driver firmware files are packaged in linux-firmware
%exclude /lib/firmware/updates/intel/ice

%config(noreplace) %{_modulesdir}/dracut.conf.d/%{name}.conf

%files docs
%defattr(-,root,root)
%{_defaultdocdir}/linux-%{uname_r}/*
%{_mandir}/*

%files devel
%defattr(-,root,root)
%{_modulesdir}/build
%{_usrsrc}/linux-headers-%{uname_r}

%changelog
* Fri Apr 14 2023 Him Kalyan Bordoloi <bordoloih@vmware.com> 6.1.10-9
- Update Guest timer advancement feature
* Fri Mar 31 2023 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 6.1.10-8
- Expose Photon kernel macros to simplify building out-of-tree drivers.
* Thu Mar 30 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 6.1.10-7
- Update drivers
- iavf: 4.8.2
- ice: 1.11.14
- i40e: 2.22.18
* Sun Mar 26 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 6.1.10-6
- Use canister version 5.0.0-6.1.10-8
* Tue Mar 21 2023 Shreenidhi Shedi <sshedi@vmware.com> 6.1.10-5
- Fix initramfs trigger
* Thu Mar 16 2023 Keerthana K <keerthanak@vmware.com> 6.1.10-4
- Enable FIPS canister binary usage
* Thu Mar 02 2023 Shreenidhi Shedi <sshedi@vmware.com> 6.1.10-3
- Fix initrd generation logic
- Add dracut, initramfs to requires
* Fri Feb 24 2023 Ankit Jain <ankitja@vmware.com> 6.1.10-2
- Exclude iavf.conf
* Thu Feb 16 2023 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 6.1.10-1
- Update to version 6.1.10
* Thu Feb 16 2023 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 6.0.7-12
- Update i40e driver to v2.19.3 to prevent kernel warnings
* Tue Feb 07 2023 Shreenidhi Shedi <sshedi@vmware.com> 6.0.7-11
- Fix requires
* Thu Feb 02 2023 Keerthana K <keerthanak@vmware.com> 6.0.7-10
- Disable CONFIG_SYSFB_SIMPLEFB
* Wed Jan 25 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 6.0.7-9
- Enable CONFIG_PCI_PF_STUB
* Thu Jan 19 2023 Keerthana K <keerthanak@vmware.com> 6.0.7-8
- Enable VMWGFX configs
* Fri Jan 13 2023 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 6.0.7-7
- Revert "PCI: Clear PCI_STATUS when setting up device"
* Fri Jan 13 2023 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 6.0.7-6
- Fix IRQ affinities of i40e, iavf and ice drivers
* Mon Jan 09 2023 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 6.0.7-5
- Update Intel drivers i40e to v2.16.11, iavf to v4.5.3 and ice to v1.9.11
* Mon Jan 09 2023 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 6.0.7-4
- Reduce latency spikes when process using vfio-pci terminates,
- by avoiding vfio-pci-core toggling io/memory decoding.
* Fri Jan 06 2023 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 6.0.7-3
- Port patch to allow disabling PCI resets from vfio_pci driver to 6.0
- Move the module parameter disable_resets from vfio_pci to
- vfio_pci_core module, to make it work with kernel 6.0.
- Re-enable 0001-Add-PCI-quirk-for-VMware-PCIe-Root-Port.patch
* Fri Jan 06 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 6.0.7-2
- Bump up due to change in elfutils
* Thu Dec 01 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 6.0.7-1
- Update to version 6.0.7
* Thu Oct 20 2022 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 5.10.142-2
- Fix build with latest toolchain
* Wed Sep 28 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.142-1
- Update to version 5.10.142
* Tue Sep 27 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.132-1
- Update to version 5.10.132
* Tue Sep 27 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.118-13
- Backport fixes for CVE-2022-0500
* Tue Sep 27 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.118-12
- Fix for CVE-2022-2585, CVE-2022-2586 and CVE-2022-2588
* Tue Sep 27 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.118-11
- Update iavf driver to v4.4.2
- Update ice driver to v1.8.3
* Mon Sep 26 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.118-10
- .config: enable CROSS_MEMORY_ATTACH
- Add elfutils-libelf-devel required to build objtool
* Mon Sep 26 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.118-9
- Patch for timer padding on guest
* Mon Sep 26 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.118-8
- Backport hrtick changes to fix lost timer wakeups
* Mon Sep 26 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.118-7
- .config: enable CONFIG_NET_ACT_SIMP
* Mon Sep 26 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.118-6
- Enable cgroup v1 stats
- .config: enable PERCPU_STATS
* Fri Sep 23 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.118-5
- Avoid TSC recalibration
* Fri Sep 23 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.118-4
- Enable config options needed to build N3000 FPGA driver.
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
* Tue Sep 20 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.103-3
- Fix for CVE-2022-1016
* Mon Sep 19 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.103-2
- Fix SEV and Hypercall alternative inst. patches
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
- crypto_self_test and broken kattest module enhancements
* Tue Sep 13 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.83-3
- mm: fix percpu allocation for memoryless nodes
- pvscsi: fix disk detection issue
* Tue Sep 13 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.83-2
- remove lvm in add-drivers list
- lvm drivers are built as part of dm-mod
* Mon Sep 12 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.83-1
- Update to version 5.10.83
* Mon Sep 12 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.78-17
- .config: Enable eBPF net packet filtering support.
* Tue Aug 23 2022 Shivani Agarwal <shivania2@vmware.com> 5.10.78-16
- .config: Enable MPLS and other routing related options, namely,
- CGROUP_BPF, XFRM_INTERFACE, NFT_XFRM, NETFILTER_XT_TARGET_NOTRACK
- NET_ACT_BPF, MPLS_ROUTING, MPLS_IPTUNNEL, LWTUNNEL, LWTUNNEL_BPF, PPP
* Mon Aug 08 2022 Shreenidhi Shedi <sshedi@vmware.com> 5.10.78-15
- Scriptlets fixes and improvements
* Wed Aug 03 2022 Keerthana K <keerthanak@vmware.com> 5.10.78-14
- Fix linux headers, doc folder and linux-<uname -r>.cfg names
- Drop rt_version from uname_r
- Patch to skip reading localversion-rt
* Mon Aug 01 2022 Tejaswini Jayaramaiah <jtejaswini@vmware.com> 5.10.78-13
- Enable CONFIG_CGROUP_BPF in config to run containers with cgroup v2
* Fri Jul 22 2022 Him Kalyan Bordoloi <bordoloih@vmware.com> 5.10.78-12
- Add vhost and vhost-net drivers in config
* Wed Jul 13 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.78-11
- Add PCI quirk to allow multiple devices under the same virtual
- PCI bridge to be put into separate IOMMU groups.
* Tue Jul 12 2022 Him Kalyan Bordoloi <bordoloih@vmware.com> 5.10.78-10
- Enable nohz for idle=poll
* Tue Jul 12 2022 Sharan Turlapati <sturlpati@vmware.com> 5.10.78-9
- Allow PCI resets to be disabled from vfio_pci
* Wed Jun 29 2022 Keerthana K <keerthanak@vmware.com> 5.10.78-8
- Reduce FIPS canister memory footprint by disabling CONFIG_KALLSYMS_ALL
- Add only fips_canister-kallsyms to vmlinux instead of all symbols
* Fri Jun 24 2022 Shreenidhi Shedi <sshedi@vmware.com> 5.10.78-7
- Fix debug_package macro usage while adding vmlinux to debuginfo rpm
* Tue Jun 14 2022 Brennan Lamoreaux <blamoreaux@vmware.com> 5.10.78-6
- Enable CONFIG_LIVEPATCH
* Tue Apr 05 2022 Shreenidhi Shedi <sshedi@vmware.com> 5.10.78-5
- Enable CONFIG_EXT2_FS_XATTR & related parameters
* Tue Jan 25 2022 Alexey Makhalov <amakhalov@vmware.com> 5.10.78-4
- .config: enable zstd compression for squashfs.
- .config: enable crypto user api rng.
* Thu Nov 25 2021 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 5.10.78-3
- Disable md5 algorithm for sctp if fips is enabled.
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
* Thu Jun 24 2021 Ankit Jain <ankitja@vmware.com> 5.10.42-4
- Conditional tick_restart upon idle_exit
* Tue Jun 22 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.42-3
- Fix for CVE-2021-3609
* Thu Jun 10 2021 Keerthana K <keerthanak@vmware.com> 5.10.42-2
- Added script to check structure compatibility between fips_canister.o and vmlinux.
* Thu Jun 03 2021 Keerthana K <keerthanak@vmware.com> 5.10.42-1
- Update to version 5.10.42
- Remove XR usb driver support
- .config: Enable CONFIG_FANOTIFY_ACCESS_PERMISSIONS
* Wed Jun 02 2021 Keerthana K <keerthanak@vmware.com> 5.10.35-3
- Fix for CVE-2021-3573
* Thu May 20 2021 Ajay Kaher <akaher@vmware.com> 5.10.35-2
- Fix for CVE-2021-3564
* Mon May 17 2021 Ajay Kaher <akaher@vmware.com> 5.10.35-1
- Update to version 5.10.35
* Thu May 13 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.25-10
- Fix for CVE-2021-23133
* Tue May 11 2021 Ankit Jain <ankitja@vmware.com> 5.10.25-9
- .config: Enable INFINIBAND, MLX5_INFINIBAND
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
* Wed Mar 17 2021 Srinidhi Rao <srinidhir@vmware.com> 5.10.21-2
- Use jitterentropy rng instead of urandom in rng module.
* Tue Mar 16 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 5.10.21-1
- Update to version 5.10.21
* Mon Mar 01 2021 Alexey Makhalov <amakhalov@vmware.com> 5.10.4-10
- FIPS canister update
* Thu Feb 18 2021 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.4-9
- Fix /boot/photon.cfg symlink when /boot is a separate partition.
* Thu Feb 18 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.4-8
- Enable CONFIG_IFB
* Wed Feb 17 2021 Ankit Jain <ankitja@vmware.com> 5.10.4-7
- Added latest out of tree version of Intel ice driver
* Wed Feb 17 2021 Vikash Bansal <bvikas@vmware.com> 5.10.4-6
- Added support for RT RUNTIME GREED
* Mon Feb 15 2021 Keerthana K <keerthanak@vmware.com> 5.10.4-5
- Added crypto_self_test and kattest module.
- These patches are applied when kat_build is enabled.
* Wed Feb 03 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 5.10.4-4
- Update i40e driver to v2.13.10
- Add out of tree iavf driver
- Enable CONFIG_NET_TEAM
* Wed Jan 27 2021 Alexey Makhalov <amakhalov@vmware.com> 5.10.4-3
- Build kernel with FIPS canister.
* Mon Jan 25 2021 Ankit Jain <ankitja@vmware.com> 5.10.4-2
- Enabled CONFIG_WIREGUARD
* Mon Jan 11 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 5.10.4-1
- Update to version 5.10.4
* Tue Nov 10 2020 Keerthana K <keerthanak@vmware.com> 5.9.0-4
- Fix CVE-2020-8694
* Fri Nov 06 2020 Keerthana K <keerthanak@vmware.com> 5.9.0-3
- Fix CVE-2020-25704
* Tue Oct 27 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.9.0-2
- Revert d254087 (clockevents: Stop unused clockevent devices)
- Solve cyclictest regression introduced in 4.1
* Tue Oct 27 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.9.0-1
- Update to version 5.9.0
* Tue Oct 06 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.9.0-rc7.1
- Update to version 5.9.0-rc7
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 4.19.127-2
- openssl 1.1.1
* Tue Jun 23 2020 Keerthana K <keerthanak@vmware.com> 4.19.127-1
- Update to version 4.19.127
* Tue Jun 16 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.115-10
- Add latest out of tree version of i40e driver
* Wed Jun 10 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.115-9
- Enable CONFIG_VFIO_NOIOMMU
* Fri Jun 05 2020 Ankit Jain <ankitja@vmware.com> 4.19.115-8
- Enabled CONFIG_BINFMT_MISC
* Tue Jun 02 2020 Vikash Bansal <bvikas@vmware.com> 4.19.115-7
- Add patch to fix CVE-2019-18885
* Fri May 29 2020 Shreenidhi Shedi <sshedi@vmware.com> 4.19.115-6
- Keep modules of running kernel till next boot
* Fri May 22 2020 Tapas Kundu <tkundu@vmware.com> 4.19.115-5
- Deprecate linux-rt-tools in favor of linux-tools.
- Deprecate python3-perf in favor of linux-python3-perf.
* Thu May 21 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.115-4
- Add ICE network driver support in config
* Fri May 15 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.115-3
- Add uio_pic_generic driver support in config
* Wed May 06 2020 Siddharth Chandrasekaran <csiddharth@vmware.com> 4.19.115-2
- Add patch to fix CVE-2020-10711
* Wed May 06 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.115-1
- Upgrade to 4.19.115
* Wed Apr 29 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.98-5
- Enable additional config options.
* Mon Mar 23 2020 Alexey Makhalov <amakhalov@vmware.com> 4.19.98-4
- Fix perf compilation issue with binutils >= 2.34.
* Sun Mar 22 2020 Tapas Kundu <tkundu@vmware.com> 4.19.98-3
- Added python3-perf subpackage
* Tue Mar 17 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.98-2
- Add tools subpackage to include perf, turbostat and cpupower.
- Update the last few perf python scripts in Linux kernel to use
- python3 syntax.
* Tue Jan 28 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.98-1
- Upgrade to 4.19.98
* Thu Jan 16 2020 Srinidhi Rao <srinidhir@vmware.com> 4.19.82-4
- Enable DRBG HASH and DRBG CTR support.
* Fri Jan 03 2020 Keerthana K <keerthanak@vmware.com> 4.19.82-3
- Remove FIPS patch that enables fips for algorithms which are not fips allowed.
* Thu Dec 12 2019 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.82-2
- Fix patch that wont apply on 4.19.82. Revert when upgraded to 4.19.87 or more
* Tue Nov 12 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.82-1
- Introduce a new kernel flavor 'linux-rt' supporting real-time (RT) features.
