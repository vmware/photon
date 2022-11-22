%global major 78
Summary:       Mozilla's JavaScript engine.
Name:          mozjs
Version:       78.3.1
Release:       6%{?dist}
Group:         Applications/System
Vendor:        VMware, Inc.
License:       GPLv2+ or LGPLv2+ or MPL-2.0
URL:           https://developer.mozilla.org/en-US/docs/Mozilla/Projects/SpiderMonkey
Distribution:  Photon

Source0: https://ftp.mozilla.org/pub/firefox/releases/%{version}esr/source/firefox-%{version}esr.source.tar.xz
%define sha512 firefox-%{version}=162860df8e4ef7322e91924bd4aae731a49dbd9829f02b306e4e5acc69c611f4a1e5727c3857b2f98e951745a3b1d8f550966105badc095205644d1ad7f5a340

Patch0:        emitter.patch
Patch1:        emitter_test.patch
# Build fixes
Patch2:        init_patch.patch
Patch3:        spidermonkey_checks_disable.patch
Patch4:        rust-nix-fix.patch
Patch5:        compile-with-python3.10.patch

BuildRequires: which
BuildRequires: python3-xml
BuildRequires: python3-devel
BuildRequires: zlib-devel
BuildRequires: clang-devel
BuildRequires: icu-devel >= 70.1
BuildRequires: rust
BuildRequires: autoconf = 2.13

Requires:      icu >= 70.1
Requires:      python3

Obsoletes:     mozjs60
Obsoletes:     js

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
%autosetup -p1 -n firefox-%{version}
rm -rf modules/zlib

%build
cd js/src
%configure \
    --with-system-icu \
    --enable-readline \
    --disable-jemalloc \
    --disable-tests \
    --with-system-zlib

%make_build

%install
cd js/src
%make_install %{?_smp_mflags}
chmod -x %{buildroot}%{_libdir}/pkgconfig/*.pc
# remove non required files
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
