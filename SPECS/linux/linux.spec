%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%global security_hardening none
%ifarch x86_64
%define arch x86_64
%define archdir x86

# Set this flag to 0 to build without canister
%global fips 1

# If kat_build is enabled, canister is not used.
%if 0%{?kat_build:1}
%global fips 0
%endif

%endif

%ifarch aarch64
%define arch arm64
%define archdir arm64
%endif

Summary:        Kernel
Name:           linux
Version:        5.10.61
Release:        3%{?kat_build:.kat}%{?dist}
License:    	GPLv2
URL:        	http://www.kernel.org/
Group:        	System Environment/Kernel
Vendor:         VMware, Inc.
Distribution: 	Photon

%define uname_r %{version}-%{release}

Source0:        http://www.kernel.org/pub/linux/kernel/v5.x/linux-%{version}.tar.xz
%define sha1 linux=7bf2b48bccb0a7fce7a2cfaf801929b3e81f8709
Source1:	config_%{_arch}
Source2:	initramfs.trigger
%define ena_version 2.4.0
Source3:	https://github.com/amzn/amzn-drivers/archive/ena_linux_%{ena_version}.tar.gz
%define sha1 ena_linux=054d4c724b037ff8d722cd3bc04e92bb159d7824
%define sgx_version 1.8
Source5:	https://github.com/intel/SGXDataCenterAttestationPrimitives/archive/DCAP_%{sgx_version}.tar.gz
%define sha1 DCAP=6161846c2ba03099a2307f28a91e9d45627614d7
Source6:        pre-preun-postun-tasks.inc
Source7:        check_for_config_applicability.inc
%define i40e_version 2.15.9
Source10:       https://sourceforge.net/projects/e1000/files/i40e%20stable/%{i40e_version}/i40e-%{i40e_version}.tar.gz
%define sha1 i40e=ec8b4794cea15bb3162a74ef3bfe35f2fd08a036
%define iavf_version 4.2.7
Source11:       https://sourceforge.net/projects/e1000/files/iavf%20stable/%{iavf_version}/iavf-%{iavf_version}.tar.gz
%define sha1 iavf=5b0f144a60bdfcc5928f78691dc42cb85c2ed734
Source12:       ena-Use-new-API-interface-after-napi_hash_del-.patch
%define ice_version 1.6.4
Source13:       https://sourceforge.net/projects/e1000/files/ice%20stable/%{ice_version}/ice-%{ice_version}.tar.gz
%define sha1 ice=9e860bf3cafcabd1d4897e87e749334f73828bad
%if 0%{?fips}
Source9:        check_fips_canister_struct_compatibility.inc
%define fips_canister_version 4.0.1-5.10.21-3-secure
Source16:       fips-canister-%{fips_canister_version}.tar.bz2
%define sha1 fips-canister=e793f09579cf7b17608095ed80c973000f5f8407
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
# floppy:
Patch17:        0001-floppy-lower-printk-message-priority.patch

#vmxnet3
Patch20:        0001-vmxnet3-Remove-buf_info-from-device-accessible-struc.patch

# VMW:
Patch55:        x86-vmware-Use-Efficient-and-Correct-ALTERNATIVEs-fo-510.patch
Patch56:        x86-vmware-Log-kmsg-dump-on-panic-510.patch
Patch57:        x86-vmware-Fix-steal-time-clock-under-SEV.patch

# CVE:
Patch100:       apparmor-fix-use-after-free-in-sk_peer_label.patch
# Fix CVE-2017-1000252
Patch101:       KVM-Don-t-accept-obviously-wrong-gsi-values-via-KVM_.patch
# Fix for CVE-2019-12379
Patch102:       consolemap-Fix-a-memory-leaking-bug-in-drivers-tty-v.patch

%ifarch aarch64
# Rpi of_configfs patches
Patch201:        0001-OF-DT-Overlay-configfs-interface.patch
Patch202:        0002-of-configfs-Use-of_overlay_fdt_apply-API-call.patch
Patch203:        0003-of-overlay-Correct-symbol-path-fixups.patch

# Rpi fan driver
Patch204:        0001-Add-rpi-poe-fan-driver.patch
%endif

# Crypto:
# Patch to add drbg_pr_ctr_aes256 test vectors to testmgr
Patch500:       crypto-testmgr-Add-drbg_pr_ctr_aes256-test-vectors.patch
# Patch to call drbg and dh crypto tests from tcrypt
Patch501:       tcrypt-disable-tests-that-are-not-enabled-in-photon.patch
Patch502:       0001-Initialize-jitterentropy-before-ecdh.patch
Patch503:       0002-FIPS-crypto-self-tests.patch
# Patch to remove urandom usage in rng module
Patch504:       0001-FIPS-crypto-rng-Jitterentropy-RNG-as-the-only-RND-source.patch
# Patch to remove urandom usage in drbg and ecc modules
Patch505:       0003-FIPS-crypto-drbg-Jitterentropy-RNG-as-the-only-RND.patch
#Patch to not make shash_no_setkey static
Patch506:       0001-fips-Continue-to-export-shash_no_setkey.patch
%if 0%{?fips}
# FIPS canister usage patch
Patch508:       0001-FIPS-canister-binary-usage.patch
# Patch to remove urandom usage in rng module
Patch509:       0001-FIPS-crypto-rng-Jitterentropy-RNG-as-the-only-RND-source.patch
%else
%if 0%{?kat_build:1}
Patch510:       0003-FIPS-broken-kattest.patch
%endif
%endif

# SEV on VMware:
Patch600:       0079-x86-sev-es-Disable-BIOS-ACPI-RSDP-probing-if-SEV-ES-.patch
Patch601:       0080-x86-boot-Enable-vmw-serial-port-via-Super-I-O.patch
Patch602:       0081-x86-sev-es-Disable-use-of-WP-via-PAT-for-__sme_early.patch
Patch603:       x86-sev-es-load-idt-before-entering-long-mode-to-han-510.patch
Patch604:       x86-swiotlb-Adjust-SWIOTLB-bounce-buffer-size-for-SE.patch
Patch605:       x86-sev-es-Do-not-unroll-string-IO-for-SEV-ES-guests.patch

#Patches for i40e driver
Patch1500:      i40e-xdp-remove-XDP_QUERY_PROG-and-XDP_QUERY_PROG_HW-XDP-.patch
Patch1501:      0001-Add-support-for-gettimex64-interface.patch

#Patches for ice driver
Patch1510:      0001-ice-Use-PTP_SYS_OFFSET_EXTENDED_IOCTL-support.patch

#Patches for iavf driver
Patch1511:      0001-iavf-Use-PTP_SYS_OFFSET_EXTENDED_IOCTL-support.patch

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
%if 0%{?fips}
BuildRequires:  gdb
%endif
Requires:       filesystem kmod
Requires(pre): (coreutils or toybox)
Requires(preun): (coreutils or toybox)
Requires(post): (coreutils or toybox)
Requires(postun): (coreutils or toybox)

%description
The Linux package contains the Linux kernel.
%if 0%{?fips}
This kernel is FIPS certified.
%endif

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
Requires:       audit elfutils-libelf binutils-libs xz-libs libunwind slang python3 traceevent-plugins
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

%prep
#TODO: remove rcN after 5.9 goes out of rc
# Using autosetup is not feasible
%setup -q -n linux-%{version}
%ifarch x86_64
# Using autosetup is not feasible
%setup -D -b 3 -n linux-%{version}
# Using autosetup is not feasible
%setup -D -b 5 -n linux-%{version}
# Using autosetup is not feasible
%setup -D -b 10 -n linux-%{version}
# Using autosetup is not feasible
%setup -D -b 11 -n linux-%{version}
# Using autosetup is not feasible
%setup -D -b 13 -n linux-%{version}
%endif

%if 0%{?fips}
# Using autosetup is not feasible
%setup -D -b 16 -n linux-%{version}
%endif

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
%patch17 -p1

#vmxnet3
%patch20 -p1

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

%ifarch aarch64
# Rpi of_configfs patches
%patch201 -p1
%patch202 -p1
%patch203 -p1
#Rpi fan driver
%patch204 -p1
%endif

# crypto
%patch500 -p1
%patch501 -p1
%patch502 -p1
%patch503 -p1
%patch504 -p1
%patch505 -p1
%patch506 -p1
%if 0%{?fips}
%patch508 -p1
%patch509 -p1
%else
%if 0%{?kat_build:1}
%patch510 -p1
%endif
%endif

%ifarch x86_64
# SEV on VMware
%patch600 -p1
%patch601 -p1
%patch602 -p1
%patch603 -p1
%patch604 -p1
%patch605 -p1

#Patches for i40e driver
pushd ../i40e-%{i40e_version}
%patch1500 -p1
%patch1501 -p1
popd

#Patches for ice driver
pushd ../ice-%{ice_version}
%patch1510 -p1
popd

#Patches for iavf river
pushd ../iavf-%{iavf_version}
%patch1511 -p1
popd
%endif

%build
make %{?_smp_mflags} mrproper
cp %{SOURCE1} .config
%if 0%{?fips}
cp ../fips-canister-%{fips_canister_version}/fips_canister.o crypto/
cp ../fips-canister-%{fips_canister_version}/fips_canister_wrapper.c crypto/
%endif

sed -i 's/CONFIG_LOCALVERSION=""/CONFIG_LOCALVERSION="-%{release}"/' .config

%include %{SOURCE7}

# Set/add CONFIG_CROSS_COMPILE= if needed
if [ %{_host} != %{_build} ]; then
grep -q CONFIG_CROSS_COMPILE= .config && sed -i '/^CONFIG_CROSS_COMPILE=/c\CONFIG_CROSS_COMPILE="%{_host}-"' .config || \
	echo 'CONFIG_CROSS_COMPILE="%{_host}-"' >> .config
fi

make %{?_smp_mflags} V=1 KBUILD_BUILD_VERSION="1-photon" KBUILD_BUILD_HOST="photon" ARCH=%{arch} %{?_smp_mflags}

%if 0%{?fips}
%include %{SOURCE9}
%endif

%ifarch aarch64
ARCH_FLAGS="EXTRA_CFLAGS=-Wno-error=format-overflow"
%endif
make %{?_smp_mflags} ARCH=%{arch} -C tools perf PYTHON=python3 $ARCH_FLAGS

%ifarch x86_64
#build turbostat and cpupower
make %{?_smp_mflags} ARCH=%{arch} -C tools turbostat cpupower PYTHON=python3

# build ENA module
bldroot=`pwd`
pushd ../amzn-drivers-ena_linux_%{ena_version}/kernel/linux/ena
patch -p4 < %{SOURCE12}
make %{?_smp_mflags} -C $bldroot M=`pwd` V=1 modules %{?_smp_mflags}
popd

# build Intel SGX module
bldroot=`pwd`
pushd ../SGXDataCenterAttestationPrimitives-DCAP_%{sgx_version}/driver/linux
make %{?_smp_mflags} KDIR=$bldroot ARCH=%{arch} %{?_smp_mflags}
popd

# build i40e module
bldroot=`pwd`
pushd ../i40e-%{i40e_version}
make %{?_smp_mflags} -C src KSRC=$bldroot clean
make %{?_smp_mflags} -C src KSRC=$bldroot %{?_smp_mflags}
popd

# build iavf module
bldroot=`pwd`
pushd ../iavf-%{iavf_version}
make %{?_smp_mflags} -C src KSRC=$bldroot clean
make %{?_smp_mflags} -C src KSRC=$bldroot %{?_smp_mflags}
popd

# build ice module
bldroot=`pwd`
pushd ../ice-%{ice_version}
make %{?_smp_mflags} -C src KSRC=$bldroot clean
make %{?_smp_mflags} -C src KSRC=$bldroot %{?_smp_mflags}
popd
%endif

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
make %{?_smp_mflags} ARCH=%{arch} INSTALL_MOD_PATH=%{buildroot} modules_install

%ifarch x86_64
# install ENA module
bldroot=`pwd`
pushd ../amzn-drivers-ena_linux_%{ena_version}/kernel/linux/ena
make %{?_smp_mflags} -C $bldroot M=`pwd` INSTALL_MOD_PATH=%{buildroot} modules_install
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
make %{?_smp_mflags} -C src KSRC=$bldroot INSTALL_MOD_PATH=%{buildroot} INSTALL_MOD_DIR=extra MANDIR=%{_mandir} modules_install mandocs_install
popd

# install iavf module
bldroot=`pwd`
pushd ../iavf-%{iavf_version}
make %{?_smp_mflags} -C src KSRC=$bldroot INSTALL_MOD_PATH=%{buildroot} INSTALL_MOD_DIR=extra MANDIR=%{_mandir} modules_install mandocs_install
popd

# install ice module
bldroot=`pwd`
pushd ../ice-%{ice_version}
make %{?_smp_mflags} -C src KSRC=$bldroot INSTALL_MOD_PATH=%{buildroot} INSTALL_MOD_DIR=extra MANDIR=%{_mandir} modules_install mandocs_install
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
photon_cmdline=init=/lib/systemd/systemd ro loglevel=3 quiet
photon_linux=vmlinuz-%{uname_r}
photon_initrd=initrd.img-%{uname_r}
EOF

# Register myself to initramfs
mkdir -p %{buildroot}/%{_localstatedir}/lib/initramfs/kernel
cat > %{buildroot}/%{_localstatedir}/lib/initramfs/kernel/%{uname_r} << "EOF"

%ifarch x86_64
--add-drivers "tmem xen-scsifront xen-blkfront xen-acpi-processor xen-evtchn xen-gntalloc xen-gntdev xen-privcmd xen-pciback xenfs hv_utils hv_vmbus hv_storvsc hv_netvsc hv_sock hv_balloon cn lvm dm-mod megaraid_sas"
%endif

%ifarch aarch64
--add-drivers "tmem xen-scsifront xen-blkfront xen-acpi-processor xen-evtchn xen-gntalloc xen-gntdev xen-privcmd xen-pciback xenfs hv_utils hv_vmbus hv_storvsc hv_netvsc hv_sock hv_balloon cn lvm dm-mod megaraid_sas nvme nvme-core"
%endif

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
ARCH_FLAGS="EXTRA_CFLAGS=-Wno-error=format-overflow"
%endif
make %{?_smp_mflags} -C tools ARCH=%{arch} DESTDIR=%{buildroot} prefix=%{_prefix} perf_install PYTHON=python3 $ARCH_FLAGS
make %{?_smp_mflags} -C tools/perf ARCH=%{arch} DESTDIR=%{buildroot} prefix=%{_prefix} PYTHON=python3 install-python_ext
%ifarch x86_64
make %{?_smp_mflags} -C tools ARCH=%{arch} DESTDIR=%{buildroot} prefix=%{_prefix} mandir=%{_mandir} turbostat_install cpupower_install PYTHON=python3
%endif

%include %{SOURCE2}
%include %{SOURCE6}

%post
/sbin/depmod -a %{uname_r}
ln -sf %{name}-%{uname_r}.cfg /boot/photon.cfg

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
%config(noreplace) /boot/%{name}-%{uname_r}.cfg
%config %{_localstatedir}/lib/initramfs/kernel/%{uname_r}
%defattr(0644,root,root)
/lib/modules/%{uname_r}/*
%exclude /lib/modules/%{uname_r}/build
%exclude /lib/modules/%{uname_r}/kernel/drivers/gpu
%exclude /lib/modules/%{uname_r}/kernel/sound
%ifarch aarch64
%exclude /lib/modules/%{uname_r}/kernel/drivers/staging/vc04_services/bcm2835-audio
%endif
%ifarch x86_64
%exclude /lib/modules/%{uname_r}/kernel/arch/x86/oprofile/
%exclude /lib/modules/%{uname_r}/extra/intel_sgx.ko.xz
/etc/modprobe.d/iavf.conf
# ICE driver firmware files are packaged in linux-firmware
%exclude /lib/firmware/updates/intel/ice
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
%exclude /usr/lib64/traceevent
%endif
%ifarch aarch64
%exclude /usr/lib/traceevent
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
*   Thu Oct 07 2021 Srinidhi Rao <srinidhir@vmware.com> 5.10.61-3
-   Use jitterentropy rng instead of urandom in rng module.
*   Thu Sep 09 2021 Alexey Makhalov <amakhalov@vmware.com> 5.10.61-2
-   .config enable CONFIG_MOUSE_PS2_VMMOUSE and CONFIG_INPUT_UINPUT
-   Enable sta by default
*   Fri Aug 27 2021 Ankit Jain <ankitja@vmware.com> 5.10.61-1
-   Update to version 5.10.61
*   Wed Aug 18 2021 Keerthana K <keerthanak@vmware.com> 5.10.52-2
-   Update ice driver to v1.6.4
-   Update i40e driver to v2.15.9
-   Update iavf driver to v4.2.7
*   Fri Jul 23 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 5.10.52-1
-   Update to version 5.10.52
*   Thu Jul 15 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 5.10.46-2
-   Fix for CVE-2021-33909
*   Mon Jun 28 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.46-1
-   Update to version 5.10.46
*   Tue Jun 22 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.42-3
-   Fix for CVE-2021-3609
*   Thu Jun 10 2021 Keerthana K <keerthanak@vmware.com> 5.10.42-2
-   Added script to check structure compatibility between fips_canister.o and vmlinux.
*   Thu Jun 03 2021 Keerthana K <keerthanak@vmware.com> 5.10.42-1
-   Update to version 5.10.42
-   Remove XR usb driver support
-   .config: Enable CONFIG_FANOTIFY_ACCESS_PERMISSIONS
*   Wed Jun 02 2021 Keerthana K <keerthanak@vmware.com> 5.10.35-4
-   Fix for CVE-2021-3573
*   Thu May 20 2021 Ajay Kaher <akaher@vmware.com> 5.10.35-3
-   Add Rpi fan driver
*   Thu May 20 2021 Ajay Kaher <akaher@vmware.com> 5.10.35-2
-   Fix for CVE-2021-3564
*   Mon May 17 2021 Ajay Kaher <akaher@vmware.com> 5.10.35-1
-   Update to version 5.10.35
*   Thu May 13 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.25-10
-   Fix for CVE-2021-23133
*   Tue May 11 2021 Ankit Jain <ankitja@vmware.com> 5.10.25-9
-   .config: Enable MLX5_INFINIBAND
*   Tue May 11 2021 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.25-8
-   Fix CVE-2020-26147, CVE-2020-24587, CVE-2020-24586, CVE-2020-24588,
-   CVE-2020-26145, CVE-2020-26141
*   Tue May 11 2021 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.25-7
-   Fix CVE-2021-3489, CVE-2021-3490, CVE-2021-3491
*   Tue May 04 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.25-6
-   Remove buf_info from device accessible structures in vmxnet3
*   Thu Apr 29 2021 Alexey Makhalov <amakhalov@vmware.com> 5.10.25-5
-   Update canister binary.
-   use jent by drbg and ecc.
-   Enable hmac(sha224) self test and broket KAT test.
*   Thu Apr 22 2021 Keerthana K <keerthanak@vmware.com> 5.10.25-4
-   Remove hmac(sha224) test from broken kat test.
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
*   Mon Mar 01 2021 Alexey Makhalov <amakhalov@vmware.com> 5.10.4-17
-   FIPS canister update
*   Fri Feb 19 2021 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.4-16
-   Fix /boot/photon.cfg symlink when /boot is a separate partition.
*   Fri Feb 19 2021 Ajay Kaher <akaher@vmware.com> 5.10.4-15
-   Added SEV-ES improvement patches
*   Thu Feb 18 2021 Ajay Kaher <akaher@vmware.com> 5.10.4-14
-   Enable CONFIG_WDAT_WDT
*   Thu Feb 18 2021 Ajay Kaher <akaher@vmware.com> 5.10.4-13
-   lower the loglevel for floppy driver
*   Thu Feb 18 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.4-12
-   Enable CONFIG_IFB
*   Wed Feb 17 2021 Ankit Jain <ankitja@vmware.com> 5.10.4-11
-   Added latest out of tree version of Intel ice driver
*   Tue Feb 16 2021 Alexey Makhalov <amakhalov@vmware.com> 5.10.4-10
-   Fix perf compilation issue with gcc-10.2.0 for aarch64
*   Mon Feb 15 2021 Keerthana K <keerthanak@vmware.com> 5.10.4-9
-   Added crypto_self_test and kattest module.
-   These patches are applied when kat_build is enabled.
*   Wed Feb 03 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 5.10.4-8
-   Update i40e driver to v2.13.10
-   Add out of tree iavf driver
-   Enable CONFIG_NET_TEAM
*   Thu Jan 28 2021 Alexey Makhalov <amakhalov@vmware.com> 5.10.4-7
-   Use secure FIPS canister.
*   Mon Jan 25 2021 Ankit Jain <ankitja@vmware.com> 5.10.4-6
-   Enabled CONFIG_WIREGUARD
*   Fri Jan 22 2021 Keerthana K <keerthanak@vmware.com> 5.10.4-5
-   Build kernel with FIPS canister.
*   Wed Jan 20 2021 Alexey Makhalov <amakhalov@vmware.com> 5.10.4-4
-   Handle module.lds for aarch64 in the same way as for x86_64
*   Wed Jan 13 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.4-3
-   Remove traceevent/plugins from linux-tools
*   Mon Jan 11 2021 Bo Gan <ganb@vmware.com> 5.10.4-2
-   Fix aarch64 build failure
*   Mon Jan 04 2021 Bo Gan <ganb@vmware.com> 5.10.4-1
-   Update to 5.10.4
-   Drop out-of-tree SEV-ES functional patches (already upstreamed).
*   Wed Dec 09 2020 Ajay Kaher <akaher@vmware.com> 5.9.0-9
-   To dynamic load Overlays adding of_configfs patches v5.9.y.
*   Tue Dec 01 2020 Prashant S Chauhan <psinghchauha@vmware.com> 5.9.0-8
-   Added ami for arm support in linux generic, added multiple drivers
-   in aarch64 to support aws ami
*   Thu Nov 12 2020 Ajay Kaher <akaher@vmware.com> 5.9.0-7
-   .config: support for floppy disk and ch341 usb to serial
*   Wed Nov 11 2020 Tapas Kundu <tkundu@vmware.com> 5.9.0-6
-   Fix perf python script for compatibility with python 3.9
*   Tue Nov 10 2020 Keerthana K <keerthanak@vmware.com> 5.9.0-5
-   Fix CVE-2020-8694
*   Fri Nov 06 2020 Keerthana K <keerthanak@vmware.com> 5.9.0-4
-   Fix CVE-2020-25704
*   Tue Nov 03 2020 Srinidhi Rao <srinidhir@vmware.com> 5.9.0-3
-   Remove the support of fipsify and hmacgen
*   Tue Oct 27 2020 Piyush Gupta <gpiyush@vmware.com> 5.9.0-2
-   Fix aarch64 build failure due to missing CONFIG_FB_ARMLCD
*   Mon Oct 19 2020 Bo Gan <ganb@vmware.com> 5.9.0-1
-   Update to 5.9.0
*   Wed Sep 30 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.9.0-rc7.1
-   Update to version 5.9.0-rc7
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
