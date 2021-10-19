Summary:        Replication Manager for PostgreSQL Clusters
Name:           repmgr
Version:        5.1.0
Release:        5%{?dist}
License:        GNU Public License (GPL) v3
URL:            https://repmgr.org/
Group:          Applications/Databases
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://repmgr.org/download/%{name}-%{version}.tar.gz
%define sha1    repmgr=5859789e71f93c1315b9520e197b92fe60693418
BuildRequires:  postgresql-devel cpio
Requires:       postgresql-libs

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
*   Tue Oct 19 2021 Michael Paquier <mpaquier@vmware.com> 5.1.0-5
-   Rework dependency list with postgresql
-   Add support for autosetup and _smp_mflags
*   Thu Jan 14 2021 Alexey Makhalov <amakhalov@vmware.com> 5.1.0-4
-   GCC-10 support.
*   Wed Sep 30 2020 Dweep Advani <photon-checkins@vmware.com> 5.1.0-3
-   Preferring libedit
*   Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 5.1.0-2
-   openssl 1.1.1
*   Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 5.1.0-1
-   Automatic Version Bump
*   Thu Apr 09 2020 Stanislav Paskalev <spaskalev@vmware.com> 5.0.0-1
-   Initial build.  First version
