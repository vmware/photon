%define srcname repmgr

%define _pg13basedir    %{_usr}/pgsql/13

Summary:        Replication Manager for PostgreSQL Clusters
Name:           repmgr13
Version:        5.3.0
Release:        5%{?dist}
License:        GNU Public License (GPL) v3
URL:            https://repmgr.org
Group:          Applications/Databases
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://repmgr.org/download/%{srcname}-%{version}.tar.gz
%define sha512 %{srcname}=1b3c64a9746b7b3f7faf4475750913822b918d415fb0fc19fff5ee8f51c92aeb886d1c6f35b749fc76895b4512ca40c3b5bece57eb012d7d77467c4da72bb8db

BuildRequires: postgresql13-devel
BuildRequires: cyrus-sasl
BuildRequires: openldap
BuildRequires: krb5-devel

Requires: postgresql13
Requires: openssl
Requires: krb5
Requires: openldap
Requires: cyrus-sasl

%description
repmgr is an open-source tool suite for managing replication and failover
in a cluster of PostgreSQL servers.

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
%{_pg13basedir}/bin/*
%{_pg13basedir}/lib/*
%{_pg13basedir}/share/*

%changelog
* Thu Aug 24 2023 Shreenidhi Shedi <sshedi@vmware.com> 5.3.0-5
- repmgr13 for pgsql13
