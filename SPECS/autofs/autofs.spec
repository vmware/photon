%global debug_package %{nil}
Summary:        A kernel-based automounter for Linux
Name:           autofs
Version:        5.1.7
Release:        1%{?dist}
License:        GPLv2+
URL:            http://www.kernel.org/pub/linux/daemons/autofs
Group:          System Environment/Daemons
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://www.kernel.org/pub/linux/daemons/%{name}/v5/%{name}-%{version}.tar.xz
%define sha1    %{name}=69ec5339ca9a7ec15f0a28e18f9c4e93906ffcd2
Source1:        %{name}.service

BuildRequires:  systemd
BuildRequires:  rpcsvc-proto-devel
BuildRequires:  libtirpc-devel

Requires:       systemd
Requires:       libtirpc

%description
Automounting is the process of automatically mounting and unmounting of file systems by a daemon. Autofs includes both a user-space daemon and code in the kernel that assists the daemon.

%prep
%autosetup -p1

%build
%configure --with-libtirpc

make %{?_smp_mflags}

%install
mkdir -p -m755 %{buildroot}/lib/systemd/system \
               %{buildroot}/etc/auto.master.d

make install mandir=%{_mandir} INSTALLROOT=%{buildroot} %{?_smp_mflags}

mkdir -p -m755 %{buildroot}/etc/sysconfig
make -C redhat %{?_smp_mflags}
install -p -D -m 0644 %{SOURCE1} %{buildroot}/lib/systemd/system/autofs.service
install -m 644 redhat/autofs.conf %{buildroot}/etc/autofs.conf
install -m 644 redhat/autofs.sysconfig %{buildroot}/etc/sysconfig/autofs
install -m 644 samples/auto.master %{buildroot}/etc/auto.master
install -m 644 samples/auto.misc %{buildroot}/etc/auto.misc
install -m 755 samples/auto.net %{buildroot}/etc/auto.net
install -m 755 samples/auto.smb %{buildroot}/etc/auto.smb
install -m 600 samples/autofs_ldap_auth.conf %{buildroot}/etc/autofs_ldap_auth.conf
rm -rf %{buildroot}/etc/rc.d

#%%check
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
%{_libdir}/libautofs.so
%dir %{_sysconfdir}/auto.master.d
%{_mandir}/man5/*
%{_mandir}/man8/*
/lib/systemd/system/autofs.service

%changelog
* Mon Apr 12 2021 Gerrit Photon <photon-checkins@vmware.com> 5.1.7-1
- Automatic Version Bump
* Mon Aug 10 2020 Shreyas B <shreyasb@vmware.com> 5.1.6-2
- Fix service start issue
* Fri Oct 18 2019 Shreyas B <shreyasb@vmware.com> 5.1.6-1
- Update version to 5.1.6
* Fri Sep 21 2018 Alexey Makhalov <amakhalov@vmware.com> 5.1.4-2
- Use rpcsvc-proto and libtirpc
* Thu Sep 06 2018 Anish Swaminathan <anishs@vmware.com> 5.1.4-1
- Update version to 5.1.4
* Thu Jul 06 2017 Xiaolin Li <xiaolinl@vmware.com> 5.1.3-1
- Initial build. First version
