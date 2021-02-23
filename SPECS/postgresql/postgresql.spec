Summary:        PostgreSQL database engine
Name:           postgresql
Version:        13.2
Release:        1%{?dist}
License:        PostgreSQL
URL:            www.postgresql.org
Group:          Applications/Databases
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://ftp.postgresql.org/pub/source/v%{version}/%{name}-%{version}.tar.bz2
%define sha1    postgresql=fc40c06ee7f2fd5f4ee5af88c8502f06a44c8698

# Common libraries needed
BuildRequires:  diffutils
BuildRequires:  gcc
BuildRequires:  krb5-devel
BuildRequires:  libedit-devel
BuildRequires:  libxml2-devel
BuildRequires:  linux-api-headers
BuildRequires:  openldap
BuildRequires:  perl
BuildRequires:  readline-devel
BuildRequires:  openssl-devel
BuildRequires:  tar
BuildRequires:  tzdata
BuildRequires:  zlib-devel
Requires:       krb5
Requires:       libedit
Requires:       libxml2
Requires:       openldap
Requires:       openssl
Requires:       readline
Requires:       tzdata
Requires:       zlib

Requires:   %{name}-libs = %{version}-%{release}

%description
PostgreSQL is an advanced Object-Relational database management system (DBMS).
The base postgresql package contains the client programs that you'll need to
access a PostgreSQL DBMS server. These client programs can be located on the
same machine as the PostgreSQL server, or on a remote machine that accesses
a PostgreSQL server over a network connection. The PostgreSQL server can be
found in the postgresql-server sub-package.

If you want to manipulate a PostgreSQL database on a local or remote PostgreSQL
server, you need this package. You also need to install this package
if you're installing the postgresql-server package.

%package libs
Summary:    The shared libraries required for any PostgreSQL clients
Group:      Applications/Databases

%description libs
The postgresql-libs package provides the essential shared libraries for any
PostgreSQL client program or interface. You will need to install this package
to use any other PostgreSQL package or any clients that need to connect to a
PostgreSQL server.

%package server
Summary:	The programs needed to create and run a PostgreSQL server
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-libs = %{version}-%{release}

%description server
PostgreSQL is an advanced Object-Relational database management system (DBMS).
The postgresql-server package contains the programs needed to create
and run a PostgreSQL server, which will in turn allow you to create
and maintain PostgreSQL databases.

%package docs
Summary:	Extra documentation for PostgreSQL

%description docs
The postgresql-docs package includes the documentation.

%package contrib
Summary:	Contributed source and binaries distributed with PostgreSQL
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-libs = %{version}-%{release}
Requires:	%{name}-server = %{version}-%{release}

%description contrib
The postgresql-contrib package contains various extension modules that are
included in the PostgreSQL distribution.

%package devel
Summary:	PostgreSQL development header files and libraries
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-libs = %{version}-%{release}

%description devel
The postgresql-devel package contains the header files and libraries
needed to compile C or C++ applications which will directly interact
with a PostgreSQL database management server. It also contains the ecpg
Embedded C Postgres preprocessor. You need to install this package if you
want to develop applications which will interact with a PostgreSQL server.

%prep
%setup -q

%build
sed -i '/DEFAULT_PGSOCKET_DIR/s@/tmp@/run/postgresql@' src/include/pg_config_manual.h

%configure \
    --enable-thread-safety \
    --with-ldap \
    --with-libxml \
    --with-openssl \
    --with-gssapi \
    --with-libedit-preferred \
    --with-readline \
    --with-system-tzdata=%{_datadir}/zoneinfo \
	--docdir=%{_docdir}/postgresql
make world %{?_smp_mflags}

%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make install-world DESTDIR=%{buildroot}

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
%{_bindir}/clusterdb
%{_bindir}/createdb
%{_bindir}/createuser
%{_bindir}/dropdb
%{_bindir}/dropuser
%{_bindir}/pgbench
%{_bindir}/pg_basebackup
%{_bindir}/pg_config
%{_bindir}/pg_dump
%{_bindir}/pg_dumpall
%{_bindir}/pg_isready
%{_bindir}/pg_receivewal
%{_bindir}/pg_restore
%{_bindir}/pg_waldump
%{_bindir}/psql
%{_bindir}/reindexdb
%{_bindir}/vacuumdb
%{_datadir}/postgresql/errcodes.txt
%{_mandir}/man1/clusterdb.*
%{_mandir}/man1/createdb.*
%{_mandir}/man1/createuser.*
%{_mandir}/man1/dropdb.*
%{_mandir}/man1/dropuser.*
%{_mandir}/man1/pgbench.*
%{_mandir}/man1/pg_basebackup.*
%{_mandir}/man1/pg_config.*
%{_mandir}/man1/pg_dump.*
%{_mandir}/man1/pg_dumpall.*
%{_mandir}/man1/pg_isready.*
%{_mandir}/man1/pg_restore.*
%{_mandir}/man1/psql.*
%{_mandir}/man1/reindexdb.*
%{_mandir}/man1/vacuumdb.*
%{_mandir}/man3/*
%{_mandir}/man7/*

%files libs
%defattr(-,root,root)
%{_libdir}/libpq.so.*
%{_libdir}/libecpg.so*
%{_libdir}/libpgtypes.so.*
%{_libdir}/libecpg_compat.so.*
%{_libdir}/postgresql/libpqwalreceiver.so

%files server
%defattr(-,root,root)
%{_bindir}/initdb
%{_bindir}/pg_archivecleanup
%{_bindir}/pg_checksums
%{_bindir}/pg_controldata
%{_bindir}/pg_ctl
%{_bindir}/pg_resetwal
%{_bindir}/pg_rewind
%{_bindir}/pg_test_fsync
%{_bindir}/pg_test_timing
%{_bindir}/pg_upgrade
%{_bindir}/pg_verifybackup
%{_bindir}/postgres
%{_bindir}/postmaster
%{_mandir}/man1/initdb.*
%{_mandir}/man1/pg_archivecleanup.*
%{_mandir}/man1/pg_checksums.*
%{_mandir}/man1/pg_controldata.*
%{_mandir}/man1/pg_ctl.*
%{_mandir}/man1/pg_resetwal.*
%{_mandir}/man1/pg_receivewal.*
%{_mandir}/man1/pg_rewind.*
%{_mandir}/man1/pg_test_fsync.*
%{_mandir}/man1/pg_test_timing.*
%{_mandir}/man1/pg_upgrade.*
%{_mandir}/man1/pg_verifybackup.*
%{_mandir}/man1/pg_waldump.*
%{_mandir}/man1/postgres.*
%{_mandir}/man1/postmaster.*
%{_datadir}/postgresql/*.sample
%{_datadir}/postgresql/postgres.bki
%{_datadir}/postgresql/information_schema.sql
%{_datadir}/postgresql/snowball_create.sql
%{_datadir}/postgresql/sql_features.txt
%{_datadir}/postgresql/system_views.sql
%dir %{_datadir}/postgresql/extension
%{_datadir}/postgresql/extension/plpgsql*
%{_datadir}/postgresql/timezonesets/*
%{_datadir}/postgresql/tsearch_data/*.affix
%{_datadir}/postgresql/tsearch_data/*.dict
%{_datadir}/postgresql/tsearch_data/*.ths
%{_datadir}/postgresql/tsearch_data/*.rules
%{_datadir}/postgresql/tsearch_data/*.stop
%{_datadir}/postgresql/tsearch_data/*.syn
%{_libdir}/postgresql/dict_int.so
%{_libdir}/postgresql/dict_snowball.so
%{_libdir}/postgresql/dict_xsyn.so
%{_libdir}/postgresql/euc2004_sjis2004.so
%{_libdir}/postgresql/pgoutput.so
%{_libdir}/postgresql/plpgsql.so
%{_libdir}/postgresql/*_and_*.so

%files docs
%defattr(-,root,root)
%{_docdir}/postgresql/html/*

%files contrib
%defattr(-,root,root)
%{_bindir}/oid2name
%{_bindir}/vacuumlo
%{_bindir}/pg_recvlogical
%{_bindir}/pg_standby
%{_datadir}/postgresql/extension/adminpack*
%{_datadir}/postgresql/extension/amcheck*
%{_datadir}/postgresql/extension/autoinc*
%{_datadir}/postgresql/extension/bloom*
%{_datadir}/postgresql/extension/btree_gin*
%{_datadir}/postgresql/extension/btree_gist*
%{_datadir}/postgresql/extension/citext*
%{_datadir}/postgresql/extension/cube*
%{_datadir}/postgresql/extension/dblink*
%{_datadir}/postgresql/extension/dict_int*
%{_datadir}/postgresql/extension/dict_xsyn*
%{_datadir}/postgresql/extension/earthdistance*
%{_datadir}/postgresql/extension/file_fdw*
%{_datadir}/postgresql/extension/fuzzystrmatch*
%{_datadir}/postgresql/extension/hstore.control
%{_datadir}/postgresql/extension/hstore--*.sql
%{_datadir}/postgresql/extension/insert_username*
%{_datadir}/postgresql/extension/intagg*
%{_datadir}/postgresql/extension/intarray*
%{_datadir}/postgresql/extension/isn*
%{_datadir}/postgresql/extension/lo*
%{_datadir}/postgresql/extension/ltree.control
%{_datadir}/postgresql/extension/ltree--*.sql
%{_datadir}/postgresql/extension/moddatetime*
%{_datadir}/postgresql/extension/pageinspect*
%{_datadir}/postgresql/extension/pg_buffercache*
%{_datadir}/postgresql/extension/pg_freespacemap*
%{_datadir}/postgresql/extension/pg_prewarm*
%{_datadir}/postgresql/extension/pg_stat_statements*
%{_datadir}/postgresql/extension/pg_trgm*
%{_datadir}/postgresql/extension/pg_visibility*
%{_datadir}/postgresql/extension/pgcrypto*
%{_datadir}/postgresql/extension/pgrowlocks*
%{_datadir}/postgresql/extension/pgstattuple*
%{_datadir}/postgresql/extension/postgres_fdw*
%{_datadir}/postgresql/extension/refint*
%{_datadir}/postgresql/extension/seg*
%{_datadir}/postgresql/extension/sslinfo*
%{_datadir}/postgresql/extension/tablefunc*
%{_datadir}/postgresql/extension/tcn*
%{_datadir}/postgresql/extension/tsm_system_rows*
%{_datadir}/postgresql/extension/tsm_system_time*
%{_datadir}/postgresql/extension/unaccent*
%{_datadir}/postgresql/extension/xml2*
%{_docdir}/postgresql/extension/*.example
%{_libdir}/postgresql/_int.so
%{_libdir}/postgresql/adminpack.so
%{_libdir}/postgresql/amcheck.so
%{_libdir}/postgresql/auth_delay.so
%{_libdir}/postgresql/autoinc.so
%{_libdir}/postgresql/auto_explain.so
%{_libdir}/postgresql/bloom.so
%{_libdir}/postgresql/btree_gin.so
%{_libdir}/postgresql/btree_gist.so
%{_libdir}/postgresql/citext.so
%{_libdir}/postgresql/cube.so
%{_libdir}/postgresql/dblink.so
%{_libdir}/postgresql/earthdistance.so
%{_libdir}/postgresql/file_fdw.so*
%{_libdir}/postgresql/fuzzystrmatch.so
%{_libdir}/postgresql/insert_username.so
%{_libdir}/postgresql/isn.so
%{_libdir}/postgresql/hstore.so
%{_libdir}/postgresql/lo.so
%{_libdir}/postgresql/ltree.so
%{_libdir}/postgresql/moddatetime.so
%{_libdir}/postgresql/pageinspect.so
%{_libdir}/postgresql/passwordcheck.so
%{_libdir}/postgresql/pgcrypto.so
%{_libdir}/postgresql/pgrowlocks.so
%{_libdir}/postgresql/pgstattuple.so
%{_libdir}/postgresql/pg_buffercache.so
%{_libdir}/postgresql/pg_freespacemap.so
%{_libdir}/postgresql/pg_prewarm.so
%{_libdir}/postgresql/pg_stat_statements.so
%{_libdir}/postgresql/pg_trgm.so
%{_libdir}/postgresql/pg_visibility.so
%{_libdir}/postgresql/pgxml.so
%{_libdir}/postgresql/postgres_fdw.so
%{_libdir}/postgresql/refint.so
%{_libdir}/postgresql/seg.so
%{_libdir}/postgresql/sslinfo.so
%{_libdir}/postgresql/tablefunc.so
%{_libdir}/postgresql/tcn.so
%{_libdir}/postgresql/test_decoding.so
%{_libdir}/postgresql/tsm_system_rows.so
%{_libdir}/postgresql/tsm_system_time.so
%{_libdir}/postgresql/unaccent.so
%{_mandir}/man1/oid2name.*
%{_mandir}/man1/pg_recvlogical.*
%{_mandir}/man1/pg_standby.*
%{_mandir}/man1/vacuumlo.*

%files devel
%defattr(-,root,root)
%{_bindir}/ecpg
%{_includedir}/*
%{_libdir}/libpq.so
%{_libdir}/libecpg.so
%{_libdir}/libpq.a
%{_libdir}/libecpg.a
%{_libdir}/libecpg_compat.so
%{_libdir}/libecpg_compat.a
%{_libdir}/libpgcommon.a
%{_libdir}/libpgcommon_shlib.a
%{_libdir}/libpgfeutils.a
%{_libdir}/libpgport.a
%{_libdir}/libpgport_shlib.a
%{_libdir}/libpgtypes.so
%{_libdir}/libpgtypes.a
%{_libdir}/pkgconfig/*
%{_libdir}/postgresql/pgxs/*
%{_mandir}/man1/ecpg.*

%changelog
*   Mon Feb 22 2021 Michael Paquier <mpaquier@vmware.com>
-   Redesign of the packages, splitting client, server and contrib.
*   Fri Feb 19 2021 Michael Paquier <mpaquier@vmware.com> 13.2-1
-   Upgraded to version 13.2
*   Fri Feb 5 2021 Michael Paquier <mpaquier@vmware.com> 13.1-1
-   Fix and reorganize list of BuildRequires
-   Removal of custom patch for CVE-2016-5423 committed in upstream.
-   Upgraded to version 13.1
*   Wed Sep 30 2020 Dweep Advani <dadvani@vmware.com> 13.0-3
-   Prefer libedit over readline
*   Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 13.0-2
-   openssl 1.1.1
*   Thu Sep 24 2020 Gerrit Photon <photon-checkins@vmware.com> 13.0-1
-   Automatic Version Bump
*   Thu Aug 20 2020 Gerrit Photon <photon-checkins@vmware.com> 12.4-1
-   Automatic Version Bump
*   Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 12.3-1
-   Automatic Version Bump
*   Mon Aug 12 2019 Shreenidhi Shedi <sshedi@vmware.com> 11.5-1
-   Upgraded to version 11.5
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
