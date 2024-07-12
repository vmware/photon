Summary:        Kubernetes Dashboard UI
Name:           kubernetes-dashboard
Version:        2.7.0
Release:        13%{?dist}
License:        Apache-2.0
URL:            https://github.com/kubernetes/dashboard
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: %{name}-%{version}.tar.gz
%define sha512 %{name}=bd5567bd5a8163cf13de5b935ce90aafb4acba58acc07740eb1ed22ae761c68a7d160a22cfe3d49a9e700a4139c3cc1bef6a76a1bebd88caabef909cd85607b3

Source1: dashboard-dist-%{version}.tar.gz
%define sha512 dashboard-dist=e31051bef71d85f553bd26af94bd698d3e417f596d9a1bfe46aafee175c5ccaf8e1fb754364672b395444c0a67cd24392f2f3aee99b3e3fd9ec325b8dc21c7d0

BuildArch:      x86_64

BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  go
BuildRequires:  linux-api-headers
BuildRequires:  nodejs
BuildRequires:  which
BuildRequires:  ncurses-terminfo
BuildRequires:  bc
BuildRequires:  openjdk8

Requires:       nodejs
Requires: (openjre8 or openjdk11-jre or openjdk17-jre)

%description
Kubernetes Dashboard UI.

%prep
%autosetup -p1 -n dashboard-%{version} -a1
# Change the npm default registry to enterprise registry
#sed -i 's#https://registry.npmjs.org#http://<url>#g' *.json
#npm config set registry http://<url>

%build
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

%install
mkdir -p %{buildroot}%{_bindir} \
          %{buildroot}/opt/k8dashboard

pushd ./dist/amd64/
cp -pr dashboard %{buildroot}%{_bindir}/
cp -pr locale_conf.json public Dockerfile %{buildroot}/opt/k8dashboard/
popd

%files
%defattr(-,root,root)
%{_bindir}/dashboard
/opt/k8dashboard/Dockerfile
/opt/k8dashboard/locale_conf.json
/opt/k8dashboard/public/*

%changelog
* Tue Jul 16 2024 Mukul Sikka <mukul.sikka@broadcom.com> 2.7.0-13
- Bump version as a part of go upgrade
* Mon Jul 15 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 2.7.0-12
- Bump version as a part of nodejs upgrade
* Thu Jun 20 2024 Mukul Sikka <msikka@vmware.com> 2.7.0-11
- Bump version as a part of go upgrade
* Wed Jun 19 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 2.7.0-10
- Bump version as a part of nodejs upgrade
* Thu Apr 18 2024 Mukul Sikka <msikka@vmware.com> 2.7.0-9
- Bump version as a part of go upgrade
* Tue Apr 02 2024 Mukul Sikka <mukul.sikka@broadcom.com> 2.7.0-8
- Bump version as a part of openjdk8 upgrade
* Tue Mar 26 2024 Anmol Jain <anmol.jain@broadcom.com> 2.7.0-7
- Bump version as a part of nodejs upgrade
* Sat Dec 23 2023 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 2.7.0-6
- Fix dist shasum
* Tue Nov 21 2023 Piyush Gupta <gpiyush@vmware.com> 2.7.0-5
- Bump up version to compile with new go
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 2.7.0-4
- Bump up version to compile with new go
* Tue Sep 12 2023 Piyush Gupta <gpiyush@vmware.com> 2.7.0-3
- Bump up version to compile with new go
* Fri Sep 08 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.7.0-2
- Require jre8 or jdk11-jre or jdk17-jre
* Tue Jun 27 2023 Prashant S Chauhan <psinghchauha@vmware.com> 2.7.0-1
- Update to 2.7.0, Fixes multiple second level CVE
* Tue Jun 20 2023 Piyush Gupta <gpiyush@vmware.com> 2.3.1-17
- Bump up version to compile with new go
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 2.3.1-16
- Bump up version to compile with new go
* Thu Mar 16 2023 Piyush Gupta <gpiyush@vmware.com> 2.3.1-15
- Bump up version to compile with new go
* Tue Dec 20 2022 Piyush Gupta <gpiyush@vmware.com> 2.3.1-14
- Bump up version to compile with new go
* Sun Nov 13 2022 Piyush Gupta <gpiyush@vmware.com> 2.3.1-13
- Bump up version to compile with new go
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
