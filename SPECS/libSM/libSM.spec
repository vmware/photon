Summary:        X11 SM runtime library.
Name:           libSM
Version:        1.2.4
Release:        2%{?dist}
URL:            http://www.x.org/
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://ftp.x.org/pub/individual/lib/%{name}-%{version}.tar.xz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  proto
BuildRequires:  libICE-devel
Requires:       libICE

%description
The X11 Session Management runtime library.

%package        devel
Summary:        Header and development files
Requires:       %{name} = %{version}-%{release}
Requires:       libICE-devel

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
*   Wed Dec 11 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.2.4-2
-   Release bump for SRP compliance
*   Sun Feb 12 2023 Shivani Agarwal <shivania2@vmware.com> 1.2.4-1
-   Upgrade version to 1.2.4
*   Tue May 19 2015 Alexey Makhalov <amakhalov@vmware.com> 1.2.2-1
-   initial version
