Name:           kpatch
Summary:        Dynamic kernel patching
Version:        0.9.8
Release:        3%{?dist}
URL:            http://github.com/dynup/kpatch
License:        GPLv2
Group:          System Environment/Kernel
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/dynup/kpatch/archive/refs/tags/%{name}-v%{version}.tar.gz
%define sha512  %{name}=ab3a771dfcde92a9eee768afcf7fddb6f1ad5ba9e8c7f44d579d258ce9b6ee1722869b1b70c4597ae951b0faf71413efa26a5b135f50308c996b284a9dcee5b7

Source1:        scripts/auto_livepatch.sh
Source2:        scripts/gen_livepatch.sh
Source3:        scripts/README.txt
Source4:        scripts/rpm/spec.file

BuildArch:      x86_64

Patch0:         0001-Added-support-for-Photon-OS.patch
Patch1:         0001-adding-option-to-set-description-field-of-module.patch
Patch2:         0001-allow-livepatches-to-be-visible-to-modinfo-after-loa.patch

# Bug fix
Patch3:         kpatch-build-ignore-init-version-timestamp-o.patch
Patch4:         0001-Support-multiline-MODULE_DESCRIPTION.patch

BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  elfutils
BuildRequires:  elfutils-devel
BuildRequires:  systemd-rpm-macros

Requires:       kmod
Requires:       bash
Requires:       rpm-build
Requires:       (coreutils or coreutils-selinux)
Requires:       gawk
Requires:       util-linux
Requires:       binutils
Requires:       sed
Requires:       findutils

%description
Contains the kpatch utility, which allows loading of kernel livepatches.
kpatch is a Linux dynamic kernel patching tool which allows you to patch a
running kernel without rebooting or restarting any processes.  It enables
sysadmins to apply critical security patches to the kernel immediately, without
having to wait for long-running tasks to complete, users to log off, or
for scheduled reboot windows.  It gives more control over up-time without
sacrificing security or stability.

%package build
Requires: %{name} = %{version}-%{release}
Requires: build-essential
Requires: tar
Requires: curl
Summary: Dynamic kernel patching

%description build
Contains the kpatch-build tool, to enable creation of kernel livepatches.

%package devel
Summary: Development files for kpatch

%description devel
Contains files for developing with kpatch.

%package utils
Requires: %{name} = %{version}-%{release}
Requires: %{name}-build = %{version}-%{release}
Requires: docker
Summary: Tools to automate livepatch building.

%description utils
Contains auto_livepatch and gen_livepatch scripts.

%prep
%autosetup -p1

%build
%make_build

%install
%make_install PREFIX=%{_usr} %{?_smp_mflags}
mkdir -p %{buildroot}%{_sysconfdir}/{auto_livepatch,gen_livepatch}
cp %{SOURCE1} %{SOURCE2} %{buildroot}%{_bindir}
cp %{SOURCE3} %{buildroot}%{_sysconfdir}/auto_livepatch
cp %{SOURCE4} %{buildroot}%{_sysconfdir}/gen_livepatch/build-rpm.spec

%files
%defattr(-,root,root,-)
%{_sbindir}/kpatch
%{_unitdir}/*
%config(noreplace) %{_sysconfdir}/init/kpatch.conf

%files build
%defattr(-,root,root,-)
%exclude %{_bindir}/{auto_livepatch.sh,gen_livepatch.sh}
%{_bindir}/*
%{_libexecdir}/*
%{_datadir}/%{name}

%files devel
%defattr(-,root,root,-)
%{_mandir}/man1/kpatch-build.1*
%{_mandir}/man1/kpatch.1*

%files utils
%defattr(-,root,root,-)
%doc %{_sysconfdir}/auto_livepatch/README.txt
%{_bindir}/auto_livepatch.sh
%{_bindir}/gen_livepatch.sh
%{_sysconfdir}/gen_livepatch/build-rpm.spec

%changelog
* Thu Apr 10 2025 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 0.9.8-3
- Limit auto generated livepatch kernel module name to 38 characters
- Added support for multiline module descriptions
- Removed redirection of stderr to /dev/null
* Sat Apr 29 2023 Harinadh D <hdommaraju@vmware.com> 0.9.8-2
- Fix for requires
* Mon Apr 24 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 0.9.8-1
- Update to 0.9.8, consume latest scripts
* Tue Feb 21 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 0.9.7-1
- Update to latest version and add support for Photon 5.0
* Mon Sep 12 2022 Brennan Lamoreaux <blamoreaux@vmware.com> 0.9.6-3
- Adding option to package livepatch modules as rpm.
- Adding patch to enable modinfo to find livepatch modules.
* Mon Aug 15 2022 Brennan Lamoreaux <blamoreaux@vmware.com> 0.9.6-2
- Adding option both in kpatch-utils scripts and kpatch-build itself for
- setting the description field of a livepatch module.
* Tue Jun 28 2022 Brennan Lamoreaux <blamoreaux@vmware.com> 0.9.6-1
- Initial addition to photon. Modified from provided kpatch.spec on GitHub.
- Adding automated livepatch generating tools as subpackage kpatch-utils
