Name:          erlang
Summary:       erlang
Version:       26.2.5
Release:       1%{?dist}
Group:         Development/Languages
Vendor:        VMware, Inc.
Distribution:  Photon
License:       ASL2.0
URL:           https://www.erlang.org

Source0: https://github.com/erlang/otp/archive/refs/tags/OTP-%{version}.tar.gz
%define sha512 OTP=f06d34290c0d93609aa3efbdc97206e8d3ce17aa2c3f62b6c566c7631ee3a3d45a89b61ce0ace81604b5a94610d03ad98558f27ee888ca90ecdeeeb2759c0184

Patch0: 0001-erlang-fix-vernemq-build-fail.patch
Patch1: 0002-lib-crypto-c_src-crypto.c-load-fips-provider-in-fips.patch

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
* Tue Jun 18 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 26.2.5-1
- Upgrade to v26.2.5
* Sun Nov 19 2023 Shreenidhi Shedi <sshedi@vmware.com> 25.1.2-3
- Bump version as a part of openssl upgrade
* Fri Jun 09 2023 Nitesh Kumar <kunitesh@vmware.com> 25.1.2-2
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
