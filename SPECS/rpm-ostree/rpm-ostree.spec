Summary:        Commit RPMs to an OSTree repository
Name:           rpm-ostree
Version:        2019.3
Release:        10%{?dist}
License:        LGPLv2+
URL:            https://github.com/projectatomic/rpm-ostree
Vendor:         VMware, Inc.
Distribution:   Photon
Group:          Applications/System

Source0:        https://github.com/projectatomic/rpm-ostree/releases/download/v%{version}/rpm-ostree-%{version}.tar.xz
%define sha512  %{name}=3960fea97b0716746f9d9f8748244d3abe258f4f04c1120c807284cfc82c260a5bdc836b47df41c2a510d3a4af2b347454c8a3a34cf4d43a96bd04142ae8eeaa
Source3:        mk-ostree-host.sh
Source4:        function.inc
Source5:        mkostreerepo

Patch0:         rpm-ostree-libdnf-build.patch
Patch1:         rpm-ostree-disable-selinux.patch
Patch2:         0001-rust-vendor-Fix-for-uninitialized-mem.patch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  check
BuildRequires:  cmake
BuildRequires:  libtool
BuildRequires:  git
BuildRequires:  json-glib-devel
BuildRequires:  json-c-devel
BuildRequires:  gtk-doc
BuildRequires:  libcap-devel
BuildRequires:  sqlite-devel
BuildRequires:  cppunit-devel
BuildRequires:  polkit-devel
BuildRequires:  ostree-devel
BuildRequires:  libgsystem-devel
BuildRequires:  docbook-xsl
BuildRequires:  libxslt
BuildRequires:  gobject-introspection-devel
BuildRequires:  openssl-devel
BuildRequires:  rpm-devel
BuildRequires:  librepo-devel
BuildRequires:  attr-devel
BuildRequires:  python2-libs
BuildRequires:  python3-xml
BuildRequires:  python2
BuildRequires:  gobject-introspection-python
BuildRequires:  autogen
BuildRequires:  libsolv-devel
BuildRequires:  libsolv
BuildRequires:  systemd-devel
BuildRequires:  libarchive-devel
BuildRequires:  gperf
BuildRequires:  which
BuildRequires:  popt-devel
BuildRequires:  createrepo_c
BuildRequires:  jq
BuildRequires:  photon-release
BuildRequires:  photon-repos
BuildRequires:  bubblewrap
BuildRequires:  dbus
BuildRequires:  rust
BuildRequires:  libmodulemd-devel
BuildRequires:  gpgme-devel

Requires:       libcap
Requires:       librepo
Requires:       openssl
Requires:       ostree
Requires:       ostree-libs
Requires:       ostree-grub2
Requires:       libgsystem
Requires:       json-glib
Requires:       libsolv
Requires:       bubblewrap

%description
This tool takes a set of packages, and commits them to an OSTree
repository.  At the moment, it is intended for use on build servers.

%package    devel
Summary:    Development headers for rpm-ostree
Group:      Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
Includes the header files for the rpm-ostree library.

%package    host
Summary:    File for rpm-ostree-host creation
Group:      Development/Libraries
Requires: %{name} = %{version}-%{release}

%description host
Includes the scripts for rpm-ostree host creation

%package    repo
Summary:    File for Repo Creation to act as server
Group:      Applications/System
Requires: %{name} = %{version}-%{release}

%description repo
Includes the scripts for rpm-ostree repo creation to act as server

%prep
%autosetup -p1

%build
env NOCONFIGURE=1 ./autogen.sh
%configure --disable-silent-rules --enable-gtk-doc
%make_build

%install
%make_install
find %{buildroot} -name '*.la' -delete
install -d %{buildroot}%{_bindir}/rpm-ostree-host
install -d %{buildroot}%{_bindir}/rpm-ostree-server
install -p -m 755 -D %{SOURCE3} %{buildroot}%{_bindir}/rpm-ostree-host
install -p -m 644 -D %{SOURCE4} %{buildroot}%{_bindir}/rpm-ostree-host
install -p -m 755 -D %{SOURCE5} %{buildroot}%{_bindir}/rpm-ostree-server

%files
%{_bindir}/*
%{_libdir}/%{name}/
%{_libdir}/*.so.1*
%{_libdir}/girepository-1.0/*.typelib
%{_sysconfdir}/dbus-1/system.d/*
%{_prefix}%{_unitdir}/*.service
%{_libexecdir}/*
%{_datadir}/dbus-1/system-services/*
%config(noreplace) %{_sysconfdir}/rpm-ostreed.conf
%{_libdir}/systemd/system/rpm-ostreed-automatic.timer
%{_datadir}/bash-completion/completions/rpm-ostree
%{_datadir}/dbus-1/interfaces/org.projectatomic.rpmostree1.xml
%{_datadir}/polkit-1/actions/org.projectatomic.rpmostree1.policy
%{_mandir}/man1/rpm-ostree.1.gz
%{_mandir}/man5/rpm-ostreed*
%{_mandir}/man8/rpm-ostreed*

%files devel
%{_libdir}/lib*.so
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{_datadir}/gtk-doc/html/*
%{_datadir}/gir-1.0/*-1.0.gir

%files host
%{_bindir}/rpm-ostree-host/mk-ostree-host.sh
%{_bindir}/rpm-ostree-host/function.inc

%files repo
%{_bindir}/rpm-ostree-server/mkostreerepo

%changelog
*   Thu Nov 23 2023 Ankit Jain <ankitja@vmware.com> 2019.3-10
-   Updated vendor/rayor to fix unitialized mem issue
*   Sun Jun 19 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 2019.3-9
-   Bump version as a part of libxslt upgrade
*   Mon Jan 24 2022 Ankit Jain <ankitja@vmware.com> 2019.3-8
-   Version Bump to build with new version of cmake
*   Thu Oct 07 2021 Tapas Kundu <tkundu@vmware.com> 2019.3-7
-   Added python3-xml as build requires
*   Wed Aug 18 2021 Shreenidhi Shedi <sshedi@vmware.com> 2019.3-6
-   Bump version as a part of rpm upgrade
*   Tue Jun 23 2020 Ankit Jain <ankitja@vmware.com> 2019.3-5
-   Added sshd and sshd-keygen in units to enable it on bootup
*   Fri Jun 05 2020 Ankit Jain <ankitja@vmware.com> 2019.3-4
-   Modified mkostreerepo with updated repos
*   Thu Oct 24 2019 Ankit Jain <ankitja@vmware.com> 2019.3-3
-   Added for ARM Build
*   Fri Sep 20 2019 Ankit Jain <ankitja@vmware.com> 2019.3-2
-   Added script to create repo data to act as ostree-server
*   Tue May 14 2019 Ankit Jain <ankitja@vmware.com> 2019.3-1
-   Initial version of rpm-ostree
