Summary:    libsoup HTTP client/server library
Name:       libsoup
Version:    2.50.0
Release:    1
License:    GPLv2
URL:        http://wiki.gnome.org/LibSoup
Group:      System Environment/Development
Vendor:     VMware, Inc.
Distribution:   Photon
Source0:    http://ftp.gnome.org/pub/GNOME/sources/libsoup/2.50/%{name}-%{version}.tar.xz
BuildRequires:   glib
BuildRequires:   glib-devel
BuildRequires:   gobject-introspection
BuildRequires:   libxml2-devel
BuildRequires:   intltool
BuildRequires:   python2
BuildRequires:   python2-libs
BuildRequires:   python2-devel
BuildRequires:   python2-tools

%description
libsoup is HTTP client/server library for GNOME

%package devel
Summary: Header files for libsoup
Group: System Environment/Development
Requires: libsoup
%description devel
Header files for libsoup.

%package doc
Summary: gtk-doc files for libsoup
Group: System Environment/Development
Requires: libsoup
%description doc
gtk-doc files for libsoup.

%package lang
Summary: Additional language files for libsoup
Group: System Environment/Development
Requires: libsoup
%description lang
These are the additional language files of libsoup.

%prep
%setup -q

%build
export CFLAGS="%{optflags}"
./configure  --prefix=%{_prefix} \
    --disable-tls-check

make %{?_smp_mflags}

%install
rm -rf %{buildroot}%{_infodir}
make DESTDIR=%{buildroot} install
%find_lang %{name}

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/*
%exclude %{_libdir}/debug

%files devel
%{_includedir}/*

%files doc
%{_datadir}/*

%files lang -f %{name}.lang
%defattr(-,root,root)

%changelog
*   Fri Jun 5 2015 Touseef Liaqat <tliaqat@vmware.com> 2.50.0-1
-   Initial build.  First version
