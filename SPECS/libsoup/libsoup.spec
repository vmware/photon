Summary:    libsoup HTTP client/server library
Name:       libsoup
Version:    2.53.90
Release:    4%{?dist}
License:    GPLv2
URL:        http://wiki.gnome.org/LibSoup
Group:      System Environment/Development
Vendor:     VMware, Inc.
Distribution:   Photon
Source0:    http://ftp.gnome.org/pub/GNOME/sources/libsoup/2.50/%{name}-%{version}.tar.xz
%define sha1 libsoup=d8511f0a8a07e4f5125c9354be7d43d62ea55eb3
Patch0:          CVE-2017-2885.patch
Patch1:          CVE-2018-12910.patch
BuildRequires:   glib
BuildRequires:   glib-devel
BuildRequires:   gobject-introspection
BuildRequires:   libxml2-devel
BuildRequires:   intltool
BuildRequires:   python2
BuildRequires:   python2-libs
BuildRequires:   python2-devel
BuildRequires:   python2-tools
BuildRequires:   glib-networking
BuildRequires:   autogen
Requires:        libxml2
Requires:        glib-networking

%description
libsoup is HTTP client/server library for GNOME

%package devel
Summary: Header files for libsoup
Group: System Environment/Development
Requires: libsoup
Requires: libxml2-devel
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
%patch0 -p1
%patch1 -p1

%build
export CFLAGS="%{optflags}"
./configure  --prefix=%{_prefix} --disable-vala

make %{?_smp_mflags}

%install
rm -rf %{buildroot}%{_infodir}
make DESTDIR=%{buildroot} install
%find_lang %{name}
find %{buildroot}%{_libdir} -name '*.la' -delete

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/*.so.*
%exclude %{_libdir}/debug

%files devel
/usr/include/*
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/pkgconfig/*

%files doc
/usr/share/*

%files lang -f %{name}.lang
%defattr(-,root,root)

%changelog
*   Mon Sep 03 2018 Ankit Jain <ankitja@vmware.com> 2.53.90-4
-   Fix for CVE-2018-12910
*   Mon Jun 18 2018 Tapas Kundu <tkundu@vmware.com> 2.53.90-3
-   CVE-2017-2885
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.53.90-2
-	GA - Bump release of all rpms
*   Fri Feb 26 2016 Kumar Kaushik <kaushikk@vmware.com> 2.53.90-1
-   Updated version.
*   Mon Oct 12 2015 Xiaolin Li <xiaolinl@vmware.com> 2.50.0-5
-   Moving static lib files to devel package.
*   Fri Oct 9 2015 Xiaolin Li <xiaolinl@vmware.com> 2.50.0-4
-   Removing la files from packages.
*   Mon Jul 20 2015 Divya Thaluru <dthaluru@vmware.com> 2.50.0-3
-   Addinf libxml2 to Requires 
*   Mon Jul 13 2015 Alexey Makhalov <amakhalov@vmware.com> 2.50.0-2
-   Exclude /usr/lib/debug
*   Fri Jun 5 2015 Touseef Liaqat <tliaqat@vmware.com> 2.50.0-1
-   Initial build.  First version
