Summary:	Heapster enables Container Cluster Monitoring and Performance Analysis.
Name:		heapster
Version:        1.4.2
Release:        5%{?dist}
License:	Apache 2.0
URL:		https://github.com/wavefrontHQ/cadvisor
Source0:	https://github.com/kubernetes/heapster/archive/%{name}-%{version}.tar.gz
%define sha1 heapster=e7c22e3f6c5223345259cabb761571b815a587e6
Patch0:         go-27704.patch
Patch1:         go-27842.patch
Group:		Development/Tools
Vendor:		VMware, Inc.
Distribution: 	Photon
BuildRequires:  go
BuildRequires:  unzip

%description
Heapster collects and interprets various signals like compute resource usage, lifecycle events, etc, and exports cluster metrics via REST endpoints.

%prep
%setup -q

pushd vendor/golang.org/x/net
%patch0 -p1
%patch1 -p1
popd

%build
mkdir -p $GOPATH/src/k8s.io/heapster
cp -r . $GOPATH/src/k8s.io/heapster
cd $GOPATH/src/k8s.io/heapster
make build

%install
cd $GOPATH/src/k8s.io/heapster
install -d -p %{buildroot}%{_bindir}
install -p -m 0755 heapster %{buildroot}%{_bindir}
install -p -m 0755 eventer %{buildroot}%{_bindir}

%check
cd $GOPATH/src/k8s.io/heapster
make test-unit

%files
%defattr(-,root,root)
%{_bindir}/heapster
%{_bindir}/eventer

%changelog
*   Fri Apr 10 2020 Harinadh D <hdommaraju@vmware.com> 1.4.2-5
-   Bump up version to compile with go 1.13.5-2
*   Tue Jan 07 2020 Ashwin H <ashwinh@vmware.com> 1.4.2-4
-   Bump up version to compile with new go
*   Fri Aug 30 2019 Ashwin H <ashwinh@vmware.com> 1.4.2-3
-   Bump up version to compile with new go
*   Fri May 03 2019 Bo Gan <ganb@vmware.com> 1.4.2-2
-   Fix CVE-2018-17846 and CVE-2018-17143
*   Thu Aug 31 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.4.2-1
-   Initial heapster package
