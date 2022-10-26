Summary:        Calico Network Policy for Kubernetes
Name:           calico-k8s-policy
Version:        3.21.0
Release:        5%{?dist}
License:        Apache-2.0
URL:            https://github.com/projectcalico/k8s-policy
Source0:        %{name}-%{version}.tar.gz
%define sha512  calico-k8s-policy=c2f9267a1b924935bd7b4c36d47af3f72e24f841a5b46540e17ca8cf15dcaf38b72b3b7bfcdc067f21977439dc88af033d2fffd55465188bfc0be07b40902392
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  git
BuildRequires:  glide
BuildRequires:  go >= 1.8
BuildRequires:  libcalico
BuildRequires:  libffi-devel
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
%autosetup -n kube-controllers-%{version}
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
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 3.21.0-5
- Bump up version to compile with new go
* Thu Sep 15 2022 Piyush Gupta <gpiyush@vmware.com> 3.21.0-4
- Bump up version to compile with new go
* Thu Aug 18 2022 Piyush Gupta <gpiyush@vmware.com> 3.21.0-3
- Bump up version to compile with new go
* Fri May 27 2022 Piyush Gupta <gpiyush@vmware.com> 3.21.0-2
- Bump up version to compile with new go.
* Tue May 17 2022 Prashant S Chauhan <psinghchauha@vmware.com> 3.21.0-1
- Update to 3.21.0
* Wed Mar 16 2022 Piyush Gupta <gpiyush@vmware.com> 1.0.0-16
- Bump up version to compile with new go
* Tue Feb 22 2022 Piyush Gupta <gpiyush@vmware.com> 1.0.0-15
- Bump up version to compile with new go
* Tue Nov 16 2021 Piyush Gupta <gpiyush@vmware.com> 1.0.0-13
- Bump up version to compile with new go
* Wed Oct 20 2021 Piyush Gupta <gpiyush@vmware.com> 1.0.0-12
- Bump up version to compile with new go
* Sat Aug 21 2021 Piyush Gupta<gpiyush@vmware.com> 1.0.0-11
- Bump up version to compile with new go
* Tue Jun 29 2021 Piyush Gupta <gpiyush@vmware.com> 1.0.0-10
- Bump up version to compile with new go
* Mon May 03 2021 Piyush Gupta<gpiyush@vmware.com> 1.0.0-9
- Bump up version to compile with new go
* Mon Feb 08 2021 Harinadh D <hdommaraju@vmware.com> 1.0.0-8
- Bump up version to compile with new go
* Fri Nov 27 2020 HarinadhD <hdommaraju@vmware.com> 1.0.0-7
- Bump up version to compile with new go
* Tue Aug 18 2020 Ashwin H <ashwinh@vmware.com> 1.0.0-6
- Bump up version to compile with new go
* Fri Apr 10 2020 Harinadh D <hdommaraju@vmware.com> 1.0.0-5
- Bump up version to compile with go 1.13.3-2
* Tue Oct 22 2019 Ashwin H <ashwinh@vmware.com> 1.0.0-4
- Bump up version to compile with go 1.13.3
* Fri Aug 30 2019 Ashwin H <ashwinh@vmware.com> 1.0.0-3
- Bump up version to compile with new go
* Mon Jan 28 2019 Bo Gan <ganb@vmware.com> 1.0.0-2
- Fix CVE-2018-17846 and CVE-2018-17143
* Tue Nov 14 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.0.0-1
- Calico kubernetes policy v1.0.0.
* Tue Nov 07 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.7.0-1
- Calico kubernetes policy v0.7.0.
* Tue Aug 22 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.5.4-1
- Calico kubernetes policy for PhotonOS.
