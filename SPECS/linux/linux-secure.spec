%global security_hardening none
Summary:        Kernel
Name:           linux-secure
Version:        4.19.6
Release:        1%{?kat_build:.%kat_build}%{?dist}
License:        GPLv2
URL:            http://www.kernel.org/
Group:          System Environment/Kernel
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://www.kernel.org/pub/linux/kernel/v4.x/linux-%{version}.tar.xz
%define sha1 linux=d96fd72968960268b2203a3b4aff9497cd3abc61
Source1:        config-secure
Source2:        initramfs.trigger
# common
Patch0:         linux-4.14-Log-kmsg-dump-on-panic.patch
Patch1:         double-tcp_mem-limits.patch
# TODO: disable this patch, check for regressions
#Patch2:         linux-4.9-watchdog-Disable-watchdog-on-virtual-machines.patch
Patch3:         SUNRPC-Do-not-reuse-srcport-for-TIME_WAIT-socket.patch
Patch4:         SUNRPC-xs_bind-uses-ip_local_reserved_ports.patch
Patch5:         vsock-transport-for-9p.patch
Patch6:         4.18-x86-vmware-STA-support.patch
# secure
Patch7:         0001-bpf-ext4-bonding-Fix-compilation-errors.patch
Patch13:        0001-NOWRITEEXEC-and-PAX-features-MPROTECT-EMUTRAMP.patch
Patch14:        0002-Added-PAX_RANDKSTACK.patch
Patch15:        0003-Added-rap_plugin.patch
# HyperV Patches
Patch16:        0004-vmbus-Don-t-spam-the-logs-with-unknown-GUIDs.patch
#FIPS patches - allow some algorithms
Patch24:        4.18-Allow-some-algo-tests-for-FIPS.patch
Patch26:        4.18-add-sysctl-to-disallow-unprivileged-CLONE_NEWUSER-by-default.patch
# Fix CVE-2017-1000252
Patch31:        kvm-dont-accept-wrong-gsi-values.patch
# Out-of-tree patches from AppArmor:
Patch32:        4.17-0001-apparmor-patch-to-provide-compatibility-with-v2.x-ne.patch
Patch33:        4.17-0002-apparmor-af_unix-mediation.patch
Patch34:        4.17-0003-apparmor-fix-use-after-free-in-sk_peer_label.patch
Patch35:        4.18-0001-hwrng-rdrand-Add-RNG-driver-based-on-x86-rdrand-inst.patch
# NSX requirements (should be removed)
Patch99:        LKCM.patch

%if 0%{?kat_build:1}
Patch1000:	%{kat_build}.patch
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
Requires(post):(coreutils or toybox)
%define uname_r %{version}-%{release}-secure

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

%patch0 -p1
%patch1 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch24 -p1
%patch26 -p1
%patch31 -p1
%patch32 -p1
%patch33 -p1
%patch34 -p1
%patch35 -p1

pushd ..
%patch99 -p0
popd

%if 0%{?kat_build:1}
%patch1000 -p1
%endif

%build
# patch vmw_balloon driver
sed -i 's/module_init/late_initcall/' drivers/misc/vmw_balloon.c

make mrproper
cp %{SOURCE1} .config
sed -i 's/CONFIG_LOCALVERSION="-secure"/CONFIG_LOCALVERSION="-%{release}-secure"/' .config
make LC_ALL= oldconfig
make VERBOSE=1 KBUILD_BUILD_VERSION="1-photon" KBUILD_BUILD_HOST="photon" ARCH="x86_64" %{?_smp_mflags}
# build LKCM module
bldroot=`pwd`
pushd ../LKCM
sed -i '/#include <asm\/uaccess.h>/d' drv_fips_test.c
sed -i '/#include <asm\/uaccess.h>/d' fips_test.c
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


%include %{SOURCE2}

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
