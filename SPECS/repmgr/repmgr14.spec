%define srcname repmgr

%define _pgbasedir    %{_usr}/pgsql/14

Summary:        Replication Manager for PostgreSQL Clusters
Name:           repmgr14
Version:        5.3.3
Release:        3%{?dist}
URL:            https://repmgr.org
Group:          Applications/Databases
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://repmgr.org/download/%{srcname}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires: cpio
BuildRequires: Linux-PAM-devel
BuildRequires: postgresql14-devel
BuildRequires: cyrus-sasl
BuildRequires: openldap
BuildRequires: krb5-devel
BuildRequires: libedit-devel

Requires: libedit
Requires: postgresql14
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
%dir %{_usr}/pgsql
%dir %{_pgbasedir}
%dir %{_pgbasedir}/bin
%dir %{_pgbasedir}/share
%{_pgbasedir}/bin/*
%{_pgbasedir}/lib/*
%{_pgbasedir}/share/*

%changelog
* Fri Aug 08 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 5.3.3-3
- Fix directory ownership during file packaging
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 5.3.3-2
- Release bump for SRP compliance
* Sat Aug 19 2023 Shreenidhi Shedi <sshedi@vmware.com> 5.3.3-1
- repmgr14 for pgsql14
