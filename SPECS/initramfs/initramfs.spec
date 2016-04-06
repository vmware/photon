Summary:	initramfs
Name:		initramfs
Version:	1.0
Release:	1%{?dist}
License:	Apache License
Group:		System Environment/Base
Source:		photon-release-1.0.2.tar.gz
%define sha1 photon-release=4c03ec658315e25873e5e5f3e77c0006ddfeecc6
Vendor:		VMware, Inc.
Distribution:	Photon
Provides:	initramfs
BuildRequires:       linux
BuildRequires:       dracut
BuildRequires:       ostree

%description
Photon release files such as yum configs and other /etc/ release related files

%prep
%setup -q -n photon-release-1.0.2
echo 'add_drivers+="tmem xen-acpi-processor xen-evtchn xen-gntalloc xen-gntdev xen-privcmd xen-pciback xenfs hv_ballon hv_utils hv_vmbus cn"' >> /etc/dracut.conf

echo 'add_dracutmodules+=" ostree systemd "' > /etc/dracut.conf.d/ostree.conf

%build
dracut --force --kver  4.2.0 initrd.img-no-kmods 
%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/boot
install -m 600 initrd.img-no-kmods $RPM_BUILD_ROOT/boot/initrd.img-no-kmods

%post

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%dir /boot
/boot/initrd.img-no-kmods 

%changelog
*  		Thu Mar 24 2016 Xiaolin Li <xiaolinl@vmware.com> 1.0-1
-		Initial version.