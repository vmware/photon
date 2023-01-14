%define srcname         postgresql
%global pgmajorversion  13
%global _pgbaseinstdir  %{_usr}/pgsql/%{pgmajorversion}
%global _pgbindir       %{_pgbaseinstdir}/bin
%global _pglibdir       %{_pgbaseinstdir}/lib/%{srcname}
%global _pgincludedir   %{_pgbaseinstdir}/include/%{srcname}
%global _pgdatadir      %{_pgbaseinstdir}/share/%{srcname}
%global _pgmandir       %{_pgdatadir}/man/%{srcname}
%global _pgdocdir       %{_pgbaseinstdir}/share/doc/%{srcname}
%define alter_weight    300

Summary:        PostgreSQL database engine
Name:           postgresql13
Version:        13.8
Release:        9%{?dist}
License:        PostgreSQL
URL:            www.postgresql.org
Group:          Applications/Databases
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://ftp.postgresql.org/pub/source/v%{version}/%{srcname}-%{version}.tar.bz2
%define sha512 %{srcname}=3b39448b291342a5e9b610d410c222aeb85f8acf95632e73e138ae316133af3dadc795a6e706f6447f543cf10df3c786da4f1afa1d91489b50eb77e2d9ed5d84

Patch0: llvm-15.x-psql-build-err-fixes.patch

BuildRequires:  clang-devel
BuildRequires:  diffutils
BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  krb5-devel
BuildRequires:  icu-devel
BuildRequires:  libedit-devel
BuildRequires:  libxml2-devel
BuildRequires:  libxslt-devel
BuildRequires:  linux-api-headers
BuildRequires:  Linux-PAM-devel
BuildRequires:  llvm-devel
BuildRequires:  openldap
BuildRequires:  perl
BuildRequires:  perl-IPC-Run
BuildRequires:  python3-devel
BuildRequires:  readline-devel
BuildRequires:  openssl-devel
BuildRequires:  systemtap-sdt-devel
BuildRequires:  systemd-devel
BuildRequires:  tar
BuildRequires:  tcl-devel
BuildRequires:  tzdata
BuildRequires:  util-linux-libs
BuildRequires:  zlib-devel

Requires:       krb5
Requires:       icu
Requires:       libedit
Requires:       libxml2
Requires:       openldap
Requires:       openssl
Requires:       readline
Requires:       systemd
Requires:       tzdata
Requires:       zlib
Requires:       %{name}-libs = %{version}-%{release}

%description
PostgreSQL is an advanced Object-Relational database management system (DBMS).
The base postgresql package contains the client programs that you'll need to
access a PostgreSQL DBMS server. These client programs can be located on the
same machine as the PostgreSQL server, or on a remote machine that accesses
a PostgreSQL server over a network connection. The PostgreSQL server can be
found in the postgresql13-server sub-package.

If you want to manipulate a PostgreSQL database on a local or remote PostgreSQL
server, you need this package. You also need to install this package
if you're installing the postgresql13-server package.

%package libs
Summary:    The shared libraries required for any PostgreSQL clients
Group:      Applications/Databases
Requires:   chkconfig
Requires(postun): chkconfig

%description libs
The postgresql13-libs package provides the essential shared libraries for any
PostgreSQL client program or interface. You will need to install this package
to use any other PostgreSQL package or any clients that need to connect to a
PostgreSQL server.

%package server
Summary:    The programs needed to create and run a PostgreSQL server
Requires:   %{name} = %{version}-%{release}
Requires:   %{name}-libs = %{version}-%{release}

%description server
PostgreSQL is an advanced Object-Relational database management system (DBMS).
The postgresql13-server package contains the programs needed to create
and run a PostgreSQL server, which will in turn allow you to create
and maintain PostgreSQL databases.

%package i18n
Summary:    Additional language files for PostgreSQL
Requires:   %{name} = %{version}-%{release}

%description i18n
The postgresql13-i18n package includes additional language files for
PostgreSQL.

%package docs
Summary:    Extra documentation for PostgreSQL

%description docs
The postgresql13-docs package includes the documentation.

%package contrib
Summary:    Contributed source and binaries distributed with PostgreSQL
Requires:   %{name} = %{version}-%{release}
Requires:   %{name}-libs = %{version}-%{release}
Requires:   %{name}-server = %{version}-%{release}

%description contrib
The postgresql13-contrib package contains various extension modules that are
included in the PostgreSQL distribution.

%package devel
Summary:    PostgreSQL development header files and libraries
Requires:   %{name} = %{version}-%{release}
Requires:   %{name}-libs = %{version}-%{release}
Requires:   clang-devel
Requires:   libxslt-devel
Requires:   llvm-devel
Requires:   perl-IPC-Run

%description devel
The postgresql13-devel package contains the header files and libraries
needed to compile C or C++ applications which will directly interact
with a PostgreSQL database management server. It also contains the ecpg
Embedded C Postgres preprocessor. You need to install this package if you
want to develop applications which will interact with a PostgreSQL server.

%package llvmjit
Summary:    Just-in-time compilation support for PostgreSQL
Requires:   %{name}-server = %{version}-%{release}
Requires:   llvm

%description llvmjit
The postgresql13-llvmjit package contains support for just-in-time
compilation with PostgreSQL queries.

%package plperl
Summary:    The Perl procedural language for PostgreSQL
Requires:   %{name}-server = %{version}-%{release}

%description plperl
The postgresql13-plperl package contains the PL/Perl procedural language,
which is an extension to the PostgreSQL database server.
Install this if you want to write database functions in Perl.

%package plpython3
Summary:    The Python3 procedural language for PostgreSQL
Requires:   %{name} = %{version}-%{release}
Requires:   %{name}-server = %{version}-%{release}
Requires:   python3-libs

%description plpython3
The postgresql13-plpython3 package contains the PL/Python3 procedural language,
which is an extension to the PostgreSQL database server.
Install this if you want to write database functions in Python 3.

%package pltcl
Summary:    The Tcl procedural language for PostgreSQL
Requires:   %{name} = %{version}-%{release}
Requires:   %{name}-server = %{version}-%{release}
Requires:   tcl

%description pltcl
PostgreSQL is an advanced Object-Relational database management
system. The %{name}-pltcl package contains the PL/Tcl language
for the backend.

%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
sed -i '/DEFAULT_PGSOCKET_DIR/s@/tmp@/run/postgresql@' src/include/pg_config_manual.h

# Note that %configure is not used here as this command relies on non-default
# values.
sh ./configure \
    --prefix=%{_pgbaseinstdir} \
    --enable-dtrace \
    --enable-thread-safety \
    --enable-nls \
    --enable-tap-tests \
    --with-icu \
    --with-ldap \
    --with-libxml \
    --with-libxslt \
    --with-llvm \
    --with-openssl \
    --with-gssapi \
    --with-libedit-preferred \
    --with-pam \
    --with-perl \
    --with-python \
    --with-readline \
    --with-systemd \
    --with-system-tzdata=%{_datadir}/zoneinfo \
    --with-tcl \
    --with-uuid=e2fs \
    --includedir=%{_pgincludedir} \
    --bindir=%{_pgbindir} \
    --datadir=%{_pgdatadir} \
    --libdir=%{_pglibdir} \
    --docdir=%{_pgdocdir} \
    --mandir=%{_pgmandir}

make world %{?_smp_mflags}

%install
make install-world DESTDIR=%{buildroot} %{?_smp_mflags}

# Remove anything related to Python 2.  These have no need to be
# around as only Python 3 is supported.
rm -f %{buildroot}%{_pgdatadir}/extension/*plpython2u* \
      %{buildroot}%{_pgdatadir}/extension/*plpythonu-* \
      %{buildroot}%{_pgdatadir}/extension/*_plpythonu.control

echo "%{_pglibdir}" > %{buildroot}%{_pgbaseinstdir}/%{srcname}.conf

# Create file lists, for --enable-nls and i18n
%find_lang ecpg-%{pgmajorversion}
%find_lang ecpglib6-%{pgmajorversion}
%find_lang initdb-%{pgmajorversion}
%find_lang libpq5-%{pgmajorversion}
%find_lang pg_archivecleanup-%{pgmajorversion}
%find_lang pg_basebackup-%{pgmajorversion}
%find_lang pg_checksums-%{pgmajorversion}
%find_lang pg_config-%{pgmajorversion}
%find_lang pg_controldata-%{pgmajorversion}
%find_lang pg_ctl-%{pgmajorversion}
%find_lang pg_dump-%{pgmajorversion}
%find_lang pg_resetwal-%{pgmajorversion}
%find_lang pg_rewind-%{pgmajorversion}
%find_lang pg_test_fsync-%{pgmajorversion}
%find_lang pg_test_timing-%{pgmajorversion}
%find_lang pg_upgrade-%{pgmajorversion}
%find_lang pg_verifybackup-%{pgmajorversion}
%find_lang pg_waldump-%{pgmajorversion}
%find_lang pgscripts-%{pgmajorversion}
%find_lang plperl-%{pgmajorversion}
cat plperl-%{pgmajorversion}.lang >> pg_i18n.lst
%find_lang plpgsql-%{pgmajorversion}
# plpython3 shares message files with plpython
%find_lang plpython-%{pgmajorversion}
cat plpython-%{pgmajorversion}.lang >> pg_i18n.lst
%find_lang pltcl-%{pgmajorversion}
cat pltcl-%{pgmajorversion}.lang >> pg_i18n.lst
%find_lang postgres-%{pgmajorversion}
%find_lang psql-%{pgmajorversion}

cat libpq5-%{pgmajorversion}.lang >> pg_i18n.lst

cat pg_config-%{pgmajorversion}.lang ecpg-%{pgmajorversion}.lang \
    ecpglib6-%{pgmajorversion}.lang >> pg_i18n.lst

cat initdb-%{pgmajorversion}.lang pg_ctl-%{pgmajorversion}.lang \
    psql-%{pgmajorversion}.lang pg_dump-%{pgmajorversion}.lang \
    pg_basebackup-%{pgmajorversion}.lang pgscripts-%{pgmajorversion}.lang >> pg_i18n.lst

cat postgres-%{pgmajorversion}.lang pg_resetwal-%{pgmajorversion}.lang \
    pg_checksums-%{pgmajorversion}.lang pg_verifybackup-%{pgmajorversion}.lang \
    pg_controldata-%{pgmajorversion}.lang plpgsql-%{pgmajorversion}.lang \
    pg_test_timing-%{pgmajorversion}.lang pg_test_fsync-%{pgmajorversion}.lang \
    pg_archivecleanup-%{pgmajorversion}.lang pg_waldump-%{pgmajorversion}.lang \
    pg_rewind-%{pgmajorversion}.lang pg_upgrade-%{pgmajorversion}.lang >> pg_i18n.lst

%if 0%{?with_check}
%check
# Run the main regression test suites in the source tree.
run_test_path()
{
  make_path="$1"
  chown -Rv nobody .
  sudo -u nobody -s /bin/bash -c "PATH=$PATH make -C $make_path -k check"
}
# SQL test suites, mostly.
run_test_path "src/test/regress"
run_test_path "src/test/isolation"
run_test_path "src/test/modules"
run_test_path "src/pl"
run_test_path "contrib"
# TAP tests
run_test_path "src/test/authentication"
run_test_path "src/test/recovery"
run_test_path "src/test/ssl"
run_test_path "src/test/subscription"
%endif

%post
/sbin/ldconfig

%posttrans
alternatives --install %{_bindir}/clusterdb clusterdb %{_pgbindir}/clusterdb %{alter_weight} \
    --slave %{_bindir}/createdb createdb %{_pgbindir}/createdb \
    --slave %{_bindir}/createuser createuser %{_pgbindir}/createuser \
    --slave %{_bindir}/dropdb dropdb %{_pgbindir}/dropdb \
    --slave %{_bindir}/dropuser dropuser %{_pgbindir}/dropuser \
    --slave %{_bindir}/pgbench pgbench %{_pgbindir}/pgbench \
    --slave %{_bindir}/pg_basebackup pg_basebackup %{_pgbindir}/pg_basebackup \
    --slave %{_bindir}/pg_config pg_config %{_pgbindir}/pg_config \
    --slave %{_bindir}/pg_dump pg_dump %{_pgbindir}/pg_dump \
    --slave %{_bindir}/pg_dumpall pg_dumpall %{_pgbindir}/pg_dumpall \
    --slave %{_bindir}/pg_isready pg_isready %{_pgbindir}/pg_isready \
    --slave %{_bindir}/pg_receivewal pg_receivewal %{_pgbindir}/pg_receivewal \
    --slave %{_bindir}/pg_restore pg_restore %{_pgbindir}/pg_restore \
    --slave %{_bindir}/pg_waldump pg_waldump %{_pgbindir}/pg_waldump \
    --slave %{_bindir}/psql psql %{_pgbindir}/psql \
    --slave %{_bindir}/reindexdb reindexdb %{_pgbindir}/reindexdb \
    --slave %{_bindir}/vacuumdb vacuumdb %{_pgbindir}/vacuumdb

/sbin/ldconfig

%postun
alternatives --remove clusterdb %{_pgbindir}/clusterdb
/sbin/ldconfig

%post libs
/sbin/ldconfig

%posttrans libs
alternatives --install %{_sysconfdir}/ld.so.conf.d/%{srcname}.conf %{srcname}.conf %{_pgbaseinstdir}/%{srcname}.conf %{alter_weight}
/sbin/ldconfig

%postun libs
alternatives --remove %{srcname}.conf %{_pgbaseinstdir}/%{srcname}.conf
/sbin/ldconfig

%posttrans devel
alternatives --install %{_includedir}/%{srcname} %{srcname} %{_pgincludedir} %{alter_weight} \
    --slave %{_bindir}/ecpg ecpg %{_pgbindir}/ecpg

/sbin/ldconfig

%postun devel
alternatives --remove %{srcname} %{_pgincludedir}
/sbin/ldconfig

%posttrans server
alternatives --install %{_bindir}/initdb initdb %{_pgbindir}/initdb %{alter_weight} \
    --slave %{_bindir}/pg_archivecleanup pg_archivecleanup %{_pgbindir}/pg_archivecleanup \
    --slave %{_bindir}/pg_checksums pg_checksums %{_pgbindir}/pg_checksums \
    --slave %{_bindir}/pg_controldata pg_controldata %{_pgbindir}/pg_controldata \
    --slave %{_bindir}/pg_ctl pg_ctl %{_pgbindir}/pg_ctl \
    --slave %{_bindir}/pg_resetwal pg_resetwal %{_pgbindir}/pg_resetwal \
    --slave %{_bindir}/pg_rewind pg_rewind %{_pgbindir}/pg_rewind \
    --slave %{_bindir}/pg_test_fsync pg_test_fsync %{_pgbindir}/pg_test_fsync \
    --slave %{_bindir}/pg_test_timing pg_test_timing %{_pgbindir}/pg_test_timing \
    --slave %{_bindir}/pg_upgrade pg_upgrade %{_pgbindir}/pg_upgrade \
    --slave %{_bindir}/pg_verifybackup pg_verifybackup %{_pgbindir}/pg_verifybackup \
    --slave %{_bindir}/postgres postgres %{_pgbindir}/postgres \
    --slave %{_bindir}/postmaster postmaster %{_pgbindir}/postmaster

/sbin/ldconfig

%postun server
alternatives --remove initdb %{_pgbindir}/initdb
/sbin/ldconfig

%posttrans contrib
alternatives --install %{_bindir}/oid2name oid2name %{_pgbindir}/oid2name %{alter_weight} \
    --slave %{_bindir}/vacuumlo vacuumlo %{_pgbindir}/vacuumlo \
    --slave %{_bindir}/pg_recvlogical pg_recvlogical %{_pgbindir}/pg_recvlogical \
    --slave %{_bindir}/pg_standby pg_standby %{_pgbindir}/pg_standby

/sbin/ldconfig

%postun contrib
alternatives --remove oid2name %{_pgbindir}/oid2name
/sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_pgbindir}/clusterdb
%{_pgbindir}/createdb
%{_pgbindir}/createuser
%{_pgbindir}/dropdb
%{_pgbindir}/dropuser
%{_pgbindir}/pgbench
%{_pgbindir}/pg_basebackup
%{_pgbindir}/pg_config
%{_pgbindir}/pg_dump
%{_pgbindir}/pg_dumpall
%{_pgbindir}/pg_isready
%{_pgbindir}/pg_receivewal
%{_pgbindir}/pg_restore
%{_pgbindir}/pg_waldump
%{_pgbindir}/psql
%{_pgbindir}/reindexdb
%{_pgbindir}/vacuumdb
%{_pgdatadir}/errcodes.txt
%{_pgmandir}/man1/clusterdb.*
%{_pgmandir}/man1/createdb.*
%{_pgmandir}/man1/createuser.*
%{_pgmandir}/man1/dropdb.*
%{_pgmandir}/man1/dropuser.*
%{_pgmandir}/man1/pgbench.*
%{_pgmandir}/man1/pg_basebackup.*
%{_pgmandir}/man1/pg_config.*
%{_pgmandir}/man1/pg_dump.*
%{_pgmandir}/man1/pg_dumpall.*
%{_pgmandir}/man1/pg_isready.*
%{_pgmandir}/man1/pg_restore.*
%{_pgmandir}/man1/psql.*
%{_pgmandir}/man1/reindexdb.*
%{_pgmandir}/man1/vacuumdb.*
%{_pgmandir}/man3/*
%{_pgmandir}/man7/*

%files libs
%defattr(-,root,root)
%{_pgbaseinstdir}/%{srcname}.conf
%{_pglibdir}/libpq.so.*
%{_pglibdir}/libecpg.so*
%{_pglibdir}/libpgtypes.so.*
%{_pglibdir}/libecpg_compat.so.*
%{_pglibdir}/libpqwalreceiver.so

%files server
%defattr(-,root,root)
%{_pgbindir}/initdb
%{_pgbindir}/pg_archivecleanup
%{_pgbindir}/pg_checksums
%{_pgbindir}/pg_controldata
%{_pgbindir}/pg_ctl
%{_pgbindir}/pg_resetwal
%{_pgbindir}/pg_rewind
%{_pgbindir}/pg_test_fsync
%{_pgbindir}/pg_test_timing
%{_pgbindir}/pg_upgrade
%{_pgbindir}/pg_verifybackup
%{_pgbindir}/postgres
%{_pgbindir}/postmaster
%{_pgmandir}/man1/initdb.*
%{_pgmandir}/man1/pg_archivecleanup.*
%{_pgmandir}/man1/pg_checksums.*
%{_pgmandir}/man1/pg_controldata.*
%{_pgmandir}/man1/pg_ctl.*
%{_pgmandir}/man1/pg_resetwal.*
%{_pgmandir}/man1/pg_receivewal.*
%{_pgmandir}/man1/pg_rewind.*
%{_pgmandir}/man1/pg_test_fsync.*
%{_pgmandir}/man1/pg_test_timing.*
%{_pgmandir}/man1/pg_upgrade.*
%{_pgmandir}/man1/pg_verifybackup.*
%{_pgmandir}/man1/pg_waldump.*
%{_pgmandir}/man1/postgres.*
%{_pgmandir}/man1/postmaster.*
%{_pgdatadir}/*.sample
%{_pgdatadir}/postgres.bki
%{_pgdatadir}/information_schema.sql
%{_pgdatadir}/snowball_create.sql
%{_pgdatadir}/sql_features.txt
%{_pgdatadir}/system_views.sql
%dir %{_pgdatadir}/extension
%{_pgdatadir}/extension/plpgsql*
%{_pgdatadir}/timezonesets/*
%{_pgdatadir}/tsearch_data/*.affix
%{_pgdatadir}/tsearch_data/*.dict
%{_pgdatadir}/tsearch_data/*.ths
%{_pgdatadir}/tsearch_data/*.rules
%{_pgdatadir}/tsearch_data/*.stop
%{_pgdatadir}/tsearch_data/*.syn
%{_pglibdir}/dict_int.so
%{_pglibdir}/dict_snowball.so
%{_pglibdir}/dict_xsyn.so
%{_pglibdir}/euc2004_sjis2004.so
%{_pglibdir}/pgoutput.so
%{_pglibdir}/plpgsql.so
%{_pglibdir}/*_and_*.so

%files i18n -f pg_i18n.lst

%files docs
%defattr(-,root,root)
%{_pgdocdir}/*

%files contrib
%defattr(-,root,root)
%{_pgbindir}/oid2name
%{_pgbindir}/vacuumlo
%{_pgbindir}/pg_recvlogical
%{_pgbindir}/pg_standby
%{_pgdatadir}/extension/adminpack*
%{_pgdatadir}/extension/amcheck*
%{_pgdatadir}/extension/autoinc*
%{_pgdatadir}/extension/bloom*
%{_pgdatadir}/extension/btree_gin*
%{_pgdatadir}/extension/btree_gist*
%{_pgdatadir}/extension/citext*
%{_pgdatadir}/extension/cube*
%{_pgdatadir}/extension/dblink*
%{_pgdatadir}/extension/dict_int*
%{_pgdatadir}/extension/dict_xsyn*
%{_pgdatadir}/extension/earthdistance*
%{_pgdatadir}/extension/file_fdw*
%{_pgdatadir}/extension/fuzzystrmatch*
%{_pgdatadir}/extension/hstore.control
%{_pgdatadir}/extension/hstore--*.sql
%{_pgdatadir}/extension/insert_username*
%{_pgdatadir}/extension/intagg*
%{_pgdatadir}/extension/intarray*
%{_pgdatadir}/extension/isn*
%{_pgdatadir}/extension/lo*
%{_pgdatadir}/extension/ltree.control
%{_pgdatadir}/extension/ltree--*.sql
%{_pgdatadir}/extension/moddatetime*
%{_pgdatadir}/extension/pageinspect*
%{_pgdatadir}/extension/pg_buffercache*
%{_pgdatadir}/extension/pg_freespacemap*
%{_pgdatadir}/extension/pg_prewarm*
%{_pgdatadir}/extension/pg_stat_statements*
%{_pgdatadir}/extension/pg_trgm*
%{_pgdatadir}/extension/pg_visibility*
%{_pgdatadir}/extension/pgcrypto*
%{_pgdatadir}/extension/pgrowlocks*
%{_pgdatadir}/extension/pgstattuple*
%{_pgdatadir}/extension/postgres_fdw*
%{_pgdatadir}/extension/refint*
%{_pgdatadir}/extension/seg*
%{_pgdatadir}/extension/sslinfo*
%{_pgdatadir}/extension/tablefunc*
%{_pgdatadir}/extension/tcn*
%{_pgdatadir}/extension/tsm_system_rows*
%{_pgdatadir}/extension/tsm_system_time*
%{_pgdatadir}/extension/unaccent*
%{_pgdatadir}/extension/uuid-ossp*
%{_pgdatadir}/extension/xml2*
%{_pgdocdir}/extension/*.example
%{_pglibdir}/_int.so
%{_pglibdir}/adminpack.so
%{_pglibdir}/amcheck.so
%{_pglibdir}/auth_delay.so
%{_pglibdir}/autoinc.so
%{_pglibdir}/auto_explain.so
%{_pglibdir}/bloom.so
%{_pglibdir}/btree_gin.so
%{_pglibdir}/btree_gist.so
%{_pglibdir}/citext.so
%{_pglibdir}/cube.so
%{_pglibdir}/dblink.so
%{_pglibdir}/earthdistance.so
%{_pglibdir}/file_fdw.so*
%{_pglibdir}/fuzzystrmatch.so
%{_pglibdir}/insert_username.so
%{_pglibdir}/isn.so
%{_pglibdir}/hstore.so
%{_pglibdir}/lo.so
%{_pglibdir}/ltree.so
%{_pglibdir}/moddatetime.so
%{_pglibdir}/pageinspect.so
%{_pglibdir}/passwordcheck.so
%{_pglibdir}/pgcrypto.so
%{_pglibdir}/pgrowlocks.so
%{_pglibdir}/pgstattuple.so
%{_pglibdir}/pg_buffercache.so
%{_pglibdir}/pg_freespacemap.so
%{_pglibdir}/pg_prewarm.so
%{_pglibdir}/pg_stat_statements.so
%{_pglibdir}/pg_trgm.so
%{_pglibdir}/pg_visibility.so
%{_pglibdir}/pgxml.so
%{_pglibdir}/postgres_fdw.so
%{_pglibdir}/refint.so
%{_pglibdir}/seg.so
%{_pglibdir}/sslinfo.so
%{_pglibdir}/tablefunc.so
%{_pglibdir}/tcn.so
%{_pglibdir}/test_decoding.so
%{_pglibdir}/tsm_system_rows.so
%{_pglibdir}/tsm_system_time.so
%{_pglibdir}/unaccent.so
%{_pglibdir}/uuid-ossp.so
%{_pgmandir}/man1/oid2name.*
%{_pgmandir}/man1/pg_recvlogical.*
%{_pgmandir}/man1/pg_standby.*
%{_pgmandir}/man1/vacuumlo.*

%files llvmjit
%defattr(-,root,root)
%{_pglibdir}/bitcode/*
%{_pglibdir}/llvmjit.so
%{_pglibdir}/llvmjit_types.bc

%files devel
%defattr(-,root,root)
%{_pgbindir}/ecpg
%{_pgincludedir}/*
%{_pglibdir}/libpq.so
%{_pglibdir}/libecpg.so
%{_pglibdir}/libpq.a
%{_pglibdir}/libecpg.a
%{_pglibdir}/libecpg_compat.so
%{_pglibdir}/libecpg_compat.a
%{_pglibdir}/libpgcommon.a
%{_pglibdir}/libpgcommon_shlib.a
%{_pglibdir}/libpgfeutils.a
%{_pglibdir}/libpgport.a
%{_pglibdir}/libpgport_shlib.a
%{_pglibdir}/libpgtypes.so
%{_pglibdir}/libpgtypes.a
%{_pglibdir}/pkgconfig/*
%{_pglibdir}/pgxs/*
%{_pgmandir}/man1/ecpg.*

%files plperl
%defattr(-,root,root)
%{_pgdatadir}/extension/bool_plperl*
%{_pgdatadir}/extension/hstore_plperl*
%{_pgdatadir}/extension/jsonb_plperl*
%{_pgdatadir}/extension/plperl*
%{_pglibdir}/bool_plperl.so
%{_pglibdir}/hstore_plperl.so
%{_pglibdir}/jsonb_plperl.so
%{_pglibdir}/plperl.so

%files pltcl
%defattr(-,root,root)
%{_pgdatadir}/extension/pltcl*
%{_pglibdir}/pltcl.so

%files plpython3
%defattr(-,root,root)
%{_pgdatadir}/extension/hstore_plpython3*
%{_pgdatadir}/extension/ltree_plpython3*
%{_pgdatadir}/extension/jsonb_plpython3*
%{_pgdatadir}/extension/plpython3*
%{_pglibdir}/hstore_plpython3.so
%{_pglibdir}/jsonb_plpython3.so
%{_pglibdir}/ltree_plpython3.so
%{_pglibdir}/plpython3.so

%changelog
* Sat Jan 14 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 13.8-9
- Bump version as a part of gettext upgrade
* Thu Jan 05 2023 Shreenidhi Shedi <sshedi@vmware.com> 13.8-8
- Use alternatives and allow parallel installation of pgsql
* Tue Dec 20 2022 Guruswamy Basavaiah <bguruswamy@vmware.com> 13.8-7
- Bump release as a part of readline upgrade
* Thu Dec 08 2022 Dweep Advani <dadvani@vmware.com> 13.8-6
- Perl version upgrade to 5.36.0
* Fri Dec 02 2022 Srinidhi Rao <srinidhir@vmware.com> 13.8-5
- Bump version as a part of systemtap upgrade
* Fri Oct 07 2022 Shreenidhi Shedi <sshedi@vmware.com> 13.8-4
- Bump version as a part of libxslt upgrade
* Thu Oct 06 2022 Shreenidhi Shedi <sshedi@vmware.com> 13.8-3
- Bump version as a part of icu upgrade
* Wed Sep 28 2022 Shreenidhi Shedi <sshedi@vmware.com> 13.8-2
- Bump version as a part of llvm upgrade
* Thu Aug 11 2022 Julien Rouhaud <jrouhaud@vmware.com> 13.8-1
- Upgraded to version 13.8.
* Thu Jun 16 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 13.7-2
- Bump version as a part of libxslt upgrade
* Fri May 13 2022 Michael Paquier <mpaquier@vmware.com> 13.7-1
- Upgraded to version 13.7.
* Mon Feb 14 2022 Michael Paquier <mpaquier@vmware.com> 13.6-1
- Upgraded to version 13.6.
* Wed Nov 17 2021 Nitesh Kumar <kunitesh@vmware.com> 13.5-2
- Release bump up to use libxml2 2.9.12-1.
* Mon Nov 15 2021 Michael Paquier <mpaquier@vmware.com> 13.5-1
- Upgraded to version 13.5.
* Thu Sep 30 2021 Michael Paquier <mpaquier@vmware.com> 13.4-1
- Add new package for PostgreSQL 13.
