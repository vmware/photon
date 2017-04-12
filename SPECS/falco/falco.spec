%global security_hardening none
Summary:        The Behavioral Activity Monitor With Container Support
Name:           falco
Version:        0.6.0
Release:        1%{?kernelsubrelease}%{?dist}
License:        GPLv2
URL:            http://www.sysdig.org/falco/
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/draios/%{name}/archive/%{name}-%{version}.tar.gz
%define sha1    falco=04dc79c1c4773ba2080c2c49c718305e7920c2f7
Source1:        https://github.com/draios/sysdig/archive/sysdig-0.15.1.tar.gz
%define sha1    sysdig=5b1a7a4978315176412989b5400572d849691917
Source2:        http://stedolan.github.io/jq/download/linux64/jq
%define sha1    jq=e820e9e91c9cce6154f52949a3b2a451c4de8af4
Source3:        http://libvirt.org/sources/libvirt-2.0.0.tar.xz
%define sha1    libvirt=9a923b06df23f7a5526e4ec679cdadf4eb35a38f
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
Requires:       zlib
Requires:       ncurses
Requires:       openssl
Requires:       curl
Requires:       libyaml
Requires:       lua
Requires:       sysdig

%description
Sysdig falco is an open source, behavioral activity monitor designed to detect anomalous activity in your applications. Falco lets you continuously monitor and detect container, application, host, and network activity... all in one place, from one source of data, with one set of customizable rules. 

%prep
%setup
%setup -T -D -a 1
chmod +x %{SOURCE2}
cp %{SOURCE2} /usr/bin
tar xf %{SOURCE3} --no-same-owner

%build
mv sysdig-0.15.1 ../sysdig
sed -i 's|../falco/rules|rules|g' userspace/engine/CMakeLists.txt
sed -i 's|../falco/userspace|userspace|g' userspace/engine/config_falco_engine.h.in
# fix for linux-4.9
sed -i 's|task_thread_info(current)->status|current->thread.status|g' ../sysdig/driver/main.c
sed -i 's|task_thread_info(task)->status|current->thread.status|g' ../sysdig/driver/ppm_syscall.h
cmake -DCMAKE_INSTALL_PREFIX=%{_prefix} CMakeLists.txt
make KERNELDIR="/lib/modules/%{KERNEL_VERSION}-%{KERNEL_RELEASE}/build"

%install
make install KERNELDIR="/lib/modules/%{KERNEL_VERSION}-%{KERNEL_RELEASE}/build" DESTDIR=%{buildroot}

%check
easy_install pip
pip install avocado-framework
pip install fabric
pip install aexpect
test/run_regression_tests.sh

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/*
%exclude %{_usrsrc}
%{_sysconfdir}/*
%{_datadir}/*

%changelog
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
