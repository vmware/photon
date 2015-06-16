%define    OPENVMTOOLS_NAME            open-vm-tools
%define    OPENVMTOOLS_VERSION         9.10.0
Summary:        Kernel
Name:        linux
Version:    3.19.2
Release:    2%{?dist}
License:    GPLv2
URL:        http://www.kernel.org/
Group:        System Environment/Kernel
Vendor:        VMware, Inc.
Distribution: Photon
Source0:    http://www.kernel.org/pub/linux/kernel/v3.x/%{name}-%{version}.tar.xz
#Source1:    config-%{version}-generic.amd64
Source1:    http://downloads.sourceforge.net/project/open-vm-tools/open-vm-tools/stable-9.10.0/open-vm-tools-9.10.0.tar.gz
Patch0:        vmhgfs_fix_3.19.patch
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
The Linux package contains the Linux kernel. Open vmware tools package contains the kernel module vmhgfs



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
%setup -c -n Linux-package -a 1
cd %{OPENVMTOOLS_NAME}-%{OPENVMTOOLS_VERSION}
%patch -P 0 -p1

%build
#make linux 
cd %{name}-%{version}
make mrproper
cp %{_topdir}/config .config
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
/sbin/depmod

%files
%defattr(-,root,root)
/boot/system.map-%{version}
/boot/config-%{version}
/boot/vmlinuz-%{version}
%config(noreplace) /etc/modules-load.d/vmhgfs.conf
/lib/firmware/*
/lib/modules/*
%exclude /lib/modules/%{version}/build

%files docs
%defattr(-,root,root)
%{_defaultdocdir}/%{name}-%{version}/*



%files dev
%defattr(-,root,root)
/lib/modules/%{version}/build



%changelog
*   Mon May 18 2015 Touseef Liaqat <tliaqat@vmware.com> 3.13.3-2
-   Update according to UsrMove.
*   Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 3.13.3-1
-   Initial build. First version

