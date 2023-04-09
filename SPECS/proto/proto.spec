%define xproto_ver 7.0.31
%define xextproto_ver 7.3.0
%define inputproto_ver 2.3.1
%define kbproto_ver 1.0.7
%define renderproto_ver 0.11.1
%define randrproto_ver 1.5.0
%define fixesproto_ver 5.0
%define compositeproto_ver 0.4.2
%define damageproto_ver 1.2.1
%define recordproto_ver 1.14.2
%define scrnsaverproto_ver 1.2.2
%define glproto_ver 1.4.17
%define xineramaproto_ver 1.2.1
%define fontsproto_ver 2.1.3
%define dri2proto_ver 2.8

Summary:        The Xorg protocol headers.
Name:           proto
Version:        7.7
Release:        5%{?dist}
License:        MIT
URL:            http://www.x.org
Group:          Development/System
BuildArch:      noarch
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://ftp.x.org/pub/individual/proto/xproto-%{xproto_ver}.tar.bz2
%define sha512  xproto=bba6141525c21fd9a3cf210853658cc7af69f82e1ac15bacfffb9280efc3fe3c6fa708095b541b6f33f114c11e808bde8c8839ae63ff88e30963abdfac12702b

Source1:        http://ftp.x.org/pub/individual/proto/xextproto-%{xextproto_ver}.tar.bz2
%define sha512  xextproto=238beed85fcf6fe5b0809e52814dd44fa45fe6868239990086cb8dd2c446292dd4794698abd07ed10bd146a7096c1679f7160da226f9e861dfaf6c8e22315d61

Source2:        http://ftp.x.org/pub/individual/proto/inputproto-%{inputproto_ver}.tar.bz2
%define sha512  inputproto=84f8acff3d54e929af6da088624adcd8dffe2eba0d9ef672e136f76d12f3814fbf6a7962de27becfaa0aa5e70d874eb5297d9eed8809576d7b0d96f8c29d9d72

Source3:        http://ftp.x.org/pub/individual/proto/kbproto-%{kbproto_ver}.tar.bz2
%define sha512  kbproto=49f24bfd11ee4ef0de658a1f55bcfb4b3a1f7057d90137b899ea3d4ecc40cebde97926a3f4315ddca4ae28d32b2d15f16fda993296acffdb4c007d2f84a39a22

Source4:        http://ftp.x.org/pub/individual/proto/renderproto-%{renderproto_ver}.tar.bz2
%define sha512  renderproto=c38bc7247fd7b89732c892ee41c061b20397f4e79195601b7015dd55054b966f0797ac3990b147f80234596ba2c201ce90e292ecefed2e133167955bca70acc5

Source5:        http://ftp.x.org/pub/individual/proto/randrproto-%{randrproto_ver}.tar.bz2
%define sha512  randrproto=5c56f6acfe3a9da5ffda45e4af2da5081a5116d53f4d2dafe399eae168656727927ca0fb4c29fc6583e87709ac83b025ae206fba9356ebf9e26d3ff545da57f4

Source6: http://ftp.x.org/pub/individual/proto/fixesproto-%{fixesproto_ver}.tar.bz2
%define sha512 fixesproto=93c6a8b6e4345c3049c08f2f3960f5eb5f92c487f26d227430964361bf82041b49e61f873fbbb8ee0e111556f90532b852c20e6082ee8008be641373251fa78c

Source7: http://ftp.x.org/pub/individual/proto/compositeproto-%{compositeproto_ver}.tar.bz2
%define sha512 compositeproto=ad5e4d87b77a8447c228ca85ac8d010d93b5c64929dc866e99a25700b9905f7c3f22e48f8c7fdc54e87879ddcc90e5d4adc338aeea393d7057b19b5ccae31f11

Source8: http://ftp.x.org/pub/individual/proto/damageproto-%{damageproto_ver}.tar.bz2
%define sha512 damageproto=f124e85fb3cc70ed3536cb9db57ac93461bbb5df1a713bc6b67a5ea49122556c321781ca150df681502f6ccfb7305f290e131ad25ce9ccbff5af268df11c86fc

Source9: http://ftp.x.org/pub/individual/proto/recordproto-%{recordproto_ver}.tar.bz2
%define sha512 recordproto=ab82d966ffacb46c001df15b272ca58f996826dc6f6835d3dc4d385b31c682acacb073a380d61938e2f242bffdabdd9b8f7107cd5ac67cb7aa3a28cc14a8ea02

Source10: http://ftp.x.org/pub/individual/proto/scrnsaverproto-%{scrnsaverproto_ver}.tar.bz2
%define sha512 scrnsaverproto=e74a512a6101967983a1d713d22a1f456f77519998116ef0f0a9e4b44ae4730ecd41eb9c0f7fa53e9f5c94967541daf10693d701af832597f5347461c5990ebc

Source11: http://ftp.x.org/pub/individual/proto/glproto-%{glproto_ver}.tar.bz2
%define sha512 glproto=3e5bb1949ab9993e07d2ed7e829b9e0a8803eab476e9f4082fc01087c3dce01f3bcb9d55261eaf60e55977a689b326ed1dcf40f74d5e1fc660c83bea094b6754

Source12: http://ftp.x.org/pub/individual/proto/xineramaproto-%{xineramaproto_ver}.tar.bz2
%define sha512 xineramaproto=ec2194c9bcad3f0f3eb3e9298792272213aa032ae9d6c00dcad567f31d7278a8c676fc67f47aae1a6deef5bade0b204346ed16da4a4c4d5a507c04d109d3dbb3

Source13: http://ftp.x.org/pub/individual/proto/fontsproto-%{fontsproto_ver}.tar.bz2
%define sha512 fontsproto=f46d5b733aa48644aa3aa75d4ed47231ef78cb60f747f7200d82331a1ba566190bf37b5b9926c690dec6356043ce7c85a5b59fc1b4b11667ef432518b5d4cc87

Source14: http://ftp.x.org/pub/individual/proto/dri2proto-%{dri2proto_ver}.tar.bz2
%define sha512  dri2proto=1602f58cd8a3371dacf894cde4889b9147fc08e83f98d8e0d1c748abe43ecb74cf4e0e3d5eb2f33568ba5e6d9f310303b98ba43ae3bc956ae693824b1ae0745a

BuildRequires:  pkg-config
Provides:       pkgconfig(xproto)

%description
The Xorg protocol headers provide the header files required to build the system, and to allow other applications to build against the installed X Window system.

%prep
# Using autosetup is not feasible
%setup -q -c %{name}-%{version} -a0 -a1 -a2 -a3 -a4 -a5 -a6 -a7 -a8 -a9 -a10 -a11 -a12 -a13 -a14

%build
for pkg in `ls`; do
  pushd $pkg
  %configure
  popd
done

%install
for pkg in `ls`; do
  make -C $pkg %{?_smp_mflags} DESTDIR=%{buildroot} install
done

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_includedir}/X11/*
%{_includedir}/GL/*
%exclude %{_includedir}/X11/extensions/XKBgeom.h
%{_libdir}/pkgconfig/*
%{_docdir}/*

%changelog
* Fri Mar 17 2023 Shivani Agarwal <shivania2@vmware.com> 7.7-5
- Added dri2proto
* Thu Sep 8 2022 Shivani Agarwal <shivania2@vmware.com> 7.7-4
- Added fixesproto, compositeproto, damageproto, recordproto, scrnsaverproto, glproto, xineramaproto, fontsproto
* Tue Jul 12 2022 Shivani Agarwal <shivania2@vmware.com> 7.7-3
- Updated kbproto
* Thu Jun 13 2019 Alexey Makhalov <amakhalov@vmware.com> 7.7-2
- Updated xproto, randrproto
* Fri May 15 2015 Alexey Makhalov <amakhalov@vmware.com> 7.7-1
- initial version
