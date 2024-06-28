Summary:       Jansson json parser
Name:          jansson
Version:       2.13.1
Release:       1%{?dist}
Group:         System Environment/Libraries
Vendor:        VMware, Inc.
License:       MIT
URL:           http://www.digip.org/jansson
Source0:       http://www.digip.org/jansson/releases/%{name}-%{version}.tar.gz
%define sha1 %{name}-%{version}=c70e94a9f3daeb16d54fb037b3e115db3ce3372d
Distribution:  Photon

%description
Jansson is a C library for encoding, decoding and manipulating JSON data.

%package devel
Summary:    Development files for jansson
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
Development files for jansson

%prep
%setup -q

%build
./configure \
    --prefix=%{_prefix} \
    --disable-static
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -delete

%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}

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
*  Wed Sep 09 2020 Gerrit Photon <photon-checkins@vmware.com> 2.13.1-1
-  Automatic Version Bump
*  Mon Sep 10 2018 Ankit Jain <ankitja@vmware.com> 2.11-1
-  Updated to version 2.11
*  Thu Mar 30 2017 Divya Thaluru <dthaluru@vmware.com> 2.10-1
-  Updated to version 2.10
*  Thu Jan 05 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.9-1
-  Initial
