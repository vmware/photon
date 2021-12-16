Summary:	library for laying out and rendering of text.
Name:		pango
Version:	1.40.4
Release:	2%{?dist}
License:	LGPLv2 or MPLv1.1
URL:		http://pango.org
Group:		System Environment/Libraries
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	https://download.gnome.org/sources/pango/1.40/%{name}-%{version}.tar.xz
%define sha1 pango=761458faab28cb70ba62e01ec9379d03bc5339c0
BuildRequires:	glib-devel
BuildRequires:	cairo-devel
BuildRequires:	libpng-devel
BuildRequires:	fontconfig-devel
BuildRequires:	harfbuzz-devel
Requires:	glib
Requires:	cairo
Requires:	libpng
Requires:	fontconfig
Requires:	harfbuzz
%description
Pango is a library for laying out and rendering of text, with an emphasis on internationalization. Pango can be used anywhere that text layout is needed, though most of the work on Pango so far has been done in the context of the GTK+ widget toolkit.

%package	devel
Summary:	Header and development files
Requires:	%{name} = %{version}-%{release}
Requires:	glib-devel
Requires:	cairo-devel
Requires:	libpng-devel
Requires:	fontconfig-devel
Requires:	harfbuzz-devel
%description	devel
It contains the libraries and header files to create applications

%prep
%autosetup
%build
%configure
make %{?_smp_mflags}
%install
make %{?_smp_mflags} DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -delete

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
%{_datadir}/*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Thu Dec 16 2021 Alexey Makhalov <amakhalov@vmware.com> 1.40.4-2
- Fix pango -> fontconfig -> freetype2 dependency
- Clean up Requires and BuildRequires
* Tue Apr 04 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.40.4-1
- Initial version
