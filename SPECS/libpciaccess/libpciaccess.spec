Summary:        PCI access library.
Name:           libpciaccess
Version:        0.16
Release:        2%{?dist}
URL:            http://www.x.org/
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://ftp.x.org/pub/individual/lib/%{name}-%{version}.tar.bz2

Source1: license.txt
%include %{SOURCE1}

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
* Wed Dec 11 2024 Mukul Sikka <mukul.sikka@broadcom.com> 0.16-2
- Release bump for SRP compliance
* Thu Oct 06 2022 Gerrit Photon <photon-checkins@vmware.com> 0.16-1
- Automatic Version Bump
* Tue May 19 2015 Alexey Makhalov <amakhalov@vmware.com> 0.13.3-1
- initial version
