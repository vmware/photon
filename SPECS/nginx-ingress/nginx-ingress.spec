%global debug_package %{nil}

Summary:        NGINX Ingress Controller for Kubernetes
Name:           nginx-ingress
Version:        3.2.0
Release:        5%{?dist}
License:        Apache-2.0
URL:            https://github.com/nginxinc/kubernetes-ingress
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/nginxinc/kubernetes-ingress/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512  %{name}=aafac25ad1f6798d8b018f9f005ff4749fa954362dcc2587b9302059ce2641fde8e064031f2d7ab38d248be3a0a815c16cff28426d86ee0b40ad77eb3f8a1b55

BuildRequires:  go >= 1.7
BuildRequires:  ca-certificates
BuildRequires:  docker
BuildRequires:  git

%description
This is an implementation of kubernetes ingress controller for NGINX.

%prep
%autosetup -Sgit -n kubernetes-ingress-%{version}

%build
mkdir -p ${GOPATH}/src/github.com/nginxinc/kubernetes-ingress
cp -pr * ${GOPATH}/src/github.com/nginxinc/kubernetes-ingress/.

%make_build build TARGET=local \
     GIT_TAG="v%{version}" \
     VERSION="%{version}" \
     GIT_COMMIT="979db22d8065b22fedb410c9b9c5875cf0a6dc66"

%install
topdir="${PWD}"
install -vdm 755 %{buildroot}%{_bindir}
install -vpm 0755 -t %{buildroot}%{_bindir} %{name}
install -vdm 0755 %{buildroot}%{_datadir}/%{name}/docker

install -vpm 0755 -t %{buildroot}%{_datadir}/%{name}/docker/ \
            ${topdir}/internal/configs/version1/nginx.ingress.tmpl

install -vpm 0755 -t %{buildroot}%{_datadir}/%{name}/docker/ \
            ${topdir}/internal/configs/version1/nginx.tmpl

install -vpm 0755 -t %{buildroot}%{_datadir}/%{name}/docker/ \
            ${topdir}/internal/configs/version2/nginx.virtualserver.tmpl

install -vpm 0755 -t %{buildroot}%{_datadir}/%{name}/docker/ \
            ${topdir}/internal/configs/version2/nginx.transportserver.tmpl

%files
%defattr(-,root,root)
%{_bindir}/%{name}
%{_datadir}/%{name}/docker/nginx.*

%changelog
* Tue Nov 21 2023 Piyush Gupta <gpiyush@vmware.com> 3.2.0-5
- Bump up version to compile with new go
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 3.2.0-4
- Bump up version to compile with new go
* Tue Sep 26 2023 Piyush Gupta <gpiyush@vmware.com> 3.2.0-3
- Bump up version to compile with new go
* Fri Aug 18 2023 Piyush Gupta <gpiyush@vmware.com> 3.2.0-2
- Bump up version to compile with new go
* Wed Jun 28 2023 Shivani Agarwal <shivania2@vmware.com> 3.2.0-1
- Update to 3.2.0 to fix CVE-2023-0296
* Thu Jun 22 2023 Piyush Gupta <gpiyush@vmware.com> 2.3.0-6
- Bump up version to compile with new go
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 2.3.0-5
- Bump up version to compile with new go
* Tue Apr 04 2023 Piyush Gupta <gpiyush@vmware.com> 2.3.0-4
- Bump up version to compile with new go
* Tue Dec 20 2022 Piyush Gupta <gpiyush@vmware.com> 2.3.0-3
- Bump up version to compile with new go
* Sun Nov 13 2022 Piyush Gupta <gpiyush@vmware.com> 2.3.0-2
- Bump up version to compile with new go
* Mon Oct 31 2022 Keerthana K <keerthanak@vmware.com> 2.3.0-1
- Update to 2.3.0
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 1.3.0-18
- Bump up version to compile with new go
* Thu Sep 15 2022 Piyush Gupta <gpiyush@vmware.com> 1.3.0-17
- Bump up version to compile with new go
* Thu Aug 18 2022 Piyush Gupta <gpiyush@vmware.com> 1.3.0-16
- Bump up version to compile with new go
* Mon May 09 2022 Piyush Gupta <gpiyush@vmware.com> 1.3.0-15
- Bump up version to compile with new go
* Wed Mar 16 2022 Piyush Gupta <gpiyush@vmware.com> 1.3.0-14
- Bump up version to compile with new go
* Tue Feb 22 2022 Piyush Gupta <gpiyush@vmware.com> 1.3.0-13
- Bump up version to compile with new go
* Mon Jan 24 2022 Piyush Gupta <gpiyush@vmware.com> 1.3.0-12
- Bump up version to compile with new go
* Tue Nov 16 2021 Piyush Gupta <gpiyush@vmware.com> 1.3.0-11
- Bump up version to compile with new go
* Wed Oct 20 2021 Piyush Gupta <gpiyush@vmware.com> 1.3.0-10
- Bump up version to compile with new go
* Sat Aug 21 2021 Piyush Gupta<gpiyush@vmware.com> 1.3.0-9
- Bump up version to compile with new go
* Tue Jun 29 2021 Piyush Gupta <gpiyush@vmware.com> 1.3.0-8
- Bump up version to compile with new go
* Mon May 03 2021 Piyush Gupta<gpiyush@vmware.com> 1.3.0-7
- Bump up version to compile with new go
* Mon Feb 08 2021 Harinadh D <hdommaraju@vmware.com> 1.3.0-6
- Bump up version to compile with new go
* Fri Nov 27 2020 HarinadhD <hdommaraju@vmware.com> 1.3.0-5
- Bump up version to compile with new go
* Fri Apr 10 2020 Harinadh D <hdommaraju@vmware.com> 1.3.0-4
- Bump up version to compile with go 1.13.3-2
* Tue Oct 22 2019 Ashwin H <ashwinh@vmware.com> 1.3.0-3
- Bump up version to compile with go 1.13.3
* Fri Aug 30 2019 Ashwin H <ashwinh@vmware.com> 1.3.0-2
- Bump up version to compile with new go
* Fri Sep 7 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 1.3.0-1
- Bumped up version to 1.3.0
* Fri May 18 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 1.1.1-1
- Bumped up version to 1.1.1
* Mon Aug 28 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.9.0-1
- K8S NGINX Ingress Controller for PhotonOS.
