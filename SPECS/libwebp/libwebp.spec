Summary:        Library to encode and decode webP format images
Name:           libwebp
Version:        1.0.3
Release:        6%{?dist}
License:        BSD
URL:            http://webmproject.org/
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/webmproject/%{name}/archive/%{name}-%{version}.tar.gz
%define sha512  libwebp=ddc0a9555fdffc2c46ccefdf7484fd0f1fe913dcdf6b198cae717d568fae0d8fd2f152c5b1ff3121596328ec19fe3aea46c4b4bc36dbed09d879321893d24a60

Patch0: CVE-2023-1999.patch

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
* Fri Jul 28 2023 Kuntal Nayak <nkuntal@vmware.com> 1.0.3-6
- Fixed CVE-2023-1999 with patch
* Fri Jul 07 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 1.0.3-5
- Bump version as a part of libtiff upgrade
* Thu Jan 12 2023 Anmol Jain <anmolja@vmware.com> 1.0.3-4
- Version bump up to use libtiff 4.5.0
* Thu Jun 2 2022 Shivani Agarwal <shivania2@vmware.com>  1.0.3-3
- Version bump up to use libtiff 4.4.0
* Wed May 26 2021 Sujay G <gsujay@vmware.com> 1.0.3-2
- version bump up to build with libtiff 4.3.0
* Wed May 26 2021 Sujay G <gsujay@vmware.com> 1.0.3-1
- Bump version to 1.0.3 to fix following CVE's:
- CVE-2018-25009, CVE-2018-25010, CVE-2018-25011, CVE-2018-25012,
- CVE-2018-25013, CVE-2018-25014, CVE-2020-36328, CVE-2020-36329,
- CVE-2020-36330, CVE-2020-36331, CVE-2020-36332
* Wed Sep 12 2018 Keerthana K <keerthanak@vmware.com> 1.0.0-1
- Update to version 1.0.0
* Thu Apr 06 2017 Kumar Kaushik <kaushikk@vmware.com> 0.6.0-1
- Upgrading version to 0.6.0
* Wed Jul 27 2016 Divya Thaluru <dthaluru@vmware.com> 0.5.1-1
- Initial version
