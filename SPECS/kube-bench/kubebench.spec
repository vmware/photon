Summary:        Kubernetes security benchmarking tool
Name:           kube-bench
Version:        0.3.1
Release:        6%{?dist}
Vendor:         VMware, Inc.
Distribution:   Photon
License:        Apache-2.0
URL:            https://github.com/aquasecurity/%{name}
Group:          Development/Tools
Source0:        https://github.com/aquasecurity/%{name}/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512  %{name}=54e46221040ac45a787ff9078de2af7b638b5f67ef5616fed532c09607aae049d4bd7496065ade72a5df07b99d7ff6f70683731783f5c651aff56dfc06d61d97
BuildRequires:  git
BuildRequires:  go

%description
The Kubernetes Bench for Security is a Go application that checks whether Kubernetes is deployed according to security best practices

%prep
%autosetup -p1

%build
KUBEBENCH_VERSION=v%{version} make %{?_smp_mflags}

%install
mkdir -p %{buildroot}%{_bindir}
cp %{name} %{buildroot}%{_bindir}

%check
make tests %{?_smp_mflags}

%files
%defattr(-,root,root,0755)
%{_bindir}/%{name}

%changelog
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 0.3.1-6
- Bump up version to compile with new go
* Fri Jun 17 2022 Piyush Gupta <gpiyush@vmware.com> 0.3.1-5
- Bump up version to compile with new go
* Fri Jun 11 2021 Piyush Gupta<gpiyush@vmware.com> 0.3.1-4
- Bump up version to compile with new go
* Fri Feb 05 2021 Harinadh D <hdommaraju@vmware.com> 0.3.1-3
- Bump up version to compile with new go
* Fri Jan 15 2021 Piyush Gupta<gpiyush@vmware.com> 0.3.1-2
- Bump up version to compile with new go
* Wed Jul 22 2020 Gerrit Photon <photon-checkins@vmware.com> 0.3.1-1
- Automatic Version Bump
* Wed Oct 30 2019 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.0.34-1
- Initial
