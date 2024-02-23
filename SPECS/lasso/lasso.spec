Summary:        Liberty Alliance Single Sign On
Name:           lasso
Version:        2.8.0
Release:        7%{?dist}
License:        GPLv2+
Group:          Development/Libraries/C++
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://lasso.entrouvert.org

Source0: http://dev.entrouvert.org/lasso/lasso-%{version}.tar.gz
%define sha512 %{name}=d1b26608ea7cd08e4e2c40cec0ddc41e3235fd5c2cee64d989ae752bbbc276fe056455e3943a778abcc7f8e8596c85beada75df4290579e6af15e82d0e2fb5ca

BuildRequires: libxml2-devel
BuildRequires: glib-devel
BuildRequires: openssl-devel
BuildRequires: python3-six
BuildRequires: which
BuildRequires: xmlsec1-devel

Requires:      xmlsec1

%description
Lasso is a library that implements the Liberty Alliance Single Sign On
standards, including the SAML and SAML2 specifications. It allows to handle
the whole life-cycle of SAML based Federations, and provides bindings
for multiple languages.

%package devel
Summary: Lasso development headers and documentation
Group: Development/Libraries/C++
Requires: %{name} = %{version}-%{release}
Requires: glib-devel

%description devel
This package contains the header files, static libraries and development
documentation for Lasso

%prep
%autosetup -p1

%build
sh ./autogen.sh --disable-java \
             --disable-perl \
             --enable-php5=no \
             --disable-python \
             --disable-gtk-doc \
             --prefix=%{_prefix}

%make_build

%install
%make_install %{?_smp_mflags}
find %{buildroot} -name '*.a' -delete

%check
%make_build check

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/liblasso.so.*

%files devel
%defattr(-,root,root)
%{_libdir}/liblasso.so
%{_libdir}/pkgconfig/lasso.pc
%{_includedir}/%{name}
%{_docdir}/%{name}

%changelog
* Tue Feb 20 2024 Ashwin Dayanand Kamat <ashwin.kamat@broadcom.com> 2.8.0-7
- Bump version as a part of libxml2 upgrade
* Sun Nov 19 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.8.0-6
- Bump version as a part of openssl upgrade
* Mon Sep 18 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.8.0-5
- Fix devel package requires
* Wed Apr 19 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 2.8.0-4
- Bump version as a part of libxml2 upgrade
* Tue Dec 06 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 2.8.0-3
- Bump version as a part of xmlsec1 upgrade
* Fri Oct 21 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 2.8.0-2
- Bump version as a part of xmlsec1 upgrade
* Mon Apr 04 2022 Prashant S Chauhan <psinghchauha@vmware.com> 2.8.0-1
- lasso initial build
