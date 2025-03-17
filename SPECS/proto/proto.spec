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
Release:        6%{?dist}
URL:            http://www.x.org
Group:          Development/System
BuildArch:      noarch
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://ftp.x.org/pub/individual/proto/xproto-%{xproto_ver}.tar.bz2

Source1:        http://ftp.x.org/pub/individual/proto/xextproto-%{xextproto_ver}.tar.bz2

Source2:        http://ftp.x.org/pub/individual/proto/inputproto-%{inputproto_ver}.tar.bz2

Source3:        http://ftp.x.org/pub/individual/proto/kbproto-%{kbproto_ver}.tar.bz2

Source4:        http://ftp.x.org/pub/individual/proto/renderproto-%{renderproto_ver}.tar.bz2

Source5:        http://ftp.x.org/pub/individual/proto/randrproto-%{randrproto_ver}.tar.bz2

Source6: http://ftp.x.org/pub/individual/proto/fixesproto-%{fixesproto_ver}.tar.bz2

Source7: http://ftp.x.org/pub/individual/proto/compositeproto-%{compositeproto_ver}.tar.bz2

Source8: http://ftp.x.org/pub/individual/proto/damageproto-%{damageproto_ver}.tar.bz2

Source9: http://ftp.x.org/pub/individual/proto/recordproto-%{recordproto_ver}.tar.bz2

Source10: http://ftp.x.org/pub/individual/proto/scrnsaverproto-%{scrnsaverproto_ver}.tar.bz2

Source11: http://ftp.x.org/pub/individual/proto/glproto-%{glproto_ver}.tar.bz2

Source12: http://ftp.x.org/pub/individual/proto/xineramaproto-%{xineramaproto_ver}.tar.bz2

Source13: http://ftp.x.org/pub/individual/proto/fontsproto-%{fontsproto_ver}.tar.bz2

Source14: http://ftp.x.org/pub/individual/proto/dri2proto-%{dri2proto_ver}.tar.bz2

Source15: license.txt
%include %{SOURCE15}

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
* Wed Dec 11 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 7.7-6
- Release bump for SRP compliance
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
