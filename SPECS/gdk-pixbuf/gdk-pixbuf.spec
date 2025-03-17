Summary:        toolkit for image loading and pixel buffer manipulation.
Name:           gdk-pixbuf
Version:        2.42.0
Release:        9%{?dist}
URL:            http://www.gt.org
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://ftp.gnome.org/pub/gnome/sources/%{name}/2.42/%{name}-%{version}.tar.xz

Source1: license.txt
%include %{SOURCE1}

Patch0:         gdk-pixbuf-CVE-2021-46829.patch
Patch1:         CVE-2020-29385.patch

BuildRequires:  meson
BuildRequires:  cmake
BuildRequires:  libpng-devel
BuildRequires:  libtiff-devel
BuildRequires:  libX11-devel
BuildRequires:  gobject-introspection-devel
BuildRequires:  gtk-doc
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  shared-mime-info

Requires:       libpng
Requires:       libtiff
Requires:       libX11
Requires:       gobject-introspection
Requires:       libjpeg-turbo

%description
The Gdk Pixbuf is a toolkit for image loading and pixel buffer manipulation. It is used by GTK+ 2 and GTK+ 3 to load and manipulate images.

%package        devel
Summary:        Header and development files
Requires:       %{name} = %{version}-%{release}
Requires:       libpng-devel
Requires:       libtiff-devel
Requires:       libX11-devel
Requires:       shared-mime-info

%description    devel
It contains the libraries and header files to create applications

%prep
%autosetup -p1

%build
%meson \
    -Dinstalled_tests=false

%meson_build

%install
%meson_install

%post
/sbin/ldconfig
gdk-pixbuf-query-loaders --update-cache

%postun -p /sbin/ldconfig

%check
%meson_test

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so.*
%{_libdir}/gdk-pixbuf-2.0
%{_libdir}/girepository-1.0

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_datadir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig

%changelog
* Wed Jan 22 2025 Tapas Kundu <tapas.kundu@broadcom.com> 2.42.0-9
- Bump version as a part of meson upgrade
* Thu Dec 12 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 2.42.0-8
- Release bump for SRP compliance
* Fri Nov 03 2023 Kuntal Nayak <nkuntal@vmware.com> 2.42.0-7
- Fix CVE-2020-29385
* Wed Jul 19 2023 Harinadh D <hdommaraju@vmware.com> 2.42.0-6
- Fix CVE-2021-46829
* Tue Jul 04 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 2.42.0-5
- Bump version as a part of libtiff upgrade
* Wed Jun 14 2023 Shivani Agarwal <shivania2@vmware.com> 2.42.0-4
- Bump version as a part of libX11 upgrade
* Fri May 19 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 2.42.0-3
- Bump version as a part of libtiff upgrade
* Tue Dec 13 2022 Guruswamy Basavaiah <bguruswamy@vmware.com> 2.42.0-2
- Bump release as a part of libpng upgrade
* Tue Sep 06 2022 Shivani Agarwal <shivania2@vmware.com> 2.42.0-1
- Upgrade version
* Sun Jun 14 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 2.33.2-1
- Updated to version 2.33.2
* Thu May 21 2015 Alexey Makhalov <amakhalov@vmware.com> 2.31.4-1
- initial version
