%global security_hardening none
Summary:       Kernel
Name:          linux-sec
Version:       4.8.0
Release:       1%{?dist}
License:       GPLv2
URL:           http://www.kernel.org/
Group:         System Environment/Kernel
Vendor:        VMware, Inc.
Distribution:  Photon
#Source0:       http://www.kernel.org/pub/linux/kernel/v4.x/linux-%{version}.tar.xz
Source0:       http://www.kernel.org/pub/linux/kernel/v4.x/linux-4.8.tar.xz
%define sha1 linux=e375f93600a7b96191498af39e5a2416b6666e59
Source1:       config-sec-%{version}
Patch0:        0001-NOWRITEEXEC-and-PAX-features-EMUTRAMP-MPROTECT.patch
Patch1:        0002-Added-rap_plugin.-Func-signature-fixing-is-still-req.patch
Patch2:        double-tcp_mem-limits.patch
Patch3:        linux-4.8-sysctl-sched_weighted_cpuload_uses_rla.patch
Patch4:        linux-4.8-watchdog-Disable-watchdog-on-virtual-machines.patch
Patch5:        SUNRPC-Do-not-reuse-srcport-for-TIME_WAIT-socket.patch
Patch6:        06-sunrpc.patch
Patch7:        linux-4.8-vmware-log-kmsg-dump-on-panic.patch
#Patch8:        linux-4.8-REVERT-sched-fair-Beef-up-wake_wide.patch
BuildRequires: bc
BuildRequires: kbd
BuildRequires: kmod
BuildRequires: glib-devel
BuildRequires: xerces-c-devel
BuildRequires: xml-security-c-devel
BuildRequires: libdnet
BuildRequires: libmspack
BuildRequires: Linux-PAM
BuildRequires: openssl-devel
BuildRequires: procps-ng-devel
Requires:      filesystem kmod coreutils

%description
Security hardened Linux kernel.

%package devel
Summary:       Kernel Dev
Group:         System Environment/Kernel
Requires:      python2
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
#%setup -q -n linux-%{version}
%setup -q -n linux-4.8
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
#%patch8 -p1

%build
# patch vmw_balloon driver
sed -i 's/module_init/late_initcall/' drivers/misc/vmw_balloon.c

make mrproper
cp %{SOURCE1} .config
make LC_ALL= oldconfig
make VERBOSE=1 KBUILD_BUILD_VERSION="1-photon" KBUILD_BUILD_HOST="photon" ARCH="x86_64" %{?_smp_mflags}

%install
install -vdm 755 %{buildroot}/etc
install -vdm 755 %{buildroot}/boot
install -vdm 755 %{buildroot}%{_defaultdocdir}/linux-sec-%{version}
install -vdm 755 %{buildroot}/etc/modprobe.d
install -vdm 755 %{buildroot}/usr/src/%{name}-headers-%{version}-%{release}
make INSTALL_MOD_PATH=%{buildroot} modules_install
cp -v arch/x86/boot/bzImage    %{buildroot}/boot/vmlinuz-sec-%{version}-%{release}
cp -v System.map        %{buildroot}/boot/system.map-sec-%{version}-%{release}
cp -v .config            %{buildroot}/boot/config-sec-%{version}-%{release}
cp -r Documentation/*        %{buildroot}%{_defaultdocdir}/linux-sec-%{version}
install -vdm 755 %{buildroot}/usr/lib/debug/lib/modules/%{version}-sec
cp -v vmlinux %{buildroot}/usr/lib/debug/lib/modules/%{version}-sec/vmlinux-sec-%{version}-%{release}

# TODO: noacpi acpi=off noapic pci=conf1,nodomains pcie_acpm=off pnpacpi=off
cat > %{buildroot}/boot/%{name}-%{version}-%{release}.cfg << "EOF"
# GRUB Environment Block
photon_cmdline=init=/lib/systemd/systemd rcupdate.rcu_expedited=1 rw systemd.show_status=0 quiet noreplace-smp cpu_init_udelay=0 plymouth.enable=0
photon_linux=vmlinuz-sec-%{version}-%{release}
EOF

# cleanup dangling symlinks
rm -f %{buildroot}/lib/modules/%{version}-sec/source
rm -f %{buildroot}/lib/modules/%{version}-sec/build

# create /use/src/linux-sec-headers-*/ content
find . -name Makefile* -o -name Kconfig* -o -name *.pl | xargs  sh -c 'cp --parents "$@" %{buildroot}/usr/src/%{name}-headers-%{version}-%{release}' copy
find arch/x86/include include scripts -type f | xargs  sh -c 'cp --parents "$@" %{buildroot}/usr/src/%{name}-headers-%{version}-%{release}' copy
find $(find arch/x86 -name include -o -name scripts -type d) -type f | xargs  sh -c 'cp --parents "$@" %{buildroot}/usr/src/%{name}-headers-%{version}-%{release}' copy
find arch/x86/include Module.symvers include scripts -type f | xargs  sh -c 'cp --parents "$@" %{buildroot}/usr/src/%{name}-headers-%{version}-%{release}' copy

# copy .config manually to be where it's expected to be
cp .config %{buildroot}/usr/src/%{name}-headers-%{version}-%{release}
# symling to the build folder
ln -sf /usr/src/%{name}-headers-%{version}-%{release} %{buildroot}/lib/modules/%{version}-sec/build
find %{buildroot}/lib/modules -name '*.ko' -print0 | xargs -0 chmod u+x

%post
/sbin/depmod -aq %{version}-sec
ln -sf %{name}-%{version}-%{release}.cfg /boot/photon.cfg

%files
%defattr(-,root,root)
/boot/system.map-sec-%{version}-%{release}
/boot/config-sec-%{version}-%{release}
/boot/vmlinuz-sec-%{version}-%{release}
%config(noreplace) /boot/%{name}-%{version}-%{release}.cfg
/lib/firmware/*
/lib/modules/*
%exclude /lib/modules/%{version}-sec/build
%exclude /usr/src

%files docs
%defattr(-,root,root)
%{_defaultdocdir}/linux-sec-%{version}/*

%files devel
%defattr(-,root,root)
/lib/modules/%{version}-sec/build
/usr/src/%{name}-headers-%{version}-%{release}

%changelog
*   Mon Oct 17 2016 Alexey Makhalov <amakhalov@vmware.com> 4.8.0-1
    Initial commit. 

