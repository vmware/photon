Summary:        Library to encode and decode webP format images
Name:           libwebp
Version:        1.3.2
Release:        1%{?dist}
License:        BSD
URL:            http://webmproject.org/
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/webmproject/%{name}/archive/%{name}-%{version}.tar.gz
%define sha512  libwebp=2b624d2ecfbff6b4db2719e38f146722638ae262acd96327073a04451dd05fb27ef70c5681187821d251df728a6be7e89209c861c561a13bfb786495a830bc20
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  libtiff-devel
BuildRequires:  libpng-devel
Requires:       libjpeg-turbo
Requires:       libtiff
Requires:       libpng
%description
The libwebp package contains a library and support programs to encode and decode images in WebP format.

%package        devel
Summary:        Header and development files
Requires:       %{name} = %{version}-%{release}
%description    devel
It contains the libraries and header files to create applications

%prep
%autosetup
%build
./autogen.sh

%configure \
        --enable-libwebpmux \
        --enable-libwebpdemux \
        --enable-libwebpdecoder \
        --enable-libwebpextras  \
        --enable-swap-16bit-csp \
        --disable-static
make %{?_smp_mflags}

%install
make %{?_smp_mflags} DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -delete

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so.*
%{_datadir}/*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Wed Sep 20 2023 Kuntal Nayak <nkuntal@vmware.com> 1.3.2-1
- Version upgrade to fix CVE-2023-4863
* Fri Jul 28 2023 Kuntal Nayak <nkuntal@vmware.com> 1.3.1-1
- Version upgrade to fix CVE-2023-1999
* Tue Jun 27 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 1.2.4-3
- Bump version as a part of libtiff upgrade
* Tue Dec 13 2022 Guruswamy Basavaiah <bguruswamy@vmware.com> 1.2.4-2
- Bump release as a part of libpng upgrade
* Mon Jul 11 2022 Gerrit Photon <photon-checkins@vmware.com> 1.2.4-1
- Automatic Version Bump
*       Mon Jun 20 2022 Shivani Agarwal <shivania2@vmware.com>  1.2.0-2
-       Version bump up to use libtiff 4.4
*       Thu Apr 29 2021 Gerrit Photon <photon-checkins@vmware.com> 1.2.0-1
-       Automatic Version Bump
*       Wed Jul 08 2020 Gerrit Photon <photon-checkins@vmware.com> 1.1.0-1
-       Automatic Version Bump
*       Wed Sep 12 2018 Keerthana K <keerthanak@vmware.com> 1.0.0-1
-       Update to version 1.0.0
*       Thu Apr 06 2017 Kumar Kaushik <kaushikk@vmware.com> 0.6.0-1
-       Upgrading version to 0.6.0
*       Wed Jul 27 2016 Divya Thaluru <dthaluru@vmware.com> 0.5.1-1
-       Initial version
