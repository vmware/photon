Summary:        Vendor Package Management for Goland
Name:           glide
Version:        0.13.2
Release:        2%{?dist}
License:        MIT
URL:            https://github.com/Masterminds/glide
Source0:        %{name}-%{version}.tar.gz
%define sha1 glide=a9cf64c17ee5d3ae201e4ea15fec8b79b7c1d52c
Patch0:         glide_nil_check.patch
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  git
BuildRequires:  go
BuildRequires:  perl

%description
Glide is a tool for managing the vendor directory within a Go package.

%prep
%setup
%patch0 -p1

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
*   Fri Aug 30 2019 Ashwin H <ashwinh@vmware.com> 0.13.2-2
-   Bump up version to compile with new go
*   Thu May 09 2019 Ashwin H <ashwinh@vmware.com> 0.13.2-1
-   Update to 0.13.2-1 to work with go 1.11
*   Thu Oct 12 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.12.3-1
-   glide for PhotonOS.
