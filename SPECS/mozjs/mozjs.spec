%global build_if %{photon_subrelease} >= 91

%global major 140

Summary:       SpiderMonkey JavaScript library
Name:          mozjs
Version:       140.7.0
Release:       3%{?dist}
Group:         Applications/System
Vendor:        VMware, Inc.
URL:           https://spidermonkey.dev
Distribution:  Photon

Source0: https://ftp.mozilla.org/pub/firefox/releases/%{version}esr/source/firefox-%{version}esr.source.tar.xz

Source1: license.txt
%include %{SOURCE1}

Patch0:     emitter.patch
Patch1:     init_patch.patch
Patch2:     spidermonkey_checks_disable.patch
Patch3:     copy-headers.patch
Patch4:     fix-soname.patch
Patch5:     CVE-2022-46175.patch
Patch6:     compile-with-py314.patch
Patch7:     CVE-2026-2781.patch

BuildRequires: which
BuildRequires: python3-xml
BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: zlib-devel
BuildRequires: clang-devel
BuildRequires: icu-devel >= 76.1
BuildRequires: rust
BuildRequires: autoconf
BuildRequires: nss-devel
BuildRequires: readline-devel
BuildRequires: python3-curses
BuildRequires: cbindgen

Requires:      icu >= 76.1
Requires:      python3

Provides:      mozjs60
Obsoletes:     mozjs60
Obsoletes:     js

%description
SpiderMonkey is the code-name for Mozilla Firefox's C++ implementation of
JavaScript. It is intended to be embedded in other applications
that provide host environments for JavaScript.

%package       devel
Summary:       mozjs devel
Group:         Development/Tools
Provides:      mozjs60-devel
Obsoletes:     mozjs60-devel
Requires:      %{name} = %{version}-%{release}

%description   devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup -p1 -n firefox-%{version}
rm -r modules/zlib security/nss third_party/rust/mp4parse/link-u-avif-sample-images/*
# Tests are disabled anyways - avoid detecting CC-BY-SA licensed test components
# Need to keep testing/mozbase/mozfile as this python module is used in many places
# outside of ./testing/
rm -r testing/web-platform

# mozscreenshots extension borderify uses CC-BY-SA licensed .png
# we don't need this for the library we package
rm -r browser/tools/mozscreenshots

%build
export CC=gcc
export CXX=g++
export M4=m4
export AWK=awk
export AC_MACRODIR=$PWD/build/autoconf/

cd js/src

%configure \
  --with-system-icu \
  --with-system-nss \
  --with-system-zlib \
  --disable-tests \
  --enable-shared-js \
  --enable-optimize \
  --disable-debug \
  --enable-pie \
  --disable-jemalloc \
  --disable-strip \
  --without-intl-api \
  --enable-readline

%make_build

%install
cd js/src
%make_install %{?_smp_mflags}
chmod -x %{buildroot}%{_libdir}/pkgconfig/*.pc

mv %{buildroot}%{_includedir}/%{name}-%{major}/js-config.h \
    %{buildroot}%{_includedir}/%{name}-%{major}/js-config-64.h

cat >%{buildroot}%{_includedir}/%{name}-%{major}/js-config.h <<EOF
#ifndef JS_CONFIG_H_MULTILIB
#define JS_CONFIG_H_MULTILIB

#include <bits/wordsize.h>

#if __WORDSIZE == 64
# include "js-config-64.h"
#else
# error "unexpected value for __WORDSIZE macro"
#endif

#endif
EOF

# Remove unneeded files
rm %{buildroot}%{_bindir}/js%{major}-config %{buildroot}%{_libdir}/libjs_static.ajs

# Rename library and create symlinks, following fix-soname.patch
mv %{buildroot}%{_libdir}/libmozjs-%{major}.so \
   %{buildroot}%{_libdir}/libmozjs-%{major}.so.0.0.0

ln -s libmozjs-%{major}.so.0.0.0 %{buildroot}%{_libdir}/libmozjs-%{major}.so.0
ln -s libmozjs-%{major}.so.0 %{buildroot}%{_libdir}/libmozjs-%{major}.so

find %{buildroot} -name '*.la' -delete

%ldconfig_scriptlets

%files
%license LICENSE
%{_libdir}/libmozjs-%{major}.so.0*

%files devel
%{_bindir}/js%{major}
%{_libdir}/libmozjs-%{major}.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/%{name}-%{major}

%changelog
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 140.7.0-3
- Extended to build for subrelease 91 and above
* Mon Mar 23 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 140.7.0-2
- Fix CVE-2026-2781
* Mon Feb 16 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 140.7.0-1
- Upgrade to build with python3.14
* Thu Oct 23 2025 Ankit Jain <ankit-aj.jain@broadcom.com> 102.12.0-10
- Bump to build with updated clang
* Thu Oct 09 2025 Ankit Jain <ankit-aj.jain@broadcom.com> 102.12.0-9
- Bump for building with updated rust
* Tue Sep 02 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 102.12.0-8
- Rebuild with clang shared libs
* Sun Aug 03 2025 Ankit Jain <ankit-aj.jain@broadcom.com> 102.12.0-7
- Bump up release to rescan licenses
* Fri Apr 11 2025 Mukul Sikka <mukul.sikka@broadcom.com> 102.12.0-6
- Fix for CVE-2022-46175, CVE-2024-45491, CVE-2024-45492
* Thu Dec 12 2024 Ajay Kaher <ajay.kaher@broadcom.com> 102.12.0-5
- Release bump for SRP compliance
* Tue Dec 12 2023 Shreenidhi Shedi <sshedi@vmware.com> 102.12.0-4
- Add provides & obsoletes for mozjs60
* Wed Sep 06 2023 Shreenidhi Shedi <sshedi@vmware.com> 102.12.0-3
- Remove autoconf-2.13 dependency
* Thu Aug 03 2023 Piyush Gupta <gpiyush@vmware.com> 102.12.0-2
- Bump up version as part of rust upgrade.
* Mon Jun 19 2023 Mukul Sikka <msikka@vmware.com> 102.12.0-1
- Upgrade to v102.12.0
* Fri Apr 14 2023 Shreenidhi Shedi <sshedi@vmware.com> 102.6.0-4
- Bump version as a part of zlib upgrade
* Sat Feb 11 2023 Shreenidhi Shedi <sshedi@vmware.com> 102.6.0-3
- Bump version as a part of icu upgrade
* Fri Dec 23 2022 Shreenidhi Shedi <sshedi@vmware.com> 102.6.0-2
- Bump version as a part of readline upgrade
* Tue Dec 13 2022 Gerrit Photon <photon-checkins@vmware.com> 102.6.0-1
- Automatic Version Bump
* Mon Oct 31 2022 Prashant S Chauhan <psinghchauha@vmware.com> 102.3.0-2
- Update release to compile with python 3.11
* Tue Oct 04 2022 Shreenidhi Shedi <sshedi@vmware.com> 102.3.0-1
- Upgrade to v102.3.0
* Tue Oct 04 2022 Shreenidhi Shedi <sshedi@vmware.com> 78.15.0-4
- Bump version as a part of icu upgrade
* Wed Sep 28 2022 Shreenidhi Shedi <sshedi@vmware.com> 78.15.0-3
- Bump version as a part of clang upgrade
* Tue Dec 07 2021 Alexey Makhalov <amakhalov@vmware.com> 78.15.0-2
- Require specific version of icu
* Tue Oct 19 2021 Shreenidhi Shedi <sshedi@vmware.com> 78.15.0-1
- Version upgrade
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 78.10.0-1
- Automatic Version Bump
* Fri Feb 19 2021 Alexey Makhalov <amakhalov@vmware.com> 78.3.1-2
- Remove python2 requirements
* Mon Oct 05 2020 Ankit Jain <ankitja@vmware.com> 78.3.1-1
- Updated to 78.3.1
* Tue Aug 25 2020 Ankit Jain <ankitja@vmware.com> 68.11.0-2
- Removed autoconf213 dependency and obsoletes js
* Sat Oct 26 2019 Ankit Jain <ankitja@vmware.com> 68.11.0-1
- initial version
