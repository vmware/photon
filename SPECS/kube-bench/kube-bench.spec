Summary:        Kubernetes security benchmarking tool
Name:           kube-bench
Version:        0.6.12
Release:        7%{?dist}
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
* Fri Jul 12 2024 Mukul Sikka <mukul.sikka@broadcom.com> 0.6.12-7
- Bump version as a part of go upgrade
* Thu Jun 20 2024 Mukul Sikka <msikka@vmware.com> 0.6.12-6
- Bump version as a part of go upgrade
* Thu Apr 18 2024 Mukul Sikka <msikka@vmware.com> 0.6.12-5
- Bump version as a part of go upgrade
* Tue Nov 21 2023 Piyush Gupta <gpiyush@vmware.com> 0.6.12-4
- Bump up version to compile with new go
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 0.6.12-3
- Bump up version to compile with new go
* Fri Aug 18 2023 Piyush Gupta <gpiyush@vmware.com> 0.6.12-2
- Bump up version to compile with new go
* Mon Jun 26 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.6.12-1
- Upgrade to v0.6.12, includes security fixes
* Tue Jun 20 2023 Piyush Gupta <gpiyush@vmware.com> 0.3.1-19
- Bump up version to compile with new go
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 0.3.1-18
- Bump up version to compile with new go
* Thu Mar 16 2023 Piyush Gupta <gpiyush@vmware.com> 0.3.1-17
- Bump up version to compile with new go
* Tue Dec 20 2022 Piyush Gupta <gpiyush@vmware.com> 0.3.1-16
- Bump up version to compile with new go
* Sun Nov 13 2022 Piyush Gupta <gpiyush@vmware.com> 0.3.1-15
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 0.3.1-14
- Bump up version to compile with new go
* Thu Sep 15 2022 Piyush Gupta <gpiyush@vmware.com> 0.3.1-13
- Bump up version to compile with new go
* Fri Aug 19 2022 Piyush Gupta <gpiyush@vmware.com> 0.3.1-12
- Bump up version to compile with new go
* Tue Jul 12 2022 Piyush Gupta <gpiyush@vmware.com> 0.3.1-11
- Bump up version to compile with new go
* Sat May 07 2022 Piyush Gupta <gpiyush@vmware.com> 0.3.1-10
- Bump up version to compile with new go
* Tue Feb 22 2022 Piyush Gupta <gpiyush@vmware.com> 0.3.1-9
- Bump up version to compile with new go
* Mon Jan 24 2022 Piyush Gupta <gpiyush@vmware.com> 0.3.1-8
- Bump up version to compile with new go
* Wed Oct 20 2021 Piyush Gupta <gpiyush@vmware.com> 0.3.1-7
- Bump up version to compile with new go
* Tue Oct 05 2021 Piyush Gupta <gpiyush@vmware.com> 0.3.1-6
- Bump up version to compile with new go
* Fri Jun 11 2021 Piyush Gupta <gpiyush@vmware.com> 0.3.1-5
- Bump up version to compile with new go
* Thu Mar 25 2021 Piyush Gupta<gpiyush@vmware.com> 0.3.1-4
- Bump up version to compile with new go
* Fri Feb 05 2021 Harinadh D <hdommaraju@vmware.com> 0.3.1-3
- Bump up version to compile with new go
* Fri Jan 15 2021 Piyush Gupta<gpiyush@vmware.com> 0.3.1-2
- Bump up version to compile with new go
* Wed Jul 22 2020 Gerrit Photon <photon-checkins@vmware.com> 0.3.1-1
- Automatic Version Bump
* Wed Oct 30 2019 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.0.34-1
- Initial
