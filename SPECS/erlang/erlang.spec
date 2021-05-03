Name:          erlang
Summary:       erlang
Version:       23.3.2
Release:       1%{?dist}
Group:         Development/Languages
Vendor:        VMware, Inc.
Distribution:  Photon
License:       ASL2.0
URL:           http://erlang.com
Source0:       OTP-%{version}.tar.gz
%define sha1   OTP=f3da06d9bfd1ad15fc2c72a08d45cbf8cb8bed55
BuildRequires: unzip
BuildRequires: openssl-devel
%description
erlang programming language

%prep
%setup -q -n otp-OTP-%{version}

%build
export ERL_TOP=`pwd`
./otp_build autoconf
%configure \
    --with-ssl=%{_libdir} \
    --with-ssl-incl=%{_includedir}/openssl \
    --with-ssl-rpath=%{_libdir} \
    --enable-dynamic-ssl-lib
make

%install
make install DESTDIR=$RPM_BUILD_ROOT

%post

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*
%exclude /usr/src
%exclude %{_libdir}/debug

%changelog
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
