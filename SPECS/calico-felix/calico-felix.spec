Summary:       A per-host daemon for Calico
Name:          calico-felix
Version:       2.6.0
Release:       2%{?dist}
Group:         Applications/System
Vendor:        VMware, Inc.
License:       Apache-2.0
URL:           https://github.com/projectcalico/felix
Source0:       %{name}-%{version}.tar.gz
%define sha1 calico-felix=24f20292c2132e1b912e99a8b6977e2af6cd7b39
Source1:       gogo-protobuf-0.4.tar.gz
%define sha1 gogo-protobuf-0.4=4fc5dda432ad929ce203486c861b7d3e48681150
Source2:       go-27704.patch
Source3:       go-27842.patch
Distribution:  Photon
BuildRequires: git
BuildRequires: glide
BuildRequires: go >= 1.7
BuildRequires: protobuf

%description
A per-host daemon for Calico.

%prep
%setup -q -n felix-%{version}
mkdir -p ${GOPATH}/src/github.com/gogo/protobuf
tar xf %{SOURCE1} --no-same-owner --strip-components 1 -C ${GOPATH}/src/github.com/gogo/protobuf/

%build
pushd ${GOPATH}/src/github.com/gogo/protobuf
make install
popd
mkdir -p /root/.glide
mkdir -p ${GOPATH}/src/github.com/projectcalico/felix
cp -r * ${GOPATH}/src/github.com/projectcalico/felix/.
pushd ${GOPATH}/src/github.com/projectcalico/felix
glide install --strip-vendor
pushd vendor/golang.org/x/net
patch -p1 < %{SOURCE2}
patch -p1 < %{SOURCE3}
popd
mkdir -p bin
cd proto
protoc --plugin=/usr/share/gocode/bin/protoc-gen-gogofaster \
       --gogofaster_out=. felixbackend.proto
cd ..
CGO_ENABLED=0 GOOS=linux go build -v -i -o bin/calico-felix -v \
     -ldflags " -X github.com/projectcalico/felix/buildinfo.GitVersion=<unknown> \
                -X github.com/projectcalico/felix/buildinfo.GitRevision=<unknown>" \
              "github.com/projectcalico/felix"

%install
install -vdm 755 %{buildroot}%{_bindir}
install ${GOPATH}/src/github.com/projectcalico/felix/bin/calico-felix %{buildroot}%{_bindir}/

%files
%defattr(-,root,root)
%{_bindir}/calico-felix

%changelog
*    Mon Jan 28 2019 Bo Gan <ganb@vmware.com> 2.6.0-2
-    Fix CVE-2018-17846 and CVE-2018-17143
*    Fri Nov 03 2017 Vinay Kulkarni <kulkarniv@vmware.com> 2.6.0-1
-    Calico Felix v2.6.0.
*    Tue Sep 12 2017 Vinay Kulkarni <kulkarniv@vmware.com> 2.4.1-2
-    Build protoc-gen-gogofaster plugin from source.
*    Sat Aug 19 2017 Vinay Kulkarni <kulkarniv@vmware.com> 2.4.1-1
-    Calico Felix for PhotonOS.
