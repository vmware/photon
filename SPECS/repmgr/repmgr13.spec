%define srcname repmgr

%define _pg13basedir    %{_usr}/pgsql/13

Summary:        Replication Manager for PostgreSQL Clusters
Name:           repmgr13
Version:        5.3.3
Release:        2%{?dist}
License:        GNU Public License (GPL) v3
URL:            https://repmgr.org
Group:          Applications/Databases
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://repmgr.org/download/%{srcname}-%{version}.tar.gz
%define sha512 %{srcname}=938eabd6a73296e657c199878050a7fac82285da9613d0fff861e969865a4c3725a13b548e84a17ee035ef536a738b67411b9c93fdafd8698bb76844f0834d15

BuildRequires: cpio
BuildRequires: Linux-PAM-devel
BuildRequires: postgresql13-devel
BuildRequires: cyrus-sasl
BuildRequires: openldap
BuildRequires: krb5-devel
BuildRequires: libedit-devel

Requires: libedit
Requires: postgresql13
Requires: openssl
Requires: krb5
Requires: openldap
Requires: cyrus-sasl
Requires: zlib
Requires: readline

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
* Sun Nov 19 2023 Shreenidhi Shedi <sshedi@vmware.com> 5.3.3-2
- Bump version as a part of openssl upgrade
* Thu Aug 24 2023 Shreenidhi Shedi <sshedi@vmware.com> 5.3.3-1
- repmgr13 for pgsql13
