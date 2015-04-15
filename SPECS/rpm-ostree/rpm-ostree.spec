Summary:        Commit RPMs to an OSTree repository
Name:           rpm-ostree
Version:        2015.3
Release:        1
Source0:        rpm-ostree-%{version}.tar.gz
License:        LGPLv2+
URL:            https://github.com/cgwalters/rpm-ostree
Vendor:		VMware, Inc.
Distribution:	Photon
# We always run autogen.sh
BuildRequires: autoconf automake libtool
BuildRequires: json-glib-devel
BuildRequires: libcap
BuildRequires: ostree
BuildRequires: libgsystem
BuildRequires: rpm-devel
BuildRequires: hawkey-devel
BuildRequires: docbook-xsl
BuildRequires:	libxslt
BuildRequires:	gobject-introspection-devel
Requires:      yum
BuildRequires:	which
BuildRequires:	popt-devel
Requires:	libcap
Requires:	hawkey
Requires:	ostree
Requires:	json-glib



%description
This tool takes a set of packages, and commits them to an OSTree
repository.  At the moment, it is intended for use on build servers.

%prep
%setup -q -n %{name}-%{version}

%build
env NOCONFIGURE=1 ./autogen.sh
%configure --disable-silent-rules --enable-patched-hawkey-and-libsolv --enable-usrbinatomic
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p -c"

%files
%doc COPYING README.md
%{_bindir}/atomic
%{_bindir}/rpm-ostree
%{_libdir}/%{name}/
%{_mandir}/man1/*
