Summary:        Kubernetes Dashboard UI
Name:           kubernetes-dashboard
Version:        1.10.1
Release:        2%{?dist}
License:        Apache-2.0
URL:            https://github.com/kubernetes/dashboard
Source0:        %{name}-%{version}.tar.gz
%define sha1    kubernetes-dashboard=ad2d26be3a7d099e0d917f04b873a72945694d58
Source1:        roboto-mono.tar.gz
%define sha1    roboto-mono=4544ed04e1aa3249efbcb8e58b957c1a7f6a8ada
Patch0:         remove_easyfont_roboto_mono.patch
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  gcc
BuildRequires:  git
BuildRequires:  glibc-devel
BuildRequires:  go
BuildRequires:  linux-api-headers
BuildRequires:  nodejs
BuildRequires:  openjre8
BuildRequires:  which
Requires:       nodejs
Requires:       openjre8

%description
Kubernetes Dashboard UI.

%prep
%setup -q -n dashboard-%{version}
%patch0 -p0

%build
export PATH=${PATH}:/usr/bin
npm install --unsafe-perm
#Remove the lines which strips the debuginfo. 
sed -i '/https:\/\/golang.org\/cmd\/link\//,+2d' ./build/backend.js
cp -r %{SOURCE1} ./node_modules/easyfont-roboto-mono
./node_modules/.bin/gulp build

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}/opt/k8dashboard
cp -p -r ./dist/amd64/dashboard %{buildroot}%{_bindir}/
cp -p -r ./dist/amd64/locale_conf.json %{buildroot}/opt/k8dashboard/
cp -p -r ./dist/amd64/public %{buildroot}/opt/k8dashboard/
cp -p -r ./src/deploy/Dockerfile %{buildroot}/opt/k8dashboard/

%check
# dashboard unit tests require chrome browser binary not present in PhotonOS

%files
%defattr(-,root,root)
%{_bindir}/dashboard
/opt/k8dashboard/Dockerfile
/opt/k8dashboard/locale_conf.json
/opt/k8dashboard/public/*

%changelog
*    Wed Apr 17 2019 Michelle Wang <michellew@vmware.com> 1.10.1-2
-    Convert roboto-mono into a source
-    due to source code not available on github
*    Mon Jan 07 2019 Girish Sadhani <gsadhani@vmware.com> 1.10.1-1
-    Updating kubernetes-dashboard to 1.10.1 for security fix
*    Tue Apr 17 2018 Dheeraj Shetty <dheerajs@vmware.com> 1.8.3-2
-    Fix build issue
*    Tue Mar 13 2018 Dheeraj Shetty <dheerajs@vmware.com> 1.8.3-1
-    kubernetes-dashboard 1.8.3.
*    Mon Sep 11 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.6.3-1
-    kubernetes-dashboard 1.6.3.
*    Fri Jul 14 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.6.1-1
-    Initial version of kubernetes-dashboard package for Photon.
