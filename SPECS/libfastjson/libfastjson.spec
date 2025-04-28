Summary:    A fast json library for C
Name:       libfastjson
Version:    1.2304.0
Release:    1%{?dist}
URL:        https://github.com/rsyslog/libfastjson
Group:      System Environment/Base
Vendor:     VMware, Inc.
Distribution:   Photon
BuildRequires:  libtool

Source0:    %{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

%description
LIBFASTJSON is fast json library for C
It offers a small library with essential json handling functions, suffieciently good json support and very fast in processing.

%package        devel
Summary:        Development files for libfastjson
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
This package contains libraries and header files for
developing applications that use libfastjson.

%prep
%autosetup -p1

%build
sh autogen.sh
%configure --enable-shared --disable-static
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}
find %{buildroot} -name '*.la' -delete -print

%check
make check %{?_smp_mflags}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{_libdir}/libfastjson.so.*

%files devel
%{_includedir}/libfastjson
%{_libdir}/libfastjson.so
%{_libdir}/pkgconfig/libfastjson.pc

%changelog
* Mon Apr 28 2025 Tapas Kundu <tapas.kundu@broadcom.com> 1.2304.0-1
- update to 1.2304.0
* Wed Dec 11 2024 Mukul Sikka <mukul.sikka@broadcom.com> 0.99.9-2
- Release bump for SRP compliance
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 0.99.9-1
- Automatic Version Bump
* Mon Sep 10 2018 Keerthana K <keerthanak@vmware.com> 0.99.8-1
- Updated to version 0.99.8
* Mon Apr 17 2017 Siju Maliakkal <smaliakkal@vmware.com>  0.99.4-1
- Initial version
