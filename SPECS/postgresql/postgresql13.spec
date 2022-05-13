Summary:        PostgreSQL database engine
Name:           postgresql13
Version:        13.7
Release:        1%{?dist}
License:        PostgreSQL
URL:            www.postgresql.org
Group:          Applications/Databases
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://ftp.postgresql.org/pub/source/v%{version}/postgresql-%{version}.tar.bz2
%define sha512  postgresql=9254f21519c8d4e926f70082503bb5593c91064a3d2a4ea18ac503dfd9aa94751d6f01ce00fca9fec9b2b7af40caf8d0951b661dd8be4d6aa87c1e35b6fa7a41

# Macros to be used for installation paths.
%global pgmajorversion 13
%global pgbaseinstdir   /usr/pgsql/%{pgmajorversion}

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

Requires:   krb5
Requires:   libedit
Requires:   libxml2
Requires:   openldap
Requires:   openssl
Requires:   readline
Requires:   tzdata
Requires:   zlib
Requires:   %{name}-libs = %{version}-%{release}

%description
PostgreSQL is an object-relational database management system.

%package libs
Summary:    Libraries for use with PostgreSQL
Group:      Applications/Databases

%description libs
The postgresql13-libs package provides the essential shared libraries for any
PostgreSQL client program or interface. You will need to install this package
to use any other PostgreSQL package or any clients that need to connect to a
PostgreSQL server.

%package        devel
Summary:        Development files for postgresql.
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The postgresql13-devel package contains libraries and header files for
developing applications that use postgresql.

%prep
%autosetup -n postgresql-%{version} -p1

%build
sed -i '/DEFAULT_PGSOCKET_DIR/s@/tmp@/run/postgresql@' src/include/pg_config_manual.h

# Note that %configure is not used here as this command relies on non-default
# values.
sh ./configure \
    --prefix=%{pgbaseinstdir} \
    --enable-thread-safety \
    --with-ldap \
    --with-libxml \
    --with-openssl \
    --with-gssapi \
    --with-libedit-preferred \
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
%if 0%{?with_check}
sed -i '2219s/",/  ; EXIT_STATUS=$? ; sleep 5 ; exit $EXIT_STATUS",/g'  src/test/regress/pg_regress.c
chown -Rv nobody .
sudo -u nobody -s /bin/bash -c "PATH=$PATH make -k check"
%endif

%ldconfig_scriptlets

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
%{pgbaseinstdir}/bin/pg_checksums
%{pgbaseinstdir}/bin/pg_verifybackup
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
* Fri May 13 2022 Michael Paquier <mpaquier@vmware.com> 13.7-1
- Upgraded to version 13.7.
* Mon Feb 14 2022 Michael Paquier <mpaquier@vmware.com> 13.6-1
- Upgraded to version 13.6.
* Thu Feb 03 2022 Shreenidhi Shedi <sshedi@vmware.com> 13.5-2
- Rebuild with libedit
* Wed Jan 5 2022 Michael Paquier <mpaquier@vmware.com> 13.5-1
- Addition of new package for PostgreSQL 13
