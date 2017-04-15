Summary:	GIO-based library with Unix/Linux specific API
Name:		libgsystem
Version:	2015.1
Release:	4%{?dist}
Group:		Development/Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/libgsystem/%{version}/%{name}-%{version}.tar.xz
%define sha1 libgsystem=9b14593c87a386d2d3c01490ba126047aa6eba30
License:	LGPLv2+
URL:		https://wiki.gnome.org/Projects/LibGSystem
Vendor:		VMware, Inc.
Distribution:	Photon
# We always run autogen.sh
BuildRequires:	autoconf automake libtool
# For docs
BuildRequires:	gtk-doc
# Core requirements
BuildRequires:  glib-devel
BuildRequires:	pkg-config
BuildRequires:	attr-devel
BuildRequires:  rpm
BuildRequires:	autoconf
BuildRequires:	which
BuildRequires:	pcre-devel
BuildRequires:	libffi-devel
BuildRequires:	python2
BuildRequires:	python2-libs
BuildRequires:	gobject-introspection-devel
BuildRequires:	gobject-introspection-python
Requires:	glib
Requires:	libffi
Requires:	pcre
%description
LibGSystem is a GIO-based library usable as a "git submodule",
targeted primarily for use by operating system components.

%prep
%setup -q

%build
env NOCONFIGURE=1 ./autogen.sh
%configure --disable-silent-rules \
	   --enable-gtk-doc
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot} INSTALL="install -p -c"
find %{buildroot} -name '*.la' -delete

%check
make %{?_smp_mflags} check

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%doc COPYING README
%{_libdir}/*.so*
%{_libdir}/pkgconfig/*
%{_includedir}/*
%{_libdir}/girepository-1.0/GSystem-1.0.typelib
%{_datarootdir}/gir-1.0/GSystem-1.0.gir

%changelog
*   Thu Nov 24 2016 Alexey Makhalov <amakhalov@vmware.com> 2015.1-4
-   BuildRequired attr-devel.
*   Thu Nov 17 2016 Alexey Makhalov <amakhalov@vmware.com> 2015.1-3
-   Use %setup instead of %autosetup
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2015.1-2
-   GA - Bump release of all rpms
*   Mon Nov 24 2014 Divya Thaluru <dthaluru@vmware.com> 2014.2-1
-   Initial build. First version
