Summary:        pixel manipulation library.
Name:           pixman
Version:        0.40.0
Release:        2%{?dist}
License:        MIT
URL:            http://cgit.freedesktop.org/pixman/
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://xorg.freedesktop.org/archive/individual/lib/%{name}-%{version}.tar.gz
%define sha512  pixman=063776e132f5d59a6d3f94497da41d6fc1c7dca0d269149c78247f0e0d7f520a25208d908cf5e421d1564889a91da44267b12d61c0bd7934cd54261729a7de5f
Patch0:         CVE-2022-44638.patch
BuildRequires:  libtool

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
*       Tue Nov 8 2022 Shivani Agarwal <shivania2@vmware.com> 0.40.0-2
-       Fix CVE-2022-44638
*       Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 0.40.0-1
-       Automatic Version Bump
*       Fri Nov 11 2016 Dheeraj Shetty <dheerajs@vmware.com> 0.34.0-1
-       Initial version
