Summary:        X11 Fontenc runtime library.
Name:           libfontenc
Version:        1.1.2
Release:        3%{?dist}
URL:            http://www.x.org
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://ftp.x.org/pub/individual/lib/%{name}-%{version}.tar.bz2

Source1: license.txt
%include %{SOURCE1}

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

%ldconfig_scriptlets

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
* Wed Dec 11 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.1.2-3
- Release bump for SRP compliance
* Fri Apr 14 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.1.2-2
- Bump version as a part of zlib upgrade
* Tue May 19 2015 Alexey Makhalov <amakhalov@vmware.com> 1.1.2-1
- initial version
