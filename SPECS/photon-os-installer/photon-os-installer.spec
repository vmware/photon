%global debug_package %{nil}

Summary:    Photon OS Installer
Name:       photon-os-installer
Version:    2.0
Release:    6%{?dist}
License:    Apache 2.0 and GPL 2.0
Group:      System Environment/Base
Vendor:     VMware, Inc.
Distribution:   Photon
URL:        https://github.com/vmware/photon-os-installer

Source0:    %{name}-%{version}.tar.gz
%define sha512 %{name}=3a7567802a6b94cf9e51fcaaab5d2dbfbc42cd1d92427a2b0739a9df9994df01a2eb81e3133832fd39d575376ecf859451a8a3049d6993a42861544de9b4f3fe

Patch0:     error_screen_selectdisk.patch
Patch1:     fix-installroot-commands.patch
Patch2:     0001-isoInstaller-Refresh-devices-in-retries-if-mount-fai.patch
Patch3:     0001-installer-Adding-support-for-dev-disk-by-path.patch
Patch4:     0001-installer-Removed-insecure_installation-and-photon_r.patch
Patch5:     0001-photon-installer-fixes-remove-photon_release_version.patch
Patch6:     0001-installer-Adding-support-for-preinstall-script.patch

BuildRequires: python3-devel
BuildRequires: python3-pyinstaller
BuildRequires: python3-requests
BuildRequires: python3-cracklib
BuildRequires: python3-curses

Requires:      zlib
Requires:      glibc

%description
This is to create rpm for installer code

%prep
%autosetup -p1

%build
pyinstaller --onefile photon-installer.spec

%install
mkdir -p %{buildroot}%{_bindir}
cp dist/photon-installer %{buildroot}%{_bindir}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/photon-installer

%changelog
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
