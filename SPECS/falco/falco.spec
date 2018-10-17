%global security_hardening none
Summary:        The Behavioral Activity Monitor With Container Support
Name:           falco
Version:        0.12.1
Release:        2%{?kernelsubrelease}%{?dist}
License:        GPLv2
URL:            http://www.sysdig.org/falco/
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/draios/%{name}/archive/%{name}-%{version}.tar.gz
%define sha1    falco=f0b18777d990bd325c712ceca67fe49d6b71b0e9
Source1:        https://github.com/draios/sysdig/archive/sysdig-0.23.1.tar.gz
%define sha1    sysdig=8d1ce894c8fcd8a1939c28adbfb661ad82110bde
Source2:        http://libvirt.org/sources/libvirt-2.0.0.tar.xz
%define sha1    libvirt=9a923b06df23f7a5526e4ec679cdadf4eb35a38f
BuildArch:      x86_64
BuildRequires:  cmake
BuildRequires:  openssl-devel
BuildRequires:  curl-devel
BuildRequires:  zlib-devel
BuildRequires:  ncurses-devel
BuildRequires:  linux-devel = %{KERNEL_VERSION}-%{KERNEL_RELEASE}
BuildRequires:  libgcrypt
BuildRequires:  sysdig
BuildRequires:  git
BuildRequires:  lua-devel
BuildRequires:  libyaml-devel
BuildRequires:  linux-api-headers
BuildRequires:  wget
%if %{with_check}
BuildRequires:  dkms
BuildRequires:  xz-devel
BuildRequires:  jq
%endif
Requires:       zlib
Requires:       ncurses
Requires:       openssl
Requires:       curl
Requires:       libyaml
Requires:       lua
Requires:       sysdig
Requires:       dkms

%description
Sysdig falco is an open source, behavioral activity monitor designed to detect anomalous activity in your applications. Falco lets you continuously monitor and detect container, application, host, and network activity... all in one place, from one source of data, with one set of customizable rules. 

%prep
%setup
%setup -T -D -a 1
tar xf %{SOURCE2} --no-same-owner

%build
mv sysdig-0.23.1 ../sysdig
sed -i 's|../falco/rules|rules|g' userspace/engine/CMakeLists.txt
sed -i 's|../falco/userspace|userspace|g' userspace/engine/config_falco_engine.h.in
cmake -DCMAKE_INSTALL_PREFIX=%{_prefix} CMakeLists.txt
make KERNELDIR="/lib/modules/%{KERNEL_VERSION}-%{KERNEL_RELEASE}/build"

%install
make install KERNELDIR="/lib/modules/%{KERNEL_VERSION}-%{KERNEL_RELEASE}/build" DESTDIR=%{buildroot}
mkdir -p %{buildroot}/lib/modules/%{KERNEL_VERSION}-%{KERNEL_RELEASE}/extra
mv driver/falco-probe.ko %{buildroot}/lib/modules/%{KERNEL_VERSION}-%{KERNEL_RELEASE}/extra
sed -i 's|/var/lib/dkms/$PACKAGE_NAME/$SYSDIG_VERSION/$KERNEL_RELEASE/$ARCH/module/$PROBE_NAME.ko|/lib/modules/$KERNEL_RELEASE/extra/$PROBE_NAME.ko|g' %{buildroot}/usr/bin/falco-probe-loader

#falco requires docker instance and dpkg to pass make check.
#%check
#easy_install pip
#pip install 'stevedore>=0.14'
#pip install 'avocado-framework<=36.0'
#pip install fabric
#pip install aexpect
#pip install pystache
#test/run_regression_tests.sh

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/*
%exclude %{_usrsrc}
%{_sysconfdir}/*
%{_datadir}/*
/lib/modules/%{KERNEL_VERSION}-%{KERNEL_RELEASE}/extra/falco-probe.ko

%changelog
*   Mon Oct 22 2018 Ajay Kaher <akaher@vmware.com> 0.12.1-2
-   Adding BuildArch
*   Mon Sep 24 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 0.12.1-1
-   Update falco and sysdig versions to fix build error with linux 4.18
*   Tue Jan 02 2018 Alexey Makhalov <amakhalov@vmware.com> 0.8.1-1
-   Version update to build against linux-4.14.y kernel
*   Thu Aug 24 2017 Rui Gu <ruig@vmware.com> 0.6.0-3
-   Disable check section (Bug 1900272).
*   Thu May 11 2017 Chang Lee <changlee@vmware.com> 0.6.0-2
-   Add falco-probe.ko and change falco-probe.ko path in falco-probe-loader
*   Mon Apr 03 2017 Chang Lee <changlee@vmware.com> 0.6.0-1
-   Update to version 0.6.0
*   Wed Jan 11 2017 Alexey Makhalov <amakhalov@vmware.com> 0.2.0-7
-   Fix building for linux-4.9.2
*   Mon Dec 19 2016 Xiaolin Li <xiaolinl@vmware.com> 0.2.0-6
-   BuildRequires curl-devel
*   Thu Dec 15 2016 Alexey Makhalov <amakhalov@vmware.com> 0.2.0-5
-   Fix building for linux-4.9
*   Wed Nov 30 2016 Alexey Makhalov <amakhalov@vmware.com> 0.2.0-4
-   Expand uname -r to have release number
-   Exclude /usr/src
*   Fri Sep  2 2016 Alexey Makhalov <amakhalov@vmware.com> 0.2.0-3
-   Use KERNEL_VERSION macro
*   Wed Jul 27 2016 Divya Thaluru <dthaluru@vmware.com> 0.2.0-2
-   Removed packaging of debug files
*   Tue Jun 28 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 0.2.0-1
-   Initial build. First version
