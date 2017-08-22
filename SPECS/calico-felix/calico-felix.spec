Summary:       A per-host daemon for Calico
Name:          calico-felix
Version:       2.4.1
Release:       1%{?dist}
Group:         Applications/System
Vendor:        VMware, Inc.
License:       Apache-2.0
URL:           https://github.com/projectcalico/felix
Source0:       %{name}-%{version}.tar.gz
Distribution:  Photon
BuildRequires: git
BuildRequires: glide
BuildRequires: go >= 1.7
BuildRequires: protobuf
BuildRequires: which
%define sha1 calico-felix=4408e0b30fee66d8813bf0351094f4b4af7d6813

%description
A per-host daemon for Calico.

%prep
%setup -q -n felix-%{version}

%build
mkdir -p /root/.glide
mkdir -p ${GOPATH}/src/github.com/projectcalico/felix
cp -r * ${GOPATH}/src/github.com/projectcalico/felix/.
pushd ${GOPATH}/src/github.com/projectcalico/felix
go get -u github.com/onsi/ginkgo/ginkgo
go get -u github.com/gogo/protobuf/protoc-gen-gogofaster
go install github.com/gogo/protobuf/protoc-gen-gogofaster
glide install --strip-vendor
mkdir -p bin
cd proto
protoc --plugin=/usr/share/gocode/bin/protoc-gen-gogofaster \
       --gogofaster_out=. felixbackend.proto
cd ..
CGO_ENABLED=0 GOOS=linux go build -v -i -o bin/calico-felix -v \
     -ldflags " -X github.com/projectcalico/felix/buildinfo.GitVersion=<unknown> \
                -X github.com/projectcalico/felix/buildinfo.GitRevision=<unknown>" \
              "github.com/projectcalico/felix"
ldd bin/calico-felix 2>&1 | grep -q "not a dynamic executable" || \
    ( echo "Error: bin/calico-felix was not statically linked"; false )

%install
install -vdm 755 %{buildroot}%{_bindir}
install ${GOPATH}/src/github.com/projectcalico/felix/bin/calico-felix %{buildroot}%{_bindir}/

%files
%defattr(-,root,root)
%{_bindir}/calico-felix

%changelog
*    Sat Aug 19 2017 Vinay Kulkarni <kulkarniv@vmware.com> 2.4.1-1
-    Calico Felix for PhotonOS.
