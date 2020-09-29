Summary:        A high performance C-based HTTP client library built upon the Apache Portable Runtime (APR) library
Name:           serf
Version:        1.3.9
Release:        4%{?dist}
License:        Apache License 2.0
URL:            https://serf.apache.org/
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://www.apache.org/dist/serf/%{name}-%{version}.tar.bz2
%define sha1    serf=26015c63e3bbb108c1689bf2090e4c26351db674
Requires:       openldap
BuildRequires:  python3-setuptools
BuildRequires:  apr-devel
BuildRequires:  apr-util-devel
BuildRequires:  scons
BuildRequires:  openssl-devel
BuildRequires:  openldap

%description
The Apache Serf library is a C-based HTTP client library built upon the Apache
Portable Runtime (APR) library. It multiplexes connections, running the
read/write communication asynchronously. Memory copies and transformations are
kept to a minimum to provide high performance operation.

%package        devel
Summary:        Header and development files
Requires:       %{name} = %{version}
%description    devel
It contains the libraries and header files to create serf applications.

%prep
%setup -q

%build
ln -sf /usr/bin/python3 /usr/bin/python
sed -i "/Append/s:RPATH=libdir,::"          SConstruct &&
sed -i "/Default/s:lib_static,::"           SConstruct &&
sed -i "/Alias/s:install_static,::"         SConstruct &&
sed -i "/  print/{s/print/print(/; s/$/)/}" SConstruct &&
sed -i "/get_contents()/s/,/.decode()&/"    SConstruct &&
scons PREFIX=%{_prefix}

%install
scons PREFIX=%{buildroot}%{_prefix} install

%check
scons check

%files
%defattr(-,root,root)
%{_libdir}/libserf-1.so.*

%files devel
%{_includedir}/*
%{_libdir}/libserf-1.so
%{_libdir}/pkgconfig/*


%changelog
*   Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.3.9-4
-   openssl 1.1.1
*   Sat Aug 15 2020 Tapas Kundu <tkundu@vmware.com> 1.3.9-3
-   Add setuptools in requires
*   Mon Jul 06 2020 Tapas Kundu <tkundu@vmware.com> 1.3.9-2
-   Build with python3
-   Mass removal python2
-   Remove static
*   Mon Jan 22 2018 Xiaolin Li <xiaolinl@vmware.com> 1.3.9-1
-   Initial build. First version
