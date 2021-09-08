Name:         erlang
Summary:      erlang
Version:      23.1
Release:      3%{?dist}
Group:        Development/Languages
Vendor:       VMware, Inc.
Distribution: Photon
License:      ASL2.0
URL:          http://erlang.com
Source0:      OTP-%{version}.tar.gz
%define sha1  OTP=2d6eaefe960f52cc79d7614c11256b73174e4161
Patch0:       0001-erlang-fix-vernemq-build-fail.patch
Patch1:       0001-crypto-declare-extern-for-BN_GENCB-APIs.patch
BuildRequires: unzip
BuildRequires: openssl-devel
%description
erlang programming language

%prep
%autosetup -p1 -n otp-OTP-%{version}

%build
export ERL_TOP=`pwd`
export CFLAGS="-Wno-error=implicit-function-declaration"
./otp_build autoconf
%configure --with-ssl=%{_libdir} --with-ssl-incl=%{_includedir}/openssl --with-ssl-rpath=%{_libdir} --enable-dynamic-ssl-lib
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot} %{?_smp_mflags}

%post

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*
%exclude /usr/src
%exclude %{_libdir}/debug

%changelog
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
