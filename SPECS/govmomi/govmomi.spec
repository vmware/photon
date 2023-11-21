Summary:        GO interface to the VMware vSphere API.
Name:           govmomi
Version:        0.29.0
Release:        10%{?dist}
Group:          Development/Languages
License:        Apache License 2.0
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/vmware/govmomi
Source0:        https://github.com/vmware/govmomi/%{name}-%{version}.tar.gz
%define sha512  govmomi=f43cdb8333775689ede39bc2f488433de1a8c6be9cffd534f50023557f5fde3bddc6f2ead88d9f23d0de3a7ed16191bc4daa1e7f31dceb80055feb202c94ab7e
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
* Tue Nov 21 2023 Piyush Gupta <gpiyush@vmware.com> 0.29.0-10
- Bump up version to compile with new go
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 0.29.0-9
- Bump up version to compile with new go
* Mon Sep 18 2023 Piyush Gupta <gpiyush@vmware.com> 0.29.0-8
- Bump up version to compile with new go
* Mon Jul 17 2023 Piyush Gupta <gpiyush@vmware.com> 0.29.0-7
- Bump up version to compile with new go
* Thu Jun 22 2023 Piyush Gupta <gpiyush@vmware.com> 0.29.0-6
- Bump up version to compile with new go
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 0.29.0-5
- Bump up version to compile with new go
* Thu Mar 09 2023 Piyush Gupta <gpiyush@vmware.com> 0.29.0-4
- Bump up version to compile with new go
* Mon Nov 21 2022 Piyush Gupta <gpiyush@vmware.com> 0.29.0-3
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 0.29.0-2
- Bump up version to compile with new go
*   Thu Sep 15 2022 Shivani Agarwal <shivania2@vmware.com> 0.29.0-1
-   Upgrade Version
*   Fri May 13 2022 Shivani Agarwal <shivania2@vmware.com> 0.28.0-1
-   Initial version of govmomi 0.28.0
