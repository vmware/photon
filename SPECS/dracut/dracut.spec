%define dracutlibdir        %{_libdir}/%{name}
%global __requires_exclude  pkg-config

Summary:        dracut to create initramfs
Name:           dracut
Version:        050
Release:        11%{?dist}
Group:          System Environment/Base
# The entire source code is GPLv2+
# except install/* which is LGPLv2+
License:        GPLv2+ and LGPLv2+
URL:            https://github.com/dracutdevs/dracut/wiki
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://www.kernel.org/pub/linux/utils/boot/dracut/%{name}-%{version}.tar.xz
%define sha512 %{name}=eba046cf1c8013369a398e585e0bff233daa8595d469ce9acc8bbc6a32d55c6a5429d4219db19abbf6001104be05b357f0961f9e66b7f926039a5d3ee7c2b850

Patch0: 0001-disable-xattr.patch
Patch1: 0002-fix-initrd-naming-for-photon.patch
Patch2: 0003-lvm-no-read-only-locking.patch
Patch3: 0004-fix-hostonly.patch
Patch4: 0005-mkinitrd-verbose-fix.patch
Patch5: 0006-dracut.sh-validate-instmods-calls.patch
Patch6: 0007-feat-dracut.sh-support-multiple-config-dirs.patch

BuildRequires:  bash
BuildRequires:  pkg-config
BuildRequires:  kmod-devel
BuildRequires:  asciidoc3
BuildRequires:  systemd-devel

Requires:       bash >= 4
Requires:       (coreutils or coreutils-selinux)
Requires:       kmod
Requires:       util-linux
Requires:       systemd
Requires:       systemd-udev
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

rm -fr -- %{buildroot}%{dracutlibdir}/modules.d/01fips

# we do not support dash in the initramfs
rm -fr -- %{buildroot}/%{dracutlibdir}/modules.d/00dash

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
ln -sr %{buildroot}%{_bindir}/%{name} %{buildroot}%{_sbindir}/%{name}

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
* Fri Jul 14 2023 Shreenidhi Shedi <sshedi@vmware.com> 050-11
- Fix a bug in finding installed kernel versions during mkinitrd
* Mon Apr 03 2023 Shreenidhi Shedi <sshedi@vmware.com> 050-10
- Add /etc/dracut.conf.d to conf dirs list during initrd creation
- Update wiki link and remove obsolete references
* Tue Feb 07 2023 Shreenidhi Shedi <sshedi@vmware.com> 050-9
- Fix requires
* Mon Dec 06 2021 Ankit Jain <ankitja@vmware.com> 050-8
- Add systemd-udev as requires to successfully
- create initrd.img
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
