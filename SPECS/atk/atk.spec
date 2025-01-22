Summary:        Accessibility interfaces to have full access to view and control running applications.
Name:           atk
Version:        2.38.0
Release:        3%{?dist}
URL:            http://www.gnome.org
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://ftp.gnome.org/pub/gnome/sources/%{name}/2.16/%{name}-%{version}.tar.xz
%define sha512  atk=dffd0a0814a9183027c38a985d86cb6544858e9e7d655843e153440467957d6bc1abd9c9479a57078aea018053410438a30a9befb7414dc79020b223cd2c774b

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  cmake
BuildRequires:  meson
BuildRequires:  glib-devel
BuildRequires:  gobject-introspection-devel
Requires:       glib

%description
ATK provides the set of accessibility interfaces that are implemented by other toolkits and applications. Using the ATK interfaces, accessibility tools have full access to view and control running applications.

%package        devel
Summary:        Header and development files for
Requires:       %{name} = %{version}-%{release}
Requires:       gobject-introspection-devel

%description    devel
It contains the libraries and header files to create applications

%prep
%autosetup -p1

%build
%meson
%meson_build

%install
%meson_install

%ldconfig_scriptlets

%check
%meson_test

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_libdir}/*.so.*
%{_datadir}/*
%{_libdir}/girepository-1.0

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig

%changelog
*   Wed Jan 22 2025 Tapas Kundu <tapas.kundu@broadcom.com> 2.38.0-3
-   Bump version as a part of meson upgrade
*   Wed Dec 11 2024 HarinadhD <harinadh.dommaraju@broadcom.com> 2.38.0-2
-   Release bump for SRP compliance
*   Fri Aug 19 2022 Shivani Agarwal <shivania2@vmware.com> 2.38.0-1
-   Upgrade version 2.38.0
*   Thu May 21 2015 Alexey Makhalov <amakhalov@vmware.com> 2.16.0-1
-   initial version
