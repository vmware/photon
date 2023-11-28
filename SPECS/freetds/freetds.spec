Summary:       ODBC driver manager
Name:          freetds
Version:       1.2.5
Release:       3%{?dist}
License:       GPLv2
URL:           http://www.unixodbc.org/
Group:         System Environment/Libraries
Vendor:        VMware, Inc.
Distribution:  Photon

Source0: https://www.freetds.org/files/stable/%{name}-%{version}.tar.gz
%define sha512 %{name}=5e228c0f8f3e102d1a414ef55eb0d11023218c709dfa7d9bfe70832c86f604b1fced979933491feb78570be44be5b2b08d9693ca1d3c5df0762816e772395a67

BuildRequires: unixODBC-devel
BuildRequires: gnutls-devel
BuildRequires: nettle-devel

Requires:      gnutls
Requires:      unixODBC
Requires:      nettle

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
%autosetup -p1

%build
%configure \
    --enable-static=no \
    --with-tdsver=auto \
    --with-unixodbc \
    --with-gnutls \
    --disable-static

%make_build

%install
%make_install %{?_smp_mflags}

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
* Tue Nov 28 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.2.5-3
- Bump version as a part of gnutls upgrade
* Mon May 31 2021 Shreenidhi Shedi<sshedi@vmware.com> 1.2.5-2
- Bump version to fix nettle dependancy issue.
* Thu Oct 01 2020 Dweep Advani <dadvani@vmware.com> 1.2.5-1
- Adding package freetds
