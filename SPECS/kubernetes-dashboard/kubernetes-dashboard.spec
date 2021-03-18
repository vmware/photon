Summary:        Kubernetes Dashboard UI
Name:           kubernetes-dashboard
Version:        2.0.3
Release:        4%{?dist}
License:        Apache-2.0
URL:            https://github.com/kubernetes/dashboard
Source0:        %{name}-%{version}.tar.gz
%define sha1    kubernetes-dashboard=267597cdd64fb20b4aa66e890349b79230e31154
Source1:        dashboard-dist-%{version}.tar.gz
%define sha1    dashboard-dist=f4ac3b53dd1053abeb94836ad3083bc6de3b9f4e
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
BuildArch:      x86_64
BuildRequires:  gcc
BuildRequires:  git
BuildRequires:  glibc-devel
BuildRequires:  go
BuildRequires:  linux-api-headers
BuildRequires:  nodejs
BuildRequires:  openjre8
BuildRequires:  which
BuildRequires:  ncurses-terminfo
BuildRequires:  bc
Requires:       nodejs
Requires:       openjre8

%description
Kubernetes Dashboard UI.

%prep
%setup -q -n dashboard-%{version}

%build
export PATH=${PATH}:/usr/bin
# During building, it looks .git/hooks in the root path
# But tar.gz file  from github/kibana/tag doesn't provide .git/hooks
# inside it. so did below steps to create the tar
# 1) git clone git@github.com:kubernetes/dashboard.git dashboard-%{version}
# 2) cd dashboard-%{version}
# 3) git checkout tags/v2.0.3 -b 2.0.3
# 4) cd ..
# 5) tar -zcvf kubernetes-dashboard-2.0.3.tar.gz dashboard-%{version}

#download npm sources in node_modules
#npm ci --unsafe-perm

#npm run build

tar xf %{SOURCE1} --no-same-owner

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}/opt/k8dashboard
cp -p -r ./dist/amd64/dashboard %{buildroot}%{_bindir}/
cp -p -r ./dist/amd64/locale_conf.json %{buildroot}/opt/k8dashboard/
cp -p -r ./dist/amd64/public %{buildroot}/opt/k8dashboard/
cp -p -r ./dist/amd64/Dockerfile %{buildroot}/opt/k8dashboard/

%check
# dashboard unit tests require chrome browser binary not present in PhotonOS

%files
%defattr(-,root,root)
%{_bindir}/dashboard
/opt/k8dashboard/Dockerfile
/opt/k8dashboard/locale_conf.json
/opt/k8dashboard/public/*

%changelog
*    Thu Mar 18 2021 Piyush Gupta <gpiyush@vmware.com> 2.0.3-4
-    Bump up internal version with new nodejs
*    Fri Feb 05 2021 Harinadh D <hdommaraju@vmware.com> 2.0.3-3
-    Bump up version to compile with new go
*    Fri Jan 15 2021 Piyush Gupta<gpiyush@vmware.com> 2.0.3-2
-    Bump up version to compile with new go
*    Mon Jul 06 2020 Tapas Kundu <tkundu@vmware.com> 2.0.3-1
-    Build with latest nodejs
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
