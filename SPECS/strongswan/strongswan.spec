Summary:          The OpenSource IPsec-based VPN Solution
Name:             strongswan
Version:          5.9.8
Release:          4%{?dist}
License:          GPLv2+
URL:              https://www.strongswan.org
Group:            System Environment/Security
Vendor:           VMware, Inc.
Distribution:     Photon

Source0: https://download.strongswan.org/%{name}-%{version}.tar.bz2
%define sha512 %{name}=16d3afc80704f896f3f97addf452b4bb29fc1911c54e980f76ac48bdbe2340ce3bd4e79024848cb7961bbe9ad5458d93389343878ca042af658d51b11219666b

%if 0%{?with_check}
Patch0: strongswan-fix-make-check.patch
%endif

Patch1: 0001-HCX-custom-remote-natt-port.patch
Patch2: 0002-ipsec-Add-clear_df-flag.patch
Patch3: 0003-reiniate-conn-on-failure.patch
Patch4: 0004-Add-new-configs-min_spi-and-max_spi.patch

# CVE fixes
Patch5: CVE-2023-26463.patch
Patch6: CVE-2023-41913.patch

BuildRequires:    autoconf
BuildRequires:    gmp-devel
BuildRequires:    systemd-devel
BuildRequires:    gperf
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
%ifarch x86_64
    --enable-aesni \
%endif
    --enable-openssl \
    --enable-socket-dynamic \
    --enable-vici \
    --enable-swanctl \
    --enable-gcm

%make_build

%install
%make_install %{?_smp_mflags}

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
%{_unitdir}/%{name}-starter.service
%{_unitdir}/%{name}.service

%changelog
* Mon Nov 27 2023 Keerthana K <keerthanak@vmware.com> 5.9.8-4
- Fix CVE-2023-41913
* Tue Apr 18 2023 Srish Srinivasan <ssrish@vmware.com> 5.9.8-3
- enable OpenSSL and GCM plugins
* Tue Mar 21 2023 Srish Srinivasan <ssrish@vmware.com> 5.9.8-2
- fix CVE-2023-26463
* Wed Feb 15 2023 Srish Srinivasan <ssrish@vmware.com> 5.9.8-1
- Version update to 5.9.8 along with HCX patches
* Tue Nov 08 2022 Shreenidhi Shedi <sshedi@vmware.com> 5.9.0-5
- Fix CVE-2022-40617
* Thu Feb 10 2022 Tapas Kundu <tkundu@vmware.com> 5.9.0-4
- Fix CVE-2021-45079
* Mon Oct 25 2021 Tapas Kundu <tkundu@vmware.com> 5.9.0-3
- Fix CVE-2021-41990 and CVE-2021-41991.
* Wed Jun 09 2021 Tapas Kundu <tkundu@vmware.com> 5.9.0-2
- Enable systemd
* Mon Aug 10 2020 Gerrit Photon <photon-checkins@vmware.com> 5.9.0-1
- Automatic Version Bump
* Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 5.8.4-1
- Automatic Version Bump
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
