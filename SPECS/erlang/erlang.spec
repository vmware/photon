Name:         erlang
Summary:      erlang
Version:      21.2.6
Release:      1%{?dist}
Group:        Development/Languages
Vendor:       VMware, Inc.
Distribution: Photon
License:      ASL2.0
URL:          http://erlang.com
Source0:      OTP-%{version}.tar.gz
%define sha1  OTP-%{version}.tar.gz=a0ea31c1a8b98e2c9d9416f840142c8e447a5880
Patch1: 0001-crypto-declare-extern-for-BN_GENCB-APIs.patch
BuildRequires: ncurses-devel

%description
erlang programming language

%prep
%setup -q -n otp-OTP-%{version}
%patch1 -p1

%build
export ERL_TOP=`pwd`
./otp_build autoconf
%configure --with-ssl=%{_libdir} --with-ssl-incl=%{_includedir}/openssl --with-ssl-rpath=%{_libdir} --enable-dynamic-ssl-lib
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
* Fri Mar 08 2019 Tapas Kundu <tkundu@vmware.com> 21.2.6-1
- Updated to 21.2.6
* Tue Dec 12 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 19.3-1
- Initial.

