Summary:	opentype text shaping engine
Name:		harfbuzz
Version:	1.9.0
Release:	1%{?dist}
License:	MIT
URL:		http://harfbuzz.org
Group:		System Environment/Libraries
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	https://www.freedesktop.org/software/harfbuzz/release/%{name}-%{version}.tar.bz2
%define sha1 harfbuzz=b1b607216af1ee16d2f86c8427ecc36b6f2fd9dd
BuildRequires:	glib-devel
BuildRequires:	freetype2
BuildRequires:	freetype2-devel
Requires:	glib

%description
HarfBuzz is an implementation of the OpenType Layout engine.

%package	devel
Summary:	Header and development files
Requires:	%{name} = %{version}-%{release}
Requires:	glib-devel
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
make %{?_smp_mflags} -k check

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/*.so*
%{_bindir}/*

%files devel
%defattr(-,root,root)
%doc %{_datadir}/gtk-doc
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_libdir}/cmake/harfbuzz/harfbuzz-config.cmake

%changelog
*       Wed Sep 12 2018 Anish Swaminathan <anishs@vmware.com> 1.9.0-1
-       Update to version 1.9.0
*       Thu Dec 07 2017 Alexey Makhalov <amakhalov@vmware.com> 1.4.5-2
-       Add glib requirement
*       Wed Apr 05 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.4.5-1
-       Initial version
