Summary:        Calico Network Policy for Kubernetes
Name:           calico-k8s-policy
Version:        3.21.0
Release:        1%{?dist}
License:        Apache-2.0
URL:            https://github.com/projectcalico/k8s-policy
Source0:        %{name}-%{version}.tar.gz
%define sha1 calico-k8s-policy=f331429c73fcfe7bb0f2bf4b7612cf2a50df8125
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
BuildRequires:  python3-pycryptodome
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
%autosetup -p1 -n kube-controllers-%{version}
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
* Tue Jan 11 2022 Prashant S Chauhan <psinghchauha@vmware.com> 3.21.0-1
- Update to version 3.21.0
* Mon Jan 03 2022 Prashant S Chauhan <psinghchauha@vmware.com> 3.17.1-7
- Replace deprecated pycrypto with pycryptodome
* Thu Dec 09 2021 Prashant S Chauhan <psinghchauha@vmware.com> 3.17.1-6
- Bump up to compile with python 3.10
* Wed Oct 20 2021 Piyush Gupta <gpiyush@vmware.com> 3.17.1-5
- Bump up version to compile with new go
* Tue Oct 05 2021 Piyush Gupta <gpiyush@vmware.com> 3.17.1-4
- Bump up version to compile with new go
* Fri Jun 11 2021 Piyush Gupta <gpiyush@vmware.com> 3.17.1-3
- Bump up version to compile with new go
* Thu Mar 25 2021 Piyush Gupta<gpiyush@vmware.com> 3.17.1-2
- Bump up version to compile with new go
* Tue Feb 09 2021 Prashant S Chauhan <psinghchauha@vmware.com> 3.17.1-1
- Update to version 3.17.1
* Fri Feb 05 2021 Harinadh D <hdommaraju@vmware.com> 3.16.1-4
- Bump up version to compile with new go
* Fri Jan 15 2021 Piyush Gupta<gpiyush@vmware.com> 3.16.1-3
- Bump up version to compile with new go
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 3.16.1-2
- openssl 1.1.1
* Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 3.16.1-1
- Automatic Version Bump
* Tue Jun 23 2020 Gerrit Photon <photon-checkins@vmware.com> 3.16.0-1
- Automatic Version Bump
* Thu Jun 18 2020 Tapas Kundu <tkundu@vmware.com> 1.0.0-5
- Build with python3
- Mass removal python2
* Wed Jun 17 2020 Ashwin H <ashwinh@vmware.com> 1.0.0-4
- Fix dependency for cloud.google.com-go
* Tue Jun 09 2020 Ashwin H <ashwinh@vmware.com> 1.0.0-3
- Use cache for dependencies
* Mon Jan 28 2019 Bo Gan <ganb@vmware.com> 1.0.0-2
- Fix CVE-2018-17846 and CVE-2018-17143
* Tue Nov 14 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.0.0-1
- Calico kubernetes policy v1.0.0.
* Tue Nov 07 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.7.0-1
- Calico kubernetes policy v0.7.0.
* Tue Aug 22 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.5.4-1
- Calico kubernetes policy for PhotonOS.
