Summary:        X11 XFIXES extension.
Name:           libXfixes
Version:        5.0.3
Release:        3%{?dist}
URL:            http://www.x.org
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://ftp.x.org/pub/individual/lib/%{name}-%{version}.tar.bz2

Source1: license.txt
%include %{SOURCE1}

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
* Wed Dec 11 2024 Ajay Kaher <ajay.kaher@broadcom.com> 5.0.3-3
- Release bump for SRP compliance
* Wed Jun 14 2023 Shivani Agarwal <shivania2@vmware.com> 5.0.3-2
- Bump version as a part of libX11 upgrade
* Thu Aug 18 2022 Shivani Agarwal <shivania2@vmware.com> 5.0.3-1
- Upgrade version to 5.0.3
* Tue May 19 2015 Alexey Makhalov <amakhalov@vmware.com> 5.0.1-1
- initial version
