Name:           fribidi
Version:        1.0.5
Release:        1
Summary:        Free Implementation of BiDi Algorithm
License:        LGPL-2.1
Group:          System/Libraries
Url:            http://fribidi.org/
Provides:       locale(ar;he)
Source:         https://github.com/fribidi/fribidi/archive/%{name}-%{version}.tar.gz
%define sha1 fribidi=616619aa88f4a89350301b7f482d6c1d807933ee
BuildRequires:  pkg-config
BuildRequires:	libtool
BuildRequires:	autoconf
BuildRequires:	meson

%description
This library implements the algorithm as described in the "Unicode
Standard Annex #9, the Bidirectional Algorithm,
http://www.unicode.org/unicode/reports/tr9/".

%package devel
Summary:        Development Files for FriBiDi
Group:          Development/Libraries/C and C++
Requires:       %{name} = %{version}
Requires:       pkg-config

%description devel
This package provides headers and manual files for FriBiDi.

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
