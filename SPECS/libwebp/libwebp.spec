Summary:        Library to encode and decode webP format images
Name:           libwebp
Version:        1.1.0
Release:        7%{?dist}
License:        BSD
URL:            http://webmproject.org/
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/webmproject/%{name}/archive/%{name}-%{version}.tar.gz
%define sha512  libwebp=c8440059a985587d4876a5e7fc2d07523bc7f582a04ee5dab0ef07df32b9635b907224de2cc15246c831dd5d9215569770196626badccc3171fe2832d7cb4549

Patch0: CVE-2023-1999.patch
Patch1: CVE-2023-4863.patch
Patch2: libwebp-Fix-invalid-incremental-decoding-check.patch

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
It contains the libraries and header files to create applications.

%prep
%autosetup -p1
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
* Wed Sep 20 2023 Kuntal Nayak <nkuntal@vmware.com> 1.1.0-7
- Fixed CVE-2023-4863 with patch
* Fri Jul 28 2023 Kuntal Nayak <nkuntal@vmware.com> 1.1.0-6
- Fixed CVE-2023-1999 with patch
* Mon Jun 26 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 1.1.0-5
- Bump version as a part of libtiff upgrade
* Tue Jan 31 2023 Shivani Agarwal <shivania2@vmware.com>  1.1.0-4
- Version bump up to use libtiff 4.5.0
* Mon Jun 20 2022 Shivani Agarwal <shivania2@vmware.com>  1.1.0-3
- Version bump up to use libtiff 4.4.0
* Wed Mar 23 2022 HarinadhD <hdommaraju@vmware.com> 1.1.0-2
- Version Bump up to build with libtiff 4.3.0
* Wed Jul 08 2020 Gerrit Photon <photon-checkins@vmware.com> 1.1.0-1
- Automatic Version Bump
* Wed Sep 12 2018 Keerthana K <keerthanak@vmware.com> 1.0.0-1
- Update to version 1.0.0
* Thu Apr 06 2017 Kumar Kaushik <kaushikk@vmware.com> 0.6.0-1
- Upgrading version to 0.6.0
* Wed Jul 27 2016 Divya Thaluru <dthaluru@vmware.com> 0.5.1-1
- Initial version
