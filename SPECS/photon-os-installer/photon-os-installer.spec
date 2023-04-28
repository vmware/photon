%global debug_package %{nil}

Summary:       Photon OS Installer
Name:          photon-os-installer
Version:       2.1
Release:       4%{?dist}
License:       Apache 2.0 and GPL 2.0
Group:         System Environment/Base
Vendor:        VMware, Inc.
Distribution:  Photon
URL:           https://github.com/vmware/photon-os-installer
Source0:       %{name}-%{version}.tar.gz
%define sha512 %{name}=16429b9b801b8bc57f6ded0a9bc0f45af49fd5e5449b9f3ab1fc25277c273899e8c45c6bd7774c65db399e9e6665419a77d266dc488d5b89177413a28f66e6f7
Patch0: 0001-create-abupdate.conf.patch
Patch1: 0002-installer.py-Set-default-value-of-live-to-True.patch
Patch2: 0003-isoInstaller.py-Raise-exception-in-case-installer-fa.patch
Patch3: 0004-generate_initrd.sh-Remove-rpmdb-files-from-the-insta.patch
Patch4: 0005-test.log-Remove-test.log.patch
Patch5: 0006-fix-a-few-network-issues.patch
Patch6: 0007-m_-postinstall-preinstall-.py-Fix-post-install-arbit.patch
Patch7: 0008-Update-isoInstaller.py.patch
Patch8: 0009-setup.py-Bump-up-version-to-2.1.patch
Patch9: 0010-photon-os-installer-Adding-docs-and-sample_ks-direct.patch
Patch10: 0011-installer.py-Code-cleanup.patch
Patch11: 0012-ostreeinstaller.py-Use-photon_release_version-from-i.patch
Patch12: 0013-Add-disk-size-percentages.patch
Patch13: 0014-add-network-examples.patch
Patch14: 0015-photon-os-installer-progressbar-Fix-installer-UI.patch
Patch15: 0016-installer-Fix-preinstall-dynamic-value-parsing.patch

BuildRequires: python3-devel
BuildRequires: python3-pyinstaller
BuildRequires: python3-requests
BuildRequires: python3-cracklib
BuildRequires: python3-curses

Requires: dosfstools
Requires: efibootmgr
Requires: glibc
Requires: gptfdisk
Requires: grub2
%ifarch x86_64
Requires: grub2-pc
%endif
Requires: kpartx
Requires: lvm2
Requires: zlib
Requires: cdrkit
Requires: findutils

%description
This is to create rpm for installer code

%prep
%autosetup -p1

%build
%py3_build

%install
%py3_install

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{python3_sitelib}/*
%{_bindir}/photon-installer
%{_bindir}/photon-iso-builder

%changelog
* Wed Mar 15 2023 Ankit Jain <ankitja@vmware.com> 2.1-4
- Sync with upstream
* Fri Mar 10 2023 Ankit Jain <ankitja@vmware.com> 2.1-3
- Sync with upstream
* Wed Mar 1 2023 Oliver Kurth <okurth@vmware.com> 2.1-2
- bug fixes
* Mon Feb 20 2023 Piyush Gupta <gpiyush@vmware.com> 2.1-1
- Upgrade to v2.1.
* Tue Nov 22 2022 Ankit Jain <ankitja@vmware.com> 2.0-8
- commandline parameter for mount retry of media
* Fri Nov 04 2022 Ankit Jain <ankitja@vmware.com> 2.0-7
- Added support for 'preinstall' scripts feature
* Sat Oct 29 2022 Ankit Jain <ankitja@vmware.com> 2.0-6
- fixes removal of 'photon_release_version' key
* Mon Oct 17 2022 Ankit Jain <ankitja@vmware.com> 2.0-5
- Added support for /dev/disk/by-path
- Removed 'insecure_installation' and 'photon_release_version' from ks
* Fri Aug 05 2022 Ankit Jain <ankitja@vmware.com> 2.0-4
- Added refresh_devices in retries if mount fails
* Wed Dec 22 2021 Shreenidhi Shedi <sshedi@vmware.com> 2.0-3
- Fix tdnf installroot commands
* Sat Dec 11 2021 Piyush Gupta <gpiyush@vmware.com> 2.0-2
- Display error screen in no block device attached.
* Wed Nov 24 2021 Piyush Gupta <gpiyush@vmware.com> 2.0-1
- Upgrade to 2.0.
* Tue Aug 17 2021 Piyush Gupta <gpiyush@vmware.com> 1.0-7
- Fix <Go Back> option in ostree server selector screen.
- Patch to add git commit hash along with version.
* Tue Feb 23 2021 Ankit Jain <ankitja@vmware.com> 1.0-6
- Update ostree release repo, point to 4.0
* Tue Feb 23 2021 Piyush Gupta <gpiyush@vmware.com> 1.0-5
- Added --releasever to tdnf install command
* Fri Feb 19 2021 Piyush Gupta <gpiyush@vmware.com> 1.0-4
- Listing block devices after user accepts license.
* Fri Jan 15 2021 Piyush Gupta <gpiyush@vmware.com> 1.0-3
- Generating PRNGs through secrets module.
* Wed Dec 16 2020 Prashant S Chauhan <psinghchauha@vmware.com> 1.0-2
- Add support for insecure_installation so that rpms can be
- served from untrusted https url
* Thu Aug 06 2020 Piyush Gupta <gpiyush@vmware.com> 1.0-1
- Initial photon installer for Photon OS.
