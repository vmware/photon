Summary:       ODBC driver manager
Name:          unixODBC
Version:       2.3.9
Release:       2%{?dist}
License:       GPLv2+ and LGPLv2+
URL:           http://www.unixodbc.org/
Group:         System Environment/Libraries
Vendor:        VMware, Inc.
Distribution:  Photon
Source0:       ftp://ftp.unixodbc.org/pub/unixODBC/%{name}-%{version}.tar.gz
%define sha512 unixODBC=6637eab751401522e0af775cb104cd07693b82927453a98e5af28e079f4b9f40e1cfab8cb36f509c46dced89b45244bc5ed1a3dda17ba5a52a844e8e82f187bb

Patch0: CVE-2024-1013.patch

BuildRequires: automake
BuildRequires: autoconf
BuildRequires: libtool

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
%autosetup -p1

%build
sh ./configure --host=%{_host} --build=%{_build} \
  CFLAGS="%{optflags}" \
  CXXFLAGS="%{optflags}" \
  --program-prefix= \
  --disable-dependency-tracking \
  --prefix=%{_prefix} \
  --exec-prefix=%{_prefix} \
  --bindir=%{_bindir} \
  --sbindir=%{_sbindir} \
  --sysconfdir=%{_sysconfdir}/%{name} \
  --datadir=%{_datadir} \
  --includedir=%{_includedir} \
  --libdir=%{_libdir} \
  --libexecdir=%{_libexecdir} \
  --localstatedir=%{_sharedstatedir}/%{name} \
  --sharedstatedir=%{_sharedstatedir} \
  --mandir=%{_mandir} \
  --infodir=%{_infodir} \
  --disable-silent-rules \
  --enable-threads=yes \
  --enable-drivers=yes \
  --enable-driverc=yes \

%make_build

%install
%make_install %{_smp_mflags}
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
%config(noreplace) %{_sysconfdir}/%{name}/odbc*
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
* Wed May 15 2024 Srish Srinivasan <srish.srinivasan@broadcom.com> 2.3.9-2
- Patched CVE-2024-1013
* Wed Sep 09 2020 Gerrit Photon <photon-checkins@vmware.com> 2.3.9-1
- Automatic Version Bump
* Wed Sep 02 2020 Gerrit Photon <photon-checkins@vmware.com> 2.3.8-2
- Fix ./configure to %configure
* Tue Sep 01 2020 Gerrit Photon <photon-checkins@vmware.com> 2.3.8-1
- Automatic Version Bump
* Mon Sep 10 2018 Michelle Wang <michellew@vmware.com> 2.3.7-1
- Update version to 2.3.7.
* Wed Oct 26 2016 Anish Swaminathan <anishs@vmware.com> 2.3.4-1
- Initial build.  First version
