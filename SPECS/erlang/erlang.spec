Name:          erlang
Summary:       erlang
Version:       23.3.2
Release:       4%{?dist}
Group:         Development/Languages
Vendor:        VMware, Inc.
Distribution:  Photon
License:       ASL2.0
URL:           http://erlang.com

Source0:       OTP-%{version}.tar.gz
%define sha512  OTP=bb3dc1d827314b71f7e4da2082681e449859a69589d566a810baf554131e239ad3fe0555f352d69506467162016d6c6864abb20926843ee4da5876b26650810e

Patch0:        0001-erlang-fix-vernemq-build-fail.patch

Requires:     ncurses-libs

BuildRequires: unzip
BuildRequires: openssl-devel
%description
erlang programming language

%prep
%autosetup -p1 -n otp-OTP-%{version}

%build
export ERL_TOP="${PWD}"
export CFLAGS="-Wno-error=implicit-function-declaration"

sh ./otp_build autoconf

%configure \
    --with-ssl=%{_libdir} \
    --with-ssl-incl=%{_includedir}/openssl \
    --with-ssl-rpath=%{_libdir} \
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
