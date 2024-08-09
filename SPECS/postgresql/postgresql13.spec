%define srcname postgresql

%global pgmajorversion  13
%global _pgbaseinstdir  %{_usr}/pgsql/%{pgmajorversion}
%global _pgbindir       %{_pgbaseinstdir}/bin
%global _pglibdir       %{_pgbaseinstdir}/lib/%{srcname}
%global _pgincludedir   %{_pgbaseinstdir}/include/%{srcname}
%global _pgdatadir      %{_pgbaseinstdir}/share/%{srcname}
%global _pgdocdir       %{_pgbaseinstdir}/share/doc/%{srcname}
%define alter_weight    200
%global service_name %{name}.service

Summary:        PostgreSQL database engine
Name:           postgresql13
Version:        13.16
Release:        1%{?dist}
License:        PostgreSQL
URL:            www.postgresql.org
Group:          Applications/Databases
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://ftp.postgresql.org/pub/source/v%{version}/%{srcname}-%{version}.tar.bz2
%define sha512 %{srcname}=e874c77e2d1d27d724f45c576c9d815da55f36712d67e3ec0a1f14ce4ac535fb39b6f23cdcd818cff05788e2c1e12f79572d90f8c145d7478aa35157b0b40679

Source1: %{srcname}.tmpfiles.d
Source2: %{srcname}.service
Source3: %{srcname}-check-db-dir.in
Source4: %{srcname}-env-vars.conf
Source5: %{srcname}.preset
Source6: systemd-unit-instructions

BuildRequires:  krb5-devel
BuildRequires:  libedit-devel
BuildRequires:  libxml2-devel
BuildRequires:  openldap
BuildRequires:  perl
BuildRequires:  readline-devel
BuildRequires:  openssl-devel
BuildRequires:  tzdata
BuildRequires:  zlib-devel
BuildRequires:  systemd-devel

Requires:   krb5
Requires:   libedit
Requires:   libxml2
Requires:   openldap
Requires:   openssl
Requires:   readline
Requires:   tzdata
Requires:   zlib
Requires:   systemd
Requires:   %{name}-libs = %{version}-%{release}

%description
PostgreSQL is an object-relational database management system.

%package libs
Summary:    Libraries for use with PostgreSQL
Group:      Applications/Databases
Requires:   chkconfig
Requires(postun): chkconfig

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
%autosetup -n %{srcname}-%{version} -p1

%build
sed -i '/DEFAULT_PGSOCKET_DIR/s@/tmp@/run/postgresql@' src/include/pg_config_manual.h

# Note that %configure is not used here as this command relies on non-default
# values.
sh ./configure \
    --prefix=%{_pgbaseinstdir} \
    --enable-thread-safety \
    --with-ldap \
    --with-libxml \
    --with-openssl \
    --with-uuid=e2fs \
    --with-systemd \
    --with-gssapi \
    --with-libedit-preferred \
    --with-readline \
    --with-system-tzdata=%{_datadir}/zoneinfo \
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

%include %{SOURCE6}

# For postgresql 10+, commands are renamed
# Ref: https://wiki.postgresql.org/wiki/New_in_postgres_10
ln -sfv pg_receivewal %{buildroot}%{_pgbindir}/pg_receivexlog
ln -sfv pg_resetwal %{buildroot}%{_pgbindir}/pg_resetxlog
ln -sfv pg_waldump %{buildroot}%{_pgbindir}/pg_xlogdump

echo "%{_pglibdir}" > %{buildroot}%{_pgbaseinstdir}/%{srcname}.conf

%{_fixperms} %{buildroot}/*

%check
sed -i '2219s/",/ ; EXIT_STATUS=$? ; sleep 5 ; exit $EXIT_STATUS",/g'  src/test/regress/pg_regress.c
chown -Rv nobody .
sudo -u nobody -s /bin/bash -c "PATH=$PATH make -k check"

%pre
groupadd -r postgres &> /dev/null || :
useradd -M -N -g postgres -r -d /var/lib/pgsql -s /bin/bash \
  -c "PostgreSQL Server" postgres &> /dev/null || :

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
%{_tmpfilesdir}/%{name}.conf
%{_unitdir}/%{name}.service
%{_presetdir}/99-%{name}.preset
%attr(700,postgres,postgres) %dir %{_sharedstatedir}/pgsql/%{name}
%attr(755,postgres,postgres) %dir %{_var}/run/%{srcname}
%attr(700,postgres,postgres) %dir %{_sharedstatedir}/pgsql
%attr(644,postgres,postgres) %config(noreplace) %{_sysconfdir}/sysconfig/%{name}.conf
%{_libexecdir}/%{name}-check-db-dir

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
* Fri Aug 09 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 13.16-1
- Upgrade to v13.16 to fix CVE-2024-7348
* Fri Mar 15 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 13.14-3
- Use version specific bindir path in service file
* Wed Feb 14 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 13.14-2
- Add systemd unit file
* Mon Feb 12 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 13.14-1
- Upgrade to v13.14
* Tue Nov 14 2023 Shreenidhi Shedi <sshedi@vmware.com> 13.13-1
- Upgrade to v13.13
* Sun Aug 13 2023 Shreenidhi Shedi <sshedi@vmware.com> 13.12-1
- Upgrade to v13.12
* Wed May 17 2023 Julien Rouhaud <jrouhaud@vmware.com> 13.11-1
- Update to v13.11, fixing CVE-2023-2454 and CVE-2023-2455
* Fri Feb 17 2023 Shreenidhi Shedi <sshedi@vmware.com> 13.10-1
- Upgrade to v13.10 to fix CVE-2022-41862
- Use alternatives for creating files in standard locations
* Tue Aug 16 2022 Julien Rouhaud <jrouhaud@vmware.com> 13.8-1
- Upgraded to version 13.8.
* Mon Jul 18 2022 Harinadh D <hdommaraju@vmware.com> 13.7-2
- add uuid with e2fs and systemd to configuration
* Fri May 13 2022 Michael Paquier <mpaquier@vmware.com> 13.7-1
- Upgraded to version 13.7.
* Mon Feb 14 2022 Michael Paquier <mpaquier@vmware.com> 13.6-1
- Upgraded to version 13.6.
* Thu Feb 03 2022 Shreenidhi Shedi <sshedi@vmware.com> 13.5-2
- Rebuild with libedit
* Wed Jan 5 2022 Michael Paquier <mpaquier@vmware.com> 13.5-1
- Addition of new package for PostgreSQL 13
