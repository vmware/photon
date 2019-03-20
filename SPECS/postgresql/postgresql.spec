Summary:        PostgreSQL database engine
Name:           postgresql
Version:        9.6.10
Release:        2%{?dist}
License:        PostgreSQL
URL:            www.postgresql.org
Group:          Applications/Databases
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://ftp.postgresql.org/pub/source/v%{version}/%{name}-%{version}.tar.bz2
%define sha1    postgresql=860ff3e2ce42246f45db1fc4519f972228168242
# Common libraries needed
BuildRequires:  krb5
BuildRequires:  libxml2-devel
BuildRequires:  openldap
BuildRequires:  perl
BuildRequires:  readline-devel
BuildRequires:  openssl-devel
BuildRequires:  zlib-devel
BuildRequires:  tzdata
Requires:       krb5
Requires:       libxml2
Requires:       openldap
Requires:       openssl
Requires:       readline
Requires:       zlib
Requires:       tzdata

Requires:       %{name}-libs = %{version}-%{release}

%description
PostgreSQL is an object-relational database management system.

%package libs
Summary:        Libraries for use with PostgreSQL
Group:          Applications/Databases

%description    libs
The postgresql-libs package provides the essential shared libraries for any
PostgreSQL client program or interface. You will need to install this package
to use any other PostgreSQL package or any clients that need to connect to a
PostgreSQL server.

%package        devel
Summary:        Development files for postgresql.
Group:          Development/Libraries
Requires:       postgresql = %{version}-%{release}

%description    devel
The postgresql-devel package contains libraries and header files for
developing applications that use postgresql.

%prep
%setup -q
%build
sed -i '/DEFAULT_PGSOCKET_DIR/s@/tmp@/run/postgresql@' src/include/pg_config_manual.h &&
./configure \
    --enable-thread-safety \
    --prefix=%{_prefix} \
    --with-ldap \
    --with-libxml \
    --with-openssl \
    --with-gssapi \
    --with-readline \
    --with-system-tzdata=%{_datadir}/zoneinfo \
    --docdir=%{_docdir}/postgresql
make %{?_smp_mflags}
cd contrib && make %{?_smp_mflags}

%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make install DESTDIR=%{buildroot}
cd contrib && make install DESTDIR=%{buildroot}
find %{buildroot}/%{_libdir} -name '*.a' -delete
%{_fixperms} %{buildroot}/*
%check
%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig
%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/initdb
%{_bindir}/oid2name
%{_bindir}/pg_archivecleanup
%{_bindir}/pg_basebackup
%{_bindir}/pg_controldata
%{_bindir}/pg_ctl
%{_bindir}/pg_receivexlog
%{_bindir}/pg_recvlogical
%{_bindir}/pg_resetxlog
%{_bindir}/pg_rewind
%{_bindir}/pg_standby
%{_bindir}/pg_test_fsync
%{_bindir}/pg_test_timing
%{_bindir}/pg_upgrade
%{_bindir}/pg_xlogdump
%{_bindir}/pgbench
%{_bindir}/postgres
%{_bindir}/postmaster
%{_bindir}/vacuumlo
%{_libdir}/postgresql/*
%{_docdir}/postgresql/extension/*.example
%exclude %{_datadir}/postgresql/pg_service.conf.sample
%exclude %{_datadir}/postgresql/psqlrc.sample
%{_datadir}/postgresql/*

%files libs
%{_bindir}/clusterdb
%{_bindir}/createdb
%{_bindir}/createlang
%{_bindir}/createuser
%{_bindir}/dropdb
%{_bindir}/droplang
%{_bindir}/dropuser
%{_bindir}/ecpg
%{_bindir}/pg_config
%{_bindir}/pg_dump
%{_bindir}/pg_dumpall
%{_bindir}/pg_isready
%{_bindir}/pg_restore
%{_bindir}/psql
%{_bindir}/reindexdb
%{_bindir}/vacuumdb
%{_libdir}/libecpg*.so.*
%{_libdir}/libpgtypes*.so.*
%{_libdir}/libpq*.so.*
%{_datadir}/postgresql/pg_service.conf.sample
%{_datadir}/postgresql/psqlrc.sample

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{_libdir}/libecpg*.so
%{_libdir}/libpgtypes*.so
%{_libdir}/libpq*.so

%changelog
*   Wed Mar 20 2019 Tapas Kundu <tkundu@vmware.com> 9.6.10-2
-   Bumped up to use latest openssl
*   Tue Aug 21 2018 Keerthana K <keerthanak@vmware.com> 9.6.10-1
-   Updated to version 9.6.10 to fix CVE-2018-10915, CVE-2018-10925.
*   Mon Jun 04 2018 Xiaolin Li <xiaolinl@vmware.com> 9.6.9-1
-   Updated to version 9.6.9
*   Tue Mar 27 2018 Dheeraj Shetty <dheerajs@vmware.com> 9.6.8-1
-   Updated to version 9.6.8 to fix CVE-2018-1058
*   Mon Feb 12 2018 Dheeraj Shetty <dheerajs@vmware.com> 9.6.7-1
-   Updated to version 9.6.7
*   Mon Nov 27 2017 Xiaolin Li <xiaolinl@vmware.com> 9.6.6-1
-   Updated to version 9.6.6
*   Fri Sep 08 2017 Xiaolin Li <xiaolinl@vmware.com> 9.6.5-1
-   Updated to version 9.6.5
*   Tue Aug 15 2017 Xiaolin Li <xiaolinl@vmware.com> 9.6.4-1
-   Upgraded to version 9.6.4
*   Fri Jun 16 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 9.6.3-1
-   Upgraded to version 9.6.3
*   Tue Jun 06 2017 Divya Thaluru <dthaluru@vmware.com> 9.5.7-1
-   Upgraded to version 9.5.7
*   Mon May 01 2017 Xiaolin Li <xiaolinl@vmware.com> 9.5.4-3
-   Removed Provides section from main libs packages. Removed static lib files.
*   Thu Apr 13 2017 Xiaolin Li <xiaolinl@vmware.com> 9.5.4-2
-   Added postgresql-devel.
*   Wed Apr 05 2017 Xiaolin Li <xiaolinl@vmware.com> 9.5.4-1
-   Updated to version 9.5.4.
*   Thu Dec 15 2016 Xiaolin Li <xiaolinl@vmware.com> 9.5.3-4
-   Applied CVE-2016-5423.patch
*   Thu May 26 2016 Xiaolin Li <xiaolinl@vmware.com> 9.5.3-3
-   Add tzdata to buildrequires and requires.
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 9.5.3-2
-   GA - Bump release of all rpms
*   Fri May 20 2016 Divya Thaluru <dthaluru@vmware.com> 9.5.3-1
-   Updated to version 9.5.3
*   Wed Apr 13 2016 Michael Paquier <mpaquier@vmware.com> 9.5.2-1
-   Updated to version 9.5.2
*   Tue Feb 23 2016 Xiaolin Li <xiaolinl@vmware.com> 9.5.1-1
-   Updated to version 9.5.1
*   Thu Jan 21 2016 Xiaolin Li <xiaolinl@vmware.com> 9.5.0-1
-   Updated to version 9.5.0
*   Thu Aug 13 2015 Divya Thaluru <dthaluru@vmware.com> 9.4.4-1
-   Update to version 9.4.4.
*   Mon Jul 13 2015 Alexey Makhalov <amakhalov@vmware.com> 9.4.1-2
-   Exclude /usr/lib/debug
*   Tue May 15 2015 Sharath George <sharathg@vmware.com> 9.4.1-1
-   Initial build.  First version
