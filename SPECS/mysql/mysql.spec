Summary:        MySQL.
Name:           mysql
Version:        5.7.18
Release:        1%{?dist}
License:        GPLv2
Group:          Applications/Databases
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            http://www.mysql.com
Source0:        http://mirrors.syringanetworks.net/mariadb/mysql-boost-%{version}/source/mysql-boost-%{version}.tar.gz
%define         sha1 mysql-boost=346e91db0160434488493966054eb25f712c89c8

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
*   Tue Jun 13 2017 Xiaolin Li <xiaolinl@vmware.com> 5.7.18-1
-   Initial packaging for Photon
