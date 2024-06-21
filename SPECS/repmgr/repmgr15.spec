%define srcname repmgr

%define _pg15basedir    %{_usr}/pgsql/15

Summary:        Replication Manager for PostgreSQL Clusters
Name:           repmgr15
Version:        5.3.3
Release:        1%{?dist}
License:        GNU Public License (GPL) v3
URL:            https://repmgr.org
Group:          Applications/Databases
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://repmgr.org/download/%{srcname}-%{version}.tar.gz
%define sha512 %{srcname}=938eabd6a73296e657c199878050a7fac82285da9613d0fff861e969865a4c3725a13b548e84a17ee035ef536a738b67411b9c93fdafd8698bb76844f0834d15

BuildRequires: cpio
BuildRequires: Linux-PAM-devel
BuildRequires: postgresql15-devel
BuildRequires: cyrus-sasl
BuildRequires: openldap
BuildRequires: krb5-devel
BuildRequires: libedit-devel
BuildRequires: lz4-devel
BuildRequires: libxml2-devel

Requires: libedit
Requires: postgresql15
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
%{_pg15basedir}/bin/*
%{_pg15basedir}/lib/*
%{_pg15basedir}/share/*

%changelog
* Wed Jun 19 2024 Ashwin Dayanand Kamat <ashwin.kamat@broadcom.com> 5.3.3-1
- Initial version
