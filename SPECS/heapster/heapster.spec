Summary:	Heapster enables Container Cluster Monitoring and Performance Analysis.
Name:		heapster
Version:    1.5.4
Release:    10%{?dist}
License:	Apache 2.0
URL:		https://github.com/wavefrontHQ/cadvisor
Source0:	https://github.com/kubernetes/heapster/archive/%{name}-%{version}.tar.gz
%define sha1 heapster=102b8f21ecebc695987701b1d97f87dda1ea5645
Patch0:         go-27704.patch
Patch1:         go-27842.patch
%if %{with_check}
Patch2:         make-check-failure.patch
%endif
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
%if %{with_check}
%patch2 -p1
%endif
%build
go env -w GO111MODULE=auto
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
*   Tue Jun 29 2021 Piyush Gupta <gpiyush@vmware.com> 1.5.4-10
-   Bump up version to compile with new go
*   Mon May 03 2021 Piyush Gupta<gpiyush@vmware.com> 1.5.4-9
-   Bump up version to compile with new go
*   Mon Feb 08 2021 Harinadh D <hdommaraju@vmware.com> 1.5.4-8
-   Bump up version to compile with new go
*   Fri Nov 27 2020 HarinadhD <hdommaraju@vmware.com> 1.5.4-7
-   Bump up version to compile with new go
*   Fri Apr 10 2020 Harinadh D <hdommaraju@vmware.com> 1.5.4-6
-   Bump up version to compile with go 1.13.3-2
*   Tue Oct 22 2019 Ashwin H <ashwinh@vmware.com> 1.5.4-5
-   Bump up version to compile with go 1.13.3
*   Mon Sep 23 2019 Prashant Singh Chauhan <psinghchauha@vmware.com> 1.5.4-4
-   Fix for make check failure
*   Fri Aug 30 2019 Ashwin H <ashwinh@vmware.com> 1.5.4-3
-   Bump up version to compile with new go
*   Mon Jan 28 2019 Bo Gan <ganb@vmware.com> 1.5.4-2
-   Fix CVE-2018-17846 and CVE-2018-17143
*   Wed Sep 12 2018 Anish Swaminathan <anishs@vmware.com> 1.5.4-1
-   Update to version 1.5.4
*   Thu Aug 31 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.4.2-1
-   Initial heapster package
