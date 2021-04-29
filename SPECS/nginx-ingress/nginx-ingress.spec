Summary:        NGINX Ingress Controller for Kubernetes
Name:           nginx-ingress
Version:        1.11.1
Release:        1%{?dist}
License:        Apache-2.0
URL:            https://github.com/nginxinc/kubernetes-ingress
Source0:        %{name}-%{version}.tar.gz
%define sha1 nginx-ingress=c54bc93f8992a712a4c402cc43775a743694fce3
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  go >= 1.7

%description
This is an implementation of kubernetes ingress controller for NGINX.

%prep
%setup -n kubernetes-ingress-%{version}

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
*   Thu Apr 29 2021 Gerrit Photon <photon-checkins@vmware.com> 1.11.1-1
-   Automatic Version Bump
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
