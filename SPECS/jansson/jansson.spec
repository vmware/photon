Summary:       Jansson json parser
Name:          jansson
Version:       2.14.1
Release:       1%{?dist}
Group:         System Environment/Libraries
Vendor:        VMware, Inc.
URL:           https://github.com/akheron/jansson
Source0:       https://github.com/akheron/jansson/releases/download/v%{version}/%{name}-%{version}.tar.gz
Source1: license.txt
%include %{SOURCE1}
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
%autosetup -p1

%build
%configure --disable-static
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}
find %{buildroot} -name '*.la' -delete

%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck} %{?_smp_mflags}

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

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
*  Fri Jul 18 2025 Ankit Jain <ankit-aj.jain@broadcom.com> 2.14.1-1
-  Updated to version 2.14.1
*  Thu Dec 12 2024 Tapas Kundu <tapas.kundu@broadcom.com> 2.13.1-2
-  Release bump for SRP compliance
*  Wed Sep 09 2020 Gerrit Photon <photon-checkins@vmware.com> 2.13.1-1
-  Automatic Version Bump
*  Mon Sep 10 2018 Ankit Jain <ankitja@vmware.com> 2.11-1
-  Updated to version 2.11
*  Thu Mar 30 2017 Divya Thaluru <dthaluru@vmware.com> 2.10-1
-  Updated to version 2.10
*  Thu Jan 05 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.9-1
-  Initial
