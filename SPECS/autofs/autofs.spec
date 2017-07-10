%global debug_package %{nil}
Summary:        A kernel-based automounter for Linux
Name:           autofs
Version:        5.1.3
Release:        1%{?dist}
License:        GPLv2+
URL:            http://www.kernel.org/pub/linux/daemons/autofs
Group:          System Environment/Daemons
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://www.kernel.org/pub/linux/daemons/%{name}/v5/%{name}-%{version}.tar.xz
%define sha1    autofs=96074f905c62e205c99e473257b0f461f0c49a60

BuildRequires:  systemd
Requires:       systemd
%description
Automounting is the process of automatically mounting and unmounting of file systems by a daemon. Autofs includes both a user-space daemon and code in the kernel that assists the daemon. 

%prep
%setup -q

%build
./configure --prefix=/usr           \
            --mandir=/usr/share/man
make

%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
mkdir -p -m755 %{buildroot}/lib/systemd/system
mkdir -p -m755 %{buildroot}/etc/auto.master.d
make install mandir=%{_mandir} INSTALLROOT=%{buildroot}
make -C redhat
install -m 644 redhat/autofs.service  %{buildroot}/lib/systemd/system/autofs.service
rm -rf %{buildroot}/etc/rc.d

%check
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
*   Thu Jul 06 2017 Xiaolin Li <xiaolinl@vmware.com> 5.1.3-1
-   Initial build. First version
