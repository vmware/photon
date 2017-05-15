Summary:	software font engine.
Name:		freetype2
Version:	2.7.1
Release:	3%{?dist}
License:	BSD/GPL
URL:		http://www.freetype.org/
Group:		System Environment/Libraries
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://download.savannah.gnu.org/releases/freetype/freetype-%{version}.tar.gz
%define sha1 freetype=60fb8097901a887b8e8f6e7f777ef0516ae68022
Patch0:         CVE-2017-7857-and-CVE-2017-7858.patch
Patch1:         CVE-2017-7864.patch
Patch2:         CVE-2017-8287.patch
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
%patch0 -p1
%patch1 -p1
%patch2 -p1

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
*       Mon May 15 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.7.1-3
-       CVE-2017-8287
*       Fri Apr 28 2017 Dheeraj Shetty <dheerajs@vmware.com> 2.7.1-2
-       CVE-2017-7857, CVE-2017-7858 and CVE-2017-7864
*       Fri Nov 11 2016 Dheeraj Shetty <dheerajs@vmware.com> 2.7.1-1
-       Initial version
