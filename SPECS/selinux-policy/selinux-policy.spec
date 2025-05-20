%define container_selinux_ver   2.181.0

Summary:        SELinux policy
Name:           selinux-policy
Version:        36.5
Release:        10%{?dist}
Group:          System Environment/Libraries
Url:            https://github.com/SELinuxProject/selinux/wiki
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/fedora-selinux/selinux-policy/archive/refs/tags/%{name}-%{version}.tar.gz

Source1: https://github.com/containers/container-selinux/archive/container-selinux-%{container_selinux_ver}.tar.gz

Source2:        build.conf
Source3:        modules.conf
Source4:        macros.%{name}
Source5:        config

Source6: license.txt
%include %{SOURCE6}

Patch0: 0001-contrib-container.patch
Patch1: 0002-contrib-cron.patch
Patch2: 0003-contrib-dbus.patch
Patch3: 0004-contrib-virt.patch
Patch4: 0005-kernel-storage.patch
Patch5: 0006-roles-staff.patch
Patch6: 0007-roles-unprivuser.patch
Patch7: 0008-motd_t-new-domain-for-motdgen.patch
Patch8: 0009-system-getty.patch
Patch9: 0010-system-init.patch
Patch10: 0011-system-logging.patch
Patch11: 0012-system-modutils.patch
Patch12: 0013-system-systemd.patch
Patch13: 0014-system-sysnetwork.patch
Patch14: 0015-system-udev.patch
Patch15: 0016-system-userdomain.patch
Patch16: 0017-admin_usermanage.patch
Patch17: 0018-system-fstool.patch
Patch18: 0019-iptables-allow-kernel_t-fifo_files.patch
Patch19: 0020-authlogin.if-add-transition-rules-for-shadow-group-p.patch
Patch20: 0021-allow-lvm_t-to-transit-to-unconfined_t.patch
Patch21: 0022-fix-fc-conflicts.patch
Patch22: 0023-Fix-AVC-denials-based-on-package-test-results.patch
Patch23: 0024-Fix-kubernetes-denials-for-K8-s-deployment-with-cont.patch
Patch24: 0025-Fix-bin-denials-for-K8-s-deployment-with-containerd.patch
Patch25: 0026-Fix-etcd-denials-for-K8-s-deployment-with-containerd.patch
Patch26: 0027-Fix-systemd-gpt-denials-for-K8-s-deployment.patch
Patch27: 0028-Fix-kubernetes-watch-denials-for-K8-deployment.patch.patch
Patch28: 0029-ssh-denial-fix.patch
Patch29: 0030-syslog-denial-fix.patch
Patch30: 0031-systemd_gpt_generator-denial-fix.patch
Patch31: 0032-systemd_userdbd-denial-fix.patch
Patch32: 0033-fix-getty_t-denial.patch
Patch33: 0034-fix-local_login_t-denial.patch
Patch34: 0035-allow-alg_socket-for-sshd.patch
Patch35: 0036-authlogin.te-fix-pwhistory-denial.patch
Patch36: 0037-systemd-init_t-denial.patch

BuildArch:      noarch

BuildRequires: checkpolicy
BuildRequires: python3-devel
BuildRequires: semodule-utils
BuildRequires: libselinux-utils
BuildRequires: libselinux-devel
BuildRequires: policycoreutils

Requires: policycoreutils
Requires: coreutils >= 9.1-10
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
%setup -q -b 1 -n container-selinux-%{container_selinux_ver}
# Using autosetup is not feasible
%setup -q
cp -r ../container-selinux-%{container_selinux_ver}/container.* policy/modules/contrib/
%autopatch -p1

%build
cp %{SOURCE2} .
cp %{SOURCE3} policy/
%make_build

%install
%make_install %{?_smp_mflags}
mkdir -p %{buildroot}%{_sharedstatedir}/selinux/default
# Use priority 100 instead of default 400
%make_install %{?_smp_mflags} SEMODULE="%{_sbindir}/semodule -p %{buildroot} -X 100" load
%make_install %{?_smp_mflags} install-headers
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
* Fri May 09 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 36.5-10
- Require coreutils only
* Wed Dec 11 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 36.5-9
- Release bump for SRP compliance
* Mon Jun 10 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 36.5-8
- Fix sshd and audit_control denials
* Mon Jun 03 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 36.5-7
- Fix config file permission
* Fri May 17 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 36.5-6
- Fix some denials
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
