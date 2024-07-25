%define srcname repmgr

%define _pg15basedir    %{_usr}/pgsql/15

Summary:        Replication Manager for PostgreSQL Clusters
Name:           repmgr15
Version:        5.3.3
Release:        4%{?dist}
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
* Sun Nov 19 2023 Shreenidhi Shedi <sshedi@vmware.com> 5.3.3-4
- Bump version as a part of openssl upgrade
* Wed Sep 06 2023 Shreenidhi Shedi <sshedi@vmware.com> 5.3.3-3
- repmgr15 for pgsql15
* Fri Apr 14 2023 Shreenidhi Shedi <sshedi@vmware.com> 5.3.3-2
- Bump version as a part of zlib upgrade
* Tue Jan 31 2023 Gerrit Photon <photon-checkins@vmware.com> 5.3.3-1
- Automatic Version Bump
* Fri Jan 20 2023 Shreenidhi Shedi <sshedi@vmware.com> 5.3.2-3
- Remove pgsql-12 dependency
* Thu Jan 05 2023 Shreenidhi Shedi <sshedi@vmware.com> 5.3.2-2
- Bump version as a part of postgresql fixes
* Mon Jul 11 2022 Gerrit Photon <photon-checkins@vmware.com> 5.3.2-1
- Automatic Version Bump
* Sun May 29 2022 Shreenidhi Shedi <sshedi@vmware.com> 5.3.1-2
- Fix binary path
* Tue Apr 19 2022 Gerrit Photon <photon-checkins@vmware.com> 5.3.1-1
- Automatic Version Bump
* Tue Oct 19 2021 Michael Paquier <mpaquier@vmware.com> 5.1.0-5
- Rework dependency list with postgresql
- Add support for autosetup and _smp_mflags
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
