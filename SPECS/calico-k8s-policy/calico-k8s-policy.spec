Summary:        Calico Network Policy for Kubernetes
Name:           calico-k8s-policy
Version:        1.0.0
Release:        4%{?dist}
License:        Apache-2.0
URL:            https://github.com/projectcalico/k8s-policy
Source0:        %{name}-%{version}.tar.gz
%define sha1 calico-k8s-policy=612eafdb2afee6ffbfc432e0110c787823b66ccc
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  git
BuildRequires:  glide
BuildRequires:  go >= 1.8
BuildRequires:  libcalico
BuildRequires:  libffi
BuildRequires:  openssl-devel
BuildRequires:  procps-ng
BuildRequires:  python2
BuildRequires:  python2-devel
BuildRequires:  python2-libs
BuildRequires:  python-asn1crypto
BuildRequires:  python-backports.ssl_match_hostname
BuildRequires:  python-ConcurrentLogHandler
BuildRequires:  python-cffi
BuildRequires:  pycrypto
BuildRequires:  python-cryptography
BuildRequires:  python-dnspython
BuildRequires:  python-docopt
BuildRequires:  python-enum34
BuildRequires:  python-etcd
BuildRequires:  python-idna
BuildRequires:  python-ipaddress
BuildRequires:  python-netaddr
BuildRequires:  python-ndg-httpsclient
BuildRequires:  python-pyOpenSSL
BuildRequires:  python-pip
BuildRequires:  python-prettytable
BuildRequires:  python-prometheus_client
BuildRequires:  python-pyasn1
BuildRequires:  python-pycparser
BuildRequires:  python-pyinstaller
BuildRequires:  PyYAML
BuildRequires:  python-requests
BuildRequires:  python-setuptools
BuildRequires:  python-simplejson
BuildRequires:  python-six
BuildRequires:  python-subprocess32
BuildRequires:  python-urllib3
BuildRequires:  python-websocket-client
BuildRequires:  python-virtualenv
BuildRequires:  python3
Requires:       python2
Requires:       python2-libs
Requires:       python-setuptools
%define debug_package %{nil}

%description
Calico Network Policy enables Calico to enforce network policy on top of Calico BGP, Flannel, or GCE native.

%prep
%setup -n kube-controllers-%{version}
echo "VERSION='`git describe --tags --dirty`'" > version.py

%build
mkdir -p /root/.glide
mkdir -p ${GOPATH}/src/github.com/projectcalico/k8s-policy
cp -r * ${GOPATH}/src/github.com/projectcalico/k8s-policy
pushd ${GOPATH}/src/github.com/projectcalico/k8s-policy
glide install -strip-vendor
mkdir -p dist
CGO_ENABLED=0 go build -v -o dist/controller -ldflags "-X main.VERSION=%{version}" ./main.go

%install
pushd ${GOPATH}/src/github.com/projectcalico/k8s-policy
install -vdm 755 %{buildroot}%{_bindir}
install -vpm 0755 -t %{buildroot}%{_bindir}/ dist/controller

%files
%defattr(-,root,root)
%{_bindir}/controller

%changelog
*   Fri Apr 24 2020 Harinadh D <hdommaraju@vmware.com> 1.0.0-4
-   Bump up version to compile with new go version
*   Fri Jan 03 2020 Ashwin H <ashwinh@vmware.com> 1.0.0-3
-   Bump up version to compile with new go
*   Fri Aug 30 2019 Ashwin H <ashwinh@vmware.com> 1.0.0-2
-   Bump up version to compile with new go
*   Fri Nov 17 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.0.0-1
-   Calico kubernetes policy v1.0.0.
*   Wed Nov 08 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.7.0-1
-   Calico kubernetes policy v0.7.0.
*   Fri Oct 13 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.5.4-1
-   Calico kubernetes policy for PhotonOS.
