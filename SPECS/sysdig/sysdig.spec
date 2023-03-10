%global security_hardening none

%define uname_r %{KERNEL_VERSION}-%{KERNEL_RELEASE}
%define _modulesdir /lib/modules/%{uname_r}

Summary:        Sysdig is a universal system visibility tool with native support for containers.
Name:           sysdig
Version:        0.27.0
Release:        8%{?kernelsubrelease}%{?dist}
License:        GPLv2
URL:            http://www.sysdig.org/
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/draios/sysdig/archive/%{name}-%{version}.tar.gz
%define sha512 %{name}=102150cc641165a6c18ce71e3c6148dc10700f614fec7e1909c29172e3cce02dfa16af56aabdcd420499d0aa89f90fee8f26d92a250b0a521d1b9d416c6a678f

Patch0:         get-lua-googletest-sources-from-photonstage.patch

BuildArch:      x86_64

BuildRequires:  cmake
BuildRequires:  linux-devel = %{uname_r}
BuildRequires:  openssl-devel
BuildRequires:  curl-devel
BuildRequires:  zlib-devel
BuildRequires:  ncurses-devel
BuildRequires:  wget
BuildRequires:  which
BuildRequires:  grpc-devel
BuildRequires:  jq-devel
BuildRequires:  c-ares-devel
BuildRequires:  protobuf-devel
BuildRequires:  git
BuildRequires:  net-tools

Requires:       linux = %{uname_r}
Requires:       zlib
Requires:       ncurses
Requires:       openssl
Requires:       curl
Requires:       grpc
Requires:       jq
Requires:       c-ares
Requires:       protobuf

%description
 Sysdig is open source, system-level exploration: capture system state and activity from a running Linux instance, then save, filter and analyze. Sysdig is scriptable in Lua and includes a command line interface and a powerful interactive UI, csysdig, that runs in your terminal

%prep
%autosetup -p1

%build
export CFLAGS="-Wno-error=misleading-indentation"
# fix for linux-4.9
sed -i 's|task_thread_info(current)->status|current->thread.status|g' driver/main.c
sed -i 's|task_thread_info(task)->status|current->thread.status|g' driver/ppm_syscall.h
sed -i '/#include <stdlib.h>/a #include<sys/sysmacros.h>' userspace/libscap/scap_fds.c
sed -i '/"${B64_LIB}"/a      "${CURL_LIBRARIES}"' userspace/libsinsp/CMakeLists.txt
%cmake \
    -DUSE_BUNDLED_OPENSSL=OFF \
    -DUSE_BUNDLED_CURL=OFF \
    -DUSE_BUNDLED_ZLIB=OFF \
    -DUSE_BUNDLED_CARES=OFF \
    -DUSE_BUNDLED_PROTOBUF=OFF \
    -DUSE_BUNDLED_GRPC=OFF \
    -DUSE_BUNDLED_JQ=OFF \
    -DUSE_BUNDLED_NCURSES=OFF \
    -DCMAKE_BUILD_TYPE=Debug \
    -DCMAKE_INSTALL_LIBDIR=%{_libdir}

export KERNELDIR="%{_modulesdir}/build"
%cmake_build

%install
export KERNELDIR="%{_modulesdir}/build"
%cmake_install

mkdir -p %{buildroot}%{_sysconfdir}
mv %{buildroot}%{_usr}%{_sysconfdir}/bash_completion.d %{buildroot}%{_sysconfdir}
rm -rf %{buildroot}%{_datadir}/zsh/

mkdir -p %{buildroot}%{_modulesdir}/extra
mv %{__cmake_builddir}/driver/sysdig-probe.ko %{buildroot}%{_modulesdir}/extra

%clean
rm -rf %{buildroot}/*

%post
/sbin/depmod -a

%postun
/sbin/depmod -a

%files
%defattr(-,root,root)
%{_sysconfdir}/bash_completion.d/*
%{_bindir}
%exclude %{_usrsrc}
%{_datadir}
%{_modulesdir}/extra/sysdig-probe.ko

%changelog
* Wed Mar 15 2023 Anmol Jain <anmolja@vmware.com> 0.27.0-8
- Version bump up to use c-ares
* Fri Jul 08 2022 Harinadh D <hdommaraju@vmware.com> 0.27.0-7
- Fix build failures in luajit and googletest
* Mon Mar 28 2022 Harinadh D <hdommaraju@vmware.com> 0.27.0-6
- version bump to build with protobuf 3.19.4
* Tue Nov 16 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 0.27.0-5
- Fix build failure
* Wed Aug 04 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 0.27.0-4
- Bump up release for openssl
* Fri Feb 19 2021 Harinadh D <hdommaraju@vmware.com> 0.27.0-3
- Version bump up to build with latest protobuf
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 0.27.0-2
- openssl 1.1.1
* Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 0.27.0-1
- Automatic Version Bump
* Fri Sep 27 2019 Ajay Kaher <akaher@vmware.com> 0.26.4-1
- Update to version 0.26.4 to fix kernel NULL pointer
- dereference crash in record_event_consumer.part
* Wed Jun 26 2019 Harinadh Dommaraju <hdommaraju@vmware.com> 0.26.0-1
- Fix for CVE-2019-8339
* Fri Dec 07 2018 Sujay G <gsujay@vmware.com> 0.23.1-3
- Disabled bundled JQ and use Photon maintained JQ
* Mon Oct 22 2018 Ajay Kaher <akaher@vmware.com> 0.23.1-2
- Adding BuildArch
* Wed Sep 19 2018 Ajay Kaher <akaher@vmware.com> 0.23.1-1
- Update to version 0.23.1
* Wed Dec 13 2017 Xiaolin Li <xiaolinl@vmware.com> 0.19.1-1
- Update to version 0.19.1
* Wed Apr 12 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.15.1-1
- Update to version 0.15.1
* Wed Jan 11 2017 Alexey Makhalov <amakhalov@vmware.com> 0.10.1-6
- Fix building for linux-4.9.2
* Mon Dec 19 2016 Xiaolin Li <xiaolinl@vmware.com> 0.10.1-5
- BuildRequires curl-devel
* Thu Dec 15 2016 Alexey Makhalov <amakhalov@vmware.com> 0.10.1-4
- Fix building for linux-4.9
* Wed Nov 30 2016 Alexey Makhalov <amakhalov@vmware.com> 0.10.1-3
- Expand uname -r to have release number
- Exclude /usr/src
* Mon Aug 1 2016 Divya Thaluru <dthaluru@vmware.com> 0.10.1-2
- Added kernel macros
* Thu Jul 14 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 0.10.1-2
- Updated sysdig to build the kernel module
* Tue Jun 28 2016 Anish Swaminathan <anishs@vmware.com> 0.10.1-1
- Upgrade sysdig to 0.10.1
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.8.0-4
- GA - Bump release of all rpms
* Fri May 20 2016 Divya Thaluru <dthaluru@vmware.com> 0.8.0-3
- Removing usage of bundled packages to build sysdig package
* Wed Mar 16 2016 Anish Swaminathan <anishs@vmware.com> 0.8.0-2
- Add openssl to buildrequires.
* Tue Feb 23 2016 Kumar Kaushik <kaushikk@vmware.com> 0.8.0-1
- Upgraded to new version.
* Wed Jan 20 2016 Anish Swaminathan <anishs@vmware.com> 0.6.0-1
- Upgrade version.
* Mon Nov 30 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 0.1.101-1
- Initial build. First version
