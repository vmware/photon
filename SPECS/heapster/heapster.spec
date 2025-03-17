%define gopath_comp_heapster k8s.io/heapster

Summary:        Heapster enables Container Cluster Monitoring and Performance Analysis.
Name:           heapster
Version:        1.5.4
Release:        22%{?dist}
URL:            https://github.com/wavefrontHQ/cadvisor
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/kubernetes/heapster/archive/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

Patch0: go-27704.patch
Patch1: go-27842.patch

%if 0%{?with_check}
Patch2: make-check-failure.patch
%endif

BuildRequires:  go
BuildRequires:  unzip

%description
Heapster collects and interprets various signals like compute resource usage, lifecycle events, etc, and exports cluster metrics via REST endpoints.

%prep
# Using autosetup is not feasible
%setup -q -c -n %{name}-%{version}

mkdir -p "$(dirname src/%{gopath_comp_heapster})"
mv %{name}-%{version} src/%{gopath_comp_heapster}
cd src/%{gopath_comp_heapster}

pushd vendor/golang.org/x/net
%autopatch -p1
popd

%if 0%{?with_check}
%patch -p1 2
%endif

%build
export GO111MODULE=auto
export GOPATH="${PWD}"
cd src/%{gopath_comp_heapster}
%make_build

%install
cd src/%{gopath_comp_heapster}
install -d -p %{buildroot}%{_bindir}
install -p -m 0755 %{name} %{buildroot}%{_bindir}
install -p -m 0755 eventer %{buildroot}%{_bindir}

%if 0%{?with_check}
%check
export GO111MODULE=auto
export GOPATH="${PWD}"
cd src/%{gopath_comp_heapster}
make test-unit %{?_smp_mflags}
%endif

%files
%defattr(-,root,root)
%{_bindir}/%{name}
%{_bindir}/eventer

%changelog
* Wed Dec 11 2024 Tapas Kundu <tapas.kundu@broadcom.com> 1.5.4-22
- Release bump for SRP compliance
* Thu Sep 19 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.5.4-21
- Bump version as a part of go upgrade
* Fri Aug 23 2024 Bo Gan <bo.gan@broadcom.com> 1.5.4-20
- Simplify build scripts
* Fri Jul 12 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.5.4-19
- Bump version as a part of go upgrade
* Thu Jun 20 2024 Mukul Sikka <msikka@vmware.com> 1.5.4-18
- Bump version as a part of go upgrade
* Thu Feb 22 2024 Mukul Sikka <msikka@vmware.com> 1.5.4-17
- Bump version as a part of go upgrade
* Tue Nov 21 2023 Piyush Gupta <gpiyush@vmware.com> 1.5.4-16
- Bump up version to compile with new go
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 1.5.4-15
- Bump up version to compile with new go
* Mon Sep 18 2023 Piyush Gupta <gpiyush@vmware.com> 1.5.4-14
- Bump up version to compile with new go
* Mon Jul 17 2023 Piyush Gupta <gpiyush@vmware.com> 1.5.4-13
- Bump up version to compile with new go
* Thu Jun 22 2023 Piyush Gupta <gpiyush@vmware.com> 1.5.4-12
- Bump up version to compile with new go
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 1.5.4-11
- Bump up version to compile with new go
* Thu Mar 09 2023 Piyush Gupta <gpiyush@vmware.com> 1.5.4-10
- Bump up version to compile with new go
* Mon Nov 21 2022 Piyush Gupta <gpiyush@vmware.com> 1.5.4-9
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 1.5.4-8
- Bump up version to compile with new go
* Fri Jun 17 2022 Piyush Gupta <gpiyush@vmware.com> 1.5.4-7
- Bump up version to compile with new go
* Fri Jun 11 2021 Piyush Gupta<gpiyush@vmware.com> 1.5.4-6
- Bump up version to compile with new go
* Fri Feb 05 2021 Harinadh D <hdommaraju@vmware.com> 1.5.4-5
- Bump up version to compile with new go
* Fri Jan 15 2021 Piyush Gupta<gpiyush@vmware.com> 1.5.4-4
- Bump up version to compile with new go
* Mon Nov 16 2020 Prashant S Chauhan <psinghchauha@vmware.com> 1.5.4-3
- Fix make check
* Mon Jan 28 2019 Bo Gan <ganb@vmware.com> 1.5.4-2
- Fix CVE-2018-17846 and CVE-2018-17143
* Wed Sep 12 2018 Anish Swaminathan <anishs@vmware.com> 1.5.4-1
- Update to version 1.5.4
* Thu Aug 31 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.4.2-1
- Initial heapster package
