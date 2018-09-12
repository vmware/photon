Summary:	Library to encode and decode webP format images
Name:		libwebp
Version:	1.0.0
Release:	1%{?dist}
License:	BSD
URL:		http://webmproject.org/
Group:		System Environment/Libraries
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:        https://github.com/webmproject/%{name}/archive/%{name}-%{version}.tar.gz
%define sha1 libwebp=919ee17845b3563a47bc5154ffa0b16f96e48bc7
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
*       Wed Sep 12 2018 Keerthana K <keerthanak@vmware.com> 1.0.0-1
-       Update to version 1.0.0
*       Thu Apr 06 2017 Kumar Kaushik <kaushikk@vmware.com> 0.6.0-1
-       Upgrading version to 0.6.0
*       Wed Jul 27 2016 Divya Thaluru <dthaluru@vmware.com> 0.5.1-1
-       Initial version
