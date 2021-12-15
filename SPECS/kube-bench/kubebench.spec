Summary:        Kubernetes security benchmarking tool
Name:           kube-bench
Version:        0.0.34
Release:        9%{?dist}
Vendor:         VMware, Inc.
Distribution:   Photon
License:        Apache-2.0
URL:            https://github.com/aquasecurity/kube-bench
Group:          Development/Tools
Source0:        %{name}-%{version}.tar.gz
%define sha1    kube-bench=edcc534b23abcf0c699fc6bde648b48ddaee9577
BuildRequires:  git
BuildRequires:  go

%description
The Kubernetes Bench for Security is a Go application that checks whether Kubernetes is deployed according to security best practices

%prep
%autosetup

%build
KUBEBENCH_VERSION=v%{version} make %{?_smp_mflags}

%install
mkdir -p %{buildroot}%{_bindir}
cp kube-bench %{buildroot}%{_bindir}

%check
make tests %{?_smp_mflags}

%files
    %defattr(-,root,root,0755)
    %{_bindir}/kube-bench

%changelog
*   Tue Nov 16 2021 Piyush Gupta <gpiyush@vmware.com> 0.0.34-9
-   Bump up version to compile with new go
*   Wed Oct 20 2021 Piyush Gupta <gpiyush@vmware.com> 0.0.34-8
-   Bump up version to compile with new go
*   Sat Aug 21 2021 Piyush Gupta<gpiyush@vmware.com> 0.0.34-7
-   Bump up version to compile with new go
*   Tue Jun 29 2021 Piyush Gupta <gpiyush@vmware.com> 0.0.34-6
-   Bump up version to compile with new go
*   Mon May 03 2021 Piyush Gupta<gpiyush@vmware.com> 0.0.34-5
-   Bump up version to compile with new go
*   Mon Feb 08 2021 Harinadh D <hdommaraju@vmware.com> 0.0.34-4
-   Bump up version to compile with new go
*   Fri Nov 27 2020 HarinadhD <hdommaraju@vmware.com> 0.0.34-3
-   Bump up version to compile with new go
*   Fri Apr 10 2020 Harinadh D <hdommaraju@vmware.com> 0.0.34-2
-   Bump up version to compile with go 1.13.3-2
*   Wed Oct 30 2019 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.0.34-1
-   Initial
