Summary:        Kubernetes Dashboard UI
Name:           kubernetes-dashboard
Version:        1.10.1
Release:        9%{?dist}
License:        Apache-2.0
URL:            https://github.com/kubernetes/dashboard
Source0:        %{name}-%{version}.tar.gz
%define sha1    kubernetes-dashboard=ad2d26be3a7d099e0d917f04b873a72945694d58
Source1:        roboto-mono.tar.gz
%define sha1    roboto-mono=4544ed04e1aa3249efbcb8e58b957c1a7f6a8ada
Source2:        node_modules-10.15.2.tar.gz
%define sha1    node_modules=9c34ab9208696e0e6464d90d040129e7fe969b12
Patch0:         remove_easyfont_roboto_mono.patch
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  gcc
BuildRequires:  git
BuildRequires:  glibc-devel
BuildRequires:  go
BuildRequires:  linux-api-headers
BuildRequires:  nodejs = 8.17.0
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
tar xf %{SOURCE2} --no-same-owner
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
*   Fri Apr 10 2020 Harinadh D <hdommaraju@vmware.com> 1.10.1-9
-   Bump up version to compile with go 1.13.5-2
*    Wed Feb 12 2020 Siju Maliakkal <smaliakkal@vmware.com> 1.10.1-8
-    To use nodejs-8.17.0
*    Tue Jan 07 2020 Ashwin H <ashwinh@vmware.com> 1.10.1-7
-    Bump up version to compile with new go
*    Wed Oct 09 2019 Tapas Kundu <tkundu@vmware.com> 1.10.1-6
-    Use npm source to build.
*    Fri Aug 30 2019 Ashwin H <ashwinh@vmware.com> 1.10.1-5
-    Bump up version to compile with new go
*    Tue May 07 2019 Ankit Jain <ankitja@vmware.com> 1.10.1-4
-    Dashboard works with Nodejs latest version as well
-    so removed version dependency
*    Thu Apr 25 2019 Ankit Jain <ankitja@vmware.com> 1.10.1-3
-    Added version number to Requires of nodejs
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
