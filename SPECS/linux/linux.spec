%global security_hardening none
Summary:        Kernel
Name:        linux
Version:    4.2.0
Release:    4%{?dist}
License:    GPLv2
URL:        http://www.kernel.org/
Group:        System Environment/Kernel
Vendor:        VMware, Inc.
Distribution: Photon
Source0:    http://www.kernel.org/pub/linux/kernel/v4.x/linux-4.2.tar.xz
%define sha1 linux=5e65d0dc94298527726fcd7458b6126e60fb2a8a
Source1:	config-%{version}
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
Requires:         filesystem kmod coreutils

%description
The Linux package contains the Linux kernel. 


%package dev
Summary:    Kernel Dev
Group:        System Environment/Kernel
Requires:    python2
%description dev
The Linux package contains the Linux kernel dev files

%package drivers-gpu
Summary:    Kernel GPU Drivers
Group:        System Environment/Kernel
Requires:    %{name} = %{version}-%{release}
%description drivers-gpu
The Linux package contains the Linux kernel drivers for GPU

%package sound
Summary:    Kernel Sound modules
Group:        System Environment/Kernel
Requires:    %{name} = %{version}-%{release}
%description sound
The Linux package contains the Linux kernel sound support

%package docs
Summary:    Kernel docs
Group:        System Environment/Kernel
Requires:    python2
%description docs
The Linux package contains the Linux kernel doc files



%prep
%setup -q -n linux-4.2

%build
make mrproper
cp %{SOURCE1} .config
make LC_ALL= oldconfig
make VERBOSE=1 KBUILD_BUILD_VERSION="1-photon" KBUILD_BUILD_HOST="photon" ARCH="x86_64" %{?_smp_mflags}

%install
install -vdm 755 %{buildroot}/etc
install -vdm 755 %{buildroot}/boot
install -vdm 755 %{buildroot}%{_defaultdocdir}/%{name}-%{version}
install -vdm 755 %{buildroot}/etc/modprobe.d
install -vdm 755 %{buildroot}/usr/src/%{name}-headers-%{version}-%{release}
make INSTALL_MOD_PATH=%{buildroot} modules_install

cp -v arch/x86/boot/bzImage    %{buildroot}/boot/vmlinuz-%{version}
cp -v System.map        %{buildroot}/boot/system.map-%{version}
cp -v .config            %{buildroot}/boot/config-%{version}
cp -r Documentation/*        %{buildroot}%{_defaultdocdir}/%{name}-%{version}
cat > %{buildroot}/boot/%{name}-%{version}-%{release}.cfg << "EOF"
# GRUB Environment Block
photon_cmdline=init=/lib/systemd/systemd rootfstype=ext4 ro loglevel=3 quiet plymouth.enable=0
photon_linux=vmlinuz-%{version}
photon_initrd=initrd.img-no-kmods
EOF

#    Cleanup dangling symlinks
rm -rf %{buildroot}/lib/modules/%{version}/source
rm -rf %{buildroot}/lib/modules/%{version}/build

find . -name Makefile* -o -name Kconfig* -o -name *.pl | xargs  sh -c 'cp --parents "$@" %{buildroot}/usr/src/%{name}-headers-%{version}-%{release}'
find arch/x86/include include scripts -type f | xargs  sh -c 'cp --parents "$@" %{buildroot}/usr/src/%{name}-headers-%{version}-%{release}'
find $(find arch/x86 -name include -o -name scripts -type d) -type f | xargs  sh -c 'cp --parents "$@" %{buildroot}/usr/src/%{name}-headers-%{version}-%{release}'
find arch/x86/include Module.symvers include scripts -type f | xargs  sh -c 'cp --parents "$@" %{buildroot}/usr/src/%{name}-headers-%{version}-%{release}'

cp .config %{buildroot}/usr/src/%{name}-headers-%{version}-%{release} # copy .config manually to be where it's expected to be
ln -sf "/usr/src/%{name}-headers-%{version}-%{release}" "%{buildroot}/lib/modules/%{version}/build"

%post
/sbin/depmod -aq %{version}
ln -sf %{name}-%{version}-%{release}.cfg /boot/photon.cfg

%post drivers-gpu
/sbin/depmod -aq %{version}

%post sound
/sbin/depmod -aq %{version}

%files
%defattr(-,root,root)
/boot/system.map-%{version}
/boot/config-%{version}
/boot/vmlinuz-%{version}
%config(noreplace) /boot/%{name}-%{version}-%{release}.cfg
/lib/firmware/*
/lib/modules/*
%exclude /lib/modules/%{version}/build
%exclude /lib/modules/%{version}/kernel/drivers/gpu
%exclude /lib/modules/%{version}/kernel/sound

%files docs
%defattr(-,root,root)
%{_defaultdocdir}/%{name}-%{version}/*

%files dev
%defattr(-,root,root)
/lib/modules/%{version}/build
/usr/src/%{name}-headers-%{version}-%{release}

%files drivers-gpu
%defattr(-,root,root)
%exclude /lib/modules/%{version}/kernel/drivers/gpu/drm/cirrus/
/lib/modules/%{version}/kernel/drivers/gpu

%files sound
%defattr(-,root,root)
/lib/modules/%{version}/kernel/sound

%changelog
*   Fri Nov 13 2015 Mahmoud Bassiouny <mbassiouny@vmware.com> 4.2.0-4
-   Change the linux image directory.
*	Wed Nov 11 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.2.0-3
- 	Added the build essential files in the dev sub-package.
*	Mon Nov 09 2015 Vinay Kulkarni <kulkarniv@vmware.com> 4.2.0-2
- 	Enable Geneve module support for generic kernel.
*	Fri Oct 23 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.2.0-1
- 	Upgraded the generic linux kernel to version 4.2.0 & and updated timer handling to full tickless mode. 
*	Tue Sep 22 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.0.9-5
- 	Added driver support for frame buffer devices and ACPI 
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

