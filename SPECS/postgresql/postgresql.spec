Summary:	PostgreSQL database engine
Name:		postgresql
Version:	9.5.3
Release:	5%{?dist}
License:	PostgreSQL
URL:		www.postgresql.org
Group:		Applications/Databases
Vendor:		VMware, Inc.
Distribution:	Photon
Provides:	%{name}

Source0:	http://ftp.postgresql.org/pub/source/v%{version}/%{name}-%{version}.tar.bz2
%define sha1 postgresql=bd8dcbc8c4882468675dcc93263182a27d4ff201

# Common libraries needed
BuildRequires:	krb5-devel
BuildRequires:	libxml2-devel
BuildRequires:	openldap
BuildRequires:	perl
BuildRequires:	readline-devel
BuildRequires:	openssl-devel
BuildRequires:	zlib-devel
BuildRequires:	tzdata
Requires:		krb5
Requires:		libxml2
Requires:		openldap
Requires:		openssl
Requires:		readline
Requires:		zlib
Requires:       tzdata

Requires:   %{name}-libs = %{version}-%{release}

%description
PostgreSQL is an object-relational database management system.

%package libs
Summary:    Libraries for use with PostgreSQL
Group:      Applications/Databases
Provides:   %{name}-libs

%description libs
The postgresql-libs package provides the essential shared libraries for any
PostgreSQL client program or interface. You will need to install this package
to use any other PostgreSQL package or any clients that need to connect to a
PostgreSQL server.

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

%{_fixperms} %{buildroot}/*

%check
chown -Rv nobody .
sudo -u nobody -s /bin/bash -c "PATH=$PATH make -k check"

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
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
%{_datadir}/postgresql/*
%{_libdir}/libpgcommon.a
%{_libdir}/libpgport.a
%{_libdir}/libpq.a
%{_libdir}/postgresql/*
%{_docdir}/postgresql/extension/*.example
%{_includedir}/postgresql/*
%exclude %{_includedir}/postgresql/informix/*
%exclude %{_includedir}/postgresql/internal/*
%exclude %{_libdir}/debug/
%exclude %{_datadir}/postgresql/pg_service.conf.sample
%exclude %{_datadir}/postgresql/psqlrc.sample

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
%{_includedir}/ecpg_config.h
%{_includedir}/ecpg_informix.h
%{_includedir}/ecpgerrno.h
%{_includedir}/ecpglib.h
%{_includedir}/ecpgtype.h
%{_includedir}/libpq-events.h
%{_includedir}/libpq-fe.h
%{_includedir}/libpq/libpq-fs.h
%{_includedir}/pg_config.h
%{_includedir}/pg_config_ext.h
%{_includedir}/pg_config_manual.h
%{_includedir}/pg_config_os.h
%{_includedir}/pgtypes_date.h
%{_includedir}/pgtypes_error.h
%{_includedir}/pgtypes_interval.h
%{_includedir}/pgtypes_numeric.h
%{_includedir}/pgtypes_timestamp.h
%{_includedir}/postgres_ext.h
%{_includedir}/postgresql/informix/*
%{_includedir}/postgresql/internal/*
%{_includedir}/sql3types.h
%{_includedir}/sqlca.h
%{_includedir}/sqlda-compat.h
%{_includedir}/sqlda-native.h
%{_includedir}/sqlda.h
%{_libdir}/libecpg*
%{_libdir}/libpgtypes*
%{_libdir}/libpq*
%{_libdir}/pkgconfig/*
%{_datadir}/postgresql/pg_service.conf.sample
%{_datadir}/postgresql/psqlrc.sample

%changelog
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
*   Tue May 15 2015 Sharath George <sharathg@vmware.com> 9.4.1-1
-   Initial build. First version
