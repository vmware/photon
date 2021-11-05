Summary:        Kubernetes Dashboard UI
Name:           kubernetes-dashboard
Version:        1.10.1
Release:        11%{?dist}
License:        Apache-2.0
URL:            https://github.com/kubernetes/dashboard
Source0:        %{name}-%{version}.tar.gz
%define sha1    kubernetes-dashboard=ad2d26be3a7d099e0d917f04b873a72945694d58
Source1:        npm-sources-9.9.0.tar.gz
%define sha1    npm-sources=0d50a69bd3a2e0cd637b752d67759755d94ece4c
Source2:        package-lock.json
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
BuildArch:      x86_64
BuildRequires:  gcc
BuildRequires:  git
BuildRequires:  glibc-devel
BuildRequires:  go
BuildRequires:  linux-api-headers
BuildRequires:  nodejs = 9.11.2
BuildRequires:  openjre8
BuildRequires:  which
Requires:       nodejs = 9.11.2
Requires:       openjre8

%description
Kubernetes Dashboard UI.

%prep
%autosetup -n dashboard-%{version}

%build
export PATH=${PATH}:/usr/bin
export GO111MODULE=auto
tar xf %{SOURCE1} --no-same-owner
cp %{SOURCE2} .
#npm install --unsafe-perm
#Remove the lines which strips the debuginfo.
sed -i '/https:\/\/golang.org\/cmd\/link\//,+2d' ./build/backend.js
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
*   Wed Oct 20 2021 Piyush Gupta <gpiyush@vmware.com> 1.10.1-11
-   Bump up version to compile with new go
*   Sat Aug 21 2021 Piyush Gupta<gpiyush@vmware.com> 1.10.1-10
-   Bump up version to compile with new go
*   Tue Jun 29 2021 Piyush Gupta <gpiyush@vmware.com> 1.10.1-9
-   Bump up version to compile with new go
*   Mon May 03 2021 Piyush Gupta<gpiyush@vmware.com> 1.10.1-8
-   Bump up version to compile with new go
*   Mon Feb 08 2021 Harinadh D <hdommaraju@vmware.com> 1.10.1-7
-   Bump up version to compile with new go
*   Fri Nov 27 2020 HarinadhD <hdommaraju@vmware.com> 1.10.1-6
-   Bump up version to compile with new go
*   Tue Aug 18 2020 Ashwin H <ashwinh@vmware.com> 1.10.1-5
-   Bump up version to compile with new go
*   Fri Apr 10 2020 Harinadh D <hdommaraju@vmware.com> 1.10.1-4
-   Bump up version to compile with go 1.13.3-2
*   Tue Oct 22 2019 Ashwin H <ashwinh@vmware.com> 1.10.1-3
-   Bump up version to compile with go 1.13.3
*   Fri Aug 30 2019 Ashwin H <ashwinh@vmware.com> 1.10.1-2
-   Bump up version to compile with new go
*    Wed Jan 23 2019 Keerthana K <keerthanak@vmware.com> 1.10.1-1
-    Updating kubernetes-dashboard to 1.10.1 for security fix
*    Mon Jan 07 2019 Siju Maliakkal <smaliakkal@vmware.com> 1.8.3-4
-    Added nodejs-9.11.2 dependency
*    Mon Oct 22 2018 Ajay Kaher <akaher@vmware.com> 1.8.3-3
-    Adding BuildArch
*    Wed Sep 19 2018 Tapas Kundu <tkundu@vmware.com> 1.8.3-2
-    Using sources instead of doing npm install.
*    Fri May 18 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 1.8.3-1
-    kubernetes-dashboard 1.8.3
*    Tue Apr 03 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 1.6.3-2
-    Fix build break in google-closure-library.
*    Mon Sep 11 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.6.3-1
-    kubernetes-dashboard 1.6.3.
*    Fri Jul 14 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.6.1-1
-    Initial version of kubernetes-dashboard package for Photon.
