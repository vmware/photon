Summary:        Vendor Package Management for Goland
Name:           glide
Version:        0.13.1
Release:        2%{?dist}
License:        MIT
URL:            https://github.com/Masterminds/glide
Source0:        %{name}-%{version}.tar.gz
%define sha1 glide=c471dbae8556c8594a042b612fe569b3df0a1991
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  git
BuildRequires:  go >= 1.7
BuildRequires:  perl >= 5.28.0

%description
Glide is a tool for managing the vendor directory within a Go package.

%prep
%setup

%build
mkdir -p ${GOPATH}/src/github.com/Masterminds/glide
cp -r * ${GOPATH}/src/github.com/Masterminds/glide/.
pushd ${GOPATH}/src/github.com/Masterminds/glide
make VERSION=%{version} build

%install
pushd ${GOPATH}/src/github.com/Masterminds/glide
make install
install -vdm 755 %{buildroot}%{_bindir}
install -vpm 0755 -t %{buildroot}%{_bindir}/ ./glide

%files
%defattr(-,root,root)
%{_bindir}/glide

%changelog
*   Mon Sep 23 2018 Dweep Advani <dadvani@vmware.com> 0.13.1-2
-   Consuming perl version upgrade of 5.28.0
*   Thu Sep 13 2018 Michelle Wang <michellew@vmware.com> 0.13.1-1
-   Update version to 0.13.1.
*   Mon Aug 14 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.12.3-1
-   glide for PhotonOS.
