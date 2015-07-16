Summary:    The Apache Portable Runtime Utility Library
Name:       apr-util
Version:    1.5.4
Release:    3%{?dist}
License:    Apache License 2.0
URL:        https://apr.apache.org/
Group:      System Environment/Libraries
Vendor:     VMware, Inc.
Distribution: Photon
Source0:    http://archive.apache.org/dist/apr/%{name}-%{version}.tar.gz
%define sha1 apr-util=72cc3ac693b52fb831063d5c0de18723bc8e0095
%define     apuver    1

BuildRequires:   apr
BuildRequires:   openldap
BuildRequires:   openssl
BuildRequires:   openssl-devel
BuildRequires:   nss-devel
Requires:   apr
Requires:   openssl
Requires:   openldap
Requires:   postgresql
%description
The Apache Portable Runtime Utility Library.

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
rm %{buildroot}/usr/lib/libexpat.so
%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/*
%exclude %{_libdir}/debug
%{_bindir}/*
%{_includedir}/*

%changelog
*   Wed Jul 15 2015 Sarah Choi <sarahc@vmware.com> 1.5.4-4
-   Use apuver(=1) instead of version for mesos 
*   Mon Jul 13 2015 Alexey Makhalov <amakhalov@vmware.com> 1.5.2-3
-   Exclude /usr/lib/debug
*   Wed Jul 01 2015 Touseef Liaqat <tliaqat@vmware.com> 1.5.2-2
-   Fix tags and paths.
*   Wed May 20 2015 Touseef Liaqat <tliaqat@vmware.com> 1.5.4-1
-   Initial build. First version
