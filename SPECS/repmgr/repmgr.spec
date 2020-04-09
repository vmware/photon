Summary:        Replication Manager for PostgreSQL Clusters
Name:           repmgr
Version:        5.0.0
Release:        1%{?dist}
License:        GNU Public License (GPL) v3
URL:            https://repmgr.org/
Group:          Applications/Databases
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://repmgr.org/download/%{name}-%{version}.tar.gz
%define sha1    repmgr=f0ae71c4f0a75fa2545661f9565b2b0c59a91357
BuildRequires:  postgresql-devel readline-devel openssl-devel zlib-devel cpio
Requires:       postgresql-libs readline openssl zlib

%description
repmgr is an open-source tool suite for managing replication and failover in a cluster of PostgreSQL servers.

%prep
%setup

%build
%configure CFLAGS="%{optflags}" CXXFLAGS="%{optflags}"
make

%install
make install DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*
%exclude %{_libdir}/debug/
%{_datadir}/*

%changelog
*   Thu Apr 09 2020 Stanislav Paskalev <spaskalev@vmware.com> 5.0.0-1
-   Initial build.  First version
