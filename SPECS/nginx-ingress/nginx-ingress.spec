%global debug_package %{nil}

Summary:        NGINX Ingress Controller for Kubernetes
Name:           nginx-ingress
Version:        2.3.0
Release:        12%{?dist}
License:        Apache-2.0
URL:            https://github.com/nginxinc/kubernetes-ingress
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/nginxinc/kubernetes-ingress/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512  %{name}=fd2877490c5fe3eba1946af9c4d675c60f7944bd0535f3e35814af3f3f4ccf2c935da22e32392a0f16c2d7cfb9902e1cfce3753a90ee603b3936e614bec706ee

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
* Tue Nov 21 2023 Piyush Gupta <gpiyush@vmware.com> 2.3.0-12
- Bump up version to compile with new go
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 2.3.0-11
- Bump up version to compile with new go
* Fri Aug 18 2023 Piyush Gupta <gpiyush@vmware.com> 2.3.0-10
- Bump up version to compile with new go
* Tue Jun 20 2023 Piyush Gupta <gpiyush@vmware.com> 2.3.0-9
- Bump up version to compile with new go
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 2.3.0-8
- Bump up version to compile with new go
* Thu Mar 16 2023 Piyush Gupta <gpiyush@vmware.com> 2.3.0-7
- Bump up version to compile with new go
* Tue Dec 20 2022 Piyush Gupta <gpiyush@vmware.com> 2.3.0-6
- Bump up version to compile with new go
* Sun Nov 13 2022 Piyush Gupta <gpiyush@vmware.com> 2.3.0-5
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 2.3.0-4
- Bump up version to compile with new go
* Thu Sep 15 2022 Piyush Gupta <gpiyush@vmware.com> 2.3.0-3
- Bump up version to compile with new go
* Fri Aug 19 2022 Piyush Gupta <gpiyush@vmware.com> 2.3.0-2
- Bump up version to compile with new go
* Mon Aug 08 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.3.0-1
- Version update
* Tue Jul 12 2022 Piyush Gupta <gpiyush@vmware.com> 1.8.1-12
- Bump up version to compile with new go
* Sat May 07 2022 Piyush Gupta <gpiyush@vmware.com> 1.8.1-11
- Bump up version to compile with new go
* Tue Feb 22 2022 Piyush Gupta <gpiyush@vmware.com> 1.8.1-10
- Bump up version to compile with new go
* Mon Jan 24 2022 Piyush Gupta <gpiyush@vmware.com> 1.8.1-9
- Bump up version to compile with new go
* Wed Oct 20 2021 Piyush Gupta <gpiyush@vmware.com> 1.8.1-8
- Bump up version to compile with new go
* Tue Oct 05 2021 Piyush Gupta <gpiyush@vmware.com> 1.8.1-7
- Bump up version to compile with new go
* Fri Jun 11 2021 Piyush Gupta <gpiyush@vmware.com> 1.8.1-6
- Bump up version to compile with new go
* Thu Mar 25 2021 Piyush Gupta<gpiyush@vmware.com> 1.8.1-5
- Bump up version to compile with new go
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
