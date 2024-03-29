%define srcname         pgaudit
%global pgmajorversion  15
%global _pgbaseinstdir  %{_usr}/pgsql/%{pgmajorversion}
%global _pglibdir       %{_pgbaseinstdir}/lib/postgresql
%global _pgdatadir      %{_pgbaseinstdir}/share/postgresql

Name:       pgaudit15
Version:    1.7.0
Release:    4%{?dist}
Summary:    PostgreSQL Audit Extension
License:    PostgreSQL
URL:        http://pgaudit.org
Group:      Applications/Databases
Vendor:     VMware, Inc.
Distribution:   Photon

Source0: https://github.com/pgaudit/pgaudit/archive/refs/tags/%{srcname}-%{version}.tar.gz
%define sha512 %{srcname}=34a8b6e448a99add4c5d659095632aa0ec421b27289a0c220d198b9352e9225617b5904a23a30da45a4918823847d2fb995470e3b66060754436f9cf2dcb65f4

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
* Sun Nov 19 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.7.0-4
- Bump version as a part of openssl upgrade
* Fri Jul 28 2023 Srish Srinivasan <ssrish@vmware.com> 1.7.0-3
- Bump version as a part of krb5 upgrade
* Thu Jan 26 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 1.7.0-2
- Bump version as a part of krb5 upgrade
* Fri Jan 20 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.7.0-1
- Initial version.
