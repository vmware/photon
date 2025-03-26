%global debug_package %{nil}

Summary:       Photon OS Installer
Name:          photon-os-installer
Version:       2.7
Release:       2%{?dist}
Group:         System Environment/Base
Vendor:        VMware, Inc.
Distribution:  Photon
URL:           https://github.com/vmware/photon-os-installer
Source0:       %{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

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
Requires: tdnf >= 3.5.6

Requires: python3-pyOpenSSL
Requires: python3-requests
Requires: python3-cracklib
Requires: python3-curses
Requires: python3-PyYAML
Requires: python3-jc

%description
Installer to build Photon images

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
* Wed Dec 11 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.7-2
- Release bump for SRP compliance
* Fri May 24 2024 Ankit Jain <ankit-aj.jain@broadcom.com> 2.7-1
- Upgrade to v2.7
* Tue Dec 26 2023 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 2.4-3
- Bump up as part of python3-pyOpenSSL update
* Wed Oct 25 2023 Ankit Jain <ankitja@vmware.com> 2.4-2
- Fix tmpfs mount issue
* Mon Oct 09 2023 Oliver Kurth <okurth@vmware.com> 2.4-1
- Upgrade to v2.4
- Add missing requires.
* Tue Apr 18 2023 Ankit Jain <ankitja@vmware.com> 2.3-1
- Upgrade to v2.3
* Fri Apr 14 2023 Harinadh D <hdommaraju@vmware.com> 2.2-3
- cleanup vgs if exists any before installation
* Fri Apr 14 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.2-2
- Bump version as a part of zlib upgrade
* Fri Mar 10 2023 Ankit Jain <ankitja@vmware.com> 2.2-1
- Upgrade to v2.2
* Fri Mar 10 2023 Ankit Jain <ankitja@vmware.com> 2.1-3
- Sync with upstream
* Wed Mar 1 2023 Oliver Kurth <okurth@vmware.com> 2.1-2
- bug fixes
* Mon Feb 20 2023 Piyush Gupta <gpiyush@vmware.com> 2.1-1
- Upgrade to v2.1.
* Tue Feb 14 2023 Oliver Kurth <okurth@vmware.com> 2.0-18
- add patch to remove noacl option for mount
* Thu Feb 02 2023 Oliver Kurth <okurth@vmware.com> 2.0-17
- require grub-pc only for x86_64
* Wed Feb 01 2023 Oliver Kurth <okurth@vmware.com> 2.0-16
- add requires for tools needed to build image
* Fri Jan 27 2023 Tapas Kundu <tkundu@vmware.com> 2.0-15
- Update EULA for 5.0 Beta
* Fri Jan 20 2023 Him Kalyan Bordoloi <bordoloih@vmware.com> 2.0-14
- Remove depricated package linux-aws from installer
* Tue Jan 17 2023 Piyush Gupta <gpiyush@vmware.com> 2.0-13
- Upgrade ostree repo for 5.0.
* Tue Jan 10 2023 Piyush Gupta <gpiyush@vmware.com> 2.0-12
- Add support for custom iso and initrd.
* Wed Jan 04 2023 Tapas Kundu <tkundu@vmware.com> 2.0-11
- Update dist version in 0009-installer-Removed-insecure_installation-and-photon_r.patch
* Mon Jan 02 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 2.0-10
- Rebuild with new cracklib
* Tue Dec 06 2022 Piyush Gupta <gpiyush@vmware.com> 2.0-9
- Add missing commits from photon-os-installer repo.
- Fix installer.py: Parse string before passing to int().
* Wed Nov 30 2022 Prashant S Chauhan <psinghchauha@vmware.com> 2.0-8
- Update release to compile with python 3.11
* Tue Nov 29 2022 Ankit Jain <ankitja@vmware.com> 2.0-7
- Release Bump-Up to build with updated pyOpenSSL version
* Fri Nov 04 2022 Ankit Jain <ankitja@vmware.com> 2.0-6
- Added support for 'preinstall' scripts feature
* Sat Oct 29 2022 Ankit Jain <ankitja@vmware.com> 2.0-5
- fixes removal of 'photon_release_version' key
* Mon Oct 17 2022 Ankit Jain <ankitja@vmware.com> 2.0-4
- Added support for /dev/disk/by-path
- Removed 'insecure_installation' and 'photon_release_version' from ks
* Fri Aug 05 2022 Ankit Jain <ankitja@vmware.com> 2.0-3
- Added refresh_devices in retries if mount fails
* Wed Dec 22 2021 Shreenidhi Shedi <sshedi@vmware.com> 2.0-2
- Fix tdnf installroot commands
* Sat Dec 18 2021 Shreenidhi Shedi <sshedi@vmware.com> 2.0-1
- Bump version as a part of requests & chardet upgrade
* Tue Jun 01 2021 Piyush Gupta <gpiyush@vmware.com> 1.0-7
- Support for xen block device.
* Thu Mar 04 2021 Piyush Gupta <gpiyush@vmware.com> 1.0-6
- User specified mount media.
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
