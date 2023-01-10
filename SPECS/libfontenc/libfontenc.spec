Summary:        X11 Fontenc runtime library.
Name:           libfontenc
Version:        1.1.2
Release:        1%{?dist}
License:        MIT
URL:            http://www.x.org
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://ftp.x.org/pub/individual/lib/%{name}-%{version}.tar.bz2
%define sha512 %{name}=e0905592b7ef65acb8298b9807f90e68d18eddf3112c6232c1c774603c95ca7ec7f6db161e133dadc00d8791c5f76d4c3d65aa95544a1500c0767b88fdb52f45

BuildRequires:  pkg-config
BuildRequires:  proto
BuildRequires:  zlib-devel

Requires:   zlib

Provides:   pkgconfig(fontenc)

%description
The X11 Fontenc runtime library.

%package    devel
Summary:    Header and development files
Requires:   %{name} = %{version}-%{release}
Requires:   proto zlib-devel

%description    devel
It contains the libraries and header files to create applications

%prep
%autosetup -p1

%build
%configure
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
%{_libdir}/*.so
%{_libdir}/pkgconfig
%{_libdir}/*.a

%changelog
* Thu Dec 22 2022 Harinadh D <hdommaraju@vmware.com> 1.1.2-1
- Initial version
