Summary:    Irqbalance daemon
Name:       irqbalance
Version:    1.7.0
Release:    2%{?dist}
License:    GPLv2
URL:        https://github.com/Irqbalance/irqbalance
Group:      System Environment/Services
Vendor:     VMware, Inc.
Distribution:   Photon
# https://github.com/Irqbalance/%{name}/archive/v%{version}.tar.gz
Source0:    %{name}-%{version}.tar.gz
%define sha1 %{name}-%{version}=21a330214be3c578748dced6173fd545ca75d2c9
BuildRequires:  systemd-devel
BuildRequires:  glib-devel
BuildRequires:  libnuma-devel
Requires:  systemd
Requires:  glib
Requires:  libnuma
%description
Irqbalance is a daemon to help balance the cpu load generated by
interrupts across all of a systems cpus.
%prep
%setup -q
%build
sed -i 's/libsystemd-journal/libsystemd/' configure.ac
./autogen.sh
%configure \
    --disable-static \
    --with-systemd

make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
install -D -m 0644 misc/irqbalance.env %{buildroot}/etc/sysconfig/irqbalance
sed -i 's#/path/to/irqbalance.env#/etc/sysconfig/irqbalance#' misc/irqbalance.service
install -D -m 0644 misc/irqbalance.service %{buildroot}%{_prefix}/lib/systemd/system/irqbalance.service

%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%post
%systemd_post %{name}.service
%preun
%systemd_preun %{name}.service
%postun
%systemd_postun_with_restart %{name}.service

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/*
%{_sbindir}/*
%exclude %{_libdir}/debug/*
%{_libdir}/systemd/*
%{_datadir}/*

%changelog
*   Thu Oct 29 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 1.7.0-2
-   Add dependency on libnuma
*   Wed Aug 12 2020 Gerrit Photon <photon-checkins@vmware.com> 1.7.0-1
-   Automatic Version Bump
*   Wed Jul 15 2020 Gerrit Photon <photon-checkins@vmware.com> 1.6.0-1
-   Automatic Version Bump
*   Fri Jul 10 2020 Tapas Kundu <tkundu@vmware.com> 1.4.0-3
-   Remove BuildArch
*   Mon Oct 22 2018 Ajay Kaher <akaher@vmware.com> 1.4.0-2
-   Adding BuildArch
*   Fri Sep 07 2018 Ankit Jain <ankitja@vmware.com>  1.4.0-1
-   Updated the package to version 1.4.0
*   Mon Apr 03 2017 Divya Thaluru <dthaluru@vmware.com>  1.2.0-1
-   Updated the package to version 1.2.0
*   Fri Nov 18 2016 Anish Swaminathan <anishs@vmware.com>  1.1.0-4
-   Change systemd dependency
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.1.0-3
-   GA - Bump release of all rpms
*   Thu May 05 2016 Kumar Kaushik <kaushikk@vmware.com> 1.1.0-2
-   Adding package upgrade support.
*   Fri Jan 15 2016 Alexey Makhalov <amakhalov@vmware.com> 1.1.0-1
-   Initial version