Summary:    Glib networking modules
Name:       glib-networking
Version:    2.45.1
Release:    1%{?dist}
License:    GPLv2
URL:        http://wiki.gnome.org/glib-networking
Group:      System Environment/Development
Vendor:     VMware, Inc.
Distribution:   Photon
Source0:    http://ftp.gnome.org/pub/GNOME/sources/glib-networking/2.45/%{name}-%{version}.tar.xz
%define sha1 glib-networking=e6e17d1d6ed86a99db228fcf3ea1bd7f844a0cb5
BuildRequires:	nettle-devel
BuildRequires:	autogen-devel
BuildRequires:	libtasn1-devel
BuildRequires:	ca-certificates
BuildRequires:  gnutls-devel
BuildRequires:	openssl-devel
BuildRequires:  intltool
BuildRequires:  glib
BuildRequires:  glib-devel
BuildRequires:  glib-schemas
Requires:	nettle
Requires:	autogen
Requires:   gnutls
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
export CFLAGS="%{optflags}"
./configure  --prefix=%{_prefix} \
    --with-ca-bundle=/etc/pki/tls/certs/ca-bundle.crt

make %{?_smp_mflags}

%install
rm -rf %{buildroot}%{_infodir}
make DESTDIR=%{buildroot} install
%find_lang %{name}

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}
%exclude %{_libdir}/debug

%files lang -f %{name}.lang
%defattr(-,root,root)

%changelog
*   Wed Aug 12 2015 Touseef Liaqat <tliaqat@vmware.com> 2.45.1-1
-   Initial build.  First version
