Summary:       confd is a lightweight configuration management tool
Name:          calico-confd
Version:       0.16.0
Release:       17%{?dist}
Group:         Applications/System
Vendor:        VMware, Inc.
License:       MIT
URL:           https://github.com/kelseyhightower/confd/releases
Source0:       %{name}-%{version}.tar.gz
Distribution:  Photon
BuildRequires: glide
BuildRequires: go
%define sha512  calico-confd=eafabf85d1d7193847a78dcfde7b9961bdf5b634165d27acc760aff6e4ef79cac9688abdfcac049773a28f997f87ea94e6a7606ee7f7d7aaaeaa8ba67f7e48b7

%description
confd is a lightweight configuration management tool that keeps local configuration files up-to-date, and reloading applications to pick up new config file changes.

%prep
%autosetup -n confd-%{version}

%build
export GO111MODULE=auto
#mkdir -p /root/.glide
mkdir -p ${GOPATH}/src/github.com/kelseyhightower/confd
cp -r * ${GOPATH}/src/github.com/kelseyhightower/confd/.
pushd ${GOPATH}/src/github.com/kelseyhightower/confd
%make_build

%install
pushd ${GOPATH}/src/github.com/kelseyhightower/confd
install -vdm 755 %{buildroot}%{_bindir}
install -vpm 0755 -t %{buildroot}%{_bindir}/ bin/confd
eu-elfcompress -q -p -t none %{buildroot}%{_bindir}/*

%files
%defattr(-,root,root)
%{_bindir}/confd

%changelog
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 0.16.0-17
- Bump up version to compile with new go
* Tue Apr 04 2023 Piyush Gupta <gpiyush@vmware.com> 0.16.0-16
- Bump up version to compile with new go
* Tue Dec 20 2022 Piyush Gupta <gpiyush@vmware.com> 0.16.0-15
- Bump up version to compile with new go
* Sun Nov 13 2022 Piyush Gupta <gpiyush@vmware.com> 0.16.0-14
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 0.16.0-13
- Bump up version to compile with new go
* Thu Sep 15 2022 Piyush Gupta <gpiyush@vmware.com> 0.16.0-12
- Bump up version to compile with new go
* Thu Aug 18 2022 Piyush Gupta <gpiyush@vmware.com> 0.16.0-11
- Bump up version to compile with new go
* Mon May 09 2022 Piyush Gupta <gpiyush@vmware.com> 0.16.0-10
- Bump up version to compile with new go
* Wed Mar 16 2022 Piyush Gupta <gpiyush@vmware.com> 0.16.0-9
- Bump up version to compile with new go
* Tue Feb 22 2022 Piyush Gupta <gpiyush@vmware.com> 0.16.0-8
- Bump up version to compile with new go
* Mon Jan 24 2022 Piyush Gupta <gpiyush@vmware.com> 0.16.0-7
- Bump up version to compile with new go
* Tue Nov 16 2021 Piyush Gupta <gpiyush@vmware.com> 0.16.0-6
- Bump up version to compile with new go
* Wed Oct 20 2021 Piyush Gupta <gpiyush@vmware.com> 0.16.0-5
- Bump up version to compile with new go
* Sat Aug 21 2021 Piyush Gupta<gpiyush@vmware.com> 0.16.0-4
- Bump up version to compile with new go
* Tue Jun 29 2021 Piyush Gupta <gpiyush@vmware.com> 0.16.0-3
- Bump up version to compile with new go
* Wed Jun 02 2021 Piyush Gupta<gpiyush@vmware.com> 0.16.0-2
- Bump up version to compile with new go
* Tue May 25 2021 Prashant S Chauhan <psinghchauha@vmware.com> 0.16.0-1
- Update to version 0.16.0
* Mon Feb 08 2021 Harinadh D <hdommaraju@vmware.com> 0.14.0-9
- Bump up version to compile with new go
* Fri Nov 27 2020 HarinadhD <hdommaraju@vmware.com> 0.14.0-8
- Bump up version to compile with new go
* Fri Apr 10 2020 Harinadh D <hdommaraju@vmware.com> 0.14.0-7
- Bump up version to compile with go 1.13.3-2
* Tue Oct 22 2019 Ashwin H <ashwinh@vmware.com> 0.14.0-6
- Bump up version to compile with go 1.13.3
* Fri Oct 11 2019 Ashwin H <ashwinh@vmware.com> 0.14.0-5
- Build with go 1.13
* Fri Aug 30 2019 Ashwin H <ashwinh@vmware.com> 0.14.0-4
- Bump up version to compile with new go
* Mon Jan 21 2019 Bo Gan <ganb@vmware.com> 0.14.0-3
- Build using go 1.9.7
* Mon Sep 24 2018 Tapas Kundu <tkundu@vmware.com> 0.14.0-2
- Build using go version 1.9
* Fri Nov 03 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.14.0-1
- Calico confd v0.14.0
* Fri Aug 18 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.12.0-1
- Calico confd for PhotonOS.
