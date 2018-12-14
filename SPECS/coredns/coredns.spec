Summary:        CoreDNS
Name:           coredns
Version:        1.2.6
Release:        1%{?dist}
License:        Apache License 2.0
URL:            https://github.com/coredns/coredns/archive/v%{version}.tar.gz
Source0:        coredns-%{version}.tar.gz
%define sha1    coredns-%{version}.tar.gz=ade0b29e32deb02e3bd79ec9d3418df78843dd41
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  go
BuildRequires:  git
%define debug_package %{nil}

%description
CoreDNS is a DNS server that chains plugins

%prep -p exit
%setup -qn coredns-%{version}

%build
export ARCH=amd64
export VERSION=%{version}
export PKG=github.com/%{name}/%{name}
export GOARCH=${ARCH}
export GOHOSTARCH=${ARCH}
export GOOS=linux
export GOHOSTOS=linux
export GOROOT=/usr/lib/golang
export GOPATH=/usr/share/gocode
export GOBIN=/usr/share/gocode/bin
export PATH=$PATH:$GOBIN
mkdir -p ${GOPATH}/src/${PKG}
cp -rf . ${GOPATH}/src/${PKG}
pushd ${GOPATH}/src/${PKG}
make

%install
install -m 755 -d %{buildroot}%{_bindir}
install -pm 755 -t %{buildroot}%{_bindir} ${GOPATH}/src/github.com/%{name}/%{name}/coredns

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/coredns

%changelog
*   Fri Dec 14 2018 Emil John <ejohn@vmware.com> 1.2.6-1
-   Update CoreDNS to v1.2.6
*   Fri Aug 03 2018 Dheeraj Shetty <dheerajs@vmware.com> 1.2.0-1
-   Initial version of coredns 1.2.0.
