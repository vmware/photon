Summary:          Database servers made by the original developers of MySQL.
Name:             mariadb
Version:          10.9.4
Release:          9%{?dist}
License:          GPLv2
Group:            Applications/Databases
Vendor:           VMware, Inc.
Distribution:     Photon
Url:              https://mariadb.org

Source0: https://archive.mariadb.org/%{name}-%{version}/source/%{name}-%{version}.tar.gz
%define sha512 %{name}=9fc5d71c08cb07efc777ef3ebd97dc4953de8aa46750f52c2dabea5af63b52938ca4b54221184f1b4fbb71b94dade27c90756123ddef51959a7b5d43c3b8d986

Source1:          %{name}.sysusers

BuildRequires:    cmake
BuildRequires:    Linux-PAM-devel
BuildRequires:    openssl-devel
BuildRequires:    zlib-devel
BuildRequires:    krb5-devel
BuildRequires:    e2fsprogs-devel
BuildRequires:    systemd-devel
BuildRequires:    curl-devel
BuildRequires:    libxml2-devel
BuildRequires:    libaio-devel
BuildRequires:    gnutls-devel
BuildRequires:    systemd-devel

Conflicts:        mysql

Requires: openssl
Requires: systemd
Requires: perl
Requires: zlib
Requires: libaio
Requires: gnutls
Requires: libxml2
Requires: curl
Requires: Linux-PAM
Requires(pre): systemd-rpm-macros

%description
MariaDB is a community developed fork from MySQL - a multi-user, multi-threaded
SQL database server. It is a client/server implementation consisting of
a server daemon (mariadbd) and many different client programs and libraries.
The base package contains the standard MariaDB/MySQL client programs and
utilities.

%package server
Summary:    MariaDB server
Requires:   %{name}-errmsg = %{version}-%{release}
Requires:   shadow
Requires:   libaio

%description server
The MariaDB server and related files

%package server-galera
Summary:    MariaDB Galera Cluster is a synchronous multi-master cluster for MariaDB
Group:      Applications/Databases
Requires:   %{name}-server = %{version}-%{release}

%description server-galera
MariaDB Galera Cluster is a synchronous multi-master cluster for MariaDB.
It is available on Linux only, and only supports the XtraDB/InnoDB storage engines
(although there is experimental support for MyISAM - see the wsrep_replicate_myisam system variable).

%package devel
Summary:    Development headers for mariadb
Requires:   %{name} = %{version}-%{release}
Requires:   openssl-devel
Requires:   zlib-devel

%description devel
Development headers for developing applications linking to maridb

%package errmsg
Summary:    errmsg for mariadb

%description errmsg
errmsg for maridb

%prep
%autosetup -p1
# Remove PerconaFT from here because of AGPL licence
rm -rf storage/tokudb/PerconaFT

%build
%{cmake} \
      -DCMAKE_BUILD_TYPE=Release \
      -DINSTALL_DOCDIR=share/doc/%{name}-%{version} \
      -DINSTALL_DOCREADMEDIR=share/doc/%{name}-%{version} \
      -DINSTALL_MANDIR=share/man \
      -DINSTALL_MYSQLSHAREDIR="share/mysql" \
      -DINSTALL_SYSCONFDIR="%{_sysconfdir}" \
      -DINSTALL_SYSCONF2DIR="%{_sysconfdir}/my.cnf.d" \
      -DINSTALL_MYSQLTESTDIR=share/mysql/test \
      -DINSTALL_PLUGINDIR=lib/mysql/plugin \
      -DINSTALL_SBINDIR=sbin \
      -DINSTALL_SCRIPTDIR=bin \
      -DINSTALL_SQLBENCHDIR=share/mysql/bench \
      -DINSTALL_SUPPORTFILESDIR=share \
      -DMYSQL_DATADIR="%{_sharedstatedir}/mysql" \
      -DMYSQL_UNIX_ADDR="%{_sharedstatedir}/mysql/mysqld.sock" \
      -DWITH_EXTRA_CHARSETS=complex \
      -DWITH_EMBEDDED_SERVER=ON \
      -DSKIP_TESTS=ON \
      -DTOKUDB_OK=0

%{cmake_build}

%install
%{cmake_install}

mkdir -p %{buildroot}%{_unitdir} %{buildroot}%{_sharedstatedir}/mysql

mv %{buildroot}%{_datadir}/systemd/%{name}.service \
    %{buildroot}%{_datadir}/systemd/%{name}@.service \
    %{buildroot}%{_datadir}/systemd/mysql.service \
    %{buildroot}%{_datadir}/systemd/mysqld.service \
    %{buildroot}%{_datadir}/systemd/%{name}-extra@.socket \
    %{buildroot}%{_datadir}/systemd/%{name}@.socket \
    %{buildroot}%{_unitdir}

install -p -D -m 0644 %{SOURCE1} %{buildroot}%{_sysusersdir}/%{name}.sysusers
rm %{buildroot}%{_sbindir}/rcmysql %{buildroot}%{_libdir}/*.a
install -vdm755 %{buildroot}%{_presetdir}
echo "disable %{name}.service" > %{buildroot}%{_presetdir}/50-%{name}.preset

%check
cd %{__cmake_builddir}
%make_build test

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%pre server
if [ $1 -eq 1 ]; then
  %sysusers_create_compat %{SOURCE1}
fi

%post server
/sbin/ldconfig
chown mysql:mysql %{_sharedstatedir}/mysql || :
mysql_install_db --datadir="%{_sharedstatedir}/mysql" --user="mysql" --basedir="/usr" >/dev/null || :
%systemd_post %{name}.service

%postun server
/sbin/ldconfig
%systemd_postun_with_restart %{name}.service

%preun server
%systemd_preun %{name}.service

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_libdir}/libmysqlclient.so
%{_libdir}/libmysqlclient_r.so
%{_libdir}/libmariadb.so.*
%{_libdir}/libmariadbd.so.*
%{_bindir}/aria_s3_copy
%{_bindir}/%{name}
%{_bindir}/%{name}-config
%{_bindir}/mariadb_config
%{_bindir}/%{name}-access
%{_bindir}/%{name}-admin
%{_bindir}/%{name}-binlog
%{_bindir}/%{name}-check
%{_bindir}/%{name}-client-test
%{_bindir}/%{name}-client-test-embedded
%{_bindir}/%{name}-conv
%{_bindir}/%{name}-convert-table-format
%{_bindir}/%{name}-dump
%{_bindir}/%{name}-dumpslow
%{_bindir}/%{name}-embedded
%{_bindir}/%{name}-find-rows
%{_bindir}/%{name}-fix-extensions
%{_bindir}/%{name}-import
%{_bindir}/%{name}-ldb
%{_bindir}/%{name}-plugin
%{_bindir}/%{name}-setpermission
%{_bindir}/%{name}-show
%{_bindir}/%{name}-slap
%{_bindir}/%{name}-test
%{_bindir}/%{name}-test-embedded
%{_bindir}/%{name}-upgrade
%{_bindir}/mariadbd-safe
%{_bindir}/mariadbd-safe-helper
%{_bindir}/msql2mysql
%{_bindir}/mysql
%{_bindir}/mysql_find_rows
%{_bindir}/mysql_plugin
%{_bindir}/mysql_waitpid
%{_bindir}/mysqlaccess
%{_bindir}/mysqladmin
%{_bindir}/mysqlbinlog
%{_bindir}/mysqlcheck
%{_bindir}/mysqldump
%{_bindir}/mysqlimport
%{_bindir}/mysqlshow
%{_bindir}/mysqlslap
%{_bindir}/test-connect-t
%{_bindir}/mysql_client_test
%{_bindir}/mysql_client_test_embedded
%{_bindir}/mysql_config
%{_bindir}/mysql_convert_table_format
%{_bindir}/mysql_embedded
%{_bindir}/mysql_fix_extensions
%{_bindir}/mysql_ldb
%{_bindir}/mysql_setpermission
%{_bindir}/mysqltest
%{_bindir}/mysqltest_embedded
%{_bindir}/mytop
%{_bindir}/perror
%{_bindir}/sst_dump
%{_bindir}/%{name}-waitpid
%{_bindir}/myrocks_hotbackup
%{_datadir}/mysql/charsets/*
%{_datadir}/magic
%{_datadir}/pam_user_map.so
%{_datadir}/user_map.conf
%{_mandir}/man1/msql2mysql.1.gz
%{_mandir}/man1/mysql.1.gz
%{_mandir}/man1/mysqlaccess.1.gz
%{_mandir}/man1/mysqladmin.1.gz
%{_mandir}/man1/mysqlbinlog.1.gz
%{_mandir}/man1/mysqlcheck.1.gz
%{_mandir}/man1/mysql_client_test.1.gz
%{_mandir}/man1/mysql_client_test_embedded.1.gz
%{_mandir}/man1/mysql_config.1.gz
%{_mandir}/man1/mysql_convert_table_format.1.gz
%{_mandir}/man1/mysqldump.1.gz
%{_mandir}/man1/mysqldumpslow.1.gz
%{_mandir}/man1/mysql_find_rows.1.gz
%{_mandir}/man1/mysql_fix_extensions.1.gz
%{_mandir}/man1/mysql_plugin.1.gz
%{_mandir}/man1/mysql_setpermission.1.gz
%{_mandir}/man1/mysqlshow.1.gz
%{_mandir}/man1/mysqlslap.1.gz
%{_mandir}/man1/mysql-stress-test.pl.1.gz
%{_mandir}/man1/mysqltest.1.gz
%{_mandir}/man1/mysqltest_embedded.1.gz
%{_mandir}/man1/mysql-test-run.pl.1.gz
%{_mandir}/man1/mysql_tzinfo_to_sql.1.gz
%{_mandir}/man1/mysql_waitpid.1.gz
%{_mandir}/man1/perror.1.gz
%{_mandir}/man1/%{name}-access.1.gz
%{_mandir}/man1/%{name}-binlog.1.gz
%{_mandir}/man1/%{name}-check.1.gz
%{_mandir}/man1/%{name}-client-test.1.gz
%{_mandir}/man1/%{name}-client-test-embedded.1.gz
%{_mandir}/man1/%{name}-test-embedded.1.gz
%{_mandir}/man1/mysql_embedded.1.gz
%{_mandir}/man1/%{name}-embedded.1.gz
%{_mandir}/man1/%{name}-conv.1.gz
%{_mandir}/man1/%{name}-convert-table-format.1.gz
%{_mandir}/man1/%{name}-dump.1.gz
%{_mandir}/man1/%{name}-dumpslow.1.gz
%{_mandir}/man1/%{name}-find-rows.1.gz
%{_mandir}/man1/%{name}-fix-extensions.1.gz
%{_mandir}/man1/%{name}-import.1.gz
%{_mandir}/man1/mysql_ldb.1.gz
%{_mandir}/man1/%{name}-ldb.1.gz
%{_mandir}/man1/%{name}-plugin.1.gz
%{_mandir}/man1/%{name}-setpermission.1.gz
%{_mandir}/man1/%{name}-show.1.gz
%{_mandir}/man1/%{name}-slap.1.gz
%{_mandir}/man1/%{name}-test.1.gz
%{_mandir}/man1/%{name}-waitpid.1.gz
%{_mandir}/man1/mariadbd-safe-helper.1.gz
%{_mandir}/man1/mariadbd-safe.1.gz
%config(noreplace) %{_sysconfdir}/my.cnf.d/s3.cnf
%config(noreplace) %{_sysconfdir}/my.cnf.d/spider.cnf
%doc COPYING CREDITS
%{_sysusersdir}/%{name}.sysusers
%exclude %{_datadir}/mysql/bench
%exclude %{_datadir}/mysql/test
%exclude %{_datadir}/doc/%{name}-%{version}/*

%files server
%config(noreplace) %{_sysconfdir}/logrotate.d/mysql
%config(noreplace) %{_sysconfdir}/my.cnf
%config(noreplace) %{_sysconfdir}/my.cnf.d/client.cnf
%config(noreplace) %{_sysconfdir}/my.cnf.d/enable_encryption.preset
%config(noreplace) %{_sysconfdir}/my.cnf.d/mysql-clients.cnf
%config(noreplace) %{_sysconfdir}/my.cnf.d/server.cnf
%config(noreplace) %{_sysconfdir}/my.cnf.d/provider_bzip2.cnf
%config(noreplace) %{_sysconfdir}/my.cnf.d/hashicorp_key_management.cnf
%dir %attr(0750,mysql,mysql) %{_sharedstatedir}/mysql
%{_libdir}/mysql/plugin*
%{_bindir}/%{name}-install-db
%{_bindir}/%{name}-backup
%{_bindir}/%{name}-hotcopy
%{_bindir}/aria_chk
%{_bindir}/aria_dump_log
%{_bindir}/aria_ftdump
%{_bindir}/aria_pack
%{_bindir}/aria_read_log
%{_bindir}/mysql_upgrade
%{_bindir}/innochecksum
%{_bindir}/mariabackup
%{_bindir}/%{name}-service-convert
%{_bindir}/%{name}-secure-installation
%{_bindir}/%{name}-tzinfo-to-sql
%{_bindir}/mbstream
%{_bindir}/myisam_ftdump
%{_bindir}/myisamchk
%{_bindir}/myisamlog
%{_bindir}/myisampack
%{_bindir}/mysql_install_db
%{_bindir}/mariadbd-multi
%{_bindir}/mysql_secure_installation
%{_bindir}/mysql_tzinfo_to_sql
%{_bindir}/mysqld_safe
%{_bindir}/mysqld_multi
%{_bindir}/%{name}-upgrade
%{_bindir}/mysqld_safe_helper
%{_bindir}/mysqldumpslow
%{_bindir}/mysqlhotcopy
%{_bindir}/my_print_defaults
%{_bindir}/replace
%{_bindir}/resolve_stack_dump
%{_bindir}/resolveip
%{_bindir}/wsrep_sst_common
%{_bindir}/wsrep_sst_mariabackup
%{_bindir}/wsrep_sst_mysqldump
%{_bindir}/wsrep_sst_rsync
%{_bindir}/wsrep_sst_rsync_wan
%{_bindir}/wsrep_sst_backup
%{_sbindir}/*
%{_unitdir}/*.service
%{_unitdir}/*.socket
%{_presetdir}/50-%{name}.preset
%{_datadir}/binary-configure
%{_datadir}/mysql-log-rotate
%{_datadir}/mysql.server
%{_datadir}/mysqld_multi.server
%{_datadir}/policy/apparmor/README
%{_datadir}/policy/apparmor/usr.sbin.mysqld
%{_datadir}/policy/apparmor/usr.sbin.mysqld.local
%{_datadir}/policy/selinux/README
%{_datadir}/policy/selinux/%{name}-server.fc
%{_datadir}/policy/selinux/%{name}-server.te
%{_datadir}/policy/selinux/%{name}.te
%{_datadir}/wsrep.cnf
%{_datadir}/wsrep_notify
%{_datadir}/mini-benchmark
%{_mandir}/man1/aria_s3_copy.1.gz
%{_mandir}/man1/aria_chk.1.gz
%{_mandir}/man1/aria_dump_log.1.gz
%{_mandir}/man1/aria_ftdump.1.gz
%{_mandir}/man1/aria_pack.1.gz
%{_mandir}/man1/aria_read_log.1.gz
%{_mandir}/man1/innochecksum.1.gz
%{_mandir}/man1/%{name}-service-convert.1.gz
%{_mandir}/man1/myisamchk.1.gz
%{_mandir}/man1/myisam_ftdump.1.gz
%{_mandir}/man1/myisamlog.1.gz
%{_mandir}/man1/myisampack.1.gz
%{_mandir}/man1/my_print_defaults.1.gz
%{_mandir}/man1/my_safe_process.1.gz
%{_mandir}/man1/mysqld_multi.1.gz
%{_mandir}/man1/mysqld_safe.1.gz
%{_mandir}/man1/mysqld_safe_helper.1.gz
%{_mandir}/man1/mysqlhotcopy.1.gz
%{_mandir}/man1/mysqlimport.1.gz
%{_mandir}/man1/mysql_upgrade.1.gz
%{_mandir}/man1/mysql_install_db.1.gz
%{_mandir}/man1/mysql.server.1.gz
%{_mandir}/man1/%{name}-install-db.1.gz
%{_mandir}/man1/replace.1.gz
%{_mandir}/man1/resolveip.1.gz
%{_mandir}/man1/resolve_stack_dump.1.gz
%{_mandir}/man1/wsrep_sst_common.1.gz
%{_mandir}/man1/wsrep_sst_mysqldump.1.gz
%{_mandir}/man1/wsrep_sst_rsync.1.gz
%{_mandir}/man1/mysql_secure_installation.1.gz
%{_mandir}/man1/mariabackup.1.gz
%{_mandir}/man1/mbstream.1.gz
%{_mandir}/man1/wsrep_sst_mariabackup.1.gz
%{_mandir}/man1/wsrep_sst_rsync_wan.1.gz
%{_mandir}/man1/%{name}-admin.1.gz
%{_mandir}/man1/%{name}-backup.1.gz
%{_mandir}/man1/%{name}-hotcopy.1.gz
%{_mandir}/man1/%{name}-tzinfo-to-sql.1.gz
%{_mandir}/man1/%{name}-upgrade.1.gz
%{_mandir}/man1/%{name}.1.gz
%{_mandir}/man1/mariadb_config.1.gz
%{_mandir}/man1/mariadbd-multi.1.gz
%{_mandir}/man1/myrocks_hotbackup.1.gz
%{_mandir}/man1/mytop.1.gz
%{_mandir}/man1/%{name}-secure-installation.1.gz
%{_mandir}/man8/*
%{_datadir}/mysql/fill_help_tables.sql
%{_datadir}/mysql/maria_add_gis_sp.sql
%{_datadir}/mysql/maria_add_gis_sp_bootstrap.sql
%{_datadir}/mysql/mroonga/install.sql
%{_datadir}/mysql/mroonga/uninstall.sql
%{_datadir}/mysql/mysql_performance_tables.sql
%{_datadir}/mysql/mysql_system_tables.sql
%{_datadir}/mysql/mysql_system_tables_data.sql
%{_datadir}/mysql/mysql_test_data_timezone.sql
%{_datadir}/mysql/mysql_test_db.sql
%{_datadir}/mysql/mysql_sys_schema.sql
%license %{_datadir}/mysql/mroonga/AUTHORS
%license %{_datadir}/mysql/mroonga/COPYING
%license %{_datadir}/groonga-normalizer-mysql/lgpl-2.0.txt
%license %{_datadir}/groonga/COPYING
%doc %{_datadir}/groonga-normalizer-mysql/README.md
%doc %{_datadir}/groonga/README.md

%files server-galera
%{_bindir}/galera_new_cluster
%{_bindir}/galera_recovery
%{_datadir}/systemd/use_galera_new_cluster.conf
%{_mandir}/man1/galera_new_cluster.1.gz
%{_mandir}/man1/galera_recovery.1.gz

%files devel
%{_includedir}/mysql/*
%{_datadir}/aclocal/mysql.m4
%{_libdir}/libmariadb.so
%{_libdir}/libmariadbd.so
%{_libdir}/libmysqld.so
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/pkgconfig/libmariadb.pc
%{_mandir}/man3/*.3.gz

%files errmsg
%{_datadir}/mysql/czech/errmsg.sys
%{_datadir}/mysql/danish/errmsg.sys
%{_datadir}/mysql/dutch/errmsg.sys
%{_datadir}/mysql/english/errmsg.sys
%{_datadir}/mysql/errmsg-utf8.txt
%{_datadir}/mysql/estonian/errmsg.sys
%{_datadir}/mysql/french/errmsg.sys
%{_datadir}/mysql/german/errmsg.sys
%{_datadir}/mysql/greek/errmsg.sys
%{_datadir}/mysql/hungarian/errmsg.sys
%{_datadir}/mysql/italian/errmsg.sys
%{_datadir}/mysql/japanese/errmsg.sys
%{_datadir}/mysql/korean/errmsg.sys
%{_datadir}/mysql/norwegian-ny/errmsg.sys
%{_datadir}/mysql/norwegian/errmsg.sys
%{_datadir}/mysql/polish/errmsg.sys
%{_datadir}/mysql/portuguese/errmsg.sys
%{_datadir}/mysql/romanian/errmsg.sys
%{_datadir}/mysql/russian/errmsg.sys
%{_datadir}/mysql/serbian/errmsg.sys
%{_datadir}/mysql/slovak/errmsg.sys
%{_datadir}/mysql/spanish/errmsg.sys
%{_datadir}/mysql/swedish/errmsg.sys
%{_datadir}/mysql/ukrainian/errmsg.sys
%{_datadir}/mysql/hindi/errmsg.sys
%{_datadir}/mysql/bulgarian/errmsg.sys
%{_datadir}/mysql/chinese/errmsg.sys

%changelog
* Fri Nov 24 2023 Shreenidhi Shedi <sshedi@vmware.com> 10.9.4-9
- Bump version as a part of gnutls upgrade
* Sun Nov 19 2023 Shreenidhi Shedi <sshedi@vmware.com> 10.9.4-8
- Bump version as a part of openssl upgrade
* Tue Oct 31 2023 Shreenidhi Shedi <sshedi@vmware.com> 10.9.4-7
- Fix devel package requires
* Sat Oct 07 2023 Shreenidhi Shedi <sshedi@vmware.com> 10.9.4-6
- Fix error in post install
* Fri Jul 28 2023 Srish Srinivasan <ssrish@vmware.com> 10.9.4-5
- Bump version as a part of krb5 upgrade
* Wed Apr 19 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 10.9.4-4
- Bump version as a part of libxml2 upgrade
* Fri Apr 14 2023 Shreenidhi Shedi <sshedi@vmware.com> 10.9.4-3
- Bump version as a part of zlib upgrade
* Fri Mar 10 2023 Mukul Sikka <msikka@vmware.com> 10.9.4-2
- Use systemd-rpm-macros for user creation
* Thu Feb 02 2023 Nitesh Kumar <kunitesh@vmware.com> 10.9.4-1
- Upgrade to v10.9.4 to fix CVE-2022-47015
* Thu Jan 26 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 10.9.2-3
- Bump version as a part of krb5 upgrade
* Tue Aug 30 2022 Shreenidhi Shedi <sshedi@vmware.com> 10.9.2-2
- Bump version as a part of gnutls upgrade
* Thu Aug 25 2022 Shreenidhi Shedi <sshedi@vmware.com> 10.9.2-1
- Upgrade to v10.9.2 to fix CVE-2022-32091
* Mon May 23 2022 Shreenidhi Shedi <sshedi@vmware.com> 10.8.3-1
- Upgrade to v10.8.3
* Thu Mar 03 2022 Shreenidhi Shedi <sshedi@vmware.com> 10.8.2-1
- CVE fixes
* Wed Feb 09 2022 Shreenidhi Shedi <sshedi@vmware.com> 10.8.1-1
- Upgrade version 10.8.1
* Thu Nov 11 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 10.7.1-2
- Bump up release for openssl
* Tue Nov 09 2021 Shreenidhi Shedi <sshedi@vmware.com> 10.7.1-1
- Upgrade to v10.7.1
* Mon Aug 23 2021 Shreyas B <shreyasb@vmware.com> 10.5.12-1
- Upgrade to v10.5.12 and adding libaio for Async I/O support
* Mon Jun 7 2021 Michelle Wang <michellew@vmware.com> 10.5.9-2
- Add shadow as requires for mariadb-server.
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 10.5.9-1
- Automatic Version Bump
* Wed Dec 02 2020 Tapas Kundu <tkundu@vmware.com> 10.5.5-3
- mariadb-server packages files symlinks to the binary files in mariadb.
- repackaged the files.
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 10.5.5-2
- openssl 1.1.1
* Wed Aug 19 2020 Gerrit Photon <photon-checkins@vmware.com> 10.5.5-1
- Automatic Version Bump
* Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 10.5.4-1
- Automatic Version Bump
* Wed Jan 23 2019 Ajay Kaher <akaher@vmware.com> 10.3.11-2
- Remove PerconaFT from mariadb pkg because of AGPL licence
* Wed Jan 02 2019 Him Kalyan Bordoloi <bordoloih@vmware.com> 10.3.11-1
- Upgrade to version 10.3.11
* Mon Nov 19 2018 Ajay Kaher <akaher@vmware.com> 10.3.9-3
- Enabling for aarch64
* Mon Oct 22 2018 Ajay Kaher <akaher@vmware.com> 10.3.9-2
- Adding BuildArch
* Thu Sep 06 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 10.3.9-1
- Update to version 10.3.9
* Tue Nov 07 2017 Xiaolin Li <xiaolinl@vmware.com> 10.2.10-1
- Update to verion 10.2.10 to address CVE-2017-10378, CVE-2017-10268
* Wed Sep 06 2017 Xiaolin Li <xiaolinl@vmware.com> 10.2.8-1
- Update to 10.2.8 and enable build server.
* Thu Aug 31 2017 Xiaolin Li <xiaolinl@vmware.com> 10.1.24-3
- Fixed make check issue.
* Fri Aug 25 2017 Dheeraj Shetty <dheerajs@vmware.com> 10.1.24-2
- Specify MariaDB conflicts with MySQL
* Wed Apr 05 2017 Xiaolin Li <xiaolinl@vmware.com> 10.1.24-1
- Initial packaging for Photon
