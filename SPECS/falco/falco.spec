%global security_hardening none
Summary:        The Behavioral Activity Monitor With Container Support
Name:           falco
Version:        0.15.0
Release:        4%{?kernelsubrelease}%{?dist}
License:        GPLv2
URL:            http://www.sysdig.org/falco/
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/draios/%{name}/archive/%{name}-%{version}.tar.gz
%define sha1    falco=0f1e3b5ab3e917084ae062de7525000f8c7ae8d7
Source1:        https://github.com/draios/sysdig/archive/sysdig-0.26.0.tar.gz
%define sha1    sysdig=0104006492afeda870b6b08a5d1f8e76d84559ff

Patch0:         falco-CVE-2021-33505.patch

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
BuildRequires:  which
BuildRequires:  libvirt-devel

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
Requires:       libvirt

%description
Sysdig falco is an open source, behavioral activity monitor designed to detect anomalous activity in your applications. Falco lets you continuously monitor and detect container, application, host, and network activity... all in one place, from one source of data, with one set of customizable rules.

%prep
%setup -q
%setup -q -T -D -a 1
%patch0 -p1

%build
mv sysdig-0.26.0 ../sysdig
sed -i 's|../falco/rules|rules|g' userspace/engine/CMakeLists.txt
sed -i 's|../falco/userspace|userspace|g' userspace/engine/config_falco_engine.h.in
# fix for linux-4.9
sed -i 's|task_thread_info(current)->status|current->thread.status|g' ../sysdig/driver/main.c
sed -i 's|task_thread_info(task)->status|current->thread.status|g' ../sysdig/driver/ppm_syscall.h
cmake -DCMAKE_INSTALL_PREFIX=%{_prefix} CMakeLists.txt
make KERNELDIR="/lib/modules/%{KERNEL_VERSION}-%{KERNEL_RELEASE}/build" %{?_smp_mflags}

%install
make install KERNELDIR="/lib/modules/%{KERNEL_VERSION}-%{KERNEL_RELEASE}/build" DESTDIR=%{buildroot} %{?_smp_mflags}
mkdir -p %{buildroot}/lib/modules/%{KERNEL_VERSION}-%{KERNEL_RELEASE}/extra
mv driver/falco-probe.ko %{buildroot}/lib/modules/%{KERNEL_VERSION}-%{KERNEL_RELEASE}/extra

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/*
%exclude %{_usrsrc}
%{_sysconfdir}/*
%{_datadir}/*
/lib/modules/%{KERNEL_VERSION}-%{KERNEL_RELEASE}/extra/falco-probe.ko

%post
/sbin/depmod -a

%postun
/sbin/depmod -a

%changelog
* Fri Jul 15 2022 Shreenidhi Shedi <sshedi@vmware.com> 0.15.0-4
- Use libvirt from available photon package
* Tue Aug 03 2021 Nitesh Kumar <kunitesh@vmware.com> 0.15.0-3
- Patched to fix CVE-2021-33505
* Wed Feb 12 2020 Ashwin H <ashwinh@vmware.com> 0.15.0-2
- Add depmod for falco-probe.ko and remove patch for falco-probe-loader
* Sun May 26 2019 Harinadh Dommaraju <hdommaraju@vmware.com> 0.15.0-1
- Fix for CVE-2019-8839
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
