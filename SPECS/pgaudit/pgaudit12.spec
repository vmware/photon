%define srcname         pgaudit
%global pgmajorversion  12
%global _pgbaseinstdir  %{_usr}/pgsql/%{pgmajorversion}
%global _pglibdir       %{_pgbaseinstdir}/lib/postgresql
%global _pgdatadir      %{_pgbaseinstdir}/share/postgresql

Name:       pgaudit12
Version:    1.4.3
Release:    1%{?dist}
Summary:    PostgreSQL Audit Extension
License:    PostgreSQL
URL:        http://pgaudit.org
Group:      Applications/Databases
Vendor:     VMware, Inc.
Distribution:   Photon

Source0: https://github.com/pgaudit/pgaudit/archive/refs/tags/%{srcname}-%{version}.tar.gz
%define sha512 %{srcname}=7503f99049752c000ece71c02d03199434e3e92a167079877ee7c66823c25379dffc9186970424681e52177febfbcc824694088af468bbb6be78ec2dfe943173

BuildRequires: build-essential
BuildRequires: postgresql%{pgmajorversion}-devel
BuildRequires: openssl-devel
BuildRequires: krb5-devel

Requires: openssl
Requires: postgresql%{pgmajorversion}-libs

%description
The PostgreSQL Audit extension (pgaudit) provides detailed session
and/or object audit logging via the standard PostgreSQL logging
facility.

The goal of the PostgreSQL Audit extension (pgaudit) is to provide
PostgreSQL users with capability to produce audit logs often required to
comply with government, financial, or ISO certifications.

An audit is an official inspection of an individual's or organization's
accounts, typically by an independent body. The information gathered by
the PostgreSQL Audit extension (pgaudit) is properly called an audit
trail or audit log. The term audit log is used in this documentation.

%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
%make_build USE_PGXS=1

%install
%make_install USE_PGXS=1

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_pglibdir}/%{srcname}.so
%{_pgdatadir}/extension/*.sql
%{_pgdatadir}/extension/*.control
%{_pglibdir}/bitcode/%{srcname}.index.bc
%{_pglibdir}/bitcode/%{srcname}/%{srcname}.bc

%changelog
* Mon Jan 16 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.4.3-1
- Initial version.
