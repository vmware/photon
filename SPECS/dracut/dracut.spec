%define dracutlibdir        %{_libdir}/%{name}
%global __requires_exclude  pkg-config

Summary:        dracut to create initramfs
Name:           dracut
Version:        059
Release:        11%{?dist}
Group:          System Environment/Base
# The entire source code is GPLv2+; except install/* which is LGPLv2+
License:        GPLv2+ and LGPLv2+
URL:            https://github.com/dracutdevs/dracut/wiki
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/dracutdevs/dracut/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512 %{name}=196bc8bf18703c72bffb51a7e0493719c58173ad2da7d121eb42f9a8de47e953af36d109214dc4a10b2dc2d3bd19e844f7f51c2bdec087e064ea11f75124032d

Patch0: 0001-Add-mkinitrd-support-to-dracut.patch
Patch1: 0002-disable-xattr.patch
Patch2: 0003-fix-initrd-naming-for-photon.patch
Patch4: 0004-fix-hostonly.patch
Patch5: 0005-mkinitrd-verbose-fix.patch
Patch6: 0006-dracut.sh-validate-instmods-calls.patch
Patch7: 0007-feat-dracut.sh-support-multiple-config-dirs.patch
Patch8: 0008-fix-dracut-systemd-rootfs-generator-cannot-write-out.patch
Patch9: 0009-install-systemd-executor.patch

BuildRequires:  bash
BuildRequires:  pkg-config
BuildRequires:  kmod-devel
BuildRequires:  asciidoc3
BuildRequires:  systemd-rpm-macros

Requires:       bash >= 4
Requires:       kmod
Requires:       sed
Requires:       grep
Requires:       xz
Requires:       gzip
Requires:       cpio
Requires:       filesystem
Requires:       util-linux
Requires:       findutils
Requires:       procps-ng
Requires:       systemd
Requires:       systemd-udev
Requires:       (coreutils or coreutils-selinux)

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

%build
%configure --systemdsystemunitdir=%{_unitdir} \
           --bashcompletiondir=$(pkg-config --variable=completionsdir bash-completion) \
           --libdir=%{_libdir} \
           --disable-documentation

%make_build

%install
%make_install %{?_smp_mflags} libdir=%{_libdir}

echo "DRACUT_VERSION=%{version}-%{release}" > %{buildroot}%{dracutlibdir}/%{name}-version.sh

rm -fr -- %{buildroot}%{dracutlibdir}/modules.d/01fips

# we do not support dash in the initramfs
rm -fr -- %{buildroot}%{dracutlibdir}/modules.d/00dash

# remove gentoo specific modules
rm -fr -- %{buildroot}%{dracutlibdir}/modules.d/96securityfs \
          %{buildroot}%{dracutlibdir}/modules.d/97masterkey \
          %{buildroot}%{dracutlibdir}/modules.d/98integrity

mkdir -p %{buildroot}/boot/%{name} \
         %{buildroot}%{_sharedstatedir}/%{name}/overlay \
         %{buildroot}%{_var}/log \
         %{buildroot}%{_var}/opt/%{name}/log \
         %{buildroot}%{_sharedstatedir}/initramfs \
         %{buildroot}%{_sbindir}

touch %{buildroot}%{_var}/opt/%{name}/log/%{name}.log
ln -srv %{buildroot}%{_var}/opt/%{name}/log/%{name}.log %{buildroot}%{_var}/log/

# create compat symlink
ln -srv %{buildroot}%{_bindir}/%{name} %{buildroot}%{_sbindir}/%{name}

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
%{dracutlibdir}/%{name}-util
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
%{_unitdir}/dracut-shutdown-onfailure.service
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
* Wed Jan 03 2024 Susant Sahani <susant.sahani@broadcom.com> 059-11
- Include systemd-executor if available
* Tue Oct 03 2023 Shreenidhi Shedi <sshedi@vmware.com> 059-10
- Add gzip, procps-ng, xz to requires
* Thu Jul 27 2023 Piyush Gupta <gpiyush@vmware.com> 059-9
- fix(dracut-systemd): rootfs-generator cannot write outside of generator dir
* Mon Jul 17 2023 Shreenidhi Shedi <sshedi@vmware.com> 059-8
- Fix a bug in finding installed kernel versions during mkinitrd
* Tue Apr 25 2023 Shreenidhi Shedi <sshedi@vmware.com> 059-7
- Code improvements in multiple conf dir support
* Sat Apr 1 2023 Laszlo Gombos <laszlo.gombos@gmail.com> 059-6
- Update wiki link and remove obsolete references
* Wed Mar 15 2023 Shreenidhi Shedi <sshedi@vmware.com> 059-5
- Add systemd-udev to requires
* Wed Mar 08 2023 Shreenidhi Shedi <sshedi@vmware.com> 059-4
- Add /etc/dracut.conf.d to conf dirs list during initrd creation
- Drop multiple conf file support
* Wed Mar 01 2023 Shreenidhi Shedi <sshedi@vmware.com> 059-3
- Fix mkinitrd verbose & add a sanity check
* Wed Jan 25 2023 Shreenidhi Shedi <sshedi@vmware.com> 059-2
- Fix requires
* Mon Jan 02 2023 Shreenidhi Shedi <sshedi@vmware.com> 059-1
- Upgrade to v059
* Wed Sep 28 2022 Shreenidhi Shedi <sshedi@vmware.com> 057-1
- Upgrade to v057
* Mon Jul 12 2021 Shreenidhi Shedi <sshedi@vmware.com> 055-1
- Upgrade to version 055
* Wed Jan 20 2021 Shreenidhi Shedi <sshedi@vmware.com> 050-7
- Added a command line option to manually override host_only
* Tue Dec 15 2020 Shreenidhi Shedi <sshedi@vmware.com> 050-6
- Adjust hostonly based on running environment
* Tue Nov 03 2020 Srinidhi Rao <srinidhir@vmware.com> 050-5
- Remove fipsify support
* Fri Oct 09 2020 Shreenidhi Shedi <sshedi@vmware.com> 050-4
- Fixed hostonly setting logic to generate initrd properly
* Mon Oct 05 2020 Susant Sahani <ssahani@vmware.com> 050-3
- Fix mkitnird and lsinitrd
* Sun Jun 21 2020 Tapas Kundu <tkundu@vmware.com> 050-2
- Use asciidoc3
* Fri Apr 24 2020 Susant Sahani <ssahani@vmware.com> 050-1
- Update to 050
* Fri Apr 03 2020 Vikash Bansal <bvikas@vmware.com> 048-4
- Added fips module
* Wed Apr 01 2020 Susant Sahani <ssahani@vmware.com> 048-3
- systemd: install systemd-tty-ask-password-agent systemd-ask-password
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
