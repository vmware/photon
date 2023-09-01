%global major 78
Summary:       Mozilla's JavaScript engine.
Name:          mozjs
Version:       78.15.0
Release:       2%{?dist}
Group:         Applications/System
Vendor:        VMware, Inc.
License:       GPLv2+ or LGPLv2+ or MPL-2.0
URL:           https://developer.mozilla.org/en-US/docs/Mozilla/Projects/SpiderMonkey
Distribution:  Photon

Source0: https://ftp.mozilla.org/pub/firefox/releases/%{version}esr/source/firefox-%{version}esr.source.tar.xz
%define sha512 firefox-%{version}=ac3de735b246ce4f0e1619cd2664321ffa374240ce6843e785d79a350dc30c967996bbcc5e3b301cb3d822ca981cbea116758fc4122f1738d75ddfd1165b6378

Patch0: 0001-build-Copy-headers-on-install-instead-of-symlinking.patch
Patch1: 0002-emitter-patch.patch
Patch2: 0003-init_patch.patch
Patch3: 0004-spidermonkey_checks_disable.patch
Patch4: 0005-autoconf213-dep-removal-1.patch
Patch5: 0006-autoconf213-dep-removal-2.patch
Patch6: 0008-FixSharedArray.patch
Patch7: 0009-Add-soname-switch-to-linker-regardless-of-Operating-.patch
Patch8: 0010-Fixup-compatibility-of-mozbuild-with-Python-3.10.patch
Patch9: 0011-icu_sources_data.py-Decouple-from-Mozilla-build-syst.patch
Patch10: CVE-2021-43539.patch
Patch11: CVE-2022-42928.patch

BuildRequires: which
BuildRequires: python3-xml
BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-six
BuildRequires: zlib-devel
BuildRequires: clang-devel
BuildRequires: icu-devel
BuildRequires: rust
BuildRequires: autoconf
BuildRequires: nss-devel

Requires: icu >= 70.1
Requires: python3

Obsoletes: mozjs60 < %{name}-%{version}%{?dist}
Obsoletes: js < %{name}-%{version}%{?dist}

%description
Mozilla's JavaScript engine includes a just-in-time compiler (JIT) that compiles
JavaScript to machine code, for a significant speed increase.

%package devel
Summary:        mozjs devel
Group:          Development/Tools
Requires:       %{name} = %{version}-%{release}

%description devel
This contains development tools and libraries for SpiderMonkey.

%prep
%autosetup -N -n firefox-%{version}
rm -rf modules/zlib security/nss
%autopatch -p1

%build
cd js/src
%configure \
    --with-system-icu \
    --disable-jemalloc \
    --disable-tests \
    --disable-strip \
    --without-intl-api \
    --disable-debug \
    --with-system-zlib \
    --with-system-nss \
    --enable-readline

%make_build

%install
cd js/src
%make_install %{?_smp_mflags}
chmod -x %{buildroot}%{_libdir}/pkgconfig/*.pc

rm -rf %{buildroot}%{_libdir}/libjs_static.ajs \
       %{buildroot}%{_libdir}/debug \
       %{buildroot}/usr/src

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/js%{major}
%{_bindir}/js%{major}-config
%{_libdir}/libmozjs-%{major}.so

%files devel
%defattr(-,root,root)
%{_includedir}/mozjs-%{major}
%{_libdir}/pkgconfig/mozjs-%{major}.pc

%changelog
* Fri Sep 01 2023 Mukul Sikka <msikka@vmware.com> 78.15.0-2
- Multiple CVE fix
* Mon Aug 28 2023 Shreenidhi Shedi <sshedi@vmware.com> 78.15.0-1
- Upgrade to v78.15.0 to fix CVE-2022-38476
* Tue Nov 22 2022 Shreenidhi Shedi <sshedi@vmware.com> 78.3.1-6
- Bump version as a part of llvm upgrade
* Tue Dec 07 2021 Alexey Makhalov <amakhalov@vmware.com> 78.3.1-5
- Require specific version of icu
* Mon Nov 15 2021 Prashant S Chauhan <psinghchauha@vmware.com> 78.3.1-4
- Update release to compile with python 3.10
* Tue Apr 20 2021 Ankit Jain <ankitja@vmware.com> 78.3.1-3
- Fix build failure with rust-1.51.0
* Fri Feb 19 2021 Alexey Makhalov <amakhalov@vmware.com> 78.3.1-2
- Remove python2 requirements
* Mon Oct 05 2020 Ankit Jain <ankitja@vmware.com> 78.3.1-1
- Updated to 78.3.1
* Tue Aug 25 2020 Ankit Jain <ankitja@vmware.com> 68.11.0-2
- Removed autoconf213 dependency and obsoletes js
* Sat Oct 26 2019 Ankit Jain <ankitja@vmware.com> 68.11.0-1
- initial version
