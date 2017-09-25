Summary:        Commit RPMs to an OSTree repository
Name:           rpm-ostree
Version:        2017.4
Release:        5%{?dist}
Source0:        rpm-ostree-%{version}.tar.gz
%define sha1    rpm-ostree=d34882a455afbf0b57617c0962725276967e838a
Source1:        libglnx-0c52d85.tar.gz
%define sha1    libglnx=137767ad957f37d6210aaa6b28e4333a42aa9fad
Source2:        libdnf-2086268.tar.gz
%define sha1    libdnf=4e913da416c61a5525f94ef09f38c658179e3e25
Source3:        mk-ostree-host.sh
Source4:        function.inc
Patch0:         rpm-ostree-libdnf-build.patch
Patch1:         Set-arch.patch
Patch2:         Makefile-test.patch
License:        LGPLv2+
URL:            https://github.com/projectatomic/rpm-ostree
Vendor:         VMware, Inc.
Distribution:   Photon
# We always run autogen.sh
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  check
BuildRequires:  cmake
BuildRequires:  libtool
BuildRequires:  git
BuildRequires:  json-glib-devel
BuildRequires:  gtk-doc
BuildRequires:  libcap-devel
BuildRequires:  ostree-devel
BuildRequires:  libgsystem-devel
BuildRequires:  docbook-xsl
BuildRequires:  libxslt
BuildRequires:  gobject-introspection-devel
BuildRequires:  openssl-devel
BuildRequires:  rpm-devel >= 4.11.0
BuildRequires:  librepo-devel >= 1.7.11
BuildRequires:  attr-devel
BuildRequires:  python2-libs
BuildRequires:  python2
BuildRequires:  gobject-introspection-python
BuildRequires:  autogen
BuildRequires:  libsolv-devel >= 0.6.26-3
BuildRequires:  systemd-devel
BuildRequires:  libarchive-devel
BuildRequires:  gperf
BuildRequires:  which
BuildRequires:  popt-devel
BuildRequires:  createrepo
BuildRequires:  jq
BuildRequires:  photon-release
BuildRequires:  photon-repos
BuildRequires:  bubblewrap
BuildRequires:  dbus

Requires:       libcap
Requires:       librepo
Requires:       openssl
Requires:       ostree
Requires:       libgsystem
Requires:       json-glib
Requires:       libsolv >= 0.6.26-3
Requires:       bubblewrap

%description
This tool takes a set of packages, and commits them to an OSTree
repository.  At the moment, it is intended for use on build servers.

%package devel
Summary: Development headers for rpm-ostree
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
Includes the header files for the rpm-ostree library.

%package host
Summary: File for rpm-ostree-host creation
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description host
Includes the scripts for rpm-ostree host creation

%prep
%setup -q
tar xf /usr/src/photon/SOURCES/libglnx-0c52d85.tar.gz --no-same-owner
tar xf /usr/src/photon/SOURCES/libdnf-2086268.tar.gz --no-same-owner
%patch0 -p0
%patch1 -p1
%patch2 -p1

%build
sed -i '/-DBUILD_SHARED_LIBS/a -DWITH_MAN=OFF \\' configure.ac
env NOCONFIGURE=1 ./autogen.sh
%configure --disable-silent-rules --enable-gtk-doc
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot} INSTALL="install -p -c"
find %{buildroot} -name '*.la' -delete
install -p -m 755 %{SOURCE3} %{buildroot}%{_bindir}/rpm-ostree-host
install -p -m 755 %{SOURCE4} %{buildroot}%{_bindir}/rpm-ostree-host
%check
make check

%files
%{_bindir}/*
%{_libdir}/%{name}/
%{_mandir}/man*/*.gz
%{_libdir}/*.so.1*
%{_libdir}/girepository-1.0/*.typelib
%{_sysconfdir}/dbus-1/system.d/*
%{_prefix}%{_unitdir}/*.service
%{_libexecdir}/*
%{_datadir}/dbus-1/system-services/*

%files devel
%{_libdir}/lib*.so
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{_datadir}/gtk-doc/html/*
%{_datadir}/gir-1.0/*-1.0.gir

%files host
%{_bindir}/rpm-ostree-host/mk-ostree-host.sh
%{_bindir}/rpm-ostree-host/function.inc

%changelog
*   Fri Sep 22 2017 Dheeraj Shetty <dheerajs@vmware.com> 2017.4-5
-   Add support to generate rpm-ostree host
*   Fri Sep 15 2017 Dheeraj Shetty <dheerajs@vmware.com> 2017.4-4
-   Changes for Makecheck
*   Thu Aug 03 2017 Xiaolin Li <xiaolinl@vmware.com> 2017.4-3
-   Added bubblewrap to requires.
*   Mon May 08 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 2017.4-2
-   Use libgsystem-devel to build instead of libgsystem.
*   Fri Apr 21 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2017.4-1
-   Update to 2017.4
*   Mon Dec 19 2016 Xiaolin Li <xiaolinl@vmware.com> 2015.7-5
-   BuildRequires libsolv-devel.
*   Thu Nov 24 2016 Alexey Makhalov <amakhalov@vmware.com> 2015.7-4
-   BuildRequired attr-devel.
*   Wed Oct 05 2016 ChangLee <changlee@vmware.com> 2015.7-3
-   Modified %check
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2015.7-2
-   GA - Bump release of all rpms
*   Thu Jun 18 2015 Anish Swaminathan <anishs@vmware.com> 2015.7-1
-   Added new version of rpm-ostree
