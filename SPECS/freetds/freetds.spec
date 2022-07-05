Summary:       ODBC driver manager
Name:          freetds
Version:       1.3.10
Release:       1%{?dist}
License:       GPLv2
URL:           http://www.unixodbc.org/
Group:         System Environment/Libraries
Vendor:        VMware, Inc.
Distribution:  Photon
Source0:       ftp://ftp.%{name}.org/pub/%{name}/stable/%{name}-%{version}.tar.gz
%define sha512 freetds=3d656833dd3e0150bf1c343699aeb89f6cb30b357a86a2baf94ac9f53016a793c78b5dcabfdb357106a7736ceb8d1fd25d817fa0861a4209b8093e6a5065dcf1
BuildRequires: unixODBC-devel
BuildRequires: gnutls-devel
Requires:      gnutls
Requires:      unixODBC

%description
FreeTDS is a project to document and implement the TDS (Tabular DataStream)
protocol. TDS is used by Sybase and Microsoft for client to database server
communications. FreeTDS includes call level interfaces for DB-Lib, CT-Lib,
and ODBC.

%package       devel
Summary:       Development files for unixODBC library
Group:         Development/Libraries
Requires:      %{name} = %{version}-%{release}

%description   devel
The freetds-devel package contains the files necessary for development with
the FreeTDS libraries.

%package       unixODBC
Summary:       FreeTDS ODBC Driver for unixODBC
Group:         System Environment/Libraries
Requires:      unixODBC

%description   unixODBC
The freetds-unixodbc package contains ODBC driver build for unixODBC.

%package       doc
Summary:       User documentation for FreeTDS
Group:         Documentation

%description   doc
The freetds-doc package contains the userguide and reference of FreeTDS
and can be installed even if FreeTDS main package is not installed

%prep
%autosetup

%build
%configure \
    --enable-static=no \
    --with-tdsver=auto \
    --with-unixodbc \
    --with-gnutls
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} %{?_smp_mflags} install
find %{buildroot} -name '*.a'  -delete
find %{buildroot} -name '*.la' -delete

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post unixODBC
echo "[FreeTDS]
Description = FreeTDS unixODBC Driver
Driver = %{_libdir}/libtdsodbc.so.0
Setup = %{_libdir}/libtdsodbc.so.0" | odbcinst -i -d -r > /dev/null 2>&1 || true
echo "[SQL Server]
Description = FreeTDS unixODBC Driver
Driver = %{_libdir}/libtdsodbc.so.0
Setup = %{_libdir}/libtdsodbc.so.0" | odbcinst -i -d -r > /dev/null 2>&1 || true

%preun unixODBC
odbcinst -u -d -n 'FreeTDS' > /dev/null 2>&1 || true
odbcinst -u -d -n 'SQL Server' > /dev/null 2>&1 || true

%files
%defattr(-,root,root)
%doc AUTHORS.md BUGS.md COPYING_LIB.txt COPYING.txt ChangeLog INSTALL.md NEWS.md README.md TODO.md
%{_bindir}/*
%{_mandir}/man?/*
%{_libdir}/libct.so.*
%{_libdir}/libsybdb.so.*
%config(noreplace) %{_sysconfdir}/locales.conf
%config(noreplace) %{_sysconfdir}/pool.conf
%config(noreplace) %{_sysconfdir}/freetds.conf

%files devel
%defattr (-,root,root)
%{_libdir}/*.so
%{_includedir}/*

%files unixODBC
%defattr(-,root,root)
%{_libdir}/libtdsodbc.so*

%files doc
%defattr (-,root,root)
%{_docdir}/%{name}/*

%changelog
*   Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 1.3.10-1
-   Automatic Version Bump
*   Sat Apr 24 2021 Gerrit Photon <photon-checkins@vmware.com> 1.2.21-1
-   Automatic Version Bump
*   Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 1.2.20-1
-   Automatic Version Bump
*   Thu Oct 01 2020 Dweep Advani <dadvani@vmware.com> 1.2.5-1
-   Adding package freetds
