%global debug_package %{nil}
Summary:    Photon OS Installer
Name:       photon-os-installer
Version:    1.0
Release:    7%{?dist}
License:    Apache 2.0 and GPL 2.0
Group:      System Environment/Base
Vendor:     VMware, Inc.
Distribution:   Photon
URL:        https://github.com/vmware/photon-os-installer
Source0:    %{name}-%{version}.tar.gz
%define sha1 %{name}=cc86d22b7ef8495164fec1fb7d96bb97a2fb82c6
Patch0:     support_insecure_installation.patch
Patch1:     insecure_randomness.patch
Patch2:     list_block_devices.patch
Patch3:     releasever_tdnf_install.patch
Patch4:     0001-ostree-release-repo-Point-to-4.0.patch
Patch5:     ostreeserverselector.patch
Patch6:     add_version_with_git_commit_hash.patch
Patch7:     ITS_terminology_fix.patch
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
*   Tue Aug 17 2021 Piyush Gupta <gpiyush@vmware.com> 1.0-7
-   Fix <Go Back> option in ostree server selector screen.
-   Patch to add git commit hash along with version.
*   Tue Feb 23 2021 Ankit Jain <ankitja@vmware.com> 1.0-6
-   Update ostree release repo, point to 4.0
*   Tue Feb 23 2021 Piyush Gupta <gpiyush@vmware.com> 1.0-5
-   Added --releasever to tdnf install command
*   Fri Feb 19 2021 Piyush Gupta <gpiyush@vmware.com> 1.0-4
-   Listing block devices after user accepts license.
*   Fri Jan 15 2021 Piyush Gupta <gpiyush@vmware.com> 1.0-3
-   Generating PRNGs through secrets module.
*   Wed Dec 16 2020 Prashant S Chauhan <psinghchauha@vmware.com> 1.0-2
-   Add support for insecure_installation so that rpms can be
-   served from untrusted https url
*   Thu Aug 06 2020 Piyush Gupta <gpiyush@vmware.com> 1.0-1
-   Initial photon installer for Photon OS.
