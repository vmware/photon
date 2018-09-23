Summary:        MySQL.
Name:           mysql
Version:        8.0.12
Release:        2%{?dist}
License:        GPLv2
Group:          Applications/Databases
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            http://www.mysql.com
Source0:        https://cdn.mysql.com//Downloads/MySQL-5.7/mysql-boost-%{version}.tar.gz
%define         sha1 mysql-boost=c144d6c1350a9897da31ebbd3b5492ab1f152352

BuildRequires:  cmake
BuildRequires:  openssl-devel
BuildRequires:  zlib-devel
BuildRequires:  libtirpc-devel
BuildRequires:  rpcsvc-proto-devel

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
      -DWITH_BOOST=boost/boost_1_67_0 \
      -DINSTALL_MANDIR=share/man \
      -DINSTALL_DOCDIR=share/doc \
      -DINSTALL_DOCREADMEDIR=share/doc \
      -DINSTALL_SUPPORTFILESDIR=share/support-files \
      -DCMAKE_BUILD_TYPE=RELEASE \
      -DCMAKE_C_FLAGS=-fPIC \
      -DCMAKE_CXX_FLAGS=-fPIC \
      -DWITH_EMBEDDED_SERVER=OFF

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

%check
make test

%files
%defattr(-,root,root)
%doc LICENSE  README
%{_libdir}/plugin/*
%{_libdir}/libmysqlclient.so.*
%{_bindir}/*
%{_mandir}/man1/*
%{_mandir}/man8/*
%{_datadir}/support-files/*
%exclude /usr/mysql-test
%exclude /usr/docs
%exclude /usr/share

%files devel
%{_libdir}/libmysqlclient.so
%{_libdir}/*.a
%{_includedir}/*
%{_libdir}/pkgconfig/mysqlclient.pc

%changelog
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
