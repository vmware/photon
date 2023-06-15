Summary:        X11 Xrender runtime library.
Name:           libXrender
Version:        0.9.10
Release:        2%{?dist}
License:        MIT
URL:            http://www.x.org/
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://ftp.x.org/pub/individual/lib/%{name}-%{version}.tar.bz2
%define sha512  libXrender=16ea0cf638b32d7df54b270457ef8c9d9a80da27fa845b105b560cb31027b4c7fe799cf23d6b6bac492be5961264e96d7845d316a9af4de9ff38bf40885ea6fe

BuildRequires:  libX11-devel
Requires:       libX11
Provides:       pkgconfig(xrender)

%description
The X11 Renderer library.

%package        devel
Summary:        Header and development files
Requires:       %{name} = %{version}-%{release}
Requires:       libX11-devel

%description    devel
X.Org X11 libXrender development package

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install %{?_smp_mflags}
find %{buildroot} -name \*.la -delete

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/pkgconfig
%{_libdir}/*.a
%{_libdir}/*.so
%{_datadir}/*

%changelog
* Wed Jun 14 2023 Shivani Agarwal <shivania2@vmware.com> 0.9.10-2
- Bump version as a part of libX11 upgrade
* Tue Jul 12 2022 Shivani Agarwal <shivania2@vmware.com> 0.9.10-1
- Upgrade to 0.9.10
* Tue May 19 2015 Alexey Makhalov <amakhalov@vmware.com> 0.9.8-1
- initial version
