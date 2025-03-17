Summary:        X11 Composite Extension library.
Name:           libXcomposite
Version:        0.4.5
Release:        3%{?dist}
URL:            http://www.x.org/
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://ftp.x.org/pub/individual/lib/%{name}-%{version}.tar.bz2

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  proto
BuildRequires:  libXfixes-devel
BuildRequires:  util-macros

Requires:       libX11
Requires:       libXfixes

%description
The X11 Composite Extension library.

%package        devel
Summary:        Header and development files
Requires:       %{name} = %{version}-%{release}
Requires:       libXfixes-devel

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
%{_libdir}/*.a
%{_libdir}/pkgconfig
%{_libdir}/*.so
%{_datadir}/*

%changelog
* Wed Dec 11 2024 Ajay Kaher <ajay.kaher@broadcom.com> 0.4.5-3
- Release bump for SRP compliance
* Wed Jun 14 2023 Shivani Agarwal <shivania2@vmware.com> 0.4.5-2
- Bump version as a part of libX11 upgrade
* Fri Aug 06 2021 Alexey Makhalov <amakhalov@vmware.com> 0.4.5-1
- Version update
* Tue May 19 2015 Alexey Makhalov <amakhalov@vmware.com> 0.4.4-1
- initial version
