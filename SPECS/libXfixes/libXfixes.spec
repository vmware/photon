Summary:        X11 XFIXES extension.
Name:           libXfixes
Version:        5.0.3
Release:        2%{?dist}
License:        MIT
URL:            http://www.x.org
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://ftp.x.org/pub/individual/lib/%{name}-%{version}.tar.bz2
%define sha512 %{name}=72d5ee496e5c0520c95ef6bbb52deff1ee4c29792f11aa17aeb25c8ec5eb992ca502de040c77ad95835d1b1432f315b6cb7a3308b434847c28b9c2c6f9d1ac10

BuildRequires:  proto
BuildRequires:  libXext-devel
BuildRequires:  util-macros

Requires:       libXext
Requires:       libX11
Provides:       pkgconfig(xfixes)

%description
The X11 Xfixes extension.

%package    devel
Summary:    Header and development files
Requires:   %{name} = %{version}-%{release}
Requires:   libXext-devel

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

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/pkgconfig/
%{_datadir}/*

%changelog
* Wed Jun 14 2023 Shivani Agarwal <shivania2@vmware.com> 5.0.3-2
- Bump version as a part of libX11 upgrade
* Thu Aug 18 2022 Shivani Agarwal <shivania2@vmware.com> 5.0.3-1
- Upgrade version to 5.0.3
* Tue May 19 2015 Alexey Makhalov <amakhalov@vmware.com> 5.0.1-1
- initial version
