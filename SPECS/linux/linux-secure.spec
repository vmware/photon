%global security_hardening none
%global lkcm_version 5.0.0

# SBAT generation of "linux.photon" component
%define linux_photon_generation 1

# Set this flag to 0 to build without canister
%global fips 1

%if 0%{?canister_build}
%global fips 0
%endif

Summary:        Kernel
Name:           linux-secure
Version:        6.1.62
Release:        6%{?kat_build:.kat}%{?dist}
License:        GPLv2
URL:            http://www.kernel.org
Group:          System Environment/Kernel
Vendor:         VMware, Inc.
Distribution:   Photon

%define uname_r %{version}-%{release}-secure
%define _modulesdir /lib/modules/%{uname_r}

Source0:        http://www.kernel.org/pub/linux/kernel/v6.x/linux-%{version}.tar.xz
%define sha512 linux=3d0ba0200fb2337e4c2a0fd417adff32dffa1d24048a457be527556d6d6321e92c7dd80a75f13e2279e1facd4784a3a4e79e1b1ea45b6dd08824a6ab7c0ea0bc
Source1:        config-secure
Source2:        initramfs.trigger
# contains pre, postun, filetriggerun tasks
Source3:        scriptlets.inc
Source4:        check_for_config_applicability.inc

%ifarch x86_64
# Secure Boot
Source5:        linux-sbat.csv.in
%endif

%if 0%{?fips}
Source9:        check_fips_canister_struct_compatibility.inc

%define fips_canister_version 5.0.0-6.1.62-2%{dist}-secure
Source16:       fips-canister-%{fips_canister_version}.tar.bz2
%define sha512 fips-canister=212844b76c93cb7b07d630c558a2968740ab1eec80209ea7f407f3f32a21135e6be74fd5622a252601495d4b3e2fe952c2a17f8501724ea1c804ca6078eef4f8
%endif

%if 0%{?canister_build}
Source17: check_kernel_struct_in_canister.inc
Source18: fips_canister_wrapper.c
Source19: fips_canister_wrapper.h
Source20: fips_integrity.c
Source21: fips_integrity.h
Source22: update_canister_hmac.sh
Source23: canister_combine.lds
Source24: gen_canister_relocs.c
Source25: fips_canister_wrapper_asm.S
Source26: fips_canister_wrapper_internal.h
Source27: aesni-intel_glue_fips_canister_wrapper.c
Source28: testmgr_fips_canister_wrapper.c
%endif

Source29: spec_install_post.inc
Source30: %{name}-dracut.conf

Source31:       photon_sb2020.pem

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
Patch0:  net-Double-tcp_mem-limits.patch
Patch1:  SUNRPC-xs_bind-uses-ip_local_reserved_ports.patch
Patch2:  6.0-9p-transport-for-9p.patch
Patch3:  9p-trans_fd-extend-port-variable-to-u32.patch
Patch4:  vsock-delay-detach-of-QP-with-outgoing-data-59.patch
Patch5:  6.0-Discard-.note.gnu.property-sections-in-generic-NOTES.patch
# Expose Photon kernel macros to identify kernel flavor and version
Patch6:  0001-kbuild-Makefile-Introduce-macros-to-distinguish-Phot.patch
Patch7:  0002-linux-secure-Makefile-Add-kernel-flavor-info-to-the-.patch

Patch8: Performance-over-security-model.patch

# RDRAND-based RNG driver to enhance the kernel's entropy pool:
Patch10:  6.0-0001-hwrng-rdrand-Add-RNG-driver-based-on-x86-rdrand-inst.patch
Patch11:  6.0-0001-cgroup-v1-cgroup_stat-support.patch

#HyperV patches
Patch20:  vmbus-Don-t-spam-the-logs-with-unknown-GUIDs.patch
Patch21:  6.1-0001-fork-add-sysctl-to-disallow-unprivileged-CLONE_NEWUS.patch

# Out-of-tree patches from AppArmor:
Patch30: 6.0-0001-apparmor-patch-to-provide-compatibility-with-v2.x-ne.patch
Patch31: 6.0-0002-apparmor-af_unix-mediation.patch
Patch32: 6.0-0003-apparmor-fix-use-after-free-in-sk_peer_label.patch

# Disable md5 algorithm for sctp if fips is enabled.
Patch33: 6.0-0001-disable-md5-algorithm-for-sctp-if-fips-is-enabled.patch

# VMW: [40..49]
%ifarch x86_64
Patch40: 6.0-x86-vmware-Use-Efficient-and-Correct-ALTERNATIVEs-fo.patch
Patch41: 6.0-x86-vmware-Log-kmsg-dump-on-panic.patch

# Secure Boot and Kernel Lockdown
Patch42: 0001-kernel-lockdown-when-UEFI-secure-boot-enabled.patch
Patch43: 0002-Add-.sbat-section.patch
Patch44: 0003-Verify-SBAT-on-kexec.patch
%endif

#Secure:
Patch51: 0002-NOWRITEEXEC-and-PAX-features-MPROTECT-EMUTRAMP.patch
Patch52: 0003-gcc-rap-plugin-with-kcfi.patch
Patch53: 0004-Fix-PAX-function-pointer-overwritten-for-tasklet-cal.patch
Patch54: fix-warn-definition.patch

# SEV-ES, TDX
%ifarch x86_64
Patch61: 0001-x86-boot-unconditional-preserve-CR4.MCE.patch
%endif

# CVE:
# Fix CVE-2017-1000252
Patch100: KVM-Don-t-accept-obviously-wrong-gsi-values-via-KVM_.patch
#Fix CVE-2023-28464
Patch101: 0001-Bluetooth-Fix-double-free-in-hci_conn_cleanup.patch
# Fix CVE-2023-0597
Patch102: 0001-x86-mm-Randomize-per-cpu-entry-area.patch
Patch103: 0002-x86-mm-Do-not-shuffle-CPU-entry-areas-without-KASLR.patch
# Fix CVE-2023-2176
Patch105: RDMA-core-Refactor-rdma_bind_addr.patch
Patch106: RDMA-core-Update-CMA-destination-address-on-rdma_resolve_addr.patch

# Crypto:
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
%endif

%if 0%{?fips}
# FIPS canister usage patch
Patch508: 6.1.62-2-0001-FIPS-canister-binary-usage.patch
Patch509: 0001-scripts-kallsyms-Extra-kallsyms-parsing.patch
Patch510: FIPS-do-not-allow-not-certified-algos-in-fips-2.patch
%endif

%if 0%{?canister_build}
# Below patches are common for fips and canister_build flags
# 0001-FIPS-canister-binary-usage.patch is renamed as <ver-rel>-0001-FIPS-canister-binary-usage.patch
# in both places until final canister binary is released
Patch10000: 6.1.62-2-0001-FIPS-canister-binary-usage.patch
Patch10001: 0001-scripts-kallsyms-Extra-kallsyms-parsing.patch
# Below patches are specific to canister_build flag
Patch10003: 0002-FIPS-canister-creation.patch
Patch10004: 0003-aesni_intel-Remove-static-call.patch
Patch10005: 0004-Disable-retpoline_sites-and-return_sites-section-in-.patch
Patch10006: 0005-Move-__bug_table-section-to-fips_canister_wrapper.patch
Patch10007: 0006-crypto-Add-prandom-module_kthread_exit-to-canister-w.patch
Patch10008: 0007-crypto-Remove-EXPORT_SYMBOL-EXPORT_SYMBOL_GPL-from-c.patch
Patch10009: 0008-Move-kernel-structures-usage.patch
Patch10010: 0009-ecc-Add-pairwise-consistency-test-for-every-generate.patch
Patch10011: 0001-List-canister-objs-in-a-file.patch

%if 0%{?kat_build}
Patch10012: 0001-Crypto-Tamper-KAT-PCT-and-Integrity-Test.patch
%endif
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
BuildRequires:  bison
BuildRequires: gdb

Requires: kmod
Requires: filesystem
Requires(pre):    (coreutils or coreutils-selinux)
Requires(preun):  (coreutils or coreutils-selinux)
Requires(post):   (coreutils or coreutils-selinux)
Requires(postun): (coreutils or coreutils-selinux)
# Linux-secure handles user.pax.flags extended attribute
# User must have setfattr/getfattr tools available
Requires: attr

%description
Security hardened Linux kernel.
# Enable post FIPS certification
%if 0
This kernel is FIPS certified.
%endif

%package devel
Summary:       Kernel Dev
Group:         System Environment/Kernel
Requires:      python3
Requires:      gawk
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

%if 0%{?canister_build}
%package fips-canister
Summary:       FIPS canister tarball
Group:         System Environment/Kernel
Requires:      python3
Requires:      %{name} = %{version}-%{release}
%description fips-canister
The kernel fips-canister
%endif

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

%autopatch -p1 -m0 -M33

%ifarch x86_64
# VMW x86
%autopatch -p1 -m40 -M49
%endif

#Secure
%autopatch -p1 -m50 -M54

%ifarch x86_64
#SEV-ES, TDX
%autopatch -p1 -m61 -M61
%endif

# CVE
%autopatch -p1 -m100 -M129

# crypto
%autopatch -p1 -m500 -M504

%ifarch x86_64
%autopatch -p1 -m505 -M505
%endif

%if 0%{?fips}
%autopatch -p1 -m508 -M510
%endif

%if 0%{?canister_build}
%autopatch -p1 -m10000 -M10011

%if 0%{?kat_build}
%autopatch -p1 -m10012 -M10012
%endif
%endif

%ifarch x86_64
cp -r ../jitterentropy-%{jent_major_version}-%{jent_ph_version}/ \
      crypto/jitterentropy-%{jent_major_version}/
cp %{SOURCE33} crypto/jitterentropy-%{jent_major_version}/
cp %{SOURCE34} crypto/jitterentropy-%{jent_major_version}/
cp %{SOURCE35} crypto/jitterentropy-%{jent_major_version}/
%endif

make %{?_smp_mflags} mrproper
cp %{SOURCE1} .config
cp %{SOURCE31} photon_sb2020.pem
%if 0%{?fips}
cp ../fips-canister-%{fips_canister_version}/fips_canister.o \
   ../fips-canister-%{fips_canister_version}/fips_canister_wrapper.c \
   ../fips-canister-%{fips_canister_version}/.fips_canister.o.cmd \
   ../fips-canister-%{fips_canister_version}/fips_canister-kallsyms \
   ../fips-canister-%{fips_canister_version}/fips_canister_wrapper_asm.S \
   ../fips-canister-%{fips_canister_version}/fips_canister_wrapper_internal.h \
   ../fips-canister-%{fips_canister_version}/aesni-intel_glue_fips_canister_wrapper.c \
   ../fips-canister-%{fips_canister_version}/testmgr_fips_canister_wrapper.c \
   crypto/
%endif

%if 0%{?canister_build}
cp %{SOURCE18} crypto/
cp %{SOURCE19} crypto/
cp %{SOURCE20} crypto/
cp %{SOURCE21} crypto/
cp %{SOURCE22} crypto/
cp %{SOURCE23} crypto/
cp %{SOURCE24} crypto/
cp %{SOURCE25} crypto/
cp %{SOURCE26} crypto/
cp %{SOURCE27} crypto/
cp %{SOURCE28} crypto/
%endif

sed -i 's/CONFIG_LOCALVERSION="-secure"/CONFIG_LOCALVERSION="-%{release}-secure"/' .config

%if 0%{?canister_build}
sed -i "0,/FIPS_CANISTER_VERSION.*$/s/FIPS_CANISTER_VERSION.*$/FIPS_CANISTER_VERSION \"%{lkcm_version}\"/" crypto/fips_integrity.c
sed -i "0,/FIPS_KERNEL_VERSION.*$/s/FIPS_KERNEL_VERSION.*$/FIPS_KERNEL_VERSION \"%{version}-%{release}-secure\"/" crypto/fips_integrity.c

%if 0%{?kat_build}
sed -i '/CONFIG_CRYPTO_SELF_TEST=y/a CONFIG_CRYPTO_TAMPER_TEST=y' .config
%endif
%endif

%ifarch x86_64
sed -e "s,@@NAME@@,%{name},g" \
    -e "s,@@VERSION_RELEASE@@,%{version}-%{release},g" \
    -e "s,@@LINUX_PH_GEN@@,%{linux_photon_generation},g" \
    %{SOURCE5} > linux-sbat.csv
%endif

%include %{SOURCE4}

%build
make V=1 KBUILD_BUILD_VERSION="1-photon" \
    KBUILD_BUILD_HOST="photon" ARCH="x86_64" %{?_smp_mflags}

%if 0%{?fips}
%include %{SOURCE9}
%endif

%if 0%{?canister_build}
%include %{SOURCE17}
%endif

%install
%if 0%{?canister_build}
install -vdm 755 %{buildroot}%{_libdir}/fips-canister/
pushd crypto/
mkdir fips-canister-%{lkcm_version}-%{version}-%{release}-secure
cp fips_canister.o \
   fips_canister-kallsyms \
   fips_canister_wrapper_asm.S \
   fips_canister_wrapper.c \
   fips_canister_wrapper_internal.h \
   aesni-intel_glue_fips_canister_wrapper.c \
   testmgr_fips_canister_wrapper.c \
   .fips_canister.o.cmd \
   fips-canister-%{lkcm_version}-%{version}-%{release}-secure/
tar -cvjf fips-canister-%{lkcm_version}-%{version}-%{release}-secure.tar.bz2 fips-canister-%{lkcm_version}-%{version}-%{release}-secure/
popd
cp crypto/fips-canister-%{lkcm_version}-%{version}-%{release}-secure.tar.bz2 %{buildroot}%{_libdir}/fips-canister/
%endif

install -vdm 755 %{buildroot}%{_sysconfdir}
install -vdm 755 %{buildroot}/boot
install -vdm 755 %{buildroot}%{_docdir}/linux-%{uname_r}
install -vdm 755 %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}
make %{?_smp_mflags} INSTALL_MOD_PATH=%{buildroot} modules_install

install -vm 644 arch/x86/boot/bzImage %{buildroot}/boot/vmlinuz-%{uname_r}
install -vm 400 System.map %{buildroot}/boot/System.map-%{uname_r}
install -vm 644 .config %{buildroot}/boot/config-%{uname_r}
cp -r Documentation/* %{buildroot}%{_docdir}/linux-%{uname_r}

%if 0%{?__debug_package}
install -vdm 755 %{buildroot}%{_libdir}/debug%{_modulesdir}
install -vm 644 vmlinux %{buildroot}%{_libdir}/debug%{_modulesdir}/vmlinux-%{uname_r}
%endif

# Since we use compressed modules we cann't use load pinning,
# because .ko files will be loaded from the memory (LoadPin: obj=<unknown>)
cat > %{buildroot}/boot/linux-%{uname_r}.cfg << "EOF"
# GRUB Environment Block
photon_cmdline=init=/lib/systemd/systemd ro loglevel=3 quiet loadpin.enabled=0 audit=1 slab_nomerge pti=on
photon_linux=vmlinuz-%{uname_r}
photon_initrd=initrd.img-%{uname_r}
EOF

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

mkdir -p %{buildroot}%{_modulesdir}/dracut.conf.d/
cp -p %{SOURCE30} %{buildroot}%{_modulesdir}/dracut.conf.d/%{name}.conf

%include %{SOURCE2}
%include %{SOURCE3}
%include %{SOURCE29}

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

%if 0%{?canister_build}
%files fips-canister
%defattr(-,root,root)
%{_libdir}/fips-canister/*
%endif

%changelog
* Fri Nov 24 2023 Keerthana K <keerthanak@vmware.com> 6.1.62-6
- Fix initcall for crypto_tamper_test module
* Wed Nov 22 2023 Keerthana K <keerthanak@vmware.com> 6.1.62-5
- Added tamper KAT, PCT and integrity test for CMVP demo
* Wed Nov 22 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 6.1.62-4
- Fix for CVE-2023-2176
* Tue Nov 21 2023 Keerthana K <keerthanak@vmware.com> 6.1.62-3
- Update canister to 5.0.0-6.1.62-2
* Sat Nov 18 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 6.1.62-2
- Fix RSA self tests
* Tue Nov 14 2023 Ankit Jain <ankitja@vmware.com> 6.1.62-1
- Update to version 6.1.62
* Fri Nov 03 2023 Keerthana K <keerthanak@vmware.com> 6.1.60-6
- Add wrapper for task_struct, spinlock etc structures in seqiv and geniv
- Include a script to fail canister build if common kernel structures found
- Disable RSA test vectors added in previous commit due to test failure
- Skip PCT for ECDH p192 curve.
- Fix fcw_warn wrapper API
* Thu Nov 02 2023 Ankit Jain <ankitja@vmware.com> 6.1.60-5
- Fix for CVE-2023-0597
* Mon Oct 30 2023 Keerthana K <keerthanak@vmware.com> 6.1.60-4
- Include seqiv and geniv into canister
- Add missing rsa, drbg_nopr_sha1, rfc4106(gcm(aes)) self-test
* Fri Oct 27 2023 Srish Srinivasan <ssrish@vmware.com> 6.1.60-3
- Create a non-production canister for katbuild kernels when kat_build is
  enabled along with canister_build
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
- Add Pairwise Consistency Test for ECC generated keypairs
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
- canister build for 6.1.53
- Add pkcs1pad test vectors in crytpo_self_test module
* Mon Sep 25 2023 Keerthana K <keerthanak@vmware.com> 6.1.53-3
- Fix CVE-2023-42756
* Mon Sep 25 2023 Keerthana K <keerthanak@vmware.com> 6.1.53-2
- Fix for CVE-2023-42755
* Wed Sep 20 2023 Roye Eshed <eshedr@vmware.com> 6.1.53-1
- Update to version 6.1.53
* Tue Sep 19 2023 Alexey Makhalov <amakhalov@vmware.com> 6.1.45-10
- Apply patches introduced by previous commimt
* Fri Sep 15 2023 Ajay Kaher <akaher@vmware.com> 6.1.45-9
- Fix: net: roundup issue in kmalloc_reserve()
* Mon Sep 11 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 6.1.45-8
- Move all prep to %prep section
* Mon Sep 11 2023 Srish Srinivasan <ssrish@vmware.com> 6.1.45-7
- LKCM 5.0 specific changes to crypto self-tests and tcrypt
* Fri Sep 08 2023 Keerthana K <keerthanak@vmware.com> 6.1.45-6
- Build with jitterentropy v3.4.1
* Fri Sep 08 2023 Keerthana K <keerthanak@vmware.com> 6.1.45-5
- Update fips_canister version 6.1.45-4
* Thu Sep 07 2023 Keerthana K <keerthanak@vmware.com> 6.1.45-4
- Remove jitterentropy from FIPS canister
* Tue Sep 05 2023 Ankit Jain <ankitja@vmware.com> 6.1.45-3
- Fix for CVE-2023-28464
* Sat Sep 02 2023 Guruswamy Basavaiah <bguruswamy@vmware.com> 6.1.45-2
- Cherry pick performance over security option for RETBleed (pos=1)
- patch from Photon 4.0
* Wed Aug 30 2023 Ajay Kaher <akaher@vmware.com> 6.1.45-1
- Update to version 6.1.45
* Mon Aug 21 2023 Kuntal Nayak <nkuntal@vmware.com> 6.1.41-5
- Enable Kconfig CONFIG_KEXEC_FILE for kexec signature verify
* Wed Aug 16 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 6.1.41-4
- Remove DES/DES3 from canister
* Wed Aug 02 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 6.1.41-3
- Zero the runtime_hmac in fips_integrity after use
* Mon Jul 31 2023 Ajay Kaher <akaher@vmware.com> 6.1.41-2
- Fix: unconditional preserve CR4.MCE
* Thu Jul 20 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 6.1.41-1
- Update to version 6.1.41
* Wed Jul 19 2023 Keerthana K <keerthanak@vmware.com> 6.1.37-4
- Fix rap_plugin patch
* Mon Jul 17 2023 Keerthana K <keerthanak@vmware.com> 6.1.37-3
- Use canister version 5.0.0-6.1.37-2
* Tue Jul 11 2023 Keerthana K <keerthanak@vmware.com> 6.1.37-2
- fips_canister: Merge changes from dev branch
* Tue Jul 04 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 6.1.37-1
- Update to version 6.1.37
* Tue Jun 06 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 6.1.32-1
- Update to version 6.1.32
* Wed May 31 2023 Guruswamy Basavaiah <bguruswamy@vmware.com> 6.1.28-4
- disable kconfig CONFIG_RAID6_PQ_BENCHMARK
* Wed May 24 2023 Alexey Makhalov <amakhalov@vmware.com> 6.1.28-3
- PaX: Support xattr 'em' file markings
* Sat May 20 2023 Keerthana K <keerthanak@vmware.com> 6.1.28-2
- Fix canister kernel config
* Fri May 19 2023 Ankit Jain <ankitja@vmware.com> 6.1.28-1
- Update to version 6.1.28
* Wed May 17 2023 Keerthana K <keerthanak@vmware.com> 6.1.10-13
- Fix static call patch and disable RANDSTRUCT
* Tue Apr 25 2023 Shreenidhi Shedi <sshedi@vmware.com> 6.1.10-12
- Remove dracut & initramfs from requires
* Thu Apr 13 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 6.1.10-11
- Use canister version 5.0.0-6.1.10-10
* Wed Apr 12 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 6.1.10-10
- Add new algorithms to canister.
- cfb, cmac, cts, ecdsa, ccm, gcm
* Thu Apr 06 2023 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 6.1.10-9
- Expose Photon kernel macros to simplify building out-of-tree drivers.
* Fri Mar 24 2023 Keerthana K <keerthanak@vmware.com> 6.1.10-8
- Disable FIPS canister binary usage
* Tue Mar 21 2023 Shreenidhi Shedi <sshedi@vmware.com> 6.1.10-7
- Fix initramfs trigger
* Thu Mar 16 2023 Keerthana K <keerthanak@vmware.com> 6.1.10-6
- Build with fips canister binary
* Wed Mar 15 2023 Keerthana K <keerthanak@vmware.com> 6.1.10-5
- Add fips=2 and alg_request_report support
* Thu Mar 02 2023 Shreenidhi Shedi <sshedi@vmware.com> 6.1.10-4
- Fix initrd generation logic
- Add dracut, initramfs to requires
* Thu Feb 23 2023 Keerthana K <keerthanak@vmware.com> 6.1.10-3
- Add stackleak_track_stack() in fips_canister_wrapper
* Fri Feb 17 2023 Keerthana K <keerthanak@vmware.com> 6.1.10-2
- FIPS canister build for 6.1.10 secure kernel
* Wed Feb 08 2023 Keerthana K <keerthanak@vmware.com> 6.1.10-1
- Update to 6.1.10
* Wed Jan 25 2023 Shreenidhi Shedi <sshedi@vmware.com> 6.0.7-8
- Fix requires
* Fri Jan 13 2023 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 6.0.7-7
- Revert "PCI: Clear PCI_STATUS when setting up device"
* Tue Jan 03 2023 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 6.0.7-6
- .config: Enable CONFIG_CGROUP_BPF to run containers with cgroup v2
* Thu Dec 15 2022 Srinidhi Rao <srinidhir@vmware.com> 6.0.7-5
- Fix issues for non-canister builds
* Tue Dec 13 2022 Keerthana K <keerthanak@vmware.com> 6.0.7-4
- FIPS canister relocations in bytecode
* Tue Dec 13 2022 Keerthana K <keerthanak@vmware.com> 6.0.7-3
- FIPS canister build for 6.0.7 secure kernel
* Fri Dec 09 2022 Mukul Sikka <msikka@vmware.com> 6.0.7-2
- Moving fips canister from support to spec
* Mon Nov 28 2022 Keerthana K <keerthanak@vmware.com> 6.0.7-1
- Update to 6.0.7
* Thu Oct 20 2022 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 5.10.142-2
- Fix build with latest toolchain
* Wed Sep 28 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.142-1
- Update to version 5.10.142
* Tue Sep 27 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.132-1
- Update to version 5.10.132
* Tue Sep 27 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.118-7
- Backport fixes for CVE-2022-0500
* Tue Sep 27 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.118-6
- Fix for CVE-2022-2585, CVE-2022-2586 and CVE-2022-2588
* Fri Sep 23 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.118-5
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
- remove lvm, tmem in add-drivers list
- lvm drivers are built as part of dm-mod
- tmem module no longer exists
* Mon Sep 12 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.83-1
- Update to version 5.10.83
* Mon Aug 08 2022 Shreenidhi Shedi <sshedi@vmware.com> 5.10.78-9
- Scriptlets fixes and improvements
* Wed Jun 29 2022 Keerthana K <keerthanak@vmware.com> 5.10.78-8
- Reduce FIPS canister memory footprint by disabling CONFIG_KALLSYMS_ALL
- Add only fips_canister-kallsyms to vmlinux instead of all symbols
* Fri Jun 24 2022 Shreenidhi Shedi <sshedi@vmware.com> 5.10.78-7
- Fix debug_package macro usage while adding vmlinux to debuginfo rpm
* Mon Apr 18 2022 Alexey Makhalov <amakhalov@vmware.com> 5.10.78-6
- Add objtool to the -devel package.
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
