%define srcname repmgr

%define _pg14basedir    %{_usr}/pgsql/14

Summary:        Replication Manager for PostgreSQL Clusters
Name:           repmgr14
Version:        5.3.0
Release:        5%{?dist}
License:        GNU Public License (GPL) v3
URL:            https://repmgr.org
Group:          Applications/Databases
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://repmgr.org/download/%{srcname}-%{version}.tar.gz
%define sha512 %{srcname}=1b3c64a9746b7b3f7faf4475750913822b918d415fb0fc19fff5ee8f51c92aeb886d1c6f35b749fc76895b4512ca40c3b5bece57eb012d7d77467c4da72bb8db

BuildRequires: postgresql14-devel
BuildRequires: cyrus-sasl
BuildRequires: openldap
BuildRequires: krb5-devel

Requires: postgresql14
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
%{_pg14basedir}/bin/*
%{_pg14basedir}/lib/*
%{_pg14basedir}/share/*

%changelog
* Sat Aug 19 2023 Shreenidhi Shedi <sshedi@vmware.com> 5.3.0-5
- repmgr14 for pgsql14
* Fri Dec 09 2022 Shreenidhi Shedi <sshedi@vmware.com> 5.3.0-4
- Fix pgsql requires
* Tue Mar 01 2022 Shreenidhi Shedi <sshedi@vmware.com> 5.3.0-3
- Exclude debug symbols properly
* Mon Jan 31 2022 Susant Sahani  <ssahani@vmware.com> 5.3.0-2
- Rebuild with libedit
* Mon Nov 29 2021 Tapas Kundu <tkundu@vmware.com> 5.3.0-1
- Update to 5.3.0
* Thu Jan 14 2021 Alexey Makhalov <amakhalov@vmware.com> 5.1.0-4
- GCC-10 support.
* Wed Sep 30 2020 Dweep Advani <photon-checkins@vmware.com> 5.1.0-3
- Preferring libedit
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 5.1.0-2
- openssl 1.1.1
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 5.1.0-1
- Automatic Version Bump
* Thu Apr 09 2020 Stanislav Paskalev <spaskalev@vmware.com> 5.0.0-1
- Initial build.  First version
