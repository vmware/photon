Summary:        SELinux policy
Name:           selinux-policy
Version:        3.14.8
Release:        3%{?dist}
License:        GPLv2
Group:          System Environment/Libraries
Url:            https://github.com/SELinuxProject/selinux/wiki
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/fedora-selinux/%{name}/archive/db2614cce37245ba4fc5de73b1f6f33cc46686e4/%{name}-db2614cc.tar.gz
%define sha1 selinux-policy-db=ffba5a771c95d3b6837f8b1d66f2d9ea52661e1c
Source1:        https://github.com/containers/container-selinux/archive/container-selinux-2.145.0.tar.gz
%define sha1 container-selinux=93676d051407d4e57ae517dd4dc45239d1369e3d
Source2:        build.conf
Source3:        modules.conf

Patch1:         contrib-container.patch
Patch2:         contrib-cron.patch
Patch3:         contrib-dbus.patch
Patch4:         contrib-virt.patch
Patch5:         kernel-storage.patch
Patch6:         roles-staff.patch
Patch7:         roles-unprivuser.patch
Patch8:         motd_t-new-domain-for-motdgen.patch
Patch9:         system-getty.patch
Patch10:        system-init.patch
Patch11:        system-logging.patch
Patch12:        system-modutils.patch
Patch13:        system-systemd.patch
Patch14:        system-sysnetwork.patch
Patch15:        system-udev.patch
Patch16:        system-userdomain.patch
Patch17:        admin_usermanage.patch
Patch18:        system-fstool.patch
Patch19:        iptables-allow-kernel_t-fifo_files.patch
Patch20:        authlogin.if-add-transition-rules-for-shadow.patch

BuildArch:      noarch

BuildRequires:  checkpolicy python3 semodule-utils libselinux-utils
BuildRequires:  policycoreutils

Requires:       policycoreutils
Requires:       coreutils-selinux

%description
Provides default Photon OS SELinux policy.

%package devel
Summary: SELinux policy devel
Requires: selinux-policy = %{version}-%{release}
Requires: m4 checkpolicy

%description devel
SELinux policy development

%prep
# Using autosetup is not feasible
%setup -q -b 1 -n container-selinux-2.145.0
# Using autosetup is not feasible
%setup -qn %{name}-db2614cce37245ba4fc5de73b1f6f33cc46686e4
cp -r ../container-selinux-2.145.0/container.* policy/modules/contrib/
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1

%build
cp %{SOURCE2} .
cp %{SOURCE3} policy/
make %{?_smp_mflags}

%install
make %{?_smp_mflags} DESTDIR=%{buildroot} install
mkdir -p %{buildroot}/var/lib/selinux/default
# Use priority 100 instead of default 400
make %{?_smp_mflags} DESTDIR=%{buildroot} SEMODULE="%{_sbindir}/semodule -p %{buildroot} -X 100" load
make %{?_smp_mflags} DESTDIR=%{buildroot} install-headers
mkdir %{buildroot}%{_datadir}/selinux/devel
cp doc/Makefile.example %{buildroot}%{_datadir}/selinux/devel/Makefile
cp config/file_contexts.subs_dist %{buildroot}%{_sysconfdir}/selinux/default/contexts/files/
cat > %{buildroot}%{_sysconfdir}/selinux/config << EOF
# This file controls the state of SELinux on the system.
# SELINUX= can take one of these three values:
#     enforcing - SELinux security policy is enforced.
#     permissive - SELinux prints warnings instead of enforcing.
#     disabled - No SELinux policy is loaded.
SELINUX=permissive
# SELINUXTYPE= can take one of these values:
#     default - minimal Photon container host MCS protection.
SELINUXTYPE=default
EOF

%posttrans
if [ $1 -ge 0 ] ; then
    /sbin/setfiles /etc/selinux/default/contexts/files/file_contexts /
fi

%files
%defattr(-,root,root,-)
%dir %{_sysconfdir}/selinux/
%config(noreplace) %{_sysconfdir}/selinux/config
%{_sysconfdir}/selinux/default
%{_sysconfdir}/selinux/default/contexts/files/file_contexts.subs_dist

%files devel
%defattr(-,root,root,-)
%{_datadir}/selinux
%{_sharedstatedir}/selinux/default

%changelog
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
