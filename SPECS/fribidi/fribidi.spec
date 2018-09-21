Summary:	Free Implementation of the Unicode Bidirectional Algorithm
Name:		fribidi
Version:	1.0.5
Release:	1%{?dist}
License:	LGPL-2.1
URL:		http://fribidi.org/
Source0:	https://github.com/fribidi/fribidi/archive/%{name}-%{version}.tar.gz
%define sha1 fribidi=616619aa88f4a89350301b7f482d6c1d807933ee
Group:		System/Libraries
Vendor:		VMware, Inc.
Distribution:	Photon
BuildRequires:  pkg-config
BuildRequires:  libtool
BuildRequires:  autoconf
BuildRequires:  meson

%description
Bidi is a free implementation of the Unicode Bidirectional (BiDi) Algorithm.
It also provides utility functions to aid in the development of interactive
editors and widgets that implement BiDi functionality. The BiDi algorithm is
a prerequisite for supporting right-to-left scripts such as Hebrew, Arabic,
Syriac, and Thaana

%package	devel
Summary:	Header and development files
Requires:	%{name} = %{version}
Requires:       pkg-config

%description	devel
It contains the libraries and header files to create applications

%prep
%setup -q

%build
mkdir build
cd build
meson -Ddocs=false \
      --prefix=%{_prefix} ..
ninja

%install
cd build && %ninja_install

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/fribidi
%{_libdir}/libfribidi.so.*

%files devel
%defattr(-, root, root)
%dir %{_includedir}/fribidi
%{_includedir}/fribidi/*
%{_libdir}/libfribidi.so
%{_libdir}/pkgconfig/fribidi.pc

%changelog
*   Thu Sep 13 2018 Him Kalyan Bordoloi <bordoloi@vmware.com> 1.0.5-1
-   Initial version
