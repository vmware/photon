Summary:        Kubernetes Dashboard UI
Name:           kubernetes-dashboard
Version:        1.6.1
Release:        1%{?dist}
License:        Apache-2.0
URL:            https://github.com/kubernetes/dashboard
Source0:        %{name}-v%{version}.tar.gz
%define sha1    kubernetes-dashboard=8342a3a217388f46103d1082d5fe14b85ffc5644
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  gcc
BuildRequires:  git
BuildRequires:  glibc-devel
BuildRequires:  go
BuildRequires:  linux-api-headers
BuildRequires:  nodejs
BuildRequires:  nodejs
BuildRequires:  openjdk
BuildRequires:  openjre
BuildRequires:  which
Requires:       nodejs
Requires:       openjre

%description
Kubernetes Dashboard UI.

%prep
%setup -q -n dashboard-%{version}

%build
export PATH=${PATH}:/usr/bin
npm install
./build/postinstall.sh
./node_modules/.bin/gulp build

%install
mkdir -p %{buildroot}/k8dash
cp -p -r ./dist/amd64/* %{buildroot}/k8dash/
cp -p -r ./src/deploy/Dockerfile %{buildroot}/k8dash/

%files
%defattr(-,root,root)
/k8dash/dashboard
/k8dash/Dockerfile
/k8dash/locale_conf.json
/k8dash/public/*

%changelog
*    Fri Jul 14 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.6.1-1
-    Initial version of kubernetes-dashboard package for Photon.
