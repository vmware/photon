%global debug_package %{nil}

Summary:        A kernel-based automounter for Linux
Name:           autofs
Version:        5.1.8
Release:        2%{?dist}
License:        GPLv2+
URL:            http://www.kernel.org/pub/linux/daemons/autofs
Group:          System Environment/Daemons
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://www.kernel.org/pub/linux/daemons/%{name}/v5/%{name}-%{version}.tar.xz
%define sha512 %{name}=6ee6283c0977c82848a654dc24745ee687f6916de441c3688fa91f67ca7295e632ee3808cc2358984a4b9f19841e6e1a91ab48aad6341ac8e63827fe8c32d223

Source1:        %{name}.service

BuildRequires:  systemd-devel
BuildRequires:  rpcsvc-proto-devel
BuildRequires:  libtirpc-devel
BuildRequires:  bison

Requires:       systemd
Requires:       libtirpc

%description
Automounting is the process of automatically mounting and unmounting of file systems by a daemon. Autofs includes both a user-space daemon and code in the kernel that assists the daemon.

%prep
%autosetup -p1

%build
%configure --with-libtirpc

%make_build

%install
mkdir -p -m755 %{buildroot}%{_unitdir} \
               %{buildroot}%{_sysconfdir}/auto.master.d

%make_install mandir=%{_mandir} INSTALLROOT=%{buildroot}

mkdir -p -m755 %{buildroot}%{_sysconfdir}/sysconfig
make -C redhat %{?_smp_mflags}
install -p -D -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}
install -m 644 redhat/autofs.conf %{buildroot}%{_sysconfdir}/autofs.conf
install -m 644 redhat/autofs.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/autofs
install -m 644 samples/auto.master %{buildroot}%{_sysconfdir}/auto.master
install -m 644 samples/auto.misc %{buildroot}%{_sysconfdir}/auto.misc
install -m 755 samples/auto.net %{buildroot}%{_sysconfdir}/auto.net
install -m 755 samples/auto.smb %{buildroot}%{_sysconfdir}/auto.smb
install -m 600 samples/autofs_ldap_auth.conf %{buildroot}%{_sysconfdir}/autofs_ldap_auth.conf
rm -rf %{buildroot}%{_sysconfdir}/rc.d

%post
/sbin/ldconfig
%systemd_post autofs.service

%postun
/sbin/ldconfig
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
%{_unitdir}/autofs.service

%changelog
* Sun Nov 13 2022 Shreenidhi Shedi <sshedi@vmware.com> 5.1.8-2
- Bump version as a part of libtirpc upgrade
* Thu Aug 25 2022 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 5.1.8-1
- Update version to 5.1.8
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
