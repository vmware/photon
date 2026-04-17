Name:          erlang
Summary:       erlang
Version:       27.3.4.10
Release:       1%{?dist}
Group:         Development/Languages
Vendor:        VMware, Inc.
Distribution:  Photon
License:       ASL2.0
URL:           https://www.erlang.org

Source0: https://github.com/erlang/otp/archive/refs/tags/OTP-%{version}.tar.gz
%define sha512 OTP=4234947c74b0bd74f899b0026a6c6977da82d19bcd661e3fc66a3c0573490640f7e808fff7971ac6c5a30573647240b20af1b6958e5a4c2b237e9f15589e0931

Requires:     ncurses-libs

BuildRequires: unzip
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
* Fri Apr 17 2026 Mukul Sikka <mukul.sikka@broadcom.com> 27.3.4.10-1
- Update to 27.3.4.10
* Tue Nov 18 2025 Harinadh Dommaraju <Harinadh.Dommaraju@broadcom.com> 27.3.4.3-1
- Update to 27.3.4.3
* Tue Oct 14 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 26.2.5.15-1
- Upgrade to v26.2.5.15 to fix CVEs
* Tue Apr 22 2025 Tapas Kundu <tapas.kundu@broadcom.com> 26.2.5.11-1
- Update to 26.2.5.11
* Thu Apr 10 2025 Tapas Kundu <tapas.kundu@broadcom.com> 26.2.5.10-1
- Update to 26.2.5.10
* Tue Jun 11 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 26.2.5-1
- Upgrade to v26.2.5
* Wed Nov 09 2022 Shreenidhi Shedi <sshedi@vmware.com> 25.1.2-1
- Upgrade to v25.1.2
* Tue Mar 01 2022 Shreenidhi Shedi <sshedi@vmware.com> 23.1-5
- Exclude debug symbols properly
* Tue Jan 11 2022 Nitesh Kumar <kunitesh@vmware.com> 23.1-4
- Enable FIPS, Adding ncurses-libs as Requires.
* Fri Jun 04 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 23.1-3
- openssl 3.0.0 support
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
