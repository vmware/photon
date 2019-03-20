Summary:        A high performance C-based HTTP client library built upon the Apache Portable Runtime (APR) library
Name:           serf
Version:        1.3.9
Release:        2%{?dist}
License:        Apache License 2.0
URL:            https://serf.apache.org/
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://www.apache.org/dist/serf/%{name}-%{version}.tar.bz2
%define sha1    serf=26015c63e3bbb108c1689bf2090e4c26351db674
Requires:       openldap
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
%{_libdir}/libserf-1.a
%{_libdir}/pkgconfig/*


%changelog
*   Wed Mar 20 2019 Tapas Kundu <tkundu@vmware.com> 1.3.9-2
-   Bumped up to use latest openssl
*   Mon Jan 22 2018 Xiaolin Li <xiaolinl@vmware.com> 1.3.9-1
-   Initial build. First version
