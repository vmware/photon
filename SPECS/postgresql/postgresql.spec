Summary:        PostgreSQL database engine
Name:           postgresql
Version:        14.5
Release:        3%{?dist}
License:        PostgreSQL
URL:            www.postgresql.org
Group:          Applications/Databases
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://ftp.postgresql.org/pub/source/v%{version}/%{name}-%{version}.tar.bz2
%define sha512 %{name}=3051c5ab729f6a55952c6108098b022517398b1de64f7fefbdd6c806c7e2eb0637d00f3c98a6203c5bee654656528c4ff3530db5a69470e7888864c77900178a

Patch0: llvm-15.x-psql-build-err-fixes.patch

# Macros to be used by find_lang and such.
%global pgmajorversion 14

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
BuildRequires:  lz4-devel
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
Requires:       icu
Requires:       libedit
Requires:       libxml2
Requires:       lz4
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
Requires:   krb5
Requires:   openldap
Requires:   openssl

%description libs
The postgresql-libs package provides the essential shared libraries for any
PostgreSQL client program or interface. You will need to install this package
to use any other PostgreSQL package or any clients that need to connect to a
PostgreSQL server.

%package server
Summary:    The programs needed to create and run a PostgreSQL server
Requires:   %{name} = %{version}-%{release}
Requires:   %{name}-libs = %{version}-%{release}

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
%autosetup -p1

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
    --docdir=%{_docdir}/%{name}

make world %{?_smp_mflags}

%install
make install-world DESTDIR=%{buildroot} %{?_smp_mflags}

# Remove anything related to Python 2.  These have no need to be
# around as only Python 3 is supported.
rm -f %{buildroot}%{_datadir}/%{name}/extension/*plpython2u* \
      %{buildroot}%{_datadir}/%{name}/extension/*plpythonu-* \
      %{buildroot}%{_datadir}/%{name}/extension/*_plpythonu.control

# Create file lists, for --enable-nls and i18n
%find_lang ecpg-%{pgmajorversion}
%find_lang ecpglib6-%{pgmajorversion}
%find_lang initdb-%{pgmajorversion}
%find_lang libpq5-%{pgmajorversion}
%find_lang pg_amcheck-%{pgmajorversion}
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

cat initdb-%{pgmajorversion}.lang pg_amcheck-%{pgmajorversion}.lang \
    pg_ctl-%{pgmajorversion}.lang psql-%{pgmajorversion}.lang \
    pg_dump-%{pgmajorversion}.lang pg_basebackup-%{pgmajorversion}.lang \
    pgscripts-%{pgmajorversion}.lang >> pg_i18n.lst

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
%{_datadir}/%{name}/errcodes.txt
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
%{_libdir}/%{name}/libpqwalreceiver.so

%files server
%defattr(-,root,root)
%{_bindir}/initdb
%{_bindir}/pg_amcheck
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
%{_mandir}/man1/pg_amcheck.*
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
%{_datadir}/%{name}/*.sample
%{_datadir}/%{name}/postgres.bki
%{_datadir}/%{name}/information_schema.sql
%{_datadir}/%{name}/snowball_create.sql
%{_datadir}/%{name}/sql_features.txt
%{_datadir}/%{name}/system_constraints.sql
%{_datadir}/%{name}/system_functions.sql
%{_datadir}/%{name}/system_views.sql
%dir %{_datadir}/%{name}/extension
%{_datadir}/%{name}/extension/plpgsql*
%{_datadir}/%{name}/timezonesets/*
%{_datadir}/%{name}/tsearch_data/*.affix
%{_datadir}/%{name}/tsearch_data/*.dict
%{_datadir}/%{name}/tsearch_data/*.ths
%{_datadir}/%{name}/tsearch_data/*.rules
%{_datadir}/%{name}/tsearch_data/*.stop
%{_datadir}/%{name}/tsearch_data/*.syn
%{_libdir}/%{name}/dict_int.so
%{_libdir}/%{name}/dict_snowball.so
%{_libdir}/%{name}/dict_xsyn.so
%{_libdir}/%{name}/euc2004_sjis2004.so
%{_libdir}/%{name}/pgoutput.so
%{_libdir}/%{name}/plpgsql.so
%{_libdir}/%{name}/*_and_*.so

%files i18n -f pg_i18n.lst

%files docs
%defattr(-,root,root)
%{_docdir}/%{name}/html/*

%files contrib
%defattr(-,root,root)
%{_bindir}/oid2name
%{_bindir}/vacuumlo
%{_bindir}/pg_recvlogical
%{_datadir}/%{name}/extension/adminpack*
%{_datadir}/%{name}/extension/amcheck*
%{_datadir}/%{name}/extension/autoinc*
%{_datadir}/%{name}/extension/bloom*
%{_datadir}/%{name}/extension/btree_gin*
%{_datadir}/%{name}/extension/btree_gist*
%{_datadir}/%{name}/extension/citext*
%{_datadir}/%{name}/extension/cube*
%{_datadir}/%{name}/extension/dblink*
%{_datadir}/%{name}/extension/dict_int*
%{_datadir}/%{name}/extension/dict_xsyn*
%{_datadir}/%{name}/extension/earthdistance*
%{_datadir}/%{name}/extension/file_fdw*
%{_datadir}/%{name}/extension/fuzzystrmatch*
%{_datadir}/%{name}/extension/hstore.control
%{_datadir}/%{name}/extension/hstore--*.sql
%{_datadir}/%{name}/extension/insert_username*
%{_datadir}/%{name}/extension/intagg*
%{_datadir}/%{name}/extension/intarray*
%{_datadir}/%{name}/extension/isn*
%{_datadir}/%{name}/extension/lo*
%{_datadir}/%{name}/extension/ltree.control
%{_datadir}/%{name}/extension/ltree--*.sql
%{_datadir}/%{name}/extension/moddatetime*
%{_datadir}/%{name}/extension/old_snapshot*
%{_datadir}/%{name}/extension/pageinspect*
%{_datadir}/%{name}/extension/pg_buffercache*
%{_datadir}/%{name}/extension/pg_freespacemap*
%{_datadir}/%{name}/extension/pg_prewarm*
%{_datadir}/%{name}/extension/pg_stat_statements*
%{_datadir}/%{name}/extension/pg_surgery*
%{_datadir}/%{name}/extension/pg_trgm*
%{_datadir}/%{name}/extension/pg_visibility*
%{_datadir}/%{name}/extension/pgcrypto*
%{_datadir}/%{name}/extension/pgrowlocks*
%{_datadir}/%{name}/extension/pgstattuple*
%{_datadir}/%{name}/extension/postgres_fdw*
%{_datadir}/%{name}/extension/refint*
%{_datadir}/%{name}/extension/seg*
%{_datadir}/%{name}/extension/sslinfo*
%{_datadir}/%{name}/extension/tablefunc*
%{_datadir}/%{name}/extension/tcn*
%{_datadir}/%{name}/extension/tsm_system_rows*
%{_datadir}/%{name}/extension/tsm_system_time*
%{_datadir}/%{name}/extension/unaccent*
%{_datadir}/%{name}/extension/uuid-ossp*
%{_datadir}/%{name}/extension/xml2*
%{_docdir}/%{name}/extension/*.example
%{_libdir}/%{name}/_int.so
%{_libdir}/%{name}/adminpack.so
%{_libdir}/%{name}/amcheck.so
%{_libdir}/%{name}/auth_delay.so
%{_libdir}/%{name}/autoinc.so
%{_libdir}/%{name}/auto_explain.so
%{_libdir}/%{name}/bloom.so
%{_libdir}/%{name}/btree_gin.so
%{_libdir}/%{name}/btree_gist.so
%{_libdir}/%{name}/citext.so
%{_libdir}/%{name}/cube.so
%{_libdir}/%{name}/dblink.so
%{_libdir}/%{name}/earthdistance.so
%{_libdir}/%{name}/file_fdw.so*
%{_libdir}/%{name}/fuzzystrmatch.so
%{_libdir}/%{name}/insert_username.so
%{_libdir}/%{name}/isn.so
%{_libdir}/%{name}/hstore.so
%{_libdir}/%{name}/lo.so
%{_libdir}/%{name}/ltree.so
%{_libdir}/%{name}/moddatetime.so
%{_libdir}/%{name}/old_snapshot.so
%{_libdir}/%{name}/pageinspect.so
%{_libdir}/%{name}/passwordcheck.so
%{_libdir}/%{name}/pgcrypto.so
%{_libdir}/%{name}/pgrowlocks.so
%{_libdir}/%{name}/pgstattuple.so
%{_libdir}/%{name}/pg_buffercache.so
%{_libdir}/%{name}/pg_freespacemap.so
%{_libdir}/%{name}/pg_prewarm.so
%{_libdir}/%{name}/pg_stat_statements.so
%{_libdir}/%{name}/pg_surgery.so
%{_libdir}/%{name}/pg_trgm.so
%{_libdir}/%{name}/pg_visibility.so
%{_libdir}/%{name}/pgxml.so
%{_libdir}/%{name}/postgres_fdw.so
%{_libdir}/%{name}/refint.so
%{_libdir}/%{name}/seg.so
%{_libdir}/%{name}/sslinfo.so
%{_libdir}/%{name}/tablefunc.so
%{_libdir}/%{name}/tcn.so
%{_libdir}/%{name}/test_decoding.so
%{_libdir}/%{name}/tsm_system_rows.so
%{_libdir}/%{name}/tsm_system_time.so
%{_libdir}/%{name}/unaccent.so
%{_libdir}/%{name}/uuid-ossp.so
%{_mandir}/man1/oid2name.*
%{_mandir}/man1/pg_recvlogical.*
%{_mandir}/man1/vacuumlo.*

%files llvmjit
%defattr(-,root,root)
%{_libdir}/%{name}/bitcode/*
%{_libdir}/%{name}/llvmjit.so
%{_libdir}/%{name}/llvmjit_types.bc

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
%{_libdir}/%{name}/pgxs/*
%{_mandir}/man1/ecpg.*

%files plperl
%defattr(-,root,root)
%{_datadir}/%{name}/extension/bool_plperl*
%{_datadir}/%{name}/extension/hstore_plperl*
%{_datadir}/%{name}/extension/jsonb_plperl*
%{_datadir}/%{name}/extension/plperl*
%{_libdir}/%{name}/bool_plperl.so
%{_libdir}/%{name}/hstore_plperl.so
%{_libdir}/%{name}/jsonb_plperl.so
%{_libdir}/%{name}/plperl.so

%files pltcl
%defattr(-,root,root)
%{_datadir}/%{name}/extension/pltcl*
%{_libdir}/%{name}/pltcl.so

%files plpython3
%defattr(-,root,root)
%{_datadir}/%{name}/extension/hstore_plpython3*
%{_datadir}/%{name}/extension/ltree_plpython3*
%{_datadir}/%{name}/extension/jsonb_plpython3*
%{_datadir}/%{name}/extension/plpython3*
%{_libdir}/%{name}/hstore_plpython3.so
%{_libdir}/%{name}/jsonb_plpython3.so
%{_libdir}/%{name}/ltree_plpython3.so
%{_libdir}/%{name}/plpython3.so

%changelog
* Thu Oct 06 2022 Shreenidhi Shedi <sshedi@vmware.com> 14.5-3
- Bump version as a part of icu upgrade
* Wed Sep 28 2022 Shreenidhi Shedi <sshedi@vmware.com> 14.5-2
- Bump version as a part of llvm upgrade
* Thu Aug 11 2022 Julien Rouhaud <jrouhaud@vmware.com> 14.5-1
- Upgraded to version 14.5.
* Wed Jun 22 2022 Michael Paquier <mpaquier@vmware.com> 14.4-1
- Upgraded to version 14.4.
* Thu Jun 16 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 14.3-2
- Bump version as a part of libxslt upgrade
* Fri May 13 2022 Michael Paquier <mpaquier@vmware.com> 14.3-1
- Upgraded to version 14.3.
* Mon Feb 14 2022 Michael Paquier <mpaquier@vmware.com> 14.2-1
- Upgraded to version 14.2.
* Fri Nov 19 2021 Nitesh Kumar <kunitesh@vmware.com> 14.1-3
- Release bump up to use libxml2 2.9.12-1.
* Thu Nov 18 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 14.1-2
- Bump up release for openssl
* Mon Nov 15 2021 Michael Paquier <mpaquier@vmware.com> 14.1-1
- Upgraded to version 14.1.
* Wed Oct 20 2021 Michael Paquier <mpaquier@vmware.com> 14.0-3
- Add support for LZ4
* Tue Oct 19 2021 Michael Paquier <mpaquier@vmware.com> 14.0-2
- Rework dependency list for -libs and -devel packages.
* Thu Sep 30 2021 Michael Paquier <mpaquier@vmware.com> 14.0-1
- Upgraded to version 14.0
* Sat Aug 14 2021 Michael Paquier <mpaquier@vmware.com> 13.4-1
- Upgraded to version 13.4
* Fri May 14 2021 Michael Paquier <mpaquier@vmware.com> 13.3-1
- Upgraded to version 13.3
* Tue Mar 16 2021 Michael Paquier <mpaquier@vmware.com> 13.2-9
- Add support for JIT and LLVM
* Thu Mar 11 2021 Michael Paquier <mpaquier@vmware.com> 13.2-8
- Add support for libxslt
* Wed Mar 10 2021 Michael Paquier <mpaquier@vmware.com> 13.2-7
- Add support for ICU, systemd, PAM, libuuid and dtrace
* Mon Mar 08 2021 Michael Paquier <mpaquier@vmware.com> 13.2-6
- Add tests for more modules in the %check phase, with TAP tests
* Thu Mar 04 2021 Michael Paquier <mpaquier@vmware.com> 13.2-5
- Add support for internationalization support
* Tue Mar 02 2021 Michael Paquier <mpaquier@vmware.com> 13.2-4
- Removed unnecessary tweak for pg_regress.c for check phase
* Mon Mar 01 2021 Michael Paquier <mpaquier@vmware.com> 13.2-3
- Add new packages for PL/Perl, PL/Python and PL/Tcl
* Fri Feb 26 2021 Michael Paquier <mpaquier@vmware.com> 13.2-2
- Bump sub-release number as per the package redesign.
* Mon Feb 22 2021 Michael Paquier <mpaquier@vmware.com>
- Redesign of the packages, splitting client, server and contrib.
* Fri Feb 19 2021 Michael Paquier <mpaquier@vmware.com> 13.2-1
- Upgraded to version 13.2
* Fri Feb 5 2021 Michael Paquier <mpaquier@vmware.com> 13.1-1
- Fix and reorganize list of BuildRequires
- Removal of custom patch for CVE-2016-5423 committed in upstream.
- Upgraded to version 13.1
* Wed Sep 30 2020 Dweep Advani <dadvani@vmware.com> 13.0-3
- Prefer libedit over readline
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 13.0-2
- openssl 1.1.1
* Thu Sep 24 2020 Gerrit Photon <photon-checkins@vmware.com> 13.0-1
- Automatic Version Bump
* Thu Aug 20 2020 Gerrit Photon <photon-checkins@vmware.com> 12.4-1
- Automatic Version Bump
* Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 12.3-1
- Automatic Version Bump
* Mon Aug 12 2019 Shreenidhi Shedi <sshedi@vmware.com> 11.5-1
- Upgraded to version 11.5
* Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> 10.5-1
- Updated to version 10.5
* Tue Mar 27 2018 Dheeraj Shetty <dheerajs@vmware.com> 9.6.8-1
- Updated to version 9.6.8 to fix CVE-2018-1058
* Mon Feb 12 2018 Dheeraj Shetty <dheerajs@vmware.com> 9.6.7-1
- Updated to version 9.6.7
* Mon Nov 27 2017 Xiaolin Li <xiaolinl@vmware.com> 9.6.6-1
- Updated to version 9.6.6
* Fri Sep 08 2017 Xiaolin Li <xiaolinl@vmware.com> 9.6.5-1
- Updated to version 9.6.5
* Tue Aug 15 2017 Xiaolin Li <xiaolinl@vmware.com> 9.6.4-1
- Updated to version 9.6.4
* Thu Aug 10 2017 Rongrong Qiu <rqiu@vmware.com> 9.6.3-3
- add sleep 5 when initdb in make check for bug 1900371
* Wed Jul 05 2017 Divya Thaluru <dthaluru@vmware.com> 9.6.3-2
- Added postgresql-devel
* Tue Jun 06 2017 Divya Thaluru <dthaluru@vmware.com> 9.6.3-1
- Upgraded to 9.6.3
* Mon Apr 03 2017 Rongrong Qiu <rqiu@vmware.com> 9.6.2-1
- Upgrade to 9.6.2 for Photon upgrade bump
* Thu Dec 15 2016 Xiaolin Li <xiaolinl@vmware.com> 9.5.3-6
- Applied CVE-2016-5423.patch
* Thu Nov 24 2016 Alexey Makhalov <amakhalov@vmware.com> 9.5.3-5
- Required krb5-devel.
* Mon Oct 03 2016 ChangLee <changLee@vmware.com> 9.5.3-4
- Modified %check
* Thu May 26 2016 Xiaolin Li <xiaolinl@vmware.com> 9.5.3-3
- Add tzdata to buildrequires and requires.
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 9.5.3-2
- GA - Bump release of all rpms
* Fri May 20 2016 Divya Thaluru <dthaluru@vmware.com> 9.5.3-1
- Updated to version 9.5.3
* Wed Apr 13 2016 Michael Paquier <mpaquier@vmware.com> 9.5.2-1
- Updated to version 9.5.2
* Tue Feb 23 2016 Xiaolin Li <xiaolinl@vmware.com> 9.5.1-1
- Updated to version 9.5.1
* Thu Jan 21 2016 Xiaolin Li <xiaolinl@vmware.com> 9.5.0-1
- Updated to version 9.5.0
* Thu Aug 13 2015 Divya Thaluru <dthaluru@vmware.com> 9.4.4-1
- Update to version 9.4.4.
* Mon Jul 13 2015 Alexey Makhalov <amakhalov@vmware.com> 9.4.1-2
- Exclude /usr/lib/debug
* Fri May 15 2015 Sharath George <sharathg@vmware.com> 9.4.1-1
- Initial build. First version
