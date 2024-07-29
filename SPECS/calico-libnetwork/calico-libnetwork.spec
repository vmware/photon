%define debug_package   %{nil}
%define src_path        "${GOPATH}/src/github.com/projectcalico/libnetwork-plugin"
# if you are fetching glide dependencies freshly, set this to 1
# for dev purpose only
%define refetch_deps    0

Summary:       Docker libnetwork plugin for Calico
Name:          calico-libnetwork
Version:       1.1.3
Release:       16%{?dist}
Group:         Applications/System
Vendor:        VMware, Inc.
License:       Apache-2.0
Distribution:  Photon
URL:           https://github.com/projectcalico/libnetwork-plugin

Source0: https://github.com/projectcalico/libnetwork-plugin/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512 %{name}=40b7b0962e58fced7a02fa743b0f92aae2c6d1e43046cd0d59153f4022ad22ca0b29ac3a9cbc6e67218a35dce3306a1a88194d22248a2f589ee385d0c1ce3852

Source1: glide-cache-for-calico-libnetwork-%{version}-15.tar.xz
%define sha512 glide-cache-for-%{name}=9e8bc36c77f939e4c8a87e3461e0de8e9fe6b59235109f627b743b9c7317a1cf79d1b7fd41f6c89b8edb116d94912e658b3689a95bd14149487350f91bd919c4

BuildRequires: git
BuildRequires: glide
BuildRequires: go

%description
Docker libnetwork plugin for Calico.

%prep
%autosetup -p1 -n libnetwork-plugin-%{version}

%build
export GO111MODULE=auto

glide_cache_dir="${HOME}/.glide"
mkdir -p ${glide_cache_dir} %{src_path}/dist
tar -C ${glide_cache_dir} -xf %{SOURCE1}
%if 0%{?refetch_deps}
pushd ${glide_cache_dir}/cache/src
ln -srv https-cloud.google.com-go https-code.googlesource.com-gocloud
popd
%endif

cp -a * %{src_path}
pushd %{src_path}
%if 0%{?refetch_deps}
glide mirror set https://cloud.google.com/go https://code.googlesource.com/gocloud
%endif
# glide install checks ~/.glide dir before downloading from the web.
glide install --force --strip-vendor

CGO_ENABLED=0 go build -v -o dist/libnetwork-plugin -ldflags "-X main.VERSION=%{version} -s -w" main.go
popd

%install
pushd %{src_path}
install -vdm 0755 %{buildroot}%{_datadir}/calico/docker
install -vpm 0755 -t %{buildroot}%{_datadir}/calico/docker/ dist/libnetwork-plugin
popd

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_datadir}/calico/docker/libnetwork-plugin

%changelog
* Mon Jul 29 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.1.3-16
- Changes to help building offline
* Tue Nov 21 2023 Piyush Gupta <gpiyush@vmware.com> 1.1.3-15
- Bump up version to compile with new go
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 1.1.3-14
- Bump up version to compile with new go
* Mon Sep 18 2023 Piyush Gupta <gpiyush@vmware.com> 1.1.3-13
- Bump up version to compile with new go
* Mon Jul 17 2023 Piyush Gupta <gpiyush@vmware.com> 1.1.3-12
- Bump up version to compile with new go
* Mon Jul 03 2023 Piyush Gupta <gpiyush@vmware.com> 1.1.3-11
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
