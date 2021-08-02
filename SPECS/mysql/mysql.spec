Summary:        MySQL.
Name:           mysql
Version:        8.0.26
Release:        1%{?dist}
License:        GPLv2
Group:          Applications/Databases
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            http://www.mysql.com
Source0:        https://dev.mysql.com/get/Downloads/MySQL-8.0/mysql-boost-%{version}.tar.gz
%define         sha1 mysql-boost=fbac872bbc125f0f05ce1f3224dbaeddf368da40

BuildRequires:  cmake
BuildRequires:  openssl-devel
BuildRequires:  zlib-devel
BuildRequires:  libtirpc-devel
BuildRequires:  rpcsvc-proto-devel
BuildRequires:  protobuf-devel
Requires:       protobuf

%description
MySQL is a free, widely used SQL engine. It can be used as a fast database as well as a rock-solid DBMS using a modular engine architecture.

%package devel
Summary:        Development headers for mysql
Requires:       %{name} = %{version}-%{release}

%description devel
Development headers for developing applications linking to maridb


%prep
%setup -q %{name}-boost-%{version}

%build
cmake . \
      -DCMAKE_INSTALL_PREFIX=/usr   \
      -DWITH_BOOST=boost/boost_1_73_0 \
      -DINSTALL_MANDIR=share/man \
      -DINSTALL_DOCDIR=share/doc \
      -DINSTALL_DOCREADMEDIR=share/doc \
      -DINSTALL_SUPPORTFILESDIR=share/support-files \
      -DCMAKE_BUILD_TYPE=RELEASE \
      -DCMAKE_C_FLAGS=-fPIC \
      -DCMAKE_CXX_FLAGS=-fPIC \
      -DWITH_EMBEDDED_SERVER=OFF \
      -DFORCE_INSOURCE_BUILD=1 \
      -DWITH_PROTOBUF=system

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

%check
make test

%files
%defattr(-,root,root)
%doc LICENSE  README router/LICENSE.router router/README.router
%{_libdir}/plugin/*
%{_libdir}/*.so.*
%{_libdir}/mysqlrouter/*.so
%{_libdir}/mysqlrouter/private/libmysql*.so.*
%{_bindir}/*
%{_mandir}/man1/*
%{_mandir}/man8/*
%{_datadir}/support-files/*
%exclude /usr/mysql-test
%exclude /usr/docs
%exclude /usr/share
%exclude /usr/*.router
%exclude /usr/mysqlrouter-log-rotate

%files devel
%{_libdir}/*.so
%{_libdir}/*.a
%{_includedir}/*
%{_libdir}/pkgconfig/mysqlclient.pc

%changelog
*   Mon Aug 02 2021 Shreyas B <shreyasb@vmware.com> 8.0.26-1
-   Update to 8.0.26
*   Mon May 03 2021 Shreyas B <shreyasb@vmware.com> 8.0.24-1
-   Update to 8.0.24
*   Tue Feb 02 2021 Shreyas B <shreyasb@vmware.com> 8.0.23-1
-   Update to 8.0.23
*   Mon Nov 02 2020 Shreyas B. <shreyasb@vmware.com> 8.0.22-1
-   Upgrade to v8.0.22
*   Mon Jul 20 2020 Tapas Kundu <tkundu@vmware.com> 8.0.21-1
-   Update to 8.0.21
*   Mon Jun 15 2020 Tapas Kundu <tkundu@vmware.com> 8.0.20-1
-   Update to 8.0.20
*   Thu Apr 16 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 8.0.19-1
-   Upgrade to version 8.0.19 to fix several CVEs
*   Wed Jul 31 2019 Him Kalyan Bordoloi <bordoloih@vmware.com> 8.0.17-1
-   Upgrade to version 8.0.17 to fix CVE-2019-2800, CVE-2019-2822 and more
*   Tue May 07 2019 Him Kalyan Bordoloi <bordoloih@vmware.com> 8.0.16-1
-   Upgrade to version 8.0.16 to fix CVE-2019-2632 and more
*   Tue Jan 22 2019 Siju Maliakkal <smaliakkal@vmware.com> 8.0.14-1
-   Upgrade to 8.0.14
*   Wed Jan 02 2019 Him Kalyan Bordoloi <bordoloih@vmware.com> 8.0.13-1
-   Upgrade to version 8.0.13
-   Workaround for broken DCMAKE_BUILD_TYPE=RELEASE(Mysql Bug#92945). Revert in next version
*   Mon Nov 19 2018 Ajay Kaher <akaher@vmware.com> 8.0.12-4
-   Enabling for aarch64
*   Mon Oct 22 2018 Ajay Kaher <akaher@vmware.com> 8.0.12-3
-   Adding BuildArch
*   Fri Sep 21 2018 Alexey Makhalov <amakhalov@vmware.com> 8.0.12-2
-   Use libtirpc instead obsoleted rpc from glibc.
*   Mon Sep 10 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 8.0.12-1
-   Update to version 8.0.12
*   Wed Aug 08 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 5.7.23-1
-   Update to version 5.7.23 to get it to build with gcc 7.3
*   Thu Jan 25 2018 Divya Thaluru <dthaluru@vmware.com> 5.7.20-2
-   Added patch for CVE-2018-2696
*   Wed Oct 25 2017 Xiaolin Li <xiaolinl@vmware.com> 5.7.20-1
-   Update to version 5.7.20
*   Fri Oct 13 2017 Alexey Makhalov <amakhalov@vmware.com> 5.7.18-3
-   Fix typo in description
*   Fri Jul 14 2017 Xiaolin Li <xiaolinl@vmware.com> 5.7.18-2
-   Run make test in the %check section
*   Tue Jun 13 2017 Xiaolin Li <xiaolinl@vmware.com> 5.7.18-1
-   Initial packaging for Photon
