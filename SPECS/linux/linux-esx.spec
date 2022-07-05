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

%ifarch aarch64
%define arch arm64
%define archdir arm64
%endif

Summary:        Kernel
Name:           linux-esx
Version:        5.10.78
Release:        14%{?kat_build:.kat}%{?dist}
License:        GPLv2
URL:            http://www.kernel.org
Group:          System Environment/Kernel
Vendor:         VMware, Inc.
Distribution:   Photon

%define uname_r %{version}-%{release}-esx
%define _modulesdir /lib/modules/%{uname_r}

Source0:        http://www.kernel.org/pub/linux/kernel/v5.x/linux-%{version}.tar.xz
%define sha512 linux=3ec352e6d50480dddfa3fa903c37f72b1b027c541862182e910013c5d461431d4782fb4908c74513d20a4c093abf0318ca9a76bac6c1b56145d0fb21ad194169

Source1:        config-esx_%{_arch}
Source2:        initramfs.trigger
Source3:        pre-preun-postun-tasks.inc
Source4:        check_for_config_applicability.inc
Source5:        modify_kernel_configs.inc

%define i40e_version 2.15.9
Source6:        https://sourceforge.net/projects/e1000/files/i40e%20stable/%{i40e_version}/i40e-%{i40e_version}.tar.gz
%define sha512 i40e=891723116fca72c51851d7edab0add28c2a0b4c4768a7646794c8b3bc4d44a1786115e67f05cfa5bb3bc484a4e07145fc4640a621f3bc755cc07257b1b531dd5

%define iavf_version 4.2.7
Source7:       https://sourceforge.net/projects/e1000/files/iavf%20stable/%{iavf_version}/iavf-%{iavf_version}.tar.gz
%define sha512 iavf=1f491d9ab76444db1d5f0edbd9477eb3b15fa75f73785715ff8af31288b0490c01b54cc50b6bac3fc36d9caf25bae94fb4ef4a7e73d4360c7031ece32d725e70

%define ice_version 1.6.4
Source8:       https://sourceforge.net/projects/e1000/files/ice%20stable/%{ice_version}/ice-%{ice_version}.tar.gz
%define sha512 ice=e88be3b416184d5c157aecda79b2580403b67c68286221ae154a92fa1d46cacd23aa55365994fa53f266d6df4ca2046cc2fcb35620345fd23e80b90a45ec173c

%if 0%{?fips}
Source9:        check_fips_canister_struct_compatibility.inc

%define fips_canister_version 4.0.1-5.10.21-3-secure
Source16:       fips-canister-%{fips_canister_version}.tar.bz2
%define sha512 fips-canister=1d3b88088a23f7d6e21d14b1e1d29496ea9e38c750d8a01df29e1343034f74b0f3801d1f72c51a3d27e9c51113c808e6a7aa035cb66c5c9b184ef8c4ed06f42a
%endif

# common
Patch0: net-Double-tcp_mem-limits.patch
# TODO: disable this patch, check for regressions
#Patch: linux-4.9-watchdog-Disable-watchdog-on-virtual-machines.patch
Patch1: SUNRPC-Do-not-reuse-srcport-for-TIME_WAIT-socket.patch
Patch2: SUNRPC-xs_bind-uses-ip_local_reserved_ports.patch
Patch3: 9p-transport-for-9p.patch
Patch4: 9p-trans_fd-extend-port-variable-to-u32.patch
Patch5: vsock-delay-detach-of-QP-with-outgoing-data-59.patch
Patch6: hwrng-rdrand-Add-RNG-driver-based-on-x86-rdrand-inst.patch
Patch7: 9p-file-attributes-caching-support.patch
Patch8: 9p-support-for-local-file-lock.patch
Patch9: fork-add-sysctl-to-disallow-unprivileged-CLONE_NEWUSER-by.patch
Patch10: apparmor-patch-to-provide-compatibility-with-v2.x-ne.patch
Patch11: apparmor-af_unix-mediation.patch

# floppy:
Patch17: 0001-floppy-lower-printk-message-priority.patch

#vmxnet3
Patch20: 0001-vmxnet3-Remove-buf_info-from-device-accessible-struc.patch

# aarch64
Patch21: 0001-x86-hyper-generalize-hypervisor-type-detection.patch
Patch22: 0002-arm64-hyper-implement-VMware-hypervisor-features.patch
Patch23: 0003-scsi-vmw_pvscsi-add-arm64-support.patch
# Current VMCI driver crashes during module load in fusion arm64
# Commented out these patches till we get a new version of VMCI driver
#Patch: 0004-vmw_vmci-add-arm64-support.patch
#Patch: 0005-vmw_balloon-add-arm64-support.patch
Patch24: 0004-vmxnet3-build-only-for-x86-and-arm64.patch

# VMW:
Patch30: x86-vmware-Use-Efficient-and-Correct-ALTERNATIVEs-fo.patch
Patch31: x86-vmware-Log-kmsg-dump-on-panic-510.patch
Patch32: x86-vmware-Fix-steal-time-clock-under-SEV.patch
Patch33: x86-probe_roms-Skip-OpROM-probing-if-running-as-VMwa.patch

# -esx
Patch50: init-do_mounts-recreate-dev-root.patch
Patch51: serial-8250-do-not-probe-U6-16550A-fifo-size.patch
Patch52: 01-clear-linux.patch
Patch53: 02-pci-probe.patch
Patch54: poweroff-without-firmware.patch
Patch55: 04-quiet-boot.patch
Patch56: 05-pv-ops-clocksource.patch
# TODO: make it working for v5.9+
#Patch57: 06-pv-ops-boot_clock.patch
Patch58: 07-vmware-only.patch
Patch59: initramfs-support-for-page-aligned-format-newca.patch
Patch60: 0001-Remove-OOM_SCORE_ADJ_MAX-limit-check.patch
Patch61: 0001-fs-VTAR-archive-to-TPMFS-extractor.patch
Patch62: 0001-fs-A-new-VTARFS-file-system-to-mount-VTAR-archive.patch
Patch63: halt-on-panic.patch
Patch64: initramfs-multiple-image-extraction-support.patch
Patch65: initramfs-support-selective-freeing-of-initramfs-images.patch
Patch66: initramfs-large-files-support-for-newca-format.patch
Patch67: revert-x86-entry-Align-entry-text-section-to-PMD-boundary.patch

# Hotplug support without firmware
Patch69: 0001-vmw_extcfg-hotplug-without-firmware-support.patch
Patch70: 0002-vmw_extcfg-hotplug-without-firmware-support.patch
Patch71: 0003-vmw_extcfg-hotplug-without-firmware-support.patch

#TARFS
Patch80: 0001-fs-TARFS-file-system-to-mount-TAR-archive.patch

# initialize MMCONFIG
Patch85: 0001-initialize-MMCONFIG-if-already-not-initialized.patch
Patch86: 0001-MMIO_should_have_more_priority_then_IO.patch

# Disable md5 algorithm for sctp if fips is enabled.
Patch90: 0001-disable-md5-algorithm-for-sctp-if-fips-is-enabled.patch

# CVE:
Patch100: apparmor-fix-use-after-free-in-sk_peer_label.patch
# Fix CVE-2017-1000252
Patch101: KVM-Don-t-accept-obviously-wrong-gsi-values-via-KVM_.patch
# Fix for CVE-2019-12379
Patch102: consolemap-Fix-a-memory-leaking-bug-in-drivers-tty-v.patch

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
%if 0%{?fips}
# FIPS canister usage patch
Patch508: 0001-FIPS-canister-binary-usage.patch
%else
%if 0%{?kat_build}
Patch510: 0003-FIPS-broken-kattest.patch
%endif
%endif

# SEV:
Patch600: 0079-x86-sev-es-Disable-BIOS-ACPI-RSDP-probing-if-SEV-ES-.patch
Patch601: 0080-x86-boot-Enable-vmw-serial-port-via-Super-I-O.patch
Patch602: 0081-x86-sev-es-Disable-use-of-WP-via-PAT-for-__sme_early.patch
Patch603: x86-sev-es-load-idt-before-entering-long-mode-to-han-510.patch
Patch604: x86-swiotlb-Adjust-SWIOTLB-bounce-buffer-size-for-SE.patch
Patch605: x86-sev-es-Do-not-unroll-string-IO-for-SEV-ES-guests.patch

#Patches for i40e driver
Patch1500: i40e-xdp-remove-XDP_QUERY_PROG-and-XDP_QUERY_PROG_HW-XDP-.patch
Patch1501: 0001-Add-support-for-gettimex64-interface.patch

#Patches for ice driver
Patch1510: 0001-ice-Use-PTP_SYS_OFFSET_EXTENDED_IOCTL-support.patch

#Patches for iavf driver
Patch1511: 0001-iavf-Use-PTP_SYS_OFFSET_EXTENDED_IOCTL-support.patch

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

%if 0%{?fips}
BuildRequires: gdb
%endif

Requires: kmod
Requires: filesystem
Requires(pre): (coreutils or toybox)
Requires(preun): (coreutils or toybox)
Requires(post):(coreutils or toybox)
Requires(postun):(coreutils or toybox)

%description
The Linux kernel build for GOS for VMware hypervisor.
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

%autopatch -p1 -m0 -M20

%ifarch aarch64
%autopatch -p1 -m21 -M24
%endif

# VMW
%ifarch x86_64
%autopatch -p1 -m30 -M33
%endif

# -esx
%autopatch -p1 -m50 -M56

%ifarch x86_64
%patch58 -p1
%endif

%autopatch -p1 -m59 -M80

%ifarch x86_64
%autopatch -p1 -m85 -M86
%endif

%patch90 -p1

# CVE
%autopatch -p1 -m100 -M102

# crypto
%autopatch -p1 -m500 -M506

%if 0%{?fips}
%patch508 -p1
%else
%if 0%{?kat_build}
%patch510 -p1
%endif
%endif

%ifarch x86_64
# SEV
%autopatch -p1 -m600 -M605
%endif

%ifarch x86_64
#Patches for i40e driver
pushd ../i40e-%{i40e_version}
%autopatch -p1 -m1500 -M1501
popd

#Patches for ice driver
pushd ../ice-%{ice_version}
%patch1510 -p1
popd

#Patches for iavf driver
pushd ../iavf-%{iavf_version}
%patch1511 -p1
popd
%endif

%build
make %{?_smp_mflags} mrproper
cp %{SOURCE1} .config
%if 0%{?fips}
cp ../fips-canister-%{fips_canister_version}/fips_canister.o \
   ../fips-canister-%{fips_canister_version}/fips_canister_wrapper.c \
   crypto/
# Change m to y for modules that are in the canister
%include %{SOURCE5}
%else
%if 0%{?kat_build}
# Change m to y for modules in katbuild
%include %{SOURCE5}
%endif
%endif
sed -i 's/CONFIG_LOCALVERSION="-esx"/CONFIG_LOCALVERSION="-%{release}-esx"/' .config

%include %{SOURCE4}

make %{?_smp_mflags} VERBOSE=1 KBUILD_BUILD_VERSION="1-photon" \
    KBUILD_BUILD_HOST="photon" ARCH=%{arch} %{?_smp_mflags}

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

# build ice module
pushd ../ice-%{ice_version}
make %{?_smp_mflags} -C src KSRC=${bldroot} clean
make %{?_smp_mflags} -C src KSRC=${bldroot} %{?_smp_mflags}
popd

# build iavf module
pushd ../iavf-%{iavf_version}
make %{?_smp_mflags} -C src KSRC=${bldroot} clean
make %{?_smp_mflags} -C src KSRC=${bldroot} %{?_smp_mflags}
popd
%endif

# Do not compress modules which will be loaded at boot time
# to speed up boot process
%define __modules_install_post \
  find %{buildroot}%{_modulesdir} -name "*.ko" \! \"(" -name "*evdev*" -o -name "*mousedev*" -o -name "*sr_mod*"  -o -name "*cdrom*" -o -name "*vmwgfx*" -o -name "*drm_kms_helper*" -o -name "*ttm*" -o -name "*psmouse*" -o -name "*drm*" -o -name "*apa_piix*" -o -name "*vmxnet3*" -o -name "*i2c_core*" -o -name "*libata*" -o -name "*processor*" -o -path "*ipv6*" \")" | xargs xz \
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
make %{?_smp_mflags} ARCH=%{arch} INSTALL_MOD_PATH=%{buildroot} modules_install

%ifarch x86_64

# install i40e module
bldroot="${PWD}"
pushd ../i40e-%{i40e_version}
make %{?_smp_mflags} -C src KSRC=${bldroot} INSTALL_MOD_PATH=%{buildroot} \
    INSTALL_MOD_DIR=extra MANDIR=%{_mandir} modules_install mandocs_install
popd

# install ice module
pushd ../ice-%{ice_version}
make %{?_smp_mflags} -C src KSRC=${bldroot} INSTALL_MOD_PATH=%{buildroot} \
    INSTALL_MOD_DIR=extra MANDIR=%{_mandir} modules_install mandocs_install
popd

# install iavf module
pushd ../iavf-%{iavf_version}
make %{?_smp_mflags} -C src KSRC=${bldroot} INSTALL_MOD_PATH=%{buildroot} \
    INSTALL_MOD_DIR=extra MANDIR=%{_mandir} modules_install mandocs_install
popd

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

# Register myself to initramfs
mkdir -p %{buildroot}%{_localstatedir}/lib/initramfs/kernel
cat > %{buildroot}%{_localstatedir}/lib/initramfs/kernel/%{uname_r} << "EOF"
--add-drivers "lvm dm-mod"
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
%exclude %{_modulesdir}/build
%ifarch x86_64
%{_sysconfdir}/modprobe.d/iavf.conf
# ICE driver firmware files are packaged in linux-firmware
%exclude /lib/firmware/updates/intel/ice
%endif

%files docs
%defattr(-,root,root)
%{_defaultdocdir}/linux-%{uname_r}/*
%ifarch x86_64
%{_mandir}/*
%endif

%files devel
%defattr(-,root,root)
%{_modulesdir}/build
%{_usrsrc}/linux-headers-%{uname_r}

%changelog
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
