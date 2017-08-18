Summary:        Kubernetes Dashboard UI
Name:           kubernetes-dashboard
Version:        1.6.1
Release:        2%{?dist}
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
export LD_LIBRARY_PATH=/usr/lib/jvm/OpenJDK-1.8.0.141/jre/lib/amd64/jli/:${LD_LIBRARY_PATH}
npm install
./build/postinstall.sh
./node_modules/.bin/gulp build

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}/opt/k8dashboard
cp -p -r ./dist/amd64/dashboard %{buildroot}%{_bindir}/
cp -p -r ./dist/amd64/locale_conf.json %{buildroot}/opt/k8dashboard/
cp -p -r ./dist/amd64/public %{buildroot}/opt/k8dashboard/
cp -p -r ./src/deploy/Dockerfile %{buildroot}/opt/k8dashboard/

%files
%defattr(-,root,root)
%{_bindir}/dashboard
/opt/k8dashboard/Dockerfile
/opt/k8dashboard/locale_conf.json
/opt/k8dashboard/public/*

%changelog
*    Thu Aug 17 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.6.1-2
-    Set library path to libjli required by java.
*    Fri Jul 14 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.6.1-1
-    Initial version of kubernetes-dashboard package for Photon.
