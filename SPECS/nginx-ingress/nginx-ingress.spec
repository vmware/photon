Summary:        NGINX Ingress Controller for Kubernetes
Name:           nginx-ingress
Version:        0.9.0
Release:        1%{?dist}
License:        Apache-2.0
URL:            https://github.com/nginxinc/kubernetes-ingress
Source0:        %{name}-%{version}.tar.gz
%define sha1 nginx-ingress=ea71044b1c8298c85cf5f0971100f735f99240ce
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
pushd ${GOPATH}/src/github.com/nginxinc/kubernetes-ingress/nginx-controller
CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -ldflags "-w -X main.version=%{version}" -o nginx-ingress *.go

%install
pushd ${GOPATH}/src/github.com/nginxinc/kubernetes-ingress/nginx-controller
install -vdm 755 %{buildroot}%{_bindir}
install -vpm 0755 -t %{buildroot}%{_bindir} nginx-ingress
install -vdm 0755 %{buildroot}/usr/share/nginx-ingress/docker
install -vpm 0755 -t %{buildroot}/usr/share/nginx-ingress/docker/ nginx/templates/nginx.ingress.tmpl
install -vpm 0755 -t %{buildroot}/usr/share/nginx-ingress/docker/ nginx/templates/nginx.tmpl

%files
%defattr(-,root,root)
%{_bindir}/nginx-ingress
/usr/share/nginx-ingress/docker/nginx.*

%changelog
*   Mon Aug 28 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.9.0-1
-   K8S NGINX Ingress Controller for PhotonOS.
