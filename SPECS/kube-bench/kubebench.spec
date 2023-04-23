Summary:        Kubernetes security benchmarking tool
Name:           kube-bench
Version:        0.0.34
Release:        20%{?dist}
Vendor:         VMware, Inc.
Distribution:   Photon
License:        Apache-2.0
URL:            https://github.com/aquasecurity/kube-bench
Group:          Development/Tools
Source0:        %{name}-%{version}.tar.gz
%define sha512  kube-bench=4df1b88ae3d6425dff7473066bfa6561f32e5ef6f137984f7a90e713f3dd1e59f8551353cbc3e86fe35c6cd3793d2acc13b9db426bd7930d22d1a06e9c7f4156
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
eu-elfcompress -q -p -t none %{buildroot}%{_bindir}/kube-bench

%check
make tests %{?_smp_mflags}

%files
    %defattr(-,root,root,0755)
    %{_bindir}/kube-bench

%changelog
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 0.0.34-20
- Bump up version to compile with new go
* Tue Apr 04 2023 Piyush Gupta <gpiyush@vmware.com> 0.0.34-19
- Bump up version to compile with new go
* Tue Dec 20 2022 Piyush Gupta <gpiyush@vmware.com> 0.0.34-18
- Bump up version to compile with new go
* Sun Nov 13 2022 Piyush Gupta <gpiyush@vmware.com> 0.0.34-17
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 0.0.34-16
- Bump up version to compile with new go
* Thu Sep 15 2022 Piyush Gupta <gpiyush@vmware.com> 0.0.34-15
- Bump up version to compile with new go
* Thu Aug 18 2022 Piyush Gupta <gpiyush@vmware.com> 0.0.34-14
- Bump up version to compile with new go
* Mon May 09 2022 Piyush Gupta <gpiyush@vmware.com> 0.0.34-13
- Bump up version to compile with new go
* Wed Mar 16 2022 Piyush Gupta <gpiyush@vmware.com> 0.0.34-12
- Bump up version to compile with new go
* Tue Feb 22 2022 Piyush Gupta <gpiyush@vmware.com> 0.0.34-11
- Bump up version to compile with new go
* Mon Jan 24 2022 Piyush Gupta <gpiyush@vmware.com> 0.0.34-10
- Bump up version to compile with new go
* Tue Nov 16 2021 Piyush Gupta <gpiyush@vmware.com> 0.0.34-9
- Bump up version to compile with new go
* Wed Oct 20 2021 Piyush Gupta <gpiyush@vmware.com> 0.0.34-8
- Bump up version to compile with new go
* Sat Aug 21 2021 Piyush Gupta<gpiyush@vmware.com> 0.0.34-7
- Bump up version to compile with new go
* Tue Jun 29 2021 Piyush Gupta <gpiyush@vmware.com> 0.0.34-6
- Bump up version to compile with new go
* Mon May 03 2021 Piyush Gupta<gpiyush@vmware.com> 0.0.34-5
- Bump up version to compile with new go
* Mon Feb 08 2021 Harinadh D <hdommaraju@vmware.com> 0.0.34-4
- Bump up version to compile with new go
* Fri Nov 27 2020 HarinadhD <hdommaraju@vmware.com> 0.0.34-3
- Bump up version to compile with new go
* Fri Apr 10 2020 Harinadh D <hdommaraju@vmware.com> 0.0.34-2
- Bump up version to compile with go 1.13.3-2
* Wed Oct 30 2019 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.0.34-1
- Initial
