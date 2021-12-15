Summary:        PostgreSQL database engine
Name:           postgresql
Version:        10.19
Release:        2%{?dist}
License:        PostgreSQL
URL:            www.postgresql.org
Group:          Applications/Databases
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://ftp.postgresql.org/pub/source/v%{version}/%{name}-%{version}.tar.bz2
%define sha1    postgresql=f44edcc4d612f6a1b39c233ee7b1e80feb6d0456
# Common libraries needed
BuildRequires:  krb5-devel
BuildRequires:  libxml2-devel
BuildRequires:  openldap
BuildRequires:  perl
BuildRequires:  readline-devel
BuildRequires:  openssl-devel
BuildRequires:  zlib-devel
BuildRequires:  tzdata
BuildRequires:  systemd-devel
Requires:       krb5
Requires:       libxml2
Requires:       openldap
Requires:       openssl
Requires:       readline
Requires:       zlib
Requires:       tzdata
Requires:       systemd

Requires:   %{name}-libs = %{version}-%{release}

%description
PostgreSQL is an object-relational database management system.

%package libs
Summary:    Libraries for use with PostgreSQL
Group:      Applications/Databases

%description libs
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
%autosetup -p1

%build
sed -i '/DEFAULT_PGSOCKET_DIR/s@/tmp@/run/postgresql@' src/include/pg_config_manual.h &&
%configure \
    --enable-thread-safety \
    --with-ldap \
    --with-libxml \
    --with-openssl \
    --with-gssapi \
    --with-uuid=e2fs \
    --with-readline \
    --with-systemd \
    --with-system-tzdata=%{_datadir}/zoneinfo \
    --docdir=%{_docdir}/postgresql
make %{?_smp_mflags}
cd contrib && make %{?_smp_mflags}

%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make install DESTDIR=%{buildroot} %{?_smp_mflags}
cd contrib && make install DESTDIR=%{buildroot} %{?_smp_mflags}

# For postgresql 10+, commands are renamed
# Ref: https://wiki.postgresql.org/wiki/New_in_postgres_10
ln -sf pg_receivewal %{buildroot}%{_bindir}/pg_receivexlog
ln -sf pg_resetwal %{buildroot}%{_bindir}/pg_resetxlog
ln -sf  pg_waldump %{buildroot}%{_bindir}/pg_xlogdump
%{_fixperms} %{buildroot}/*

%check
sed -i '2219s/",/  ; EXIT_STATUS=$? ; sleep 5 ; exit $EXIT_STATUS",/g'  src/test/regress/pg_regress.c
chown -Rv nobody .
sudo -u nobody -s /bin/bash -c "PATH=$PATH make -k check"

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
%{_bindir}/pg_receivewal
%{_bindir}/pg_receivexlog
%{_bindir}/pg_recvlogical
%{_bindir}/pg_resetwal
%{_bindir}/pg_resetxlog
%{_bindir}/pg_rewind
%{_bindir}/pg_standby
%{_bindir}/pg_test_fsync
%{_bindir}/pg_test_timing
%{_bindir}/pg_upgrade
%{_bindir}/pg_waldump
%{_bindir}/pg_xlogdump
%{_bindir}/pgbench
%{_bindir}/postgres
%{_bindir}/postmaster
%{_bindir}/vacuumlo
%{_datadir}/postgresql/*
%{_libdir}/postgresql/*
%{_docdir}/postgresql/extension/*.example
%exclude %{_datadir}/postgresql/pg_service.conf.sample
%exclude %{_datadir}/postgresql/psqlrc.sample

%files libs
%{_bindir}/clusterdb
%{_bindir}/createdb
%{_bindir}/createuser
%{_bindir}/dropdb
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
%{_libdir}/libpgcommon.a
%{_libdir}/libpgfeutils.a
%{_libdir}/libpgport.a
%{_libdir}/libpq.a
%{_libdir}/libecpg.a
%{_libdir}/libecpg_compat.a
%{_libdir}/libpgtypes.a

%changelog
*   Thu Nov 18 2021 Nitesh Kumar <kunitesh@vmware.com> 10.19-2
-   Version bump up to use libxml2 2.9.11-4.
*   Mon Nov 15 2021 Michael Paquier <mpaquier@vmware.com> 10.19-1
-   update version to 10.19
*   Sat Aug 14 2021 Michael Paquier <mpaquier@vmware.com> 10.18-1
-   update version to 10.18
*   Fri May 14 2021 Michael Paquier <mpaquier@vmware.com> 10.17-1
-   update version to 10.17
*   Thu Feb 18 2021 Michael Paquier <mpaquier@vmware.com> 10.16-1
-   update version to 10.16
*   Thu Nov 19 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 10.15-1
-   update version to 10.15
*   Wed Sep 02 2020 Dweep Advani <dadvani@vmware.com> 10.10-5
-   Patched for CVE-2020-14349 and CVE-2020-14350
*   Fri Apr 03 2020 Anisha Kumari <kanisha@vmware.com> 10.10-4
-   added patch to fix CVE-2020-1720
*   Mon Sep 02 2019 Satya Naga Vasamsetty <svasamsetty@vmware.com> 10.10-3
-   add uuid with e2fs configuration
*   Thu Aug 29 2019 Satya Naga Vasamsetty <svasamsetty@vmware.com> 10.10-2
-   configure with systemd
*   Fri Aug 09 2019 Siju Maliakkal <smaliakkal@vmware.com> 10.10-1
-   Upgrade to 10.10 for 2019-10208
*   Tue Jun 25 2019 Siju Maliakkal <smaliakkal@vmware.com> 10.9-1
-   Upgrade to 10.9 for CVE-2019-10164
*   Tue Apr 09 2019 Dweep Advani <dadvani@vmware.com> 10.5-2
-   Fixed CVE-2018-16850
*   Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> 10.5-1
-   Updated to version 10.5
*   Tue Mar 27 2018 Dheeraj Shetty <dheerajs@vmware.com> 9.6.8-1
-   Updated to version 9.6.8 to fix CVE-2018-1058
*   Mon Feb 12 2018 Dheeraj Shetty <dheerajs@vmware.com> 9.6.7-1
-   Updated to version 9.6.7
*   Mon Nov 27 2017 Xiaolin Li <xiaolinl@vmware.com> 9.6.6-1
-   Updated to version 9.6.6
*   Fri Sep 08 2017 Xiaolin Li <xiaolinl@vmware.com> 9.6.5-1
-   Updated to version 9.6.5
*   Tue Aug 15 2017 Xiaolin Li <xiaolinl@vmware.com> 9.6.4-1
-   Updated to version 9.6.4
*   Thu Aug 10 2017 Rongrong Qiu <rqiu@vmware.com> 9.6.3-3
-   add sleep 5 when initdb in make check for bug 1900371
*   Wed Jul 05 2017 Divya Thaluru <dthaluru@vmware.com> 9.6.3-2
-   Added postgresql-devel
*   Tue Jun 06 2017 Divya Thaluru <dthaluru@vmware.com> 9.6.3-1
-   Upgraded to 9.6.3
*   Mon Apr 03 2017 Rongrong Qiu <rqiu@vmware.com> 9.6.2-1
-   Upgrade to 9.6.2 for Photon upgrade bump
*   Thu Dec 15 2016 Xiaolin Li <xiaolinl@vmware.com> 9.5.3-6
-   Applied CVE-2016-5423.patch
*   Thu Nov 24 2016 Alexey Makhalov <amakhalov@vmware.com> 9.5.3-5
-   Required krb5-devel.
*   Mon Oct 03 2016 ChangLee <changLee@vmware.com> 9.5.3-4
-   Modified %check
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
*   Fri May 15 2015 Sharath George <sharathg@vmware.com> 9.4.1-1
-   Initial build. First version
