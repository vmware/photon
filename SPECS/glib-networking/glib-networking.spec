Summary:    Glib networking modules
Name:       glib-networking
Version:    2.46.1
Release:    3%{?dist}
License:    GPLv2
URL:        http://wiki.gnome.org/glib-networking
Group:      System Environment/Development
Vendor:     VMware, Inc.
Distribution:   Photon
Source0:    http://ftp.gnome.org/pub/GNOME/sources/glib-networking/2.46/%{name}-%{version}.tar.xz
%define sha1 glib-networking=5e44eb1227eef11eeea8b003207611fa4d3b1fa1
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
Requires:	nettle
#Requires:	autogen-libopts
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
*   Sat Apr 17 2021 Shreenidhi Shedi <sshedi@vmware.com> 2.46.1-3
-   Bump version as a part of nettle upgrade
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.46.1-2
-	GA - Bump release of all rpms
*   Tue Feb 23 2016 Kumar Kaushik <kaushikk@vmware.com> 2.46.1-1
-   Updating to new version.
*   Wed Aug 12 2015 Touseef Liaqat <tliaqat@vmware.com> 2.45.1-1
-   Initial build.  First version
