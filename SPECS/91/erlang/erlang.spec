%global build_if %{photon_subrelease} <= 91

Name:          erlang
Summary:       erlang
Version:       27.3.4.13
Release:       1%{?dist}
Group:         Development/Languages
Vendor:        VMware, Inc.
Distribution:  Photon
URL:           https://www.erlang.org

Source0: https://github.com/erlang/otp/archive/refs/tags/OTP-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

Requires: ncurses-libs

BuildRequires: openssl-devel

%description
Erlang is a general-purpose programming language and runtime
environment. Erlang has built-in support for concurrency, distribution
and fault tolerance. Erlang is used in several large telecommunication
systems from Ericsson.

%prep
%autosetup -p1 -n otp-OTP-%{version}

%build
export ERL_TOP="${PWD}"
export CFLAGS="-Wno-error=implicit-function-declaration -O2 -g"

%configure \
    --enable-dynamic-ssl-lib \
    --enable-fips

%make_build

%install
%make_install %{?_smp_mflags}

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/%{name}/*
%exclude %dir %{_usrsrc}
%exclude %dir %{_libdir}/debug

%changelog
* Tue Jun 16 2026 Mukul Sikka <mukul.sikka@broadcom.com> 27.3.4.13-1
- Upgrade to 27.3.4.13, includes fixes for CVE-2026-42789, CVE-2026-42790,
- CVE-2026-42791, CVE-2026-48858
* Tue May 26 2026 Ajay Kaher <ajay.kaher@broadcom.com> 27.3.4.11-2
- Drop unzip BuildRequires; not needed for tar.gz source
* Tue May 26 2026 Harinadh Dommaraju <Harinadh.Dommaraju@broadcom.com> 27.3.4.11-1
- Update to 27.3.4.11
* Tue Apr 21 2026 Mukul Sikka <mukul.sikka@broadcom.com> 27.3.4.10-1
- Update to 27.3.4.10
* Mon Oct 13 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 27.3.4.3-1
- Update to 27.3.4.3
* Tue Apr 22 2025 Tapas Kundu <tapas.kundu@broadcom.com> 26.2.5.11-1
- Update to 26.2.5.11
* Thu Apr 10 2025 Tapas Kundu <tapas.kundu@broadcom.com> 26.2.5.10-1
- Update to 26.2.5.10
* Thu Dec 12 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 26.2.5-2
- Release bump for SRP compliance
* Tue Jun 18 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 26.2.5-1
- Upgrade to v26.2.5
* Fri Dec 22 2023 Harinadh D <hdommaraju@vmware.com> 25.1.2-3
- Fix CVE-2023-48795
* Thu Jun 01 2023 Nitesh Kumar <kunitesh@vmware.com> 25.1.2-2
- Bump version as a part of ncurses upgrade to v6.4
* Fri Oct 28 2022 Gerrit Photon <photon-checkins@vmware.com> 25.1.2-1
- Automatic Version Bump
* Wed Sep 28 2022 Shreenidhi Shedi <sshedi@vmware.com> 24.3.4.5-1
- Upgrade to v24.3.4.5
* Tue Mar 01 2022 Shreenidhi Shedi <sshedi@vmware.com> 23.3.2-4
- Fix binary path
* Tue Jan 11 2022 Nitesh Kumar <kunitesh@vmware.com> 23.3.2-3
- Enable FIPS, Adding ncurses-libs as Requires.
* Fri Jun 04 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 23.3.2-2
- openssl 3.0.0 support
* Mon May 03 2021 Gerrit Photon <photon-checkins@vmware.com> 23.3.2-1
- Automatic Version Bump
* Mon Apr 12 2021 Gerrit Photon <photon-checkins@vmware.com> 23.3.1-1
- Automatic Version Bump
* Wed Sep 23 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 23.1-2
- Make openssl changes
* Wed Sep 23 2020 Gerrit Photon <photon-checkins@vmware.com> 23.1-1
- Automatic Version Bump
* Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 23.0.4-1
- Automatic Version Bump
* Fri Aug 21 2020 Gerrit Photon <photon-checkins@vmware.com> 23.0.3-1
- Automatic Version Bump
* Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 23.0-1
- Automatic Version Bump
* Tue Oct 29 2019 Keerthana K <keerthanak@vmware.com> 22.1-1
- Update to latest version 22.1
* Thu Jan 31 2019 Siju Maliakkal <smaliakkal@vmware.com> 19.3-3
- Revert to old version to fix rabbitmq-server startup failure
* Fri Dec 07 2018 Ashwin H <ashwinh@vmware.com> 21.1.4-1
- Update to version 21.1.4
* Mon Sep 24 2018 Dweep Advani <dadvani@vmware.com> 21.0-1
- Update to version 21.0
* Fri Oct 13 2017 Alexey Makhalov <amakhalov@vmware.com> 19.3-2
- Remove BuildArch
* Thu Apr 06 2017 Chang Lee <changlee@vmware.com> 19.3-1
- Updated Version
* Mon Dec 12 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 19.1-1
- Initial.
