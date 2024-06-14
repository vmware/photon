%define container_selinux_ver   2.232.0
%define distro                  photon

Summary:        SELinux policy
Name:           selinux-policy
Version:        41.3
Release:        1%{?dist}
License:        GPLv2
Group:          System Environment/Libraries
Url:            https://github.com/SELinuxProject/selinux/wiki
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/fedora-selinux/selinux-policy/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512 %{name}=b58fe2a40608189c85f7addb4a3e59bb346c53e06b189dd71aad903aa38a01ffd525d26e2597e5885952ff01f33d224013bfa1e84668bcfa7b46e440884ba77e

Source1: https://github.com/containers/container-selinux/archive/container-selinux-%{container_selinux_ver}.tar.gz
%define sha512 container-selinux=30bdbd37682b89dce1e69e73dd66023f54b7d7f78b39ca6881f8735f7820b5a8d8fe2b04e12eb90bcb7e71fb3cd529ebd717f433164f198d4f1a4e6f48f8b4da

Source2: build.conf
Source3: modules.conf
Source4: macros.%{name}
Source5: config
Source6: users
Source7: patches.inc

%include %{SOURCE7}

BuildArch: noarch

BuildRequires: checkpolicy
BuildRequires: python3-devel
BuildRequires: semodule-utils
BuildRequires: libselinux-utils
BuildRequires: libselinux-devel
BuildRequires: policycoreutils

Requires: policycoreutils
Requires: coreutils-selinux
Requires: libselinux-utils

%description
Provides default Photon OS SELinux policy.

%package devel
Summary: SELinux policy devel
Requires: %{name} = %{version}-%{release}
Requires: m4
Requires: checkpolicy
Requires: selinux-python
Requires: semodule-utils
Requires: rpm-build
Requires: build-essential

%description devel
SELinux policy development

%prep
# Using autosetup is not feasible
%setup -q -b1 -n container-selinux-%{container_selinux_ver}
# Using autosetup is not feasible
%setup -q
cp -a ../container-selinux-%{container_selinux_ver}/container.* policy/modules/contrib/
%autopatch -p1

%build
cp %{SOURCE2} .
cp %{SOURCE3} %{SOURCE6} policy/

%make_build DISTRO=%{distro}

%install
%make_install %{?_smp_mflags} DISTRO=%{distro}
mkdir -p %{buildroot}%{_sharedstatedir}/selinux/default
# Use priority 100 instead of default 400
%make_install %{?_smp_mflags} \
  SEMODULE="%{_sbindir}/semodule -p %{buildroot} -X 100" load \
  DISTRO=%{distro}

%make_install %{?_smp_mflags} \
  install-headers \
  DISTRO=%{distro}

mkdir %{buildroot}%{_datadir}/selinux/devel
cp doc/Makefile.example %{buildroot}%{_datadir}/selinux/devel/Makefile
cp config/file_contexts.subs_dist %{buildroot}%{_sysconfdir}/selinux/default/contexts/files/
install -v -m644 %{SOURCE5} %{buildroot}%{_sysconfdir}/selinux/config

mkdir -p %{buildroot}%{_rpmmacrodir}
cp -p %{SOURCE4} %{buildroot}%{_rpmmacrodir}/

rel="$(echo %{release} | sed 's/\.[^.]*$//')"
sed -i "s/SELINUXPOLICYVERSION/%{version}-${rel}/" %{buildroot}%{_rpmmacrodir}/macros.%{name}
sed -i "s@SELINUXSTOREPATH@%{_sharedstatedir}/selinux@" %{buildroot}%{_rpmmacrodir}/macros.%{name}

%posttrans
if [ $1 -ge 0 ]; then
  %{_sbindir}/setfiles %{_sysconfdir}/selinux/default/contexts/files/file_contexts /
fi

%files
%defattr(-,root,root,-)
%dir %{_sysconfdir}/selinux/
%config(noreplace) %{_sysconfdir}/selinux/config
%{_sysconfdir}/selinux/default
%{_sharedstatedir}/selinux/default
%{_rpmmacrodir}/macros.%{name}

%files devel
%defattr(-,root,root,-)
%{_datadir}/selinux

%changelog
* Mon Jun 10 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 41.3-1
- Upgrade to v41.2
* Mon Jun 03 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 36.5-7
- Fix some denials
- Fix config file permission
* Mon Nov 06 2023 Shreenidhi Shedi <sshedi@vmware.com> 36.5-6
- Bump version as a part of rpm upgrade
* Tue Oct 24 2023 Shreenidhi Shedi <sshedi@vmware.com> 36.5-5
- Fix devel package requires
* Fri Feb 17 2023 Shivani Agarwal <shivania2@vmware.com> 36.5-4
- Added rpm macros and selinux policy for k8's watch denial message
* Fri Sep 16 2022 Shivani Agarwal <shivania2@vmware.com> 36.5-3
- Added selinux policy for k8's deployment with containerd
* Fri Sep 16 2022 Shreenidhi Shedi <sshedi@vmware.com> 36.5-2
- Bump version and fix build failure after libsepol upgrade
* Mon Mar 28 2022 Shreenidhi Shedi <sshedi@vmware.com> 36.5-1
- Upgrade to v36.5
* Tue Mar 22 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.14.8-4
- Fix some more AVC denials
* Wed Mar 16 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.14.8-3
- Fix passwd, shadow transitions
* Mon Mar 07 2022 Alexey Makhalov <amakhalov@vmware.com> 3.14.8-2
- Fix iptables and sshd issues
* Thu Aug 06 2020 Vikash Bansal <bvikas@vmware.com> 3.14.8-1
- Version Bump up to 3.14.8
* Thu Aug 06 2020 Vikash Bansal <bvikas@vmware.com> 3.14.6-1
- Version Bump up to 3.14.6
* Fri Jul 31 2020 Vikash Bansal <bvikas@vmware.com> 3.14.5-8
- Add support of rabbitmq module
- Fixed issue of accessing "ds-identify.log" by blkid
* Tue Jul 28 2020 Vikash Bansal <bvikas@vmware.com> 3.14.5-7
- Fix motgen "avc:denied" error and removed duplicate rules.
* Tue Jul 21 2020 Vikash Bansal <bvikas@vmware.com> 3.14.5-6
- Fix "avc:denied" errors for passwd and systemd-timesync
* Mon Jul 20 2020 Vikash Bansal <bvikas@vmware.com> 3.14.5-5
- Add support of cloudform & redis  module in modules.conf
* Wed Jul 15 2020 Vikash Bansal <bvikas@vmware.com> 3.14.5-4
- Added file_contexts.subs_dist
- This file is used to configure base path aliases
* Sun Jul 05 2020 Vikash Bansal <bvikas@vmware.com> 3.14.5-3
- Resolve "avc:  denied" errors
* Thu Jun 04 2020 Vikash Bansal <bvikas@vmware.com> 3.14.5-2
- Add coreutils-selinux in requires, needed for setting labels
* Fri Apr 24 2020 Alexey Makhalov <amakhalov@vmware.com> 3.14.5-1
- Initial build.
