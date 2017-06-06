Summary:	A 2D graphics library.
Name:		cairo
Version:	1.14.8
Release:	2%{?dist}
License:	LGPLv2 or MPLv1.1
URL:		http://cairographics.org
Group:		System Environment/Libraries
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://cairographics.org/releases/%{name}-%{version}.tar.xz
%define sha1 cairo=c6f7b99986f93c9df78653c3e6a3b5043f65145e
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

%description	devel
It contains the libraries and header files to create applications 

%prep
%setup -q 
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
*       Tue Jun 06 2017 Chang Lee <changlee@vmware.com> 1.14.8-2
-       Remove %check
*       Wed Apr 05 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.14.8-1
-       Initial version
