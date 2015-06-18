Summary:        Commit RPMs to an OSTree repository
Name:           rpm-ostree
Version:        2015.7
Release:        1%{?dist}
Source0:        rpm-ostree-%{version}.tar.gz
License:        LGPLv2+
URL:            https://github.com/cgwalters/rpm-ostree
Vendor:		VMware, Inc.
Distribution:	Photon
# We always run autogen.sh
BuildRequires: autoconf automake libtool git
BuildRequires: json-glib-devel
BuildRequires: gtk-doc
BuildRequires: libcap
BuildRequires: ostree-devel
BuildRequires: libgsystem
BuildRequires: docbook-xsl
BuildRequires:	libxslt
BuildRequires:	gobject-introspection-devel
BuildRequires:	openssl-devel
BuildRequires:	libhif-devel >= 0.2.0
BuildRequires: 	hawkey-devel >= 0.4.6
BuildRequires: 	rpm-devel >= 4.11.0
BuildRequires: 	librepo-devel >= 1.7.11
BuildRequires:	attr
BuildRequires: 	python2-libs
BuildRequires:	python2
BuildRequires: 	gobject-introspection-python

Requires:      yum
BuildRequires:	which
BuildRequires:	popt-devel
Requires:	libcap
Requires:	librepo
Requires:	hawkey
Requires:	rpm
Requires:	libhif
Requires:	ostree
Requires:	json-glib


%description
This tool takes a set of packages, and commits them to an OSTree
repository.  At the moment, it is intended for use on build servers.

%package devel
Summary: Development headers for rpm-ostree
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
Includes the header files for the rpm-ostree library.

%prep
%autosetup -Sgit -n %{name}-%{version}
git clone git://git.gnome.org/libglnx libglnx

%build
env NOCONFIGURE=1 ./autogen.sh
%configure --disable-silent-rules --enable-usrbinatomic
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot} INSTALL="install -p -c"
find %{buildroot} -name '*.la' -delete

%files
%{_bindir}/rpm-ostree
%{_bindir}/atomic
%{_libdir}/%{name}/
%{_mandir}/man*/*.gz
%{_libdir}/*.so.1*
%{_libdir}/girepository-1.0/*.typelib

%files devel
%{_libdir}/lib*.so
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{_datadir}/gir-1.0/*-1.0.gir
