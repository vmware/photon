Name:           kpatch
Summary:        Dynamic kernel patching
Version:        0.9.10
Release:        2%{?dist}
URL:            http://github.com/dynup/kpatch
Group:          System Environment/Kernel
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/dynup/kpatch/archive/refs/tags/kpatch-v%{version}.tar.gz

Source1:        utils/auto_livepatch
Source2:        utils/gen_livepatch
Source3:        utils/livepatch.sh
Source4:        utils/README.txt
Source5:        utils/rpm/livepatch_spec.template
Source6:        utils/Dockerfile.ph5
Source7:        utils/Dockerfile.ph4
Source8:        utils/Dockerfile.ph3

Source9:        license.txt
%include %{SOURCE9}

BuildArch:      x86_64

Patch0:         0001-adding-option-to-set-description-field-of-module.patch
# Compatibility with linux-secure->linux merger
Patch1:         0002-kpatch-compatibility-with-Photon-gcc-RAP-patch.patch
Patch2:         0003-patch-hook-fix-cast-errors.patch

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
Summary: Dynamic kernel patching
Requires: %{name} = %{version}-%{release}
Requires: build-essential
Requires: tar
Requires: curl

%description build
Contains the kpatch-build tool, to enable creation of kernel livepatches.

%package devel
Summary: Development files for kpatch

%description devel
Contains files for developing with kpatch.

%package utils
Summary: Tools to automate livepatch building.
Requires: %{name} = %{version}-%{release}
Requires: %{name}-build = %{version}-%{release}
Requires: docker
Requires: docker-buildx
Requires: wget

%description utils
Contains auto_livepatch and gen_livepatch scripts.

%prep
%autosetup -p1

%build
%make_build

%install
%make_install PREFIX=%{_usr} %{?_smp_mflags}
install -vdm755 %{buildroot}%{_datadir}/livepatch/dockerfiles/
cp %{SOURCE1} %{SOURCE2} %{buildroot}%{_bindir}
cp %{SOURCE3} %{buildroot}%{_libdir}
cp %{SOURCE4} %{SOURCE5} %{buildroot}%{_datadir}/livepatch
cp %{SOURCE6} %{SOURCE7} %{SOURCE8} %{buildroot}%{_datadir}/livepatch/dockerfiles

%files
%defattr(-,root,root,-)
%{_sbindir}/kpatch
%{_unitdir}/*
%config(noreplace) %{_sysconfdir}/init/kpatch.conf

%files build
%defattr(-,root,root,-)
%exclude %{_bindir}/auto_livepatch
%exclude %{_bindir}/gen_livepatch
%exclude %{_libdir}/livepatch.sh
%{_bindir}/*
%{_libexecdir}/*
%{_datadir}/%{name}

%files devel
%defattr(-,root,root,-)
%{_mandir}/man1/kpatch-build.1*
%{_mandir}/man1/kpatch.1*

%files utils
%defattr(0755,root,root,0755)
%{_bindir}/auto_livepatch
%{_bindir}/gen_livepatch
%{_libdir}/livepatch.sh
%defattr(0644,root,root,0755)
%doc %{_datadir}/livepatch/README.txt
%{_datadir}/livepatch/livepatch_spec.template
%{_datadir}/livepatch/dockerfiles/Dockerfile.ph5
%{_datadir}/livepatch/dockerfiles/Dockerfile.ph4
%{_datadir}/livepatch/dockerfiles/Dockerfile.ph3

%changelog
* Wed Jun 18 2025 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 0.9.10-2
- Bug fixes
- Various code improvements
* Tue May 13 2025 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 0.9.10-1
- upgrade to 0.9.10 to get latest fixes upstream by Photon
- Allow non-root users in the docker group to run the autolive patch script
- Moved common functions to livepatch.sh
- Enhanced cleanup function
- Switched from docker build to docker buildx
- Included a static Dockerfile instead of generating it dynamically in the script
- Improved help message
- Various code improvements
* Wed May 07 2025 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 0.9.8-6
- Improve multiline descriptions
* Thu Apr 10 2025 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 0.9.8-5
- Limit auto generated livepatch kernel module name to 38 characters
- Added support for multiline module descriptions
- Removed redirection of stderr to /dev/null
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
