%global build_if %{photon_subrelease} <= 90

Summary:        GUI library.
Name:           gtk3
Version:        3.23.3
Release:        17.1%{?dist}
URL:            http://www.gtk.org
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://ftp.gnome.org/pub/gnome/sources/gtk/3.23/gtk+-%{version}.tar.xz

Source1: license.txt
%include %{SOURCE1}

Patch0: CVE-2024-6655.patch

BuildRequires:  meson
BuildRequires:  cmake
BuildRequires:  gobject-introspection-devel
BuildRequires:  atk-devel
BuildRequires:  libXi-devel
BuildRequires:  libglvnd-devel
BuildRequires:  libepoxy-devel
BuildRequires:  at-spi2-core-devel
BuildRequires:  glib-devel
BuildRequires:  glib-schemas
BuildRequires:  fontconfig-devel
BuildRequires:  libpng-devel
BuildRequires:  harfbuzz-devel
BuildRequires:  cairo-devel
BuildRequires:  fribidi-devel
BuildRequires:  pango-devel
BuildRequires:  shared-mime-info
BuildRequires:  gdk-pixbuf-devel
BuildRequires:  libXfixes-devel
BuildRequires:  libxkbcommon-x11
BuildRequires:  libxkbcommon-devel
BuildRequires:  libX11-devel
BuildRequires:  libxml2-devel
BuildRequires:  graphene-devel
BuildRequires:  libXrandr-devel
BuildRequires:  gst-plugins-bad-devel
BuildRequires:  cups-devel
BuildRequires:  wayland-devel
BuildRequires:  wayland-protocols-devel
BuildRequires:  libXinerama-devel
BuildRequires:  libXcomposite-devel
BuildRequires:  libXdamage-devel

Requires:       libXdamage
Requires:       libXcomposite
Requires:       libXinerama
Requires:       gobject-introspection
Requires:       glib >= 2.68.0
Requires:       cairo
Requires:       cups
Requires:       harfbuzz
Requires:       gdk-pixbuf
Requires:       at-spi2-core
Requires:       pango
Requires:       libX11
Requires:       libXi
Requires:       libXext
Requires:       libXrandr
Requires:       libXfixes
Requires:       atk
Requires:       at-spi2-core
Requires:       fontconfig
Requires:       freetype2
Requires:       graphene
Requires:       gst-plugins-bad
Requires:       libglvnd-egl
Requires:       libglvnd-glx
Requires:       libglvnd-gles
Requires:       libepoxy

%description
The GTK+ 3 package contains libraries used for creating graphical user interfaces for applications.

%package        devel
Summary:        Header and development files
Requires:       %{name} = %{version}-%{release}
Requires:       gobject-introspection-devel
Requires:       libglvnd-devel
Requires:       libepoxy-devel
Requires:       pango-devel
Requires:       libXi-devel
Requires:       libXfixes-devel
Requires:       libX11-devel
Requires:       libxml2-devel
Requires:       libxkbcommon-x11
Requires:       libxkbcommon-devel
Requires:       glib-devel >= 2.68.0
Requires:       glib-schemas >= 2.68.0
Requires:       harfbuzz-devel
Requires:       atk-devel
Requires:       at-spi2-core-devel
Requires:       fontconfig-devel
Requires:       graphene-devel
Requires:       cairo-devel
Requires:       gdk-pixbuf-devel
Requires:       libXext-devel
Requires:       libXrandr-devel

%description    devel
It contains the libraries and header files to create applications

%prep
%autosetup -n gtk+-%{version} -p1
rm po/*.po* po/*.gmo

%build
export CFLAGS="-Wno-maybe-uninitialized"
%configure \
  --enable-xkb \
  --enable-xinerama \
  --enable-xrandr \
  --enable-xfixes \
  --enable-xcomposite \
  --enable-xdamage \
  --enable-wayland-backend \
  --enable-x11-backend \
  --disable-gtk-doc-html \
  --disable-gtk-doc \
  --disable-nls

%make_build

%install
%make_install %{?_smp_mflags}

%if 0%{?with_check}
%check
cd tests
%make_build
fns=$(find -name 'test*' -executable -maxdepth 1)
for fn in $fns; do
  $fn || :
done
%endif

%clean
rm -rf %{buildroot}/*

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so.*
%{_libdir}/gtk-3.0/*
%{_libdir}/girepository-1.0/
%{_datadir}/glib-2.0/*
%{_datadir}/gettext/*
%{_datadir}/gtk-doc
%{_datadir}/man

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/
%{_datadir}/gir-1.0/*
%{_datadir}/gtk-3.0/*
%{_datadir}/icons
%{_datadir}/applications
%{_datadir}/themes
%{_datadir}/aclocal
%{_sysconfdir}/gtk-3.0/

%changelog
* Sat May 16 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 3.23.3-17.1
- Bump after moving to SPECS/90
* Mon Dec 08 2025 Mukul Sikka <mukul.sikka@broadcom.com> 3.23.3-17
- Release bump due to libpng update
* Thu Nov 27 2025 Mukul Sikka <mukul.sikka@broadcom.com> 3.23.3-16
- Release bump due to libpng update
* Fri Oct 24 2025 Shivani Agarwal <shivani.agarwal@broadcom.com> 3.23.3-15
- Bump release as part of wayland upgrade
* Tue Aug 05 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 3.23.3-14
- Remove unused po files
* Wed Jan 22 2025 Tapas Kundu <tapas.kundu@broadcom.com> 3.23.3-13
- Bump version as a part of meson upgrade
* Tue Jan 07 2025 Oliver Kurth <oliver.kurth@@broadcom.com> 3.23.3-12
- add patch for CVE-2024-6655
* Mon Dec 16 2024 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 3.23.3-11
- Bump version as part of cups upgrade
* Thu Dec 12 2024 Tapas Kundu <tapas.kundu@broadcom.com> 3.23.3-10
- Release bump for SRP compliance
* Fri Dec 08 2023 Shivani Agarwal <shivania2@vmware.com> 3.23.3-9
- Bump version as part of gst-plugins-bad
* Fri Sep 29 2023 Srish Srinivasan <ssrish@vmware.com> 3.23.3-8
- Version bump as a part of cups upgrade
* Mon Jul 10 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 3.23.3-7
- Bump version as a part of cups upgrade
* Wed Jun 21 2023 Kuntal Nayak <nkuntal@vmware.com> 3.23.3-6
- Bump version as a part of libXi upgrade
* Wed Jun 14 2023 Shivani Agarwal <shivania2@vmware.com> 3.23.3-5
- Bump version as a part of libX11 upgrade
* Thu May 25 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 3.23.3-4
- Bump version as a part of libxml2 upgrade
* Wed Apr 19 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 3.23.3-3
- Bump version as a part of freetype2 upgrade
* Tue Dec 13 2022 Guruswamy Basavaiah <bguruswamy@vmware.com> 3.23.3-2
- Bump release as a part of libpng upgrade
* Mon Aug 22 2022 Shivani Agarwal <shivania2@vmware.com> 3.23.3-1
- Updated to version 3.23.3
* Wed Nov 15 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.20.8-2
- Updated build requires & requires to build with Photon 2.0
* Thu Mar 03 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.20.8-1
- Updated to version 3.20.8
* Thu Mar 03 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.19.11-1
- Updated to version 3.19.11
* Wed May 27 2015 Alexey Makhalov <amakhalov@vmware.com> 3.14.13-1
- initial version
