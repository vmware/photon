Name:           kpatch
Summary:        Dynamic kernel patching
Version:        0.9.8
Release:        5%{?dist}
URL:            http://github.com/dynup/kpatch
Group:          System Environment/Kernel
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/dynup/kpatch/archive/refs/tags/kpatch-v%{version}.tar.gz

Source1:        scripts/auto_livepatch.sh
Source2:        scripts/gen_livepatch.sh
Source3:        scripts/README.txt
Source4:        scripts/rpm/spec.file

Source5: license.txt
%include %{SOURCE5}

BuildArch:      x86_64

Patch0:         0001-Added-support-for-Photon-OS.patch
Patch1:         0001-adding-option-to-set-description-field-of-module.patch
Patch2:         0001-allow-livepatches-to-be-visible-to-modinfo-after-loa.patch

# Bug fix
Patch3:         kpatch-build-ignore-init-version-timestamp-o.patch

# Compatibility with linux-secure->linux merger
Patch4:         0001-create-diff-object-support-x86-NOP-padded-functions.patch
Patch5:         0002-kpatch-compatibility-with-Photon-gcc-RAP-patch.patch
Patch6:         0003-patch-hook-fix-cast-errors.patch

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
mkdir -p %{buildroot}%{_sysconfdir}/{auto_livepatch/dockerfiles,gen_livepatch}
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
%exclude %{_bindir}/auto_livepatch.sh
%exclude %{_bindir}/gen_livepatch.sh
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
* Mon Apr 28 2025 Tapas Kundu <tapas.kundu@broadcom.com> 0.9.8-5
- Do not need xml-security-c for building kernel
* Wed Dec 11 2024 Mukul Sikka <mukul.sikka@broadcom.com> 0.9.8-4
- Release bump for SRP compliance
* Wed Dec 4 2024 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 0.9.8-3
- Patches for compatibility after linux-secure->linux merger
* Fri Nov 22 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.9.8-2
- Bump up as part of docker upgrade
* Fri Mar 24 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 0.9.8-1
- Update to 0.9.8
* Wed Feb 15 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 0.9.7-4
- Add support for future Photon versions, including 5.0
* Sun Feb 12 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.9.7-3
- Fix requires
* Fri Jan 06 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 0.9.7-2
- Bump up due to change in elfutils
* Thu Dec 15 2022 Brennan Lamoreaux <blamoreaux@vmware.com> 0.9.7-1
- Update to latest version
* Thu Aug 25 2022 Brennan Lamoreaux <blamoreaux@vmware.com> 0.9.6-5
- Add a patch to make installed livepatches visible to modinfo.
- Add capability of packaging livepatch modules as RPMs.
* Mon Aug 22 2022 Brennan Lamoreaux <blamoreaux@vmware.com> 0.9.6-4
- Fix issue where description file was being copied into container at all times.
* Mon Aug 15 2022 Brennan Lamoreaux <blamoreaux@vmware.com> 0.9.6-3
- Adding option both in kpatch-utils scripts and kpatch-build itself for
- setting the description field of a livepatch module.
* Tue Jun 28 2022 Brennan Lamoreaux <blamoreaux@vmware.com> 0.9.6-2
- Adding automatic livepatch generating utilities as subpackage
- Adding more dependencies that are needed. Moved some from the kpatch-build
- patch to just kpatch-build requires section. Moved the installation of
- kernel build dependencies from after extraction of src rpm to before.
* Tue May 24 2022 Brennan Lamoreaux <blamoreaux@vmware.com> 0.9.6-1
- Initial addition to photon. Modified from provided kpatch.spec on GitHub.
