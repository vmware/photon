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
BuildRequires: curl-devel
Source0:       %{name}-%{version}.tar.gz
%define sha1 copenapi=b44e37254aff4c35edb1e65739481e558f427d67

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
*  Mon May 08 2017 Dheeraj Shetty <dheerajs@vmware.com> 0.0.1-1
-  Changed version to 0.0.1
*  Thu May 04 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.1-1
-  Initial build.  First version
