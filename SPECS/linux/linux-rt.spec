%global security_hardening none

# SBAT generation of "linux.photon" component
%define linux_photon_generation 1

%ifarch x86_64
%define arch x86_64
%define archdir x86

# Set this flag to 0 to build without canister
%global fips 1
%endif

Summary:        Kernel
Name:           linux-rt
Version:        6.1.70
Release:        3%{?dist}
License:        GPLv2
URL:            http://www.kernel.org
Group:          System Environment/Kernel
Vendor:         VMware, Inc.
Distribution:   Photon

# Keep rt_version matched up with localversion.patch
%define rt_version rt21
%define uname_r %{version}-%{release}-rt
%define _modulesdir /lib/modules/%{uname_r}

Source0:        http://www.kernel.org/pub/linux/kernel/v6.x/linux-%{version}.tar.xz
%define sha512 linux=e5ad2477005291d21168d9417f329b3ddee47d0af5ada3e7325490f2a673c9546458e84829aff0728f23a07d693470a7650ae64106e46aa76af4cbf92c22cd36

%ifarch x86_64
Source1: config-rt
%endif

Source2: initramfs.trigger
# contains pre, postun, filetriggerun tasks
Source4: scriptlets.inc
Source5: check_for_config_applicability.inc
# Real-Time kernel (PREEMPT_RT patches)
# Source: http://cdn.kernel.org/pub/linux/kernel/projects/rt/6.1/
Source6: preempt_rt.patches

%if 0%{?fips}
Source10: check_fips_canister_struct_compatibility.inc

%define fips_canister_version 5.0.0-6.1.62-13%{?dist}-secure
Source16: fips-canister-%{fips_canister_version}.tar.bz2
%define sha512 fips-canister=51f09934bf41186f5e6a6dd06df84ffc9718f5aaea59eaeb887b639c8f0e8f98caac1339ce51139ab8064c1797631024b10fd92f2c65c35d38b88a17857b96b3
%endif

Source19: spec_install_post.inc

Source20: %{name}-dracut.conf

Source21: photon_sb2020.pem

%ifarch x86_64
# Secure Boot
Source25: linux-sbat.csv.in

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

Patch11: Performance-over-security-model.patch

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

# VMW: [55..60]
Patch55: 6.0-x86-vmware-Use-Efficient-and-Correct-ALTERNATIVEs-fo.patch
Patch56: 6.0-x86-vmware-Log-kmsg-dump-on-panic.patch

# Disable md5 algorithm for sctp if fips is enabled.
Patch57: 6.0-0001-disable-md5-algorithm-for-sctp-if-fips-is-enabled.patch

# Secure Boot and Kernel Lockdown
Patch58: 0001-kernel-lockdown-when-UEFI-secure-boot-enabled.patch
Patch59: 0002-Add-.sbat-section.patch
Patch60: 0003-Verify-SBAT-on-kexec.patch

# SEV-ES, TDX
%ifarch x86_64
Patch61: 0001-x86-boot-unconditional-preserve-CR4.MCE.patch
%endif

# CVE:
Patch100: 6.0-0003-apparmor-fix-use-after-free-in-sk_peer_label.patch
# Fix CVE-2023-0597
Patch102: 0001-x86-mm-Randomize-per-cpu-entry-area.patch
Patch103: 0002-x86-mm-Do-not-shuffle-CPU-entry-areas-without-KASLR.patch
# Fix CVE-2023-2176
Patch105: RDMA-core-Refactor-rdma_bind_addr.patch
Patch106: RDMA-core-Update-CMA-destination-address-on-rdma_resolve_addr.patch
# Fix CVE-2023-5633
Patch107: 0001-drm-vmwgfx-Fix-possible-invalid-drm-gem-put-calls.patch
Patch108: 0002-drm-vmwgfx-Keep-a-gem-reference-to-user-bos-in-surfa.patch
# Fix CVE-2024-0340
Patch109: 0001-vhost_use_kzalloc_instead_of_kmalloc.patch
# Fix CVE-2023-39191
%include %{SOURCE42}

# Real-Time kernel (PREEMPT_RT patches)
# Source: http://cdn.kernel.org/pub/linux/kernel/projects/rt/6.1/
%include %{SOURCE6}

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

# Provide mixed cpusets guarantees for processes placement
Patch717: 0001-Enable-and-enhance-SCHED-isolation.patch

# Crypto:
# Patch to invoke crypto self-tests and add missing test vectors to testmgr
Patch1000: 0002-FIPS-crypto-self-tests.patch
# Patch to call drbg and dh crypto tests from tcrypt
Patch1001: tcrypt-disable-tests-that-are-not-enabled-in-photon.patch
Patch1002: 0001-Initialize-jitterentropy-before-ecdh.patch
# Patch to remove urandom usage in rng module
Patch1003: 0001-FIPS-crypto-rng-Jitterentropy-RNG-as-the-only-RND-source.patch
# Patch to remove urandom usage in drbg and ecc modules
Patch1004: 0003-FIPS-crypto-drbg-Jitterentropy-RNG-as-the-only-RND.patch

%ifarch x86_64
Patch1005: 0001-changes-to-build-with-jitterentropy-v3.4.1.patch
%endif

%if 0%{?fips}
# FIPS canister usage patch
Patch1008: 0001-FIPS-canister-binary-usage.patch
Patch1009: 0001-scripts-kallsyms-Extra-kallsyms-parsing.patch
%endif

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
BuildRequires:  dwarves-devel
# i40e build scripts require getopt
BuildRequires:  util-linux

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
%if 0%{?fips}
# Using autosetup is not feasible
%setup -q -T -D -b 16 -n linux-%{version}
%endif

%ifarch x86_64
# Using autosetup is not feasible
%setup -q -T -D -b 32 -n linux-%{version}
%endif

%autopatch -p1 -m0 -M23

#VMW
%autopatch -p1 -m55 -M60

#SEV-ES, TDX
%ifarch x86_64
%autopatch -p1 -m61 -M61
%endif

# CVE
%autopatch -p1 -m100 -M129

# RT
%autopatch -p1 -m301 -M717

%autopatch -p1 -m1000 -M1004

%ifarch x86_64
%autopatch -p1 -m1005 -M1005
%endif

%if 0%{?fips}
%autopatch -p1 -m1008 -M1009
%endif

%ifarch x86_64
cp -r ../jitterentropy-%{jent_major_version}-%{jent_ph_version}/ \
      crypto/jitterentropy-%{jent_major_version}/
cp %{SOURCE33} crypto/jitterentropy-%{jent_major_version}/
cp %{SOURCE34} crypto/jitterentropy-%{jent_major_version}/
cp %{SOURCE35} crypto/jitterentropy-%{jent_major_version}/
%endif

make %{?_smp_mflags} mrproper
cp %{SOURCE21} photon_sb2020.pem

%ifarch x86_64
cp %{SOURCE1} .config
%endif
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
%endif

sed -i 's/CONFIG_LOCALVERSION="-rt"/CONFIG_LOCALVERSION="-%{release}-rt"/' .config

%ifarch x86_64
sed -e "s,@@NAME@@,%{name},g" \
    -e "s,@@VERSION_RELEASE@@,%{version}-%{release},g" \
    -e "s,@@LINUX_PH_GEN@@,%{linux_photon_generation},g" \
    %{SOURCE25} > linux-sbat.csv
%endif

%include %{SOURCE5}

%build
make %{?_smp_mflags} V=1 KBUILD_BUILD_VERSION="1-photon" KBUILD_BUILD_HOST="photon" ARCH=%{?arch} %{?_smp_mflags}

%if 0%{?fips}
%include %{SOURCE10}
%endif

%install
install -vdm 755 %{buildroot}%{_sysconfdir}
install -vdm 755 %{buildroot}/boot
install -vdm 755 %{buildroot}%{_docdir}/linux-%{uname_r}
install -vdm 755 %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}
install -vdm 755 %{buildroot}%{_libdir}/debug/%{_modulesdir}
make %{?_smp_mflags} INSTALL_MOD_PATH=%{buildroot} modules_install

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
%config(noreplace) %{_modulesdir}/dracut.conf.d/%{name}.conf

%files docs
%defattr(-,root,root)
%{_defaultdocdir}/linux-%{uname_r}/*

%files devel
%defattr(-,root,root)
%{_modulesdir}/build
%{_usrsrc}/linux-headers-%{uname_r}

%changelog
* Tue Jan 16 2024 Ajay Kaher <ajay.kaher@broadcom.com> 6.1.70-3
- Fix CVE-2024-0340
* Mon Jan 08 2024 Roye Eshed <roye.eshed@broadcom.com> 6.1.70-2
- Move Intel i40e, iavf and ice drivers for linux-rt to their own spec files.
* Mon Jan 01 2024 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 6.1.70-1
- Update to version 6.1.70
* Thu Dec 14 2023 Keerthana K <keerthanak@vmware.com> 6.1.62-10
- Update canister to 5.0.0-6.1.62-13
* Thu Dec 14 2023 Keerthana K <keerthanak@vmware.com> 6.1.62-9
- FIPS: Add log messages for approved and non-approved services
- Remove fips=2 logic
* Tue Dec 12 2023 Kuntal Nayak <nkuntal@vmware.com> 6.1.62-8
- Fix CVE-2023-39191
* Fri Dec 08 2023 Srish Srinivasan <ssrish@vmware.com> 6.1.62-7
- Added self-tests for rsa-pkcs1pad in combination with sha1, sha224, sha384 and sha512
* Mon Nov 27 2023 Kuntal Nayak <nkuntal@vmware.com> 6.1.62-6
- Fix CVE-2023-5633
* Sat Nov 25 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 6.1.62-5
- Update canister to 5.0.0-6.1.62-7
* Wed Nov 22 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 6.1.62-4
- Fix for CVE-2023-2176
* Tue Nov 21 2023 Keerthana K <keerthanak@vmware.com> 6.1.62-3
- Update canister to 5.0.0-6.1.62-2
* Sat Nov 18 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 6.1.62-2
- Fix RSA self tests
* Tue Nov 14 2023 Ankit Jain <ankitja@vmware.com> 6.1.62-1
- Update to version 6.1.62
* Fri Oct 27 2023 Ankit Jain <ankitja@vmware.com> 6.1.60-4
- Fix for CVE-2023-0597
* Fri Oct 27 2023 Srish Srinivasan <ssrish@vmware.com> 6.1.60-3
- Remove kat_build and its associated spec changes
* Fri Oct 27 2023 Srinidhi Rao <srinidhir@vmware.com> 6.1.60-2
- Jitterentropy sample collection support in ACVP Build.
* Fri Oct 27 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 6.1.60-1
- Upgrade to 6.1.60
* Thu Oct 26 2023 Alexey Makhalov <amakhalov@vmware.com> 6.1.56-8
- Add .sbat section for bzImage
- Introduce SBAT verificaion in addition to signature on kexec
* Thu Oct 26 2023 Srish Srinivasan <ssrish@vmware.com> 6.1.56-7
- Upgrade canister to 5.0.0-6.1.56-6
* Tue Oct 24 2023 Srish Srinivasan <ssrish@vmware.com> 6.1.56-6
- Added cts to crypto self-tests
- Removed rsa(pkcs1pad, sha256), rsa(pkcs1pad, sha512),
  cbc, and ctr from crypto self-tests
- Added ECC pubkey generation and verification success messages
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
* Tue Oct 03 2023 Kuntal Nayak <nkunal@vmware.com> 6.1.53-7
- Kconfig to lockdown kernel in UEFI Secure Boot
* Sun Oct 01 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 6.1.53-6
- Fix for CVE-2023-42754
* Fri Sep 29 2023 Keerthana K <keerthanak@vmware.com> 6.1.53-5
- Enable fips and update canister binary version 5.0.0-6.1.53-4
- Removed jent_lock struct from ignore list of check_fips_canister
* Tue Sep 26 2023 Keerthana K <keerthanak@vmware.com> 6.1.53-4
- Add pkcs1pad test vectors in crytpo_self_test module
* Mon Sep 25 2023 Keerthana K <keerthanak@vmware.com> 6.1.53-3
- Fix CVE-2023-42756
* Mon Sep 25 2023 Keerthana K <keerthanak@vmware.com> 6.1.53-2
- Fix for CVE-2023-42755
* Wed Sep 20 2023 Roye Eshed <eshedr@vmware.com> 6.1.53-1
- Update to version 6.1.53
* Tue Sep 19 2023 Alexey Makhalov <amakhalov@vmware.com> 6.1.45-9
- Enable and enhance sched isolation.
- Apply patches introduced by previous commimt
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
* Wed Aug 30 2023 Ajay Kaher <akaher@vmware.com> 6.1.45-1
- Update to version 6.1.45
* Mon Aug 21 2023 Kuntal Nayak <nkuntal@vmware.com> 6.1.41-4
- Enable Kconfig CONFIG_KEXEC_FILE for kexec signature verify
* Wed Aug 09 2023 Srish Srinivasan <ssrish@vmware.com> 6.1.41-3
- Enable CONFIG_DEBUG_INFO_BTF=y
* Mon Jul 31 2023 Ajay Kaher <akaher@vmware.com> 6.1.41-2
- Fix: unconditional preserve CR4.MCE
* Thu Jul 20 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 6.1.41-1
- Update to version 6.1.41
* Mon Jul 17 2023 Keerthana K <keerthanak@vmware.com> 6.1.37-2
- Use canister version 5.0.0-6.1.37-2
* Tue Jul 04 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 6.1.37-1
- Update to version 6.1.37
* Tue Jun 06 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 6.1.32-1
- Update to version 6.1.32
* Wed May 31 2023 Guruswamy Basavaiah <bguruswamy@vmware.com> 6.1.28-2
- disable kconfig CONFIG_RAID6_PQ_BENCHMARK
* Tue May 16 2023 Ankit Jain <ankitja@vmware.com> 6.1.28-1
- Update to version 6.1.28
* Tue Apr 25 2023 Shreenidhi Shedi <sshedi@vmware.com> 6.1.10-11
- Remove dracut & initramfs from requires
* Fri Apr 14 2023 Him Kalyan Bordoloi <bordoloih@vmware.com> 6.1.10-10
- Update Guest timer advancement feature
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
