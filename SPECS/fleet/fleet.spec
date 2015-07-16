Summary:	A Distributed init System
Name:		fleet
Version:	0.11.1
Release:	1%{?dist}
License:	Apache 2.0
URL:		https://coreos.com/using-coreos/clustering/
Group:		OS/ClusterManagement
BuildRequires:	go
Vendor:		VMware, Inc.
Distribution: Photon
Source0:	https://github.com/coreos/%{name}/archive/%{name}-%{version}.tar.gz
%define sha1 fleet=2de21c48f918c7611564f5960858ad3f53b8f58d
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
*	Mon Jul 13 2015 Danut Moraru <dmoraru@vmware.com> 0.11.1-1
-	Initial build.

