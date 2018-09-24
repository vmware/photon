Summary:        Vendor Package Management for Goland
Name:           glide
Version:        0.12.3
Release:        2%{?dist}
License:        MIT
URL:            https://github.com/Masterminds/glide
Source0:        %{name}-%{version}.tar.gz
%define sha1 glide=259cfe5a4d598434865c9bb95ed5a98bfd2d8e77
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  git
BuildRequires:  go == 1.9.4
BuildRequires:  perl

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
*   Mon Sep 24 2018 Tapas Kundu <tkundu@vmware.com> 0.12.3-2
-   Build using go version 1.9.4
*   Mon Aug 14 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.12.3-1
-   glide for PhotonOS.
