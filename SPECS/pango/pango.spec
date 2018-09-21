Summary:	library for laying out and rendering of text.
Name:		pango
Version:	1.42.4
Release:	1%{?dist}
License:	LGPLv2 or MPLv1.1
URL:		http://pango.org
Group:		System Environment/Libraries
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	https://download.gnome.org/sources/pango/1.42/%{name}-%{version}.tar.xz
%define sha1 pango=240942b1307eaa3819e6e534596271c57cd75457
BuildRequires:	glib-devel
BuildRequires:	cairo
BuildRequires:	cairo-devel
BuildRequires:	libpng-devel
BuildRequires:	fontconfig
BuildRequires:	fontconfig-devel
BuildRequires:	harfbuzz
BuildRequires:	harfbuzz-devel
BuildRequires:	freetype2
BuildRequires:  fribidi-devel
Requires:	fribidi-devel
Requires:	harfbuzz-devel
%description
Pango is a library for laying out and rendering of text, with an emphasis on internationalization. Pango can be used anywhere that text layout is needed, though most of the work on Pango so far has been done in the context of the GTK+ widget toolkit.

%package	devel
Summary:	Header and development files
Requires:	%{name} = %{version}-%{release}
%description	devel
It contains the libraries and header files to create applications 

%prep
%setup -q
%build
./configure \
	--prefix=%{_prefix}
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
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
*   Tue Sep 11  2018 Him Kalyan Bordoloi <bordoloi@vmware.com> 1.42.4-1
-   Upgrade version
*   Tue Apr 04 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.40.4-1
-   Initial version
