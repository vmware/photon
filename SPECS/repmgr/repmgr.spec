Summary:        Replication Manager for PostgreSQL Clusters
Name:           repmgr
Version:        5.3.0
Release:        2%{?dist}
License:        GNU Public License (GPL) v3
URL:            https://repmgr.org/
Group:          Applications/Databases
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://repmgr.org/download/%{name}-%{version}.tar.gz
%define sha1    repmgr=2c233183daaf766353312d1693e394d1c1753dd9
BuildRequires:  postgresql-devel readline-devel openssl-devel zlib-devel cpio libedit-devel
Requires:       postgresql-libs readline openssl zlib libedit

%description
repmgr is an open-source tool suite for managing replication and failover in a cluster of PostgreSQL servers.

%prep
%autosetup

%build
%configure CFLAGS="%{optflags}" CXXFLAGS="%{optflags}"
make %{_smp_mflags} CFLAGS="-O2 -g -fcommon"

%install
make install DESTDIR=%{buildroot} %{_smp_mflags}

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*
%exclude %{_libdir}/debug/
%{_datadir}/*

%changelog
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
