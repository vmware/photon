Summary:        toolkit for image loading and pixel buffer manipulation.
Name:           gdk-pixbuf
Version:        2.42.0
Release:        7%{?dist}
License:        LGPLv2+
URL:            http://www.gt.org
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://ftp.gnome.org/pub/gnome/sources/%{name}/2.42/%{name}-%{version}.tar.xz
%define sha512 %{name}=c9962d42e5bf13514091234342e259be1e06b2c4dea2936e16104a3b58f0b6837f070224c04be9541d75f5ea34d1da398f178a1eed1f9059f6429faf5c223e34
Patch0:         gdk-pixbuf-CVE-2021-46829.patch
Patch1: CVE-2021-44648.patch
Patch2: CVE-2020-29385.patch

BuildRequires:  meson
BuildRequires:  cmake
BuildRequires:  curl-devel
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
* Wed Jan 22 2025 Tapas Kundu <tapas.kundu@broadcom.com> 2.42.0-7
- Bump version as a part of meson upgrade
* Fri Nov 03 2023 Kuntal Nayak <nkuntal@vmware.com> 2.42.0-6
- Fix CVE-2021-44648 and CVE-2020-29385
* Tue Jul 04 2023 Harinadh D <hdommaraju@vmware.com> 2.42.0-5
- Fix CVE-2021-46829
* Mon Jun 26 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 2.42.0-4
- Bump version as a part of libtiff upgrade
* Wed Jun 14 2023 Shivani Agarwal <shivania2@vmware.com> 2.42.0-3
- Bump version as a part of libX11 upgrade
* Fri Jan 06 2023 Michelle Wang <michellew@vmware.com> 2.42.0-2
- Release version bump up for gdk and libtiff update
* Tue Sep 06 2022 Shivani Agarwal <shivania2@vmware.com> 2.42.0-1
- Upgrade version
* Sun Jun 14 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 2.33.2-1
- Updated to version 2.33.2
* Thu May 21 2015 Alexey Makhalov <amakhalov@vmware.com> 2.31.4-1
- initial version
