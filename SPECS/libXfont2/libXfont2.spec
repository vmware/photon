Summary:        X11 Xfont2 runtime library.
Name:           libXfont2
Version:        2.0.3
Release:        3%{?dist}
URL:            http://www.x.org
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://ftp.x.org/pub/individual/lib/%{name}-%{version}.tar.bz2

Source1: license.txt
%include %{SOURCE1}

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
* Wed Dec 11 2024 Ajay Kaher <ajay.kaher@broadcom.com> 2.0.3-3
- Release bump for SRP compliance
* Wed Apr 19 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 2.0.3-2
- Bump version as a part of freetype2 upgrade
* Thu Jun 13 2019 Alexey Makhalov <amakhalov@vmware.com> 2.0.3-1
- Version update
* Wed Nov 15 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.5.1-2
- Updated build requires & requires to build with Photon 2.0
* Tue May 19 2015 Alexey Makhalov <amakhalov@vmware.com> 1.5.1-1
- initial version
