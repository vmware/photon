Summary:        PostgreSQL database engine
Name:           postgresql13
Version:        13.4
Release:        1%{?dist}
License:        PostgreSQL
URL:            www.postgresql.org
Group:          Applications/Databases
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://ftp.postgresql.org/pub/source/v%{version}/postgresql-%{version}.tar.bz2
%define sha1    postgresql=92146ec62ad80e8f5d2959b5cc1766311dc00d64

# Macros to be used by find_lang and such.
%global pgmajorversion 13
%global pgbaseinstdir   /usr/pgsql/%{pgmajorversion}

# Common libraries needed
# clang-devel is needed for LLVM.
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

Requires:   %{name}-libs = %{version}-%{release}

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

%description libs
The postgresql13-libs package provides the essential shared libraries for any
PostgreSQL client program or interface. You will need to install this package
to use any other PostgreSQL package or any clients that need to connect to a
PostgreSQL server.

%package server
Summary:	The programs needed to create and run a PostgreSQL server
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-libs = %{version}-%{release}

%description server
PostgreSQL is an advanced Object-Relational database management system (DBMS).
The postgresql13-server package contains the programs needed to create
and run a PostgreSQL server, which will in turn allow you to create
and maintain PostgreSQL databases.

%package i18n
Summary:    Additional language files for PostgreSQL
Requires:	%{name} = %{version}-%{release}

%description i18n
The postgresql13-i18n package includes additional language files for
PostgreSQL.

%package docs
Summary:	Extra documentation for PostgreSQL

%description docs
The postgresql13-docs package includes the documentation.

%package contrib
Summary:	Contributed source and binaries distributed with PostgreSQL
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-libs = %{version}-%{release}
Requires:	%{name}-server = %{version}-%{release}

%description contrib
The postgresql13-contrib package contains various extension modules that are
included in the PostgreSQL distribution.

%package devel
Summary:	PostgreSQL development header files and libraries
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-libs = %{version}-%{release}
Requires:  clang-devel
Requires:  libxslt
Requires:  libxslt-devel
Requires:  llvm-devel
Requires:  perl-IPC-Run

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
Summary:	The Perl procedural language for PostgreSQL
Requires:	%{name}-server = %{version}-%{release}

%description plperl
The postgresql13-plperl package contains the PL/Perl procedural language,
which is an extension to the PostgreSQL database server.
Install this if you want to write database functions in Perl.

%package plpython3
Summary:	The Python3 procedural language for PostgreSQL
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-server = %{version}-%{release}
Requires:	python3-libs

%description plpython3
The postgresql13-plpython3 package contains the PL/Python3 procedural language,
which is an extension to the PostgreSQL database server.
Install this if you want to write database functions in Python 3.

%package pltcl
Summary:	The Tcl procedural language for PostgreSQL
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-server = %{version}-%{release}
Requires:	tcl

%description pltcl
PostgreSQL is an advanced Object-Relational database management
system. The %{name}-pltcl package contains the PL/Tcl language
for the backend.

%prep
%autosetup -n postgresql-%{version}

%build
sed -i '/DEFAULT_PGSOCKET_DIR/s@/tmp@/run/postgresql@' src/include/pg_config_manual.h

# Note that %configure is not used here as this command relies on non-default
# values.
sh ./configure \
    --prefix=%{pgbaseinstdir} \
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
    --includedir=%{pgbaseinstdir}/include \
    --bindir=%{pgbaseinstdir}/bin \
    --mandir=%{pgbaseinstdir}/share/man \
    --datadir=%{pgbaseinstdir}/share \
    --libdir=%{pgbaseinstdir}/lib \
    --docdir=%{pgbaseinstdir}/doc
make world %{?_smp_mflags}

%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make install-world DESTDIR=%{buildroot} %{?_smp_mflags}
# Remove anything related to Python 2.  These have no need to be
# around as only Python 3 is supported.
rm -f %{buildroot}/%{pgbaseinstdir}/share/extension/*plpython2u*
rm -f %{buildroot}/%{pgbaseinstdir}/share/extension/*plpythonu-*
rm -f %{buildroot}/%{pgbaseinstdir}/share/extension/*_plpythonu.control
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
cat pg_config-%{pgmajorversion}.lang ecpg-%{pgmajorversion}.lang ecpglib6-%{pgmajorversion}.lang >> pg_i18n.lst
cat initdb-%{pgmajorversion}.lang pg_ctl-%{pgmajorversion}.lang psql-%{pgmajorversion}.lang pg_dump-%{pgmajorversion}.lang pg_basebackup-%{pgmajorversion}.lang pgscripts-%{pgmajorversion}.lang >> pg_i18n.lst
cat postgres-%{pgmajorversion}.lang pg_resetwal-%{pgmajorversion}.lang pg_checksums-%{pgmajorversion}.lang pg_verifybackup-%{pgmajorversion}.lang pg_controldata-%{pgmajorversion}.lang plpgsql-%{pgmajorversion}.lang pg_test_timing-%{pgmajorversion}.lang pg_test_fsync-%{pgmajorversion}.lang pg_archivecleanup-%{pgmajorversion}.lang pg_waldump-%{pgmajorversion}.lang pg_rewind-%{pgmajorversion}.lang pg_upgrade-%{pgmajorversion}.lang >> pg_i18n.lst

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

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig
%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{pgbaseinstdir}/bin/clusterdb
%{pgbaseinstdir}/bin/createdb
%{pgbaseinstdir}/bin/createuser
%{pgbaseinstdir}/bin/dropdb
%{pgbaseinstdir}/bin/dropuser
%{pgbaseinstdir}/bin/pgbench
%{pgbaseinstdir}/bin/pg_basebackup
%{pgbaseinstdir}/bin/pg_config
%{pgbaseinstdir}/bin/pg_dump
%{pgbaseinstdir}/bin/pg_dumpall
%{pgbaseinstdir}/bin/pg_isready
%{pgbaseinstdir}/bin/pg_receivewal
%{pgbaseinstdir}/bin/pg_restore
%{pgbaseinstdir}/bin/pg_waldump
%{pgbaseinstdir}/bin/psql
%{pgbaseinstdir}/bin/reindexdb
%{pgbaseinstdir}/bin/vacuumdb
%{pgbaseinstdir}/share/errcodes.txt
%{pgbaseinstdir}/share/man/man1/clusterdb.*
%{pgbaseinstdir}/share/man/man1/createdb.*
%{pgbaseinstdir}/share/man/man1/createuser.*
%{pgbaseinstdir}/share/man/man1/dropdb.*
%{pgbaseinstdir}/share/man/man1/dropuser.*
%{pgbaseinstdir}/share/man/man1/pgbench.*
%{pgbaseinstdir}/share/man/man1/pg_basebackup.*
%{pgbaseinstdir}/share/man/man1/pg_config.*
%{pgbaseinstdir}/share/man/man1/pg_dump.*
%{pgbaseinstdir}/share/man/man1/pg_dumpall.*
%{pgbaseinstdir}/share/man/man1/pg_isready.*
%{pgbaseinstdir}/share/man/man1/pg_restore.*
%{pgbaseinstdir}/share/man/man1/psql.*
%{pgbaseinstdir}/share/man/man1/reindexdb.*
%{pgbaseinstdir}/share/man/man1/vacuumdb.*
%{pgbaseinstdir}/share/man/man3/*
%{pgbaseinstdir}/share/man/man7/*

%files libs
%defattr(-,root,root)
%{pgbaseinstdir}/lib/libpq.so.*
%{pgbaseinstdir}/lib/libecpg.so*
%{pgbaseinstdir}/lib/libpgtypes.so.*
%{pgbaseinstdir}/lib/libecpg_compat.so.*
%{pgbaseinstdir}/lib/libpqwalreceiver.so

%files server
%defattr(-,root,root)
%{pgbaseinstdir}/bin/initdb
%{pgbaseinstdir}/bin/pg_archivecleanup
%{pgbaseinstdir}/bin/pg_checksums
%{pgbaseinstdir}/bin/pg_controldata
%{pgbaseinstdir}/bin/pg_ctl
%{pgbaseinstdir}/bin/pg_resetwal
%{pgbaseinstdir}/bin/pg_rewind
%{pgbaseinstdir}/bin/pg_test_fsync
%{pgbaseinstdir}/bin/pg_test_timing
%{pgbaseinstdir}/bin/pg_upgrade
%{pgbaseinstdir}/bin/pg_verifybackup
%{pgbaseinstdir}/bin/postgres
%{pgbaseinstdir}/bin/postmaster
%{pgbaseinstdir}/share/man/man1/initdb.*
%{pgbaseinstdir}/share/man/man1/pg_archivecleanup.*
%{pgbaseinstdir}/share/man/man1/pg_checksums.*
%{pgbaseinstdir}/share/man/man1/pg_controldata.*
%{pgbaseinstdir}/share/man/man1/pg_ctl.*
%{pgbaseinstdir}/share/man/man1/pg_resetwal.*
%{pgbaseinstdir}/share/man/man1/pg_receivewal.*
%{pgbaseinstdir}/share/man/man1/pg_rewind.*
%{pgbaseinstdir}/share/man/man1/pg_test_fsync.*
%{pgbaseinstdir}/share/man/man1/pg_test_timing.*
%{pgbaseinstdir}/share/man/man1/pg_upgrade.*
%{pgbaseinstdir}/share/man/man1/pg_verifybackup.*
%{pgbaseinstdir}/share/man/man1/pg_waldump.*
%{pgbaseinstdir}/share/man/man1/postgres.*
%{pgbaseinstdir}/share/man/man1/postmaster.*
%{pgbaseinstdir}/share/*.sample
%{pgbaseinstdir}/share/postgres.bki
%{pgbaseinstdir}/share/information_schema.sql
%{pgbaseinstdir}/share/snowball_create.sql
%{pgbaseinstdir}/share/sql_features.txt
%{pgbaseinstdir}/share/system_views.sql
%dir %{pgbaseinstdir}/share/extension
%{pgbaseinstdir}/share/extension/plpgsql*
%{pgbaseinstdir}/share/timezonesets/*
%{pgbaseinstdir}/share/tsearch_data/*.affix
%{pgbaseinstdir}/share/tsearch_data/*.dict
%{pgbaseinstdir}/share/tsearch_data/*.ths
%{pgbaseinstdir}/share/tsearch_data/*.rules
%{pgbaseinstdir}/share/tsearch_data/*.stop
%{pgbaseinstdir}/share/tsearch_data/*.syn
%{pgbaseinstdir}/lib/dict_int.so
%{pgbaseinstdir}/lib/dict_snowball.so
%{pgbaseinstdir}/lib/dict_xsyn.so
%{pgbaseinstdir}/lib/euc2004_sjis2004.so
%{pgbaseinstdir}/lib/pgoutput.so
%{pgbaseinstdir}/lib/plpgsql.so
%{pgbaseinstdir}/lib/*_and_*.so

%files i18n -f pg_i18n.lst

%files docs
%defattr(-,root,root)
%{pgbaseinstdir}/doc/*

%files contrib
%defattr(-,root,root)
%{pgbaseinstdir}/bin/oid2name
%{pgbaseinstdir}/bin/vacuumlo
%{pgbaseinstdir}/bin/pg_recvlogical
%{pgbaseinstdir}/bin/pg_standby
%{pgbaseinstdir}/share/extension/adminpack*
%{pgbaseinstdir}/share/extension/amcheck*
%{pgbaseinstdir}/share/extension/autoinc*
%{pgbaseinstdir}/share/extension/bloom*
%{pgbaseinstdir}/share/extension/btree_gin*
%{pgbaseinstdir}/share/extension/btree_gist*
%{pgbaseinstdir}/share/extension/citext*
%{pgbaseinstdir}/share/extension/cube*
%{pgbaseinstdir}/share/extension/dblink*
%{pgbaseinstdir}/share/extension/dict_int*
%{pgbaseinstdir}/share/extension/dict_xsyn*
%{pgbaseinstdir}/share/extension/earthdistance*
%{pgbaseinstdir}/share/extension/file_fdw*
%{pgbaseinstdir}/share/extension/fuzzystrmatch*
%{pgbaseinstdir}/share/extension/hstore.control
%{pgbaseinstdir}/share/extension/hstore--*.sql
%{pgbaseinstdir}/share/extension/insert_username*
%{pgbaseinstdir}/share/extension/intagg*
%{pgbaseinstdir}/share/extension/intarray*
%{pgbaseinstdir}/share/extension/isn*
%{pgbaseinstdir}/share/extension/lo*
%{pgbaseinstdir}/share/extension/ltree.control
%{pgbaseinstdir}/share/extension/ltree--*.sql
%{pgbaseinstdir}/share/extension/moddatetime*
%{pgbaseinstdir}/share/extension/pageinspect*
%{pgbaseinstdir}/share/extension/pg_buffercache*
%{pgbaseinstdir}/share/extension/pg_freespacemap*
%{pgbaseinstdir}/share/extension/pg_prewarm*
%{pgbaseinstdir}/share/extension/pg_stat_statements*
%{pgbaseinstdir}/share/extension/pg_trgm*
%{pgbaseinstdir}/share/extension/pg_visibility*
%{pgbaseinstdir}/share/extension/pgcrypto*
%{pgbaseinstdir}/share/extension/pgrowlocks*
%{pgbaseinstdir}/share/extension/pgstattuple*
%{pgbaseinstdir}/share/extension/postgres_fdw*
%{pgbaseinstdir}/share/extension/refint*
%{pgbaseinstdir}/share/extension/seg*
%{pgbaseinstdir}/share/extension/sslinfo*
%{pgbaseinstdir}/share/extension/tablefunc*
%{pgbaseinstdir}/share/extension/tcn*
%{pgbaseinstdir}/share/extension/tsm_system_rows*
%{pgbaseinstdir}/share/extension/tsm_system_time*
%{pgbaseinstdir}/share/extension/unaccent*
%{pgbaseinstdir}/share/extension/uuid-ossp*
%{pgbaseinstdir}/share/extension/xml2*
%{pgbaseinstdir}/doc/extension/*.example
%{pgbaseinstdir}/lib/_int.so
%{pgbaseinstdir}/lib/adminpack.so
%{pgbaseinstdir}/lib/amcheck.so
%{pgbaseinstdir}/lib/auth_delay.so
%{pgbaseinstdir}/lib/autoinc.so
%{pgbaseinstdir}/lib/auto_explain.so
%{pgbaseinstdir}/lib/bloom.so
%{pgbaseinstdir}/lib/btree_gin.so
%{pgbaseinstdir}/lib/btree_gist.so
%{pgbaseinstdir}/lib/citext.so
%{pgbaseinstdir}/lib/cube.so
%{pgbaseinstdir}/lib/dblink.so
%{pgbaseinstdir}/lib/earthdistance.so
%{pgbaseinstdir}/lib/file_fdw.so*
%{pgbaseinstdir}/lib/fuzzystrmatch.so
%{pgbaseinstdir}/lib/insert_username.so
%{pgbaseinstdir}/lib/isn.so
%{pgbaseinstdir}/lib/hstore.so
%{pgbaseinstdir}/lib/lo.so
%{pgbaseinstdir}/lib/ltree.so
%{pgbaseinstdir}/lib/moddatetime.so
%{pgbaseinstdir}/lib/pageinspect.so
%{pgbaseinstdir}/lib/passwordcheck.so
%{pgbaseinstdir}/lib/pgcrypto.so
%{pgbaseinstdir}/lib/pgrowlocks.so
%{pgbaseinstdir}/lib/pgstattuple.so
%{pgbaseinstdir}/lib/pg_buffercache.so
%{pgbaseinstdir}/lib/pg_freespacemap.so
%{pgbaseinstdir}/lib/pg_prewarm.so
%{pgbaseinstdir}/lib/pg_stat_statements.so
%{pgbaseinstdir}/lib/pg_trgm.so
%{pgbaseinstdir}/lib/pg_visibility.so
%{pgbaseinstdir}/lib/pgxml.so
%{pgbaseinstdir}/lib/postgres_fdw.so
%{pgbaseinstdir}/lib/refint.so
%{pgbaseinstdir}/lib/seg.so
%{pgbaseinstdir}/lib/sslinfo.so
%{pgbaseinstdir}/lib/tablefunc.so
%{pgbaseinstdir}/lib/tcn.so
%{pgbaseinstdir}/lib/test_decoding.so
%{pgbaseinstdir}/lib/tsm_system_rows.so
%{pgbaseinstdir}/lib/tsm_system_time.so
%{pgbaseinstdir}/lib/unaccent.so
%{pgbaseinstdir}/lib/uuid-ossp.so
%{pgbaseinstdir}/share/man/man1/oid2name.*
%{pgbaseinstdir}/share/man/man1/pg_recvlogical.*
%{pgbaseinstdir}/share/man/man1/pg_standby.*
%{pgbaseinstdir}/share/man/man1/vacuumlo.*

%files llvmjit
%defattr(-,root,root)
%{pgbaseinstdir}/lib/bitcode/*
%{pgbaseinstdir}/lib/llvmjit.so
%{pgbaseinstdir}/lib/llvmjit_types.bc

%files devel
%defattr(-,root,root)
%{pgbaseinstdir}/bin/ecpg
%{pgbaseinstdir}/include/*
%{pgbaseinstdir}/lib/libpq.so
%{pgbaseinstdir}/lib/libecpg.so
%{pgbaseinstdir}/lib/libpq.a
%{pgbaseinstdir}/lib/libecpg.a
%{pgbaseinstdir}/lib/libecpg_compat.so
%{pgbaseinstdir}/lib/libecpg_compat.a
%{pgbaseinstdir}/lib/libpgcommon.a
%{pgbaseinstdir}/lib/libpgcommon_shlib.a
%{pgbaseinstdir}/lib/libpgfeutils.a
%{pgbaseinstdir}/lib/libpgport.a
%{pgbaseinstdir}/lib/libpgport_shlib.a
%{pgbaseinstdir}/lib/libpgtypes.so
%{pgbaseinstdir}/lib/libpgtypes.a
%{pgbaseinstdir}/lib/pkgconfig/*
%{pgbaseinstdir}/lib/pgxs/*
%{pgbaseinstdir}/share/man/man1/ecpg.*

%files plperl
%defattr(-,root,root)
%{pgbaseinstdir}/share/extension/bool_plperl*
%{pgbaseinstdir}/share/extension/hstore_plperl*
%{pgbaseinstdir}/share/extension/jsonb_plperl*
%{pgbaseinstdir}/share/extension/plperl*
%{pgbaseinstdir}/lib/bool_plperl.so
%{pgbaseinstdir}/lib/hstore_plperl.so
%{pgbaseinstdir}/lib/jsonb_plperl.so
%{pgbaseinstdir}/lib/plperl.so

%files pltcl
%defattr(-,root,root)
%{pgbaseinstdir}/share/extension/pltcl*
%{pgbaseinstdir}/lib/pltcl.so

%files plpython3
%defattr(-,root,root)
%{pgbaseinstdir}/share/extension/hstore_plpython3*
%{pgbaseinstdir}/share/extension/ltree_plpython3*
%{pgbaseinstdir}/share/extension/jsonb_plpython3*
%{pgbaseinstdir}/share/extension/plpython3*
%{pgbaseinstdir}/lib/hstore_plpython3.so
%{pgbaseinstdir}/lib/jsonb_plpython3.so
%{pgbaseinstdir}/lib/ltree_plpython3.so
%{pgbaseinstdir}/lib/plpython3.so

%changelog
*   Thu Sep 30 2021 Michael Paquier <mpaquier@vmware.com> 13.4-1
-   Add new package for PostgreSQL 13.
