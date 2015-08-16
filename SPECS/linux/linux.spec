%global security_hardening none
%define    OPENVMTOOLS_NAME            open-vm-tools
%define    OPENVMTOOLS_VERSION         10.0.0
Summary:        Kernel
Name:        linux
Version:    4.0.9
Release:    3%{?dist}
License:    GPLv2
URL:        http://www.kernel.org/
Group:        System Environment/Kernel
Vendor:        VMware, Inc.
Distribution: Photon
Source0:    http://www.kernel.org/pub/linux/kernel/v4.x/%{name}-%{version}.tar.xz
%define sha1 linux=355d1ab33bfea50442b54b7a594ae4d015ea47e0
#Source1:    config-%{version}-generic.amd64
Source1:    http://downloads.sourceforge.net/project/open-vm-tools/open-vm-tools/stable-10.0.0/open-vm-tools-10.0.0.tar.gz
%define sha1 open-vm-tools=1658ab1b73438e746bb6f11f16fe570eaf753747
Source2:	config-%{version}
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
Requires:    %{name} = %{version}
%description drivers-gpu
The Linux package contains the Linux kernel drivers for GPU

%package sound
Summary:    Kernel Sound modules
Group:        System Environment/Kernel
Requires:    %{name} = %{version}
%description sound
The Linux package contains the Linux kernel sound support

%package docs
Summary:    Kernel docs
Group:        System Environment/Kernel
Requires:    python2
%description docs
The Linux package contains the Linux kernel doc files



%prep
%setup -c -n Linux-package -a 1
cd %{OPENVMTOOLS_NAME}-%{OPENVMTOOLS_VERSION}

%build
#make linux 
cd %{name}-%{version}
make mrproper
cp %{SOURCE2} .config
make LC_ALL= oldconfig
#make LC_ALL= silentoldconfig
#make LC_ALL= defconfig
make VERBOSE=1 KBUILD_BUILD_VERSION="1-photon" KBUILD_BUILD_HOST="photon" ARCH="x86_64" %{?_smp_mflags}

%install
cd %{name}-%{version}
install -vdm 755 %{buildroot}/etc
install -vdm 755 %{buildroot}/boot
install -vdm 755 %{buildroot}%{_defaultdocdir}/%{name}-%{version}
install -vdm 755 %{buildroot}/etc/modprobe.d
make INSTALL_MOD_PATH=%{buildroot} modules_install
cp -v arch/x86/boot/bzImage    %{buildroot}/boot/vmlinuz-%{version}
cp -v System.map        %{buildroot}/boot/system.map-%{version}
cp -v .config            %{buildroot}/boot/config-%{version}
cp -r Documentation/*        %{buildroot}%{_defaultdocdir}/%{name}-%{version}
cat > %{buildroot}/boot/%{name}-%{version}-%{release}.cfg << "EOF"
# GRUB Environment Block
photon_cmdline=init=/lib/systemd/systemd rootfstype=ext4 ro loglevel=3 quiet
photon_linux=/boot/vmlinuz-%{version}
photon_initrd=/boot/initrd.img-no-kmods
EOF

#    Cleanup dangling symlinks
rm -rf %{buildroot}/lib/modules/%{version}/source
rm -rf %{buildroot}/lib/modules/%{version}/build



#Copy necessary files to build other kernel modules.   
install -vdm 755 %{buildroot}/lib/modules/%{version}/build
install -vdm 755 %{buildroot}/lib/modules/%{version}/build/arch
mv include %{buildroot}/lib/modules/%{version}/build/
mv scripts %{buildroot}/lib/modules/%{version}/build/
mv arch/x86_64 %{buildroot}/lib/modules/%{version}/build/arch/
mv arch/x86 %{buildroot}/lib/modules/%{version}/build/arch/
cp Makefile %{buildroot}/lib/modules/%{version}/build/

# make open vm tools - vmhgfs
cd ../%{OPENVMTOOLS_NAME}-%{OPENVMTOOLS_VERSION}
#copy buildroot's kernel modules to chroot's kernel
cp -R %{buildroot}/lib/modules/ /lib/modules/
cd modules/linux/vmhgfs
make %{?_smp_mflags} VM_KBUILD=%{version} OVT_SOURCE_DIR=/usr/src/photon/BUILD/Linux-package/%{OPENVMTOOLS_NAME}-%{OPENVMTOOLS_VERSION}/ VM_UNAME=%{version}
# install vmhgfs
mkdir %{buildroot}/lib/modules/%{version}/misc
install -vm 755 vmhgfs.ko %{buildroot}/lib/modules/%{version}/misc/

rm -rf /lib/modules
#Load the vmhgfs module at boot
install -vdm 755 %{buildroot}/etc/modules-load.d
cat > %{buildroot}/etc/modules-load.d/vmhgfs.conf <<- "EOF"
# Begin /etc/modules-load.d/vmhgfs.conf
vmhgfs
# End /etc/modules-load.d/vmhgfs.conf
EOF

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
%config(noreplace) /etc/modules-load.d/vmhgfs.conf
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

%files drivers-gpu
%defattr(-,root,root)
%exclude /lib/modules/%{version}/kernel/drivers/gpu/drm/cirrus/
/lib/modules/%{version}/kernel/drivers/gpu

%files sound
%defattr(-,root,root)
/lib/modules/%{version}/kernel/sound

%changelog
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

