Summary:	GD is an open source code library for the dynamic creation of images by programmers.
Name:		libgd
Version:	2.2.3
Release:	3%{?dist}
License:	MIT
URL:		https://libgd.github.io/
Group:		System/Libraries
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	https://github.com/libgd/libgd/releases/download/gd-2.2.3/%{name}-%{version}.tar.gz
%define sha1 libgd=8681e4c801e51d62c13384a9334f1bd253ce630d
Patch0:         libgd-2.2.3-CVE-2016-7568.patch
Patch1:         CVE-2016-8670.patch
BuildRequires:	libjpeg-turbo-devel 
BuildRequires:	libpng-devel
BuildRequires:	libwebp-devel
BuildRequires:	libtiff-devel
Requires:		libpng
Requires:		libwebp
Requires:		libtiff
Requires:		libjpeg-turbo
Provides:	pkgconfig(libgd)
%description
GD is an open source code library for the dynamic creation of images by programmers.

GD is written in C, and "wrappers" are available for Perl, PHP and other languages. GD can read and write many different image formats. GD is commonly used to generate charts, graphics, thumbnails, and most anything else, on the fly.
%package	devel
Summary:	Header and development files
Requires:	%{name} = %{version}
%description	devel
Header & Development files 
%prep
%setup -q
%patch1 -p1
%build
./configure --prefix=%{_prefix} --with-webp --with-tiff --with-jpeg --with-png --disable-werror --disable-static
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install

%check
make %{?_smp_mflags} -k check

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*
%exclude %{_libdir}/debug/
%exclude %{_libdir}/*.la
%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.la
%changelog
*    Wed Jan 18 2017 Kumar Kaushik <kaushikk@vmware.com>  2.2.3-3
-    Fix for CVE-2016-8670
*    Fri Oct 07 2016 Anish Swaminathan <anishs@vmware.com>  2.2.3-2
-    Fix for CVE-2016-7568
*    Thu Jul 28 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 2.2.3-1
-    Initial version
