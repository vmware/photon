Summary:    A fast json library for C
Name:       libfastjson
Version:    0.99.8
Release:    1%{?dist}
License:    MIT
URL:        https://github.com/rsyslog/libfastjson
Source0:    %{name}-%{version}.tar.gz
%define sha1 libfastjson=df1ab2602bc73cf4c49a16860cf6a065b636fe6d
Group:      System Environment/Base
Vendor:     VMware, Inc.
Distribution:   Photon
BuildRequires:  libtool

%description
LIBFASTJSON is fast json library for C
It offers a small library with essential json handling functions, suffieciently good json support and very fast in processing. 

%package	devel
Summary:	Development files for libfastjson
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}


%description	devel
This package contains libraries and header files for
developing applications that use libfastjson.

%prep
%setup -q
%build
sh autogen.sh
%configure --enable-shared --disable-static
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -delete -print

%check
make check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{_libdir}/libfastjson.so.*

%files devel
%{_includedir}/libfastjson
%{_libdir}/libfastjson.so
%{_libdir}/pkgconfig/libfastjson.pc


%changelog
*       Fri Mar 22 2019 Keerthana K <keerthanak@vmware.com> 0.99.8-1
-       Initial version
