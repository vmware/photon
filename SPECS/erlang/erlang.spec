Name:         erlang
Summary:      erlang
Version:      21.1.4
Release:      1%{?dist}
Group:        Development/Languages
Vendor:       VMware, Inc.
Distribution: Photon
License:      ASL2.0
URL:          https://github.com/erlang/otp
Source0:      https://github.com/erlang/otp/archive/OTP-%{version}.zip
%define sha1  OTP=295ea477fcf00b85a3ebb063ebccbd84e25e4be1
BuildRequires: unzip
%description
erlang programming language

%prep
%setup -q -n otp-OTP-%{version}

%build
export ERL_TOP=`pwd`
./otp_build autoconf
%configure --disable-hipe

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

