Summary:  A 2D graphics library.
Name:     cairo
Version:  1.17.6
Release:  10%{?dist}
URL:      https://cairographics.org
Group:    System Environment/Libraries
Vendor:   VMware, Inc.
Distribution:   Photon

Source0: http://cairographics.org/releases/%{name}-%{version}.tar.xz
%define sha512 %{name}=15d9a82097b9c5a43071ff9fbfe90d7aaee5fddb84f519cdddfe312c5fc7248a50b73a5351922de2aaafa4b2e86f911b3147609538346f8a7635f34d631c9146

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  pkg-config
BuildRequires:  libpng-devel
BuildRequires:  libxml2-devel
BuildRequires:  pixman-devel
BuildRequires:  freetype2-devel
BuildRequires:  fontconfig-devel
BuildRequires:  glib-devel
BuildRequires:  libX11-devel
BuildRequires:  libXext-devel

Requires:       pixman
Requires:       glib
Requires:       libpng
Requires:       expat
Requires:       freetype2
Requires:       fontconfig
Requires:       binutils-libs
Requires:       libX11
Requires:       libXext

%description
Cairo is a 2D graphics library with support for multiple output devices.

%package    devel
Summary:    Header and development files
Requires:   %{name} = %{version}-%{release}
Requires:   freetype2-devel
Requires:   pixman-devel
Requires:   libpng-devel
Requires:       libX11-devel
Requires:       libXext-devel

%description    devel
It contains the libraries and header files to create applications

%prep
%autosetup -p1

%build
export CFLAGS="-O3 -fPIC"
# Fix build with latest binutils
sed 's/PTR/void */' -i util/cairo-trace/lookup-symbol.c

%configure \
    --enable-xlib=yes \
    --enable-xlib-render=no \
    --enable-win32=no \
    --disable-static \

%make_build

%install
%make_install %{?_smp_mflags}

%ldconfig_scriptlets

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so.*
%{_libdir}/%{name}/*.so

%files devel
%defattr(-,root,root)
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/gtk-doc/html/%{name}/*

%changelog
* Thu Dec 12 2024 HarinadhD <harinadh.dommaraju@broadcom.com> 1.17.6-10
- Release bump for SRP compliance
* Wed Jun 14 2023 Shivani Agarwal <shivania2@vmware.com> 1.17.6-9
- Bump version as a part of libX11 upgrade
* Thu May 25 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 1.17.6-8
- Bump version as a part of libxml2 upgrade
* Wed May 24 2023 Him Kalyan Bordoloi <bordoloih@vmware.com> 1.17.6-7
- Bump version as a part of pixman upgrade
* Wed Apr 19 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 1.17.6-6
- Bump version as a part of freetype2 upgrade
* Tue Dec 13 2022 Guruswamy Basavaiah <bguruswamy@vmware.com> 1.17.6-5
- Bump release as a part of libpng upgrade
* Wed Nov 30 2022 Shivani Agarwal <shivania2@vmware.com> 1.17.6-4
- Enabled xlib
* Sun Nov 13 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.17.6-3
- Fix packaging and spec improvements
* Thu Sep 01 2022 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 1.17.6-2
- Fix build with latest binutils
* Fri May 20 2022 Gerrit Photon <photon-checkins@vmware.com> 1.17.6-1
- Automatic Version Bump
* Mon Apr 12 2021 Gerrit Photon <photon-checkins@vmware.com> 1.17.4-1
- Automatic Version Bump
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
