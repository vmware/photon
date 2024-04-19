Summary:    Heapster enables Container Cluster Monitoring and Performance Analysis.
Name:       heapster
Version:    1.5.4
Release:    25%{?dist}
License:    Apache 2.0
URL:        https://github.com/wavefrontHQ/cadvisor
Group:      Development/Tools
Vendor:     VMware, Inc.
Distribution: Photon

Source0:  https://github.com/kubernetes/heapster/archive/%{name}-%{version}.tar.gz
%define sha512  heapster=9c5f1e11b224efe6aaa42aad0daecede2c22d86d692a9d008643d9731d78becce98c8332ebe8d17568a93abe1f56dabf868dcd7ebc1e7b48e1f6f6f8f3878152

Patch0:     go-27704.patch
Patch1:     go-27842.patch

%if 0%{?with_check}
Patch2:     make-check-failure.patch
%endif

BuildRequires:  go
BuildRequires:  unzip

%description
Heapster collects and interprets various signals like compute resource usage, lifecycle events, etc, and exports cluster metrics via REST endpoints.

%prep
# Using autosetup is not feasible
%setup -q

pushd vendor/golang.org/x/net
%autopatch -p1 -M1
popd
%if 0%{?with_check}
%patch2 -p1
%endif

%build
export GO111MODULE=auto
mkdir -p $GOPATH/src/k8s.io/heapster
cp -r . $GOPATH/src/k8s.io/heapster
cd $GOPATH/src/k8s.io/heapster
%make_build

%install
cd $GOPATH/src/k8s.io/heapster
install -d -p %{buildroot}%{_bindir}
install -p -m 0755 heapster %{buildroot}%{_bindir}
install -p -m 0755 eventer %{buildroot}%{_bindir}

%if 0%{?with_check}
%check
#keeping GO111MODULE as off in order to use GOPATH.
export GO111MODULE=off
cd $GOPATH/src/k8s.io/heapster
make test-unit %{?_smp_mflags}
%endif

%files
%defattr(-,root,root)
%{_bindir}/heapster
%{_bindir}/eventer

%changelog
* Thu Apr 18 2024 Mukul Sikka <msikka@vmware.com> 1.5.4-25
- Bump version as a part of go upgrade
* Tue Nov 21 2023 Piyush Gupta <gpiyush@vmware.com> 1.5.4-24
- Bump up version to compile with new go
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 1.5.4-23
- Bump up version to compile with new go
* Fri Aug 18 2023 Piyush Gupta <gpiyush@vmware.com> 1.5.4-22
- Bump up version to compile with new go
* Tue Jun 20 2023 Piyush Gupta <gpiyush@vmware.com> 1.5.4-21
- Bump up version to compile with new go
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 1.5.4-20
- Bump up version to compile with new go
* Thu Mar 16 2023 Piyush Gupta <gpiyush@vmware.com> 1.5.4-19
- Bump up version to compile with new go
* Tue Dec 20 2022 Piyush Gupta <gpiyush@vmware.com> 1.5.4-18
- Bump up version to compile with new go
* Sun Nov 13 2022 Piyush Gupta <gpiyush@vmware.com> 1.5.4-17
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 1.5.4-16
- Bump up version to compile with new go
* Thu Sep 15 2022 Piyush Gupta <gpiyush@vmware.com> 1.5.4-15
- Bump up version to compile with new go
* Fri Aug 19 2022 Piyush Gupta <gpiyush@vmware.com> 1.5.4-14
- Bump up version to compile with new go
* Tue Jul 12 2022 Piyush Gupta <gpiyush@vmware.com> 1.5.4-13
- Bump up version to compile with new go
* Sat May 07 2022 Piyush Gupta <gpiyush@vmware.com> 1.5.4-12
- Bump up version to compile with new go
* Tue Feb 22 2022 Piyush Gupta <gpiyush@vmware.com> 1.5.4-11
- Bump up version to compile with new go
* Mon Jan 24 2022 Piyush Gupta <gpiyush@vmware.com> 1.5.4-10
- Bump up version to compile with new go
* Wed Oct 20 2021 Piyush Gupta <gpiyush@vmware.com> 1.5.4-9
- Bump up version to compile with new go
* Tue Oct 05 2021 Piyush Gupta <gpiyush@vmware.com> 1.5.4-8
- Bump up version to compile with new go
* Fri Jun 11 2021 Piyush Gupta <gpiyush@vmware.com> 1.5.4-7
- Bump up version to compile with new go
* Thu Mar 25 2021 Piyush Gupta<gpiyush@vmware.com> 1.5.4-6
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
