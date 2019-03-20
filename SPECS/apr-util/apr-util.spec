Summary:        The Apache Portable Runtime Utility Library
Name:           apr-util
Version:        1.6.1
Release:        1%{?dist}
License:        Apache License 2.0
URL:            https://apr.apache.org/
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://archive.apache.org/dist/apr/%{name}-%{version}.tar.gz
%define sha1 apr-util=5bae4ff8f1dad3d7091036d59c1c0b2e76903bf4
%define         apuver    1

BuildRequires:  apr-devel
BuildRequires:  openssl
BuildRequires:  openssl-devel
BuildRequires:  nss-devel
Requires:       apr
Requires:       openssl
%description
The Apache Portable Runtime Utility Library.

%package devel
Group: Development/Libraries
Summary: APR utility library development kit
Requires: apr-devel
Requires: %{name} = %{version}
%description devel
This package provides the support files which can be used to 
build applications using the APR utility library.

%package ldap
Group: Development/Libraries
Summary: APR utility library LDAP support
BuildRequires: openldap
Requires: apr-util
Requires: openldap

%description ldap
This package provides the LDAP support for the apr-util.

%package pgsql
Group: Development/Libraries
Summary: APR utility library PostgreSQL DBD driver
BuildRequires: postgresql-devel
Requires: apr-util
Requires: postgresql

%description pgsql
This package provides the PostgreSQL driver for the apr-util DBD (database abstraction) interface.

%package sqlite
Group: Development/Libraries
Summary: APR utility library SQLite DBD driver.
Requires: apr-util

%description sqlite
This package provides the SQLite driver for the apr-util DBD
(database abstraction) interface.

%prep
%setup -q
%build
%configure --with-apr=%{_prefix} \
        --includedir=%{_includedir}/apr-%{apuver} \
        --with-ldap --without-gdbm \
        --with-sqlite3 --with-pgsql \
        --without-sqlite2 \
        --with-openssl=/usr \
        --with-nss \
        --with-crypto


make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/aprutil.exp
%{_libdir}/libaprutil-%{apuver}.so.*
%{_libdir}/apr-util-%{apuver}/apr_crypto_nss*
%{_libdir}/apr-util-%{apuver}/apr_crypto_openssl*
%exclude %{_libdir}/debug

%files devel
%defattr(-,root,root)
%{_libdir}/libaprutil-%{apuver}.*a
%{_libdir}/libaprutil-%{apuver}.so
%{_bindir}/*
%{_includedir}/*
%{_libdir}/pkgconfig/apr-util-%{apuver}.pc

%files ldap
%defattr(-,root,root,-)
%{_libdir}/apr-util-%{apuver}/apr_ldap*

%files pgsql
%defattr(-,root,root,-)
%{_libdir}/apr-util-%{apuver}/apr_dbd_pgsql*

%files sqlite
%defattr(-,root,root,-)
%{_libdir}/apr-util-%{apuver}/apr_dbd_sqlite*

%changelog
*   Sun Mar 10 2019 Tapas Kundu <tkundu@vmware.com> 1.6.1-1
-   Updated to 1.6.1
*   Thu Apr 13 2017 Xiaolin Li <xiaolinl@vmware.com> 1.5.4-8
-   BuildRequires postgresql-devel.
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.5.4-7
-   GA - Bump release of all rpms
*   Wed Apr 13 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.5.4-6
-   remove libexpat files
*   Tue Sep 22 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.5.4-5
-   Updated build-requires after creating devel package for apr. 
*   Wed Sep 16 2015 Xiaolin Li <xiaolinl@vmware.com> 1.5.4-4
-   Seperate Separate apr-util to apr-util, apr-util-devel, aprutil-ldap, apr-util-pgsql, and apr-utilsqlite.
*   Wed Jul 15 2015 Sarah Choi <sarahc@vmware.com> 1.5.4-4
-   Use apuver(=1) instead of version for mesos 
*   Mon Jul 13 2015 Alexey Makhalov <amakhalov@vmware.com> 1.5.2-3
-   Exclude /usr/lib/debug
*   Wed Jul 01 2015 Touseef Liaqat <tliaqat@vmware.com> 1.5.2-2
-   Fix tags and paths.
*   Wed May 20 2015 Touseef Liaqat <tliaqat@vmware.com> 1.5.4-1
-   Initial build. First version
