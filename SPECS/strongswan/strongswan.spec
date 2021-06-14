Summary:          The OpenSource IPsec-based VPN Solution
Name:             strongswan
Version:          5.9.0
Release:          2%{?dist}
License:          GPLv2+
URL:              https://www.strongswan.org
Group:            System Environment/Security
Vendor:           VMware, Inc.
Distribution:     Photon
Source0:          https://download.strongswan.org/%{name}-%{version}.tar.bz2
%define sha1      %{name}=8bb52214f72f2571f55dababfe76ff97fd31ca1f
BuildRequires:    autoconf
BuildRequires:    gmp-devel
BuildRequires:    systemd-devel
Patch0:           strongswan-fix-make-check.patch
%{?systemd_requires}

%description
strongSwan is a complete IPsec implementation for Linux 2.6, 3.x, and 4.x kernels.

%prep
%autosetup -p1

%build
%configure --enable-systemd
sed -i '/stdlib.h/a #include <stdint.h>' src/libstrongswan/utils/utils.h &&
make %{?_smp_mflags}

%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install %{?_smp_mflags}
find %{buildroot} -name '*.la' -delete
find %{buildroot} -name '*.a' -delete

%check
make check %{?_smp_mflags}

%clean
rm -rf %{buildroot}/*

%post
/sbin/ldconfig
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
/sbin/ldconfig
%systemd_postun_with_restart %{name}.service

%files
%defattr(-,root,root)
%{_sysconfdir}/*
%{_bindir}/*
%{_sbindir}/*
%{_libdir}/ipsec/*
%{_libexecdir}/*
%{_mandir}/man[158]/*
%{_datadir}/strongswan/*
%{_unitdir}/strongswan-starter.service
%{_unitdir}/strongswan.service

%changelog
*   Wed Jun 09 2021 Tapas Kundu <tkundu@vmware.com> 5.9.0-2
-   Enable systemd
*   Mon Aug 10 2020 Gerrit Photon <photon-checkins@vmware.com> 5.9.0-1
-   Automatic Version Bump
*   Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 5.8.4-1
-   Automatic Version Bump
*   Fri Dec 21 2018 Keerthana K <keerthanak@vmware.com> 5.6.3-3
-   Fix for CVE-2018-16151 and CVE-2018-16152.
*   Thu Dec 06 2018 Keerthana K <keerthanak@vmware.com> 5.6.3-2
-   Fixed make check failures.
*   Mon Sep 17 2018 Tapas Kundu <tkundu@vmware.com> 5.6.3-1
-   Updated to 5.6.3 release
*   Thu Aug 16 2018 Tapas Kundu <tkundu@vmware.com> 5.5.2-5
-   Fix for CVE-2018-10811
*   Mon Jul 23 2018 Ajay Kaher <akaher@vmware.com> 5.5.2-4
-   Fix CVE-2018-5388
*   Tue Oct 10 2017 Dheeraj Shetty <dheerajs@vmware.com> 5.5.2-3
-   Fix CVE-2017-11185 CVE-2017-9022 and CVE-2017-9023
*   Thu Aug 24 2017 Alexey Makhalov <amakhalov@vmware.com> 5.5.2-2
-   Fix compilation issue for glibc-2.26
*   Wed Apr 12 2017 Vinay Kulkarni <kulkarniv@vmware.com> 5.5.2-1
-   Update to version 5.5.2
*   Wed Dec 21 2016 Xiaolin Li <xiaolinl@vmware.com>  5.5.1-1
-   Initial build.
