Summary:	opentype text shaping engine
Name:		harfbuzz
Version:	1.4.5
Release:	1%{?dist}
License:	MIT
URL:		http://harfbuzz.org
Group:		System Environment/Libraries
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	https://www.freedesktop.org/software/harfbuzz/release/%{name}-%{version}.tar.bz2
%define sha1 harfbuzz=e979eb20b789c1fc47107ef93a584924e34dd195
BuildRequires:	glib-devel
BuildRequires:	freetype2
BuildRequires:	freetype2-devel

%description
HarfBuzz is an implementation of the OpenType Layout engine.

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

%changelog
*       Wed Apr 05 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.4.5-1
-       Initial version
