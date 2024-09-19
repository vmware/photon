%define network_required 1
%global debug_package %{nil}

Summary:        NGINX Ingress Controller for Kubernetes
Name:           nginx-ingress
Version:        2.4.2
Release:        12%{?dist}
License:        Apache-2.0
URL:            https://github.com/nginxinc/kubernetes-ingress
Source0:        https://github.com/nginxinc/kubernetes-ingress/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512  nginx-ingress=1d2415b73afab9c3338e2cfa717bae6e12f7bbd98f8a20606e274b09c3e4724e56fff0acdc261215ca95107e175489fef4aba9df6e3f9cb5b72d9f98859ae7d9
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
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
* Thu Sep 19 2024 Mukul Sikka <mukul.sikka@broadcom.com> 2.4.2-12
- Bump version as a part of go upgrade
* Fri Jul 12 2024 Mukul Sikka <mukul.sikka@broadcom.com> 2.4.2-11
- Bump version as a part of go upgrade
* Thu Jun 20 2024 Mukul Sikka <msikka@vmware.com> 2.4.2-10
- Bump version as a part of go upgrade
* Thu Feb 22 2024 Mukul Sikka <msikka@vmware.com> 2.4.2-9
- Bump version as a part of go upgrade
* Tue Nov 21 2023 Piyush Gupta <gpiyush@vmware.com> 2.4.2-8
- Bump up version to compile with new go
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 2.4.2-7
- Bump up version to compile with new go
* Mon Sep 18 2023 Piyush Gupta <gpiyush@vmware.com> 2.4.2-6
- Bump up version to compile with new go
* Mon Jul 17 2023 Piyush Gupta <gpiyush@vmware.com> 2.4.2-5
- Bump up version to compile with new go
* Thu Jun 22 2023 Piyush Gupta <gpiyush@vmware.com> 2.4.2-4
- Bump up version to compile with new go
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 2.4.2-3
- Bump up version to compile with new go
* Thu Mar 09 2023 Piyush Gupta <gpiyush@vmware.com> 2.4.2-2
- Bump up version to compile with new go
* Tue Dec 13 2022 Gerrit Photon <photon-checkins@vmware.com> 2.4.2-1
- Automatic Version Bump
* Mon Nov 21 2022 Piyush Gupta <gpiyush@vmware.com> 2.3.0-3
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 2.3.0-2
- Bump up version to compile with new go
* Mon Aug 08 2022 Harinadh D <hdommaraju@vmware.com> 2.3.0-1
- Version update
* Fri Jun 17 2022 Piyush Gupta <gpiyush@vmware.com> 1.11.1-3
- Bump up version to compile with new go
* Fri Jun 11 2021 Piyush Gupta<gpiyush@vmware.com> 1.11.1-2
- Bump up version to compile with new go
* Thu Apr 29 2021 Gerrit Photon <photon-checkins@vmware.com> 1.11.1-1
- Automatic Version Bump
* Fri Feb 05 2021 Harinadh D <hdommaraju@vmware.com> 1.8.1-4
- Bump up version to compile with new go
* Fri Jan 15 2021 Piyush Gupta<gpiyush@vmware.com> 1.8.1-3
- Bump up version to compile with new go
* Sun Nov 01 2020 Prashant S Chauhan <psinghchauha@vmware.com> 1.8.1-2
- Added missing nginx.virtualserver.tmpl file
* Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 1.8.1-1
- Automatic Version Bump
* Fri Sep 7 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 1.3.0-1
- Bumped up version to 1.3.0
* Fri May 18 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 1.1.1-1
- Bumped up version to 1.1.1
* Mon Aug 28 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.9.0-1
- K8S NGINX Ingress Controller for PhotonOS.
