Summary:	Library to encode and decode webP format images
Name:		libwebp
Version:	0.6.0
Release:	2%{?dist}
License:	BSD
URL:		http://webmproject.org/
Group:		System Environment/Libraries
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:        https://github.com/webmproject/%{name}/archive/%{name}-%{version}.tar.gz
%define sha1 libwebp=7294e5571657b8acdc3048d0a2d7a4cf746f5c80
BuildRequires:	libjpeg-turbo-devel
BuildRequires:	libtiff-devel
BuildRequires:	libpng-devel
Requires:	libjpeg-turbo
Requires:	libtiff
Requires:	libpng
%description
The libwebp package contains a library and support programs to encode and decode images in WebP format.

%package	devel
Summary:	Header and development files
Requires:	%{name} = %{version}-%{release}
%description	devel
It contains the libraries and header files to create applications 

%prep
%setup -q 
%build
./autogen.sh

./configure \
	--prefix=%{_prefix} \
	--enable-libwebpmux \
	--enable-libwebpdemux \
	--enable-libwebpdecoder \
	--enable-libwebpextras  \
	--enable-swap-16bit-csp \
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
%{_datadir}/*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
*       Tue Feb 12 2019 Ankit Jain <ankitja@vmware.com> 0.6.0-2
-       Release Bump up
*       Thu Apr 06 2017 Kumar Kaushik <kaushikk@vmware.com> 0.6.0-1
-       Upgrading version to 0.6.0
*       Wed Jul 27 2016 Divya Thaluru <dthaluru@vmware.com> 0.5.1-1
-       Initial version
