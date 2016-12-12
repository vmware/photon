Name:      erlang
Summary:   erlang
Version:   19.1
Release:   1
Group:     Development/Languages
Vendor:    VMware, Inc.
License:   ASL2.0
URL:       http://erlang.com
BuildArch: x86_64
Source0:   OTP-%{version}.tar.gz
%define sha1 OTP-19.1=e5e0fa26b0128e50904c57fd9d77b798df309c84

%description
erlang programming language

%prep
%setup -q -n otp-OTP-%{version}

%build
export ERL_TOP=`pwd`
./otp_build autoconf
./configure \
    --prefix=%{_prefix}

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
* Mon Dec 12 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 19.1-1
- Initial.

