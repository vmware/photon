Summary:        MySQL.
Name:           mysql
Version:        5.7.25
Release:        1%{?dist}
License:        GPLv2
Group:          Applications/Databases
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            http://www.mysql.com
Source0:        https://cdn.mysql.com//Downloads/MySQL-5.7/mysql-boost-%{version}.tar.gz
%define         sha1 mysql-boost=cbec35bbe2f2540232105a307770c432380be352

BuildRequires:  cmake
BuildRequires:  openssl-devel
BuildRequires:  zlib-devel
BuildRequires:  ncurses-devel

%description
MySQL is a free, widely used SQL engine. It can be used as a fast database as well as a rock-solid DBMS using a modular engine architecture.

%package devel
Summary:        Development headers for musql
Requires:       %{name} = %{version}-%{release}

%description devel
Development headers for developing applications linking to maridb


%prep
%setup -q %{name}-boost-%{version}

%build
cmake . \
      -DCMAKE_INSTALL_PREFIX=/usr   \
      -DWITH_BOOST=boost/boost_1_59_0 \
      -DINSTALL_MANDIR=share/man \
      -DINSTALL_DOCDIR=share/doc \
      -DINSTALL_DOCREADMEDIR=share/doc \
      -DINSTALL_SUPPORTFILESDIR=share/support-files \
      -DCMAKE_BUILD_TYPE=RELEASE \
      -DWITH_EMBEDDED_SERVER=OFF

make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install

%check
make check

%files
%defattr(-,root,root)
%doc COPYING  README
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
*   Wed Feb 14 2019 Him Kalyan Bordoloi <bordoloih@vmware.com> 5.7.25-1
-   Update to version 5.7.25 to fix CVE-2019-2534, CVE-2018-3155
*   Mon Jul 30 2018 Ajay Kaher <akaher@vmware.com> 5.7.23-1
-   Update to version 5.7.23 to fix CVE-2018-3064, CVE-2018-3060,
-   CVE-2018-3065, CVE-2018-3070, CVE-2018-3073, CVE-2018-3062,
-   CVE-2018-3074, CVE-2018-3081, CVE-2018-3054, CVE-2018-3061,
-   CVE-2018-3077, CVE-2018-3067, CVE-2018-3075, CVE-2018-3078,
-   CVE-2018-3079, CVE-2018-3080, CVE-2018-3056, CVE-2018-3058
*   Thu Apr 26 2018 Xiaolin Li <xiaolinl@vmware.com> 5.7.22-1
-   Update to version 5.7.22 to fix CVE-2018-2755
*   Tue Apr 17 2018 Xiaolin Li <xiaolinl@vmware.com> 5.7.21-1
-   Update to version 5.7.21 to fix CVE-2018-2583, CVE-2018-2665,
-   CVE-2018-2573, CVE-2018-2612, CVE-2018-2622, CVE-2018-2640
*   Thu Jan 25 2018 Divya Thaluru <dthaluru@vmware.com> 5.7.20-2
-   Added patch for CVE-2018-2696
*   Tue Oct 17 2017 Xiaolin Li <xiaolinl@vmware.com> 5.7.20-1
-   Update to version 5.7.20
*   Tue Jun 13 2017 Xiaolin Li <xiaolinl@vmware.com> 5.7.18-1
-   Initial packaging for Photon
