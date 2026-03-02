%global build_if %{photon_subrelease} >= 92

%define srcname repmgr
%define _pgbasedir    %{_usr}/pgsql/18

Summary:        Replication Manager for PostgreSQL Clusters
Name:           repmgr18
Version:        5.5.0
Release:        1%{?dist}
URL:            https://repmgr.org
Group:          Applications/Databases
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://repmgr.org/download/%{srcname}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires: cpio
BuildRequires: Linux-PAM-devel
BuildRequires: postgresql18-devel
BuildRequires: cyrus-sasl
BuildRequires: openldap
BuildRequires: krb5-devel
BuildRequires: libedit-devel
BuildRequires: curl-devel
BuildRequires: json-c-devel

Requires: json-c
Requires: curl-libs
Requires: libedit
Requires: postgresql18
Requires: openssl
Requires: krb5
Requires: openldap
Requires: cyrus-sasl
Requires: zlib
Requires: readline

%description
repmgr is an open-source tool suite for managing replication and failover in a cluster of PostgreSQL servers.

%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
%configure
%make_build

%install
%make_install %{?_smp_mflags}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%exclude %dir %{_libdir}/debug
%dir %{_usr}/pgsql
%dir %{_pgbasedir}
%dir %{_pgbasedir}/bin
%dir %{_pgbasedir}/share
%{_pgbasedir}/bin/*
%{_pgbasedir}/lib/*
%{_pgbasedir}/share/*

%changelog
* Mon Mar 02 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 5.5.0-1
- Initial version
