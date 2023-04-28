%global security_hardening none

%define uname_r %{KERNEL_VERSION}-%{KERNEL_RELEASE}

%define _modulesdir /lib/modules/%{uname_r}

Summary:        The Behavioral Activity Monitor With Container Support
Name:           falco
Version:        0.32.2
Release:        2%{?kernelsubrelease}%{?dist}
License:        GPLv2
URL:            https://falco.org
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/falcosecurity/falco/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512 %{name}=88a98e32285746c2c04bd640495c12a1114a511ef6a9ee276ddaf60ad441effffe8da4879442c82a7fbab76cbecb157bd2cddc01eaa17d3876eb1860e6ec6260

Patch0: build-Distinguish-yamlcpp-in-USE_BUNDLED-macro.patch

BuildArch:      x86_64

BuildRequires:  cmake
BuildRequires:  openssl-devel
BuildRequires:  curl-devel
BuildRequires:  zlib-devel
BuildRequires:  ncurses-devel
BuildRequires:  linux-devel = %{uname_r}
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

Requires:       linux = %{uname_r}
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

%package    devel
Summary:    falco
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
Development files for %{name}

%description
Sysdig %{name} is an open source, behavioral activity monitor designed to detect anomalous activity in your applications.
Falco lets you continuously monitor and detect container, application, host, and network activity; all in one place, from one source of data, with one set of customizable rules.

%prep
%autosetup -p1

%build
%{cmake} \
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

%clean
rm -rf %{buildroot}/*

%post
/sbin/depmod -a

%postun
/sbin/depmod -a

%files
%defattr(-,root,root)
%{_bindir}/*
%exclude %{_usrsrc}
%{_sysconfdir}/%{name}
%{_datadir}/%{name}
%{_modulesdir}/extra/%{name}.ko

%files devel
%defattr(-,root,root)
%{_libdir}/falcosecurity/*
%{_includedir}/falcosecurity/*

%changelog
* Fri Apr 14 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.32.2-2
- Bump version as a part of zlib upgrade
* Thu Sep 15 2022 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 0.32.2-1
- Upgrade to v0.32.2
* Fri Jun 17 2022 Shreenidhi Shedi <sshedi@vmware.com> 0.32.0-1
- Upgrade to v0.32.0
- Introduce devel sub package
* Tue Nov 23 2021 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 0.30.0-1
- Update to version 0.30.0.
- Add missing runtime dependency on linux.
* Wed Aug 04 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 0.25.0-5
- compile with openssl 3.0.0
* Tue Aug 03 2021 Nitesh Kumar <kunitesh@vmware.com> 0.25.0-4
- Patched for CVE-2021-33505.
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
