Name:          nvme-cli
Summary:       NVM-Express user space tooling for Linux
Version:       2.3
Release:       2%{?dist}
Group:         Applications/System
Vendor:        VMware, Inc.
Distribution:  Photon
License:       GPLv2
URL:           https://github.com/linux-nvme/nvme-cli
Source0:       %{name}-%{version}.tar.gz
%define sha512 nvme-cli=9ef654e782ba737d3858fb11f24caf27aea820480179d07d32599731be204e52693062cdb86786ab5cdd1d94fe32ae9028baa0a58693d2eaee5a2b71155e3db2
BuildRequires: meson
BuildRequires: cmake
BuildRequires: libnvme-devel
BuildRequires: json-c-devel
BuildRequires: pkg-config
Requires: zlib
Requires: json-c
Requires: libnvme

Patch0: 0001-change-install-location-to-usr.patch

%description
NVM-Express user space tooling for Linux

%prep
%autosetup

%build
%meson
%meson_build

%install
%meson_install
rm -rf %{buildroot}%{_datadir}/zsh/*

%if 0%{?with_check}
%check
%meson_test
%endif

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/nvme/discovery.conf
%{_libdir}/dracut/dracut.conf.d/70-nvmf-autoconnect.conf
%{_unitdir}/*.service
%{_unitdir}/*.target
%{_udevrulesdir}/*.rules
%{_sbindir}/nvme
%{_datadir}/bash-completion/completions/nvme

%changelog
*  Fri Apr 14 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.3-2
-  Bump version as a part of zlib upgrade
*  Fri Mar 10 2023 Srish Srinivasan <ssrish@vmware.com> 2.3-1
-  Update to v2.3
-  Change install location from /usr/local to /usr
*  Tue Dec 13 2022 Gerrit Photon <photon-checkins@vmware.com> 2.2.1-1
-  Automatic Version Bump
*  Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 2.1.2-1
-  Automatic Version Bump
*  Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 2.0-1
-  Automatic Version Bump
*  Tue Apr 20 2021 Gerrit Photon <photon-checkins@vmware.com> 1.14-1
-  Automatic Version Bump
*  Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 1.13-1
-  Automatic Version Bump
*  Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 1.12-1
-  Automatic Version Bump
*  Mon Sep 10 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 1.6-1
-  Upgrade to 1.6
*  Thu Jul 26 2018 Ajay Kaher <akaher@vmware.com> 1.5-2
-  Resolved compilation error for aarch64
*  Thu Jun 14 2018 Anish Swaminathan <anishs@vmware.com> 1.5-1
-  Initial build.
