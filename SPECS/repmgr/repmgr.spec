Summary:        Replication Manager for PostgreSQL Clusters
Name:           repmgr
Version:        5.3.0
Release:        4%{?dist}
License:        GNU Public License (GPL) v3
URL:            https://repmgr.org
Group:          Applications/Databases
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://repmgr.org/download/%{name}-%{version}.tar.gz
%define sha512 %{name}=1b3c64a9746b7b3f7faf4475750913822b918d415fb0fc19fff5ee8f51c92aeb886d1c6f35b749fc76895b4512ca40c3b5bece57eb012d7d77467c4da72bb8db

BuildRequires:  postgresql14-devel
BuildRequires:  readline-devel
BuildRequires:  openssl-devel
BuildRequires:  zlib-devel
BuildRequires:  cpio
BuildRequires:  libedit-devel

Requires:       (postgresql14-libs or postgresql13-libs or postgresql10-libs)
Requires:       readline
Requires:       openssl
Requires:       zlib
Requires:       libedit

%description
repmgr is an open-source tool suite for managing replication and failover in a cluster of PostgreSQL servers.

%prep
%autosetup -p1

%build
%configure CFLAGS="%{optflags}" CXXFLAGS="%{optflags}"
%make_build

%install
%make_install %{?_smp_mflags}

mkdir -p %{buildroot}%{_usr}

pg_ver="$(pg_config --version | cut -d' ' -f2 | cut -d. -f1)"

pushd %{buildroot}%{_usr}/pgsql/"${pg_ver}"
mv bin share lib %{buildroot}%{_usr}
popd

rmdir %{buildroot}%{_usr}/pgsql/"${pg_ver}" \
      %{buildroot}%{_usr}/pgsql

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/postgresql/*
%exclude %dir %{_libdir}/debug
%{_datadir}/*

%changelog
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
