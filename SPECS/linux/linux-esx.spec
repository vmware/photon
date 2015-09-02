%global security_hardening none
Summary:        Kernel
Name:        linux-esx
Version:    4.2
Release:    1%{?dist}
License:    GPLv2
URL:        http://www.kernel.org/
Group:        System Environment/Kernel
Vendor:        VMware, Inc.
Distribution: Photon
Source0:    http://www.kernel.org/pub/linux/kernel/v4.x/linux-%{version}.tar.xz
%define sha1 linux=5e65d0dc94298527726fcd7458b6126e60fb2a8a
Source1:	config-esx-%{version}
patch1:		01-blkdev-max-rq.patch
patch2:		02-sysrq-Skip-synchronize_rcu-if-there-is-no-old-op.patch
patch3:		03-enable-no-blink-by-default.patch
patch4:		04-vmstat-update-interval.patch
patch5:		05-pci-probe-vmware.patch
patch6:		06-calibrate-delay-is-known-by-cpu-0.patch
patch7:		07-perf.patch
patch8:		08-No-wait-for-the-known-devices.patch
patch9:		09-Turn-mmput-into-an-async-function.patch
Patch10:	ptdamage.patch

BuildRequires:    bc
BuildRequires:    kbd
BuildRequires:    kmod
BuildRequires:     glib-devel
BuildRequires:     xerces-c-devel
BuildRequires:     xml-security-c-devel
BuildRequires:     libdnet
BuildRequires:     libmspack
BuildRequires:    Linux-PAM
BuildRequires:    openssl-devel
BuildRequires:    procps-ng-devel
Requires:    filesystem kmod coreutils

%description
The Linux kernel build for GOS for VMware hypervisor.



%package dev
Summary:    Kernel Dev
Group:        System Environment/Kernel
Requires:    python2
%description dev
The Linux package contains the Linux kernel dev files

%package docs
Summary:    Kernel docs
Group:        System Environment/Kernel
Requires:    python2
%description docs
The Linux package contains the Linux kernel doc files



%prep
%setup -q -n linux-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1

%build
make mrproper
cp %{SOURCE1} .config
make LC_ALL= oldconfig
make VERBOSE=1 KBUILD_BUILD_VERSION="1-photon" KBUILD_BUILD_HOST="photon" ARCH="x86_64" %{?_smp_mflags}

%install
install -vdm 755 %{buildroot}/etc
install -vdm 755 %{buildroot}/boot
install -vdm 755 %{buildroot}%{_defaultdocdir}/linux-esx-%{version}
install -vdm 755 %{buildroot}/etc/modprobe.d
make INSTALL_MOD_PATH=%{buildroot} modules_install
cp -v arch/x86/boot/bzImage    %{buildroot}/boot/vmlinuz-esx-%{version}
cp -v System.map        %{buildroot}/boot/system.map-esx-%{version}
cp -v .config            %{buildroot}/boot/config-esx-%{version}
cp -r Documentation/*        %{buildroot}%{_defaultdocdir}/linux-esx-%{version}

cat > %{buildroot}/boot/%{name}-%{version}-%{release}.cfg << "EOF"
# GRUB Environment Block
photon_cmdline=init=/lib/systemd/systemd tsc=reliable no_timer_check rcupdate.rcu_expedited=1 rootfstype=ext4 rw systemd.show_status=0 elevator=noop cpu_init_udelay=0 quiet
photon_linux=/boot/vmlinuz-esx-%{version}
EOF

%post
/sbin/depmod -aq %{version}-esx
ln -sf %{name}-%{version}-%{release}.cfg /boot/photon.cfg

%files
%defattr(-,root,root)
/boot/system.map-esx-%{version}
/boot/config-esx-%{version}
/boot/vmlinuz-esx-%{version}
%config(noreplace) /boot/%{name}-%{version}-%{release}.cfg
/lib/modules/*
%exclude /lib/modules/%{version}-esx/build

%files docs
%defattr(-,root,root)
%{_defaultdocdir}/linux-esx-%{version}/*



%files dev
%defattr(-,root,root)
/lib/modules/%{version}-esx/build

%changelog
*   Tue Sep 1 2015 Alexey Makhalov <amakhalov@vmware.com> 4.2-1
-   Update to linux-4.2. Enable CONFIG_EFI
*   Fri Aug 28 2015 Alexey Makhalov <amakhalov@vmware.com> 4.1.3-5
-   Added MD/LVM/DM modules.
-   Pci probe improvements.
*   Fri Aug 14 2015 Alexey Makhalov <amakhalov@vmware.com> 4.1.3-4
-   Use photon.cfg as a symlink.
*   Thu Aug 13 2015 Alexey Makhalov <amakhalov@vmware.com> 4.1.3-3
-   Added environment file(photon.cfg) for a grub.
*   Tue Aug 11 2015 Alexey Makhalov <amakhalov@vmware.com> 4.1.3-2
    Added pci-probe-vmware.patch. Removed unused modules. Decreased boot time. 
*   Tue Jul 28 2015 Alexey Makhalov <amakhalov@vmware.com> 4.1.3-1
    Initial commit. Use patchset from Clear Linux. 

