Summary:        Vendor Package Management for Goland
Name:           glide
Version:        0.13.3
Release:        1%{?dist}
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
*   Tue Aug 18 2020 Ashwin H <ashwinh@vmware.com> 0.13.3-1
-   Update to work with go 1.13
*   Fri Apr 10 2020 Harinadh D <hdommaraju@vmware.com> 0.12.3-6
-   Bump up version to compile with go 1.13.5-2
*   Tue Jan 07 2020 Ashwin H <ashwinh@vmware.com> 0.12.3-5
-   Bump up version to compile with new go
*   Fri Aug 30 2019 Ashwin H <ashwinh@vmware.com> 0.12.3-4
-   Bump up version to compile with new go
*   Wed Aug 14 2019 Harinadh Dommaraju <hdommaraju@vmware.com> 0.12.3-3
-   Version bump to build using go version 1.9.4-6
*   Mon Aug 06 2018 Dheeraj Shetty <dheerajs@vmware.com> 0.12.3-2
-   Build using go version 1.9.4
*   Mon Aug 14 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.12.3-1
-   glide for PhotonOS.
