Summary:       Mozilla's JavaScript engine.
Name:          js
Version:       45.0.2
Release:       1%{?dist}
Group:         Applications/System
Vendor:        VMware, Inc.
License:       MPLv2.0
URL:           https://developer.mozilla.org/en-US/docs/Mozilla/Projects/SpiderMonkey/Releases/45
Source0:       https://archive.mozilla.org/pub/spidermonkey/releases/%{version}/moz%{name}-%{version}.tar.bz2
%define sha1 moz%{name}-%{version}=68a0fbb9c3f988ab28ea3817e0669ee6fe6c93ed
Distribution:  Photon
Patch0:        configure-icu-version-num-fix.patch
BuildRequires: autoconf
BuildRequires: ncurses-devel
BuildRequires: nspr-devel >= 4.7
BuildRequires: zip
BuildRequires: python-pip
Requires:      ncurses
Requires:      nspr

%description
Mozilla's JavaScript engine includes a just-in-time compiler (JIT) that compiles
JavaScript to machine code, for a significant speed increase. 

%package devel
Summary:        js devel
Group:          Development/Tools
Requires:       %{name} = %{version}-%{release}
%description devel
This contains development tools and libraries for SpiderMonkey.

%prep
%setup -q -n moz%{name}-%{version}
%patch0 -p1

%build
cd js/src
mkdir obj
cd obj
../configure \
    --prefix=%{_prefix}
make %{?_smp_mflags}

%install
cd js/src/obj
make DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -delete

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/%{name}
%{_bindir}/js-config

%files devel
%defattr(-,root,root)
%{_includedir}/moz%{name}-45/*
%{_libdir}/libjs_static.ajs
%{_libdir}/libmozjs-45.so
%{_libdir}/pkgconfig/%{name}.pc

%changelog
*   Thu Sep 20 2018 Ankit Jain <ankitja@vmware.com> 45.0.2-1
-   Updated to version 45.0.2
*   Tue Nov 14 2017 Alexey Makhalov <amakhalov@vmware.com> 1.8.5-2
-   Aarch64 support
*   Thu Oct 05 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.8.5-1
-   mozjs v1.8.5.
*   Fri May 22 2015 Alexey Makhalov <amakhalov@vmware.com> 17.0.0-1
-   initial version
