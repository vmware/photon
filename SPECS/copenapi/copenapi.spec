Name:          copenapi
Summary:       c open api spec parser
Version:       0.0.1
Release:       1%{?dist}
Group:         Development/Libraries
Vendor:        VMware, Inc.
Distribution:  Photon
License:       Apache 2.0
URL:           https://www.github.com/vmware/copenapi
BuildArch:     x86_64
Requires:      jansson
Requires:      curl
BuildRequires: jansson-devel
BuildRequires: curl
Source0:       %{name}-%{version}.tar.gz
%define sha1 copenapi=0cfd79271ec3639129a36c4a5c3375cca8c54f32

%description
copenapi is an openapi parser written in c

%package devel
Summary: copenapi development files
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
copenapi development files

%prep
%setup -q

%build
autoreconf -mif
./configure \
    --prefix=%{_prefix} \
    --disable-static
make

%install

make install DESTDIR=$RPM_BUILD_ROOT
rm -f %{buildroot}%{_libdir}/*.la

%post
    /sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so.*

%files devel
%{_libdir}/pkgconfig/copenapi.pc
%{_includedir}/*
%{_libdir}/*.so

%changelog
*  Thu May 04 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.0.1-1
-  Initial build.  First version
