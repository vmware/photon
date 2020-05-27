Summary:	GIO-based library with Unix/Linux specific API
Name:		libgsystem
Version:	2015.2
Release:	2%{?dist}
Group:		Development/Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/libgsystem/%{version}/%{name}-%{version}.tar.gz
%define sha1 libgsystem=d7f12beb17d3a3b288d68ca2cdcb595f9e5fccea
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
BuildRequires:	libcap-devel
BuildRequires:	libffi-devel
BuildRequires:	python3
BuildRequires:	python3-libs
BuildRequires:	gobject-introspection-devel
BuildRequires:	gobject-introspection-python
Requires:	glib
Requires:	libcap
Requires:	libffi
Requires:	pcre
Requires:	gobject-introspection
%description
LibGSystem is a GIO-based library usable as a "git submodule",
targeted primarily for use by operating system components.

%package        devel
Summary:        Development files for libgsystem
Requires:       %{name} = %{version}
Requires:       gobject-introspection-devel

%description    devel
The libgsystem-devel package contains libraries and header files for
developing applications.

%prep
%setup -qn libgsystem

%build
alias python=python3
env NOCONFIGURE=1 ./autogen.sh
%configure --disable-silent-rules \
			   --enable-gtk-doc
make %{?_smp_mflags}

%install
alias python=python3
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
%{_libdir}/girepository-1.0/GSystem-1.0.typelib

%files devel
%{_includedir}/*
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/*
%{_datadir}/gir-*/*.gir

%changelog
*   Tue Sep 18 2018 Keerthana K <keerthanak@vmware.com> 2015.2-2
-   Removed % from autosetup in the changelog to address the
-   build break with latest RPM version.
*   Wed Apr 26 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 2015.2-1
-   Updated to version 2015.2
*   Thu Nov 24 2016 Alexey Makhalov <amakhalov@vmware.com> 2015.1-4
-   BuildRequired attr-devel.
*   Thu Nov 17 2016 Alexey Makhalov <amakhalov@vmware.com> 2015.1-3
-   Use setup instead of autosetup
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2015.1-2
-   GA - Bump release of all rpms
*   Mon Nov 24 2014 Divya Thaluru <dthaluru@vmware.com> 2014.2-1
-   Initial build. First version
