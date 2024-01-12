%global major 60

Summary:       Mozilla's JavaScript engine.
Name:          mozjs%{major}
Version:       60.9.0
Release:       4%{?dist}
Group:         Applications/System
Vendor:        VMware, Inc.
License:       GPLv2+ or LGPLv2+ or MPL-2.0
URL:           https://developer.mozilla.org/en-US/docs/Mozilla/Projects/SpiderMonkey
Distribution:  Photon

Source0:       https://ftp.mozilla.org/pub/firefox/releases/%{version}esr/source/firefox-%{version}esr.source.tar.xz
%define sha512 firefox-%{version}=4baea5c9c4eff257834bbaee6d7786f69f7e6bacd24ca13c2705226f4a0d88315ab38c650b2c5e9c76b698f2debc7cea1e5a99cb4dc24e03c48a24df5143a3cf

Patch0: emitter.patch
Patch1: CVE-2019-17026.patch
Patch2: CVE-2020-15656.patch
Patch3: CVE-2021-29984.patch
Patch4: CVE-2023-0767.patch

BuildRequires: autoconf213
BuildRequires: which
BuildRequires: python2-devel
BuildRequires: python-xml
BuildRequires: zlib-devel

Requires: python2
Requires: zlib

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

rm -rf modules/zlib \
       security

%build
cd js/src
sh ./configure \
    --prefix=%{_prefix} \
    --without-system-icu \
    --enable-readline \
    --disable-jemalloc \
    --disable-tests \
    --with-system-zlib

%make_build

%install
cd js/src
%make_install

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
* Fri Jan 12 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 60.9.0-4
- Fix CVE-2023-0767
* Fri Sep 01 2023 Mukul Sikka <msikka@vmware.com> 60.9.0-3
- Multiple CVE fix
* Thu Jul 21 2022 Shreenidhi Shedi <sshedi@vmware.com> 60.9.0-2
- Fix .so packaging
* Sat Oct 26 2019 Ankit Jain <ankitja@vmware.com> 60.9.0-1
- initial version
