%global security_hardening      none
%define uname_r                 %{KERNEL_VERSION}-%{KERNEL_RELEASE}
%define _modulesdir             /lib/modules/%{uname_r}

# check the release bundle & use the right version, example:
# https://github.com/draios/sysdig/blob/0.30.2/cmake/modules/falcosecurity-libs.cmake#L35
%define falcosecurity_libs_ver  0.9.1

Summary:        Sysdig is a universal system visibility tool with native support for containers.
Name:           sysdig
Version:        0.30.2
Release:        7%{?kernelsubrelease}%{?dist}
License:        GPLv2
URL:            http://www.sysdig.org
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/draios/sysdig/archive/%{name}-%{version}.tar.gz
%define sha512 %{name}=08e5c4f6e393838fca0b8b72f152fde9873af2095fe28084463f22238c65ad45f699c724b21f2d25051eae803f253f41a319fb38b405977de382809a74a4f625

Source1: https://github.com/falcosecurity/libs/archive/falconsecurity-libs-0.9.1.tar.gz
%define sha512 falconsecurity-libs=06d894e6ea8cd66c80682dcce64e38667f6d7315c1c552898b3944fa16cf57ae49932bd283e2b5d09e2e0462f438df217c722f98e437aa0989fdef69aefd79a2

Patch0: get-googletest-sources-from-photonstage.patch
Patch1: falcosecurity-libs-nodownload.patch
Patch2: bashcomp-location.patch

BuildArch: x86_64

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
BuildRequires:  jsoncpp-devel
BuildRequires:  re2-devel

Requires:       linux = %{uname_r}
Requires:       zlib
Requires:       ncurses
Requires:       openssl
Requires:       curl
Requires:       grpc
Requires:       jq
Requires:       c-ares
Requires:       protobuf
Requires:       jsoncpp
Requires:       re2

%description
Sysdig is open source, system-level exploration, capture system state and activity from a running Linux instance.
Then save, filter and analyze.
Sysdig is scriptable in Lua and includes a command line interface and a powerful interactive UI, csysdig,
that runs in your terminal

%prep
%autosetup -p1 -a0 -a1

%build
export CFLAGS="-Wno-error=misleading-indentation"

%{cmake} \
    -DUSE_BUNDLED_OPENSSL=OFF \
    -DUSE_BUNDLED_CURL=OFF \
    -DUSE_BUNDLED_ZLIB=OFF \
    -DUSE_BUNDLED_CARES=OFF \
    -DUSE_BUNDLED_PROTOBUF=OFF \
    -DUSE_BUNDLED_GRPC=OFF \
    -DUSE_BUNDLED_JQ=OFF \
    -DUSE_BUNDLED_JSONCPP=OFF \
    -DUSE_BUNDLED_NJSON=OFF \
    -DUSE_BUNDLED_NCURSES=OFF \
    -DBUILD_DRIVER=ON \
    -DBUILD_LIBSCAP_EXAMPLES=OFF \
    -DBUILD_LIBSINSP_EXAMPLES=OFF \
    -DFALCOSECURITY_LIBS_SOURCE_DIR=%{_builddir}/%{name}-%{version}/libs-%{falcosecurity_libs_ver} \
    -DFALCOSECURITY_LIBS_VERSION=%{falcosecurity_libs_ver} \
    -DCMAKE_INSTALL_BINDIR:PATH=%{_bindir} \
    -DCMAKE_INSTALL_SBINDIR:PATH=%{_sbindir} \
    -DCMAKE_INSTALL_LIBDIR:PATH=%{_libdir} \
    -DCMAKE_INSTALL_LIBEXECDIR:PATH=%{_libexecdir} \
    -DCMAKE_INSTALL_LOCALSTATEDIR:PATH=%{_localstatedir} \
    -DCMAKE_INSTALL_SHAREDSTATEDIR:PATH=%{_sharedstatedir} \
    -DCMAKE_INSTALL_INCLUDEDIR:PATH=%{_includedir} \
    -DCMAKE_INSTALL_INFODIR:PATH=%{_infodir} \
    -DCMAKE_INSTALL_MANDIR:PATH=%{_mandir} \
    -DBUILD_SHARED_LIBS:BOOL=OFF \
    -DCMAKE_BUILD_TYPE=Release

export KERNELDIR="%{_modulesdir}/build"
%{cmake_build}

%install
export KERNELDIR="%{_modulesdir}/build"
%{cmake_install}

rm -rf %{buildroot}%{_datadir}/zsh/
mkdir -p %{buildroot}%{_modulesdir}/extra
mv %{__cmake_builddir}/driver/scap.ko %{buildroot}%{_modulesdir}/extra

%clean
rm -rf %{buildroot}/*

%post
/sbin/depmod -a

%postun
/sbin/depmod -a

%files
%defattr(-,root,root)
%{_bindir}/*
%{_includedir}/%{name}
%{_libdir}/%{name}
%exclude %{_usrsrc}
%{_datadir}/%{name}/*
%{_datadir}/bash-completion/*
%{_mandir}/*
%{_modulesdir}/extra/scap.ko

%changelog
* Sun Nov 19 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.30.2-7
- Bump version as a part of openssl upgrade
* Wed Aug 09 2023 Mukul Sikka <msikka@vmware.com> 0.30.2-6
- Bump version as a part of grpc upgrade
* Sat Jun 17 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.30.2-5
- Bump version as a part of protobuf upgrade
* Fri Jun 09 2023 Nitesh Kumar <kunitesh@vmware.com> 0.30.2-4
- Bump version as a part of ncurses upgrade to v6.4
* Fri Apr 14 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.30.2-3
- Bump version as a part of zlib upgrade
* Tue Jan 17 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.30.2-2
- Fix build options to make installation work
* Mon Dec 19 2022 Bo Gan <ganb@vmware.com> 0.30.2-1
- Update to 0.30.2
- Correct cmake configurations
* Tue Aug 30 2022 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 0.29.3-1
- Update to latest version
* Sat Jul 09 2022 Shreenidhi Shedi <sshedi@vmware.com> 0.27.0-7
- Use cmake macros for build
* Fri Jul 08 2022 Harinadh D <hdommaraju@vmware.com> 0.27.0-6
- fix build errors
* Tue Nov 16 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 0.27.0-5
- Bump up release for openssl
* Tue Nov 16 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 0.27.0-4
- Fix build failure
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
