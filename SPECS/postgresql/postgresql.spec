Summary:        PostgreSQL database engine
Name:           postgresql
Version:        13.3
Release:        1%{?dist}
License:        PostgreSQL
URL:            www.postgresql.org
Group:          Applications/Databases
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://ftp.postgresql.org/pub/source/v%{version}/%{name}-%{version}.tar.bz2
%define sha1    postgresql=7a775f95367613ed5f7e4cd632586f9628475a92

# Macros to be used by find_lang and such.
%global pgmajorversion 13

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

%package i18n
Summary:    Additional language files for PostgreSQL
Requires:	%{name} = %{version}-%{release}

%description i18n
The postgresql-i18n package includes additional language files for
PostgreSQL.

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
Requires:  clang-devel
Requires:  libxslt
Requires:  libxslt-devel
Requires:  llvm-devel
Requires:  perl-IPC-Run

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
Summary:	The Perl procedural language for PostgreSQL
Requires:	%{name}-server = %{version}-%{release}

%description plperl
The postgresql-plperl package contains the PL/Perl procedural language,
which is an extension to the PostgreSQL database server.
Install this if you want to write database functions in Perl.

%package plpython3
Summary:	The Python3 procedural language for PostgreSQL
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-server = %{version}-%{release}
Requires:	python3-libs

%description plpython3
The postgresql-plpython3 package contains the PL/Python3 procedural language,
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
%setup -q

%build
sed -i '/DEFAULT_PGSOCKET_DIR/s@/tmp@/run/postgresql@' src/include/pg_config_manual.h

%configure \
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
    --docdir=%{_docdir}/postgresql
make world %{?_smp_mflags}

%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make install-world DESTDIR=%{buildroot}
# Remove anything related to Python 2.  These have no need to be
# around as only Python 3 is supported.
rm -f %{buildroot}/%{_datadir}/postgresql/extension/*plpython2u*
rm -f %{buildroot}/%{_datadir}/postgresql/extension/*plpythonu-*
rm -f %{buildroot}/%{_datadir}/postgresql/extension/*_plpythonu.control
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

%files i18n -f pg_i18n.lst

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
%{_datadir}/postgresql/extension/uuid-ossp*
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
%{_libdir}/postgresql/uuid-ossp.so
%{_mandir}/man1/oid2name.*
%{_mandir}/man1/pg_recvlogical.*
%{_mandir}/man1/pg_standby.*
%{_mandir}/man1/vacuumlo.*

%files llvmjit
%defattr(-,root,root)
%{_libdir}/postgresql/bitcode/*
%{_libdir}/postgresql/llvmjit.so
%{_libdir}/postgresql/llvmjit_types.bc

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

%files plperl
%defattr(-,root,root)
%{_datadir}/postgresql/extension/bool_plperl*
%{_datadir}/postgresql/extension/hstore_plperl*
%{_datadir}/postgresql/extension/jsonb_plperl*
%{_datadir}/postgresql/extension/plperl*
%{_libdir}/postgresql/bool_plperl.so
%{_libdir}/postgresql/hstore_plperl.so
%{_libdir}/postgresql/jsonb_plperl.so
%{_libdir}/postgresql/plperl.so

%files pltcl
%defattr(-,root,root)
%{_datadir}/postgresql/extension/pltcl*
%{_libdir}/postgresql/pltcl.so

%files plpython3
%defattr(-,root,root)
%{_datadir}/postgresql/extension/hstore_plpython3*
%{_datadir}/postgresql/extension/ltree_plpython3*
%{_datadir}/postgresql/extension/jsonb_plpython3*
%{_datadir}/postgresql/extension/plpython3*
%{_libdir}/postgresql/hstore_plpython3.so
%{_libdir}/postgresql/jsonb_plpython3.so
%{_libdir}/postgresql/ltree_plpython3.so
%{_libdir}/postgresql/plpython3.so

%changelog
*   Fri May 14 2021 Michael Paquier <mpaquier@vmware.com> 13.3-1
-   Upgraded to version 13.3
*   Tue Mar 16 2021 Michael Paquier <mpaquier@vmware.com> 13.2-9
-   Add support for JIT and LLVM
*   Thu Mar 11 2021 Michael Paquier <mpaquier@vmware.com> 13.2-8
-   Add support for libxslt
*   Wed Mar 10 2021 Michael Paquier <mpaquier@vmware.com> 13.2-7
-   Add support for ICU, systemd, PAM, libuuid and dtrace
*   Mon Mar 08 2021 Michael Paquier <mpaquier@vmware.com> 13.2-6
-   Add tests for more modules in the %check phase, with TAP tests
*   Thu Mar 04 2021 Michael Paquier <mpaquier@vmware.com> 13.2-5
-   Add support for internationalization support
*   Tue Mar 02 2021 Michael Paquier <mpaquier@vmware.com> 13.2-4
-   Removed unnecessary tweak for pg_regress.c for check phase
*   Mon Mar 01 2021 Michael Paquier <mpaquier@vmware.com> 13.2-3
-   Add new packages for PL/Perl, PL/Python and PL/Tcl
*   Fri Feb 26 2021 Michael Paquier <mpaquier@vmware.com> 13.2-2
-   Bump sub-release number as per the package redesign.
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
