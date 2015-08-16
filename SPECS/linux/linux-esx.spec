%global security_hardening none
# Kernel parameters:
# init=/lib/systemd/systemd tsc=reliable no_timer_check rcupdate.rcu_expedited=1 rootfstype=ext4 root=/dev/sda2 rw systemd.show_status=0 elevator=noop quiet
Summary:        Kernel
Name:        linux-esx
Version:    4.1.3
Release:    4%{?dist}
License:    GPLv2
URL:        http://www.kernel.org/
Group:        System Environment/Kernel
Vendor:        VMware, Inc.
Distribution: Photon
Source0:    http://www.kernel.org/pub/linux/kernel/v4.x/linux-%{version}.tar.xz
%define sha1 linux=718cdc5fab5d24bbcba26d1a5a19e1c950b087c0
Source1:	config-%{version}-esx
Patch1:		0001-msleep.patch
patch2:		0002-Skip-synchronize_rcu-on-single-CPU-systems.patch
patch3:		0003-sysrq-Skip-synchronize_rcu-if-there-is-no-old-op.patch
patch4:		0004-enable-no-blink-by-default.patch
patch5:		0005-wakeups.patch
patch6:		pci-probe-vmware.patch
patch7:		0007-cgroup.patch
patch8:		0008-smpboot.patch
patch9: 	0009-perf.patch
patch10:	0010-tweak-the-scheduler-to-favor-CPU-0.patch
patch11:	0012-No-wait-for-the-known-devices.patch
patch12:	0013-Turn-mmput-into-an-async-function.patch
Patch13:	ptdamage.patch

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
The Linux kernel build for GOS for ESX hypervisor.



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
%patch11 -p1
%patch12 -p1
%patch13 -p1

%build
#make linux 
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
photon_cmdline=init=/lib/systemd/systemd tsc=reliable no_timer_check rcupdate.rcu_expedited=1 rootfstype=ext4 rw systemd.show_status=0 elevator=noop quiet
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
#/lib/firmware/*
/lib/modules/*
%exclude /lib/modules/%{version}-esx/build

%files docs
%defattr(-,root,root)
%{_defaultdocdir}/linux-esx-%{version}/*



%files dev
%defattr(-,root,root)
/lib/modules/%{version}-esx/build

%changelog
*   Fri Aug 14 2015 Alexey Makhalov <amakhalov@vmware.com> 4.1.3-4
-   Use photon.cfg as a symlink.
*   Thu Aug 13 2015 Alexey Makhalov <amakhalov@vmware.com> 4.1.3-3
-   Added environment file(photon.cfg) for grub.
*   Tue Aug 11 2015 Alexey Makhalov <amakhalov@vmware.com> 4.1.3-2
    Added pci-probe-vmware.patch. Removed unused modules. Decreased boot time. 
*   Tue Jul 28 2015 Alexey Makhalov <amakhalov@vmware.com> 4.1.3-1
    Initial commit. Use patchset from Clear Linux. 

