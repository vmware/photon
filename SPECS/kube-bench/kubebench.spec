Summary:        Kubernetes security benchmarking tool
Name:           kube-bench
Version:        0.3.1
Release:        14%{?dist}
Vendor:         VMware, Inc.
Distribution:   Photon
License:        Apache-2.0
URL:            https://github.com/aquasecurity/kube-bench
Group:          Development/Tools
Source0:        %{name}-%{version}.tar.gz
%define sha512  kube-bench=54e46221040ac45a787ff9078de2af7b638b5f67ef5616fed532c09607aae049d4bd7496065ade72a5df07b99d7ff6f70683731783f5c651aff56dfc06d61d97
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
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 0.3.1-14
- Bump up version to compile with new go
* Thu Sep 15 2022 Piyush Gupta <gpiyush@vmware.com> 0.3.1-13
- Bump up version to compile with new go
* Fri Aug 19 2022 Piyush Gupta <gpiyush@vmware.com> 0.3.1-12
- Bump up version to compile with new go
* Tue Jul 12 2022 Piyush Gupta <gpiyush@vmware.com> 0.3.1-11
- Bump up version to compile with new go
*   Sat May 07 2022 Piyush Gupta <gpiyush@vmware.com> 0.3.1-10
-   Bump up version to compile with new go
*   Tue Feb 22 2022 Piyush Gupta <gpiyush@vmware.com> 0.3.1-9
-   Bump up version to compile with new go
*   Mon Jan 24 2022 Piyush Gupta <gpiyush@vmware.com> 0.3.1-8
-   Bump up version to compile with new go
*   Wed Oct 20 2021 Piyush Gupta <gpiyush@vmware.com> 0.3.1-7
-   Bump up version to compile with new go
*   Tue Oct 05 2021 Piyush Gupta <gpiyush@vmware.com> 0.3.1-6
-   Bump up version to compile with new go
*   Fri Jun 11 2021 Piyush Gupta <gpiyush@vmware.com> 0.3.1-5
-   Bump up version to compile with new go
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
