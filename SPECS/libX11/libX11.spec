Summary:        Core X11 protocol client library.
Name:           libX11
Version:        1.8.1
Release:        1%{?dist}
License:        MIT
URL:            http://www.x.org/
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/freedesktop/xorg-libX11/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512  libX11=ac73ff99abfc13a0b8d04e3e4fde2a3b97813120c73c4dbf57e0ec56bbde8cd0272f1c09f417f10561f57def22878509adced897ebb2adfc1cb0d30385ee9396

BuildRequires:  libxcb-devel
BuildRequires:  xtrans-devel

Requires:       fontconfig
Requires:       libxcb
Requires:       libXau
Requires:       libXdmcp
Provides:       pkgconfig(x11)

%description
Core X11 protocol client library.

%package        devel
Summary:        Header and development files for libX11
Requires:       %{name} = %{version}-%{release}
Requires:       libxcb-devel
Requires:       xtrans-devel

%description    devel
X.Org X11 libX11 development package

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

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_libdir}/*.so.*
%{_datadir}/X11/
%{_mandir}/man5/

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.a
%{_libdir}/pkgconfig/
%{_libdir}/*.so
%{_docdir}/
%{_mandir}/man3/

%changelog
* Thu Dec 22 2022 Harinadh D <hdommaraju@vmware.com> 1.8.1-1
- Initial release
