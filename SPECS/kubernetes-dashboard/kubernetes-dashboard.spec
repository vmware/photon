Summary:        Kubernetes Dashboard UI
Name:           kubernetes-dashboard
Version:        2.3.1
Release:        12%{?dist}
License:        Apache-2.0
URL:            https://github.com/kubernetes/dashboard
Source0:        %{name}-%{version}.tar.gz
%define sha512  kubernetes-dashboard=806ca363c4d99b638216e9833e99849bafe60be90c5804627acb2ef18bcea7419c5a0cdb8135e1652ce3dd3a58df7c53e9d7f08b3fa5c5287e890b59ef5767f4
Source1:        dashboard-dist-%{version}.tar.gz
%define sha512  dashboard-dist=662715400fb64d661beedcd69ee84119345c10339d401976e9652dcb86a0df9cb0f95de6d13c58783ecbc9523af61eabcc2d8329db3a621a2a9b48c5cd702341
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
%autosetup -p1 -n dashboard-%{version}
# Change the npm default registry to enterprise registry
#sed -i 's#https://registry.npmjs.org#http://<url>#g' *.json
#npm config set registry http://<url>

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
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 2.3.1-12
- Bump up version to compile with new go
* Tue Oct 11 2022 Shivani Agarwal <shivania2@vmware.com> 2.3.1-11
- Bump up version to compile with nodejs-18.10.0
* Thu Sep 15 2022 Piyush Gupta <gpiyush@vmware.com> 2.3.1-10
- Bump up version to compile with new go
* Fri Aug 19 2022 Piyush Gupta <gpiyush@vmware.com> 2.3.1-9
- Bump up version to compile with new go
* Tue Aug 09 2022 Shivani Agarwal <shivania2@vmware.com> 2.3.1-8
- Bump up version to compile with nodejs-18.6.0
* Tue Jul 12 2022 Piyush Gupta <gpiyush@vmware.com> 2.3.1-7
- Bump up version to compile with new go
* Sat May 07 2022 Piyush Gupta <gpiyush@vmware.com> 2.3.1-6
- Bump up version to compile with new go
* Tue Feb 22 2022 Piyush Gupta <gpiyush@vmware.com> 2.3.1-5
- Bump up version to compile with new go
* Mon Jan 24 2022 Piyush Gupta <gpiyush@vmware.com> 2.3.1-4
- Bump up version to compile with new go
* Wed Oct 20 2021 Piyush Gupta <gpiyush@vmware.com> 2.3.1-3
- Bump up version to compile with new go
* Sun Aug 29 2021 Piyush Gupta <gpiyush@vmware.com> 2.3.1-2
- Bump up version to compile with new go
* Thu Aug 26 2021 Ankit Jain <ankitja@vmware.com> 2.3.1-1
- Update to 2.3.1
* Fri Jun 11 2021 Piyush Gupta <gpiyush@vmware.com> 2.0.3-6
- Bump up version to compile with new go
* Thu Mar 25 2021 Piyush Gupta<gpiyush@vmware.com> 2.0.3-5
- Bump up version to compile with new go
* Thu Mar 18 2021 Piyush Gupta <gpiyush@vmware.com> 2.0.3-4
- Bump up internal version with new nodejs
* Fri Feb 05 2021 Harinadh D <hdommaraju@vmware.com> 2.0.3-3
- Bump up version to compile with new go
* Fri Jan 15 2021 Piyush Gupta<gpiyush@vmware.com> 2.0.3-2
- Bump up version to compile with new go
* Mon Jul 06 2020 Tapas Kundu <tkundu@vmware.com> 2.0.3-1
- Build with latest nodejs
* Wed Jan 23 2019 Keerthana K <keerthanak@vmware.com> 1.10.1-1
- Updating kubernetes-dashboard to 1.10.1 for security fix
* Mon Jan 07 2019 Siju Maliakkal <smaliakkal@vmware.com> 1.8.3-4
- Added nodejs-9.11.2 dependency
* Mon Oct 22 2018 Ajay Kaher <akaher@vmware.com> 1.8.3-3
- Adding BuildArch
* Wed Sep 19 2018 Tapas Kundu <tkundu@vmware.com> 1.8.3-2
- Using sources instead of doing npm install.
* Fri May 18 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 1.8.3-1
- kubernetes-dashboard 1.8.3
* Tue Apr 03 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 1.6.3-2
- Fix build break in google-closure-library.
* Mon Sep 11 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.6.3-1
- kubernetes-dashboard 1.6.3.
* Fri Jul 14 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.6.1-1
- Initial version of kubernetes-dashboard package for Photon.
