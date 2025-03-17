Summary:        X11 ICE runtime library.
Name:           libICE
Version:        1.1.1
Release:        2%{?dist}
URL:            http://www.x.org/
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://ftp.x.org/pub/individual/lib/%{name}-%{version}.tar.xz

Source1: license.txt
%include %{SOURCE1}
BuildRequires:  xtrans
BuildRequires:  proto

%description
The X11 Inter-Client Exchange runtime library.

%package    devel
Summary:    Header and development files
Requires:   %{name} = %{version}-%{release}
Requires:   xtrans

%description    devel
It contains the libraries and header files to create applications

%prep
%autosetup

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
*   Wed Dec 11 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.1.1-2
-   Release bump for SRP compliance
*   Sun Feb 12 2023 Shivani Agarwal <shivania2@vmware.com> 1.1.1-1
-   upgrade version to 1.1.1
*   Tue May 19 2015 Alexey Makhalov <amakhalov@vmware.com> 1.0.9-1
-   initial version
