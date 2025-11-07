Summary:        unbound dns server
Name:           unbound
Version:        1.24.1
Release:        1%{?dist}
Group:          System/Servers
Vendor:         VMware, Inc.
License:        BSD
Distribution:   Photon
URL:            http://www.unbound.net

Source0: https://github.com/NLnetLabs/unbound/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512 %{name}=7ed9f0ba9b855c931767fb2657e2cd8ae97a2863f5b5df3902a35ac12ef08883ebb9a07850c8f65e5fa0ec680ae035a5d1695d548c5384690f89dfcca5327482

Source1: %{name}.service

Requires:       systemd
Requires(pre):  /usr/sbin/useradd /usr/sbin/groupadd

BuildRequires:  systemd
BuildRequires:  expat-devel
BuildRequires:  bison

%description
Unbound is a validating, recursive, and caching DNS resolver.

%package    devel
Summary:    unbound development libs and headers
Group:      Development/Libraries
Requires:   expat-devel
Requires:   %{name} = %{version}-%{release}

%description devel
Development files for unbound dns server

%package    docs
Summary:    unbound docs
Group:      Documentation

%description docs
unbound dns server docs

%prep
%autosetup -p1 -n %{name}-release-%{version}

%build
%configure \
    --with-conf-file=%{_sysconfdir}/%{name}/%{name}.conf \
    --disable-static

%make_build

%install
%make_install %{?_smp_mflags}
install -vdm755 %{buildroot}%{_unitdir}
install -pm 0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service

%check
%make_build check

%pre
getent group unbound >/dev/null || groupadd -r unbound
getent passwd unbound >/dev/null || \
useradd -r -g unbound -d %{_sysconfdir}/unbound -s /sbin/nologin \
        -c "Unbound DNS resolver" unbound

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_libdir}/*.so.*
%{_sbindir}/*
%{_sysconfdir}/*
%{_unitdir}/%{name}.service

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*

%files docs
%defattr(-,root,root)
%{_mandir}/*

%changelog
* Fri Nov 07 2025 Mukul Sikka <mukul.sikka@broadcom.com> 1.24.1-1
- Update to v1.24.1
- Fix CVE-2025-11411, CVE-2025-5994
* Mon May 05 2025 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 1.21.0-3
- Version bump for expat upgrade
* Tue Oct 22 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.21.0-2
- Fix CVE-2024-8508
* Mon Aug 26 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.21.0-1
- Upgrade to v1.12.0, fixes CVE-2024-33655
* Tue Aug 20 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.16.3-3
- Fix CVE-2024-43167 and CVE-2024-43168
* Thu Feb 29 2024 Anmol Jain <anmol.jain@broadcom.com> 1.16.3-2
- Bump version as a part of expat upgrade
* Mon Feb 12 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.16.3-1
- Upgrade to v1.16.3
- Fix CVE-2023-50387, CVE-2023-50868
* Fri Sep 30 2022 Srish Srinivasan <ssrish@vmware.com> 1.16.2-2
- Fix for CVE-2022-3204
* Wed Aug 17 2022 Srish Srinivasan <ssrish@vmware.com> 1.16.2-1
- Update to 1.16.2 for fixing CVE-2022-30698 and CVE-2022-30699
* Fri Jul 30 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.12.0-2
- Fix openssl 3.0.0 beta2 compatibility with unbound
* Fri Jul 23 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.12.0-1
- Update to 1.12.0 for openssl 3.0 compatibility
* Tue Feb 02 2021 Shreyas B. <shryasb@vmware.com> 1.11.0-2
- Fix for CVE-2020-28935
* Mon Jul 27 2020 Gerrit Photon <photon-checkins@vmware.com> 1.11.0-1
- Automatic Version Bump
* Sun May 24 2020 Shreyas B. <shryasb@vmware.com> 1.8.0-4
- Fix for CVE-2020-12662 & CVE-2020-12663
* Fri Dec 20 2019 Shreyas B. <shryasb@vmware.com> 1.8.0-3
- Fix for vulnerability CVE-2019-18934 that can cause shell code
- execution after receiving a specially crafted answer.
* Mon Oct 14 2019 Shreyas B. <shryasb@vmware.com> 1.8.0-2
- Fix for CVE-2019-16866.
* Mon Sep 10 2018 Michelle Wang <michellew@vmware.com> 1.8.0-1
- Update to version 1.8.0.
* Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 1.6.1-3
- Remove shadow from requires and use explicit tools for post actions
* Fri Apr 14 2017 Alexey Makhalov <amakhalov@vmware.com> 1.6.1-2
- Requires expat-devel
* Wed Apr 05 2017 Xiaolin Li <xiaolinl@vmware.com> 1.6.1-1
- Updated to version 1.6.1
* Fri Jan 06 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.6.0-1
- Initial
