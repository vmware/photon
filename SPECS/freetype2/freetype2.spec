Summary:	software font engine.
Name:		freetype2
Version:	2.7.1
Release:	1%{?dist}
License:	BSD/GPL
URL:		http://www.freetype.org/
Group:		System Environment/Libraries
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://download.savannah.gnu.org/releases/freetype/freetype-%{version}.tar.gz
%define sha1 freetype=60fb8097901a887b8e8f6e7f777ef0516ae68022
BuildRequires:	libtool
BuildRequires:	zlib-devel

%description
FreeType is a software font engine that is designed to be small, efficient, highly customizable, and portable while capable of producing high-quality output (glyph images). It can be used in graphics libraries, display servers, font conversion tools, text image generation tools, and many other products as well.

%package	devel
Summary:	Header and development files
Requires:	freetype2 = %{version}-%{release}
%description	devel
It contains the libraries and header files to create applications 

%prep
%setup -q -n freetype-%{version}
%build
./configure \
	--prefix=%{_prefix} \
	--with-harfbuzz=no
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -delete
find %{buildroot} -name '*.a' -delete

%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}

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
*       Fri Nov 11 2016 Dheeraj Shetty <dheerajs@vmware.com> 2.7.1-1
-       Initial version
