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
%define sha512  serf=9f5418d991840a08d293d1ecba70cd9534a207696d002f22dbe62354e7b005955112a0d144a76c89c7f7ad3b4c882e54974441fafa0c09c4aa25c49c021ca75d
Requires:       openldap
Requires:       openssl
BuildRequires:  apr-devel
BuildRequires:  apr-util-devel
BuildRequires:  scons
BuildRequires:  openssl-devel
BuildRequires:  openldap
BuildRequires:  python2-devel

%description
The Apache Serf library is a C-based HTTP client library built upon the Apache
Portable Runtime (APR) library. It multiplexes connections, running the
read/write communication asynchronously. Memory copies and transformations are
kept to a minimum to provide high performance operation.

%package        devel
Summary:        Header and development files
Requires:       %{name} = %{version}-%{release}
%description    devel
It contains the libraries and header files to create serf applications.

%prep
%autosetup -p1

%build
scons PREFIX=%{_prefix}

%install
scons PREFIX=%{buildroot}%{_prefix} install

%check
scons check

%files
%defattr(-,root,root)
%exclude %{_libdir}/libserf-1.a
%{_libdir}/libserf-1.so.*

%files devel
%{_includedir}/*
%{_libdir}/libserf-1.so
%{_libdir}/pkgconfig/*

%changelog
*   Tue Apr 25 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 1.3.9-2
-   Version bump for scons upgrade
*   Mon Jan 22 2018 Xiaolin Li <xiaolinl@vmware.com> 1.3.9-1
-   Initial build. First version
