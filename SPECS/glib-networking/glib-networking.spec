Summary:    Glib networking modules
Name:       glib-networking
Version:    2.59.1
Release:    1%{?dist}
License:    GPLv2
URL:        http://wiki.gnome.org/glib-networking
Group:      System Environment/Development
Vendor:     VMware, Inc.
Distribution:   Photon
Source0:    http://ftp.gnome.org/pub/GNOME/sources/glib-networking/2.50/%{name}-%{version}.tar.xz
%define sha1 glib-networking=91b9c594712be28e4e3b2d7c60b06c20b62667ee
BuildRequires:	nettle-devel
BuildRequires:	autogen-libopts-devel
BuildRequires:	libtasn1-devel
BuildRequires:	ca-certificates
BuildRequires:  gnutls-devel
BuildRequires:	openssl-devel
BuildRequires:  intltool
BuildRequires:  glib
BuildRequires:  glib-devel
BuildRequires:  glib-schemas
BuildRequires:  meson
BuildRequires:  gnome-common
BuildRequires:  ninja-build
Requires:	nettle
Requires:	gnutls
Requires:	libtasn1
Requires:	openssl
Requires:	ca-certificates

%description
Glib-netowkring contains networking related gio modules for Glib.

%package lang
Summary: Additional language files for glib-networking
Group: System Environment/Development
Requires: glib-networking
%description lang
These are the additional language files of glib-networking.

%prep
%setup -q

%build
mkdir build &&
cd    build &&
meson --prefix=/usr            \
      -Dlibproxy_support=false \
      -Dgnome_proxy_support=false \
      -Dpkcs11_support=false .. &&
ninja

%install
cd build
DESTDIR=%{buildroot} ninja install
%find_lang %{name}

%check
ninja test

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}
%exclude %{_libdir}/debug

%files lang -f build/%{name}.lang
%defattr(-,root,root)

%changelog
*       Wed Nov 21 2018 Ashwin H <ashwinh@vmware.com> 2.59.1-1
-       Updated to 2.59.1 for make check fixes
*       Fri Sep 14 2018 Keerthana K <keerthanak@vmware.com> 2.58.0-1
-       Update to version 2.58.0
*	Mon Apr 10 2017 Danut Moraru <dmoraru@vmware.com> 2.50.0-1
-	Updated to version 2.50.0
*       Wed Oct 05 2016 ChangLee <changlee@vmware.com> 2.46.1-3
-       Modified %check
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.46.1-2
-	GA - Bump release of all rpms
*   Tue Feb 23 2016 Kumar Kaushik <kaushikk@vmware.com> 2.46.1-1
-   Updating to new version.
*   Wed Aug 12 2015 Touseef Liaqat <tliaqat@vmware.com> 2.45.1-1
-   Initial build.  First version
