Summary:	A Distributed init System
Name:		fleet
Version:	0.11.5
Release:	1%{?dist}
License:	Apache 2.0
URL:		https://coreos.com/using-coreos/clustering/
Group:		OS/ClusterManagement
BuildRequires:	go
Vendor:		VMware, Inc.
Distribution: Photon
Source0:	https://github.com/coreos/%{name}/archive/%{name}-%{version}.tar.gz
%define sha1 fleet=df90c76e7c6458a05a77078993d9bd705a25b8c5
%description
fleet ties together systemd and etcd into a simple distributed init system.

%prep
%setup -q


%build
./build

%install
mkdir -p %{buildroot}%{_bindir}
cp bin/* %{buildroot}%{_bindir}

%files
%defattr(-,root,root)
%{_bindir}/*

%changelog
*       Wed Feb 24 2016 Kumar Kaushik <kaushikk@vmware.com> 0.11.5-1
-       Updated version.
*	Mon Jul 13 2015 Danut Moraru <dmoraru@vmware.com> 0.11.1-1
-	Initial build.

