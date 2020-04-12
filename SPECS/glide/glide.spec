Summary:        Vendor Package Management for Goland
Name:           glide
Version:        0.13.3
Release:        3%{?dist}
License:        MIT
URL:            https://github.com/Masterminds/glide
Source0:        %{name}-%{version}.tar.gz
%define sha1 glide=64df138d1150b8194d154ec411404b9d4dfeb848
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

%build
mkdir -p ${GOPATH}/src/github.com/Masterminds/glide
cp -r * ${GOPATH}/src/github.com/Masterminds/glide/.
pushd ${GOPATH}/src/github.com/Masterminds/glide
make VERSION=%{version} build
popd

%check
pushd ${GOPATH}/src/github.com/Masterminds/glide
make test
popd

%install
pushd ${GOPATH}/src/github.com/Masterminds/glide
make install
install -vdm 755 %{buildroot}%{_bindir}
install -vpm 0755 -t %{buildroot}%{_bindir}/ ./glide
popd

%files
%defattr(-,root,root)
%{_bindir}/glide

%changelog
*   Fri Apr 10 2020 Harinadh D <hdommaraju@vmware.com> 0.13.3-3
-   Bump up version to compile with go 1.13.3-2
*   Tue Oct 22 2019 Ashwin H <ashwinh@vmware.com> 0.13.3-2
-   Bump up version to compile with go 1.13.3
*   Fri Oct 11 2019 Ashwin H <ashwinh@vmware.com> 0.13.3-1
-   Update to 0.13.3 to build using go 1.13
*   Fri Aug 30 2019 Ashwin H <ashwinh@vmware.com> 0.13.1-5
-   Bump up version to compile with new go
*   Mon Jan 21 2019 Bo Gan <ganb@vmware.com> 0.13.1-4
-   Build using go 1.9.7
*   Fri Nov 23 2018 Ashwin H <ashwinh@vmware.com> 0.13.1-3
-   Fix %check
*   Mon Sep 24 2018 Tapas Kundu <tkundu@vmware.com> 0.13.1-2
-   Build using go version 1.9
*   Thu Sep 13 2018 Michelle Wang <michellew@vmware.com> 0.13.1-1
-   Update version to 0.13.1.
*   Mon Aug 14 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.12.3-1
-   glide for PhotonOS.
