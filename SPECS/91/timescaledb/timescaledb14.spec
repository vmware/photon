%global build_if 0

%define srcname         timescaledb
%global pgmajorversion  14
%global _pgbaseinstdir  %{_usr}/pgsql/%{pgmajorversion}
%global _pglibdir       %{_pgbaseinstdir}/lib/postgresql
%global _pgdatadir      %{_pgbaseinstdir}/share/postgresql

Summary:        A PostgreSQL extension for high-performance real-time analytics
Name:           timescaledb14
Version:        2.19.2
Release:        3%{?dist}
URL:            https://www.timescale.com
Group:          Productivity/Databases/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/timescale/timescaledb/archive/refs/tags/%{srcname}-%{version}.tar.gz
Source1: license.txt
%include %{SOURCE1}

BuildRequires: cmake
BuildRequires: postgresql%{pgmajorversion}-devel

Requires: postgresql%{pgmajorversion}-libs

%description
TimescaleDB is an database built as an extension of PostgreSQL,
designed to efficiently handle and analyze large volumes of time-series data.
It combines the reliability and SQL capabilities of PostgreSQL with
optimizations for time-series and event workloads.

%prep
%autosetup -n %{srcname}-%{version}

%build
%cmake \
    -DAPACHE_ONLY=1 \
    -DREGRESS_CHECKS=OFF \
    -DSEND_TELEMETRY_DEFAULT=OFF

%{cmake_build}

%install
%{cmake_install}

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%license LICENSE-APACHE
%doc README.md
%dir %{_usr}/pgsql
%dir %{_pgbaseinstdir}
%dir %{_pgbaseinstdir}/lib
%dir %{_pglibdir}
%dir %{_pgbaseinstdir}/share
%dir %{_pgdatadir}
%dir %{_pgdatadir}/extension
%{_pglibdir}/%{srcname}-%{version}.so
%{_pglibdir}/%{srcname}.so
%{_pgdatadir}/extension/%{srcname}--*%{version}.sql
%{_pgdatadir}/extension/%{srcname}.control
%exclude %{_pglibdir}/pgxs/src/test/perl/

%changelog
* Fri Jun 26 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 2.19.2-3
- Restore timescaledb14 for subrelease >= 91
* Fri Aug 08 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.19.2-2
- Fix directory ownership during file packaging
* Thu Jun 05 2025 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 2.19.2-1
- Initial Build
