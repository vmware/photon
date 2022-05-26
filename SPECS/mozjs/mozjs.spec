%global major 102

Summary:       SpiderMonkey JavaScript library
Name:          mozjs
Version:       102.3.0
Release:       1%{?dist}
Group:         Applications/System
Vendor:        VMware, Inc.
License:       GPLv2+ or LGPLv2+ or MPL-2.0
URL:           https://spidermonkey.dev
Distribution:  Photon

Source0: https://ftp.mozilla.org/pub/firefox/releases/%{version}esr/source/firefox-%{version}esr.source.tar.xz
%define sha512 firefox-%{version}=35357791f4de8b474780083a22fb52b7846b8012cbf01403f2b9526151d11c196ce0f9fba8e0f16d8235d7259af6fba1bc3acbb5b7e79129a28f390467aa7556

Patch0:        emitter.patch

# Build fixes
Patch1:     init_patch.patch
Patch2:     spidermonkey_checks_disable.patch
Patch3:     copy-headers.patch
Patch4:     fix-soname.patch
Patch5:     remove-sloppy-m4-detection-from-bundled-autoconf.patch

BuildRequires: which
BuildRequires: python3-xml
BuildRequires: python3-libs
BuildRequires: python3-devel
BuildRequires: zlib-devel
BuildRequires: clang-devel
BuildRequires: icu-devel >= 70.1
BuildRequires: rust
BuildRequires: autoconf = 2.13

Requires:      icu >= 70.1
Requires:      python3
Requires:      python3-libs

Obsoletes:     mozjs60
Obsoletes:     js

%description
SpiderMonkey is the code-name for Mozilla Firefox's C++ implementation of
JavaScript. It is intended to be embedded in other applications
that provide host environments for JavaScript.

%package       devel
Summary:       mozjs devel
Group:         Development/Tools
Requires:      %{name} = %{version}-%{release}

%description   devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup -p1 -n firefox-%{version}
rm -rf modules/zlib

%build
export CC=gcc
export CXX=g++
export M4=m4
export AWK=awk
export AC_MACRODIR=$PWD/build/autoconf/

cd js/src

sh ../../build/autoconf/autoconf.sh --localdir=$PWD configure.in > configure
chmod +x configure

%configure \
  --with-system-icu \
  --with-system-zlib \
  --disable-tests \
  --disable-strip \
  --with-intl-api \
  --enable-readline \
  --enable-shared-js \
  --enable-optimize \
  --disable-debug \
  --enable-pie \
  --disable-jemalloc

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
