Summary:        A 2D graphics library.
Name:           cairo
Version:        1.16.0
Release:        1%{?dist}
License:        LGPLv2 or MPLv1.1
URL:            http://cairographics.org
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://cairographics.org/releases/%{name}-%{version}.tar.xz
%define sha1    cairo=00e81842ae5e81bb0343108884eb5205be0eac14
BuildRequires:  pkg-config
BuildRequires:  libpng-devel
BuildRequires:  libxml2-devel
BuildRequires:  pixman-devel
BuildRequires:  freetype2-devel
BuildRequires:  fontconfig-devel
BuildRequires:  glib-devel
Requires:       pixman
Requires:       glib
Requires:       libpng
Requires:       expat

%description
Cairo is a 2D graphics library with support for multiple output devices.

%package    devel
Summary:    Header and development files
Requires:   %{name} = %{version}-%{release}
Requires:   freetype2-devel
Requires:   pixman-devel

%description    devel
It contains the libraries and header files to create applications 

%prep
%setup -q
%build
%configure \
    --prefix=%{_prefix}     \
    --enable-xlib=no        \
    --enable-xlib-render=no \
    --enable-win32=no       \
        CFLAGS="-O3 -fPIC"  \
    --disable-static
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -delete

%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so.*
%{_libdir}/cairo/*.so*
%{_datadir}/*

%files devel
%defattr(-,root,root)
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
*   Thu Mar 14 2019 Michelle Wang <michellew@vmware.com> 1.16.0-1
-   Upgrade cairo to 1.16.0 for CVE-2018-18064
-   CVE-2018-18064 is for version up to (including) 1.15.14
*   Tue Oct 10 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.14.8-2
-   Fix CVE-2017-9814
*   Wed Apr 05 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.14.8-1
-   Initial version
