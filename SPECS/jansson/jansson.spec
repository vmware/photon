Summary:       Jansson json parser
Name:          jansson
Version:       2.9
Release:       1%{?dist}
Group:         System Environment/Libraries
Vendor:        VMware, Inc.
License:       MIT
URL:           http://www.digip.org/jansson
Source0:       http://www.digip.org/jansson/releases/%{name}-%{version}.tar.gz
%define sha1 jansson=d843b7f0b8a01c42c9caab9394120fdb53ada070
Distribution:  Photon

%description
Jansson is a C library for encoding, decoding and manipulating JSON data.

%package devel
Summary:    Development files for jansson
Group:      Development/Libraries
Requires:   jansson = %{version}-%{release}

%description devel
Development files for jansson

%prep
%setup -q

%build
./configure \
    --prefix=%{_prefix} \
    --disable-static
make

%install
make DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -delete

%post

    /sbin/ldconfig

    # First argument is 1 => New Installation
    # First argument is 2 => Upgrade

%clean
rm -rf %{buildroot}/*

%files
%doc LICENSE CHANGES
%{_libdir}/*.so.*

%files devel
%{_libdir}/*.so
%{_includedir}/*
%{_libdir}/pkgconfig/%{name}.pc

%changelog
*  Thu Jan 05 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.9-1
-  Initial
