Summary:         X11 libXt runtime library.
Name:            libXt
Version:         1.2.1
Release:         3%{?dist}
URL:             http://www.x.org/
Group:           System Environment/Libraries
Vendor:          VMware, Inc.
Distribution:    Photon
Source0:         http://ftp.x.org/pub/individual/lib/%{name}-%{version}.tar.bz2

Source1: license.txt
%include %{SOURCE1}
BuildRequires:   libX11-devel
BuildRequires:   libSM-devel
BuildRequires:   proto
Requires:        libSM
Requires:        libICE
Requires:        libX11

%description
The X11 Toolkit Intrinsics library.

%package        devel
Summary:        Header and development files
Requires:       %{name} = %{version}-%{release}
Requires:       libX11-devel
Requires:       libSM-devel

%description    devel
It contains the libraries and header files to create applications

%prep
%autosetup -p1

%build
%configure --with-appdefaultdir=%{_sysconfdir}/X11/app-defaults
%make_build

%install
%make_install %{?_smp_mflags}

%ldconfig_scriptlets

%clean
rm -rf %{buildroot}/*

%check
make %{?_smp_mflags} check

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
*   Wed Dec 11 2024 Ajay Kaher <ajay.kaher@broadcom.com> 1.2.1-3
-   Release bump for SRP compliance
*   Wed Jun 14 2023 Shivani Agarwal <shivania2@vmware.com> 1.2.1-2
-   Bump version as a part of libX11 upgrade
*   Sun Feb 12 2023 Shivani Agarwal <shivania2@vmware.com> 1.2.1-1
-   Upgraded version
*   Tue May 19 2015 Alexey Makhalov <amakhalov@vmware.com> 1.1.4-1
-   initial version
