Summary:        Kubernetes security benchmarking tool
Name:           kube-bench
Version:        0.3.1
Release:        4%{?dist}
Vendor:         VMware, Inc.
Distribution:   Photon
License:        Apache-2.0
URL:            https://github.com/aquasecurity/kube-bench
Group:          Development/Tools
Source0:        %{name}-%{version}.tar.gz
%define sha1    kube-bench=239bdff14467764c38211615e09b41b0e8a047ad
BuildRequires:  git
BuildRequires:  go

%description
The Kubernetes Bench for Security is a Go application that checks whether Kubernetes is deployed according to security best practices

%prep
%setup -q

%build
KUBEBENCH_VERSION=v%{version} make

%install
mkdir -p %{buildroot}%{_bindir}
cp kube-bench %{buildroot}%{_bindir}

%check
make tests

%files
%defattr(-,root,root,0755)
%{_bindir}/kube-bench

%changelog
*   Thu Mar 25 2021 Piyush Gupta<gpiyush@vmware.com> 0.3.1-4
-   Bump up version to compile with new go
*   Fri Feb 05 2021 Harinadh D <hdommaraju@vmware.com> 0.3.1-3
-   Bump up version to compile with new go
*   Fri Jan 15 2021 Piyush Gupta<gpiyush@vmware.com> 0.3.1-2
-   Bump up version to compile with new go
*   Wed Jul 22 2020 Gerrit Photon <photon-checkins@vmware.com> 0.3.1-1
-   Automatic Version Bump
*   Wed Oct 30 2019 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.0.34-1
-   Initial
