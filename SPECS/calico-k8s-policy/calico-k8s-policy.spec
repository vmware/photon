Summary:        Calico Network Policy for Kubernetes
Name:           calico-k8s-policy
Version:        0.7.0
Release:        1%{?dist}
License:        Apache-2.0
URL:            https://github.com/projectcalico/k8s-policy
Source0:        %{name}-%{version}.tar.gz
%define sha1 calico-k8s-policy=da2699fa9094ea497996930f172dbdf001dc648b
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  git
BuildRequires:  libcalico
BuildRequires:  libffi-devel
BuildRequires:  openssl-devel
BuildRequires:  python2
BuildRequires:  python2-devel
BuildRequires:  python2-libs
BuildRequires:  python-pip
BuildRequires:  python-backports.ssl_match_hostname
BuildRequires:  python-ConcurrentLogHandler
BuildRequires:  python-docopt
BuildRequires:  python-pip
BuildRequires:  python-prettytable
BuildRequires:  python-prometheus_client
BuildRequires:  python-pyinstaller
BuildRequires:  PyYAML
BuildRequires:  python-requests
BuildRequires:  python-setuptools
BuildRequires:  python-simplejson
BuildRequires:  python-websocket-client
BuildRequires:  python-virtualenv
BuildRequires:  python3
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
*   Tue Aug 22 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.7.0-1
-   Calico kubernetes policy for PhotonOS.
