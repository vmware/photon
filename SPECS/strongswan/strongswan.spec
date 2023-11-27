Summary:          The OpenSource IPsec-based VPN Solution
Name:             strongswan
Version:          5.6.3
Release:          9%{?dist}
License:          GPLv2+
URL:              https://www.strongswan.org
Group:            System Environment/Security
Vendor:           VMware, Inc.
Distribution:     Photon

Source0: https://download.strongswan.org/%{name}-%{version}.tar.bz2
%define sha512 %{name}=080402640952b1a08e95bfe9c7f33c6a7dd01ac401b5e7e2e78257c0f2bf0a4d6078141232ac62abfacef892c493f6824948b3165d54d72b4e436ed564fd2609

%if 0%{?with_check}
Patch0: strongswan-fix-make-check.patch
%endif

Patch1: CVE-2018-16151-16152.patch
Patch2: CVE-2021-41990.patch
Patch3: CVE-2021-41991.patch
Patch4: CVE-2021-45079.patch
Patch5: CVE-2022-40617.patch
Patch6: CVE-2023-41913.patch

BuildRequires:    autoconf
BuildRequires:    gmp-devel
BuildRequires:    systemd-devel
%{?systemd_requires}

Requires: systemd
Requires: gmp

%description
strongSwan is a complete IPsec implementation for Linux 2.6, 3.x, and 4.x kernels.

%prep
%autosetup -p1

%build
%configure \
    --enable-systemd \
    --enable-openssl \
    --enable-gcm

%make_build

%install
%make_install %{?_smp_mflags}
find %{buildroot} -name '*.a' -delete

%if 0%{?with_check}
%check
make check %{?_smp_mflags}
%endif

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
%config(noreplace) %{_sysconfdir}/*.conf
%config(noreplace) %{_sysconfdir}/%{name}.d/*.conf
%config(noreplace) %{_sysconfdir}/%{name}.d/charon/*.conf
%config(noreplace) %{_sysconfdir}/ipsec.secrets
%{_sysconfdir}/swanctl/*
%{_sysconfdir}/ipsec.d/*
%{_bindir}/*
%{_sbindir}/*
%{_libdir}/ipsec/*
%{_libexecdir}/*
%{_mandir}/man[158]/*
%{_datadir}/%{name}/*
%{_unitdir}/%{name}-swanctl.service
%{_unitdir}/%{name}.service

%changelog
* Mon Nov 27 2023 Keerthana K <keerthanak@vmware.com> 5.6.3-9
- Fix CVE-2023-41913
* Tue Apr 18 2023 Srish Srinivasan <ssrish@vmware.com> 5.6.3-8
- enable OpenSSL and GCM plugin
* Tue Nov 08 2022 Shreenidhi Shedi <sshedi@vmware.com> 5.6.3-7
- Fix CVE-2022-40617
* Thu Feb 10 2022 Tapas Kundu <tkundu@vmware.com> 5.6.3-6
- Fix CVE-2021-45079
* Mon Oct 25 2021 Tapas Kundu <tkundu@vmware.com> 5.6.3-5
- Fix CVE-2021-41990 and CVE-2021-41991
* Tue Jun 08 2021 Tapas Kundu <tkundu@vmware.com> 5.6.3-4
- Enable systemd
* Fri Dec 21 2018 Keerthana K <keerthanak@vmware.com> 5.6.3-3
- Fix for CVE-2018-16151 and CVE-2018-16152.
* Thu Dec 06 2018 Keerthana K <keerthanak@vmware.com> 5.6.3-2
- Fixed make check failures.
* Mon Sep 17 2018 Tapas Kundu <tkundu@vmware.com> 5.6.3-1
- Updated to 5.6.3 release
* Thu Aug 16 2018 Tapas Kundu <tkundu@vmware.com> 5.5.2-5
- Fix for CVE-2018-10811
* Mon Jul 23 2018 Ajay Kaher <akaher@vmware.com> 5.5.2-4
- Fix CVE-2018-5388
* Tue Oct 10 2017 Dheeraj Shetty <dheerajs@vmware.com> 5.5.2-3
- Fix CVE-2017-11185 CVE-2017-9022 and CVE-2017-9023
* Thu Aug 24 2017 Alexey Makhalov <amakhalov@vmware.com> 5.5.2-2
- Fix compilation issue for glibc-2.26
* Wed Apr 12 2017 Vinay Kulkarni <kulkarniv@vmware.com> 5.5.2-1
- Update to version 5.5.2
* Wed Dec 21 2016 Xiaolin Li <xiaolinl@vmware.com>  5.5.1-1
- Initial build.
