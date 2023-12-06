Summary:        Kubernetes Dashboard UI
Name:           kubernetes-dashboard
Version:        2.7.0
Release:        12%{?dist}
License:        Apache-2.0
URL:            https://github.com/kubernetes/dashboard
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/kubernetes/dashboard/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512 %{name}=bd5567bd5a8163cf13de5b935ce90aafb4acba58acc07740eb1ed22ae761c68a7d160a22cfe3d49a9e700a4139c3cc1bef6a76a1bebd88caabef909cd85607b3
Source1: dashboard-dist-%{version}.v1.tar.gz
%define sha512 dashboard-dist=1ade7bdbdce573027f3e94f1ef0614e04cc72762671d225bb67f22c3b3f0ecbfc83f6744aba179d153c1800611a07348a6cd901d31981f6951f038f806b1cf1d

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
BuildRequires:  openjdk11

Requires:       (openjdk11-jre or openjdk17-jre)
Requires:       nodejs

%description
Kubernetes Dashboard UI.

%prep
%autosetup -p1 -n dashboard-%{version}
# Change the npm default registry to enterprise registry
#sed -i 's#https://registry.npmjs.org#http://<url>#g' *.json
#npm config set registry http://<url>

%build
export PATH=${PATH}:%{_bindir}
# During building, it looks .git/hooks in the root path
# But tar.gz file  from github/kibana/tag doesn't provide .git/hooks
# inside it. so did below steps to create the tar
# 1) git clone git@github.com:kubernetes/dashboard.git dashboard-%{version}
# 2) cd dashboard-%{version}
# 3) git checkout tags/v%{version} -b %{version}
# 4) cd ..
# 5) tar -zcvf kubernetes-dashboard-%{version}.tar.gz dashboard-%{version}

#download npm sources in node_modules
#npm ci --unsafe-perm

#npm run build

tar xf %{SOURCE1} --no-same-owner

%install
mkdir -p %{buildroot}%{_bindir} %{buildroot}/opt/k8dashboard
cp -pr ./dist/amd64/dashboard %{buildroot}%{_bindir}/
cp -pr ./dist/amd64/locale_conf.json ./dist/amd64/public \
          ./dist/amd64/Dockerfile %{buildroot}/opt/k8dashboard/

%files
%defattr(-,root,root)
%{_bindir}/dashboard
/opt/k8dashboard/Dockerfile
/opt/k8dashboard/locale_conf.json
/opt/k8dashboard/public/*

%changelog
* Fri Dec 22 2023 Prashant S Chauhan <psinghchauha@vmware.com> 2.7.0-12
- Bump up as part of nodejs
* Tue Nov 21 2023 Piyush Gupta <gpiyush@vmware.com> 2.7.0-11
- Bump up version to compile with new go
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 2.7.0-10
- Bump up version to compile with new go
* Mon Sep 18 2023 Piyush Gupta <gpiyush@vmware.com> 2.7.0-9
- Bump up version to compile with new go
* Sat Aug 26 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.7.0-8
- Require jdk11 or jdk17
* Mon Jul 17 2023 Piyush Gupta <gpiyush@vmware.com> 2.7.0-7
- Bump up version to compile with new go
* Tue Jun 27 2023 Prashant S Chauhan <psinghchauha@vmware.com> 2.7.0-6
- Compiled with go 1.20.5, Fixes multiple second level CVEs
* Thu Jun 22 2023 Piyush Gupta <gpiyush@vmware.com> 2.7.0-5
- Bump up version to compile with new go
* Sat Jun 17 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.7.0-4
- Bump version as a part of openjdk11 upgrade
* Tue May 23 2023 Shivani Agarwal <shivania2@vmware.com> 2.7.0-3
- Bump up version to compile with new nodejs
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 2.7.0-2
- Bump up version to compile with new go
* Mon Apr 17 2023 Prashant S Chauhan <psinghchauha@vmware.com> 2.7.0-1
- Update to 2.7.0
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
