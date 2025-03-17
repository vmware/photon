Summary:        X11 Damage extension.
Name:           libXdamage
Version:        1.1.5
Release:        2%{?dist}
URL:            http://www.x.org
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://ftp.x.org/pub/individual/lib/%{name}-%{version}.tar.bz2

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  libXfixes-devel
BuildRequires:  proto
BuildRequires:  util-macros

Requires:       libXfixes

%description
The X11 Damage extension.

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
%{_libdir}/*.so
%{_libdir}/pkgconfig

%changelog
* Wed Dec 11 2024 Ajay Kaher <ajay.kaher@broadcom.com> 1.1.5-2
- Release bump for SRP compliance
* Thu Aug 18 2022 Shivani Agarwal <shivania2@vmware.com> 1.1.5-1
- Upgrade to version 1.1.5
* Tue May 19 2015 Alexey Makhalov <amakhalov@vmware.com> 1.1.4-1
- initial version
