%global debug_package %{nil}

Summary:       Photon OS Installer
Name:          photon-os-installer
Version:       2.7
Release:       4%{?dist}
License:       Apache 2.0 and GPL 2.0
Group:         System Environment/Base
Vendor:        VMware, Inc.
Distribution:  Photon
URL:           https://github.com/vmware/photon-os-installer
Source0:       %{name}-%{version}.tar.gz
%define sha512 %{name}=9c2b6df1e9136e94db1451064b51a286b2894849b309dde9539cb9df4fc82e807c74ccb0f7795d7d1d5b2c1ea856dfb38623e1c08e94c567696a637ca6f75fe8

Patch0: 0001-photon-os-installer-Fix-copytree-compatiblity-issue.patch
Patch1: 0001-installer.py-fix-df-command-parsing.patch

BuildRequires: python3-devel
BuildRequires: python3-pyinstaller
BuildRequires: python3-requests
BuildRequires: python3-cracklib
BuildRequires: python3-curses
BuildRequires: python3-jc

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
# needed for --rpmdefine option
Requires: tdnf >= 3.3.11-2

Requires: python3-pyOpenSSL
Requires: python3-requests
Requires: python3-cracklib
Requires: python3-curses
Requires: python3-PyYAML
Requires: python3-jc

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
* Fri Aug 30 2024 Ankit Jain <ankit-aj.jain@broadcom.com> 2.7-4
- Added a none check while parsing df output
* Tue Aug 27 2024 Ankit Jain <ankit-aj.jain@broadcom.com> 2.7-3
- Fix 'df' command parsing by 'jc'
* Fri Aug 09 2024 Ankit Jain <ankit-aj.jain@broadcom.com> 2.7-2
- Fix copytree() for old python version
* Fri May 24 2024 Ankit Jain <ankit-aj.jain@broadcom.com> 2.7-1
- Upgrade to v2.7
* Wed Oct 25 2023 Ankit Jain <ankitja@vmware.com> 2.4-2
- Fix tmpfs mount issue
* Tue Oct 17 2023 Piyush Gupta <gpiyush@vmware.com> 2.4-1
- Upgrade to v2.4.
- Add missing requires.
* Tue Jul 04 2023 Ankit Jain <ankitja@vmware.com> 2.3-3
- Fix for file based repo in container
* Fri Jun 30 2023 Ankit Jain <ankitja@vmware.com> 2.3-2
- Sync with upstream
* Tue May 02 2023 Ankit Jain <ankitja@vmware.com> 2.3-1
- Sync with upstream
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
