Summary:        MySQL.
Name:           mysql
Version:        8.4.4
Release:        2%{?dist}
Group:          Applications/Databases
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            http://www.mysql.com

Source0: https://cdn.mysql.com/Downloads/MySQL-8.4/mysql-%{version}.tar.gz

Source1: %{name}.sysusers

Source2: license.txt
%include %{SOURCE2}

BuildRequires: cmake
BuildRequires: rpcsvc-proto-devel
BuildRequires: icu-devel
BuildRequires: libedit-devel
BuildRequires: libevent-devel
BuildRequires: curl-devel
BuildRequires: zstd-devel
BuildRequires: lz4-devel
BuildRequires: protobuf-devel
BuildRequires: openssl-devel
BuildRequires: libtirpc-devel
BuildRequires: ncurses-devel
BuildRequires: libnuma-devel
BuildRequires: libfido2-devel
BuildRequires: systemd-devel
BuildRequires: libaio-devel

Requires: icu
Requires: libedit
Requires: libevent
Requires: curl-libs
Requires: zstd-libs
Requires: lz4
Requires: protobuf
Requires: openssl
Requires: libtirpc
Requires: perl
Requires: ncurses-libs
Requires: libnuma
Requires: libfido2
Requires: libaio

%description
MySQL is a free, widely used SQL engine.
It can be used as a fast database as well as a rock-solid DBMS using a modular engine architecture.

%package devel
Summary:        Development headers for mysql
Requires:       %{name} = %{version}-%{release}

%description    devel
Development headers for developing applications linking to maridb

%package        icu-data-files
Summary:        MySQL packaging of ICU data files

%description    icu-data-files
This package contains ICU data files needed by MySQL regular expressions.

%prep
%autosetup -p1 %{name}-boost-%{version}

%build
%{cmake} \
  -DBUILD_CONFIG="mysql_release" \
  -DCMAKE_INSTALL_PREFIX="%{_prefix}" \
  -DINSTALL_LIBDIR="lib" \
  -DINSTALL_PLUGINDIR="lib/plugin" \
  -DINSTALL_SUPPORTFILESDIR="share/support-files" \
  -DINSTALL_LAYOUT=RPM \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DTMPDIR=%{_var}/tmp \
  -DWITH_BOOST=boost \
  -DCMAKE_C_FLAGS=-fPIC \
  -DCMAKE_CXX_FLAGS=-fPIC \
  -DWITH_EMBEDDED_SERVER=OFF \
  -DFORCE_INSOURCE_BUILD=1 \
  -DWITH_UNIT_TESTS=OFF \
  -DWITH_ROUTER=OFF \
  -DWITH_SYSTEM_LIBS=ON \
  -DMYSQL_UNIX_ADDR="%{_sharedstatedir}/%{name}/%{name}.sock" \
  -DDAEMON_NAME="mysqld" \
  -DNICE_PROJECT_NAME="MySQL" \
  -DWITH_SYSTEMD=1 \
  -DSYSTEMD_SERVICE_NAME="mysqld" \
  -DSYSTEMD_PID_DIR="/run/mysqld" \
  -DWITH_PROTOBUF=bundled

%{cmake_build}

%install
%{cmake_install}

# Ensure that needed directories exist
install -d -m 0751 %{buildroot}%{_sharedstatedir}/%{name}
install -d -m 0755 %{buildroot}/run/mysqld
install -d -m 0750 %{buildroot}%{_sharedstatedir}/%{name}-files
install -d -m 0750 %{buildroot}%{_sharedstatedir}/%{name}-keyring

pushd %{__cmake_builddir}
# Install config and logrotate
install -D -m 0644 packaging/rpm-common/%{name}.logrotate \
            %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

install -D -m 0644 packaging/rpm-common/my.cnf \
            %{buildroot}%{_sysconfdir}/my.cnf

install -d %{buildroot}%{_sysconfdir}/my.cnf.d
popd

rm -rf %{buildroot}%{_datadir}/%{name}-test \
       %{buildroot}%{_libdir}/*.a

install -p -D -m 0644 %{SOURCE1} %{buildroot}%{_sysusersdir}/%{name}.conf

%check
pushd %{__cmake_builddir}/%{name}-test
./%{name}-test-run.pl --parallel=$(nproc) \
                    --force --retry=2 \
                    --max-test-fail=9999 \
                    --summary-report=test-summary.log ||:
test $(grep -w "Completed:" var/test-summary.log | cut -d' ' -f5 | cut -d. -f1) -gt 95
popd

%clean
rm -rf %{buildroot}/*

%pre
if [ $1 -eq 1 ]; then
  %sysusers_create_compat %{SOURCE1}
fi

%post
/sbin/ldconfig
[ -e /var/log/mysqld.log ] || \
  install -m0640 -omysql -gmysql /dev/null /var/log/mysqld.log >/dev/null 2>&1 || :

%systemd_post mysqld.service

%preun
%systemd_preun mysqld.service

%postun
/sbin/ldconfig
%systemd_postun_with_restart mysqld.service

%files
%defattr(-,root,root)
%dir %attr(751,mysql,mysql) %{_sharedstatedir}/mysql
%dir %attr(755,mysql,mysql) /run/mysqld
%dir %attr(750,mysql,mysql) %{_sharedstatedir}/mysql-files
%dir %attr(750,mysql,mysql) %{_sharedstatedir}/mysql-keyring
%config(noreplace) %{_sysconfdir}/my.cnf
%dir %{_sysconfdir}/my.cnf.d
%{_sysusersdir}/%{name}.conf
%{_bindir}/*
%{_sbindir}/*
%{_libdir}/*.so.*
%dir %{_lib64dir}/%{name}/private
%{_lib64dir}/%{name}/private/*.so
%attr(755,root,root) %{_lib64dir}/%{name}/private/libprotobuf*.so.*
%{_libdir}/plugin/*
%{_datadir}/*
%{_unitdir}/*.service
%{_tmpfilesdir}/%{name}.conf
%{_sysconfdir}/logrotate.d/%{name}

%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_includedir}/*
%{_libdir}/pkgconfig/mysqlclient.pc

%files icu-data-files
%defattr(-,root,root)

%changelog
* Thu May 08 2025 Mukul Sikka <mukul.sikka@broadcom.com> 8.4.4-2
- Renaming sysusers to conf to fix auto user creation
* Tue Feb 04 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 8.4.4-1
- Upgrade to v8.4.4
* Thu Dec 12 2024 Ajay Kaher <ajay.kaher@broadcom.com> 8.4.2-2
- Release bump for SRP compliance
* Tue Jul 23 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 8.4.2-1
- Upgrade to v8.4.2 to fix a bunch of CVEs
* Fri May 10 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 8.4.0-1
- Upgrade to v8.4.0, fixes bunch of CVEs
* Fri Jan 19 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 8.3.0-1
- Upgrade to v8.3.0
* Wed Nov 29 2023 Shreenidhi Shedi <sshedi@vmware.com> 8.0.35-2
- Use bundled protobuf, build breaks with latest protobuf provided by system
* Wed Nov 08 2023 Shreenidhi Shedi <sshedi@vmware.com> 8.0.35-1
- Upgrade to v8.0.35
- Add systemd service files for mysql-server
* Sun Jul 23 2023 Shreenidhi Shedi <sshedi@vmware.com> 8.0.34-1
- Upgrade to v8.0.34
* Mon Jul 17 2023 Shreenidhi Shedi <sshedi@vmware.com> 8.0.33-4
- Use system libs
* Sat Jun 17 2023 Shreenidhi Shedi <sshedi@vmware.com> 8.0.33-3
- Bump version as a part of protobuf upgrade
* Thu Jun 01 2023 Nitesh Kumar <kunitesh@vmware.com> 8.0.33-2
- Bump version as a part of ncurses upgrade to v6.4
* Wed May 10 2023 Oliver Kurth <okurth@vmware.com> 8.0.33-1
- Upgrade to v8.0.33, fixing CVE-2023-21980 and others
* Fri Apr 14 2023 Shreenidhi Shedi <sshedi@vmware.com> 8.0.32-2
- Bump version as a part of zlib upgrade
* Fri Jan 27 2023 Shreenidhi Shedi <sshedi@vmware.com> 8.0.32-1
- Upgrade to v8.0.32
* Sun Nov 13 2022 Shreenidhi Shedi <sshedi@vmware.com> 8.0.31-2
- Bump version as a part of libtirpc upgrade
* Mon Oct 24 2022 Shreenidhi Shedi <sshedi@vmware.com> 8.0.31-1
- Upgrade to v8.0.31
* Tue Oct 04 2022 Shreenidhi Shedi <sshedi@vmware.com> 8.0.29-3
- Bump version as a part of icu upgrade
* Thu Jul 07 2022 Shreenidhi Shedi <sshedi@vmware.com> 8.0.29-2
- Use cmake macros for build & fix requires
* Mon May 02 2022 Nitesh Kumar <kunitesh@vmware.com> 8.0.29-1
- Upgrade version to 8.0.29 to fix bunch of CVE's
* Mon Jan 31 2022 Nitesh Kumar <kunitesh@vmware.com> 8.0.28-1
- Upgrade version to 8.0.28 to fix bunch of CVE's
* Wed Nov 10 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 8.0.27-2
- openssl 3.0.0 compatibility
* Wed Oct 27 2021 Tapas Kundu <tkundu@vmware.com> 8.0.27-1
- Update to 8.0.27
* Mon Aug 02 2021 Shreyas B <shreyasb@vmware.com> 8.0.26-1
- Update to 8.0.26
* Mon May 03 2021 Shreyas B <shreyasb@vmware.com> 8.0.24-1
- Update to 8.0.24
* Sat Mar 20 2021 Shreyas B <shreyasb@vmware.com> 8.0.23-1
- Update to 8.0.23
* Fri Feb 19 2021 Harinadh D <hdommaraju@vmware.com> 8.0.21-2
- Version bump up to build with latest protobuf
* Mon Oct 05 2020 Tapas Kundu <tkundu@vmware.com> 8.0.21-1
- Update to 8.0.21
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 8.0.19-2
- openssl 1.1.1
* Thu Apr 16 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 8.0.19-1
- Upgrade to version 8.0.19 to fix several CVEs
* Fri Oct 11 2019 Satya Naga Vasamsetty <svasamsetty@vmware.com> 8.0.17-1
- Upgrade to version 8.0.17 which addresses several CVEs
* Tue Jan 22 2019 Siju Maliakkal <smaliakkal@vmware.com> 8.0.14-1
- Upgrade to 8.0.14
* Wed Jan 02 2019 Him Kalyan Bordoloi <bordoloih@vmware.com> 8.0.13-1
- Upgrade to version 8.0.13
- Workaround for broken DCMAKE_BUILD_TYPE=RELEASE(Mysql Bug#92945). Revert in next version
* Mon Nov 19 2018 Ajay Kaher <akaher@vmware.com> 8.0.12-4
- Enabling for aarch64
* Mon Oct 22 2018 Ajay Kaher <akaher@vmware.com> 8.0.12-3
- Adding BuildArch
* Fri Sep 21 2018 Alexey Makhalov <amakhalov@vmware.com> 8.0.12-2
- Use libtirpc instead obsoleted rpc from glibc.
* Mon Sep 10 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 8.0.12-1
- Update to version 8.0.12
* Wed Aug 08 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 5.7.23-1
- Update to version 5.7.23 to get it to build with gcc 7.3
* Thu Jan 25 2018 Divya Thaluru <dthaluru@vmware.com> 5.7.20-2
- Added patch for CVE-2018-2696
* Wed Oct 25 2017 Xiaolin Li <xiaolinl@vmware.com> 5.7.20-1
- Update to version 5.7.20
* Fri Oct 13 2017 Alexey Makhalov <amakhalov@vmware.com> 5.7.18-3
- Fix typo in description
* Fri Jul 14 2017 Xiaolin Li <xiaolinl@vmware.com> 5.7.18-2
- Run make test in the %check section
* Tue Jun 13 2017 Xiaolin Li <xiaolinl@vmware.com> 5.7.18-1
- Initial packaging for Photon
