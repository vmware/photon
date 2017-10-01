Name:          copenapi
Summary:       c open api spec parser
Version:       0.0.2
Release:       2%{?dist}
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
%define sha1 copenapi=64d947d4eb6e671fc6284bbca6da0201f741653f
Patch0:        copenapi-fix-status-size.patch

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
%patch0 -p1

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
*  Sat Sep 30 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.0.2-2
-  Apply patch to correct response code status size.
*  Thu Sep 28 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.0.2-1
-  Update to 0.0.2
*  Thu May 04 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.0.1-1
-  Initial build.  First version
