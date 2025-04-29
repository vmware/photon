%define srcname repmgr

%define _pg16basedir    %{_usr}/pgsql/16

Summary:        Replication Manager for PostgreSQL Clusters
Name:           repmgr16
Version:        5.3.3
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
BuildRequires: postgresql16-devel
BuildRequires: cyrus-sasl
BuildRequires: openldap
BuildRequires: krb5-devel
BuildRequires: libedit-devel

Requires: libedit
Requires: postgresql16
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
%{_pg16basedir}/bin/*
%{_pg16basedir}/lib/*
%{_pg16basedir}/share/*

%changelog
* Thu Apr 10 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 5.3.3-1
- Build with pgsql16
