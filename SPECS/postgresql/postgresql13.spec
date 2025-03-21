%define srcname         postgresql
%global pgmajorversion  13
%global _pgbaseinstdir  %{_usr}/pgsql/%{pgmajorversion}
%global _pgbindir       %{_pgbaseinstdir}/bin
%global _pglibdir       %{_pgbaseinstdir}/lib/%{srcname}
%global _pgincludedir   %{_pgbaseinstdir}/include/%{srcname}
%global _pgdatadir      %{_pgbaseinstdir}/share/%{srcname}
%global _pgdocdir       %{_pgbaseinstdir}/share/doc/%{srcname}
%define alter_weight    200
%define obsoletes_version 10.23-2

Summary:        PostgreSQL database engine
Name:           postgresql13
Version:        13.20
Release:        1%{?dist}
License:        PostgreSQL
URL:            www.postgresql.org
Group:          Applications/Databases
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://ftp.postgresql.org/pub/source/v%{version}/%{srcname}-%{version}.tar.bz2
%define sha512 %{srcname}=884ee8327b803c66679238525e7d51320ea537b41138d7fe8fd7e725631f734a61e53646d9cec78154f3f05a3b50e90508793a56a8f0f76699a53773930cb1d0

BuildRequires: krb5-devel
BuildRequires: libedit-devel
BuildRequires: libxml2-devel
BuildRequires: openldap
BuildRequires: perl
BuildRequires: readline-devel
BuildRequires: openssl-devel
BuildRequires: tzdata
BuildRequires: zlib-devel
BuildRequires: systemd-devel
BuildRequires: util-linux-devel

Requires: krb5
Requires: libedit
Requires: libxml2
Requires: openldap
Requires: openssl
Requires: readline
Requires: tzdata
Requires: zlib
Requires: util-linux-libs
Requires: systemd

Requires: %{name}-libs = %{version}-%{release}
Obsoletes: postgresql < %{obsoletes_version}

%description
PostgreSQL is an object-relational database management system.

%package libs
Summary:        Libraries for use with PostgreSQL
Group:          Applications/Databases
Obsoletes:      postgresql-libs < %{obsoletes_version}
Requires:   chkconfig
Requires(postun): chkconfig

%description libs
The %{name}-libs package provides the essential shared libraries for any
PostgreSQL client program or interface. You will need to install this package
to use any other PostgreSQL package or any clients that need to connect to a
PostgreSQL server.

%package        devel
Summary:        Development files for postgresql.
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Obsoletes:      postgresql-devel < %{obsoletes_version}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use postgresql.

%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
sed -i '/DEFAULT_PGSOCKET_DIR/s@/tmp@/run/postgresql@' src/include/pg_config_manual.h

sh ./configure \
    --prefix=%{_pgbaseinstdir} \
    --enable-thread-safety \
    --with-ldap \
    --with-libxml \
    --with-openssl \
    --with-gssapi \
    --with-libedit-preferred \
    --with-readline \
    --with-system-tzdata=%{_datadir}/zoneinfo \
    --with-uuid=e2fs \
    --with-systemd \
    --includedir=%{_pgincludedir} \
    --bindir=%{_pgbindir} \
    --datadir=%{_pgdatadir} \
    --libdir=%{_pglibdir} \
    --docdir=%{_pgdocdir}

%make_build
%make_build -C contrib

%install
%make_install %{?_smp_mflags}
%make_install -C contrib %{?_smp_mflags}

# For postgresql 10+, commands are renamed
# Ref: https://wiki.postgresql.org/wiki/New_in_postgres_10
ln -sfv pg_receivewal %{buildroot}%{_pgbindir}/pg_receivexlog
ln -sfv pg_resetwal %{buildroot}%{_pgbindir}/pg_resetxlog
ln -sfv pg_waldump %{buildroot}%{_pgbindir}/pg_xlogdump

echo "%{_pglibdir}" > %{buildroot}%{_pgbaseinstdir}/%{srcname}.conf

%{_fixperms} %{buildroot}/*

%if 0%{?with_check}
%check
sed -i '2219s/",/  ; EXIT_STATUS=$? ; sleep 5 ; exit $EXIT_STATUS",/g' src/test/regress/pg_regress.c
chown -Rv nobody .
sudo -u nobody -s /bin/bash -c "PATH=$PATH make -k check"
%endif

%post
/sbin/ldconfig

%posttrans
alternatives --install %{_bindir}/initdb initdb %{_pgbindir}/initdb %{alter_weight} \
    --slave %{_bindir}/oid2name oid2name %{_pgbindir}/oid2name \
    --slave %{_bindir}/pg_archivecleanup pg_archivecleanup %{_pgbindir}/pg_archivecleanup \
    --slave %{_bindir}/pg_basebackup pg_basebackup %{_pgbindir}/pg_basebackup \
    --slave %{_bindir}/pg_controldata pg_controldata %{_pgbindir}/pg_controldata \
    --slave %{_bindir}/pg_ctl pg_ctl %{_pgbindir}/pg_ctl \
    --slave %{_bindir}/pg_receivewal pg_receivewal %{_pgbindir}/pg_receivewal \
    --slave %{_bindir}/pg_receivexlog pg_receivexlog %{_pgbindir}/pg_receivexlog \
    --slave %{_bindir}/pg_recvlogical pg_recvlogical %{_pgbindir}/pg_recvlogical \
    --slave %{_bindir}/pg_resetwal pg_resetwal %{_pgbindir}/pg_resetwal \
    --slave %{_bindir}/pg_resetxlog pg_resetxlog %{_pgbindir}/pg_resetxlog \
    --slave %{_bindir}/pg_rewind pg_rewind %{_pgbindir}/pg_rewind \
    --slave %{_bindir}/pg_standby pg_standby %{_pgbindir}/pg_standby \
    --slave %{_bindir}/pg_test_fsync pg_test_fsync %{_pgbindir}/pg_test_fsync \
    --slave %{_bindir}/pg_test_timing pg_test_timing %{_pgbindir}/pg_test_timing \
    --slave %{_bindir}/pg_upgrade pg_upgrade %{_pgbindir}/pg_upgrade \
    --slave %{_bindir}/pg_waldump pg_waldump %{_pgbindir}/pg_waldump \
    --slave %{_bindir}/pg_xlogdump pg_xlogdump %{_pgbindir}/pg_xlogdump \
    --slave %{_bindir}/pgbench pgbench %{_pgbindir}/pgbench \
    --slave %{_bindir}/postgres postgres %{_pgbindir}/postgres \
    --slave %{_bindir}/postmaster postmaster %{_pgbindir}/postmaster \
    --slave %{_bindir}/vacuumlo vacuumlo %{_pgbindir}/vacuumlo

/sbin/ldconfig

%postun
alternatives --remove initdb %{_pgbindir}/initdb
/sbin/ldconfig

%post libs
/sbin/ldconfig

%posttrans libs
alternatives --install %{_bindir}/clusterdb clusterdb %{_pgbindir}/clusterdb %{alter_weight} \
    --slave %{_bindir}/createdb createdb %{_pgbindir}/createdb \
    --slave %{_bindir}/createuser createuser %{_pgbindir}/createuser \
    --slave %{_bindir}/dropdb dropdb %{_pgbindir}/dropdb \
    --slave %{_bindir}/dropuser dropuser %{_pgbindir}/dropuser \
    --slave %{_bindir}/ecpg ecpg %{_pgbindir}/ecpg \
    --slave %{_bindir}/pg_config pg_config %{_pgbindir}/pg_config \
    --slave %{_bindir}/pg_dump pg_dump %{_pgbindir}/pg_dump \
    --slave %{_bindir}/pg_dumpall pg_dumpall %{_pgbindir}/pg_dumpall \
    --slave %{_bindir}/pg_isready pg_isready %{_pgbindir}/pg_isready \
    --slave %{_bindir}/pg_restore pg_restore %{_pgbindir}/pg_restore \
    --slave %{_bindir}/psql psql %{_pgbindir}/psql \
    --slave %{_bindir}/reindexdb reindexdb %{_pgbindir}/reindexdb \
    --slave %{_bindir}/vacuumdb vacuumdb %{_pgbindir}/vacuumdb \
    --slave %{_sysconfdir}/ld.so.conf.d/%{srcname}.conf %{srcname}.conf %{_pgbaseinstdir}/%{srcname}.conf

/sbin/ldconfig

%postun libs
alternatives --remove clusterdb %{_pgbindir}/clusterdb
/sbin/ldconfig

%posttrans devel
alternatives --install %{_includedir}/%{srcname} %{srcname} %{_pgincludedir} %{alter_weight}
/sbin/ldconfig

%postun devel
alternatives --remove %{srcname} %{_pgincludedir}
/sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%dir %{_pgbindir}
%dir %{_pglibdir}
%dir %{_pgdatadir}
%dir %{_pgdocdir}
%{_pgbindir}/initdb
%{_pgbindir}/oid2name
%{_pgbindir}/pg_archivecleanup
%{_pgbindir}/pg_basebackup
%{_pgbindir}/pg_controldata
%{_pgbindir}/pg_ctl
%{_pgbindir}/pg_receivewal
%{_pgbindir}/pg_receivexlog
%{_pgbindir}/pg_recvlogical
%{_pgbindir}/pg_resetwal
%{_pgbindir}/pg_resetxlog
%{_pgbindir}/pg_rewind
%{_pgbindir}/pg_standby
%{_pgbindir}/pg_test_fsync
%{_pgbindir}/pg_test_timing
%{_pgbindir}/pg_upgrade
%{_pgbindir}/pg_waldump
%{_pgbindir}/pg_xlogdump
%{_pgbindir}/pg_checksums
%{_pgbindir}/pg_verifybackup
%{_pgbindir}/pgbench
%{_pgbindir}/postgres
%{_pgbindir}/postmaster
%{_pgbindir}/vacuumlo
%{_pgdatadir}/*
%{_pglibdir}/*
%{_pgdocdir}/extension/*.example

%files libs
%defattr(-,root,root)
%dir %{_pgbindir}
%dir %{_pglibdir}
%{_pgbaseinstdir}/%{srcname}.conf
%{_pgbindir}/clusterdb
%{_pgbindir}/createdb
%{_pgbindir}/createuser
%{_pgbindir}/dropdb
%{_pgbindir}/dropuser
%{_pgbindir}/ecpg
%{_pgbindir}/pg_config
%{_pgbindir}/pg_dump
%{_pgbindir}/pg_dumpall
%{_pgbindir}/pg_isready
%{_pgbindir}/pg_restore
%{_pgbindir}/psql
%{_pgbindir}/reindexdb
%{_pgbindir}/vacuumdb
%{_pglibdir}/libecpg*.so.*
%{_pglibdir}/libpgtypes*.so.*
%{_pglibdir}/libpq*.so.*
%{_pgdatadir}/pg_service.conf.sample
%{_pgdatadir}/psqlrc.sample

%files devel
%defattr(-,root,root)
%{_pgincludedir}/*
%{_pglibdir}/pkgconfig/*
%{_pglibdir}/libecpg*.so
%{_pglibdir}/libpgtypes*.so
%{_pglibdir}/libpq*.so
%{_pglibdir}/libpgcommon*.a
%{_pglibdir}/libpgfeutils.a
%{_pglibdir}/libpgport*.a
%{_pglibdir}/libpq.a
%{_pglibdir}/libecpg.a
%{_pglibdir}/libecpg_compat.a
%{_pglibdir}/libpgtypes.a

%changelog
* Thu Mar 20 2025 Tapas Kundu <tapas.kundu@broadcom.com> 13.20-1
- Version upgrade to fix CVEs
* Tue Dec 03 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 13.18-1
- Version upgrade to fix CVEs
* Mon Aug 12 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 13.16-1
- Upgrade to v13.16 to fix CVE-2024-7348
* Mon Feb 12 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 13.14-1
- Upgrade to v13.14
* Tue Nov 14 2023 Shreenidhi Shedi <sshedi@vmware.com> 13.13-1
- Upgrade to v13.13
* Fri Aug 11 2023 Julien Rouhaud <jrouhaud@vmware.com> 13.12-1
- Upgraded to version  13.12.
* Wed Jul 05 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 13.11-2
- Bump version to build with updated tzdata
* Wed May 17 2023 Julien Rouhaud <jrouhaud@vmware.com> 13.11-1
- Update to version 13.11, fixing CVE-2023-2454 and CVE-2023-2455
* Wed Feb 15 2023 Julien Rouhaud <jrouhaud@vmware.com> 13.10-1
- Upgraded to version  13.10.
* Thu Feb 09 2023 Shreenidhi Shedi <sshedi@vmware.com> 13.9-3
- Fix CVE-2022-41862
* Thu Jan 05 2023 Shreenidhi Shedi <sshedi@vmware.com> 13.9-2
- Fix chkconfig mishap
* Fri Nov 18 2022 Shreenidhi Shedi <sshedi@vmware.com> 13.9-1
- Intial version.
