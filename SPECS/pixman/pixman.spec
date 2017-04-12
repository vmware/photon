Summary:	pixel manipulation library.
Name:		pixman
Version:	0.34.0
Release:	1%{?dist}
License:	MIT
URL:		http://cgit.freedesktop.org/pixman/
Group:		System Environment/Libraries
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	https://xorg.freedesktop.org/archive/individual/lib/%{name}-%{version}.tar.gz
%define sha1 pixman=a1b1683c1a55acce9d928fea1ab6ceb79142ddc7
BuildRequires:	libtool

%description
Pixman is a pixel manipulation library for X and Cairo.

%package	devel
Summary:	Header and development files
Requires:	%{name} = %{version}-%{release}
Provides:	pkgconfig(pixman-1)

%description	devel
It contains the libraries and header files to create applications 

%prep
%setup -q 
%build
./configure \
	--prefix=%{_prefix} \
	CFLAGS="-O3 -fPIC" \
	--disable-static
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
%doc COPYING
%{_libdir}/*.so*

%files devel
%defattr(-,root,root)
%dir %{_includedir}/pixman-1
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
*       Fri Nov 11 2016 Dheeraj Shetty <dheerajs@vmware.com> 0.34.0-1
-       Initial version
