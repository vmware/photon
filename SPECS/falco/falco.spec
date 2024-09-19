%global security_hardening none

Summary:        The Behavioral Activity Monitor With Container Support
Name:           falco
Version:        0.35.0
Release:        11%{?kernelsubrelease}%{?dist}
License:        GPLv2
URL:            https://github.com/falcosecurity/%{name}/archive/refs/tags/%{version}.tar.gz
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/falcosecurity/falco/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512 %{name}=16c76d5d6013ae67a4d103248d9ac910f92d906d1565cd7043c94e4b1deee05db6be0e98aa23b90b45e12adc59c4e59d4c8a9e46e22c1738a3dee597dbe28011

Patch0:         build-Distinguish-yamlcpp-in-USE_BUNDLED-macro.patch
Patch1:         0001-build-plugins-locally.patch
Patch2:         0002-falcoctl-build-locally.patch

BuildArch:      x86_64

BuildRequires:  cmake
BuildRequires:  openssl-devel
BuildRequires:  curl-devel
BuildRequires:  zlib-devel
BuildRequires:  ncurses-devel
BuildRequires:  linux-devel = %{KERNEL_VERSION}-%{KERNEL_RELEASE}
BuildRequires:  jq-devel
BuildRequires:  git
BuildRequires:  lua-devel
BuildRequires:  libyaml-devel
BuildRequires:  linux-api-headers
BuildRequires:  wget
BuildRequires:  which
BuildRequires:  grpc-devel
BuildRequires:  c-ares-devel
BuildRequires:  protobuf-devel
BuildRequires:  go

Requires:       linux = %{KERNEL_VERSION}-%{KERNEL_RELEASE}
Requires:       zlib
Requires:       ncurses
Requires:       openssl
Requires:       curl
Requires:       libyaml
Requires:       lua
Requires:       sysdig
Requires:       dkms
Requires:       grpc
Requires:       jq
Requires:       protobuf
Requires:       c-ares

%define uname_r %{KERNEL_VERSION}-%{KERNEL_RELEASE}
%define _modulesdir /lib/modules/%{uname_r}

%description
Sysdig falco is an open source, behavioral activity monitor designed to detect anomalous activity in your applications. Falco lets you continuously monitor and detect container, application, host, and network activity... all in one place, from one source of data, with one set of customizable rules.

%prep
%autosetup -p1

%build
%cmake \
    -DCMAKE_BUILD_TYPE=Debug \
    -DUSE_BUNDLED_DEPS:BOOL=OFF \
    -DUSE_BUNDLED_OPENSSL:BOOL=OFF \
    -DUSE_BUNDLED_JQ:BOOL=OFF \
    -DUSE_BUNDLED_YAMLCPP:BOOL=ON \
    -DBUILD_SHARED_LIBS:BOOL=OFF \
    -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
    -DCMAKE_INSTALL_SYSCONFDIR=%{_sysconfdir}

export KERNELDIR="%{_modulesdir}/build"
%{cmake_build}

%install
export KERNELDIR="%{_modulesdir}/build"
%{cmake_install}
mkdir -p %{buildroot}%{_modulesdir}/extra
install -vm 644 %{__cmake_builddir}/driver/%{name}.ko %{buildroot}%{_modulesdir}/extra

%post
/sbin/depmod -a

%postun
/sbin/depmod -a

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/*
%exclude %{_usrsrc}
%exclude %{_includedir}
%exclude %{_libdir}/{falcosecurity,pkgconfig}
%{_sysconfdir}/falco
%{_sysconfdir}/falcoctl
%{_datadir}/falco
%{_modulesdir}/extra/falco.ko

%changelog
* Thu Sep 19 2024 Mukul Sikka <mukul.sikka@broadcom.com> 0.35.0-11
- Bump version as a part of go upgrade
* Fri Jul 12 2024 Mukul Sikka <mukul.sikka@broadcom.com> 0.35.0-10
- Bump version as a part of go upgrade
* Thu Jun 20 2024 Mukul Sikka <msikka@vmware.com> 0.35.0-9
- Bump version as a part of go upgrade
* Thu Apr 18 2024 Mukul Sikka <msikka@vmware.com> 0.35.0-8
- Bump version as a part of go upgrade
* Tue Nov 21 2023 Piyush Gupta <gpiyush@vmware.com> 0.35.0-7
- Bump up version to compile with new go
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 0.35.0-6
- Bump up version to compile with new go
* Fri Aug 18 2023 Piyush Gupta <gpiyush@vmware.com> 0.35.0-5
- Bump up version to compile with new go
* Fri Jul 07 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 0.35.0-4
- Build all Go components locally
* Wed Jun 28 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.35.0-3
- Bump version as a part of sysdig upgrade
* Fri Jun 16 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.35.0-2
- Bump version as a part of protobuf upgrade
* Tue Jun 13 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 0.35.0-1
- Update to 0.35.0
* Wed Mar 15 2023 Anmol Jain <anmolja@vmware.com> 0.30.0-3
- Version bump up to use c-ares
* Mon Mar 28 2022 Harinadh D <hdommaraju@vmware.com> 0.30.0-2
- version bump to build with protobuf 3.19.4
* Tue Nov 23 2021 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 0.30.0-1
- Update to version 0.30.0.
- Add missing runtime dependency on linux.
* Wed Aug 04 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 0.25.0-6
- compile with openssl 3.0.0
* Tue Aug 03 2021 Nitesh Kumar <kunitesh@vmware.com> 0.25.0-5
- Patched for CVE-2021-33505.
* Tue Mar 23 2021 Piyush Gupta <gpiyush@vmware.com> 0.25.0-4
- Internal version bump up in order to compile with new lua.
* Fri Feb 19 2021 Harinadh D <hdommaraju@vmware.com> 0.25.0-3
- Version bump up to build with latest protobuf
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 0.25.0-2
- openssl 1.1.1
* Wed Sep 16 2020 Bo Gan <ganb@vmware.com> 0.25.0-1
- Updated to 0.25.0
* Mon Sep 14 2020 Ankit Jain <ankitja@vmware.com> 0.15.1-2
- Fix build failure with grpc in patch
* Wed Jun 26 2019 Harinadh Dommaraju <hdommaraju@vmware.com> 0.15.1-1
- Updated to fix CVE-2019-8339
* Wed Dec 12 2018 Sujay G <gsujay@vmware.com> 0.12.1-4
- Disabled bundled JQ, openssl and instead use Photon maintained packages.
* Wed Oct 24 2018 Ajay Kaher <akaher@vmware.com> 0.12.1-3
- Adding BuildArch
* Wed Oct 24 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 0.12.1-2
- Add depmod for falco-probe.ko and removed patch from new falco-probe-loader
* Mon Sep 24 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 0.12.1-1
- Update falco and sysdig versions to fix build error with linux 4.18
* Tue Jan 02 2018 Alexey Makhalov <amakhalov@vmware.com> 0.8.1-1
- Version update to build against linux-4.14.y kernel
* Thu Aug 24 2017 Rui Gu <ruig@vmware.com> 0.6.0-3
- Disable check section (Bug 1900272).
* Thu May 11 2017 Chang Lee <changlee@vmware.com> 0.6.0-2
- Add falco-probe.ko and change falco-probe.ko path in falco-probe-loader
* Mon Apr 03 2017 Chang Lee <changlee@vmware.com> 0.6.0-1
- Update to version 0.6.0
* Wed Jan 11 2017 Alexey Makhalov <amakhalov@vmware.com> 0.2.0-7
- Fix building for linux-4.9.2
* Mon Dec 19 2016 Xiaolin Li <xiaolinl@vmware.com> 0.2.0-6
- BuildRequires curl-devel
* Thu Dec 15 2016 Alexey Makhalov <amakhalov@vmware.com> 0.2.0-5
- Fix building for linux-4.9
* Wed Nov 30 2016 Alexey Makhalov <amakhalov@vmware.com> 0.2.0-4
- Expand uname -r to have release number
- Exclude /usr/src
* Fri Sep  2 2016 Alexey Makhalov <amakhalov@vmware.com> 0.2.0-3
- Use KERNEL_VERSION macro
* Wed Jul 27 2016 Divya Thaluru <dthaluru@vmware.com> 0.2.0-2
- Removed packaging of debug files
* Tue Jun 28 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 0.2.0-1
- Initial build. First version
