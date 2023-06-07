Summary:        MySQL.
Name:           mysql
Version:        8.0.33
Release:        2%{?dist}
License:        GPLv2
Group:          Applications/Databases
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            http://www.mysql.com

Source0: https://dev.mysql.com/get/Downloads/MySQL-8.0/mysql-boost-%{version}.tar.gz
%define sha512 %{name}-boost=47f76819004c7c545d1b0b6b6646d8816899976f92d35c5564b1255b144b597ff7d3e674c721a45bcbb13cc0da3f4474fb29221c0e21d2ff91a1892cd42c636c

BuildRequires: cmake
BuildRequires: openssl-devel
BuildRequires: zlib-devel
BuildRequires: libtirpc-devel
BuildRequires: rpcsvc-proto-devel
BuildRequires: protobuf-devel
BuildRequires: libevent-devel

Requires: protobuf
Requires: libtirpc
Requires: libevent
Requires: zlib
Requires: openssl
Requires: ncurses-libs
Requires: perl
Requires: %{name}-icu-data-files = %{version}-%{release}

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
   -DCMAKE_INSTALL_PREFIX=%{_prefix} \
   -DWITH_BOOST=boost \
   -DINSTALL_MANDIR=share/man \
   -DINSTALL_DOCDIR=share/doc \
   -DINSTALL_DOCREADMEDIR=share/doc \
   -DINSTALL_SUPPORTFILESDIR=share/support-files \
   -DCMAKE_BUILD_TYPE=RELEASE \
   -DCMAKE_C_FLAGS=-fPIC \
   -DCMAKE_CXX_FLAGS=-fPIC \
   -DWITH_EMBEDDED_SERVER=OFF \
   -DFORCE_INSOURCE_BUILD=1 \
   -DWITH_PROTOBUF=system \
   -DWITH_ROUTER=OFF \
   -DWITH_UNIT_TESTS=OFF \
   -DWITH_LIBEVENT=system

%{cmake_build}

%install
%{cmake_install}

%if 0%{?with_check}
%check
pushd %{__cmake_builddir}/mysql-test
./mysql-test-run.pl --parallel=$(nproc) \
                    --force --retry=2 \
                    --max-test-fail=9999 \
                    --summary-report=test-summary.log ||:
[ $(grep -w "Completed:" var/test-summary.log | cut -d ' ' -f5 | cut -d '.' -f1) -gt 95 ]
popd
%endif

%{ldconfig_scriptlets}

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_libdir}/plugin/*
%{_libdir}/*.so.*
%{_bindir}/*
%{_mandir}/man1/*
%{_mandir}/man8/*
%{_datadir}/support-files/*
%exclude %{_usr}/mysql-test
%exclude %{_usr}/docs
%exclude %{_datadir}

%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/*.a
%{_includedir}/*
%{_libdir}/pkgconfig/mysqlclient.pc

%files icu-data-files
%defattr(-,root,root)
%{_libdir}/private/icudt69l

%changelog
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
