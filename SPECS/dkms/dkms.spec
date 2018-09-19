%global commit 7c3e7c52a3816c82fc8a0ef4bed9cebedc9dd02d
Summary:	Dynamic Kernel Module Support
Name:		dkms
Version:	2.6.1
Release:	1%{?dist}
License:	GPLv2+
URL:		http://linux.dell.com/dkms/
Group:		System Environment/Base
Vendor:		VMware, Inc.
Distribution: Photon
Source0:	https://github.com/dell/dkms/archive/%{name}-%{version}.tar.gz
%define sha1 dkms=9cdfecc29116d578e693cf3273ea9695d9471cf2
BuildArch:	noarch
BuildRequires:	systemd
Requires:	systemd
%description
Dynamic Kernel Module Support (DKMS) is a program/framework that enables generating Linux kernel modules whose sources generally reside outside the kernel source tree. The concept is to have DKMS modules automatically rebuilt when a new kernel is installed.

%prep
%setup -q -n %{name}-%{version}
%build
%install
make install-redhat-systemd DESTDIR=%{buildroot} \
    SBIN=%{buildroot}%{_sbindir} \
    VAR=%{buildroot}%{_localstatedir}/lib/%{name} \
    MAN=%{buildroot}%{_mandir}/man8 \
    ETC=%{buildroot}%{_sysconfdir}/%{name} \
    BASHDIR=%{buildroot}%{_sysconfdir}/bash_completion.d \
    LIBDIR=%{buildroot}%{_prefix}/lib/%{name} \
    SYSTEMD=%{buildroot}%{_unitdir}

install -vdm755 %{buildroot}/usr/lib/systemd/system-preset
echo "disable dkms.service" > %{buildroot}/usr/lib/systemd/system-preset/50-dkms.preset

%post
%systemd_post dkms.service

%preun
%systemd_preun dkms.service

%postun
%systemd_postun_with_restart dkms.service

%files
%defattr(-,root,root)
%{_sysconfdir}/bash_completion.d/dkms
%{_sysconfdir}/%{name}/framework.conf
%{_sysconfdir}/%{name}/template-dkms-mkrpm.spec
%{_sysconfdir}/%{name}/template-dkms-redhat-kmod.spec
%{_sysconfdir}/kernel/postinst.d/dkms
%{_sysconfdir}/kernel/prerm.d/dkms
/lib/systemd/system/dkms.service
%{_libdir}/systemd/system-preset/50-dkms.preset
%{_libdir}/%{name}/*
%{_sbindir}/dkms
%{_mandir}/man8/dkms.8.gz
%{_localstatedir}/lib/dkms/dkms_dbversion

%changelog
*   Mon Sep 10 2018 Ajay Kaher <akaher@vmware.com> 2.6.1-1
-   Upgraded to version 2.6.1
*   Thu May 26 2016 Divya Thaluru <dthaluru@vmware.com>  2.2.0.3-4
-   Fixed logic to restart the active services after upgrade 
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.2.0.3-3
-	GA - Bump release of all rpms
*	Tue Aug 25 2015 Alexey Makhalov <amakhalov@vmware.com> 2.2.0.3-2
-	Added systemd preset file with 'disable' default value.
-	Set BuildArch to noarch.
*	Thu Aug 6 2015 Divya Thaluru <dthaluru@vmware.com> 2.2.0.3-1
-	Initial version

