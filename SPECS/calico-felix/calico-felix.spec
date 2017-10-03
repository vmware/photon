Summary:       A per-host daemon for Calico
Name:          calico-felix
Version:       2.4.1
Release:       3%{?dist}
Group:         Applications/System
Vendor:        VMware, Inc.
License:       Apache-2.0
URL:           https://github.com/projectcalico/felix
Source0:       %{name}-%{version}.tar.gz
%define sha1 calico-felix=4408e0b30fee66d8813bf0351094f4b4af7d6813
Source1:       gogo-protobuf-0.4.tar.gz
%define sha1 gogo-protobuf-0.4=4fc5dda432ad929ce203486c861b7d3e48681150
Distribution:  Photon
BuildRequires: git
BuildRequires: glide
BuildRequires: go >= 1.7
BuildRequires: protobuf

%description
A per-host daemon for Calico.

%prep
%setup -q -T -D -b 1 -n protobuf-0.4
%setup -q -n felix-%{version}

%build
export GOPATH="$(pwd)"
cd ..
mv "${GOPATH}" felix
mkdir -p "${GOPATH}/src/github.com/projectcalico"
mv felix "${GOPATH}/src/github.com/projectcalico/"
mkdir -p "${GOPATH}/src/github.com/gogo"
mv protobuf-0.4 "${GOPATH}/src/github.com/gogo/protobuf/"

pushd "${GOPATH}/src/github.com/gogo/protobuf"
make install
popd

mkdir -p /root/.glide
cd "${GOPATH}/src/github.com/projectcalico/felix"
glide install --strip-vendor
mkdir -p bin

cd proto
protoc "--plugin=${GOPATH}/bin/protoc-gen-gogofaster" \
       --gogofaster_out=. felixbackend.proto
cd ..
CGO_ENABLED=0 GOOS=linux go build -v -i -o bin/calico-felix -v \
     -ldflags " -X github.com/projectcalico/felix/buildinfo.GitVersion=<unknown> \
                -X github.com/projectcalico/felix/buildinfo.GitRevision=<unknown>" \
              "github.com/projectcalico/felix"

%install
install -vdm 755 %{buildroot}%{_bindir}
install src/github.com/projectcalico/felix/bin/calico-felix %{buildroot}%{_bindir}/

%files
%defattr(-,root,root)
%{_bindir}/calico-felix

%changelog
*    Thu Oct 12 2017 Bo Gan <ganb@vmware.com> 2.4.1-3
-    cleanup GOPATH
*    Tue Sep 12 2017 Vinay Kulkarni <kulkarniv@vmware.com> 2.4.1-2
-    Build protoc-gen-gogofaster plugin from source.
*    Sat Aug 19 2017 Vinay Kulkarni <kulkarniv@vmware.com> 2.4.1-1
-    Calico Felix for PhotonOS.
