%global security_hardening none

Summary:        The Behavioral Activity Monitor With Container Support
Name:           falco
Version:        0.31.1
Release:        10%{?kernelsubrelease}%{?dist}
License:        GPLv2
URL:            https://github.com/falcosecurity/%{name}/archive/refs/tags/%{version}.tar.gz
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/falcosecurity/falco/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512 %{name}=9b4a50b47d703ba05bf2e91f1b9a3e88c22380bc70b35338fa9735c5c48645fb714c910ab6d6193e304d333bd81dcefaf07021aa8b55dadae358108a873c9f79

Patch0:         build-Distinguish-yamlcpp-in-USE_BUNDLED-macro.patch
Patch1:         0001-cmake-force-civetweb-library-into-lib-instead-of-lib.patch
Patch2:         0001-build-plugins-locally.patch
Patch3:         0001-fix_lua_lpeg_library_link.patch

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
%if 0%{?with_check}
BuildRequires:  dkms
BuildRequires:  xz-devel
BuildRequires:  jq
%endif

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

%description
Sysdig falco is an open source, behavioral activity monitor designed to detect anomalous activity in your applications. Falco lets you continuously monitor and detect container, application, host, and network activity... all in one place, from one source of data, with one set of customizable rules.

%prep
%autosetup -p1

%build
mkdir build
cd build
%{cmake} \
    -DCMAKE_BUILD_TYPE=Debug \
    -DUSE_BUNDLED_DEPS:BOOL=OFF \
    -DUSE_BUNDLED_OPENSSL:BOOL=OFF \
    -DUSE_BUNDLED_JQ:BOOL=OFF \
    -DUSE_BUNDLED_YAMLCPP:BOOL=ON \
    -DBUILD_SHARED_LIBS:BOOL=OFF \
    -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
    -DCMAKE_INSTALL_SYSCONFDIR=%{_sysconfdir} \
    ..
make %{?_smp_mflags} all KERNELDIR="/lib/modules/%{uname_r}/build"

%install
cd build
make install DESTDIR=%{buildroot} KERNELDIR="/lib/modules/%{uname_r}/build" %{?_smp_mflags}
mkdir -p %{buildroot}/lib/modules/%{uname_r}/extra
install -vm 644 driver/falco.ko %{buildroot}/lib/modules/%{uname_r}/extra

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/*
%exclude %{_usrsrc}
%{_sysconfdir}/falco
%{_datadir}/falco
/lib/modules/%{uname_r}/extra/falco.ko

%post
/sbin/depmod -a

%postun
/sbin/depmod -a

%changelog
* Tue Apr 29 2025 Mukul Sikka <mukul.sikka@broadcom.com> 0.31.1-10
- Fix lua lpeg library link
* Mon Jun 24 2024 Mukul Sikka <msikka@vmware.com> 0.31.1-9
- Bump version as a part of go upgrade
* Tue Nov 21 2023 Piyush Gupta <gpiyush@vmware.com> 0.31.1-8
- Bump up version to compile with new go
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 0.31.1-7
- Bump up version to compile with new go
* Tue Sep 26 2023 Piyush Gupta <gpiyush@vmware.com> 0.31.1-6
- Bump up version to compile with new go
* Mon Sep 11 2023 Harinadh D <hdommaraju@vmware.com> 0.31.1-5
- Bump up version to compile with updated c-ares
* Fri Aug 18 2023 Piyush Gupta <gpiyush@vmware.com> 0.31.1-4
- Bump up version to compile with new go
* Fri Jul 07 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 0.31.1-3
- Build Go plugins locally
* Wed Jun 28 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.31.1-2
- Bump version as a part of sysdig upgrade
* Tue Jun 13 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 0.31.1-1
- Update to 0.31.1
* Tue Mar 14 2023 Anmol Jain <anmolja@vmware.com> 0.30.0-3
- Version bump up to use c-ares
* Mon Jan 24 2022 Ankit Jain <ankitja@vmware.com> 0.30.0-2
- Version Bump to build with new version of cmake
* Tue Nov 23 2021 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 0.30.0-1
- Update to version 0.30.0.
- Add missing runtime dependency on linux.
* Tue Aug 03 2021 Nitesh Kumar <kunitesh@vmware.com> 0.15.1-2
- Patched to fix CVE-2021-33505
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
