%global security_hardening none
# Kernel parameters:
# console=ttyS0,115200n8 quiet init=/lib/systemd/systemd notsc no_timer_check noreplace-smp rcupdate.rcu_expedited=1 rootfstype=ext4 root=/dev/vda2 rw systemd.show_status=0 elevator=noop
Summary:        Kernel
Name:        linux-kvm
Version:    4.1.3
Release:    1%{?dist}
License:    GPLv2
URL:        http://www.kernel.org/
Group:        System Environment/Kernel
Vendor:        VMware, Inc.
Distribution: Photon
Source0:    http://www.kernel.org/pub/linux/kernel/v4.x/linux-%{version}.tar.xz
%define sha1 linux=718cdc5fab5d24bbcba26d1a5a19e1c950b087c0
Source1:	config-%{version}-kvm
Patch1:		0001-msleep.patch
patch2:		0002-Skip-synchronize_rcu-on-single-CPU-systems.patch
patch3:		0003-sysrq-Skip-synchronize_rcu-if-there-is-no-old-op.patch
patch4:		0004-enable-no-blink-by-default.patch
patch5:		0005-wakeups.patch
patch6:		0006-probe.patch
patch7:		0007-cgroup.patch
patch8:		0008-smpboot.patch
patch9: 	0009-perf.patch
patch10:	0010-tweak-the-scheduler-to-favor-CPU-0.patch
patch11:	0011-probe2.patch
patch12:	0012-No-wait-for-the-known-devices.patch
patch13:	0013-Turn-mmput-into-an-async-function.patch
Patch14:	ptdamage.patch

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
Requires:    xerces-c
Requires:    libdnet
Requires:    libmspack
Requires:    glib
Requires:    xml-security-c
Requires:    openssl
Requires:    filesystem

%description
The Linux kernel build for GOS for KVM hypervisor.



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
%patch14 -p1

%build
#make linux 
make mrproper
cp %{SOURCE1} .config
make LC_ALL= oldconfig
make VERBOSE=1 KBUILD_BUILD_VERSION="1-photon" KBUILD_BUILD_HOST="photon" ARCH="x86_64" %{?_smp_mflags}

%install
install -vdm 755 %{buildroot}/etc
install -vdm 755 %{buildroot}/boot
install -vdm 755 %{buildroot}%{_defaultdocdir}/linux-%{version}
install -vdm 755 %{buildroot}/etc/modprobe.d
make INSTALL_MOD_PATH=%{buildroot} modules_install
cp -v arch/x86/boot/bzImage    %{buildroot}/boot/vmlinuz-%{version}
cp -v System.map        %{buildroot}/boot/system.map-%{version}
cp -v .config            %{buildroot}/boot/config-%{version}
cp -r Documentation/*        %{buildroot}%{_defaultdocdir}/linux-%{version}

%post
/sbin/depmod -aq %{version}

%files
%defattr(-,root,root)
/boot/system.map-%{version}
/boot/config-%{version}
/boot/vmlinuz-%{version}
#/lib/firmware/*
/lib/modules/*
%exclude /lib/modules/%{version}-kvm/build

%files docs
%defattr(-,root,root)
%{_defaultdocdir}/linux-%{version}/*



%files dev
%defattr(-,root,root)
/lib/modules/%{version}-kvm/build

%changelog
*   Tue Jul 28 2015 Alexey Makhalov <amakhalov@vmware.com> 4.1.3-1
    Initial commit. Use patchset from Clear Linux. 

