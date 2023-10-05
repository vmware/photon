Summary:        X11 libxshmfence runtime library.
Name:           libxshmfence
Version:        1.3.2
Release:        2%{?dist}
License:        MIT
URL:            http://www.x.org/
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://ftp.x.org/pub/individual/lib/%{name}-%{version}.tar.gz
%define sha512 %{name}=1c5d2d183c7a1c5c79efd6da21d3884325209a10f75809584fe2b5e9ab244c0a09bb8b0d5ffad72781665bd3141232343c567ccb58ad74c71883d6d996997a76

BuildRequires:  pkg-config
BuildRequires:  util-macros
BuildRequires:  proto

%description
The X11 Shared Memory fences library.

%package        devel
Summary:        Header and development files
Requires:       %{name} = %{version}-%{release}
Requires:       pkg-config
Requires:       util-macros
Requires:       proto

%description    devel
It contains the libraries and header files to create applications

%prep
%autosetup -p1

%build
%configure \
  --disable-static

%make_build

%install
%make_install %{?_smp_mflags}

%check
%make_build check

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/

%changelog
* Thu Oct 05 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.3.2-2
- Fix devel package requires
* Thu Feb 23 2023 Shivani Agarwal <shivania2@vmware.com> 1.3.2-1
- Version update
* Tue Aug 03 2021 Alexey Makhalov <amakhalov@vmware.com> 1.3-1
- Version update
* Tue May 19 2015 Alexey Makhalov <amakhalov@vmware.com> 1.2-1
- initial version
