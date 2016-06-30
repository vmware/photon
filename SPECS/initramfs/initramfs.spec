%define LINUX_VERSION 4.4.8
Summary:	initramfs
Name:		initramfs
Version:	1.0
Release:	4%{?dist}
License:	Apache License
Group:		System Environment/Base
Vendor:		VMware, Inc.
Distribution:	Photon
Provides:	initramfs
BuildRequires:       linux = %{LINUX_VERSION}
BuildRequires:       dracut
BuildRequires:       ostree
Requires:	     linux = %{LINUX_VERSION}

%description
Photon release files such as yum configs and other /etc/ release related files

%prep
umask 022
cd /usr/src/photon/BUILD
cd /usr/src/photon/BUILD
rm -rf initramfs
mkdir initramfs
cd initramfs
/bin/chmod -Rf a+rX,u+w,g-w,o-w .
echo 'add_drivers+="tmem xen-acpi-processor xen-evtchn xen-gntalloc xen-gntdev xen-privcmd xen-pciback xenfs hv_ballon hv_utils hv_vmbus cn"' >> /etc/dracut.conf

echo 'add_dracutmodules+=" ostree systemd "' > /etc/dracut.conf.d/ostree.conf

%build
dracut --force --kver %{LINUX_VERSION} initrd.img-no-kmods
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
*   Thu Jun 30 2016 Xiaolin Li <xiaolinl@vmware.com> 1.0-4
-   Exapand setup macro and remove the source file.
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0-3
-	GA - Bump release of all rpms
*   Thu Apr 28 2016 Alexey Makhalov <amakhalov@vmware.com> 1.0-2
-   Update to linux-4.4.8
*   Thu Mar 24 2016 Xiaolin Li <xiaolinl@vmware.com> 1.0-1
-   Initial version.
