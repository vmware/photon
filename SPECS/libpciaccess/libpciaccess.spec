Summary:        PCI access library.
Name:           libpciaccess
Version:        0.13.3
Release:        1%{?dist}
License:        MIT
URL:            http://www.x.org/
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:	http://ftp.x.org/pub/individual/lib/%{name}-%{version}.tar.bz2
%define sha512  libpciaccess=11ad783c6278e340973a621339cece3776c098952d0eaf96bfe745d013347e928c0883ed8444c5ddea870f5e4b3c25da16a44facb9d7fc1c8fea1c7e77bd592b

BuildRequires:  pkg-config
Provides:       pkgconfig(pciaccess)

%description
The PCI access library.

%package        devel
Summary:        Header and development files
Requires:       %{name} = %{version}-%{release}
Requires:       pkg-config

%description    devel
Development package for libpciaccess.

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
%{_libdir}/libpciaccess.so.0
%{_libdir}/libpciaccess.so.0.11.1

%files devel
%defattr(-,root,root)
%{_libdir}/pkgconfig
%{_includedir}/*
%{_libdir}/*.a
%{_libdir}/libpciaccess.so

%changelog
* Tue May 19 2015 Alexey Makhalov <amakhalov@vmware.com> 0.13.3-1
- initial version
