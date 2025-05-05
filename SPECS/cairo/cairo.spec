Summary:        A 2D graphics library.
Name:           cairo
Version:        1.17.2
Release:        9%{?dist}
License:        LGPLv2 or MPLv1.1
URL:            http://www.linuxfromscratch.org/blfs/view/svn/x/cairo.html
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://cairographics.org/releases/%{name}-%{version}.tar.xz
%define sha512  cairo=cacdbd470b4ce592446da5a6e76eedfb4210139f3fd8611e629d21499b8648124af08c3ec541c183e00ade227e5c261002cebb93d71937e611b6f7da52e57f20

Patch0:         CVE-2020-35492.patch

BuildRequires:  pkg-config
BuildRequires:  libpng-devel
BuildRequires:  libxml2-devel
BuildRequires:  pixman-devel
BuildRequires:  freetype2-devel
BuildRequires:  fontconfig-devel
BuildRequires:  glib-devel >= 2.68.4
BuildRequires:  libX11-devel
BuildRequires:  libXext-devel

Requires:       pixman
Requires:       glib >= 2.68.4
Requires:       libpng
Requires:       expat
Requires:       libX11
Requires:       libXext
Requires:       fontconfig
Requires:       freetype2

%description
Cairo is a 2D graphics library with support for multiple output devices.

%package        devel
Summary:        Header and development files
Requires:       %{name} = %{version}-%{release}
Requires:       freetype2-devel
Requires:       pixman-devel
Requires:       libX11-devel
Requires:       libXext-devel
Requires:       glib-devel
Requires:       fontconfig-devel

%description    devel
It contains the libraries and header files to create applications.

%prep
# Using autosetup is not feasible
%setup -cqn %{name}-%{version}
mv %{name}-%{version}*/* .
%autopatch -p1

%build
# add this since build failed in not find automake-1.15 in making test for cairo
# Before running ./configure try running autoreconf -f -i.
# The autoreconf program automatically runs autoheader, aclocal, automake, autopoint and libtoolize as required.
autoreconf -fiv

%configure \
    --enable-xlib=yes        \
    --enable-xlib-render=no \
    --enable-win32=no       \
    CFLAGS="-O3 -fPIC"      \
    --disable-static

%make_build

%install
%make_install %{?_smp_mflags}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so.*
%{_libdir}/cairo/*.so*

%files devel
%defattr(-,root,root)
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Mon May 05 2025 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 1.17.2-9
- Version bump for expat upgrade
* Mon Apr 21 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.17.2-8
- Fix devel package requires
* Thu Feb 29 2024 Anmol Jain <anmol.jain@broadcom.com> 1.17.2-7
- Bump version as a part of expat upgrade
* Sat Oct 07 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 1.17.2-6
- Bump version as part of glib upgrade
* Wed Jun 14 2023 Shivani Agarwal <shivania2@vmware.com> 1.17.2-5
- Bump version as a part of libX11 upgrade
* Wed Apr 19 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 1.17.2-4
- Bump version as a part of freetype2 upgrade
* Mon Sep 5 2022 Shivani Agarwal <shivania2@vmware.com> 1.17.2-3
- Enabled xlib
* Thu Apr 1 2021 Michelle Wang <michellew@vmware.com> 1.17.2-2
- Add patch for CVE-2020-3549
* Tue Jul 14 2020 Gerrit Photon <photon-checkins@vmware.com> 1.17.2-1
- Automatic Version Bump
* Thu Mar 14 2019 Michelle Wang <michellew@vmware.com> 1.16.0-1
- Upgrade cairo to 1.16.0 for CVE-2018-18064
- CVE-2018-18064 is for version up to (including) 1.15.14
* Tue Sep 11 2018 Dheeraj Shetty <dheerajs@vmware.com> 1.14.12-1
- Update to version 1.14.12
* Tue Oct 10 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.14.8-3
- Fix CVE-2017-9814
* Tue Jun 06 2017 Chang Lee <changlee@vmware.com> 1.14.8-2
- Remove %check
* Wed Apr 05 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.14.8-1
- Initial version
