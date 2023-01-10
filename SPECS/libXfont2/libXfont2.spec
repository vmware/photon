Summary:        X11 Xfont2 runtime library.
Name:           libXfont2
Version:        2.0.3
Release:        1%{?dist}
License:        MIT
URL:            http://www.x.org
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://ftp.x.org/pub/individual/lib/%{name}-%{version}.tar.bz2
%define sha512 %{name}=648b664e2aa58cbc7366a1b05873aa06bd4a38060f64085783043388244af8ceced77b29a22c3ac8b6d34cd226e093bbbcc785ea1748ea65720fe7ea05b4b44b

BuildRequires:  freetype2-devel
BuildRequires:  xtrans-devel
BuildRequires:  libfontenc-devel

Requires:       freetype2
Requires:       libfontenc

%description
The X11 Xfont runtime library.

%package    devel
Summary:    Header and development files
Requires:   %{name} = %{version}-%{release}
Requires:   freetype2-devel
Requires:   xtrans-devel
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

%if 0%{?with_check}
%check
make %{?_smp_mflags} -k check
%endif

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

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
* Thu Dec 22 2022 Harinadh D <hdommaraju@vmware.com> 2.0.3-1
- Initial release
