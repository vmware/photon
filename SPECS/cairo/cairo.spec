Summary:	A 2D graphics library.
Name:		cairo
Version:	1.14.12
Release:	2%{?dist}
License:	LGPLv2 or MPLv1.1
URL:		http://cairographics.org
Group:		System Environment/Libraries
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://cairographics.org/releases/%{name}-%{version}.tar.xz
%define sha1 cairo=490025a0ba0622a853010f49fb6343f29fb70b9b
Patch0:         CVE-2017-9814.patch
BuildRequires:	pkg-config
BuildRequires:	libpng-devel
BuildRequires:	libxml2-devel
BuildRequires:	pixman-devel
BuildRequires:	freetype2-devel
BuildRequires:	fontconfig-devel
BuildRequires:	glib-devel
Requires:	pixman
Requires:	glib
Requires:	libpng
Requires:	expat

%description
Cairo is a 2D graphics library with support for multiple output devices.

%package	devel
Summary:	Header and development files
Requires:	%{name} = %{version}-%{release}
Requires:	freetype2-devel
Requires:	pixman-devel
Provides:       pkgconfig(cairo)

%description	devel
It contains the libraries and header files to create applications 

%prep
%setup -q
%patch0 -p1
%build
./configure \
	--prefix=%{_prefix} \
	--enable-xlib=no \
	--enable-xlib-render=no \
	--enable-win32=no \
        CFLAGS="-O3 -fPIC" \
	--disable-static
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -delete

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
*       Fri Sep 28 2018 Tapas Kundu <tkundu@vmware.com> 1.14.12-2
-       Added provides pkgconfig(cairo) for devel pkg.
*       Tue Sep 11 2018 Dheeraj Shetty <dheerajs@vmware.com> 1.14.12-1
-       Update to version 1.14.12
*       Tue Oct 10 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.14.8-3
-       Fix CVE-2017-9814
*       Tue Jun 06 2017 Chang Lee <changlee@vmware.com> 1.14.8-2
-       Remove %check
*       Wed Apr 05 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.14.8-1
-       Initial version
