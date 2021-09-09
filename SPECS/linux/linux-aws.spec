%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%global security_hardening none
%ifarch x86_64
%define arch x86_64
%define archdir x86
%endif

Summary:        Kernel
Name:           linux-aws
Version:        5.10.61
Release:        2%{?dist}
License:    	GPLv2
URL:        	http://www.kernel.org/
Group:        	System Environment/Kernel
Vendor:         VMware, Inc.
Distribution: 	Photon

%define uname_r %{version}-%{release}-aws


Source0:        http://www.kernel.org/pub/linux/kernel/v5.x/linux-%{version}.tar.xz
%define sha1 linux=7bf2b48bccb0a7fce7a2cfaf801929b3e81f8709
Source1:	config-aws
Source2:	initramfs.trigger
Source3:        pre-preun-postun-tasks.inc
Source4:        check_for_config_applicability.inc

# common
Patch0:         net-Double-tcp_mem-limits.patch
Patch1:         SUNRPC-Do-not-reuse-srcport-for-TIME_WAIT-socket.patch
Patch2:         SUNRPC-xs_bind-uses-ip_local_reserved_ports.patch
Patch3:         9p-transport-for-9p.patch
Patch4:         vsock-delay-detach-of-QP-with-outgoing-data-59.patch
# RDRAND-based RNG driver to enhance the kernel's entropy pool:
Patch5:         hwrng-rdrand-Add-RNG-driver-based-on-x86-rdrand-inst.patch

#HyperV patches
Patch6:        vmbus-Don-t-spam-the-logs-with-unknown-GUIDs.patch

# TODO: Is CONFIG_HYPERV_VSOCKETS the same?
#Patchx:        0014-hv_sock-introduce-Hyper-V-Sockets.patch
Patch7:        fork-add-sysctl-to-disallow-unprivileged-CLONE_NEWUSER-by.patch
# Out-of-tree patches from AppArmor:
Patch8:        apparmor-patch-to-provide-compatibility-with-v2.x-ne.patch
Patch9:        apparmor-af_unix-mediation.patch

#vmxnet3
Patch20:        0001-vmxnet3-Remove-buf_info-from-device-accessible-struc.patch

# VMW:
Patch55:        x86-vmware-Use-Efficient-and-Correct-ALTERNATIVEs-fo-510.patch
Patch56:        x86-vmware-Log-kmsg-dump-on-panic-510.patch

# CVE:
Patch100:       apparmor-fix-use-after-free-in-sk_peer_label.patch
# Fix CVE-2017-1000252
Patch101:       KVM-Don-t-accept-obviously-wrong-gsi-values-via-KVM_.patch
# Fix for CVE-2019-12379
Patch102:       consolemap-Fix-a-memory-leaking-bug-in-drivers-tty-v.patch

#Amazon AWS
Patch201:       0002-bump-the-default-TTL-to-255.patch
Patch202:       0003-bump-default-tcp_wmem-from-16KB-to-20KB.patch
Patch203:       0005-drivers-introduce-AMAZON_DRIVER_UPDATES.patch
Patch204:       0006-drivers-amazon-add-network-device-drivers-support.patch
Patch205:       0007-drivers-amazon-introduce-AMAZON_ENA_ETHERNET.patch
Patch206:       0008-Importing-Amazon-ENA-driver-1.5.0-into-amazon-4.14.y.patch
Patch207:       0009-xen-manage-keep-track-of-the-on-going-suspend-mode.patch
Patch208:       0010-xen-manage-introduce-helper-function-to-know-the-on-.patch
Patch209:       0011-xenbus-add-freeze-thaw-restore-callbacks-support.patch
Patch210:       0012-x86-xen-Introduce-new-function-to-map-HYPERVISOR_sha.patch
Patch211:       0013-x86-xen-add-system-core-suspend-and-resume-callbacks.patch
Patch212:       0014-xen-blkfront-add-callbacks-for-PM-suspend-and-hibern.patch
Patch213:       0015-xen-netfront-add-callbacks-for-PM-suspend-and-hibern.patch
Patch214:       0016-xen-time-introduce-xen_-save-restore-_steal_clock.patch
Patch215:       0017-x86-xen-save-and-restore-steal-clock.patch
Patch216:       0018-xen-events-add-xen_shutdown_pirqs-helper-function.patch
Patch217:       0019-x86-xen-close-event-channels-for-PIRQs-in-system-cor.patch
Patch218:       0020-PM-hibernate-update-the-resume-offset-on-SNAPSHOT_SE.patch
Patch219:       0021-Not-for-upstream-PM-hibernate-Speed-up-hibernation-b.patch
Patch220:       0022-xen-blkfront-add-persistent_grants-parameter.patch
Patch221:       0023-Revert-xen-dont-fiddle-with-event-channel-masking-in.patch
Patch222:       0024-xen-blkfront-Fixed-blkfront_restore-to-remove-a-call.patch
Patch223:       0025-x86-tsc-avoid-system-instability-in-hibernation.patch
Patch224:       0026-block-xen-blkfront-consider-new-dom0-features-on-res.patch
Patch225:       0028-xen-restore-pirqs-on-resume-from-hibernation.patch
Patch226:       0029-xen-Only-restore-the-ACPI-SCI-interrupt-in-xen_resto.patch
Patch227:       0030-net-ena-Import-the-ENA-v2-driver-2.0.2g.patch
Patch228:       0031-xen-netfront-call-netif_device_attach-on-resume.patch
Patch229:       0032-net-ena-replace-dma_zalloc_coherent-with-dma_alloc_c.patch
Patch230:       0060-xen-Restore-xen-pirqs-on-resume-from-hibernation.patch
Patch231:       0061-block-xen-blkfront-bump-the-maximum-number-of-indire.patch
Patch232:       0063-linux-ena-update-ENA-linux-driver-to-version-2.1.1.patch
Patch233:       0064-Update-ena-driver-to-version-2.1.3.patch
Patch234:       0065-Add-Amazon-EFA-driver-version-1.4.patch
Patch235:       0066-libfs-revert-d4f4de5e5ef8efde85febb6876cd3c8ab163199.patch
Patch236:       0070-ena-update-to-2.2.3.patch
Patch237:       0071-ena-update-to-2.2.6.patch
Patch238:       0082-ena-Update-to-2.2.10.patch
Patch239:       0123-drivers-amazon-efa-update-to-1.9.0.patch
Patch240:       drivers-amazon-efa-driver-compilation-fix-on-5.10.patch

# Crypto:
# Patch to add drbg_pr_ctr_aes256 test vectors to testmgr
Patch500:       crypto-testmgr-Add-drbg_pr_ctr_aes256-test-vectors.patch
# Patch to call drbg and dh crypto tests from tcrypt
Patch501:       tcrypt-disable-tests-that-are-not-enabled-in-photon.patch

BuildArch:      x86_64
BuildRequires:  bc
BuildRequires:  kmod-devel
BuildRequires:  glib-devel
BuildRequires:  elfutils-devel
BuildRequires:  libunwind-devel
#BuildRequires:  Linux-PAM-devel
BuildRequires:  openssl-devel
BuildRequires:  procps-ng-devel
BuildRequires:  audit-devel
Requires:       filesystem kmod
Requires(pre): (coreutils or toybox)
Requires(preun): (coreutils or toybox)
Requires(post): (coreutils or toybox)
Requires(postun): (coreutils or toybox)

%description
The Linux package contains the Linux kernel.

%package devel
Summary:        Kernel Dev
Group:          System Environment/Kernel
Requires:       %{name} = %{version}-%{release}
Requires:       python3 gawk
%description devel
The Linux package contains the Linux kernel dev files

%package drivers-gpu
Summary:        Kernel GPU Drivers
Group:          System Environment/Kernel
Requires:       %{name} = %{version}-%{release}
%description drivers-gpu
The Linux package contains the Linux kernel drivers for GPU

%package sound
Summary:        Kernel Sound modules
Group:          System Environment/Kernel
Requires:       %{name} = %{version}-%{release}
%description sound
The Linux package contains the Linux kernel sound support

%package docs
Summary:        Kernel docs
Group:          System Environment/Kernel
Requires:       python3
%description docs
The Linux package contains the Linux kernel doc files

%ifarch x86_64
%package oprofile
Summary:        Kernel driver for oprofile, a statistical profiler for Linux systems
Group:          System Environment/Kernel
Requires:       %{name} = %{version}-%{release}
%description oprofile
Kernel driver for oprofile, a statistical profiler for Linux systems
%endif

%prep
#TODO: remove rcN after 5.9 goes out of rc
# Using autosetup is not feasible
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

#vmxnet3
%patch20 -p1

# VMW
%patch55 -p1
%patch56 -p1

# CVE
%patch100 -p1
%patch101 -p1
%patch102 -p1

#Amazon AWS
%patch201 -p1
%patch202 -p1
%patch203 -p1
%patch204 -p1
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


# crypto
%patch500 -p1
%patch501 -p1

%build
make %{?_smp_mflags} mrproper
cp %{SOURCE1} .config

sed -i 's/CONFIG_LOCALVERSION="-aws"/CONFIG_LOCALVERSION="-%{release}-aws"/' .config

%include %{SOURCE4}

make %{?_smp_mflags} VERBOSE=1 KBUILD_BUILD_VERSION="1-photon" KBUILD_BUILD_HOST="photon" ARCH=%{arch} %{?_smp_mflags}

%define __modules_install_post \
for MODULE in `find %{buildroot}/lib/modules/%{uname_r} -name *.ko` ; do \
    ./scripts/sign-file sha512 certs/signing_key.pem certs/signing_key.x509 $MODULE \
    rm -f $MODULE.{sig,dig} \
    xz $MODULE \
    done \
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
install -vdm 755 %{buildroot}%{_docdir}/%{name}-%{uname_r}
install -vdm 755 %{buildroot}%{_usrsrc}/%{name}-headers-%{uname_r}
install -vdm 755 %{buildroot}/usr/lib/debug/lib/modules/%{uname_r}
make %{?_smp_mflags} INSTALL_MOD_PATH=%{buildroot} modules_install

%ifarch x86_64

# Verify for build-id match
# We observe different IDs sometimes
# TODO: debug it
ID1=`readelf -n vmlinux | grep "Build ID"`
./scripts/extract-vmlinux arch/x86/boot/bzImage > extracted-vmlinux
ID2=`readelf -n extracted-vmlinux | grep "Build ID"`
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
cp -r Documentation/*        %{buildroot}%{_docdir}/%{name}-%{uname_r}
install -vm 644 vmlinux %{buildroot}/usr/lib/debug/lib/modules/%{uname_r}/vmlinux-%{uname_r}
# `perf test vmlinux` needs it
ln -s vmlinux-%{uname_r} %{buildroot}/usr/lib/debug/lib/modules/%{uname_r}/vmlinux

cat > %{buildroot}/boot/%{name}-%{uname_r}.cfg << "EOF"
# GRUB Environment Block
photon_cmdline=init=/lib/systemd/systemd ro loglevel=3 quiet nvme_core.io_timeout=4294967295
photon_linux=vmlinuz-%{uname_r}
photon_initrd=initrd.img-%{uname_r}
EOF

# Register myself to initramfs
mkdir -p %{buildroot}/%{_localstatedir}/lib/initramfs/kernel
cat > %{buildroot}/%{_localstatedir}/lib/initramfs/kernel/%{uname_r} << "EOF"
--add-drivers "tmem xen-scsifront xen-blkfront xen-evtchn xen-gntalloc xen-gntdev xen-privcmd xen-pciback xenfs hv_utils hv_vmbus hv_storvsc hv_netvsc hv_sock hv_balloon dm-mod nvme nvme-core"
EOF

#    Cleanup dangling symlinks
rm -rf %{buildroot}/lib/modules/%{uname_r}/source
rm -rf %{buildroot}/lib/modules/%{uname_r}/build

find . -name Makefile* -o -name Kconfig* -o -name *.pl | xargs  sh -c 'cp --parents "$@" %{buildroot}%{_usrsrc}/%{name}-headers-%{uname_r}' copy
find arch/%{archdir}/include include scripts -type f | xargs  sh -c 'cp --parents "$@" %{buildroot}%{_usrsrc}/%{name}-headers-%{uname_r}' copy
find $(find arch/%{archdir} -name include -o -name scripts -type d) -type f | xargs  sh -c 'cp --parents "$@" %{buildroot}%{_usrsrc}/%{name}-headers-%{uname_r}' copy
find arch/%{archdir}/include Module.symvers include scripts -type f | xargs  sh -c 'cp --parents "$@" %{buildroot}%{_usrsrc}/%{name}-headers-%{uname_r}' copy
%ifarch x86_64
# CONFIG_STACK_VALIDATION=y requires objtool to build external modules
install -vsm 755 tools/objtool/objtool %{buildroot}/usr/src/%{name}-headers-%{uname_r}/tools/objtool/
install -vsm 755 tools/objtool/fixdep %{buildroot}/usr/src/%{name}-headers-%{uname_r}/tools/objtool/
%endif

cp .config %{buildroot}%{_usrsrc}/%{name}-headers-%{uname_r} # copy .config manually to be where it's expected to be
ln -sf "%{_usrsrc}/%{name}-headers-%{uname_r}" "%{buildroot}/lib/modules/%{uname_r}/build"
find %{buildroot}/lib/modules -name '*.ko' -print0 | xargs -0 chmod u+x

# disable (JOBS=1) parallel build to fix this issue:
# fixdep: error opening depfile: ./.plugin_cfg80211.o.d: No such file or directory
# Linux version that was affected is 4.4.26

%include %{SOURCE2}
%include %{SOURCE3}

%post
/sbin/depmod -aq %{uname_r}
ln -sf %{name}-%{uname_r}.cfg /boot/photon.cfg

%post drivers-gpu
/sbin/depmod -aq %{uname_r}

%post sound
/sbin/depmod -aq %{uname_r}

%ifarch x86_64
%post oprofile
/sbin/depmod -aq %{uname_r}
%endif

%files
%defattr(-,root,root)
/boot/System.map-%{uname_r}
/boot/config-%{uname_r}
/boot/vmlinuz-%{uname_r}
%config(noreplace) /boot/%{name}-%{uname_r}.cfg
%config %{_localstatedir}/lib/initramfs/kernel/%{uname_r}
%defattr(0644,root,root)
/lib/modules/%{uname_r}/*
%exclude /lib/modules/%{uname_r}/build
%exclude /lib/modules/%{uname_r}/kernel/drivers/gpu
%exclude /lib/modules/%{uname_r}/kernel/sound
%ifarch x86_64
%exclude /lib/modules/%{uname_r}/kernel/arch/x86/oprofile/
%endif

%files docs
%defattr(-,root,root)
%{_defaultdocdir}/%{name}-%{uname_r}/*

%files devel
%defattr(-,root,root)
/lib/modules/%{uname_r}/build
%{_usrsrc}/%{name}-headers-%{uname_r}

%files drivers-gpu
%defattr(-,root,root)
%exclude /lib/modules/%{uname_r}/kernel/drivers/gpu/drm/cirrus/
/lib/modules/%{uname_r}/kernel/drivers/gpu

%files sound
%defattr(-,root,root)
/lib/modules/%{uname_r}/kernel/sound

%ifarch x86_64
%files oprofile
%defattr(-,root,root)
/lib/modules/%{uname_r}/kernel/arch/x86/oprofile/
%endif

%changelog
*   Thu Sep 09 2021 Alexey Makhalov <amakhalov@vmware.com> 5.10.61-2
-   Remove no-vmw-sta as it is not supported in AWS.
*   Fri Aug 27 2021 Ankit Jain <ankitja@vmware.com> 5.10.61-1
-   Update to version 5.10.61
*   Fri Jul 23 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 5.10.52-1
-   Update to version 5.10.52
*   Thu Jul 15 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 5.10.46-2
-   Fix for CVE-2021-33909
*   Mon Jun 28 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.46-1
-   Update to version 5.10.46
*   Tue Jun 22 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.42-2
-   Fix for CVE-2021-3609
*   Thu Jun 03 2021 Keerthana K <keerthanak@vmware.com> 5.10.42-1
-   Update to version 5.10.42
*   Mon May 17 2021 Ajay Kaher <akaher@vmware.com> 5.10.35-1
-   Update to version 5.10.35
*   Thu May 13 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.25-7
-   Fix for CVE-2021-23133
*   Tue May 11 2021 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.25-6
-   Fix CVE-2020-26147, CVE-2020-24587, CVE-2020-24586, CVE-2020-24588,
-   CVE-2020-26145, CVE-2020-26141
*   Tue May 11 2021 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.25-5
-   Fix CVE-2021-3489, CVE-2021-3490, CVE-2021-3491
*   Tue May 04 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.25-4
-   Remove buf_info from device accessible structures in vmxnet3
*   Mon Apr 19 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.25-3
-   Fix for CVE-2021-23133
*   Thu Apr 15 2021 Srinidhi Rao <srinidhir@vmware.com> 5.10.25-2
-   Fix for CVE-2021-29154
*   Mon Mar 22 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 5.10.25-1
-   Update to version 5.10.25
*   Mon Mar 08 2021 Vikash Bansal <bvikas@vmware.com> 5.10.21-1
-   Update to version 5.10.21
*   Thu Feb 18 2021 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.4-4
-   Fix /boot/photon.cfg symlink when /boot is a separate partition.
*   Tue Feb 02 2021 Keerthana K <keerthanak@vmware.com> 5.10.4-3
-   Removed katbuild patch.
*   Mon Jan 25 2021 Ankit Jain <ankitja@vmware.com> 5.10.4-2
-   Enabled CONFIG_WIREGUARD
*   Mon Jan 11 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 5.10.4-1
-   Update to version 5.10.4
*   Tue Nov 10 2020 Keerthana K <keerthanak@vmware.com> 5.9.0-4
-   Fix CVE-2020-8694
*   Fri Nov 06 2020 Keerthana K <keerthanak@vmware.com> 5.9.0-3
-   Fix CVE-2020-25704
*   Tue Nov 03 2020 Srinidhi Rao <srinidhir@vmware.com> 5.9.0-2
-   Remove the support of fipsify and hmacgen
*   Wed Oct 28 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 5.9.0-1
-   Update to version 5.9.0
*   Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 4.19.127-3
-   openssl 1.1.1
*   Mon Jul 27 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.127-2
-   Fix CVE-2020-14331
*   Tue Jun 23 2020 Keerthana K <keerthanak@vmware.com> 4.19.127-1
-   Update to version 4.19.127
*   Tue Jun 02 2020 Vikash Bansal <bvikas@vmware.com> 4.19.112-6
-   Add patch to fix CVE-2019-18885
*   Fri May 29 2020 Shreenidhi Shedi <sshedi@vmware.com> 4.19.112-5
-   Keep modules of running kernel till next boot
*   Wed May 06 2020 Siddharth Chandrasekaran <csiddharth@vmware.com> 4.19.112-4
-   Add patch to fix CVE-2020-10711
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
*   Thu Jan 02 2020 Keerthana K <keerthanak@vmware.com> 4.19.87-3
-   Modify tcrypt to remove tests for algorithms that are not supported in photon.
-   Added tests for DH, DRBG algorithms.
*   Fri Dec 20 2019 Keerthana K <keerthanak@vmware.com> 4.19.87-2
-   Update fips Kat tests.
*   Fri Dec 06 2019 Ajay Kaher <akaher@vmware.com> 4.19.87-1
-   Update to version 4.19.87
*   Thu Dec 05 2019 Ajay Kaher <akaher@vmware.com> 4.19.84-4
-   Adding nvme and nvme-core to initrd list
-   Removing unwanted modules from initrd list
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
*   Wed Jul 10 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.52-2
-   Deprecate linux-aws-tools in favor of linux-tools.
*   Mon Jun 17 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.52-1
-   Update to version 4.19.52
-   Fix CVE-2019-12456, CVE-2019-12379, CVE-2019-12380, CVE-2019-12381,
-   CVE-2019-12382, CVE-2019-12378, CVE-2019-12455
*   Thu May 23 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.40-3
-   Fix CVE-2019-11191 by deprecating a.out file format support.
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
*   Mon Jan 07 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.6-2
-   Enable additional security hardening options in the config.
*   Mon Dec 10 2018 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.6-1
-   Update to version 4.19.6
-   Enable EFI in config-aws to support kernel signing.
*   Mon Dec 10 2018 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.1-3
-   Set nvme io_timeout to maximum in kernel cmdline.
*   Wed Nov 14 2018 Ajay Kaher <akaher@vmware.com> 4.19.1-2
-   Adding BuildArch
*   Tue Nov 06 2018 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.1-1
-   Update to version 4.19.1
*   Mon Oct 22 2018 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.18.9-1
-   Update to version 4.18.9
*   Mon Oct 08 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.14.67-2
-   Add enhancements from Amazon.
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
*   Thu Feb 22 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.14.8-1
-   First build based on linux.spec and config. No AWS-specific patches yet.
