%global debug_package %{nil}
Summary:        Build Tools
Name:           mm-common
Version:        1.0.4
Release:        1%{?dist}
License:        GPLv2+
URL:            https://gitlab.gnome.org/GNOME/mm-common
Group:          Applications/System
Source0:        https://gitlab.gnome.org/GNOME/mm-common/-/archive/%{version}/mm-common-%{version}.tar.gz
%define sha512    mm-common=58a6202115a7c888306d169a0850c5cdbe44c9bbf1e29a4569051a9feeea47bce830615640d2b83ba4396a9d930d65834964e91c534ffe9922eecfcfbf1259c9
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  wget

%description
This module is part of the GNOME C++ bindings effort <http://www.gtkmm.org/>.
The mm-common module provides the build infrastructure and utilities shared among the GNOME C++ binding libraries.
It is only a required dependency for building the C++ bindings from the gnome.org version make control repository.
An installation of mm-common is not required for building tarball releases, unless configured to use maintainer-mode.

%prep
%autosetup

%build
./autogen.sh
%configure --enable-network
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} %{?_smp_mflags} install

%check
make %{?_smp_mflags} check

%files
%defattr(-,root,root)
%{_bindir}/mm-common-get
%{_bindir}/mm-common-prepare
%{_datadir}/aclocal/*.m4
%{_mandir}/man1/*.gz
%{_datadir}/doc/mm-common/*
%{_datadir}/pkgconfig/*.pc
%{_datadir}/mm-common/build/*.*
%{_datadir}/mm-common/doctags/*.tag
%{_datadir}/mm-common/doctool/*.*

%changelog
*   Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 1.0.4-1
-   Automatic Version Bump
*   Mon Oct 5 2020 Michelle Wang <michellew@vmware.com> 1.0.2-1
-   Initial build and add this for libsigc++ build requires
