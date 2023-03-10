Summary:        Kubernetes Dashboard UI
Name:           kubernetes-dashboard
Version:        2.0.3
Release:        10%{?dist}
License:        Apache-2.0
URL:            https://github.com/kubernetes/dashboard
Source0:        https://github.com/kubernetes/dashboard/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512  %{name}=8f2bb1aac9f78f9d9fb3388d3b89a1e24743e9c811a6ca95da3c199f954b157f85c896b9d6896b205f560ffef940269ebd5a9457e5e7a270d23b024b849e6210
Source1:        dashboard-dist-%{version}.tar.gz
%define sha512  dashboard-dist=e1d126b59f8ababe6506a1ed7d3b36c5e09cd6cdc6e7a846c95db03680461dbfe033229c59020fbc67c921314d71b8e44aa283a0faaa04bb5687985a94bdb59c
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
BuildRequires:  openjdk11
BuildRequires:  which
BuildRequires:  ncurses-terminfo
BuildRequires:  bc
Requires:       nodejs
Requires:       openjdk11

%description
Kubernetes Dashboard UI.

%prep
%autosetup -p1 -n dashboard-%{version}

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
mkdir -p %{buildroot}%{_bindir}  %{buildroot}/opt/k8dashboard
cp -p -r ./dist/amd64/dashboard %{buildroot}%{_bindir}/
cp -p -r ./dist/amd64/locale_conf.json ./dist/amd64/public \
          ./dist/amd64/Dockerfile %{buildroot}/opt/k8dashboard/

%check
# dashboard unit tests require chrome browser binary not present in PhotonOS

%files
%defattr(-,root,root)
%{_bindir}/dashboard
/opt/k8dashboard/Dockerfile
/opt/k8dashboard/locale_conf.json
/opt/k8dashboard/public/*

%changelog
* Thu Mar 09 2023 Piyush Gupta <gpiyush@vmware.com> 2.0.3-10
- Bump up version to compile with new go
* Mon Nov 21 2022 Piyush Gupta <gpiyush@vmware.com> 2.0.3-9
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 2.0.3-8
- Bump up version to compile with new go
* Wed Sep 21 2022 Vamsi Krishna Brahmajosuyula <vbrahmajosyula@vmware.com> 2.0.3-7
- Use openjdk11
* Fri Jun 17 2022 Piyush Gupta <gpiyush@vmware.com> 2.0.3-6
- Bump up version to compile with new go
* Fri Jun 11 2021 Piyush Gupta<gpiyush@vmware.com> 2.0.3-5
- Bump up version to compile with new go
* Thu Mar 18 2021 Piyush Gupta <gpiyush@vmware.com> 2.0.3-4
- Bump up internal version with new nodejs.
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
