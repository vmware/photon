%define dracutlibdir        %{_libdir}/%{name}
%define _unitdir            %{_libdir}/systemd/system
%global __requires_exclude  pkg-config

Name:           dracut
Version:        048
Release:        9%{?dist}
Group:          System Environment/Base
# The entire source code is GPLv2+
# except install/* which is LGPLv2+
License:        GPLv2+ and LGPLv2+
URL:            https://dracut.wiki.kernel.org
Summary:        dracut to create initramfs
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://www.kernel.org/pub/linux/utils/boot/dracut/%{name}-%{version}.tar.xz
%define sha512 %{name}=97fcfd5d314ef40687c245d95d2f1d0f3f9ff0472e66b6e6324bf9bd6b98186104f9d71fd9af344126d6ea9fa47b744d52831a374225633225f6f17fb15c04e0

Patch0:         disable-xattr.patch
Patch1:         fix-initrd-naming-for-photon.patch
Patch2:         lvm-no-read-only-locking.patch
Patch3:         0001-fips-changes.patch
Patch4:         fix-hostonly.patch

BuildRequires:  bash
BuildRequires:  pkg-config
BuildRequires:  kmod-devel
BuildRequires:  asciidoc
BuildRequires:  systemd-devel

Requires:       bash >= 4
Requires:       coreutils
Requires:       kmod
Requires:       util-linux
Requires:       systemd
Requires:       /bin/sed
Requires:       /bin/grep
Requires:       findutils
Requires:       cpio

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
%autosetup -p1

%build
%configure \
   --systemdsystemunitdir=%{_unitdir} \
   --bashcompletiondir=$(pkg-config --variable=completionsdir bash-completion) \
   --libdir=%{_libdir} \
   --disable-documentation

%make_build

%install
%make_install %{?_smp_mflags} libdir=%{_libdir}

echo "DRACUT_VERSION=%{version}-%{release}" > %{buildroot}%{dracutlibdir}/%{name}-version.sh

rm -fr -- %{buildroot}%{dracutlibdir}/modules.d/02fips-aesni \
          %{buildroot}%{dracutlibdir}/modules.d/00bootchart

# we do not support dash in the initramfs
rm -fr -- %{buildroot}%{dracutlibdir}/modules.d/00dash

# remove gentoo specific modules
rm -fr -- %{buildroot}%{dracutlibdir}/modules.d/50gensplash \
          %{buildroot}%{dracutlibdir}/modules.d/96securityfs \
          %{buildroot}%{dracutlibdir}/modules.d/97masterkey \
          %{buildroot}%{dracutlibdir}/modules.d/98integrity

mkdir -p %{buildroot}/boot/%{name} \
          %{buildroot}%{_sharedstatedir}/%{name}/overlay \
          %{buildroot}%{_var}/log \
          %{buildroot}%{_var}/opt/%{name}/log \
          %{buildroot}%{_sharedstatedir}/initramfs \
          %{buildroot}%{_sbindir}

touch %{buildroot}%{_var}/opt/%{name}/log/%{name}.log
ln -sfrv %{_var}/opt/%{name}/log/%{name}.log %{buildroot}%{_var}/log/

rm -f %{buildroot}%{_mandir}/man?/*suse*

# create compat symlink
ln -sfrv %{buildroot}%{_bindir}/%{name} %{buildroot}%{_sbindir}/%{name}

%clean
rm -rf -- %{buildroot}

%files
%defattr(-,root,root,0755)
%{_bindir}/%{name}
%{_bindir}/mkinitrd
%{_bindir}/lsinitrd
# compat symlink
%{_sbindir}/%{name}
%{_datadir}/bash-completion/completions/%{name}
%{_datadir}/bash-completion/completions/lsinitrd
%dir %{dracutlibdir}
%dir %{dracutlibdir}/modules.d
%{dracutlibdir}/modules.d/*
%exclude %{_libdir}/kernel
%{_libdir}/%{name}/%{name}-init.sh
%{_datadir}/pkgconfig/%{name}.pc
%{dracutlibdir}/%{name}-functions.sh
%{dracutlibdir}/%{name}-functions
%{dracutlibdir}/%{name}-version.sh
%{dracutlibdir}/%{name}-logger.sh
%{dracutlibdir}/%{name}-initramfs-restore
%{dracutlibdir}/%{name}-install
%{dracutlibdir}/skipcpio
%config(noreplace) %{_sysconfdir}/%{name}.conf
%dir %{_sysconfdir}/%{name}.conf.d
%dir %{dracutlibdir}/%{name}.conf.d
%dir %{_var}/opt/%{name}/log
%attr(0644,root,root) %ghost %config(missingok,noreplace) %{_var}/opt/%{name}/log/%{name}.log
%{_var}/log/%{name}.log
%dir %{_sharedstatedir}/initramfs
%{_unitdir}/%{name}-shutdown.service
%{_unitdir}/sysinit.target.wants/%{name}-shutdown.service
%{_unitdir}/%{name}-cmdline.service
%{_unitdir}/%{name}-initqueue.service
%{_unitdir}/%{name}-mount.service
%{_unitdir}/%{name}-pre-mount.service
%{_unitdir}/%{name}-pre-pivot.service
%{_unitdir}/%{name}-pre-trigger.service
%{_unitdir}/%{name}-pre-udev.service
%{_unitdir}/initrd.target.wants/%{name}-cmdline.service
%{_unitdir}/initrd.target.wants/%{name}-initqueue.service
%{_unitdir}/initrd.target.wants/%{name}-mount.service
%{_unitdir}/initrd.target.wants/%{name}-pre-mount.service
%{_unitdir}/initrd.target.wants/%{name}-pre-pivot.service
%{_unitdir}/initrd.target.wants/%{name}-pre-trigger.service
%{_unitdir}/initrd.target.wants/%{name}-pre-udev.service

%files tools
%defattr(-,root,root,0755)
%{_bindir}/%{name}-catimages
%dir /boot/%{name}
%dir %{_sharedstatedir}/%{name}
%dir %{_sharedstatedir}/%{name}/overlay

%changelog
* Tue Feb 07 2023 Shreenidhi Shedi <sshedi@vmware.com> 048-9
- Fix requires
* Thu Jun 30 2022 Shreenidhi Shedi <sshedi@vmware.com> 048-8
- Don't create orpan debug file under kernel modules directory
- This was getting created by 0001-fips-changes.patch
* Fri Feb 11 2022 Ajay Kaher <akaher@vmware.com> 048-7
- Fix mount_boot()
* Tue Jan 19 2021 Shreenidhi Shedi <sshedi@vmware.com> 048-6
- Added a command line option to manually override host_only
* Wed Dec 23 2020 Vikash Bansal <bvikas@vmware.com> 048-5
- Fix for processors which don't support AESNI
* Wed Dec 23 2020 Shreenidhi Shedi <sshedi@vmware.com> 048-4
- Adjust hostonly based on running environment
* Tue Jan 28 2020 Vikash Bansal <bvikas@vmware.com> 048-3
- Added fips module
* Thu Oct 10 2019 Alexey Makhalov <amakhalov@vmware.com> 048-2
- lvm.conf: Do not set read-only locking.
* Mon Oct 01 2018 Alexey Makhalov <amakhalov@vmware.com> 048-1
- Version update
* Thu Dec 28 2017 Divya Thaluru <dthaluru@vmware.com>  045-6
- Fixed the log file directory structure
* Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 045-5
- Requires coreutils/util-linux/findutils or toybox,
    /bin/grep, /bin/sed
* Fri Jun 23 2017 Xiaolin Li <xiaolinl@vmware.com> 045-4
- Add kmod-devel to BuildRequires
* Fri May 26 2017 Bo Gan <ganb@vmware.com> 045-3
- Fix dependency
* Thu Apr 27 2017 Bo Gan <ganb@vmware.com> 045-2
- Disable xattr for cp
* Wed Apr 12 2017 Chang Lee <changlee@vmware.com> 045-1
- Updated to 045
* Wed Jan 25 2017 Harish Udaiya Kumar <hudaiyakumr@vmware.com> 044-6
- Added the patch for bash 4.4 support.
* Wed Nov 23 2016 Anish Swaminathan <anishs@vmware.com>  044-5
- Add systemd initrd root device target to list of modules
* Fri Oct 07 2016 ChangLee <changlee@vmware.com> 044-4
- Modified %check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 044-3
- GA - Bump release of all rpms
* Mon Apr 25 2016 Gengsheng Liu <gengshengl@vmware.com> 044-2
- Fix incorrect systemd directory.
* Thu Feb 25 2016 Kumar Kaushik <kaushikk@vmware.com> 044-1
- Updating Version.
