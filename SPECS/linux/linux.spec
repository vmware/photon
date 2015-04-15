Summary:	Kernel
Name:		linux
Version:	3.19.2
Release:	1
License:	GPLv2
URL:		http://www.kernel.org/
Group:		System Environment/Kernel
Vendor:		VMware, Inc.
Distribution: Photon
Source0:	http://www.kernel.org/pub/linux/kernel/v3.x/%{name}-%{version}.tar.xz
#Source1:	config-%{version}-generic.amd64
BuildRequires:	bc
BuildRequires:	kbd
BuildRequires:	kmod
%description
The Linux package contains the Linux kernel.

%package dev
Summary:	Kernel Dev
Group:		System Environment/Kernel
Requires:	python2
%description dev
The Linux package contains the Linux kernel dev files

%package docs
Summary:	Kernel docs
Group:		System Environment/Kernel
Requires:	python2
%description docs
The Linux package contains the Linux kernel doc files

%prep
%setup -q
%build
make mrproper
cp %{_topdir}/config .config
make LC=ALL= oldconfig
#make LC_ALL= silentoldconfig
#make LC_ALL= defconfig
make VERBOSE=1 KBUILD_BUILD_VERSION="1-photon" KBUILD_BUILD_HOST="photon" ARCH="x86_64" %{?_smp_mflags}
%install
install -vdm 755 %{buildroot}/etc
install -vdm 755 %{buildroot}/boot
install -vdm 755 %{buildroot}%{_defaultdocdir}/%{name}-%{version}
install -vdm 755 %{buildroot}/etc/modprobe.d
make INSTALL_MOD_PATH=%{buildroot} modules_install
cp -v arch/x86/boot/bzImage	%{buildroot}/boot/vmlinuz-%{version}
cp -v System.map		%{buildroot}/boot/system.map-%{version}
cp -v .config			%{buildroot}/boot/config-%{version}
cp -r Documentation/*		%{buildroot}%{_defaultdocdir}/%{name}-%{version}

cat > %{buildroot}/etc/modprobe.d/usb.conf << "EOF"
# Begin /etc/modprobe.d/usb.conf

install ohci_hcd /sbin/modprobe ehci_hcd ; /sbin/modprobe -i ohci_hcd ; true
install uhci_hcd /sbin/modprobe ehci_hcd ; /sbin/modprobe -i uhci_hcd ; true

# End /etc/modprobe.d/usb.conf
EOF
#	Cleanup dangling symlinks
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
%files
%defattr(-,root,root)
/boot/system.map-%{version}
/boot/config-%{version}
/boot/vmlinuz-%{version}
%config(noreplace)/etc/modprobe.d/usb.conf
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
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 3.13.3-1
-	Initial build. First version
