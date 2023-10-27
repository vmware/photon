Summary:        Liberty Alliance Single Sign On
Name:           lasso
Version:        2.8.0
Release:        2%{?dist}
License:        GPLv2+
Group:          Development/Libraries/C++
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://lasso.entrouvert.org/
Source0:        http://dev.entrouvert.org/lasso/lasso-%{version}.tar.gz
%define sha512 lasso=d1b26608ea7cd08e4e2c40cec0ddc41e3235fd5c2cee64d989ae752bbbc276fe056455e3943a778abcc7f8e8596c85beada75df4290579e6af15e82d0e2fb5ca
BuildRequires: libxml2-devel
BuildRequires: glib-devel >= 2.68.4
BuildRequires: openssl-devel
BuildRequires: python3-six
BuildRequires: which
BuildRequires: xmlsec1-devel
Requires:      xmlsec1
Requires:      glib >= 2.68.4

%description
Lasso is a library that implements the Liberty Alliance Single Sign On
standards, including the SAML and SAML2 specifications. It allows to handle
the whole life-cycle of SAML based Federations, and provides bindings
for multiple languages.

%package devel
Summary: Lasso development headers and documentation
Group: Development/Libraries/C++
Requires: %{name} = %{version}-%{release}
Requires: glib-devel >= 2.68.4

%description devel
This package contains the header files, static libraries and development
documentation for Lasso

%prep
%autosetup

%build
./autogen.sh --disable-java \
             --disable-perl \
             --enable-php5=no \
             --disable-python \
             --disable-gtk-doc \
             --prefix=%{_prefix}

%make_build %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}
find %{buildroot} -name '*.la' -delete
find %{buildroot} -name '*.a' -delete

%check
%make_build %{?_smp_mflags} check

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%{_libdir}/liblasso.so.3*
%doc AUTHORS NEWS README
%license COPYING

%files devel

%{_libdir}/liblasso.so
%{_libdir}/pkgconfig/lasso.pc
%{_includedir}/%{name}
%{_defaultdocdir}/%{name}

%changelog
* Sat Oct 07 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 2.8.0-2
- Bump version as part of glib upgrade
* Mon Apr 04 2022 Prashant S Chauhan <psinghchauha@vmware.com> 2.8.0-1
- lasso initial build
