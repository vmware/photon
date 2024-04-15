Summary:       ODBC driver manager
Name:          unixODBC
Version:       2.3.12
Release:       1%{?dist}
License:       GPLv2+ and LGPLv2+
URL:           http://www.unixodbc.org/
Group:         System Environment/Libraries
Vendor:        VMware, Inc.
Distribution:  Photon
Source0: ftp://ftp.unixodbc.org/pub/unixODBC/%{name}-%{version}.tar.gz
%define sha512 %{name}=ca9d8db943195679a44db1fc09391dc6662ab1721112c93d448f04011e98502462ffe14b8364eb03707d851db456eced20eb61a22370392ca88d917038d45b56

BuildRequires: automake
BuildRequires: autoconf
BuildRequires: libtool

Patch0: PostgreSQL-driver-fix.patch

%description
The unixODBC package is an Open Source ODBC (Open DataBase Connectivity) sub-system and an ODBC SDK for Linux, Mac OSX, and UNIX.
ODBC is an open specification for providing application developers with a predictable API with which to access data sources.

%package devel
Summary: Development files for unixODBC library
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
To develop programs that will access data through
ODBC, you need to install this package.

%prep

%autosetup -p1

%build
%configure --enable-threads=yes        \
            --enable-drivers=yes        \
            --enable-driverc=yes
make %{?_smp_mflags}

%install
make %{?_smp_mflags} DESTDIR=%{buildroot} install
find doc -name "Makefile*" -delete
rm -rf %{buildroot}%{_libdir}/*.a \
       %{buildroot}%{_libdir}/*.la \
       %{buildroot}%{_libdir}/libltdl.* \
       %{buildroot}%{_datadir}/libtool

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc README COPYING AUTHORS ChangeLog NEWS doc
%config(noreplace) %{_sysconfdir}/odbc*
%{_bindir}/odbcinst
%{_bindir}/isql
%{_bindir}/dltest
%{_bindir}/iusql
%{_bindir}/odbc_config
%{_bindir}/slencheck
%{_libdir}/*.so.*
%{_mandir}/man*/*

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig

%changelog
*   Tue Apr 30 2024 Roye Eshed <roye.eshed@broadcom.com> 2.3.12-1
-   Update to 2.3.12 and Fix for CVE-2024-1013
*   Mon Sep 10 2018 Michelle Wang <michellew@vmware.com> 2.3.7-1
-   Update version to 2.3.7.
*   Wed Oct 26 2016 Anish Swaminathan <anishs@vmware.com> 2.3.4-1
-   Initial build.  First version
