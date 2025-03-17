Summary:        pixel manipulation library.
Name:           pixman
Version:        0.42.2
Release:        2%{?dist}
URL:            http://cgit.freedesktop.org/pixman/
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://xorg.freedesktop.org/archive/individual/lib/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}
BuildRequires:  libtool

%description
Pixman is a pixel manipulation library for X and Cairo.

%package        devel
Summary:        Header and development files
Requires:       %{name} = %{version}-%{release}
Provides:       pkgconfig(pixman-1)

%description    devel
It contains the libraries and header files to create applications

%prep
%autosetup
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
*       Wed Dec 11 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 0.42.2-2
-       Release bump for SRP compliance
*       Mon May 22 2023 Him Kalyan Bordoloi <bordoloih@vmware.com> 0.42.2-1
-       Version bump
*       Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 0.40.0-1
-       Automatic Version Bump
*       Fri Nov 11 2016 Dheeraj Shetty <dheerajs@vmware.com> 0.34.0-1
-       Initial version
