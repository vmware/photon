Summary:        Port of libtls from LibreSSL to OpenSSL
Name:           libretls
Version:        3.8.1
Release:        1%{?dist}
URL:            https://git.causal.agency/libretls/about
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://causal.agency/libretls/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires: openssl-devel

Requires: openssl

%description
LibreTLS is a port of libtls from LibreSSL to OpenSSL. OpenBSD's libtls is a
new TLS library, designed to make it easier to write foolproof applications.

%package devel
Summary:  Development files for libretls
Requires: %{name} = %{version}-%{release}
Requires: pkg-config

%description devel
The libretls-devel package contains libraries and header files for developing
applications that use libtls.

%prep
%autosetup -p1

%build
%configure --disable-static
%make_build

%install
%make_install %{?_smp_mflags}

rm -rf %{buildroot}%{_mandir}

%if 0%{?with_check}
%check
# this currently does nothing
%make_build check
%endif

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/libtls.so.*

%files devel
%defattr(-,root,root)
%{_libdir}/libtls.so
%{_libdir}/pkgconfig/libtls.pc
%{_includedir}/tls.h

%changelog
* Tue Sep 10 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 3.8.1-1
- Initial version. Needed by bsd-netcat.
