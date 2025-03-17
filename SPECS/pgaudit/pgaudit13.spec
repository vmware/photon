%define srcname         pgaudit
%global pgmajorversion  13
%global _pgbaseinstdir  %{_usr}/pgsql/%{pgmajorversion}
%global _pglibdir       %{_pgbaseinstdir}/lib/postgresql
%global _pgdatadir      %{_pgbaseinstdir}/share/postgresql

Name:       pgaudit13
Version:    1.5.2
Release:    4%{?dist}
Summary:    PostgreSQL Audit Extension
URL:        http://pgaudit.org
Group:      Applications/Databases
Vendor:     VMware, Inc.
Distribution:   Photon

Source0: https://github.com/pgaudit/pgaudit/archive/refs/tags/%{srcname}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

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
* Wed Dec 11 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.5.2-4
- Release bump for SRP compliance
* Fri Jul 28 2023 Srish Srinivasan <ssrish@vmware.com> 1.5.2-3
- Bump version as a part of krb5 upgrade
* Thu Jan 26 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 1.5.2-2
- Bump version as a part of krb5 upgrade
* Mon Jan 16 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.5.2-1
- Initial version.
