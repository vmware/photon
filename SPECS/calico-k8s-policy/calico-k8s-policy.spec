Summary:        Calico Network Policy for Kubernetes
Name:           calico-k8s-policy
Version:        0.5.4
Release:        1%{?dist}
License:        Apache-2.0
URL:            https://github.com/projectcalico/k8s-policy
Source0:        %{name}-%{version}.tar.gz
%define sha1 calico-k8s-policy=83623f81e50d81dc1dd858c9ae340a10ba3670e3
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  git
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
%setup -n k8s-policy-%{version}
echo "VERSION='`git describe --tags --dirty`'" > version.py

%build
pyinstaller controller.py -ayF

%install
install -vdm 755 %{buildroot}%{_bindir}
install -vpm 0755 -t %{buildroot}%{_bindir}/ dist/controller

%files
%defattr(-,root,root)
%{_bindir}/controller

%changelog
*   Tue Aug 22 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.5.4-1
-   Calico kubernetes policy for PhotonOS.
