Summary:        Replication Manager for PostgreSQL Clusters
Name:           repmgr
Version:        5.2.1
Release:        3%{?dist}
License:        GNU Public License (GPL) v3
URL:            https://repmgr.org
Group:          Applications/Databases
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://repmgr.org/download/%{name}-%{version}.tar.gz
%define sha512 %{name}=609ca27322087a042ede3a54565e425e9f39d74df510cbc103390cf60a31b35ce311cd942d5efd062bec2026864bd45466dbaf323963060d3ce89ce167c2a0b1

BuildRequires: postgresql10-devel
BuildRequires: readline-devel
BuildRequires: openssl-devel
BuildRequires: zlib-devel
BuildRequires: cpio

Requires: (postgresql10-libs >= 10.5 or postgresql13-libs)
Requires: readline
Requires: openssl
Requires: zlib

%description
repmgr is an open-source tool suite for managing replication and failover in a cluster of PostgreSQL servers.

%prep
%autosetup -p1 -n %{name}-%{version}

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
%{_datadir}/*
%{_libdir}/postgresql/*
%exclude %dir %{_libdir}/debug

%changelog
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
