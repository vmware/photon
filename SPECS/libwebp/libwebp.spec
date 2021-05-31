Summary:	Library to encode and decode webP format images
Name:		libwebp
Version:	1.0.3
Release:	1%{?dist}
License:	BSD
URL:		http://webmproject.org/
Group:		System Environment/Libraries
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:        https://github.com/webmproject/%{name}/archive/%{name}-%{version}.tar.gz
%define sha1 libwebp=7b78c45ec1a20c83613e287fac71f7ac3203de69
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

%configure \
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
* Mon May 31 2021 Sujay G <gsujay@vmware.com> 1.0.3-1
- Bump version to 1.0.3 to fix following CVE's:
- CVE-2018-25009, CVE-2018-25010, CVE-2018-25011, CVE-2018-25012,
- CVE-2018-25013, CVE-2018-25014, CVE-2020-36328, CVE-2020-36329,
- CVE-2020-36330, CVE-2020-36331, CVE-2020-36332
* Tue Feb 12 2019 Ankit Jain <ankitja@vmware.com> 0.6.0-2
- Release Bump up
* Thu Apr 06 2017 Kumar Kaushik <kaushikk@vmware.com> 0.6.0-1
- Upgrading version to 0.6.0
* Wed Jul 27 2016 Divya Thaluru <dthaluru@vmware.com> 0.5.1-1
- Initial version
