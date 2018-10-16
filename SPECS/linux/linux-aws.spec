%global security_hardening none
Summary:        Kernel
Name:           linux-aws
Version:        4.14.67
Release:        2%{?kat_build:.%kat_build}%{?dist}
License:    	GPLv2
URL:        	http://www.kernel.org/
Group:        	System Environment/Kernel
Vendor:         VMware, Inc.
Distribution: 	Photon
Source0:        http://www.kernel.org/pub/linux/kernel/v4.x/linux-%{version}.tar.xz
%define sha1 linux=4a6aa8d8a5190dbf1a835a5171609f02b27809e1
Source1:	config-aws
Source2:	initramfs.trigger
# common
Patch0:         linux-4.14-Log-kmsg-dump-on-panic.patch
Patch1:         double-tcp_mem-limits.patch
# TODO: disable this patch, check for regressions
#Patch2:         linux-4.9-watchdog-Disable-watchdog-on-virtual-machines.patch
Patch3:         SUNRPC-Do-not-reuse-srcport-for-TIME_WAIT-socket.patch
Patch4:         SUNRPC-xs_bind-uses-ip_local_reserved_ports.patch
Patch5:         vsock-transport-for-9p.patch
Patch6:         x86-vmware-STA-support.patch
#HyperV patches
Patch13:        0004-vmbus-Don-t-spam-the-logs-with-unknown-GUIDs.patch
# TODO: Is CONFIG_HYPERV_VSOCKETS the same?
#Patch23:        0014-hv_sock-introduce-Hyper-V-Sockets.patch
#FIPS patches - allow some algorithms
Patch24:        Allow-some-algo-tests-for-FIPS.patch
Patch26:        add-sysctl-to-disallow-unprivileged-CLONE_NEWUSER-by-default.patch
# Fix CVE-2017-1000252
Patch28:        kvm-dont-accept-wrong-gsi-values.patch
# Out-of-tree patches from AppArmor:
Patch29:        0001-apparmor-add-base-infastructure-for-socket-mediation.patch
Patch30:        0002-apparmor-af_unix-mediation.patch
Patch31:        0001-hwrng-rdrand-Add-RNG-driver-based-on-x86-rdrand-inst.patch

# Amazon AWS
Patch101: 0002-watchdog-Disable-watchdog-on-virtual-machines.patch
Patch102: 0004-bump-the-default-TTL-to-255.patch
Patch103: 0005-bump-default-tcp_wmem-from-16KB-to-20KB.patch
Patch104: 0007-nvme-update-timeout-module-parameter-type.patch
Patch105: 0009-drivers-introduce-AMAZON_DRIVER_UPDATES.patch
Patch106: 0010-drivers-amazon-add-network-device-drivers-support.patch
Patch107: 0011-drivers-amazon-introduce-AMAZON_ENA_ETHERNET.patch
Patch108: 0012-Importing-Amazon-ENA-driver-1.5.0-into-amazon-4.14.y.patch
Patch109: 0013-xen-manage-keep-track-of-the-on-going-suspend-mode.patch
Patch110: 0014-xen-manage-introduce-helper-function-to-know-the-on-.patch
Patch111: 0015-xenbus-add-freeze-thaw-restore-callbacks-support.patch
Patch112: 0016-x86-xen-Introduce-new-function-to-map-HYPERVISOR_sha.patch
Patch113: 0017-x86-xen-add-system-core-suspend-and-resume-callbacks.patch
Patch114: 0018-xen-blkfront-add-callbacks-for-PM-suspend-and-hibern.patch
Patch115: 0019-xen-netfront-add-callbacks-for-PM-suspend-and-hibern.patch
Patch116: 0020-xen-time-introduce-xen_-save-restore-_steal_clock.patch
Patch117: 0021-x86-xen-save-and-restore-steal-clock.patch
Patch118: 0022-xen-events-add-xen_shutdown_pirqs-helper-function.patch
Patch119: 0023-x86-xen-close-event-channels-for-PIRQs-in-system-cor.patch
Patch120: 0024-PM-hibernate-update-the-resume-offset-on-SNAPSHOT_SE.patch
Patch121: 0025-Not-for-upstream-PM-hibernate-Speed-up-hibernation-b.patch
Patch122: 0026-xen-blkfront-resurrect-request-based-mode.patch
Patch123: 0027-xen-blkfront-add-persistent_grants-parameter.patch
Patch124: 0028-ACPI-SPCR-Make-SPCR-available-to-x86.patch
Patch125: 0029-Revert-xen-dont-fiddle-with-event-channel-masking-in.patch
Patch126: 0030-locking-paravirt-Use-new-static-key-for-controlling-.patch
Patch127: 0031-KVM-Introduce-paravirtualization-hints-and-KVM_HINTS.patch
Patch128: 0032-KVM-X86-Choose-qspinlock-when-dedicated-physical-CPU.patch
Patch129: 0033-x86-paravirt-Set-up-the-virt_spin_lock_key-after-sta.patch
Patch130: 0034-KVM-X86-Fix-setup-the-virt_spin_lock_key-before-stat.patch
Patch131: 0035-xen-blkfront-Fixed-blkfront_restore-to-remove-a-call.patch
Patch132: 0036-xen-netfront-Update-features-after-registering-netde.patch
Patch133: 0037-x86-tsc-avoid-system-instability-in-hibernation.patch
Patch134: 0038-blk-mq-simplify-queue-mapping-schedule-with-each-pos.patch
Patch135: 0039-blk-wbt-Avoid-lock-contention-and-thundering-herd-is.patch
Patch136: 0040-x86-MCE-AMD-Read-MCx_MISC-block-addresses-on-any-CPU.patch
Patch137: 0041-x86-bugs-Add-AMD-s-variant-of-SSB_NO.patch
Patch138: 0042-x86-bugs-Add-AMD-s-SPEC_CTRL-MSR-usage.patch
Patch139: 0043-x86-bugs-Switch-the-selection-of-mitigation-from-CPU.patch
Patch140: 0044-x86-CPU-Rename-intel_cacheinfo.c-to-cacheinfo.c.patch
Patch141: 0045-x86-CPU-AMD-Calculate-last-level-cache-ID-from-numbe.patch
Patch142: 0046-x86-CPU-AMD-Fix-LLC-ID-bit-shift-calculation.patch
Patch143: 0047-x86-bugs-Update-when-to-check-for-the-LS_CFG-SSBD-mi.patch
Patch144: 0048-x86-bugs-Fix-the-AMD-SSBD-usage-of-the-SPEC_CTRL-MSR.patch
Patch145: 0049-tools-power-turbostat-Read-extended-processor-family.patch
Patch146: 0050-sched-topology-Introduce-NUMA-identity-node-sched-do.patch
Patch147: 0051-x86-CPU-AMD-Derive-CPU-topology-from-CPUID-function-.patch
Patch148: 0052-vmxnet3-increase-default-rx-ring-sizes.patch
Patch149: 0053-Revert-e1000e-Separate-signaling-for-link-check-link.patch
Patch150: 0054-e1000e-Fix-link-check-race-condition.patch
Patch151: 0055-net-ipv4-defensive-cipso-option-parsing.patch

%if 0%{?kat_build:1}
Patch1000:	%{kat_build}.patch
%endif
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
BuildRequires:	audit-devel
Requires:       filesystem kmod
Requires(post):(coreutils or toybox)
%define uname_r %{version}-%{release}-aws

%description
The Linux package contains the Linux kernel.


%package devel
Summary:        Kernel Dev
Group:          System Environment/Kernel
Requires:       %{name} = %{version}-%{release}
Requires:       python2 gawk
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
Requires:       python2
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

%package tools
Summary:        This package contains the 'perf' performance analysis tools for Linux kernel
Group:          System/Tools
Requires:       %{name} = %{version}-%{release}
Requires:       audit
%description tools
This package contains the 'perf' performance analysis tools for Linux kernel.


%prep
%setup -q -n linux-%{version}

%patch0 -p1
%patch1 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch13 -p1
%patch24 -p1
%patch26 -p1
%patch28 -p1
%patch29 -p1
%patch30 -p1
%patch31 -p1

%patch101 -p1
%patch102 -p1
%patch103 -p1
%patch104 -p1
%patch105 -p1
%patch106 -p1
%patch107 -p1
%patch108 -p1
%patch109 -p1
%patch110 -p1
%patch111 -p1
%patch112 -p1
%patch113 -p1
%patch114 -p1
%patch115 -p1
%patch116 -p1
%patch117 -p1
%patch118 -p1
%patch119 -p1
%patch120 -p1
%patch121 -p1
%patch122 -p1
%patch123 -p1
%patch124 -p1
%patch125 -p1
%patch126 -p1
%patch127 -p1
%patch128 -p1
%patch129 -p1
%patch130 -p1
%patch131 -p1
%patch132 -p1
%patch133 -p1
%patch134 -p1
%patch135 -p1
%patch136 -p1
%patch137 -p1
%patch138 -p1
%patch139 -p1
%patch140 -p1
%patch141 -p1
%patch142 -p1
%patch143 -p1
%patch144 -p1
%patch145 -p1
%patch146 -p1
%patch147 -p1
%patch148 -p1
%patch149 -p1
%patch150 -p1
%patch151 -p1

%if 0%{?kat_build:1}
%patch1000 -p1
%endif

%build
make mrproper

%ifarch x86_64
cp %{SOURCE1} .config
arch="x86_64"
archdir="x86"
%endif

sed -i 's/CONFIG_LOCALVERSION="-aws"/CONFIG_LOCALVERSION="-%{release}-aws"/' .config
make LC_ALL= oldconfig
make VERBOSE=1 KBUILD_BUILD_VERSION="1-photon" KBUILD_BUILD_HOST="photon" ARCH=${arch} %{?_smp_mflags}
make -C tools perf

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
install -vdm 755 %{buildroot}/etc
install -vdm 755 %{buildroot}/boot
install -vdm 755 %{buildroot}%{_defaultdocdir}/%{name}-%{uname_r}
install -vdm 755 %{buildroot}/usr/src/%{name}-headers-%{uname_r}
install -vdm 755 %{buildroot}/usr/lib/debug/lib/modules/%{uname_r}
make INSTALL_MOD_PATH=%{buildroot} modules_install

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
cp -r Documentation/*        %{buildroot}%{_defaultdocdir}/%{name}-%{uname_r}
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
--add-drivers "tmem xen-scsifront xen-blkfront xen-acpi-processor xen-evtchn xen-gntalloc xen-gntdev xen-privcmd xen-pciback xenfs hv_utils hv_vmbus hv_storvsc hv_netvsc hv_sock hv_balloon cn"
EOF

#    Cleanup dangling symlinks
rm -rf %{buildroot}/lib/modules/%{uname_r}/source
rm -rf %{buildroot}/lib/modules/%{uname_r}/build

find . -name Makefile* -o -name Kconfig* -o -name *.pl | xargs  sh -c 'cp --parents "$@" %{buildroot}/usr/src/%{name}-headers-%{uname_r}' copy
find arch/${archdir}/include include scripts -type f | xargs  sh -c 'cp --parents "$@" %{buildroot}/usr/src/%{name}-headers-%{uname_r}' copy
find $(find arch/${archdir} -name include -o -name scripts -type d) -type f | xargs  sh -c 'cp --parents "$@" %{buildroot}/usr/src/%{name}-headers-%{uname_r}' copy
find arch/${archdir}/include Module.symvers include scripts -type f | xargs  sh -c 'cp --parents "$@" %{buildroot}/usr/src/%{name}-headers-%{uname_r}' copy
%ifarch x86_64
# CONFIG_STACK_VALIDATION=y requires objtool to build external modules
install -vsm 755 tools/objtool/objtool %{buildroot}/usr/src/%{name}-headers-%{uname_r}/tools/objtool/
install -vsm 755 tools/objtool/fixdep %{buildroot}/usr/src/%{name}-headers-%{uname_r}/tools/objtool/
%endif

cp .config %{buildroot}/usr/src/%{name}-headers-%{uname_r} # copy .config manually to be where it's expected to be
ln -sf "/usr/src/%{name}-headers-%{uname_r}" "%{buildroot}/lib/modules/%{uname_r}/build"
find %{buildroot}/lib/modules -name '*.ko' -print0 | xargs -0 chmod u+x

# disable (JOBS=1) parallel build to fix this issue:
# fixdep: error opening depfile: ./.plugin_cfg80211.o.d: No such file or directory
# Linux version that was affected is 4.4.26
make -C tools JOBS=1 DESTDIR=%{buildroot} prefix=%{_prefix} perf_install

%include %{SOURCE2}

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
/usr/src/%{name}-headers-%{uname_r}

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

%files tools
%defattr(-,root,root)
/usr/libexec
%exclude %{_libdir}/debug
%ifarch x86_64
/usr/lib64/traceevent
%endif
%{_bindir}
/etc/bash_completion.d/*
/usr/share/perf-core/strace/groups/file
/usr/share/doc/*

%changelog
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
