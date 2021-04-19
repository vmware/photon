%global security_hardening none

# Set this flag to 0 to build without canister
%global fips 1

# If kat_build is enabled, canister is not used.
%if 0%{?kat_build:1}
%global fips 0
%endif

Summary:        Kernel
Name:           linux-secure
Version:        5.10.25
Release:        3%{?kat_build:.kat}%{?dist}
License:        GPLv2
URL:            http://www.kernel.org/
Group:          System Environment/Kernel
Vendor:         VMware, Inc.
Distribution:   Photon

%define uname_r %{version}-%{release}-secure

Source0:        http://www.kernel.org/pub/linux/kernel/v5.x/linux-%{version}.tar.xz
%define sha1 linux=ed5006699bea2e1e10f453463f71fce5448d3b6b
Source1:        config-secure
Source2:        initramfs.trigger
Source3:        pre-preun-postun-tasks.inc
Source4:        check_for_config_applicability.inc
%if 0%{?fips}
%define fips_canister_version 4.0.1-5.10.21-3-secure
Source16:       fips-canister-%{fips_canister_version}.tar.bz2
%define sha1 fips-canister=55c0ec3f19f09a8ecaae5f4b31789138026830d4
%endif

# common
Patch0:         net-Double-tcp_mem-limits.patch
Patch1:         SUNRPC-Do-not-reuse-srcport-for-TIME_WAIT-socket.patch
Patch2:         SUNRPC-xs_bind-uses-ip_local_reserved_ports.patch
Patch3:         9p-transport-for-9p.patch
Patch4:	        9p-trans_fd-extend-port-variable-to-u32.patch
Patch5:         vsock-delay-detach-of-QP-with-outgoing-data-59.patch

# RDRAND-based RNG driver to enhance the kernel's entropy pool:
Patch6:         hwrng-rdrand-Add-RNG-driver-based-on-x86-rdrand-inst.patch

#HyperV patches
Patch11:        vmbus-Don-t-spam-the-logs-with-unknown-GUIDs.patch
Patch12:        fork-add-sysctl-to-disallow-unprivileged-CLONE_NEWUSER-by.patch

# Out-of-tree patches from AppArmor:
Patch13:        apparmor-patch-to-provide-compatibility-with-v2.x-ne.patch
Patch14:        apparmor-af_unix-mediation.patch

# VMW:
Patch55:        x86-vmware-Use-Efficient-and-Correct-ALTERNATIVEs-fo.patch
Patch56:        x86-vmware-Log-kmsg-dump-on-panic-510.patch

#Secure:
Patch90:        0001-bpf-ext4-bonding-Fix-compilation-errors.patch
Patch91:        0001-NOWRITEEXEC-and-PAX-features-MPROTECT-EMUTRAMP.patch
Patch92:        0002-Added-PAX_RANDKSTACK.patch
Patch93:        0003-Added-rap_plugin.patch
Patch94:        0004-Fix-PAX-function-pointer-overwritten-for-tasklet-cal.patch

# CVE:
Patch100:       apparmor-fix-use-after-free-in-sk_peer_label.patch
# Fix CVE-2017-1000252
Patch101:       KVM-Don-t-accept-obviously-wrong-gsi-values-via-KVM_.patch
# Fix for CVE-2019-12379
Patch102:       consolemap-Fix-a-memory-leaking-bug-in-drivers-tty-v.patch
# Fix for CVE-2021-29154
Patch103:       bpf-x86_64-Validate-computation-of-branch-displacements.patch
Patch104:       bpf-x86_32-Validate-computation-of-branch-displacements.patch
# Fix for CVE-2021-23133
Patch105:       0001-net-sctp-fix-race-condition-in-sctp_destroy_sock.patch

# Crypto:
# Patch to add drbg_pr_ctr_aes256 test vectors to testmgr
Patch500:       crypto-testmgr-Add-drbg_pr_ctr_aes256-test-vectors.patch
# Patch to call drbg and dh crypto tests from tcrypt
Patch501:       tcrypt-disable-tests-that-are-not-enabled-in-photon.patch
Patch502:       0001-Initialize-jitterentropy-before-ecdh.patch
Patch503:       0002-FIPS-crypto-self-tests.patch
# Patch to remove urandom usage in rng module
Patch504:       0001-FIPS-crypto-rng-Jitterentropy-RNG-as-the-only-RND-source.patch
%if 0%{?fips}
# FIPS canister usage patch
Patch508:       0001-FIPS-canister-binary-usage.patch
%else
%if 0%{?kat_build:1}
Patch509:       0001-Skip-rap-plugin-for-aesni-intel-modules.patch
Patch510:       0003-FIPS-broken-kattest.patch
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
Requires:       filesystem kmod
Requires(pre): (coreutils or toybox)
Requires(preun): (coreutils or toybox)
Requires(post):(coreutils or toybox)
Requires(postun):(coreutils or toybox)

%description
Security hardened Linux kernel.
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
%setup -q -n linux-%{version}
%if 0%{?fips}
%setup -D -b 16 -n linux-%{version}
%endif

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1

%ifarch x86_64
# VMW x86
%patch55 -p1
%patch56 -p1
%endif

#Secure
%patch90 -p1
%patch91 -p1
%patch92 -p1
%patch93 -p1
%patch94 -p1

# CVE
%patch100 -p1
%patch101 -p1
%patch102 -p1
%patch103 -p1
%patch104 -p1
%patch105 -p1

# crypto
%patch500 -p1
%patch501 -p1
%patch502 -p1
%patch503 -p1
%patch504 -p1
%if 0%{?fips}
%patch508 -p1
%else
%if 0%{?kat_build:1}
%patch509 -p1
%patch510 -p1
%endif
%endif

%build
make mrproper
cp %{SOURCE1} .config
%if 0%{?fips}
cp ../fips-canister-%{fips_canister_version}/fips_canister.o crypto/
cp ../fips-canister-%{fips_canister_version}/fips_canister_wrapper.c crypto/
sed -i 's/# CONFIG_KALLSYMS_ALL is not set/CONFIG_KALLSYMS_ALL=y/' .config
%endif
sed -i 's/CONFIG_LOCALVERSION="-secure"/CONFIG_LOCALVERSION="-%{release}-secure"/' .config

%include %{SOURCE4}

make V=1 KBUILD_BUILD_VERSION="1-photon" KBUILD_BUILD_HOST="photon" ARCH="x86_64" %{?_smp_mflags}

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
install -vdm 755 %{buildroot}/%{_sysconfdir}
install -vdm 755 %{buildroot}/boot
install -vdm 755 %{buildroot}%{_docdir}/linux-%{uname_r}
install -vdm 755 %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}
make INSTALL_MOD_PATH=%{buildroot} modules_install

install -vm 644 arch/x86/boot/bzImage    %{buildroot}/boot/vmlinuz-%{uname_r}
install -vm 400 System.map               %{buildroot}/boot/System.map-%{uname_r}
install -vm 644 .config                  %{buildroot}/boot/config-%{uname_r}
cp -r           Documentation/*          %{buildroot}%{_docdir}/linux-%{uname_r}
install -vdm 755                         %{buildroot}/usr/lib/debug/lib/modules/%{uname_r}
install -vm 644 vmlinux                  %{buildroot}/usr/lib/debug/lib/modules/%{uname_r}/vmlinux-%{uname_r}

# Since we use compressed modules we cann't use load pinning,
# because .ko files will be loaded from the memory (LoadPin: obj=<unknown>)
cat > %{buildroot}/boot/linux-%{uname_r}.cfg << "EOF"
# GRUB Environment Block
photon_cmdline=init=/lib/systemd/systemd ro loglevel=3 quiet no-vmw-sta loadpin.enabled=0 audit=1 slub_debug=P page_poison=1 slab_nomerge pti=on
photon_linux=vmlinuz-%{uname_r}
photon_initrd=initrd.img-%{uname_r}
EOF

# Register myself to initramfs
mkdir -p %{buildroot}/%{_localstatedir}/lib/initramfs/kernel
cat > %{buildroot}/%{_localstatedir}/lib/initramfs/kernel/%{uname_r} << "EOF"
--add-drivers "tmem xen-scsifront xen-blkfront xen-acpi-processor xen-evtchn xen-gntalloc xen-gntdev xen-privcmd xen-pciback xenfs hv_utils hv_vmbus hv_storvsc hv_netvsc hv_sock hv_balloon cn lvm dm-mod"
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
%exclude /usr/src

%files docs
%defattr(-,root,root)
%{_defaultdocdir}/linux-%{uname_r}/*

%files devel
%defattr(-,root,root)
/lib/modules/%{uname_r}/build
/usr/src/linux-headers-%{uname_r}

%changelog
*   Mon Apr 19 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.25-3
-   Fix for CVE-2021-23133
*   Thu Apr 15 2021 Srinidhi Rao <srinidhir@vmware.com> 5.10.25-2
-   Fix for CVE-2021-29154
*   Mon Mar 22 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 5.10.25-1
-   Update to version 5.10.25
*   Sun Mar 21 2021 Alexey Makhalov <amakhalov@vmware.com> 5.10.21-3
-   Do not execute some tests twice
-   Support future disablement of des3
-   Do verbose build
-   Canister update.
*   Mon Mar 15 2021 Srinidhi Rao <srinidhir@vmware.com> 5.10.21-2
-   Use jitterentropy rng instead of urandom in rng module.
*   Mon Mar 08 2021 Vikash Bansal <bvikas@vmware.com> 5.10.21-1
-   Update to version 5.10.21
*   Mon Mar 01 2021 Alexey Makhalov <amakhalov@vmware.com> 5.10.4-8
-   FIPS canister update
*   Thu Feb 18 2021 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.4-7
-   Fix /boot/photon.cfg symlink when /boot is a separate partition.
*   Tue Feb 02 2021 Keerthana K <keerthanak@vmware.com> 5.10.4-6
-   Added crypto_self_test and kattest module.
-   These patches are applied when kat_build is enabled.
*   Thu Jan 28 2021 Alexey Makhalov <amakhalov@vmware.com> 5.10.4-5
-   Build with secure FIPS canister.
*   Thu Jan 28 2021 Ankit Jain <ankitja@vmware.com> 5.10.4-4
-   Enabled CONFIG_WIREGUARD
*   Wed Jan 27 2021 Keerthana K <keerthanak@vmware.com> 5.10.4-3
-   Fix rap_plugin code to generate rap_hashes when abs-finish is enabled.
*   Wed Jan 13 2021 Keerthana K <keerthanak@vmware.com> 5.10.4-2
-   Fix build failure.
*   Wed Jan 06 2021 Keerthana K <keerthanak@vmware.com> 5.10.4-1
-   Update to 5.10.4.
*   Tue Nov 10 2020 Keerthana K <keerthanak@vmware.com> 5.9.0-4
-   Fix CVE-2020-8694
*   Fri Nov 06 2020 Keerthana K <keerthanak@vmware.com> 5.9.0-3
-   Fix CVE-2020-25704
*   Tue Nov 03 2020 Srinidhi Rao <srinidhir@vmware.com> 5.9.0-2
-   Remove the support of fipsify and hmacgen
*   Thu Oct 22 2020 Keerthana K <keerthanak@vmware.com> 5.9.0-1
-   Update to 5.9.0
*   Wed Oct 14 2020 Keerthana K <keerthanak@vmware.com> 5.9.0-rc7.1
-   Update to 5.9.0-rc7
*   Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 4.19.127-4
-   openssl 1.1.1
*   Mon Jul 27 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.127-3
-   Fix CVE-2020-14331
*   Tue Jun 23 2020 Tapas Kundu <tkundu@vmware.com> 4.19.127-2
-   Require python3
*   Tue Jun 23 2020 Keerthana K <keerthanak@vmware.com> 4.19.127-1
-   Update to version 4.19.127
*   Fri Jun 05 2020 Ankit Jain <ankitja@vmware.com> 4.19.112-8
-   Enabled CONFIG_BINFMT_MISC
*   Tue Jun 02 2020 Vikash Bansal <bvikas@vmware.com> 4.19.112-7
-   Add patch to fix CVE-2019-18885
*   Fri May 29 2020 Shreenidhi Shedi <sshedi@vmware.com> 4.19.112-6
-   Keep modules of running kernel till next boot
*   Wed May 06 2020 Siddharth Chandrasekaran <csiddharth@vmware.com> 4.19.112-5
-   Add patch to fix CVE-2020-10711
*   Mon May 04 2020 Alexey Makhalov <amakhalov@vmware.com> 4.19.112-4
-   Updated pax_rap patch to support gcc-8.4.0
*   Wed Apr 29 2020 Keerthana K <keerthanak@vmware.com> 4.19.112-3
-   Photon-checksum-generator version update to 1.1.
*   Wed Apr 15 2020 Vikash Bansal <bvikas@vmware.com> 4.19.112-2
-   HMAC-SHA256 digest of hmac_generator module moved to hmacgen package
*   Wed Apr 08 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.112-1
-   Update to version 4.19.112
*   Tue Mar 31 2020 Vikash Bansal <bvikas@vmware.com> 4.19.104-2
-   hmac generation of crypto modules and initrd generation changes if fips=1
*   Wed Mar 25 2020 Vikash Bansal <bvikas@vmware.com> 4.19.104-1
-   Update to version 4.19.104
*   Mon Mar 16 2020 Keerthana K <keerthanak@vmware.com> 4.19.97-6
-   Adding Enhances depedency to hmacgen.
*   Wed Mar 04 2020 Vikash Bansal <bvikas@vmware.com> 4.19.97-5
-   Backporting of patch continuous testing of RNG from urandom
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
*   Thu Jan 16 2020 Srinidhi Rao <srinidhir@vmware.com> 4.19.87-4
-   Enable DRBG HASH and DRBG CTR support.
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
*   Tue Aug 06 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.65-1
-   Update to version 4.19.65
-   Fix CVE-2019-1125 (SWAPGS)
*   Tue Jul 30 2019 Keerthana K <keerthanak@vmware.com> 4.19.52-3
-   Fix postun script.
*   Tue Jul 02 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.52-2
-   Fix 9p vsock 16bit port issue.
*   Mon Jun 17 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.52-1
-   Update to version 4.19.52
-   Fix CVE-2019-12456, CVE-2019-12379, CVE-2019-12380, CVE-2019-12381,
-   CVE-2019-12382, CVE-2019-12378, CVE-2019-12455
*   Tue May 28 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.40-3
-   Change default I/O scheduler to 'deadline' to fix performance issue.
*   Tue May 14 2019 Keerthana K <keerthanak@vmware.com> 4.19.40-2
-   Fix to parse through /boot folder and update symlink (/boot/photon.cfg) if
-   mulitple kernels are installed and current linux kernel is removed.
*   Tue May 07 2019 Ajay Kaher <akaher@vmware.com> 4.19.40-1
-   Update to version 4.19.40
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
*   Thu Jan 10 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.6-4
-   cmdline: added audit=1 pti=on
-   config: PANIC_TIMEOUT=-1, DEBUG_RODATA_TEST=y
*   Wed Jan 09 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.6-3
-   Additional security hardening options in the config.
*   Fri Jan 04 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.6-2
-   Enable AppArmor by default.
*   Mon Dec 10 2018 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.6-1
-   Update to version 4.19.6
*   Thu Nov 15 2018 Ajay Kaher <akaher@vmware.com> 4.19.1-2
-   Adding BuildArch
*   Thu Nov 08 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.1-1
-   Update to version 4.19.1
*   Tue Oct 30 2018 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.18.9-3
-   Fix PAX randkstack and RAP plugin patches to avoid boot panic.
*   Mon Oct 22 2018 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.18.9-2
-   Use updated steal time accounting patch.
*   Tue Sep 25 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.18.9-1
-   Update to version 4.18.9
*   Wed Sep 19 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.14.67-1
-   Update to version 4.14.67
*   Tue Sep 18 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.14.54-4
-   Add rdrand-based RNG driver to enhance kernel entropy.
*   Sun Sep 02 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.14.54-3
-   Add full retpoline support by building with retpoline-enabled gcc.
*   Thu Aug 30 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.14.54-2
-   Apply out-of-tree patches needed for AppArmor.
*   Mon Jul 09 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.14.54-1
-   Update to version 4.14.54
*   Mon Mar 19 2018 Alexey Makhalov <amakhalov@vmware.com> 4.14.8-2
-   Extra hardening: slab_nomerge and some .config changes
*   Fri Feb 16 2018 Alexey Makhalov <amakhalov@vmware.com> 4.14.8-1
-   Version update to v4.14 LTS. Drop aufs support.
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
