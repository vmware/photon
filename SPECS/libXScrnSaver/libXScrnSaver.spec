Summary:        X11 Screen Saver runtime library.
Name:           libXScrnSaver
Version:        1.2.3
Release:        3%{?dist}
URL:            http://www.x.org/
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://ftp.x.org/pub/individual/lib/%{name}-%{version}.tar.bz2
%define sha512 %{name}=7ea628324a11b25ee82c7b11c6bf98f37de219354de51c1e29467b5de422669ba1ab121f3b9dc674093c8f3960e93c5d5428122f5539092f79bc8451c768354a

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  proto
BuildRequires:  libXext-devel

Requires:       libXext
Requires:       libX11

%description
The X11 Screen Saver runtime library.

%package        devel
Summary:        Header and development files
Requires:       %{name} = %{version}-%{release}
Requires:       proto
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

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig
%{_libdir}/*.a
%{_datadir}/*

%changelog
* Wed Dec 11 2024 Ajay Kaher <ajay.kaher@broadcom.com> 1.2.3-3
- Release bump for SRP compliance
* Wed Jun 14 2023 Shivani Agarwal <shivania2@vmware.com> 1.2.3-2
- Bump version as a part of libX11 upgrade
* Fri Aug 19 2022 Shivani Agarwal <shivania2@vmware.com> 1.2.3-1
- Upgrade version 1.2.3
* Tue May 19 2015 Alexey Makhalov <amakhalov@vmware.com> 1.2.2-1
- initial version
