Summary:        Kubernetes DNS
Name:           kubernetes-dns
Version:        1.14.6
Release:        2%{?dist}
License:        ASL 2.0
URL:            https://github.com/kubernetes/dns/archive/%{version}.tar.gz
Source0:        kubernetes-dns-%{version}.tar.gz
%define sha1    kubernetes-dns-%{version}.tar.gz=456f28dcb52d5338ce076d62051e33b827172b2a
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  go

%description
Kubernetes DNS is a name lookup service for kubernetes pods.

%prep -p exit
%setup -qn dns-%{version}

%build
export GOPATH="$(pwd)"
export PKG=k8s.io/dns
cd ..
mv "${GOPATH}" dns
mkdir -p "${GOPATH}/src/k8s.io"
mv dns "${GOPATH}/src/k8s.io/"
cd "${GOPATH}/src/k8s.io/"

export VERSION=%{version}
export CGO_ENABLED=0

go install \
    -installsuffix "static" \
    -ldflags "-X ${PKG}/pkg/version.VERSION=${VERSION}" \
    ./...

%install
install -m 755 -d %{buildroot}%{_bindir}
binaries=(dnsmasq-nanny e2e ginkgo kube-dns sidecar sidecar-e2e)
for bin in "${binaries[@]}"; do
  echo "+++ INSTALLING ${bin}"
  install -pm 755 -t %{buildroot}%{_bindir} bin/${bin}
done

%check
export GOPATH="$(pwd)"

export VERSION=%{version}
export PKG=k8s.io/dns

cd "${GOPATH}/src/${PKG}"
./build/test.sh cmd pkg

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/dnsmasq-nanny
%{_bindir}/e2e
%{_bindir}/ginkgo
%{_bindir}/kube-dns
%{_bindir}/sidecar
%{_bindir}/sidecar-e2e

%changelog
*   Wed Oct 18 2017 Bo Gan <ganb@vmware.com> 1.14.6-2
-   cleanup GOPATH
*   Mon Oct 02 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.14.6-1
-   kubernetes-dns 1.14.6.
*   Mon Sep 11 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.14.4-1
-   kubernetes-dns 1.14.4.
*   Wed Jun 28 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.14.2-1
-   kubernetes-dns for PhotonOS.
