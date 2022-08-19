Summary:        GO interface to the VMware vSphere API.
Name:           govmomi
Version:        0.28.0
Release:        3%{?dist}
Group:          Development/Languages
License:        Apache License 2.0
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/vmware/govmomi
Source0:        https://github.com/vmware/govmomi/%{name}-%{version}.tar.gz
%define sha512  govmomi=8e475678bfbe68c62f51f1b7fd0804bb4058911d7550f0d91b8caca2cd77293bd659ce55cbeab457b9d92005b126a3a814030304b8e354bee4d37cf59974fb41
BuildRequires:  go
BuildRequires:  which
BuildRequires:  ca-certificates

%description
A Go library for interacting with VMware vSphere APIs (ESXi and/or vCenter). The code in the govmomi package is a wrapper for the code that is generated from the vSphere API description.
It primarily provides convenience functions for working with the vSphere API.

%prep
%autosetup -n %{name}-%{version}

%build
cd ..
mkdir -p build/src/github.com/vmware/%{name}
mkdir -p build/bin
mv %{name}-%{version}/* build/src/github.com/vmware/%{name}
cd build
export GOPATH=`pwd`
cd bin
export GOBIN=`pwd`
export PATH=$PATH:$GOBIN
export GO111MODULE=auto
cd ../src/github.com/vmware/%{name}
go build
cd govc
go build
go install
cd ../vcsim
go build
go install

%install
mkdir -p %{buildroot}%{_bindir}
cp -r ../build/bin/govc %{buildroot}%{_bindir}
cp -r ../build/bin/vcsim  %{buildroot}%{_bindir}

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/govc
%{_bindir}/vcsim

%changelog
* Fri Aug 19 2022 Piyush Gupta <gpiyush@vmware.com> 0.28.0-3
- Bump up version to compile with new go
* Tue Jul 12 2022 Piyush Gupta <gpiyush@vmware.com> 0.28.0-2
- Bump up version to compile with new go
*   Fri May 13 2022 Shivani Agarwal <shivania2@vmware.com> 0.28.0-1
-   Initial version of govmomi 0.28.0.
