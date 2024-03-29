Summary:         X11 libXt runtime library.
Name:            libXt
Version:         1.2.1
Release:         2%{?dist}
License:         MIT
URL:             http://www.x.org/
Group:           System Environment/Libraries
Vendor:          VMware, Inc.
Distribution:    Photon
Source0:         http://ftp.x.org/pub/individual/lib/%{name}-%{version}.tar.bz2
%define sha512   libXt=6877af61ba91eeed6b6f80471b84f354ad0ec0827249c7ee0a00c13508063fe8d2696dd400a4bdbc6ca2ff67cbe1317ad5ac24522fd96099dc56535e33ca052c
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
*   Wed Jun 14 2023 Shivani Agarwal <shivania2@vmware.com> 1.2.1-2
-   Bump version as a part of libX11 upgrade
*   Sun Feb 12 2023 Shivani Agarwal <shivania2@vmware.com> 1.2.1-1
-   Upgraded version
*   Tue May 19 2015 Alexey Makhalov <amakhalov@vmware.com> 1.1.4-1
-   initial version
