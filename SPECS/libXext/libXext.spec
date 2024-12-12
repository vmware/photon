Summary:        library for common extensions to the X11 protocol.
Name:           libXext
Version:        1.3.4
Release:        4%{?dist}
URL:            http://www.x.org/
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://ftp.x.org/pub/individual/lib/%{name}-%{version}.tar.bz2
%define sha512  libXext=09146397d95f80c04701be1cc0a9c580ab5a085842ac31d17dfb6d4c2e42b4253b89cba695e54444e520be359883a76ffd02f42484c9e2ba2c33a5a40c29df4a

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  libX11-devel
Requires:       libX11
Requires:       freetype2
Provides:       pkgconfig(xext)

%description
Core X11 protocol client library.

%package        devel
Summary:        Header and development files for libXext
Requires:       %{name} = %{version}-%{release}
Requires:       libX11-devel
Requires:       freetype2-devel

%description    devel
libXext - library for common extensions to the X11 protocol.

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
* Wed Dec 11 2024 Ajay Kaher <ajay.kaher@broadcom.com> 1.3.4-4
- Release bump for SRP compliance
* Wed Jun 14 2023 Shivani Agarwal <shivania2@vmware.com> 1.3.4-3
- Bump version as a part of libX11 upgrade
* Wed Apr 19 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 1.3.4-2
- Bump version as a part of freetype2 upgrade
* Tue Jul 12 2022 Shivani Agarwal <shivania2@vmware.com> 1.3.4-1
- Upgrade to 1.3.4
* Mon May 18 2015 Alexey Makhalov <amakhalov@vmware.com> 1.3.3-1
- initial version
