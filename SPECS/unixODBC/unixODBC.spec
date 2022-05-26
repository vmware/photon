Summary:       ODBC driver manager
Name:          unixODBC
Version:       2.3.11
Release:       1%{?dist}
License:       GPLv2+ and LGPLv2+
URL:           http://www.unixodbc.org/
Group:         System Environment/Libraries
Vendor:        VMware, Inc.
Distribution:  Photon
Source0:       ftp://ftp.unixodbc.org/pub/unixODBC/%{name}-%{version}.tar.gz
%define sha512   unixODBC=dddc32f90a7962e6988e1130a8093c6fb8b9ff532cad270d572250324aecbc739f45f9d8021d217313910bab25b08e69009b4f87456575535e93be1f46f5f13d
BuildRequires: automake autoconf libtool

%description
The unixODBC package is an Open Source ODBC (Open DataBase Connectivity) sub-system and an ODBC SDK for Linux, Mac OSX, and UNIX.
ODBC is an open specification for providing application developers with a predictable API with which to access data sources.

%package       devel
Summary:       Development files for unixODBC library
Group:         Development/Libraries
Requires:      %{name} = %{version}-%{release}

%description   devel
To develop programs that will access data through
ODBC, you need to install this package.

%prep
%autosetup

%build
%configure \
           --enable-threads=yes        \
           --enable-drivers=yes        \
           --enable-driverc=yes
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} %{?_smp_mflags} install
find doc -name "Makefile*" -delete
chmod 644 doc/{lst,ProgrammerManual/Tutorial}/*
install -v -m755 -d /usr/share/doc/%{name}-%{version}
cp -v -R doc/* /usr/share/doc/%{name}-%{version}
rm -f %{buildroot}%{_libdir}/*.a
rm -f %{buildroot}%{_libdir}/*.la
rm -f %{buildroot}%{_libdir}/libltdl.*
rm -rf %{buildroot}%{_datadir}/libtool

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
*   Thu May 26 2022 Gerrit Photon <photon-checkins@vmware.com> 2.3.11-1
-   Automatic Version Bump
*   Wed Sep 09 2020 Gerrit Photon <photon-checkins@vmware.com> 2.3.9-1
-   Automatic Version Bump
*   Wed Sep 02 2020 Gerrit Photon <photon-checkins@vmware.com> 2.3.8-2
-   Fix ./configure to %configure
*   Tue Sep 01 2020 Gerrit Photon <photon-checkins@vmware.com> 2.3.8-1
-   Automatic Version Bump
*   Mon Sep 10 2018 Michelle Wang <michellew@vmware.com> 2.3.7-1
-   Update version to 2.3.7.
*   Wed Oct 26 2016 Anish Swaminathan <anishs@vmware.com> 2.3.4-1
-   Initial build.  First version
