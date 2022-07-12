Summary:        NGINX Ingress Controller for Kubernetes
Name:           nginx-ingress
Version:        1.8.1
Release:        12%{?dist}
License:        Apache-2.0
URL:            https://github.com/nginxinc/kubernetes-ingress
Source0:        %{name}-%{version}.tar.gz
%define sha512  nginx-ingress=03e5d22c7a7a5b988feb445bd669bb7b22d2bde402e3932da6f1811d12a7e274c3b4da49f22255590bfca96a09ecd480c7c6a31bc0e5288ebc981b88e390edd9
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  go >= 1.7

%description
This is an implementation of kubernetes ingress controller for NGINX.

%prep
%autosetup -n kubernetes-ingress-%{version}

%build
mkdir -p ${GOPATH}/src/github.com/nginxinc/kubernetes-ingress
cp -r * ${GOPATH}/src/github.com/nginxinc/kubernetes-ingress/.
pushd ${GOPATH}/src/github.com/nginxinc/kubernetes-ingress/cmd/nginx-ingress
CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -ldflags "-w -X main.version=%{version}" -o nginx-ingress main.go

%install
pushd ${GOPATH}/src/github.com/nginxinc/kubernetes-ingress/cmd/nginx-ingress
install -vdm 755 %{buildroot}%{_bindir}
install -vpm 0755 -t %{buildroot}%{_bindir} nginx-ingress
install -vdm 0755 %{buildroot}/usr/share/nginx-ingress/docker
install -vpm 0755 -t %{buildroot}/usr/share/nginx-ingress/docker/ ../../internal/configs/version1/nginx.ingress.tmpl
install -vpm 0755 -t %{buildroot}/usr/share/nginx-ingress/docker/ ../../internal/configs/version1/nginx.tmpl
install -vpm 0755 -t %{buildroot}/usr/share/nginx-ingress/docker/ ../../internal/configs/version2/nginx.virtualserver.tmpl
install -vpm 0755 -t %{buildroot}/usr/share/nginx-ingress/docker/ ../../internal/configs/version2/nginx.transportserver.tmpl

%files
%defattr(-,root,root)
%{_bindir}/nginx-ingress
/usr/share/nginx-ingress/docker/nginx.*

%changelog
* Tue Jul 12 2022 Piyush Gupta <gpiyush@vmware.com> 1.8.1-12
- Bump up version to compile with new go
*   Sat May 07 2022 Piyush Gupta <gpiyush@vmware.com> 1.8.1-11
-   Bump up version to compile with new go
*   Tue Feb 22 2022 Piyush Gupta <gpiyush@vmware.com> 1.8.1-10
-   Bump up version to compile with new go
*   Mon Jan 24 2022 Piyush Gupta <gpiyush@vmware.com> 1.8.1-9
-   Bump up version to compile with new go
*   Wed Oct 20 2021 Piyush Gupta <gpiyush@vmware.com> 1.8.1-8
-   Bump up version to compile with new go
*   Tue Oct 05 2021 Piyush Gupta <gpiyush@vmware.com> 1.8.1-7
-   Bump up version to compile with new go
*   Fri Jun 11 2021 Piyush Gupta <gpiyush@vmware.com> 1.8.1-6
-   Bump up version to compile with new go
*   Thu Mar 25 2021 Piyush Gupta<gpiyush@vmware.com> 1.8.1-5
-   Bump up version to compile with new go
*   Fri Feb 05 2021 Harinadh D <hdommaraju@vmware.com> 1.8.1-4
-   Bump up version to compile with new go
*   Fri Jan 15 2021 Piyush Gupta<gpiyush@vmware.com> 1.8.1-3
-   Bump up version to compile with new go
*   Sun Nov 01 2020 Prashant S Chauhan <psinghchauha@vmware.com> 1.8.1-2
-   Added missing nginx.virtualserver.tmpl file
*   Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 1.8.1-1
-   Automatic Version Bump
*   Fri Sep 7 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 1.3.0-1
-   Bumped up version to 1.3.0
*   Fri May 18 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 1.1.1-1
-   Bumped up version to 1.1.1
*   Mon Aug 28 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.9.0-1
-   K8S NGINX Ingress Controller for PhotonOS.
