Summary:        PostgreSQL database engine
Name:           postgresql10
Version:        10.20
Release:        1%{?dist}
License:        PostgreSQL
URL:            www.postgresql.org
Group:          Applications/Databases
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://ftp.postgresql.org/pub/source/v%{version}/postgresql-%{version}.tar.bz2
%define sha1    postgresql=780d133ea30f654bd5e7c48f8f61fed6dcf47a3a

# Macros to be used by find_lang and such.
%global pgmajorversion 10
%global pgbaseinstdir   /usr/pgsql/%{pgmajorversion}

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
Requires:       %{name}-libs = %{version}-%{release}

%description
PostgreSQL is an object-relational database management system.

%package libs
Summary:    Libraries for use with PostgreSQL
Group:      Applications/Databases

%description libs
The postgresql10-libs package provides the essential shared libraries for any
PostgreSQL client program or interface. You will need to install this package
to use any other PostgreSQL package or any clients that need to connect to a
PostgreSQL server.

%package        devel
Summary:        Development files for postgresql.
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The postgresql10-devel package contains libraries and header files for
developing applications that use postgresql.

%prep
%autosetup -n postgresql-%{version} -p1

%build
sed -i '/DEFAULT_PGSOCKET_DIR/s@/tmp@/run/postgresql@' src/include/pg_config_manual.h &&
sh ./configure \
    --prefix=%{pgbaseinstdir} \
    --enable-thread-safety \
    --with-ldap \
    --with-libxml \
    --with-openssl \
    --with-gssapi \
    --with-uuid=e2fs \
    --with-readline \
    --with-system-tzdata=%{_datadir}/zoneinfo \
    --includedir=%{pgbaseinstdir}/include \
    --bindir=%{pgbaseinstdir}/bin \
    --mandir=%{pgbaseinstdir}/share/man \
    --datadir=%{pgbaseinstdir}/share \
    --libdir=%{pgbaseinstdir}/lib \
    --docdir=%{pgbaseinstdir}/doc

make %{?_smp_mflags}
cd contrib && make %{?_smp_mflags}

%install
[ %{buildroot} != "/" ] && rm -rf %{buildroot}/*
make install DESTDIR=%{buildroot} %{?_smp_mflags}
cd contrib && make install DESTDIR=%{buildroot} %{?_smp_mflags}

# For postgresql 10+, commands are renamed
# Ref: https://wiki.postgresql.org/wiki/New_in_postgres_10
ln -sfv pg_receivewal %{buildroot}%{pgbaseinstdir}/bin/pg_receivexlog
ln -sfv pg_resetwal %{buildroot}%{pgbaseinstdir}/bin/pg_resetxlog
ln -sfv pg_waldump %{buildroot}%{pgbaseinstdir}/bin/pg_xlogdump
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
%{pgbaseinstdir}/bin/initdb
%{pgbaseinstdir}/bin/oid2name
%{pgbaseinstdir}/bin/pg_archivecleanup
%{pgbaseinstdir}/bin/pg_basebackup
%{pgbaseinstdir}/bin/pg_controldata
%{pgbaseinstdir}/bin/pg_ctl
%{pgbaseinstdir}/bin/pg_receivewal
%{pgbaseinstdir}/bin/pg_receivexlog
%{pgbaseinstdir}/bin/pg_recvlogical
%{pgbaseinstdir}/bin/pg_resetwal
%{pgbaseinstdir}/bin/pg_resetxlog
%{pgbaseinstdir}/bin/pg_rewind
%{pgbaseinstdir}/bin/pg_standby
%{pgbaseinstdir}/bin/pg_test_fsync
%{pgbaseinstdir}/bin/pg_test_timing
%{pgbaseinstdir}/bin/pg_upgrade
%{pgbaseinstdir}/bin/pg_waldump
%{pgbaseinstdir}/bin/pg_xlogdump
%{pgbaseinstdir}/bin/pgbench
%{pgbaseinstdir}/bin/postgres
%{pgbaseinstdir}/bin/postmaster
%{pgbaseinstdir}/bin/vacuumlo
%{pgbaseinstdir}/share/*
%{pgbaseinstdir}/lib/*
%{pgbaseinstdir}/doc/extension/*.example
%exclude %{pgbaseinstdir}/share/pg_service.conf.sample
%exclude %{pgbaseinstdir}/share/psqlrc.sample

%files libs
%{pgbaseinstdir}/bin/clusterdb
%{pgbaseinstdir}/bin/createdb
%{pgbaseinstdir}/bin/createuser
%{pgbaseinstdir}/bin/dropdb
%{pgbaseinstdir}/bin/dropuser
%{pgbaseinstdir}/bin/ecpg
%{pgbaseinstdir}/bin/pg_config
%{pgbaseinstdir}/bin/pg_dump
%{pgbaseinstdir}/bin/pg_dumpall
%{pgbaseinstdir}/bin/pg_isready
%{pgbaseinstdir}/bin/pg_restore
%{pgbaseinstdir}/bin/psql
%{pgbaseinstdir}/bin/reindexdb
%{pgbaseinstdir}/bin/vacuumdb
%{pgbaseinstdir}/lib/libecpg*.so.*
%{pgbaseinstdir}/lib/libpgtypes*.so.*
%{pgbaseinstdir}/lib/libpq*.so.*
%{pgbaseinstdir}/share/pg_service.conf.sample
%{pgbaseinstdir}/share/psqlrc.sample

%files devel
%defattr(-,root,root)
%{pgbaseinstdir}/include/*
%{pgbaseinstdir}/lib/pkgconfig/*
%{pgbaseinstdir}/lib/libecpg*.so
%{pgbaseinstdir}/lib/libpgtypes*.so
%{pgbaseinstdir}/lib/libpq*.so
%{pgbaseinstdir}/lib/libpgcommon*.a
%{pgbaseinstdir}/lib/libpgfeutils.a
%{pgbaseinstdir}/lib/libpgport*.a
%{pgbaseinstdir}/lib/libpq.a
%{pgbaseinstdir}/lib/libecpg.a
%{pgbaseinstdir}/lib/libecpg_compat.a
%{pgbaseinstdir}/lib/libpgtypes.a

%changelog
*   Tue Mar 15 2022 Tapas Kundu <tkundu@vmware.com> 10.20-1
-   Packaged postgresql10 in custom path.
-   This will help in-place db upgrade for users migrating from photon os 3.0
