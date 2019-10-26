%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

%global	major 60
Summary:       Mozilla's JavaScript engine.
Name:          mozjs%{major}
Version:       60.9.0
Release:       1%{?dist}
Group:         Applications/System
Vendor:        VMware, Inc.
License:       GPLv2+ or LGPLv2+ or MPL-2.0
URL:           https://developer.mozilla.org/en-US/docs/Mozilla/Projects/SpiderMonkey
Source0:       https://ftp.mozilla.org/pub/firefox/releases/%{version}esr/source/firefox-%{version}esr.source.tar.xz
Patch0:        emitter.patch
Distribution:  Photon
BuildRequires: which
BuildRequires: autoconf213
BuildRequires: python2
BuildRequires: python-xml
BuildRequires: python2-libs
BuildRequires: python2-devel
BuildRequires: zlib-devel
%define sha1 firefox-%{version}=616f8afdee741f0bea607a671b8515ef13c68b4a

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
rm -rf modules/zlib
rm -rf security

%build
cd js/src
./configure \
    --prefix=%{_prefix} \
    --without-system-icu \
    --enable-readline \
    --disable-jemalloc \
    --with-system-zlib
make

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

%files devel
%defattr(-,root,root)
%{_includedir}/mozjs-%{major}
%{_libdir}/libmozjs-%{major}.so
%{_libdir}/pkgconfig/mozjs-%{major}.pc

%changelog
*   Sat Oct 26 2019 Ankit Jain <ankitja@vmware.com> 60.9.0-1
-   initial version
