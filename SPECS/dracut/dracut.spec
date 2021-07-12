%define dracutlibdir %{_prefix}/lib/dracut
%define _unitdir /usr/lib/systemd/system

Summary:        dracut to create initramfs
Name:           dracut
Version:        055
Release:        1%{?dist}
Group:          System Environment/Base
# The entire source code is GPLv2+; except install/* which is LGPLv2+
License:        GPLv2+ and LGPLv2+
URL:            https://dracut.wiki.kernel.org
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://www.kernel.org/pub/linux/utils/boot/dracut/dracut-%{version}.tar.xz
%define sha1    %{name}=1c0eb80f930dc1e4baac1912239aee233a108bc3

# Taken from https://www.gnu.org/licenses/lgpl-2.1.txt
Source1:        lgpl-2.1.txt

Patch0:         Add-mkinitrd-support-to-dracut.patch
Patch1:         disable-xattr.patch
Patch2:         fix-initrd-naming-for-photon.patch
Patch3:         lvm-no-read-only-locking.patch
Patch4:         fix-hostonly.patch

BuildRequires:  bash
BuildRequires:  git
BuildRequires:  pkg-config
BuildRequires:  kmod-devel
BuildRequires:  asciidoc3

Requires:       bash >= 4
Requires:       (coreutils or toybox)
Requires:       kmod
Requires:       (util-linux or toybox)
Requires:       systemd
Requires:       /bin/sed
Requires:       /bin/grep
Requires:       (findutils or toybox)
Requires:       (cpio or toybox)

%description
dracut contains tools to create a bootable initramfs for 2.6 Linux kernels.
Unlike existing implementations, dracut does hard-code as little as possible
into the initramfs. dracut contains various modules which are driven by the
event-based udev. Having root on MD, DM, LVM2, LUKS is supported as well as
NFS, iSCSI, NBD, FCoE with the dracut-network package.

%package tools
Summary: dracut tools to build the local initramfs
Requires: %{name} = %{version}-%{release}

%description tools
This package contains tools to assemble the local initrd and host configuration.

%prep
%autosetup -n %{name}-%{version} -p1
cp %{SOURCE1} .

%build
%configure --systemdsystemunitdir=%{_unitdir} \
           --bashcompletiondir=$(pkg-config --variable=completionsdir bash-completion) \
           --libdir=%{_prefix}/lib \
           --disable-documentation

make %{?_smp_mflags}

%install
rm -rf -- %{buildroot}
make %{?_smp_mflags} install \
     DESTDIR=%{buildroot} \
     libdir=%{_prefix}/lib

echo "DRACUT_VERSION=%{version}-%{release}" > %{buildroot}/%{dracutlibdir}/dracut-version.sh

rm -fr -- %{buildroot}/%{dracutlibdir}/modules.d/01fips
rm -fr -- %{buildroot}/%{dracutlibdir}/modules.d/02fips-aesni

rm -fr -- %{buildroot}/%{dracutlibdir}/modules.d/00bootchart

# we do not support dash in the initramfs
rm -fr -- %{buildroot}/%{dracutlibdir}/modules.d/00dash

# remove gentoo specific modules
rm -fr -- %{buildroot}/%{dracutlibdir}/modules.d/50gensplash

rm -fr -- %{buildroot}/%{dracutlibdir}/modules.d/96securityfs
rm -fr -- %{buildroot}/%{dracutlibdir}/modules.d/97masterkey
rm -fr -- %{buildroot}/%{dracutlibdir}/modules.d/98integrity

mkdir -p %{buildroot}/boot/dracut
mkdir -p %{buildroot}/var/lib/dracut/overlay
mkdir -p %{buildroot}%{_localstatedir}/log
mkdir -p %{buildroot}%{_localstatedir}/opt/dracut/log
touch %{buildroot}%{_localstatedir}/opt/dracut/log/dracut.log
ln -sfv %{_localstatedir}/opt/dracut/log/dracut.log %{buildroot}%{_localstatedir}/log/
mkdir -p %{buildroot}%{_sharedstatedir}/initramfs

rm -f %{buildroot}%{_mandir}/man?/*suse*

# create compat symlink
mkdir -p %{buildroot}%{_sbindir}
ln -sr %{buildroot}%{_bindir}/dracut %{buildroot}%{_sbindir}/dracut

%clean
rm -rf -- %{buildroot}

%files
%defattr(-,root,root,0755)
%{!?_licensedir:%global license %%doc}
%license COPYING lgpl-2.1.txt
%{_bindir}/dracut
%{_bindir}/mkinitrd
%{_bindir}/lsinitrd
# compat symlink
%{_sbindir}/dracut
%{_datadir}/bash-completion/completions/dracut
%{_datadir}/bash-completion/completions/lsinitrd
%dir %{dracutlibdir}
%dir %{dracutlibdir}/modules.d
%{dracutlibdir}/modules.d/*
%exclude %{_libdir}/kernel
/usr/lib/dracut/dracut-init.sh
/usr/share/pkgconfig/dracut.pc
%{dracutlibdir}/dracut-functions.sh
%{dracutlibdir}/dracut-functions
%{dracutlibdir}/dracut-version.sh
%{dracutlibdir}/dracut-logger.sh
%{dracutlibdir}/dracut-initramfs-restore
%{dracutlibdir}/dracut-install
%{dracutlibdir}/skipcpio
%{dracutlibdir}/dracut-util
%config(noreplace) %{_sysconfdir}/dracut.conf
%dir %{_sysconfdir}/dracut.conf.d
%dir %{dracutlibdir}/dracut.conf.d
%dir %{_localstatedir}/opt/dracut/log
%attr(0644,root,root) %ghost %config(missingok,noreplace) %{_localstatedir}/opt/dracut/log/dracut.log
%{_localstatedir}/log/dracut.log
%dir %{_sharedstatedir}/initramfs
%{_unitdir}/dracut-shutdown.service
%{_unitdir}/sysinit.target.wants/dracut-shutdown.service
%{_unitdir}/dracut-cmdline.service
%{_unitdir}/dracut-initqueue.service
%{_unitdir}/dracut-mount.service
%{_unitdir}/dracut-pre-mount.service
%{_unitdir}/dracut-pre-pivot.service
%{_unitdir}/dracut-pre-trigger.service
%{_unitdir}/dracut-pre-udev.service
%{_unitdir}/initrd.target.wants/dracut-cmdline.service
%{_unitdir}/initrd.target.wants/dracut-initqueue.service
%{_unitdir}/initrd.target.wants/dracut-mount.service
%{_unitdir}/initrd.target.wants/dracut-pre-mount.service
%{_unitdir}/initrd.target.wants/dracut-pre-pivot.service
%{_unitdir}/initrd.target.wants/dracut-pre-trigger.service
%{_unitdir}/initrd.target.wants/dracut-pre-udev.service

%files tools
%defattr(-,root,root,0755)

%{_bindir}/dracut-catimages
%dir /boot/dracut
%dir /var/lib/dracut
%dir /var/lib/dracut/overlay

%changelog
*   Mon Jul 12 2021 Shreenidhi Shedi <sshedi@vmware.com> 055-1
-   Upgrade to version 055
*   Wed Jan 20 2021 Shreenidhi Shedi <sshedi@vmware.com> 050-7
-   Added a command line option to manually override host_only
*   Tue Dec 15 2020 Shreenidhi Shedi <sshedi@vmware.com> 050-6
-   Adjust hostonly based on running environment
*   Tue Nov 03 2020 Srinidhi Rao <srinidhir@vmware.com> 050-5
-   Remove fipsify support
*   Fri Oct 09 2020 Shreenidhi Shedi <sshedi@vmware.com> 050-4
-   Fixed hostonly setting logic to generate initrd properly
*   Mon Oct 05 2020 Susant Sahani <ssahani@vmware.com> 050-3
-   Fix mkitnird and lsinitrd
*   Sun Jun 21 2020 Tapas Kundu <tkundu@vmware.com> 050-2
-   Use asciidoc3
*   Fri Apr 24 2020 Susant Sahani <ssahani@vmware.com> 050-1
-   Update to 050
*   Fri Apr 03 2020 Vikash Bansal <bvikas@vmware.com> 048-4
-   Added fips module
*   Wed Apr 01 2020 Susant Sahani <ssahani@vmware.com> 048-3
-   systemd: install systemd-tty-ask-password-agent systemd-ask-password
*   Thu Oct 10 2019 Alexey Makhalov <amakhalov@vmware.com> 048-2
-   lvm.conf: Do not set read-only locking.
*   Mon Oct 01 2018 Alexey Makhalov <amakhalov@vmware.com> 048-1
-   Version update
*   Thu Dec 28 2017 Divya Thaluru <dthaluru@vmware.com>  045-6
-   Fixed the log file directory structure
*   Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 045-5
-   Requires coreutils/util-linux/findutils or toybox,
    /bin/grep, /bin/sed
*   Fri Jun 23 2017 Xiaolin Li <xiaolinl@vmware.com> 045-4
-   Add kmod-devel to BuildRequires
*   Fri May 26 2017 Bo Gan <ganb@vmware.com> 045-3
-   Fix dependency
*   Thu Apr 27 2017 Bo Gan <ganb@vmware.com> 045-2
-   Disable xattr for cp
*   Wed Apr 12 2017 Chang Lee <changlee@vmware.com> 045-1
-   Updated to 045
*   Wed Jan 25 2017 Harish Udaiya Kumar <hudaiyakumr@vmware.com> 044-6
-   Added the patch for bash 4.4 support.
*   Wed Nov 23 2016 Anish Swaminathan <anishs@vmware.com>  044-5
-   Add systemd initrd root device target to list of modules
*   Fri Oct 07 2016 ChangLee <changlee@vmware.com> 044-4
-   Modified %check
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 044-3
-   GA - Bump release of all rpms
*   Mon Apr 25 2016 Gengsheng Liu <gengshengl@vmware.com> 044-2
-   Fix incorrect systemd directory.
*   Thu Feb 25 2016 Kumar Kaushik <kaushikk@vmware.com> 044-1
-   Updating Version.
