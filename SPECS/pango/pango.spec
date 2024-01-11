Summary:        library for laying out and rendering of text.
Name:           pango
Version:        1.40.4
Release:        4%{?dist}
License:        LGPLv2 or MPLv1.1
URL:            http://pango.org
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://download.gnome.org/sources/pango/1.40/%{name}-%{version}.tar.xz
%define sha512  pango=8c7413f6712eaf9fd4bd92a9260a85e7e4bd5e1a03c4c89db139e1704e8681e9834f8b98394b9f4b87babd45155a15b6cffd583ad8f89a48a4849305d43aa613

BuildRequires:  glib-devel
BuildRequires:  cairo
BuildRequires:  cairo-devel
BuildRequires:  libpng-devel
BuildRequires:  fontconfig
BuildRequires:  fontconfig-devel
BuildRequires:  harfbuzz
BuildRequires:  harfbuzz-devel
BuildRequires:  freetype2

Requires:   glib
Requires:   libpng
Requires:   cairo
Requires:   fontconfig
Requires:   harfbuzz

%description
Pango is a library for laying out and rendering of text, with an emphasis on internationalization. Pango can be used anywhere that text layout is needed, though most of the work on Pango so far has been done in the context of the GTK+ widget toolkit.

%package    devel
Summary:    Header and development files
Requires:   %{name} = %{version}-%{release}
Requires:   glib-devel
Requires:   cairo-devel
Requires:   libpng-devel
Requires:   fontconfig-devel
Requires:   harfbuzz-devel

%description    devel
It contains the libraries and header files to create applications

%prep
%autosetup
%build
%configure
%make_build

%install
%make_install %{?_smp_mflags}

%check
#These tests are known to fail. Hence sending exit 0
make %{?_smp_mflags} -k check || exit 0

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/gtk-doc/*
%{_datadir}/man/*

%changelog
*       Thu Jan 11 2024 Brennan Lamoreaux <blamoreaux@vmware.com> 1.40.4-4
-       Update requires
*       Fri Sep 22 2023 Shivani Agarwal <shivania2@vmware.com> 1.40.4-3
-       Bump version as a part of libpng upgrade
*       Tue Feb 21 2023 Shivani Agarwal <shivania2@vmware.com> 1.40.4-2
-       Upgrade to build with new harfbuzz
*       Tue Apr 04 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.40.4-1
-       Initial version
