%global debug_package %{nil}
Summary:        A kernel-based automounter for Linux
Name:           autofs
Version:        5.1.4
Release:        2%{?dist}
License:        GPLv2+
URL:            http://www.kernel.org/pub/linux/daemons/autofs
Group:          System Environment/Daemons
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://www.kernel.org/pub/linux/daemons/%{name}/v5/%{name}-%{version}.tar.xz
%define sha1    autofs=c26f2e5e24814adb0572f2c01066215d11ee0782

BuildRequires:  systemd
BuildRequires:  rpcsvc-proto-devel
BuildRequires:  libtirpc-devel
Requires:       systemd
Requires:       libtirpc
%description
Automounting is the process of automatically mounting and unmounting of file systems by a daemon. Autofs includes both a user-space daemon and code in the kernel that assists the daemon.

%prep
%setup -q

%build
./configure --prefix=/usr           \
            --mandir=/usr/share/man
make %{?_smp_mflags}

%install
mkdir -p -m755 %{buildroot}/lib/systemd/system
mkdir -p -m755 %{buildroot}/etc/auto.master.d
make install mandir=%{_mandir} INSTALLROOT=%{buildroot}
make -C redhat
install -m 644 redhat/autofs.service  %{buildroot}/lib/systemd/system/autofs.service
rm -rf %{buildroot}/etc/rc.d

#%check
#This package does not come with a test suite.

%post
%systemd_post autofs.service

%postun
%systemd_postun_with_restart autofs.service

%preun
%systemd_preun autofs.service

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/auto.master
%config(noreplace) %{_sysconfdir}/auto.misc
%config(noreplace) %{_sysconfdir}/auto.net
%config(noreplace) %{_sysconfdir}/auto.smb
%config(noreplace) %{_sysconfdir}/autofs.conf
%config(noreplace) %{_sysconfdir}/sysconfig/autofs
%config(noreplace) %{_sysconfdir}/autofs_ldap_auth.conf
%{_sbindir}/automount
%{_libdir}/autofs/*
%dir %{_sysconfdir}/auto.master.d
%{_mandir}/man5/*
%{_mandir}/man8/*
/lib/systemd/system/autofs.service

%changelog
*   Fri Sep 21 2018 Alexey Makhalov <amakhalov@vmware.com> 5.1.4-2
-   Use rpcsvc-proto and libtirpc
*   Thu Sep 06 2018 Anish Swaminathan <anishs@vmware.com> 5.1.4-1
-   Update version to 5.1.4
*   Thu Jul 06 2017 Xiaolin Li <xiaolinl@vmware.com> 5.1.3-1
-   Initial build. First version
