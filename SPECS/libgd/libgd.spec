Summary:        GD is an open source code library for the dynamic creation of images by programmers.
Name:           libgd
Version:        2.2.5
Release:        15%{?dist}
License:        MIT
URL:            https://libgd.github.io/
Group:          System/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/libgd/libgd/releases/download/gd-%{version}/%{name}-%{version}.tar.xz
%define sha512  libgd=e4598e17a277a75e02255402182cab139cb3f2cffcd68ec05cc10bbeaf6bc7aa39162c3445cd4a7efc1a26b72b9152bbedb187351e3ed099ea51767319997a6b
Source1:        %{name}-tests.tar.gz
%define sha512  libgd-tests=72da4b0f3789ad4a6850175c36b4486d04d642bd5a222a4d5b47a09e8bea88c90be378a3166e1c1c256e83354cc08e2a260ffad369e21e199643ba219359da60

Patch0:         CVE-2018-1000222.patch
Patch1:         libgd-CVE-2019-6978.patch
Patch2:         libgd-CVE-2019-6977.patch
Patch3:         libgd-CVE-2018-14553.patch
Patch4:         libgd-CVE-2017-6363.patch
Patch5:         libgd-CVE-2019-11038.patch
Patch6:         libgd-CVE-2019-11038-testcase.patch
Patch7:         libgd-CVE-2021-38115.patch
Patch8:         libgd-CVE-2021-40145.patch

BuildRequires:  libjpeg-turbo-devel
BuildRequires:  libpng-devel
BuildRequires:  libwebp-devel
BuildRequires:  libtiff-devel
BuildRequires:  freetype2-devel
BuildRequires:  fontconfig-devel

Requires:       libpng
Requires:       libwebp
Requires:       libtiff
Requires:       libjpeg-turbo
Requires:       freetype2
Requires:       fontconfig
Provides:       pkgconfig(libgd)

%description
GD is an open source code library for the dynamic creation of images by programmers.

GD is written in C, and "wrappers" are available for Perl, PHP and other languages. GD can read and write many different image formats. GD is commonly used to generate charts, graphics, thumbnails, and most anything else, on the fly.

%package    devel
Summary:    Header and development files
Requires:   %{name} = %{version}-%{release}
%description    devel
Header & Development files

%prep
%autosetup -N -a0
tar xf %{SOURCE1} --no-same-owner
cp libgd-tests/bug00383.gd tests/gd/
cp libgd-tests/bug00383.gd2 tests/gd2/
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1

%build
# To use the system installed automake latest version instead of given version in source
autoreconf -fi
%configure --with-webp --with-tiff --with-jpeg --with-png --with-freetype --with-fontconfig --disable-werror --disable-static
make %{?_smp_mflags}
%install
%make_install

%if 0%{?with_check}
%check
make %{?_smp_mflags} -k check
%endif

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/libgd.so.*
%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/libgd.so
%{_libdir}/pkgconfig/*

%changelog
* Fri Jul 07 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 2.2.5-15
- Bump version as a part of libtiff upgrade
* Fri Jan 27 2023 Harinadh D <hdommaraju@vmware.com> 2.2.5-14
- Build with freetype and fontconfig
* Thu Jan 12 2023 Anmol Jain <anmolja@vmware.com> 2.2.5-13
- Version bump up to use libtiff 4.5.0
* Mon Oct 03 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.2.5-12
- Remove .la files
* Thu Jun 2 2022 Shivani Agarwal <shivania2@vmware.com>  2.2.5-11
- Version bump up to use libtiff 4.4.0
* Mon Mar 21 2022 Harinadh D <hdommaraju@vmware.com>  2.2.5-10
- Version bump up to use libtiff 4.3.0
* Wed Sep 08 2021 Nitesh Kumar <kunitesh@vmware.com>  2.2.5-9
- Fix for CVE-2021-40145
* Thu Aug 26 2021 Nitesh Kumar <kunitesh@vmware.com>  2.2.5-8
- Fix for CVE-2021-38115
* Mon Nov 02 2020 Piyush Gupta <gpiyush@vmware.com>  2.2.5-7
- Fix for CVE-2019-11038
* Tue Mar 10 2020 Ankit Jain <ankitja@vmware.com>  2.2.5-6
- Fix for CVE-2017-6363
* Tue Feb 18 2020 Ankit Jain <ankitja@vmware.com>  2.2.5-5
- Fix for CVE-2018-14553
* Tue Feb 19 2019 Ankit Jain <ankitja@vmware.com>  2.2.5-4
- Fix for CVE-2019-6977
* Wed Jan 30 2019 Ankit Jain <ankitja@vmware.com>  2.2.5-3
- Fix for CVE-2019-6978
* Fri Nov 02 2018 Ankit Jain <ankitja@vmware.com>  2.2.5-2
- Fix for CVE-2018-1000222
* Tue Oct 10 2017 Alexey Makhalov <amakhalov@vmware.com> 2.2.5-1
- Updated to version 2.2.5 to address CVE-2017-6362
* Tue Jan 31 2017 Xiaolin Li <xiaolinl@vmware.com> 2.2.4-1
- Updated to version 2.2.4.
* Wed Jan 18 2017 Kumar Kaushik <kaushikk@vmware.com>  2.2.3-3
- Fix for CVE-2016-8670
* Fri Oct 07 2016 Anish Swaminathan <anishs@vmware.com>  2.2.3-2
- Fix for CVE-2016-7568
* Thu Jul 28 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 2.2.3-1
- Initial version
