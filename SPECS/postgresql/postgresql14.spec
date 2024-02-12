%define srcname         postgresql
%global pgmajorversion  14
%global _pgbaseinstdir  %{_usr}/pgsql/%{pgmajorversion}
%global _pgbindir       %{_pgbaseinstdir}/bin
%global _pglibdir       %{_pgbaseinstdir}/lib/%{srcname}
%global _pgincludedir   %{_pgbaseinstdir}/include/%{srcname}
%global _pgdatadir      %{_pgbaseinstdir}/share/%{srcname}
%global _pgdocdir       %{_pgbaseinstdir}/share/doc/%{srcname}
%define alter_weight    300
%define obsoletes_version 14.5

Summary:        PostgreSQL database engine
Name:           postgresql14
Version:        14.11
Release:        1%{?dist}
License:        PostgreSQL
URL:            www.postgresql.org
Group:          Applications/Databases
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://ftp.postgresql.org/pub/source/v%{version}/%{srcname}-%{version}.tar.bz2
%define sha512 %{srcname}=67289cd638ed7b13e845263d5a34394347f33735d9e2fafd6aa3562989a3a9455ea547d1b5079138648f33b093e77841654188fc74a49c0d6d458a42cfb57ffe

BuildRequires:  krb5-devel
BuildRequires:  libedit-devel
BuildRequires:  libxml2-devel
BuildRequires:  linux-api-headers
BuildRequires:  openldap
BuildRequires:  perl
BuildRequires:  readline-devel
BuildRequires:  openssl-devel
BuildRequires:  tzdata
BuildRequires:  zlib-devel
BuildRequires:  lz4-devel
BuildRequires:  systemd-devel

Requires:       krb5
Requires:       libedit
Requires:       libxml2
Requires:       openldap
Requires:       openssl
Requires:       readline
Requires:       tzdata
Requires:       zlib
Requires:       lz4
Requires:       systemd
Requires:       %{name}-libs = %{version}-%{release}

Provides:       postgresql = %{version}-%{release}
Obsoletes:      postgresql <= %{obsoletes_version}

%description
PostgreSQL is an object-relational database management system.

%package libs
Summary:    Libraries for use with PostgreSQL
Group:      Applications/Databases
Requires:   chkconfig
Requires(postun): chkconfig
Provides:   postgresql-libs = %{version}-%{release}
Obsoletes:  postgresql-libs <= %{obsoletes_version}

%description libs
The postgresql-libs package provides the essential shared libraries for any
PostgreSQL client program or interface. You will need to install this package
to use any other PostgreSQL package or any clients that need to connect to a
PostgreSQL server.

%package        devel
Summary:        Development files for postgresql.
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Provides:       postgresql-devel = %{version}-%{release}
Obsoletes:      postgresql-devel <= %{obsoletes_version}

%description    devel
The postgresql-devel package contains libraries and header files for
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
    --with-ssl=openssl \
    --with-lz4 \
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
    --slave %{_bindir}/pg_amcheck pg_amcheck %{_pgbindir}/pg_amcheck \
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
%{_pgbindir}/pg_amcheck
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
* Mon Feb 12 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 14.11-1
- Upgrade to v14.11
* Tue Nov 14 2023 Shreenidhi Shedi <sshedi@vmware.com> 14.10-1
- Upgrade to v14.10
* Sun Aug 13 2023 Shreenidhi Shedi <sshedi@vmware.com> 14.9-1
- Upgrade to v14.9
* Mon Jul 24 2023 Shreenidhi Shedi <sshedi@vmware.com> 14.8-2
- Fix obsoletes version
* Wed May 17 2023 Julien Rouhaud <jrouhaud@vmware.com> 14.8-1
- Update to v14.8, fixing CVE-2023-2454 and CVE-2023-2455
* Wed Mar 01 2023 Shreenidhi Shedi <sshedi@vmware.com> 14.7-2
- Obsolete postgresql <= 14.5-1
* Fri Feb 17 2023 Shreenidhi Shedi <sshedi@vmware.com> 14.7-1
- Upgrade to v14.7 to fix CVE-2022-41862
- Use alternatives for creating files in standard locations
- Rename package to postgresql14
* Tue Aug 16 2022 Julien Rouhaud <jrouhaud@vmware.com> 14.5-1
- Upgraded to version 14.5.
* Mon Jul 18 2022 Harinadh D <hdommaraju@vmware.com> 14.4-2
- add uuid with e2fs and systemd to configuration
* Fri Jun 17 2022 Michael Paquier <mpaquier@vmware.com> 14.4-1
- Upgraded to version 14.4.
* Fri May 13 2022 Michael Paquier <mpaquier@vmware.com> 14.3-1
- Upgraded to version 14.3.
* Mon Feb 14 2022 Michael Paquier <mpaquier@vmware.com> 14.2-1
- Upgraded to version 14.2.
* Mon Jan 31 2022 Susant Sahani <ssahani@vmware.com> 14.1-2
- Rebuild with libedit
* Mon Nov 29 2021 Tapas Kundu <tkundu@vmware.com> 14.1-1
- Upgraded to version 14.1.
- Add support for LZ4
* Thu Nov 18 2021 Nitesh Kumar <kunitesh@vmware.com> 13.5-2
- Release bump up to use libxml2 2.9.12-1.
* Mon Nov 15 2021 Michael Paquier <mpaquier@vmware.com> 13.5-1
- Upgraded to version 13.5.
* Sat Aug 21 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 13.4-2
- Bump up release for openssl
* Sat Aug 14 2021 Michael Paquier <mpaquier@vmware.com> 13.4-1
- Upgraded to version 13.4
* Fri May 14 2021 Michael Paquier <mpaquier@vmware.com> 13.3-1
- Upgraded to version 13.3
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
