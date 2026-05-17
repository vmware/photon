%global build_if %{photon_subrelease} >= 91

%define container_selinux_ver   2.247.0

Summary:        SELinux policy
Name:           selinux-policy
Version:        43.6
Release:        3%{?dist}
Group:          System Environment/Libraries
Url:            https://github.com/SELinuxProject/selinux/wiki
Vendor:         VMware, Inc.
Distribution:   Photon

BuildArch:      noarch

# Upstream GitHub tags use a leading v; the URL fragment after #/ sets the
# basename saved under SOURCES (selinux-policy-VERSION.tar.gz, etc.).
Source0: https://github.com/fedora-selinux/selinux-policy/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

Source1: https://github.com/containers/container-selinux/archive/refs/tags/v%{container_selinux_ver}.tar.gz#/container-selinux-%{container_selinux_ver}.tar.gz

Source2:        build.conf
Source3:        modules.conf
Source4:        macros.%{name}
Source5:        config

Source6: license.txt
%include %{SOURCE6}

Patch0: 0001-contrib-container.patch
Patch1: 0002-contrib-cron.patch
Patch2: 0003-contrib-virt.patch
Patch3: 0004-kernel-storage.patch
Patch4: 0005-roles-staff.patch
Patch5: 0006-roles-unprivuser.patch
Patch6: 0007-motd_t-new-domain-for-motdgen.patch
Patch7: 0008-system-getty.patch
Patch8: 0009-system-init.patch
Patch9: 0010-system-logging.patch
Patch10: 0011-system-modutils.patch
Patch11: 0012-system-systemd.patch
Patch12: 0013-system-sysnetwork.patch
Patch13: 0014-system-udev.patch
Patch14: 0015-system-userdomain.patch
Patch15: 0016-admin_usermanage.patch
Patch16: 0017-system-fstool.patch
Patch17: 0018-iptables-allow-kernel_t-fifo_files.patch
Patch18: 0019-authlogin.if-add-transition-rules-for-shadow-group-p.patch
Patch19: 0020-allow-lvm_t-to-transit-to-unconfined_t.patch
Patch20: 0021-fix-fc-conflicts.patch
Patch21: 0022-Fix-AVC-denials-based-on-package-test-results.patch
Patch22: 0023-Fix-kubernetes-denials-for-K8-s-deployment-with-cont.patch
Patch23: 0024-Fix-bin-denials-for-K8-s-deployment-with-containerd.patch
Patch24: 0025-Fix-etcd-denials-for-K8-s-deployment-with-containerd.patch
Patch25: 0026-Fix-systemd-gpt-denials-for-K8-s-deployment.patch
Patch26: 0027-Fix-kubernetes-watch-denials-for-K8-deployment.patch.patch
Patch27: 0028-ssh-denial-fix.patch
Patch28: 0029-syslog-denial-fix.patch
Patch29: 0030-systemd_gpt_generator-denial-fix.patch
Patch30: 0031-fix-getty_t-denial.patch
Patch31: 0032-fix-local_login_t-denial.patch
Patch32: 0033-domain-use-openssl-alg-socket-interface.patch
Patch33: 0034-authlogin.te-fix-pwhistory-denial.patch
Patch34: 0035-systemd-init_t-denial.patch
Patch35: 0036-Add-motd-rules-to-fix-denials.patch
Patch36: 0037-selinuxutil-restorecon-setfiles_mac_t-transition-for-unconfined_t.patch
Patch37: 0038-ssh-sshd_t-chkpwd_t-noatsecure-rlimitinh-siginh.patch
Patch38: 0039-corenetwork-syslog_tls-add-tcp-1514.patch
Patch39: 0040-drop-xserver-module.patch
Patch40: 0041-container-install_t-optional.patch
Patch41: 0042-mount-unconfined_r-mount_roles.patch

BuildRequires: checkpolicy
BuildRequires: python3-devel
BuildRequires: semodule-utils
BuildRequires: libselinux-utils
BuildRequires: libselinux-devel
BuildRequires: policycoreutils

Requires: policycoreutils
Requires: coreutils-selinux
Requires: libselinux-utils

# For automatic file labeling during an RPM transaction
Requires: rpm-plugin-selinux

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
  # Load the policy we just installed before setfiles; otherwise the kernel
  # still has the old policy and new file_contexts types (e.g. kubelet_exec_t)
  # are rejected as invalid.
  # selinuxenabled handles offline and sandboxed environments.
  %{_sbindir}/selinuxenabled && %{_sbindir}/load_policy || :
  %{_sbindir}/setfiles %{_sysconfdir}/selinux/default/contexts/files/file_contexts /
fi
exit 0

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
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 43.6-3
- Extended to build for subrelease 91 and above
* Thu Apr 23 2026 Alexey Makhalov <alexey.makhalov@broadcom.com> 43.6-2
- Allow file labeling from interactive shell (unconfined domain)
- mount: roleattribute unconfined_r mount_roles (rootless containerd mount exec)
* Mon Apr 20 2026 Alexey Makhalov <alexey.makhalov@broadcom.com> 43.6-1
- Upgrade to fedora-selinux/selinux-policy v43.6 and container-selinux v2.247.0
- Run load_policy in %%posttrans before setfiles
- Remove xserver policy module from modules.conf
* Mon Apr 06 2026 Alexey Makhalov <alexey.makhalov@broadcom.com> 36.5-15
- Fix restorecon/fixfiles mac_admin denial: domain transition unconfined_t->setfiles_mac_t
  with range_transition s0 and system_r role association outside optional_policy
- Fix sshd_t -> chkpwd_t process transition: add noatsecure/rlimitinh/siginh
- Add a macro to allow IF_ALG to jitterentropy via openssl library
- Add tcp port 1514 to syslog_tls_port_t (for vCenter)
* Tue Mar 24 2026 Alexey Makhalov <alexey.makhalov@broadcom.com> 36.5-14
- Add requires: rpm-plugin-selinux
* Wed Mar 18 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 36.5-13
- Bump version as a part of python3.14 upgrade
* Tue Mar 10 2026 Alexey Makhalov <alexey.makhalov@broadcom.com> 36.5-12
- Enforcing mode by default
* Wed Oct 22 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 36.5-11
- Fix motd denials
* Thu Aug 21 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 36.5-10
- Fix few systemd-resolved policies
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
