%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%global security_hardening none
%global photon_checksum_generator_version 1.1
%ifarch x86_64
%define arch x86_64
%define archdir x86
%endif

%ifarch aarch64
%define arch arm64
%define archdir arm64
%endif

Summary:        Kernel
Name:           linux
Version:        5.9.0
Release:        rc4.1%{?kat_build:.kat}%{?dist}
License:    	GPLv2
URL:        	http://www.kernel.org/
Group:        	System Environment/Kernel
Vendor:         VMware, Inc.
Distribution: 	Photon

%define uname_r %{version}-%{release}

#TODO: remove rcN after 5.9 goes out of rc
%define lnx_rc_ver 5.9.0-rc4
%define lnx_rc_local_ver .1%{?kat_build:.kat}%{?dist}

Source0:        http://www.kernel.org/pub/linux/kernel/v5.x/linux-%{lnx_rc_ver}.tar.xz
%define sha1 linux=19af0c05c8e16c7148dbcb3201880370f7405a4e
Source1:	config_%{_arch}
Source2:	initramfs.trigger
%define ena_version 2.2.11
Source3:	https://github.com/amzn/amzn-drivers/archive/ena_linux_%{ena_version}.tar.gz
%define sha1 ena_linux=48a9812d05805a7eefd3f87cc48a95d668b26719
Source4:	xr_usb_serial_common_lnx-3.6-and-newer-pak.tar.xz
%define sha1 xr=74df7143a86dd1519fa0ccf5276ed2225665a9db
%define sgx_version 1.8
Source5:	https://github.com/intel/SGXDataCenterAttestationPrimitives/archive/DCAP_%{sgx_version}.tar.gz
%define sha1 DCAP=6161846c2ba03099a2307f28a91e9d45627614d7
Source6:        pre-preun-postun-tasks.inc
Source7:        check_for_config_applicability.inc
# Photon-checksum-generator kernel module
Source8:        https://github.com/vmware/photon-checksum-generator/releases/photon-checksum-generator-%{photon_checksum_generator_version}.tar.gz
%define sha1 photon-checksum-generator=1d5c2e1855a9d1368cf87ea9a8a5838841752dc3
Source9:        genhmac.inc
%define i40e_version 2.12.6
Source10:       https://sourceforge.net/projects/e1000/files/i40e%20stable/%{i40e_version}/i40e-%{i40e_version}.tar.gz
%define sha1 i40e=e1a28cdf7c122f177ed75b7615a0a0e221d21ff4
Source12:       ena-xdp-remove-XDP_QUERY_PROG-and-XDP_QUERY_PROG_HW-XDP-.patch
Source13:       i40e-xdp-remove-XDP_QUERY_PROG-and-XDP_QUERY_PROG_HW-XDP-.patch
Source14:       i40e-Remove-read_barrier_depends-in-favor-of-READ_ON.patch
Source15:       i40e-Fix-minor-compilation-error.patch

# common
Patch0:         net-Double-tcp_mem-limits.patch
Patch1:         SUNRPC-Do-not-reuse-srcport-for-TIME_WAIT-socket.patch
Patch2:         SUNRPC-xs_bind-uses-ip_local_reserved_ports.patch
Patch3:         9p-transport-for-9p.patch
Patch4:	        9p-trans_fd-extend-port-variable-to-u32.patch
Patch5:         vsock-delay-detach-of-QP-with-outgoing-data-59.patch
# RDRAND-based RNG driver to enhance the kernel's entropy pool:
Patch6:         hwrng-rdrand-Add-RNG-driver-based-on-x86-rdrand-inst.patch

# ttyXRUSB support
Patch10:	usb-acm-exclude-exar-usb-serial-ports-nxt.patch
#HyperV patches
Patch11:        vmbus-Don-t-spam-the-logs-with-unknown-GUIDs.patch

# TODO: Is CONFIG_HYPERV_VSOCKETS the same?
#Patchx:        0014-hv_sock-introduce-Hyper-V-Sockets.patch
Patch12:        fork-add-sysctl-to-disallow-unprivileged-CLONE_NEWUSER-by.patch
# Out-of-tree patches from AppArmor:
Patch13:        apparmor-patch-to-provide-compatibility-with-v2.x-ne.patch
Patch14:        apparmor-af_unix-mediation.patch

# VMW:
Patch55:        x86-vmware-Use-Efficient-and-Correct-ALTERNATIVEs-fo.patch
Patch56:        x86-vmware-Log-kmsg-dump-on-panic.patch
Patch57:        x86-vmware-Fix-steal-time-clock-under-SEV.patch

# CVE:
Patch100:       apparmor-fix-use-after-free-in-sk_peer_label.patch
# Fix CVE-2017-1000252
Patch101:       KVM-Don-t-accept-obviously-wrong-gsi-values-via-KVM_.patch
# Fix for CVE-2019-12379
Patch102:       consolemap-Fix-a-memory-leaking-bug-in-drivers-tty-v.patch

# Crypto:
# Patch to add drbg_pr_ctr_aes256 test vectors to testmgr
Patch500:       crypto-testmgr-Add-drbg_pr_ctr_aes256-test-vectors.patch
# Patch to call drbg and dh crypto tests from tcrypt
Patch501:       tcrypt-disable-tests-that-are-not-enabled-in-photon.patch

%if 0%{?kat_build:1}
Patch510:       crypto-testmgr-break-KAT-fips-intentionally.patch
%endif

# SEV:
Patch600:       0001-KVM-SVM-nested-Don-t-allocate-VMCB-structures-on-sta.patch
Patch601:       0002-KVM-SVM-Add-GHCB-definitions.patch
Patch602:       0003-KVM-SVM-Add-GHCB-Accessor-functions.patch
Patch603:       0004-KVM-SVM-Use-__packed-shorthand.patch
Patch604:       0005-x86-cpufeatures-Add-SEV-ES-CPU-feature.patch
Patch605:       0006-x86-traps-Move-pf-error-codes-to-asm-trap_pf.h.patch
Patch606:       0007-x86-insn-Make-inat-tables.c-suitable-for-pre-decompr.patch
Patch607:       0008-x86-umip-Factor-out-instruction-fetch.patch
Patch608:       0009-x86-umip-Factor-out-instruction-decoding.patch
Patch609:       0010-x86-insn-Add-insn_get_modrm_reg_off.patch
Patch610:       0011-x86-insn-Add-insn_has_rep_prefix-helper.patch
Patch611:       0012-x86-boot-compressed-64-Disable-red-zone-usage.patch
Patch612:       0013-x86-boot-compressed-64-Add-IDT-Infrastructure.patch
Patch613:       0014-x86-boot-compressed-64-Rename-kaslr_64.c-to-ident_ma.patch
Patch614:       0015-x86-boot-compressed-64-Add-page-fault-handler.patch
Patch615:       0016-x86-boot-compressed-64-Always-switch-to-own-page-tab.patch
Patch616:       0017-x86-boot-compressed-64-Don-t-pre-map-memory-in-KASLR.patch
Patch617:       0018-x86-boot-compressed-64-Change-add_identity_map-to-ta.patch
Patch618:       0019-x86-boot-compressed-64-Add-stage1-VC-handler.patch
Patch619:       0020-x86-boot-compressed-64-Call-set_sev_encryption_mask-.patch
Patch620:       0021-x86-boot-compressed-64-Check-return-value-of-kernel_.patch
Patch621:       0022-x86-boot-compressed-64-Add-set_page_en-decrypted-hel.patch
Patch622:       0023-x86-boot-compressed-64-Setup-GHCB-Based-VC-Exception.patch
Patch623:       0024-x86-boot-compressed-64-Unmap-GHCB-page-before-bootin.patch
Patch624:       0025-x86-sev-es-Add-support-for-handling-IOIO-exceptions.patch
Patch625:       0026-x86-fpu-Move-xgetbv-xsetbv-into-separate-header.patch
Patch626:       0027-x86-sev-es-Add-CPUID-handling-to-VC-handler.patch
Patch627:       0028-x86-idt-Move-IDT-to-data-segment.patch
Patch628:       0029-x86-idt-Split-idt_data-setup-out-of-set_intr_gate.patch
Patch629:       0030-x86-head-64-Install-startup-GDT.patch
Patch630:       0031-x86-head-64-Setup-MSR_GS_BASE-before-calling-into-C-.patch
Patch631:       0032-x86-head-64-Load-GDT-after-switch-to-virtual-address.patch
Patch632:       0033-x86-head-64-Load-segment-registers-earlier.patch
Patch633:       0034-x86-head-64-Switch-to-initial-stack-earlier.patch
Patch634:       0035-x86-head-64-Make-fixup_pointer-static-inline.patch
Patch635:       0036-x86-head-64-Load-IDT-earlier.patch
Patch636:       0037-x86-head-64-Move-early-exception-dispatch-to-C-code.patch
Patch637:       0038-x86-head-64-Set-CR4.FSGSBASE-early.patch
Patch638:       0039-x86-sev-es-Add-SEV-ES-Feature-Detection.patch
Patch639:       0040-x86-sev-es-Print-SEV-ES-info-into-kernel-log.patch
Patch640:       0041-x86-sev-es-Compile-early-handler-code-into-kernel-im.patch
Patch641:       0042-x86-sev-es-Setup-early-VC-handler.patch
Patch642:       0043-x86-sev-es-Setup-GHCB-based-boot-VC-handler.patch
Patch643:       0044-x86-sev-es-Setup-per-cpu-GHCBs-for-the-runtime-handl.patch
Patch644:       0045-x86-sev-es-Allocate-and-Map-IST-stack-for-VC-handler.patch
Patch645:       0046-x86-sev-es-Adjust-VC-IST-Stack-on-entering-NMI-handl.patch
Patch646:       0047-x86-dumpstack-64-Add-noinstr-version-of-get_stack_in.patch
Patch647:       0048-x86-entry-64-Add-entry-code-for-VC-handler.patch
Patch648:       0049-x86-sev-es-Add-Runtime-VC-Exception-Handler.patch
Patch649:       0050-x86-sev-es-Wire-up-existing-VC-exit-code-handlers.patch
Patch650:       0051-x86-sev-es-Handle-instruction-fetches-from-user-spac.patch
Patch651:       0052-x86-sev-es-Handle-MMIO-events.patch
Patch652:       0053-x86-sev-es-Handle-MMIO-String-Instructions.patch
Patch653:       0054-x86-sev-es-Handle-MSR-events.patch
Patch654:       0055-x86-sev-es-Handle-DR7-read-write-events.patch
Patch655:       0056-x86-sev-es-Handle-WBINVD-Events.patch
Patch656:       0057-x86-sev-es-Handle-RDTSC-P-Events.patch
Patch657:       0058-x86-sev-es-Handle-RDPMC-Events.patch
Patch658:       0059-x86-sev-es-Handle-INVD-Events.patch
Patch659:       0060-x86-sev-es-Handle-MONITOR-MONITORX-Events.patch
Patch660:       0061-x86-sev-es-Handle-MWAIT-MWAITX-Events.patch
Patch661:       0062-x86-sev-es-Handle-VMMCALL-Events.patch
Patch662:       0063-x86-sev-es-Handle-AC-Events.patch
Patch663:       0064-x86-sev-es-Handle-DB-Events.patch
Patch664:       0065-x86-paravirt-Allow-hypervisor-specific-VMMCALL-handl.patch
Patch665:       0066-x86-kvm-Add-KVM-specific-VMMCALL-handling-under-SEV-.patch
Patch666:       0067-x86-vmware-Add-VMware-specific-handling-for-VMMCALL-.patch
Patch667:       0068-x86-realmode-Add-SEV-ES-specific-trampoline-entry-po.patch
Patch668:       0069-x86-realmode-Setup-AP-jump-table.patch
Patch669:       0070-x86-smpboot-Setup-TSS-for-starting-AP.patch
Patch670:       0071-x86-head-64-Don-t-call-verify_cpu-on-starting-APs.patch
Patch671:       0072-x86-head-64-Rename-start_cpu0.patch
Patch672:       0073-x86-sev-es-Support-CPU-offline-online.patch
Patch673:       0074-x86-sev-es-Handle-NMI-State.patch
Patch674:       0075-x86-efi-Add-GHCB-mappings-when-SEV-ES-is-active.patch
Patch675:       0076-x86-sev-es-Check-required-CPU-features-for-SEV-ES.patch
Patch676:       0079-x86-sev-es-Disable-BIOS-ACPI-RSDP-probing-if-SEV-ES-.patch
Patch677:       0080-x86-boot-Enable-vmw-serial-port-via-Super-I-O.patch
Patch678:       0081-x86-sev-es-Disable-use-of-WP-via-PAT-for-__sme_early.patch
Patch679:       0082-x86-sev-es-load-idt-before-entering-long-mode-to-han.patch

BuildRequires:  bc
BuildRequires:  kmod-devel
BuildRequires:  glib-devel
BuildRequires:  elfutils-devel
BuildRequires:  libunwind-devel
#BuildRequires:  Linux-PAM-devel
BuildRequires:  openssl-devel
BuildRequires:  procps-ng-devel
BuildRequires:  audit-devel
BuildRequires:  elfutils-libelf-devel
BuildRequires:  binutils-devel
BuildRequires:  xz-devel
BuildRequires:  slang-devel
BuildRequires:  python3-devel
%ifarch x86_64
BuildRequires:  pciutils-devel
BuildRequires:  libcap-devel
%endif
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
Obsoletes:      linux-dev
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

%package drivers-sound
Summary:        Kernel Sound modules
Group:          System Environment/Kernel
Requires:       %{name} = %{version}-%{release}
%description drivers-sound
The Linux package contains the Linux kernel sound support

%package docs
Summary:        Kernel docs
Group:          System Environment/Kernel
Requires:       python3
%description docs
The Linux package contains the Linux kernel doc files

%ifarch x86_64
%package drivers-intel-sgx
Summary:	Intel SGX driver
Group:		System Environment/Kernel
Requires:	%{name} = %{version}-%{release}
Requires(post): /usr/sbin/groupadd
%description drivers-intel-sgx
This Linux package contains Intel SGX kernel module.

%package oprofile
Summary:        Kernel driver for oprofile, a statistical profiler for Linux systems
Group:          System Environment/Kernel
Requires:       %{name} = %{version}-%{release}
%description oprofile
Kernel driver for oprofile, a statistical profiler for Linux systems
%endif

%package tools
Summary:        This package contains the 'perf' performance analysis tools for Linux kernel
Group:          System/Tools
Requires:       (%{name} = %{version} or linux-esx = %{version} or linux-aws = %{version} or linux-rt = %{version})
Requires:       audit elfutils-libelf binutils-libs xz-libs libunwind slang python3
%ifarch x86_64
Requires:       pciutils
%endif
Obsoletes:      linux-aws-tools <= 4.19.52-1
Provides:       linux-aws-tools
%description tools
This package contains kernel tools like perf, turbostat and cpupower.

%package python3-perf
Summary:        Python bindings for applications that will manipulate perf events.
Group:          Development/Libraries
Requires:       linux-tools = %{version}-%{release}
Requires:       python3

%description python3-perf
This package provides a module that permits applications written in the
Python programming language to use the interface to manipulate perf events.

%package hmacgen
Summary:	HMAC SHA256/HMAC SHA512 generator
Group:		System Environment/Kernel
Requires:      %{name} = %{version}-%{release}
Enhances:       %{name}
%description hmacgen
This Linux package contains hmac sha generator kernel module.

%prep
#TODO: remove rcN after 5.9 goes out of rc
%setup -q -n linux-%{lnx_rc_ver}
%ifarch x86_64
%setup -D -b 3 -n linux-%{lnx_rc_ver}
%setup -D -b 4 -n linux-%{lnx_rc_ver}
%setup -D -b 5 -n linux-%{lnx_rc_ver}
%setup -D -b 10 -n linux-%{lnx_rc_ver}
%endif
%setup -D -b 8 -n linux-%{lnx_rc_ver}

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1

%ifarch x86_64
# VMW x86
%patch55 -p1
%patch56 -p1
%patch57 -p1
%endif

# CVE
%patch100 -p1
%patch101 -p1
%patch102 -p1

# crypto
%patch500 -p1
%patch501 -p1

%if 0%{?kat_build:1}
%patch510 -p1
%endif

%ifarch x86_64
# SEV
%patch600 -p1
%patch601 -p1
%patch602 -p1
%patch603 -p1
%patch604 -p1
%patch605 -p1
%patch606 -p1
%patch607 -p1
%patch608 -p1
%patch609 -p1
%patch610 -p1
%patch611 -p1
%patch612 -p1
%patch613 -p1
%patch614 -p1
%patch615 -p1
%patch616 -p1
%patch617 -p1
%patch618 -p1
%patch619 -p1
%patch620 -p1
%patch621 -p1
%patch622 -p1
%patch623 -p1
%patch624 -p1
%patch625 -p1
%patch626 -p1
%patch627 -p1
%patch628 -p1
%patch629 -p1
%patch630 -p1
%patch631 -p1
%patch632 -p1
%patch633 -p1
%patch634 -p1
%patch635 -p1
%patch636 -p1
%patch637 -p1
%patch638 -p1
%patch639 -p1
%patch640 -p1
%patch641 -p1
%patch642 -p1
%patch643 -p1
%patch644 -p1
%patch645 -p1
%patch646 -p1
%patch647 -p1
%patch648 -p1
%patch649 -p1
%patch650 -p1
%patch651 -p1
%patch652 -p1
%patch653 -p1
%patch654 -p1
%patch655 -p1
%patch656 -p1
%patch657 -p1
%patch658 -p1
%patch659 -p1
%patch660 -p1
%patch661 -p1
%patch662 -p1
%patch663 -p1
%patch664 -p1
%patch665 -p1
%patch666 -p1
%patch667 -p1
%patch668 -p1
%patch669 -p1
%patch670 -p1
%patch671 -p1
%patch672 -p1
%patch673 -p1
%patch674 -p1
%patch675 -p1
%patch676 -p1
%patch677 -p1
%patch678 -p1
%patch679 -p1
%endif

%build
make mrproper
cp %{SOURCE1} .config

sed -i 's/CONFIG_LOCALVERSION=""/CONFIG_LOCALVERSION="%{lnx_rc_local_ver}"/' .config

%include %{SOURCE7}

# Set/add CONFIG_CROSS_COMPILE= if needed
if [ %{_host} != %{_build} ]; then
grep -q CONFIG_CROSS_COMPILE= .config && sed -i '/^CONFIG_CROSS_COMPILE=/c\CONFIG_CROSS_COMPILE="%{_host}-"' .config || \
	echo 'CONFIG_CROSS_COMPILE="%{_host}-"' >> .config
fi

make VERBOSE=1 KBUILD_BUILD_VERSION="1-photon" KBUILD_BUILD_HOST="photon" ARCH=%{arch} %{?_smp_mflags}
make ARCH=%{arch} -C tools perf PYTHON=python3

%ifarch x86_64
#build turbostat and cpupower
make ARCH=%{arch} -C tools turbostat cpupower PYTHON=python3

# build ENA module
bldroot=`pwd`
pushd ../amzn-drivers-ena_linux_%{ena_version}/kernel/linux/ena
patch -p4 < %{SOURCE12}
make -C $bldroot M=`pwd` VERBOSE=1 modules %{?_smp_mflags}
popd

# build XR module
bldroot=`pwd`
pushd ../xr_usb_serial_common_lnx-3.6-and-newer-pak
make KERNELDIR=$bldroot ARCH=%{arch} %{?_smp_mflags} all
popd

# build Intel SGX module
bldroot=`pwd`
pushd ../SGXDataCenterAttestationPrimitives-DCAP_%{sgx_version}/driver/linux
make KDIR=$bldroot ARCH=%{arch} %{?_smp_mflags}
popd

# build i40e module
bldroot=`pwd`
pushd ../i40e-%{i40e_version}
patch -p1 < %{SOURCE13}
patch -p1 < %{SOURCE14}
patch -p1 < %{SOURCE15}
make -C src KSRC=$bldroot clean
make -C src KSRC=$bldroot %{?_smp_mflags}
popd
%endif

#build photon-checksum-generator module
bldroot=`pwd`
pushd ../photon-checksum-generator-%{photon_checksum_generator_version}/kernel
make -C $bldroot M=`pwd` modules
popd

%define __modules_install_post \
for MODULE in `find %{buildroot}/lib/modules/%{uname_r} -name *.ko` ; do \
    ./scripts/sign-file sha512 certs/signing_key.pem certs/signing_key.x509 $MODULE \
    rm -f $MODULE.{sig,dig} \
    xz $MODULE \
    done \
%{nil}

%include %{SOURCE9}

# We want to compress modules after stripping. Extra step is added to
# the default __spec_install_post.
%define __spec_install_post\
    %{?__debug_package:%{__debug_install_post}}\
    %{__arch_install_post}\
    %{__os_install_post}\
    %{__modules_install_post}\
    %{__modules_gen_hmac}\
%{nil}

%install
install -vdm 755 %{buildroot}%{_sysconfdir}
install -vdm 755 %{buildroot}/boot
install -vdm 755 %{buildroot}%{_docdir}/%{name}-%{uname_r}
install -vdm 755 %{buildroot}%{_usrsrc}/%{name}-headers-%{uname_r}
install -vdm 755 %{buildroot}/usr/lib/debug/lib/modules/%{uname_r}
make ARCH=%{arch} INSTALL_MOD_PATH=%{buildroot} modules_install

%ifarch x86_64
# install ENA module
bldroot=`pwd`
pushd ../amzn-drivers-ena_linux_%{ena_version}/kernel/linux/ena
make -C $bldroot M=`pwd` INSTALL_MOD_PATH=%{buildroot} modules_install
popd

# install XR module
bldroot=`pwd`
pushd ../xr_usb_serial_common_lnx-3.6-and-newer-pak
make ARCH=%{arch} KERNELDIR=$bldroot INSTALL_MOD_PATH=%{buildroot} modules_install
popd

# install Intel SGX module
bldroot=`pwd`
pushd ../SGXDataCenterAttestationPrimitives-DCAP_%{sgx_version}/driver/linux
mkdir -p %{buildroot}%{_sysconfdir}/udev/rules.d
install -vm 644 10-sgx.rules %{buildroot}/%{_sysconfdir}/udev/rules.d
mkdir -p %{buildroot}/lib/modules/%{uname_r}/extra
install -vm 644 intel_sgx.ko %{buildroot}/lib/modules/%{uname_r}/extra/
popd

# install i40e module
bldroot=`pwd`
pushd ../i40e-%{i40e_version}
make -C src KSRC=$bldroot INSTALL_MOD_PATH=%{buildroot} INSTALL_MOD_DIR=extra MANDIR=%{_mandir} modules_install mandocs_install
popd

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

#install photon-checksum-generator module
bldroot=`pwd`
pushd ../photon-checksum-generator-%{photon_checksum_generator_version}/kernel
make -C $bldroot M=`pwd` INSTALL_MOD_PATH=%{buildroot} modules_install
popd

%ifarch aarch64
install -vm 644 arch/arm64/boot/Image %{buildroot}/boot/vmlinuz-%{uname_r}
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
photon_cmdline=init=/lib/systemd/systemd ro loglevel=3 quiet no-vmw-sta
photon_linux=vmlinuz-%{uname_r}
photon_initrd=initrd.img-%{uname_r}
EOF

# Register myself to initramfs
mkdir -p %{buildroot}/%{_localstatedir}/lib/initramfs/kernel
cat > %{buildroot}/%{_localstatedir}/lib/initramfs/kernel/%{uname_r} << "EOF"
--add-drivers "tmem xen-scsifront xen-blkfront xen-acpi-processor xen-evtchn xen-gntalloc xen-gntdev xen-privcmd xen-pciback xenfs hv_utils hv_vmbus hv_storvsc hv_netvsc hv_sock hv_balloon cn lvm dm-mod megaraid_sas"
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
install -vsm 755 tools/objtool/objtool %{buildroot}%{_usrsrc}/%{name}-headers-%{uname_r}/tools/objtool/
install -vsm 755 tools/objtool/fixdep %{buildroot}%{_usrsrc}/%{name}-headers-%{uname_r}/tools/objtool/
%endif

cp .config %{buildroot}%{_usrsrc}/%{name}-headers-%{uname_r} # copy .config manually to be where it's expected to be
ln -sf "%{_usrsrc}/%{name}-headers-%{uname_r}" "%{buildroot}/lib/modules/%{uname_r}/build"
find %{buildroot}/lib/modules -name '*.ko' -print0 | xargs -0 chmod u+x

%ifarch aarch64
cp arch/arm64/kernel/module.lds %{buildroot}%{_usrsrc}/%{name}-headers-%{uname_r}/arch/arm64/kernel/
%endif

make -C tools ARCH=%{arch} DESTDIR=%{buildroot} prefix=%{_prefix} perf_install PYTHON=python3
make -C tools/perf ARCH=%{arch} DESTDIR=%{buildroot} prefix=%{_prefix} PYTHON=python3 install-python_ext
%ifarch x86_64
make -C tools ARCH=%{arch} DESTDIR=%{buildroot} prefix=%{_prefix} mandir=%{_mandir} turbostat_install cpupower_install PYTHON=python3
%endif

%include %{SOURCE2}
%include %{SOURCE6}

%post
/sbin/depmod -a %{uname_r}
ln -sf %{name}-%{uname_r}.cfg /boot/photon.cfg

%post hmacgen
/sbin/depmod -a %{uname_r}

%post drivers-gpu
/sbin/depmod -a %{uname_r}

%post drivers-sound
/sbin/depmod -a %{uname_r}

%ifarch x86_64
%post drivers-intel-sgx
/sbin/depmod -a %{uname_r}
getent group sgx_prv >/dev/null || groupadd -r sgx_prv

%post oprofile
/sbin/depmod -a %{uname_r}
%endif

%files
%defattr(-,root,root)
/boot/System.map-%{uname_r}
/boot/config-%{uname_r}
/boot/vmlinuz-%{uname_r}
/boot/.vmlinuz-%{uname_r}.hmac
%config(noreplace) /boot/%{name}-%{uname_r}.cfg
%config %{_localstatedir}/lib/initramfs/kernel/%{uname_r}
%defattr(0644,root,root)
/lib/modules/%{uname_r}/*
%exclude /lib/modules/%{uname_r}/build
%exclude /lib/modules/%{uname_r}/kernel/drivers/gpu
%exclude /lib/modules/%{uname_r}/kernel/sound
%exclude /lib/modules/%{uname_r}/extra/hmac_generator.ko.xz
%exclude /lib/modules/%{uname_r}/extra/.hmac_generator.ko.xz.hmac
%ifarch aarch64
%exclude /lib/modules/%{uname_r}/kernel/drivers/staging/vc04_services/bcm2835-audio
%endif
%ifarch x86_64
%exclude /lib/modules/%{uname_r}/kernel/arch/x86/oprofile/
%exclude /lib/modules/%{uname_r}/extra/intel_sgx.ko.xz
%endif

%files docs
%defattr(-,root,root)
%{_docdir}/%{name}-%{uname_r}/*
# For out-of-tree Intel i40e driver.
%ifarch x86_64
%{_mandir}/*
%endif

%files devel
%defattr(-,root,root)
/lib/modules/%{uname_r}/build
%{_usrsrc}/%{name}-headers-%{uname_r}

%files drivers-gpu
%defattr(-,root,root)
%exclude /lib/modules/%{uname_r}/kernel/drivers/gpu/drm/cirrus/
/lib/modules/%{uname_r}/kernel/drivers/gpu

%files drivers-sound
%defattr(-,root,root)
/lib/modules/%{uname_r}/kernel/sound
%ifarch aarch64
/lib/modules/%{uname_r}/kernel/drivers/staging/vc04_services/bcm2835-audio
%endif

%files hmacgen
%defattr(-,root,root)
/lib/modules/%{uname_r}/extra/hmac_generator.ko.xz
/lib/modules/%{uname_r}/extra/.hmac_generator.ko.xz.hmac

%ifarch x86_64
%files drivers-intel-sgx
%defattr(-,root,root)
/lib/modules/%{uname_r}/extra/intel_sgx.ko.xz
%config(noreplace) %{_sysconfdir}/udev/rules.d/10-sgx.rules

%files oprofile
%defattr(-,root,root)
/lib/modules/%{uname_r}/kernel/arch/x86/oprofile/
%endif

%files tools
%defattr(-,root,root)
%ifarch x86_64
/usr/lib64/traceevent
%endif
%ifarch aarch64
/usr/lib/traceevent
%endif
%{_bindir}
%{_sysconfdir}/bash_completion.d/perf
%{_libexecdir}/perf-core
%{_datadir}/perf-core
%{_docdir}/perf-tip
%{_libdir}/perf/examples/bpf/*
%{_libdir}/perf/include/bpf/*
%ifarch x86_64
%{_includedir}/cpufreq.h
%{_includedir}/cpuidle.h
%{_lib64dir}/libcpupower.so*
%{_docdir}/packages/cpupower
%{_datadir}/bash-completion/completions/cpupower
%config(noreplace) %{_sysconfdir}/cpufreq-bench.conf
%{_sbindir}/cpufreq-bench
%{_mandir}/man1/cpupower*.gz
%{_mandir}/man8/turbostat*.gz
%{_datadir}/locale/*/LC_MESSAGES/cpupower.mo
%endif

%files python3-perf
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
*   Mon Sep 21 2020 Bo Gan <ganb@vmware.com> 5.9.0-rc4.1
-   Update to 5.9.0-rc4
-   AMD SEV-ES Support
-   RPI4 Support
-   config_common: Reduce linked-in modules
-   Drop NXP LS10XXa board support
*   Tue Sep 08 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 4.19.127-6
-   Fix build failure with binutils updated to 2.35
*   Wed Aug 05 2020 Sharan Turlapati <sturlapati@vmware.com> 4.19.127-5
-   Enable CONFIG_TCP_CONG_BBR
*   Wed Jul 29 2020 Alexey Makhalov <amakhalov@vmware.com> 4.19.127-4
-   .config: add zram module
*   Mon Jul 27 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.127-3
-   Fix CVE-2020-14331
*   Fri Jul 17 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.127-2
-   Fix aarch64 build failure due to missing i40e man pages.
*   Tue Jun 23 2020 Keerthana K <keerthanak@vmware.com> 4.19.127-1
-   Update to version 4.19.127
*   Tue Jun 16 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.112-14
-   Add latest out of tree version of i40e driver
*   Wed Jun 10 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.112-13
-   Enable CONFIG_VFIO_NOIOMMU
*   Tue Jun 09 2020 Alexey Makhalov <amakhalov@vmware.com> 4.19.112-12
-   Add intel_sgx module (-drivers-intel-sgx subpackage)
*   Fri Jun 05 2020 Ankit Jain <ankitja@vmware.com> 4.19.112-11
-   Enabled CONFIG_BINFMT_MISC
*   Tue Jun 02 2020 Vikash Bansal <bvikas@vmware.com> 4.19.112-10
-   Add patch to fix CVE-2019-18885
*   Mon Jun 1 2020 Shreenidhi Shedi <sshedi@vmware.com> 4.19.112-9
-   Keep modules of running kernel till next boot
*   Sat May 30 2020 Alexey Makhalov <amakhalov@vmware.com> 4.19.112-8
-   .config: add gs_usb module
*   Wed May 20 2020 Tapas Kundu <tkundu@vmware.com> 4.19.112-7
-   Added linux-python3-perf subpackage.
-   Added turbostat and cpupower to tools for x86_64.
-   linux-python3-perf replaces python3-perf.
*   Fri May 15 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.112-6
-   Add uio_pic_generic driver support in config
*   Wed May 06 2020 Siddharth Chandrasekaran <csiddharth@vmware.com> 4.19.112-5
-   Add patch to fix CVE-2020-10711
*   Wed Apr 29 2020 Keerthana K <keerthanak@vmware.com> 4.19.112-4
-   Photon-checksum-generator version update to 1.1.
*   Wed Apr 29 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.112-3
-   Enable additional config options.
*   Wed Apr 15 2020 Vikash Bansal <bvikas@vmware.com> 4.19.112-2
-   HMAC-SHA256 digest of hmac_generator module moved to hmacgen package
*   Wed Apr 08 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.112-1
-   Update to version 4.19.112
*   Tue Mar 31 2020 Vikash Bansal <bvikas@vmware.com> 4.19.104-2
-   hmac generation of crypto modules and initrd generation changes if fips=1
*   Wed Mar 25 2020 Vikash Bansal <bvikas@vmware.com> 4.19.104-1
-   Update to version 4.19.104
*   Mon Mar 23 2020 Alexey Makhalov <amakhalov@vmware.com> 4.19.97-8
-   Fix perf compilation issue with binutils >= 2.34.
*   Mon Mar 16 2020 Keerthana K <keerthanak@vmware.com> 4.19.97-7
-   Adding Enhances depedency to hmacgen.
*   Wed Mar 04 2020 Vikash Bansal <bvikas@vmware.com> 4.19.97-6
-   Backporting of patch continuous testing of RNG from urandom
*   Tue Feb 25 2020 Ajay Kaher <akaher@vmware.com> 4.19.97-5
-   Fix CVE-2019-16234
*   Tue Feb 11 2020 Keerthana K <keerthanak@vmware.com> 4.19.97-4
-   Add photon-checksum-generator source tarball and remove hmacgen patch.
-   Exclude hmacgen.ko from base package.
*   Fri Jan 31 2020 Ajay Kaher <akaher@vmware.com> 4.19.97-3
-   Move snd-bcm2835.ko to linux-drivers-sound rpm
*   Wed Jan 29 2020 Keerthana K <keerthanak@vmware.com> 4.19.97-2
-   Update tcrypt to test drbg_pr_sha256 and drbg_nopr_sha256.
-   Update testmgr to add drbg_pr_ctr_aes256 test vectors.
*   Fri Jan 17 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.97-1
-   Update to version 4.19.97
*   Thu Jan 16 2020 Srinidhi Rao <srinidhir@vmware.com> 4.19.87-6
-   Enable DRBG HASH and DRBG CTR support.
*   Wed Jan 08 2020 Ajay Kaher <akaher@vmware.com> 4.19.87-5
-   Enabled configs RTC_DRV_PL030, RTC_DRV_PL031
*   Fri Jan 03 2020 Keerthana K <keerthanak@vmware.com> 4.19.87-4
-   Modify tcrypt to remove tests for algorithms that are not supported in photon.
-   Added tests for DH, DRBG algorithms.
*   Thu Jan 02 2020 Keerthana K <keerthanak@vmware.com> 4.19.87-3
-   Update fips Kat tests patch.
*   Mon Dec 09 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.87-2
-   Cross compilation support
*   Fri Dec 06 2019 Ajay Kaher <akaher@vmware.com> 4.19.87-1
-   Update to version 4.19.87
*   Tue Dec 03 2019 Keerthana K <keerthanak@vmware.com> 4.19.84-4
-   Adding hmac sha256/sha512 generator kernel module for fips.
*   Tue Nov 26 2019 Ajay Kaher <akaher@vmware.com> 4.19.84-3
-   Fix CVE-2019-19062, CVE-2019-19066, CVE-2019-19072,
-   CVE-2019-19073, CVE-2019-19074, CVE-2019-19078
*   Mon Nov 18 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.84-2
-   .config: infiniband support.
*   Tue Nov 12 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.84-1
-   Update to version 4.19.84
-   Fix CVE-2019-18814
*   Fri Nov 08 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.82-1
-   Update to version 4.19.82
*   Thu Nov 07 2019 Jorgen Hansen (VMware) <jhansen@vmware.com> 4.19.79-3
-   Fix vsock QP detach with outgoing data
*   Thu Oct 24 2019 Ajay Kaher <akaher@vmware.com> 4.19.79-2
-   Enabled WiFi and BT config for Dell 5K.
*   Tue Oct 15 2019 Ajay Kaher <akaher@vmware.com> 4.19.79-1
-   Update to version 4.19.79
-   Fix CVE-2019-17133
*   Mon Oct 14 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.76-5
-   Add megaraid_sas driver to initramfs
*   Mon Oct 14 2019 Bo Gan <ganb@vmware.com> 4.19.76-4
-   Enable IMA with SHA256 as default hash algorithm
*   Thu Oct 10 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.76-3
-   Add additional BuildRequires and Requires to fix issues with perf, related to
-   interactive UI and C++ symbol demangling. Also update the last few perf python
-   scripts in Linux kernel to use python3 syntax.
*   Thu Oct 10 2019 Harinadh D <hdommaraju@vmware.com> 4.19.76-2
-   Adding lvm and dm-mod modules to support root as lvm
*   Wed Oct 02 2019 Ajay Kaher <akaher@vmware.com> 4.19.76-1
-   Update to version 4.19.76
-   Enable USB_SERIAL_PL2303 for aarch64
*   Mon Sep 30 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.72-1
-   Update to version 4.19.72
*   Thu Sep 05 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.69-3
-   Avoid oldconfig which leads to potential build hang
-   Fix archdir usage
*   Thu Sep 05 2019 Ajay Kaher <akaher@vmware.com> 4.19.69-2
-   Adding SPI and Audio interfaces in rpi3 device tree
-   Adding spi0 and audio overlays
-   Copying rpi dt in /boot/broadcom as u-boot picks from here
*   Fri Aug 30 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.69-1
-   Update to version 4.19.69
*   Fri Aug 23 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.65-4
-   NXP ls1046a frwy board support.
-   config_aarch64: add fsl_dpaa2 support.
-   fix fsl_dpaa_mac initialization issue.
*   Wed Aug 14 2019 Raejoon Jung <rjung@vmware.com> 4.19.65-3
-   Backport of Secure Boot UEFI certificate import from v5.2
*   Mon Aug 12 2019 Ajay Kaher <akaher@vmware.com> 4.19.65-2
-   Fix config_aarch64 for v4.19.65
*   Tue Aug 06 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.65-1
-   Update to version 4.19.65
-   Fix CVE-2019-1125 (SWAPGS)
*   Tue Jul 30 2019 Ajay Kaher <akaher@vmware.com> 4.19.52-7
-   Added of_configfs patches to dynamic load Overlays.
*   Thu Jul 25 2019 Keerthana K <keerthanak@vmware.com> 4.19.52-6
-   Fix postun scriplet.
*   Thu Jul 11 2019 Keerthana K <keerthanak@vmware.com> 4.19.52-5
-   Enable kernel configs necessary for BPF Compiler Collection (BCC).
*   Wed Jul 10 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.52-4
-   Deprecate linux-aws-tools in favor of linux-tools.
*   Tue Jul 02 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.52-3
-   Fix 9p vsock 16bit port issue.
*   Thu Jun 20 2019 Tapas Kundu <tkundu@vmware.com> 4.19.52-2
-   Enabled CONFIG_I2C_CHARDEV to support lm-sensors
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
*   Thu Apr 11 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.32-3
-   Update config_aarch64 to fix ARM64 build.
*   Fri Mar 29 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.32-2
-   Fix CVE-2019-10125
*   Wed Mar 27 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.32-1
-   Update to version 4.19.32
*   Thu Mar 14 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.29-1
-   Update to version 4.19.29
*   Tue Mar 05 2019 Ajay Kaher <akaher@vmware.com> 4.19.26-1
-   Update to version 4.19.26
*   Thu Feb 21 2019 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.15-3
-   Fix CVE-2019-8912
*   Thu Jan 24 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.15-2
-   Add WiFi (ath10k), sensors (i2c,spi), usb support for NXP LS1012A board.
*   Tue Jan 15 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.15-1
-   Update to version 4.19.15
*   Fri Jan 11 2019 Srinidhi Rao <srinidhir@vmware.com> 4.19.6-7
-   Add Network support for NXP LS1012A board.
*   Wed Jan 09 2019 Ankit Jain <ankitja@vmware.com> 4.19.6-6
-   Enable following for x86_64 and aarch64:
-    Enable Kernel Address Space Layout Randomization.
-    Enable CONFIG_SECURITY_NETWORK_XFRM
*   Fri Jan 04 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.6-5
-   Enable AppArmor by default.
*   Wed Jan 02 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.6-4
-   .config: added Compulab fitlet2 device drivers
-   .config_aarch64: added gpio sysfs support
-   renamed -sound to -drivers-sound
*   Tue Jan 01 2019 Ajay Kaher <akaher@vmware.com> 4.19.6-3
-   .config: Enable CONFIG_PCI_HYPERV driver
*   Wed Dec 19 2018 Srinidhi Rao <srinidhir@vmware.com> 4.19.6-2
-   Add NXP LS1012A support.
*   Mon Dec 10 2018 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.6-1
-   Update to version 4.19.6
*   Fri Dec 07 2018 Alexey Makhalov <amakhalov@vmware.com> 4.19.1-3
-   .config: added qmi wwan module
*   Mon Nov 12 2018 Ajay Kaher <akaher@vmware.com> 4.19.1-2
-   Fix config_aarch64 for 4.19.1
*   Mon Nov 05 2018 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.1-1
-   Update to version 4.19.1
*   Tue Oct 16 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.18.9-5
-   Change in config to enable drivers for zigbee and GPS
*   Fri Oct 12 2018 Ajay Kaher <akaher@vmware.com> 4.18.9-4
-   Enable LAN78xx for aarch64 rpi3
*   Fri Oct 5 2018 Ajay Kaher <akaher@vmware.com> 4.18.9-3
-   Fix config_aarch64 for 4.18.9
-   Add module.lds for aarch64
*   Wed Oct 03 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.18.9-2
-   Use updated steal time accounting patch.
-   .config: Enable CONFIG_CPU_ISOLATION and a few networking options
-   that got accidentally dropped in the last update.
*   Mon Oct 1 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.18.9-1
-   Update to version 4.18.9
*   Tue Sep 25 2018 Ajay Kaher <akaher@vmware.com> 4.14.67-2
-   Build hang (at make oldconfig) fix in config_aarch64
*   Wed Sep 19 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.14.67-1
-   Update to version 4.14.67
*   Tue Sep 18 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.14.54-7
-   Add rdrand-based RNG driver to enhance kernel entropy.
*   Sun Sep 02 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.14.54-6
-   Add full retpoline support by building with retpoline-enabled gcc.
*   Thu Aug 30 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.14.54-5
-   Apply out-of-tree patches needed for AppArmor.
*   Wed Aug 22 2018 Alexey Makhalov <amakhalov@vmware.com> 4.14.54-4
-   Fix overflow kernel panic in rsi driver.
-   .config: enable BT stack, enable GPIO sysfs.
-   Add Exar USB serial driver.
*   Fri Aug 17 2018 Ajay Kaher <akaher@vmware.com> 4.14.54-3
-   Enabled USB PCI in config_aarch64
-   Build hang (at make oldconfig) fix in config_aarch64
*   Thu Jul 19 2018 Alexey Makhalov <amakhalov@vmware.com> 4.14.54-2
-   .config: usb_serial_pl2303=m,wlan=y,can=m,gpio=y,pinctrl=y,iio=m
*   Mon Jul 09 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.14.54-1
-   Update to version 4.14.54
*   Fri Jan 26 2018 Alexey Makhalov <amakhalov@vmware.com> 4.14.8-2
-   Added vchiq entry to rpi3 dts
-   Added dtb-rpi3 subpackage
*   Fri Dec 22 2017 Alexey Makhalov <amakhalov@vmware.com> 4.14.8-1
-   Version update
*   Wed Dec 13 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.66-4
-   KAT build support
*   Thu Dec 07 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.66-3
-   Aarch64 support
*   Tue Dec 05 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.66-2
-   Sign and compress modules after stripping. fips=1 requires signed modules
*   Mon Dec 04 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.66-1
-   Version update
*   Tue Nov 21 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.64-1
-   Version update
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
*   Mon Jul 03 2017 Xiaolin Li <xiaolinl@vmware.com> 4.9.34-3
-   Add libdnet-devel, kmod-devel and libmspack-devel to BuildRequires
*   Thu Jun 29 2017 Divya Thaluru <dthaluru@vmware.com> 4.9.34-2
-   Added obsolete for deprecated linux-dev package
*   Wed Jun 28 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.34-1
-   [feature] 9P FS security support
-   [feature] DM Delay target support
-   Fix CVE-2017-1000364 ("stack clash") and CVE-2017-9605
*   Thu Jun 8 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.31-1
-   Fix CVE-2017-8890, CVE-2017-9074, CVE-2017-9075, CVE-2017-9076
    CVE-2017-9077 and CVE-2017-9242
-   [feature] IPV6 netfilter NAT table support
*   Fri May 26 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.30-1
-   Added ENA driver for AMI
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
-   Fix audit-devel BuildRequires.
-   .config: build nvme and nvme-core in kernel.
*   Mon Mar 6 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.13-2
-   .config: NSX requirements for crypto and netfilter
*   Tue Feb 28 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.13-1
-   Update to linux-4.9.13 to fix CVE-2017-5986 and CVE-2017-6074
*   Thu Feb 09 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.9-1
-   Update to linux-4.9.9 to fix CVE-2016-10153, CVE-2017-5546,
    CVE-2017-5547, CVE-2017-5548 and CVE-2017-5576.
-   .config: added CRYPTO_FIPS support.
*   Tue Jan 10 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.2-1
-   Update to linux-4.9.2 to fix CVE-2016-10088
-   Move linux-tools.spec to linux.spec as -tools subpackage
*   Mon Dec 19 2016 Xiaolin Li <xiaolinl@vmware.com> 4.9.0-2
-   BuildRequires Linux-PAM-devel
*   Mon Dec 12 2016 Alexey Makhalov <amakhalov@vmware.com> 4.9.0-1
-   Update to linux-4.9.0
-   Add paravirt stolen time accounting feature (from linux-esx),
    but disable it by default (no-vmw-sta cmdline parameter)
*   Thu Dec  8 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.35-3
-   net-packet-fix-race-condition-in-packet_set_ring.patch
    to fix CVE-2016-8655
*   Wed Nov 30 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.35-2
-   Expand `uname -r` with release number
-   Check for build-id matching
-   Added syscalls tracing support
-   Compress modules
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
-   .config: add cgrup_hugetlb support
-   .config: add netfilter_xt_{set,target_ct} support
-   .config: add netfilter_xt_match_{cgroup,ipvs} support
*   Thu Nov 10 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.31-1
-   Update to linux-4.4.31
*   Fri Oct 21 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.26-1
-   Update to linux-4.4.26
*   Wed Oct 19 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.20-6
-   net-add-recursion-limit-to-GRO.patch
-   scsi-arcmsr-buffer-overflow-in-arcmsr_iop_message_xfer.patch
*   Tue Oct 18 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.20-5
-   ipip-properly-mark-ipip-GRO-packets-as-encapsulated.patch
-   tunnels-dont-apply-GRO-to-multiple-layers-of-encapsulation.patch
*   Mon Oct  3 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.20-4
-   Package vmlinux with PROGBITS sections in -debuginfo subpackage
*   Tue Sep 27 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.20-3
-   .config: CONFIG_IP_SET_HASH_{IPMARK,MAC}=m
*   Tue Sep 20 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.20-2
-   Add -release number for /boot/* files
-   Use initrd.img with version and release number
-   Rename -dev subpackage to -devel
*   Wed Sep  7 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.20-1
-   Update to linux-4.4.20
-   apparmor-fix-oops-validate-buffer-size-in-apparmor_setprocattr.patch
-   keys-fix-asn.1-indefinite-length-object-parsing.patch
*   Thu Aug 25 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-11
-   vmxnet3 patches to bumpup a version to 1.4.8.0
*   Wed Aug 10 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-10
-   Added VSOCK-Detach-QP-check-should-filter-out-non-matching-QPs.patch
-   .config: pmem hotplug + ACPI NFIT support
-   .config: enable EXPERT mode, disable UID16 syscalls
*   Thu Jul 07 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-9
-   .config: pmem + fs_dax support
*   Fri Jun 17 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-8
-   patch: e1000e-prevent-div-by-zero-if-TIMINCA-is-zero.patch
-   .config: disable rt group scheduling - not supported by systemd
*   Wed Jun 15 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.4.8-7
-   fixed the capitalization for - System.map
*   Thu May 26 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-6
-   patch: REVERT-sched-fair-Beef-up-wake_wide.patch
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.4.8-5
-   GA - Bump release of all rpms
*   Mon May 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.4.8-4
-   Fixed generation of debug symbols for kernel modules & vmlinux.
*   Mon May 23 2016 Divya Thaluru <dthaluru@vmware.com> 4.4.8-3
-   Added patches to fix CVE-2016-3134, CVE-2016-3135
*   Wed May 18 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.4.8-2
-   Enabled CONFIG_UPROBES in config as needed by ktap
*   Wed May 04 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-1
-   Update to linux-4.4.8
-   Added net-Drivers-Vmxnet3-set-... patch
*   Tue May 03 2016 Vinay Kulkarni <kulkarniv@vmware.com> 4.2.0-27
-   Compile Intel GigE and VMXNET3 as part of kernel.
*   Thu Apr 28 2016 Nick Shi <nshi@vmware.com> 4.2.0-26
-   Compile cramfs.ko to allow mounting cramfs image
*   Tue Apr 12 2016 Vinay Kulkarni <kulkarniv@vmware.com> 4.2.0-25
-   Revert network interface renaming disable in kernel.
*   Tue Mar 29 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-24
-   Support kmsg dumping to vmware.log on panic
-   sunrpc: xs_bind uses ip_local_reserved_ports
*   Mon Mar 28 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.2.0-23
-   Enabled Regular stack protection in Linux kernel in config
*   Thu Mar 17 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.2.0-22
-   Restrict the permissions of the /boot/System.map-X file
*   Fri Mar 04 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-21
-   Patch: SUNRPC: Do not reuse srcport for TIME_WAIT socket.
*   Wed Mar 02 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-20
-   Patch: SUNRPC: Ensure that we wait for connections to complete
    before retrying
*   Fri Feb 26 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-19
-   Disable watchdog under VMware hypervisor.
*   Thu Feb 25 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-18
-   Added rpcsec_gss_krb5 and nfs_fscache
*   Mon Feb 22 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-17
-   Added sysctl param to control weighted_cpuload() behavior
*   Thu Feb 18 2016 Divya Thaluru <dthaluru@vmware.com> 4.2.0-16
-   Disabling network renaming
*   Sun Feb 14 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-15
-   veth patch: don’t modify ip_summed
*   Thu Feb 11 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-14
-   Full tickless -> idle tickless + simple CPU time accounting
-   SLUB -> SLAB
-   Disable NUMA balancing
-   Disable stack protector
-   No build_forced no-CBs CPUs
-   Disable Expert configuration mode
-   Disable most of debug features from 'Kernel hacking'
*   Mon Feb 08 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-13
-   Double tcp_mem limits, patch is added.
*   Wed Feb 03 2016 Anish Swaminathan <anishs@vmware.com>  4.2.0-12
-   Fixes for CVE-2015-7990/6937 and CVE-2015-8660.
*   Tue Jan 26 2016 Anish Swaminathan <anishs@vmware.com> 4.2.0-11
-   Revert CONFIG_HZ=250
*   Fri Jan 22 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-10
-   Fix for CVE-2016-0728
*   Wed Jan 13 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-9
-   CONFIG_HZ=250
*   Tue Jan 12 2016 Mahmoud Bassiouny <mbassiouny@vmware.com> 4.2.0-8
-   Remove rootfstype from the kernel parameter.
*   Mon Jan 04 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.2.0-7
-   Disabled all the tracing options in kernel config.
-   Disabled preempt.
-   Disabled sched autogroup.
*   Thu Dec 17 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.2.0-6
-   Enabled kprobe for systemtap & disabled dynamic function tracing in config
*   Fri Dec 11 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.2.0-5
-   Added oprofile kernel driver sub-package.
*   Fri Nov 13 2015 Mahmoud Bassiouny <mbassiouny@vmware.com> 4.2.0-4
-   Change the linux image directory.
*   Wed Nov 11 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.2.0-3
-   Added the build essential files in the dev sub-package.
*   Mon Nov 09 2015 Vinay Kulkarni <kulkarniv@vmware.com> 4.2.0-2
-   Enable Geneve module support for generic kernel.
*   Fri Oct 23 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.2.0-1
-   Upgraded the generic linux kernel to version 4.2.0 & and updated timer handling to full tickless mode.
*   Tue Sep 22 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.0.9-5
-   Added driver support for frame buffer devices and ACPI
*   Wed Sep 2 2015 Alexey Makhalov <amakhalov@vmware.com> 4.0.9-4
-   Added mouse ps/2 module.
*   Fri Aug 14 2015 Alexey Makhalov <amakhalov@vmware.com> 4.0.9-3
-   Use photon.cfg as a symlink.
*   Thu Aug 13 2015 Alexey Makhalov <amakhalov@vmware.com> 4.0.9-2
-   Added environment file(photon.cfg) for grub.
*   Wed Aug 12 2015 Sharath George <sharathg@vmware.com> 4.0.9-1
-   Upgrading kernel version.
*   Wed Aug 12 2015 Alexey Makhalov <amakhalov@vmware.com> 3.19.2-5
-   Updated OVT to version 10.0.0.
-   Rename -gpu-drivers to -drivers-gpu in accordance to directory structure.
-   Added -sound package/
*   Tue Aug 11 2015 Anish Swaminathan<anishs@vmware.com> 3.19.2-4
-   Removed Requires dependencies.
*   Fri Jul 24 2015 Harish Udaiya Kumar <hudaiyakumar@gmail.com> 3.19.2-3
-   Updated the config file to include graphics drivers.
*   Mon May 18 2015 Touseef Liaqat <tliaqat@vmware.com> 3.13.3-2
-   Update according to UsrMove.
*   Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 3.13.3-1
-   Initial build. First version

