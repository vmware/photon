Summary:	pixel manipulation library.
Name:		pixman
Version:	0.34.0
Release:	2%{?dist}
License:	MIT
URL:		http://cgit.freedesktop.org/pixman/
Group:		System Environment/Libraries
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	https://xorg.freedesktop.org/archive/individual/lib/%{name}-%{version}.tar.gz
%define sha512  pixman=81caca5b71582b53aaac473bc37145bd66ba9acebb4773fa8cdb51f4ed7fbcb6954790d8633aad85b2826dd276bcce725e26e37997a517760e9edd72e2669a6d
Patch0:         CVE-2022-44638.patch
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
%autosetup -p1

%build
%configure \
	CFLAGS="-O3 -fPIC" \
	--disable-static
make %{?_smp_mflags}

%install
make %{?_smp_mflags} DESTDIR=%{buildroot} install
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
*       Tue Nov 8 2022 Shivani Agarwal <shivania2@vmware.com> 0.34.0-2
-       Fix CVE-2022-44638
*       Fri Nov 11 2016 Dheeraj Shetty <dheerajs@vmware.com> 0.34.0-1
-       Initial version
