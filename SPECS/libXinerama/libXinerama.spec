Summary:        X11 libXinerama runtime library.
Name:           libXinerama
Version:        1.1.5
Release:        1%{?dist}
License:        MIT
URL:            http://www.x.org
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://pub/individual/lib/%{name}-%{version}.tar.xz
%define sha512 %{name}=735b5320de4782005b379e409bf2f976131c17d496b297d33a0e127ca1443034778586b6b25c077b2ad73a4ab34d440d7510475e0041f38202bb40f15fb08ff7

BuildRequires:  libXext-devel

Requires:       libXext

%description
The X11 libXi runtime library.

%package        devel
Summary:        Header and development files
Requires:       %{name} = %{version}-%{release}
Requires:       libXext-devel

%description    devel
It contains the libraries and header files to create applications

%prep
%autosetup -p1

%build
%configure
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
%{_libdir}/*.so
%{_libdir}/pkgconfig
%{_datadir}/*
%{_libdir}/*.a

%changelog
* Sun Nov 6 2022 Shivani Agarwal <shivania2@vmware.com> 1.1.5-1
- Upgrade to version 1.1.5
* Tue May 19 2015 Alexey Makhalov <amakhalov@vmware.com> 1.1.3-1
- initial version
