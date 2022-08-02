Summary:        Dynamic Kernel Module Support
Name:           dkms
Version:        3.0.10
Release:        1%{?dist}
License:        GPLv2+
URL:            http://linux.dell.com/dkms/
Group:          System Environment/Base
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/dell/dkms/archive/%{name}-%{version}.tar.gz
%define sha512  dkms=b271453497a004177137e972cb45cacb2dd3ac124a1fd2526218cf690f5ce77250195e73b6f9c75de4661a718d928e546bd85770ab98c2fd9af44fe777492ad7
BuildArch:      noarch
BuildRequires:  systemd
Requires:       systemd
Requires:       gcc
Requires:       make
Requires:       binutils

%description
Dynamic Kernel Module Support (DKMS) is a program/framework that enables generating Linux kernel modules whose sources generally reside outside the kernel source tree.
The concept is to have DKMS modules automatically rebuilt when a new kernel is installed.

%prep
%autosetup -n %{name}-%{version}

%build
# no /usr/bin/bash in photon os
# replace it with /bin/bash
sed -i 's/\/usr\/bin\/bash/\/bin\/bash/g' kernel_install.d_dkms

%install
make install-redhat DESTDIR=%{buildroot} \
    SBIN=%{buildroot}%{_sbindir} \
    VAR=%{buildroot}%{_localstatedir}/lib/%{name} \
    MAN=%{buildroot}%{_mandir}/man8 \
    ETC=%{buildroot}%{_sysconfdir}/%{name} \
    BASHDIR=%{buildroot}%{_sysconfdir}/bash_completion.d \
    LIBDIR=%{buildroot}%{_prefix}/lib/%{name} \
    SYSTEMD=%{buildroot}%{_unitdir} %{?_smp_mflags}

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
%config(noreplace) %{_sysconfdir}/%{name}/framework.conf
%{_sysconfdir}/kernel/install.d/%{name}
%{_sysconfdir}/kernel/postinst.d/%{name}
%{_sysconfdir}/kernel/prerm.d/%{name}
%{_libdir}/systemd/system/dkms.service
%{_libdir}/systemd/system-preset/50-dkms.preset
%{_libdir}/%{name}/*
%{_sbindir}/dkms
%{_mandir}/man8/dkms.8.gz

%changelog
*   Fri Jan 20 2023 Alexey Makhalov <amakhalov@vmware.com> 3.0.10-1
-   Version update
*   Mon May 03 2021 Gerrit Photon <photon-checkins@vmware.com> 2.8.4-1
-   Automatic Version Bump
*   Mon Jan 18 2021 Ajay Kaher <akaher@vmware.com> 2.8.2-2
-   Modified Requires list.
*   Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 2.8.2-1
-   Automatic Version Bump
*   Mon Sep 10 2018 Ajay Kaher <akaher@vmware.com> 2.6.1-1
-   Upgraded to version 2.6.1
*   Thu May 26 2016 Divya Thaluru <dthaluru@vmware.com>  2.2.0.3-4
-   Fixed logic to restart the active services after upgrade
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.2.0.3-3
-   GA - Bump release of all rpms
*   Tue Aug 25 2015 Alexey Makhalov <amakhalov@vmware.com> 2.2.0.3-2
-   Added systemd preset file with 'disable' default value.
-   Set BuildArch to noarch.
*   Thu Aug 6 2015 Divya Thaluru <dthaluru@vmware.com> 2.2.0.3-1
-   Initial version
