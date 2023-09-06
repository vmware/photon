%define srcname repmgr

%define _pg13basedir    %{_usr}/pgsql/13

Summary:        Replication Manager for PostgreSQL Clusters
Name:           repmgr13
Version:        5.2.1
Release:        4%{?dist}
License:        GNU Public License (GPL) v3
URL:            https://repmgr.org
Group:          Applications/Databases
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://repmgr.org/download/%{srcname}-%{version}.tar.gz
%define sha512 %{srcname}=609ca27322087a042ede3a54565e425e9f39d74df510cbc103390cf60a31b35ce311cd942d5efd062bec2026864bd45466dbaf323963060d3ce89ce167c2a0b1

BuildRequires: postgresql13-devel
BuildRequires: cyrus-sasl
BuildRequires: openldap
BuildRequires: krb5-devel

Requires: postgresql13
Requires: openssl
Requires: krb5
Requires: openldap
Requires: cyrus-sasl

Provides: repmgr = %{version}-%{release}

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
* Wed Sep 06 2023 Shreenidhi Shedi <sshedi@vmware.com> 5.2.1-4
- repmg13 for pgsql13
* Fri Nov 18 2022 Shreenidhi Shedi <sshedi@vmware.com> 5.2.1-3
- Require psql or psql13
* Sat Mar 26 2022 Shreenidhi Shedi <sshedi@vmware.com> 5.2.1-2
- Exclude debug symbols properly
* Thu Aug 26 2021 Sujay G <gsujay@vmware.com> 5.2.1-1
- Bump version to 5.2.1 as requested in PR#2824906
* Mon May 04 2020 Sujay G <gsujay@vmware.com> 5.1.0-1
- Bump to version 5.1.0
* Thu Apr 09 2020 Stanislav Paskalev <spaskalev@vmware.com> 5.0.0-1
- Initial build.  First version
