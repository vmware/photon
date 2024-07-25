%define network_required 1
Summary:        Kubernetes security benchmarking tool
Name:           kube-bench
Version:        0.6.12
Release:        10%{?dist}
Vendor:         VMware, Inc.
Distribution:   Photon
License:        Apache-2.0
URL:            https://github.com/aquasecurity/%{name}
Group:          Development/Tools

Source0: https://github.com/aquasecurity/%{name}/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512 %{name}=dc222f6fd1da5d40bdcf1b9bc366361274a00f6c90494df4006bd617aa2b5de8269ceb46b8197c787a3da3964db3b73e18334aed223e86083ea52ea544264a10

BuildRequires:  git
BuildRequires:  go

%description
The Kubernetes Bench for Security is a Go application that checks
whether Kubernetes is deployed according to security best practices.

%prep
%autosetup -p1

%build
export GOPATH=%{_builddir}
export KUBEBENCH_VERSION=%{version}-%{release}
%make_build build

%install
mkdir -p %{buildroot}%{_bindir}
cp %{name} %{buildroot}%{_bindir}

%if 0%{?with_check}
%check
make tests %{?_smp_mflags}
%endif

%files
%defattr(-,root,root,0755)
%{_bindir}/%{name}
%exclude %dir %{_libdir}/debug

%changelog
* Fri Jul 12 2024 Mukul Sikka <mukul.sikka@broadcom.com> 0.6.12-10
- Bump version as a part of go upgrade
* Thu Jun 20 2024 Mukul Sikka <msikka@vmware.com> 0.6.12-9
- Bump version as a part of go upgrade
* Thu Feb 22 2024 Mukul Sikka <msikka@vmware.com> 0.6.12-8
- Bump version as a part of go upgrade
* Tue Nov 21 2023 Piyush Gupta <gpiyush@vmware.com> 0.6.12-7
- Bump up version to compile with new go
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 0.6.12-6
- Bump up version to compile with new go
* Mon Sep 18 2023 Piyush Gupta <gpiyush@vmware.com> 0.6.12-5
- Bump up version to compile with new go
* Mon Jul 17 2023 Piyush Gupta <gpiyush@vmware.com> 0.6.12-4
- Bump up version to compile with new go
* Thu Jun 22 2023 Piyush Gupta <gpiyush@vmware.com> 0.6.12-3
- Bump up version to compile with new go
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 0.6.12-2
- Bump up version to compile with new go
* Thu Mar 09 2023 Prashant S Chauhan <psinghchauha@vmware.com> 0.6.12-1
- Update to 0.6.12
* Thu Mar 09 2023 Piyush Gupta <gpiyush@vmware.com> 0.6.10-3
- Bump up version to compile with new go
* Mon Nov 21 2022 Piyush Gupta <gpiyush@vmware.com> 0.6.10-2
- Bump up version to compile with new go
* Sun Nov 13 2022 Shreenidhi Shedi <sshedi@vmware.com> 0.6.10-1
- Upgrade to v0.6.10
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
