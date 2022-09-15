Summary:        confd is a lightweight configuration management tool
Name:           confd
Version:        3.6
Release:        18%{?dist}
License:        Apache-2.0
URL:            https://github.com/projectcalico/confd
Source0:        %{name}-%{version}.tar.gz
%define sha512  confd=19a580a0bdd834d966f956b25e281e37710596def2d3973f45a215017e5e71ebc8b0c6ae1d53bca768998d2a91795f25c3eb4dfc7a4c1f227ad2fdfdffc89266
Source1:         go-27704.patch
Source2:         go-27842.patch
Obsoletes:       calico-confd
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  git
BuildRequires:  glide
BuildRequires:  go >= 1.11
BuildRequires:  make

%description
This is a Calico-specific version of confd. It is heavily modified from the original and only supports a single backend type - namely a Calico datastore. It has a single purpose which is to monitor Calico BGP configuration and to autogenerate bird BGP templates from that config.

%prep
%autosetup

%build
export GO111MODULE=auto
mkdir -p /root/.glide
#projectcalico version of confd is forked from kelseyhightower.
#Code still uses kelseyhightower in package naming in src files.
mkdir -p ${GOPATH}/src/github.com/kelseyhightower/confd
cp -r * ${GOPATH}/src/github.com/kelseyhightower/confd
pushd ${GOPATH}/src/github.com/kelseyhightower/confd
glide install --strip-vendor
pushd vendor/golang.org/x/net
patch -p1 < %{SOURCE1}
patch -p1 < %{SOURCE2}
popd
mkdir -p dist
mkdir -p .go-pkg-cache
CGO_ENABLED=0 go build -v -i -o dist/confd github.com/kelseyhightower/confd
popd

%install
pushd ${GOPATH}/src/github.com/kelseyhightower
install -vdm 755 %{buildroot}%{_bindir}
install confd/dist/confd %{buildroot}%{_bindir}/
cp -r confd/etc/ %{buildroot}%{_sysconfdir}

%files
%defattr(-,root,root)
%{_bindir}/confd
%config(noreplace) %{_sysconfdir}/calico

%changelog
* Thu Sep 15 2022 Piyush Gupta <gpiyush@vmware.com> 3.6-18
- Bump up version to compile with new go
* Thu Aug 18 2022 Piyush Gupta <gpiyush@vmware.com> 3.6-17
- Bump up version to compile with new go
* Mon May 09 2022 Piyush Gupta <gpiyush@vmware.com> 3.6-16
- Bump up version to compile with new go
* Wed Mar 16 2022 Piyush Gupta <gpiyush@vmware.com> 3.6-15
- Bump up version to compile with new go
* Tue Feb 22 2022 Piyush Gupta <gpiyush@vmware.com> 3.6-14
- Bump up version to compile with new go
* Mon Jan 24 2022 Piyush Gupta <gpiyush@vmware.com> 3.6-13
- Bump up version to compile with new go
* Tue Nov 16 2021 Piyush Gupta <gpiyush@vmware.com> 3.6-12
- Bump up version to compile with new go
* Wed Oct 20 2021 Piyush Gupta <gpiyush@vmware.com> 3.6-11
- Bump up version to compile with new go
* Sat Aug 21 2021 Piyush Gupta<gpiyush@vmware.com> 3.6-10
- Bump up version to compile with new go
* Tue Jun 29 2021 Piyush Gupta <gpiyush@vmware.com> 3.6-9
- Bump up version to compile with new go
* Mon May 03 2021 Piyush Gupta<gpiyush@vmware.com> 3.6-8
- Bump up version to compile with new go
* Mon Feb 08 2021 Harinadh D <hdommaraju@vmware.com> 3.6-7
- Bump up version to compile with new go
* Fri Nov 27 2020 HarinadhD <hdommaraju@vmware.com> 3.6-6
- Bump up version to compile with new go
* Tue Aug 18 2020 Ashwin H <ashwinh@vmware.com> 3.6-5
- Bump up version to compile with new go
* Fri Apr 10 2020 Harinadh D <hdommaraju@vmware.com> 3.6-4
- Bump up version to compile with go 1.13.3-2
* Tue Oct 22 2019 Ashwin H <ashwinh@vmware.com> 3.6-3
- Bump up version to compile with go 1.13.3
* Fri Aug 30 2019 Ashwin H <ashwinh@vmware.com> 3.6-2
- Bump up version to compile with new go
* Fri Aug 16 2019 Ashwin H <ashwinh@vmware.com> 3.6-1
- project calico-confd initial version
