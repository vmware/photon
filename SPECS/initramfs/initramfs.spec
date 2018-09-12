# FIXME: noarch or generate debuginfo
%define debug_package %{nil}

Summary:        initramfs
Name:           initramfs
Version:        1.0
Release:        11%{?kernelsubrelease}%{?dist}
License:        Apache License
Group:          System Environment/Base
Source:        %{name}-%{version}.tar.gz
%define sha1 initramfs=9bdba4e4c13788838bc41bbf7d888e327c8783de
Vendor:         VMware, Inc.
Distribution:   Photon
Provides:       initramfs
BuildRequires:  linux = %{KERNEL_VERSION}-%{KERNEL_RELEASE}
BuildRequires:  dracut
BuildRequires:  ostree
BuildRequires:  e2fsprogs
BuildRequires:  lvm2-libs
BuildRequires:  lvm2
Requires:       linux = %{KERNEL_VERSION}-%{KERNEL_RELEASE}

%description
Photon release files such as yum configs and other /etc/ release related files

%prep
echo 'add_drivers+="tmem xen-acpi-processor xen-evtchn xen-gntalloc xen-gntdev xen-privcmd xen-pciback xenfs hv_ballon hv_utils hv_vmbus hv_storvsc hv_netvsc cn"' >> /etc/dracut.conf

echo 'add_dracutmodules+="ostree systemd"' > /etc/dracut.conf.d/ostree.conf

%build
dracut --force --kver %{KERNEL_VERSION}-%{KERNEL_RELEASE} --fscks "e2fsck fsck fsck.ext2 fsck.ext3 fsck.ext4" -a lvm --nostrip initrd.img-%{KERNEL_VERSION}-%{KERNEL_RELEASE}
%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/boot
install -m 600 initrd.img-%{KERNEL_VERSION}-%{KERNEL_RELEASE} $RPM_BUILD_ROOT/boot/initrd.img-%{KERNEL_VERSION}-%{KERNEL_RELEASE}

%post

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%dir /boot
/boot/initrd.img-%{KERNEL_VERSION}-%{KERNEL_RELEASE}

%changelog
*   Wed Sep 12 2018 Keerthana K <keerthanak@vmware.com> 1.0-11
-   Including nostrip option to the libraries packaged in initrd image.
*   Thu Sep 6 2018 Michelle Wang <michellew@vmware.com>  1.0-10
-   Add source file for initramfs for OSSTP
*   Wed Jul 11 2018 Dweep Advani <dadvani@vmware.com>  1.0-9
-   Add LVM driver for root on LVM
*   Wed Jul 12 2017 Anish Swaminathan <anishs@vmware.com>  1.0-8
-   Add missing hyperv driver
*   Wed Nov 30 2016 Alexey Makhalov <amakhalov@vmware.com> 1.0-7
-   Expand uname -r to have release number
*   Wed Nov 23 2016 Anish Swaminathan <anishs@vmware.com>  1.0-6
-   Dracut module change to include systemd initrd target
*   Thu Oct 13 2016 Alexey Makhalov <amakhalov@vmware.com> 1.0-5
-   Use kernel version and release number in initrd file name
*   Tue Oct 11 2016 Divya Thaluru <dthaluru@vmware.com> 1.0-4
-   Added kernel macros
*   Wed Oct  5 2016 Alexey Makhalov <amakhalov@vmware.com> 1.0-4
-   Added fsck tools
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0-3
-   GA - Bump release of all rpms
*   Thu Apr 28 2016 Alexey Makhalov <amakhalov@vmware.com> 1.0-2
-   Update to linux-4.4.8
*   Thu Mar 24 2016 Xiaolin Li <xiaolinl@vmware.com> 1.0-1
-   Initial version.
