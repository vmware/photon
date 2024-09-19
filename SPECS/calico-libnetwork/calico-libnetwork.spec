%define debug_package   %{nil}
%define gopath_comp_libnetwork_plugin github.com/projectcalico/libnetwork-plugin
# if you are fetching glide dependencies freshly, set this to 1
# for dev purpose only
%define refetch_deps    0

Summary:       Docker libnetwork plugin for Calico
Name:          calico-libnetwork
Version:       1.1.3
Release:       22%{?dist}
Group:         Applications/System
Vendor:        VMware, Inc.
License:       Apache-2.0
Distribution:  Photon
URL:           https://github.com/projectcalico/libnetwork-plugin

Source0: https://github.com/projectcalico/libnetwork-plugin/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512 %{name}=40b7b0962e58fced7a02fa743b0f92aae2c6d1e43046cd0d59153f4022ad22ca0b29ac3a9cbc6e67218a35dce3306a1a88194d22248a2f589ee385d0c1ce3852

# Be aware that the source tarball has a different prefix as the package name: libnetwork-plugin vs. calico-libnetwork, thus use libnetwork-plugin-%{version} as prefix
# Created by `glide install --strip-vendor && tar --owner=root --group=root --mtime='2000-01-01 00:00Z' --transform "s,^,libnetwork-plugin-${version}/," -c vendor | gzip -9`
Source1: glide-vendor-for-%{name}-%{version}.tar.gz
%define sha512 glide-vendor-for-%{name}=164866f261519403a420bf2746e5d34fbdf5be61c0141ddf9e9959e86ba93dc1b941210f4e8d9769f453da0dee8de082770e93bc05b2778dae80965eef8cee46

BuildRequires: git
BuildRequires: glide
BuildRequires: go

%description
Docker libnetwork plugin for Calico.

%prep
# Using autosetup is not feasible
%setup -q -c -n libnetwork-plugin-%{version}

# If not fetching dependencies, populate the vendor/ directory ourselves
%if 0%{?refetch_deps} == 0
tar -xf %{SOURCE1}
%endif

mkdir -p "$(dirname src/%{gopath_comp_libnetwork_plugin})"
mv libnetwork-plugin-%{version} src/%{gopath_comp_libnetwork_plugin}

# If fetching deoendencies, use `glide install -strip-vendor` the same as in Makefile
%if 0%{?refetch_deps}
export GOPATH="${PWD}"
pushd src/%{gopath_comp_libnetwork_plugin}
glide install --strip-vendor
popd
%endif

%build
export GO111MODULE=auto
export GOPATH="${PWD}"

pushd src/%{gopath_comp_libnetwork_plugin}
CGO_ENABLED=0 go build -v -o dist/libnetwork-plugin -ldflags "-X main.VERSION=%{version} -s -w" main.go
popd

%install
pushd src/%{gopath_comp_libnetwork_plugin}
install -vdm 0755 %{buildroot}%{_datadir}/calico/docker
install -vpm 0755 -t %{buildroot}%{_datadir}/calico/docker/ dist/libnetwork-plugin
popd

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_datadir}/calico/docker/libnetwork-plugin

%changelog
* Thu Sep 19 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.1.3-22
- Bump version as a part of go upgrade
* Fri Aug 23 2024 Bo Gan <bo.gan@broadcom.com> 1.1.3-21
- Simplify build scripts
* Mon Jul 29 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.1.3-20
- Changes to help building offline
* Fri Jul 12 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.1.3-19
- Bump version as a part of go upgrade
* Thu Jun 20 2024 Mukul Sikka <msikka@vmware.com> 1.1.3-18
- Bump version as a part of go upgrade
* Thu Feb 22 2024 Mukul Sikka <msikka@vmware.com> 1.1.3-17
- Bump version as a part of go upgrade
* Sat Dec 16 2023 Mukul Sikka <msikka@vmware.com> 1.1.3-16
- Bump up version to compile with new go
* Fri Dec 15 2023 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 1.1.3-15
- Use latest glide cache
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 1.1.3-14
- Bump up version to compile with new go
* Mon Sep 18 2023 Piyush Gupta <gpiyush@vmware.com> 1.1.3-13
- Bump up version to compile with new go
* Mon Jul 17 2023 Piyush Gupta <gpiyush@vmware.com> 1.1.3-12
- Bump up version to compile with new go
* Thu Jun 22 2023 Piyush Gupta <gpiyush@vmware.com> 1.1.3-11
- Bump up version to compile with new go
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 1.1.3-10
- Bump up version to compile with new go
* Thu Mar 09 2023 Piyush Gupta <gpiyush@vmware.com> 1.1.3-9
- Bump up version to compile with new go
* Mon Nov 21 2022 Piyush Gupta <gpiyush@vmware.com> 1.1.3-8
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 1.1.3-7
- Bump up version to compile with new go
* Fri Jun 17 2022 Piyush Gupta <gpiyush@vmware.com> 1.1.3-6
- Bump up version to compile with new go
* Fri Jun 11 2021 Piyush Gupta<gpiyush@vmware.com> 1.1.3-5
- Bump up version to compile with new go
* Fri Feb 05 2021 Harinadh D <hdommaraju@vmware.com> 1.1.3-4
- Bump up version to compile with new go
* Fri Jan 15 2021 Piyush Gupta<gpiyush@vmware.com> 1.1.3-3
- Bump up version to compile with new go
* Mon Jan 11 2021 Shreenidhi Shedi <sshedi@vmware.com> 1.1.3-2
- Pass `--force` option to glide install to fix build error
* Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 1.1.3-1
- Automatic Version Bump
* Wed Jun 17 2020 Ashwin H <ashwinh@vmware.com> 1.1.0-5
- Fix dependency for cloud.google.com-go
* Tue Jun 09 2020 Ashwin H <ashwinh@vmware.com> 1.1.0-4
- Use cache for dependencies
* Mon Jan 21 2019 Bo Gan <ganb@vmware.com> 1.1.0-3
- Build using go 1.9.7
* Mon Sep 24 2018 Tapas Kundu <tkundu@vmware.com> 1.1.0-2
- Build using go version 1.9
* Fri Aug 18 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.1.0-1
- Calico libnetwork plugin for PhotonOS.
