%define gopath_comp_glide github.com/Masterminds/glide

Summary:        Vendor Package Management for Goland
Name:           glide
Version:        0.13.3
Release:        21%{?dist}
URL:            https://github.com/Masterminds/glide
Source0:        https://github.com/Masterminds/glide/archive/refs/tags/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  git
BuildRequires:  go
BuildRequires:  perl

%description
Glide is a tool for managing the vendor directory within a Go package.

%prep
# Using autosetup is not feasible
%setup -q -c -n glide-%{version}

mkdir -p "$(dirname src/%{gopath_comp_glide})"
mv glide-%{version} src/%{gopath_comp_glide}

%build
export GOPATH="${PWD}"
export GO111MODULE=auto
export GOFLAGS=-mod=vendor
pushd src/%{gopath_comp_glide}
make VERSION=%{version} build %{?_smp_mflags}
popd

%check
export GOPATH="${PWD}"
export GO111MODULE=auto
export GOFLAGS=-mod=vendor
pushd src/%{gopath_comp_glide}
make test %{?_smp_mflags}
popd

%install
export GOPATH="${PWD}"
export GO111MODULE=auto
export GOFLAGS=-mod=vendor
pushd src/%{gopath_comp_glide}
make install %{?_smp_mflags}
install -vdm 755 %{buildroot}%{_bindir}
install -vpm 0755 -t %{buildroot}%{_bindir}/ ./glide
popd

%files
%defattr(-,root,root)
%{_bindir}/glide

%changelog
* Wed Dec 11 2024 Tapas Kundu <tapas.kundu@broadcom.com> 0.13.3-21
- Release bump for SRP compliance
* Thu Sep 19 2024 Mukul Sikka <mukul.sikka@broadcom.com> 0.13.3-20
- Bump version as a part of go upgrade
* Thu Aug 22 2024 Bo Gan <bo.gan@broadcom.com> 0.13.3-19
- Fix build script
* Fri Jul 12 2024 Mukul Sikka <mukul.sikka@broadcom.com> 0.13.3-18
- Bump version as a part of go upgrade
* Thu Jun 20 2024 Mukul Sikka <msikka@vmware.com> 0.13.3-17
- Bump version as a part of go upgrade
* Thu Feb 22 2024 Mukul Sikka <msikka@vmware.com> 0.13.3-16
- Bump version as a part of go upgrade
* Tue Nov 21 2023 Piyush Gupta <gpiyush@vmware.com> 0.13.3-15
- Bump up version to compile with new go
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 0.13.3-14
- Bump up version to compile with new go
* Mon Sep 18 2023 Piyush Gupta <gpiyush@vmware.com> 0.13.3-13
- Bump up version to compile with new go
* Mon Jul 17 2023 Piyush Gupta <gpiyush@vmware.com> 0.13.3-12
- Bump up version to compile with new go
* Thu Jun 22 2023 Piyush Gupta <gpiyush@vmware.com> 0.13.3-11
- Bump up version to compile with new go
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 0.13.3-10
- Bump up version to compile with new go
* Thu Mar 09 2023 Piyush Gupta <gpiyush@vmware.com> 0.13.3-9
- Bump up version to compile with new go
* Mon Nov 21 2022 Piyush Gupta <gpiyush@vmware.com> 0.13.3-8
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 0.13.3-7
- Bump up version to compile with new go
*   Fri Jun 17 2022 Piyush Gupta <gpiyush@vmware.com> 0.13.3-6
-   Bump up version to compile with new go
*   Fri Jun 11 2021 Piyush Gupta<gpiyush@vmware.com> 0.13.3-5
-   Bump up version to compile with new go
*   Fri Feb 05 2021 Harinadh D <hdommaraju@vmware.com> 0.13.3-4
-   Bump up version to compile with new go
*   Fri Jan 15 2021 Piyush Gupta<gpiyush@vmware.com> 0.13.3-3
-   Bump up version to compile with new go
*   Tue Oct 06 2020 Ashwin H <ashwinh@vmware.com> 0.13.3-2
-   Build using go 1.14
*   Tue Jun 30 2020 Gerrit Photon <photon-checkins@vmware.com> 0.13.3-1
-   Automatic Version Bump
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
