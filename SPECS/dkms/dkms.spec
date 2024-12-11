Summary:        Dynamic Kernel Module Support
Name:           dkms
Version:        3.0.10
Release:        3%{?dist}
URL:            http://linux.dell.com/dkms
Group:          System Environment/Base
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/dell/dkms/archive/%{name}-%{version}.tar.gz
%define sha512 %{name}=b271453497a004177137e972cb45cacb2dd3ac124a1fd2526218cf690f5ce77250195e73b6f9c75de4661a718d928e546bd85770ab98c2fd9af44fe777492ad7

Source1: license.txt
%include %{SOURCE1}

BuildArch:      noarch

BuildRequires:  systemd-devel

Requires:       systemd
Requires:       build-essential

%description
Dynamic Kernel Module Support (DKMS) is a program/framework that enables generating Linux kernel modules whose sources generally reside outside the kernel source tree.
The concept is to have DKMS modules automatically rebuilt when a new kernel is installed.

%prep
%autosetup -p1

%build

%install
%make_install %{?_smp_mflags} install-redhat
install -vdm755 %{buildroot}%{_presetdir}
echo "disable %{name}.service" > %{buildroot}%{_presetdir}/50-%{name}.preset

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%defattr(-,root,root)
%{_datadir}/bash-completion/completions/%{name}
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/framework.conf
%dir %{_sysconfdir}/%{name}/framework.conf.d
%{_sysconfdir}/kernel/postinst.d/%{name}
%{_sysconfdir}/kernel/install.d/%{name}
%{_sysconfdir}/kernel/prerm.d/%{name}
%{_unitdir}/%{name}.service
%{_presetdir}/50-%{name}.preset
%{_libdir}/%{name}/*
%{_sbindir}/%{name}
%{_mandir}/man8/%{name}.8.gz

%changelog
* Wed Dec 11 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 3.0.10-3
- Release bump for SRP compliance
* Tue Sep 12 2023 Shreenidhi Shedi <sshedi@vmware.com> 3.0.10-2
- Fix spec issues
* Fri Jan 20 2023 Alexey Makhalov <amakhalov@vmware.com> 3.0.10-1
- Version update
* Mon May 03 2021 Gerrit Photon <photon-checkins@vmware.com> 2.8.4-1
- Automatic Version Bump
* Mon Jan 18 2021 Ajay Kaher <akaher@vmware.com> 2.8.2-2
- Modified Requires list.
* Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 2.8.2-1
- Automatic Version Bump
* Mon Sep 10 2018 Ajay Kaher <akaher@vmware.com> 2.6.1-1
- Upgraded to version 2.6.1
* Thu May 26 2016 Divya Thaluru <dthaluru@vmware.com>  2.2.0.3-4
- Fixed logic to restart the active services after upgrade
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.2.0.3-3
- GA - Bump release of all rpms
* Tue Aug 25 2015 Alexey Makhalov <amakhalov@vmware.com> 2.2.0.3-2
- Added systemd preset file with 'disable' default value.
- Set BuildArch to noarch.
* Thu Aug 6 2015 Divya Thaluru <dthaluru@vmware.com> 2.2.0.3-1
- Initial version
