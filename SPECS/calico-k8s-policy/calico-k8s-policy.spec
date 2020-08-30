Summary:        Calico Network Policy for Kubernetes
Name:           calico-k8s-policy
Version:        3.16.0
Release:        1%{?dist}
License:        Apache-2.0
URL:            https://github.com/projectcalico/k8s-policy
Source0:        %{name}-%{version}.tar.gz
%define sha1 calico-k8s-policy=e5d0c1c7f3f589cb4c7487c7dc77d0302ac23418
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  git
BuildRequires:  go
BuildRequires:  libcalico
BuildRequires:  libffi-devel
BuildRequires:  openssl-devel
BuildRequires:  procps-ng
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-asn1crypto
BuildRequires:  python3-backports.ssl_match_hostname
BuildRequires:  python3-ConcurrentLogHandler
BuildRequires:  python3-cffi
BuildRequires:  python3-pycrypto
BuildRequires:  python3-cryptography
BuildRequires:  python3-dnspython
BuildRequires:  python3-docopt
BuildRequires:  python3-etcd
BuildRequires:  python3-idna
BuildRequires:  python3-ipaddress
BuildRequires:  python3-netaddr
BuildRequires:  python3-ndg-httpsclient
BuildRequires:  python3-pyOpenSSL
BuildRequires:  python3-pip
BuildRequires:  python3-prettytable
BuildRequires:  python3-prometheus_client
BuildRequires:  python3-pyasn1
BuildRequires:  python3-pycparser
BuildRequires:  python3-pyinstaller
BuildRequires:  python3-PyYAML
BuildRequires:  python3-requests
BuildRequires:  python3-setuptools
BuildRequires:  python3-simplejson
BuildRequires:  python3-six
BuildRequires:  python3-subprocess32
BuildRequires:  python3-urllib3
BuildRequires:  python3-websocket-client
BuildRequires:  python3-virtualenv
BuildRequires:  python3
Requires:       python3
Requires:       python3-libs
Requires:       python3-setuptools
%define debug_package %{nil}

%description
Calico Network Policy enables Calico to enforce network policy on top of Calico BGP, Flannel, or GCE native.

%prep
%setup -n kube-controllers-%{version}
echo "VERSION='`git describe --tags --dirty`'" > version.py

%build
mkdir -p dist
go build -v -o dist/controller -ldflags "-X main.VERSION=%{version}" ./cmd/kube-controllers/

%install
install -vdm 755 %{buildroot}%{_bindir}
install -vpm 0755 -t %{buildroot}%{_bindir}/ dist/controller

%files
%defattr(-,root,root)
%{_bindir}/controller

%changelog
*   Tue Jun 23 2020 Gerrit Photon <photon-checkins@vmware.com> 3.16.0-1
-   Automatic Version Bump
*   Thu Jun 18 2020 Tapas Kundu <tkundu@vmware.com> 1.0.0-5
-   Build with python3
-   Mass removal python2
*   Wed Jun 17 2020 Ashwin H <ashwinh@vmware.com> 1.0.0-4
-   Fix dependency for cloud.google.com-go
*   Tue Jun 09 2020 Ashwin H <ashwinh@vmware.com> 1.0.0-3
-   Use cache for dependencies
*   Mon Jan 28 2019 Bo Gan <ganb@vmware.com> 1.0.0-2
-   Fix CVE-2018-17846 and CVE-2018-17143
*   Tue Nov 14 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.0.0-1
-   Calico kubernetes policy v1.0.0.
*   Tue Nov 07 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.7.0-1
-   Calico kubernetes policy v0.7.0.
*   Tue Aug 22 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.5.4-1
-   Calico kubernetes policy for PhotonOS.
