Summary:        SELinux policy
Name:           selinux-policy
Version:        3.14.5
Release:        3%{?dist}
License:        GPLv2
Group:          System Environment/Libraries
Source0:        https://github.com/fedora-selinux/%{name}/archive/ad1d35503f55f535401daa0a59913aa559c38d44/%{name}-ad1d3550.tar.gz
%define sha1 selinux-policy-ad=e7bf6f64722df5ca10b6a6ee83a304e630262608
Source1:        https://github.com/fedora-selinux/%{name}-contrib/archive/6db7310a3b7385e07359a978a46c52d7ec22bedd/%{name}-contrib-6db7310a.tar.gz
%define sha1 selinux-policy-contrib=284f99c684043c24b5e8a281cf2d67bf182cd4b8
Source2:        https://github.com/containers/container-selinux/archive/container-selinux-2.132.0.tar.gz
%define sha1 container-selinux=72227c05f11c6e9b2bfc24be2ad3d9c5e1ed376c
Source3:        build.conf
Source4:        modules.conf
Url:            https://github.com/SELinuxProject/selinux/wiki
Vendor:         VMware, Inc.
Distribution:   Photon
Patch1:         contrib-container.patch
Patch2:         contrib-cron.patch
Patch3:         contrib-dbus.patch
Patch4:         contrib-virt.patch
Patch5:         kernel-storage.patch
Patch6:         roles-staff.patch
Patch7:         roles-unprivuser.patch
Patch8:         system-authlogin.patch
Patch9:         system-getty.patch
Patch10:        system-init.patch
Patch11:        system-logging.patch
Patch12:        system-modutils.patch
Patch13:        system-systemd.patch
Patch14:        system-systenwork.patch
Patch15:        system-udev.patch
Patch16:        system-userdomain.patch
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
%setup -q -b 1 -n %{name}-contrib-6db7310a3b7385e07359a978a46c52d7ec22bedd
%setup -q -b 2 -n container-selinux-2.132.0
%setup -qn %{name}-ad1d35503f55f535401daa0a59913aa559c38d44
cp ../%{name}-contrib-6db7310a3b7385e07359a978a46c52d7ec22bedd/* policy/modules/contrib/
cp -r ../container-selinux-2.132.0/container.* policy/modules/contrib/
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

%build
cp %{SOURCE3} .
cp %{SOURCE4} policy/
make %{?_smp_flags}

%install
make %{?_smp_flags} DESTDIR=%{buildroot} install
mkdir -p %{buildroot}/var/lib/selinux/default
# Use priority 100 instead of default 400
make %{?_smp_flags} DESTDIR=%{buildroot} SEMODULE="%{_sbindir}/semodule -p %{buildroot} -X 100" load
make %{?_smp_flags} DESTDIR=%{buildroot} install-headers
mkdir %{buildroot}%{_datadir}/selinux/devel
cp doc/Makefile.example %{buildroot}%{_datadir}/selinux/devel/Makefile
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

%files devel
%defattr(-,root,root,-)
%{_datadir}/selinux
%{_sharedstatedir}/selinux/default

%changelog
* Sun Jul 05 2020 Vikash Bansal <bvikas@vmware.com> 3.14.5-3
- Resolve "avc:  denied" errors
* Thu Jun 04 2020 Vikash Bansal <bvikas@vmware.com> 3.14.5-2
- Add coreutils-selinux in requires, needed for setting labels
* Fri Apr 24 2020 Alexey Makhalov <amakhalov@vmware.com> 3.14.5-1
- Initial build.
