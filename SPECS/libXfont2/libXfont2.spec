Summary:        X11 Xfont2 runtime library.
Name:           libXfont2
Version:        2.0.3
Release:        2%{?dist}
License:        MIT
URL:            http://www.x.org
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://ftp.x.org/pub/individual/lib/%{name}-%{version}.tar.bz2
%define sha512 %{name}=648b664e2aa58cbc7366a1b05873aa06bd4a38060f64085783043388244af8ceced77b29a22c3ac8b6d34cd226e093bbbcc785ea1748ea65720fe7ea05b4b44b

BuildRequires:  freetype2-devel
BuildRequires:  xtrans
BuildRequires:  libfontenc-devel

Requires:       freetype2
Requires:       libfontenc

%description
The X11 Xfont runtime library.

%package    devel
Summary:    Header and development files
Requires:   %{name} = %{version}-%{release}
Requires:   freetype2-devel
Requires:   xtrans
Requires:   libfontenc-devel

%description    devel
It contains the libraries and header files to create applications

%prep
%autosetup -p1

%build
%configure --disable-devel-docs
%make_build

%install
%make_install %{?_smp_mflags}

%ldconfig_scriptlets

%files
%defattr(-,root,root)
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Wed Apr 19 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 2.0.3-2
- Bump version as a part of freetype2 upgrade
* Thu Jun 13 2019 Alexey Makhalov <amakhalov@vmware.com> 2.0.3-1
- Version update
* Wed Nov 15 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.5.1-2
- Updated build requires & requires to build with Photon 2.0
* Tue May 19 2015 Alexey Makhalov <amakhalov@vmware.com> 1.5.1-1
- initial version
