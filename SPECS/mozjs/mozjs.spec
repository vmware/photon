%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

%global	major 68
Summary:       Mozilla's JavaScript engine.
Name:          mozjs
Version:       68.11.0
Release:       2%{?dist}
Group:         Applications/System
Vendor:        VMware, Inc.
License:       GPLv2+ or LGPLv2+ or MPL-2.0
URL:           https://developer.mozilla.org/en-US/docs/Mozilla/Projects/SpiderMonkey
Source0:       https://ftp.mozilla.org/pub/firefox/releases/%{version}esr/source/firefox-%{version}esr.source.tar.xz
%define sha1   firefox-%{version}=445acbf7b7b8f75374ee6347bb6f45748511bcf9
Patch0:        emitter.patch
Patch1:        emitter_test.patch
# Build fixes
Patch2:        init_patch.patch
Patch3:        spidermonkey_checks_disable.patch
Patch4:        Remove-unused-LLVM-and-Rust-build-dependencies.patch
Distribution:  Photon
BuildArch:     aarch64
BuildRequires: which
BuildRequires: python3-xml
BuildRequires: python3-libs
BuildRequires: python3-devel
BuildRequires: zlib-devel
BuildRequires: clang-devel
BuildRequires: autoconf = 2.13
Requires:      python3
Requires:      python3-libs
Obsoletes:     mozjs60
Obsoletes:     js
%define ExtraBuildRequires python2 python2-libs python2-devel python-xml

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
%setup -q -n firefox-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
rm -rf modules/zlib
rm -rf security

%build
cd js/src
sh configure \
    --prefix=%{_prefix} \
    --without-system-icu \
    --enable-readline \
    --disable-jemalloc \
    --disable-tests \
    --with-system-zlib
make %{?_smp_mflags}

%install
cd js/src
make DESTDIR=%{buildroot} install
chmod -x %{buildroot}%{_libdir}/pkgconfig/*.pc
# remove non required files
rm %{buildroot}%{_libdir}/libjs_static.ajs
rm -rf %{buildroot}%{_libdir}/debug
rm -rf %{buildroot}/usr/src
find %{buildroot} -name '*.la' -delete

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
*   Tue Aug 25 2020 Ankit Jain <ankitja@vmware.com> 68.11.0-2
-   Removed autoconf213 dependency and obsoletes js
*   Sat Oct 26 2019 Ankit Jain <ankitja@vmware.com> 68.11.0-1
-   initial version
