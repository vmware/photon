%global build_if %{photon_subrelease} >= 91

%define srcname         postgresql
%global pgmajorversion  18
%global _pgbaseinstdir  %{_usr}/pgsql/%{pgmajorversion}
%global _pgbindir       %{_pgbaseinstdir}/bin
%global _pglibdir       %{_pgbaseinstdir}/lib/%{srcname}
%global _pgincludedir   %{_pgbaseinstdir}/include/%{srcname}
%global _pgdatadir      %{_pgbaseinstdir}/share/%{srcname}
%global _pgmandir       %{_pgdatadir}/man/%{srcname}
%global _pgdocdir       %{_pgbaseinstdir}/share/doc/%{srcname}
%define alter_weight    700
%global service_name    %{name}.service

Summary:        PostgreSQL database engine
Name:           postgresql18
Version:        18.3
Release:        5%{?dist}
URL:            www.postgresql.org
Group:          Applications/Databases
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://ftp.postgresql.org/pub/source/v%{version}/%{srcname}-%{version}.tar.bz2

Source1: %{srcname}.tmpfiles.d
Source2: %{srcname}.service
Source3: %{srcname}-check-db-dir.in
Source4: %{srcname}-env-vars.conf
Source5: %{srcname}.preset
Source6: %{srcname}.sysusers
Source7: systemd-unit-instructions

Source8: license-postgresql18.txt
%include %{SOURCE8}

Source9: pgsql-gen-i18n.sh

BuildRequires: bison
BuildRequires: docbook-xml
BuildRequires: docbook-xsl
BuildRequires: clang-devel
BuildRequires: gettext
BuildRequires: krb5-devel
BuildRequires: icu-devel
BuildRequires: libedit-devel
BuildRequires: libxml2-devel
BuildRequires: libxslt-devel
BuildRequires: Linux-PAM-devel
BuildRequires: llvm-devel
BuildRequires: lz4-devel
BuildRequires: openldap-devel
BuildRequires: perl
BuildRequires: perl-IPC-Run
BuildRequires: python3-devel
BuildRequires: readline-devel
BuildRequires: openssl-devel
BuildRequires: systemtap-sdt-devel
BuildRequires: boost-devel
BuildRequires: systemd-devel
BuildRequires: systemd-rpm-macros
BuildRequires: tar
BuildRequires: tcl-devel
BuildRequires: tzdata
BuildRequires: util-linux-libs
BuildRequires: zlib-devel

Requires: %{name}-client = %{version}-%{release}
Requires: %{name}-server = %{version}-%{release}

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

%package client
Summary:  Postgresql client binaries
Requires: krb5
Requires: icu
Requires: libedit
Requires: libxml2
Requires: lz4
Requires: readline
Requires: systemd
Requires: tzdata
Requires: zlib
Requires: %{name}-libs = %{version}-%{release}

%description client
%{summary}

%package libs
Summary:    The shared libraries required for any PostgreSQL clients
Group:      Applications/Databases
Requires:   krb5
Requires:   openldap
Requires:   openssl
Requires:   alternatives
Requires(postun): alternatives

%description libs
The postgresql-libs package provides the essential shared libraries for any
PostgreSQL client program or interface. You will need to install this package
to use any other PostgreSQL package or any clients that need to connect to a
PostgreSQL server.

%package server
Summary:    The programs needed to create and run a PostgreSQL server
Requires:   %{name} = %{version}-%{release}
Requires:   %{name}-libs = %{version}-%{release}
Requires(pre): shadow

%description server
PostgreSQL is an advanced Object-Relational database management system (DBMS).
The postgresql-server package contains the programs needed to create
and run a PostgreSQL server, which will in turn allow you to create
and maintain PostgreSQL databases.

%package i18n
Summary:    Additional language files for PostgreSQL
Requires:   %{name} = %{version}-%{release}

%description i18n
The postgresql-i18n package includes additional language files for
PostgreSQL.

%package docs
Summary:    Extra documentation for PostgreSQL

%description docs
The postgresql-docs package includes the documentation.

%package contrib
Summary:    Contributed source and binaries distributed with PostgreSQL
Requires:   %{name} = %{version}-%{release}
Requires:   %{name}-libs = %{version}-%{release}
Requires:   %{name}-server = %{version}-%{release}

%description contrib
The postgresql-contrib package contains various extension modules that are
included in the PostgreSQL distribution.

%package devel
Summary:    PostgreSQL development header files and libraries
Requires:   %{name} = %{version}-%{release}
Requires:   %{name}-libs = %{version}-%{release}
Requires:   clang-devel
Requires:   icu-devel
Requires:   krb5-devel
Requires:   libedit-devel
Requires:   libxml2-devel
Requires:   libxslt-devel
Requires:   llvm-devel
Requires:   lz4-devel
Requires:   openldap
Requires:   openssl-devel
Requires:   perl-IPC-Run
Requires:   python3-devel
Requires:   readline-devel

%description devel
The postgresql-devel package contains the header files and libraries
needed to compile C or C++ applications which will directly interact
with a PostgreSQL database management server. It also contains the ecpg
Embedded C Postgres preprocessor. You need to install this package if you
want to develop applications which will interact with a PostgreSQL server.

%package llvmjit
Summary:    Just-in-time compilation support for PostgreSQL
Requires:   %{name}-server = %{version}-%{release}
Requires:   llvm

%description llvmjit
The postgresql-llvmjit package contains support for just-in-time
compilation with PostgreSQL queries.

%package plperl
Summary:    The Perl procedural language for PostgreSQL
Requires:   %{name}-server = %{version}-%{release}

%description plperl
The postgresql-plperl package contains the PL/Perl procedural language,
which is an extension to the PostgreSQL database server.
Install this if you want to write database functions in Perl.

%package plpython3
Summary:    The Python3 procedural language for PostgreSQL
Requires:   %{name} = %{version}-%{release}
Requires:   %{name}-server = %{version}-%{release}
Requires:   python3-libs

%description plpython3
The postgresql-plpython3 package contains the PL/Python3 procedural language,
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
sed -i '/DEFAULT_PGSOCKET_DIR/s@/tmp@/run/%{srcname}@' src/include/pg_config_manual.h

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
    --with-lz4 \
    --with-ssl=openssl \
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

%make_build world

%install
%make_install install-world

%include %{SOURCE7}

echo "%{_pglibdir}" > %{buildroot}%{_pgbaseinstdir}/%{srcname}.conf

%include %{SOURCE9}

%if 0%{?with_check}
%check
# Run the main regression test suites in the source tree.
run_test_path() {
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

%posttrans client
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

%postun client
alternatives --remove clusterdb %{_pgbindir}/clusterdb
/sbin/ldconfig

%post libs
/sbin/ldconfig

%posttrans libs
alternatives --install %{_sysconfdir}/ld.so.conf.d/%{srcname}.conf \
                 %{srcname}.conf %{_pgbaseinstdir}/%{srcname}.conf \
                 %{alter_weight}
/sbin/ldconfig

%postun libs
alternatives --remove %{srcname}.conf %{_pgbaseinstdir}/%{srcname}.conf
/sbin/ldconfig

%posttrans devel
alternatives --install %{_includedir}/%{srcname} %{srcname} %{_pgincludedir} \
                 %{alter_weight} --slave %{_bindir}/ecpg ecpg %{_pgbindir}/ecpg

/sbin/ldconfig

%postun devel
alternatives --remove %{srcname} %{_pgincludedir}
/sbin/ldconfig

%posttrans server
alternatives --install %{_bindir}/initdb initdb %{_pgbindir}/initdb %{alter_weight} \
    --slave %{_bindir}/pg_amcheck pg_amcheck %{_pgbindir}/pg_amcheck \
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
    --slave %{_bindir}/pg_createsubscriber pg_createsubscriber %{_pgbindir}/pg_createsubscriber

/sbin/ldconfig

%pre server
%sysusers_create_compat %{SOURCE6}

%preun server
%systemd_preun %{service_name}

%post server
/sbin/ldconfig
%systemd_post %{service_name}

%postun server
%systemd_postun_with_restart %{service_name}
alternatives --remove initdb %{_pgbindir}/initdb
/sbin/ldconfig

%posttrans contrib
alternatives --install %{_bindir}/oid2name oid2name %{_pgbindir}/oid2name %{alter_weight} \
    --slave %{_bindir}/vacuumlo vacuumlo %{_pgbindir}/vacuumlo \
    --slave %{_bindir}/pg_recvlogical pg_recvlogical %{_pgbindir}/pg_recvlogical \
    --slave %{_bindir}/pg_combinebackup pg_combinebackup %{_pgbindir}/pg_combinebackup \
    --slave %{_bindir}/pg_walsummary pg_walsummary %{_pgbindir}/pg_walsummary

/sbin/ldconfig

%postun contrib
alternatives --remove oid2name %{_pgbindir}/oid2name
/sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)

%files client
%defattr(-,root,root)
%dir %{_usr}/pgsql
%dir %{_pgbaseinstdir}
%dir %{_pgbindir}
%dir %{_pgdatadir}
%dir %{_pgdatadir}/man
%dir %{_pgmandir}
%dir %{_pgmandir}/man1
%dir %{_pgmandir}/man3
%dir %{_pgmandir}/man7
%dir %{_pgbaseinstdir}/share
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
%dir %{_usr}/pgsql
%dir %{_pgbaseinstdir}
%dir %{_pgbaseinstdir}/lib
%dir %{_pglibdir}
%{_pgbaseinstdir}/%{srcname}.conf
%{_pglibdir}/libpq.so.*
%{_pglibdir}/libecpg.so*
%{_pglibdir}/libpgtypes.so.*
%{_pglibdir}/libecpg_compat.so.*
%{_pglibdir}/libpqwalreceiver.so

%files server
%defattr(-,root,root)
%dir %{_usr}/pgsql
%dir %{_pgbaseinstdir}
%dir %{_pgbindir}
%dir %{_pgdatadir}/man
%dir %{_pgmandir}
%dir %{_pgmandir}/man1
%dir %{_pgbaseinstdir}/share
%dir %{_pgdatadir}
%dir %{_pgdatadir}/timezonesets
%dir %{_pgdatadir}/tsearch_data
%dir %{_pgdatadir}/extension
%dir %{_pgbaseinstdir}/lib
%dir %{_pglibdir}
%{_pgbindir}/initdb
%{_pgbindir}/pg_amcheck
%{_pgbindir}/pg_archivecleanup
%{_pgbindir}/pg_checksums
%{_pgbindir}/pg_controldata
%{_pgbindir}/pg_ctl
%{_pgbindir}/pg_resetwal
%{_pgbindir}/pg_rewind
%{_pgbindir}/pg_createsubscriber
%{_pgbindir}/pg_test_fsync
%{_pgbindir}/pg_test_timing
%{_pgbindir}/pg_upgrade
%{_pgbindir}/pg_verifybackup
%{_pgbindir}/postgres
%{_pgmandir}/man1/initdb.*
%{_pgmandir}/man1/pg_amcheck.*
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
%{_pgmandir}/man1/pg_createsubscriber.1
%{_pgdatadir}/*.sample
%{_pgdatadir}/postgres.bki
%{_pgdatadir}/information_schema.sql
%{_pgdatadir}/snowball_create.sql
%{_pgdatadir}/sql_features.txt
%{_pgdatadir}/system_constraints.sql
%{_pgdatadir}/system_functions.sql
%{_pgdatadir}/system_views.sql
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
%{_tmpfilesdir}/%{name}.conf
%{_unitdir}/%{name}.service
%{_presetdir}/99-%{name}.preset
%attr(700,postgres,postgres) %dir %{_sharedstatedir}/pgsql/%{name}
%attr(755,postgres,postgres) %dir %{_var}/run/%{srcname}
%attr(700,postgres,postgres) %dir %{_sharedstatedir}/pgsql
%attr(644,postgres,postgres) %config(noreplace) %{_sysconfdir}/sysconfig/%{name}.conf
%{_libexecdir}/%{name}-check-db-dir
%{_sysusersdir}/%{name}.sysusers

%files i18n -f %{name}.lst
%defattr(-,root,root)
%dir %{_usr}/pgsql
%dir %{_pgbaseinstdir}
%dir %{_pgbaseinstdir}/share

%files docs
%defattr(-,root,root)
%dir %{_usr}/pgsql
%dir %{_pgbaseinstdir}
%dir %{_pgbaseinstdir}/share
%dir %{_pgbaseinstdir}/share/doc
%dir %{_pgdocdir}
%{_pgdocdir}/*

%files contrib
%defattr(-,root,root)
%dir %{_usr}/pgsql
%dir %{_pgbaseinstdir}
%dir %{_pgbindir}
%dir %{_pgdatadir}
%dir %{_pgdatadir}/extension
%dir %{_pgbaseinstdir}/lib
%dir %{_pglibdir}
%dir %{_pgdatadir}/man
%dir %{_pgmandir}
%dir %{_pgmandir}/man1
%dir %{_pgbaseinstdir}/share/doc
%dir %{_pgbaseinstdir}/share
%dir %{_pgdocdir}
%dir %{_pgdocdir}/extension
%{_pgbindir}/pg_combinebackup
%{_pgbindir}/pg_walsummary
%{_pgbindir}/oid2name
%{_pgbindir}/vacuumlo
%{_pgbindir}/pg_recvlogical
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
%{_pgdatadir}/extension/pg_surgery*
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
%{_pgdatadir}/extension/pg_walinspect*
%{_pgdatadir}/extension/pg_logicalinspect--*.sql
%{_pgdatadir}/extension/pg_logicalinspect.control
%{_pglibdir}/_int.so
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
%{_pglibdir}/pg_logicalinspect.so
%{_pglibdir}/pg_overexplain.so
%{_pglibdir}/pageinspect.so
%{_pglibdir}/passwordcheck.so
%{_pglibdir}/pgcrypto.so
%{_pglibdir}/pgrowlocks.so
%{_pglibdir}/pgstattuple.so
%{_pglibdir}/pg_buffercache.so
%{_pglibdir}/pg_freespacemap.so
%{_pglibdir}/pg_prewarm.so
%{_pglibdir}/pg_stat_statements.so
%{_pglibdir}/pg_surgery.so
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
%{_pglibdir}/basebackup_to_shell.so
%{_pglibdir}/basic_archive.so
%{_pglibdir}/pg_walinspect.so
%{_pgmandir}/man1/oid2name.*
%{_pgmandir}/man1/pg_recvlogical.*
%{_pgmandir}/man1/vacuumlo.*
%{_pgmandir}/man1/pg_combinebackup.1
%{_pgmandir}/man1/pg_walsummary.1

%files llvmjit
%defattr(-,root,root)
%dir %{_usr}/pgsql
%dir %{_pgbaseinstdir}
%dir %{_pgbaseinstdir}/lib
%dir %{_pglibdir}
%dir %{_pglibdir}/bitcode
%{_pglibdir}/bitcode/*
%{_pglibdir}/llvmjit.so
%{_pglibdir}/llvmjit_types.bc

%files devel
%defattr(-,root,root)
%dir %{_usr}/pgsql
%dir %{_pgbaseinstdir}
%dir %{_pgbindir}
%dir %{_pgbaseinstdir}/include
%dir %{_pgincludedir}
%dir %{_pgdatadir}/man
%dir %{_pgmandir}
%dir %{_pgmandir}/man1
%dir %{_pgbaseinstdir}/lib
%dir %{_pglibdir}/pkgconfig
%dir %{_pglibdir}/pgxs
%dir %{_pglibdir}
%{_pgbindir}/ecpg
%{_pgincludedir}/*
%{_pglibdir}/libpq.so
%{_pglibdir}/libecpg.so
%{_pglibdir}/libecpg_compat.so
%{_pglibdir}/libpgtypes.so
%{_pglibdir}/libpq.a
%{_pglibdir}/libecpg.a
%{_pglibdir}/libecpg_compat.a
%{_pglibdir}/libpgcommon.a
%{_pglibdir}/libpgcommon_shlib.a
%{_pglibdir}/libpgfeutils.a
%{_pglibdir}/libpgport.a
%{_pglibdir}/libpgport_shlib.a
%{_pglibdir}/libpgtypes.a
%{_pglibdir}/pkgconfig/*
%{_pglibdir}/pgxs/*
%{_pgmandir}/man1/ecpg.*

%files plperl
%defattr(-,root,root)
%dir %{_usr}/pgsql
%dir %{_pgbaseinstdir}
%dir %{_pgbaseinstdir}/share
%dir %{_pgdatadir}
%dir %{_pgdatadir}/extension
%dir %{_pgbaseinstdir}/lib
%dir %{_pglibdir}
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
%dir %{_usr}/pgsql
%dir %{_pgbaseinstdir}
%dir %{_pgbaseinstdir}/lib
%dir %{_pglibdir}
%dir %{_pgbaseinstdir}/share
%dir %{_pgdatadir}
%{_pgdatadir}/extension/pltcl*
%{_pglibdir}/pltcl.so

%files plpython3
%defattr(-,root,root)
%dir %{_pgbaseinstdir}/share
%dir %{_pgdatadir}
%dir %{_pgdatadir}/extension
%dir %{_pgbaseinstdir}/lib
%dir %{_pglibdir}
%{_pgdatadir}/extension/hstore_plpython3*
%{_pgdatadir}/extension/ltree_plpython3*
%{_pgdatadir}/extension/jsonb_plpython3*
%{_pgdatadir}/extension/plpython3*
%{_pglibdir}/hstore_plpython3.so
%{_pglibdir}/jsonb_plpython3.so
%{_pglibdir}/ltree_plpython3.so
%{_pglibdir}/plpython3.so

%changelog
* Wed Jun 03 2026 Harinadh Dommaraju <Harinadh.Dommaraju@broadcom.com> 18.3-5
- Release version bump as part of libxml2/libxslt
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 18.3-4
- Extended to build for subrelease 91 and above
* Fri Mar 27 2026 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 18.3-3
- Require alternatives instead of chkconfig
* Wed Mar 18 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 18.3-2
- Bump version as a part of python3.14 upgrade
* Mon Mar 02 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 18.3-1
- Initial version
- Please refer https://www.postgresql.org/docs/release/18.0/ for the full release notes.
