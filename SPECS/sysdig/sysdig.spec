%global security_hardening none
Summary:        Sysdig is a universal system visibility tool with native support for containers.
Name:           sysdig
Version:        0.26.4
Release:        3%{?kernelsubrelease}%{?dist}
License:        GPLv2
URL:            http://www.sysdig.org/
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/draios/sysdig/archive/%{name}-%{version}.tar.gz
%define sha512  sysdig=f56f5d0a522b861df4803bfdafcaf8db3fc9c0e751d06c321082757f6828a210cb86bab4550a3b35bf6412f930e44ab0f5cf709a30651c57dd7064a68e273a88
BuildArch:      x86_64
BuildRequires:  cmake
BuildRequires:  linux-devel = %{KERNEL_VERSION}-%{KERNEL_RELEASE}
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
Requires:       linux = %{KERNEL_VERSION}-%{KERNEL_RELEASE}
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
# fix for linux-4.9
sed -i 's|task_thread_info(current)->status|current->thread.status|g' driver/main.c
sed -i 's|task_thread_info(task)->status|current->thread.status|g' driver/ppm_syscall.h
sed -i '/#include <stdlib.h>/a #include<sys/sysmacros.h>' userspace/libscap/scap_fds.c
sed -i '/"${B64_LIB}"/a      "${CURL_LIBRARIES}"' userspace/libsinsp/CMakeLists.txt
mkdir build
cd build
cmake \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DUSE_BUNDLED_OPENSSL=OFF \
    -DUSE_BUNDLED_CURL=OFF \
    -DUSE_BUNDLED_ZLIB=OFF \
    -DUSE_BUNDLED_CARES=OFF \
    -DUSE_BUNDLED_PROTOBUF=OFF \
    -DUSE_BUNDLED_GRPC=OFF \
    -DUSE_BUNDLED_JQ=OFF \
    -DUSE_BUNDLED_NCURSES=OFF ..

make %{?_smp_mflags} KERNELDIR="/lib/modules/%{KERNEL_VERSION}-%{KERNEL_RELEASE}/build"

%install
cd build
make %{?_smp_mflags} install DESTDIR=%{buildroot} KERNELDIR="/lib/modules/%{KERNEL_VERSION}-%{KERNEL_RELEASE}/build"
mv %{buildroot}/usr/src/sysdig* %{buildroot}/usr/src/sysdig-%{version}
mkdir -p %{buildroot}/etc/
mv %{buildroot}/usr/etc/bash_completion.d %{buildroot}/etc/
rm -rf %{buildroot}/usr/share/zsh/
mkdir -p %{buildroot}/lib/modules/%{KERNEL_VERSION}-%{KERNEL_RELEASE}/extra
mv driver/sysdig-probe.ko %{buildroot}/lib/modules/%{KERNEL_VERSION}-%{KERNEL_RELEASE}/extra

%clean
rm -rf %{buildroot}/*

%post
/sbin/depmod -a

%postun
/sbin/depmod -a

%files
%defattr(-,root,root)
/etc/bash_completion.d/*
%{_bindir}
%exclude %{_usrsrc}
%{_datadir}
/lib/modules/%{KERNEL_VERSION}-%{KERNEL_RELEASE}/extra/sysdig-probe.ko

%changelog
*   Tue Mar 14 2023 Anmol Jain <anmolja@vmware.com> 0.26.4-3
-   Version bump up to use c-ares
*   Mon Jan 24 2022 Ankit Jain <ankitja@vmware.com> 0.26.4-2
-   Version Bump to build with new version of cmake
*   Fri Sep 27 2019 Ajay Kaher <akaher@vmware.com> 0.26.4-1
-   Update to version 0.26.4 to fix kernel NULL pointer
-   dereference crash in record_event_consumer.part
*   Wed Jun 26 2019 Harinadh Dommaraju <hdommaraju@vmware.com> 0.26.0-1
-   Fix for CVE-2019-8339
*   Fri Dec 07 2018 Sujay G <gsujay@vmware.com> 0.23.1-3
-   Disabled bundled JQ and use Photon maintained JQ
*   Mon Oct 22 2018 Ajay Kaher <akaher@vmware.com> 0.23.1-2
-   Adding BuildArch
*   Wed Sep 19 2018 Ajay Kaher <akaher@vmware.com> 0.23.1-1
-   Update to version 0.23.1
*   Wed Dec 13 2017 Xiaolin Li <xiaolinl@vmware.com> 0.19.1-1
-   Update to version 0.19.1
*   Wed Apr 12 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.15.1-1
-   Update to version 0.15.1
*   Wed Jan 11 2017 Alexey Makhalov <amakhalov@vmware.com> 0.10.1-6
-   Fix building for linux-4.9.2
*   Mon Dec 19 2016 Xiaolin Li <xiaolinl@vmware.com> 0.10.1-5
-   BuildRequires curl-devel
*   Thu Dec 15 2016 Alexey Makhalov <amakhalov@vmware.com> 0.10.1-4
-   Fix building for linux-4.9
*   Wed Nov 30 2016 Alexey Makhalov <amakhalov@vmware.com> 0.10.1-3
-   Expand uname -r to have release number
-   Exclude /usr/src
*   Mon Aug 1 2016 Divya Thaluru <dthaluru@vmware.com> 0.10.1-2
-   Added kernel macros
*   Thu Jul 14 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 0.10.1-2
-   Updated sysdig to build the kernel module
*   Tue Jun 28 2016 Anish Swaminathan <anishs@vmware.com> 0.10.1-1
-   Upgrade sysdig to 0.10.1
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.8.0-4
-   GA - Bump release of all rpms
*   Fri May 20 2016 Divya Thaluru <dthaluru@vmware.com> 0.8.0-3
-   Removing usage of bundled packages to build sysdig package
*   Wed Mar 16 2016 Anish Swaminathan <anishs@vmware.com> 0.8.0-2
-   Add openssl to buildrequires.
*   Tue Feb 23 2016 Kumar Kaushik <kaushikk@vmware.com> 0.8.0-1
-   Upgraded to new version.
*   Wed Jan 20 2016 Anish Swaminathan <anishs@vmware.com> 0.6.0-1
-   Upgrade version.
*   Mon Nov 30 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 0.1.101-1
-   Initial build. First version
