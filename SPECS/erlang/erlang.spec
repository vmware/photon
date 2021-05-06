Name:         erlang
Summary:      erlang
Version:      23.1
Release:      2%{?dist}
Group:        Development/Languages
Vendor:       VMware, Inc.
Distribution: Photon
License:      ASL2.0
URL:          http://erlang.com
Source0:      OTP-%{version}.tar.gz
%define sha1  OTP=2d6eaefe960f52cc79d7614c11256b73174e4161
Patch0:       erlang-CVE-2021-29221.patch
BuildRequires: unzip
%description
erlang programming language

%prep
%setup -q -n otp-OTP-%{version}
%patch0 -p1

%build
export ERL_TOP=`pwd`
./otp_build autoconf
sh configure --disable-hipe --prefix=%{_prefix}

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
* Thu May 06 2021 Harinadh D <hdommaraju@vmware.com> 23.1-2
- Fix CVE-2021-29221
* Wed Nov 11 2020 Harinadh D <hdommaraju@vmware.com> 23.1-1
- Update to version 23-1 and make compatible with rabbitmq 3.8.x
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

