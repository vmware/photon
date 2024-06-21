Summary:        Vendor Package Management for Goland
Name:           glide
Version:        0.13.3
Release:        25%{?dist}
License:        MIT
URL:            https://github.com/Masterminds/glide
Source0:        %{name}-%{version}.tar.gz
%define sha512  glide=bb0cf1308a9ac0768db647552131867eaccbd8c449e10fb8c8f0fa41f0cca67983b15689ad307c5299a9a125a6a7bfea19fae39525eaf407c92d893918577945
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  git
BuildRequires:  go
BuildRequires:  perl

%description
Glide is a tool for managing the vendor directory within a Go package.

%prep
%autosetup

%build
mkdir -p ${GOPATH}/src/github.com/Masterminds/glide
cp -r * ${GOPATH}/src/github.com/Masterminds/glide/.
pushd ${GOPATH}/src/github.com/Masterminds/glide
go env -w GO111MODULE=auto
make VERSION=%{version} build %{?_smp_mflags}
popd

%check
pushd ${GOPATH}/src/github.com/Masterminds/glide
make test %{?_smp_mflags}
popd

%install
pushd ${GOPATH}/src/github.com/Masterminds/glide
make install %{?_smp_mflags}
install -vdm 755 %{buildroot}%{_bindir}
install -vpm 0755 -t %{buildroot}%{_bindir}/ ./glide
popd

%files
%defattr(-,root,root)
%{_bindir}/glide

%changelog
* Thu Jun 20 2024 Mukul Sikka <msikka@vmware.com> 0.13.3-25
- Bump version as a part of go upgrade
* Thu Apr 18 2024 Mukul Sikka <msikka@vmware.com> 0.13.3-24
- Bump version as a part of go upgrade
* Tue Nov 21 2023 Piyush Gupta <gpiyush@vmware.com> 0.13.3-23
- Bump up version to compile with new go
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 0.13.3-22
- Bump up version to compile with new go
* Fri Aug 18 2023 Piyush Gupta <gpiyush@vmware.com> 0.13.3-21
- Bump up version to compile with new go
* Tue Jun 20 2023 Piyush Gupta <gpiyush@vmware.com> 0.13.3-20
- Bump up version to compile with new go
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 0.13.3-19
- Bump up version to compile with new go
* Thu Mar 16 2023 Piyush Gupta <gpiyush@vmware.com> 0.13.3-18
- Bump up version to compile with new go
* Tue Dec 20 2022 Piyush Gupta <gpiyush@vmware.com> 0.13.3-17
- Bump up version to compile with new go
* Sun Nov 13 2022 Piyush Gupta <gpiyush@vmware.com> 0.13.3-16
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 0.13.3-15
- Bump up version to compile with new go
* Thu Sep 15 2022 Piyush Gupta <gpiyush@vmware.com> 0.13.3-14
- Bump up version to compile with new go
* Fri Aug 19 2022 Piyush Gupta <gpiyush@vmware.com> 0.13.3-13
- Bump up version to compile with new go
* Tue Jul 12 2022 Piyush Gupta <gpiyush@vmware.com> 0.13.3-12
- Bump up version to compile with new go
*   Sat May 07 2022 Piyush Gupta <gpiyush@vmware.com> 0.13.3-11
-   Bump up version to compile with new go
*   Tue Feb 22 2022 Piyush Gupta <gpiyush@vmware.com> 0.13.3-10
-   Bump up version to compile with new go
*   Mon Jan 24 2022 Piyush Gupta <gpiyush@vmware.com> 0.13.3-9
-   Bump up version to compile with new go
*   Wed Oct 20 2021 Piyush Gupta <gpiyush@vmware.com> 0.13.3-8
-   Bump up version to compile with new go
*   Tue Oct 05 2021 Piyush Gupta <gpiyush@vmware.com> 0.13.3-7
-   Bump up version to compile with new go
*   Fri Jun 11 2021 Piyush Gupta <gpiyush@vmware.com> 0.13.3-6
-   Bump up version to compile with new go
*   Thu Mar 25 2021 Piyush Gupta<gpiyush@vmware.com> 0.13.3-5
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
