%define xproto_ver 7.0.31
%define xextproto_ver 7.3.0
%define inputproto_ver 2.3.1
%define kbproto_ver 1.0.7
%define renderproto_ver 0.11.1
%define randrproto_ver 1.5.0

Summary:        The Xorg protocol headers.
Name:           proto
Version:        7.7
Release:        3%{?dist}
License:        MIT
URL:            http://www.x.org/
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

BuildRequires:  pkg-config
Provides:       pkgconfig(xproto)

%description
The Xorg protocol headers provide the header files required to build the system, and to allow other applications to build against the installed X Window system.

%prep
# Using autosetup is not feasible
%setup -c %{name}-%{version} -a0 -a1 -a2 -a3 -a4 -a5

%build
for pkg in `ls` ; do
        pushd $pkg
        %configure
        popd
done

%install
for pkg in `ls` ; do
        pushd $pkg
        make %{?_smp_mflags} DESTDIR=%{buildroot} install
        popd
done

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_prefix}/*
%exclude %{_includedir}/X11/extensions/XKBgeom.h

%changelog
* Tue Jul 12 2022 Shivani Agarwal <shivania2@vmware.com> 7.7-3
- Updated kbproto
* Thu Jun 13 2019 Alexey Makhalov <amakhalov@vmware.com> 7.7-2
- Updated xproto, randrproto
* Fri May 15 2015 Alexey Makhalov <amakhalov@vmware.com> 7.7-1
- initial version
