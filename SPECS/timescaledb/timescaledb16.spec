%define srcname         timescaledb
%global pgmajorversion  16
%global _pgbaseinstdir  %{_usr}/pgsql/%{pgmajorversion}
%global _pglibdir       %{_pgbaseinstdir}/lib/postgresql
%global _pgdatadir      %{_pgbaseinstdir}/share/postgresql

Summary:        A PostgreSQL extension for high-performance real-time analytics
Name:           timescaledb16
Version:        2.20.2
Release:        1%{?dist}
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
%{_pglibdir}/%{srcname}-%{version}.so
%{_pglibdir}/%{srcname}.so
%{_pgdatadir}/extension/%{srcname}--*%{version}.sql
%{_pgdatadir}/extension/%{srcname}.control
%exclude %{_pglibdir}/pgxs/src/test/perl/TimescaleNode.pm

%changelog
* Thu Jun 05 2025 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 2.20.2-1
- Initial Build
