Summary:       Mozilla's JavaScript engine.
Name:          js
Version:       1.8.5
Release:       3%{?dist}
Group:         Applications/System
Vendor:        VMware, Inc.
License:       GPLv2+ or LGPLv2+ or MPLv1.1
URL:           https://developer.mozilla.org/en-US/docs/Mozilla/Projects/SpiderMonkey/Releases/1.8.5
Source0:       https://archive.mozilla.org/pub/js/js185-1.0.0.tar.gz
Patch0:        mozjs-aarch64-support.patch
Distribution:  Photon
BuildRequires: autoconf
BuildRequires: ncurses-devel
BuildRequires: nspr-devel >= 4.7
BuildRequires: zip
BuildRequires: python2
Requires:      ncurses
Requires:      nspr
%define sha1 js185=52a01449c48d7a117b35f213d3e4263578d846d6

%description
Mozilla's JavaScript engine includes a just-in-time compiler (JIT) that compiles
JavaScript to machine code, for a significant speed increase.

%package devel
Summary:        js devel
Group:          Development/Tools
Requires:       %{name} = %{version}
%description devel
This contains development tools and libraries for SpiderMonkey.

%prep
%setup -q
%patch0 -p1

%build
cd js/src
%configure \
    --datadir=%{_datarootdir} \
    --with-system-nspr \
    --enable-threadsafe \
    --enable-readline
make CXX=g++ CXXFLAGS='-std=gnu++98 -DXP_UNIX=1 -DJS_THREADSAFE=1 -DENABLE_ASSEMBLER=1 -DENABLE_JIT=1'

%install
cd js/src
make DESTDIR=%{buildroot} install
pushd %{buildroot}/%{_libdir}
ln -fs libmozjs185.so.1.0.0 libmozjs185.so.1.0
ln -fs libmozjs185.so.1.0 libmozjs185.so
popd
find %{buildroot} -name '*.la' -delete

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/js-config
%{_libdir}/libmozjs185.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/%{name}/*
%{_libdir}/libmozjs185-1.0.a
%{_libdir}/libmozjs185.so
%{_libdir}/pkgconfig/mozjs185.pc

%changelog
*   Tue Jan 08 2019 Alexey Makhalov <amakhalov@vmware.com> 1.8.5-3
-   Added BuildRequires python2
*   Tue Nov 14 2017 Alexey Makhalov <amakhalov@vmware.com> 1.8.5-2
-   Aarch64 support
*   Thu Oct 05 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.8.5-1
-   mozjs v1.8.5.
*   Fri May 22 2015 Alexey Makhalov <amakhalov@vmware.com> 17.0.0-1
-   initial version
