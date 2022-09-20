Summary:        X11 libXi runtime library.
Name:           libXi
Version:        1.7.4
Release:        1%{?dist}
License:        MIT
URL:            http://www.x.org
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://ftp.x.org/pub/individual/lib/%{name}-%{version}.tar.bz2
%define sha512 %{name}=17182e580bdf6d65c743ceef4f652f7c7975761f288dfd6f2961c2fed23931569f7cf7cac745bb252fe0a6c3be2739ba6f6533b895519800e382a48f2e5297f0

BuildRequires:  libXfixes-devel
BuildRequires:  proto

Requires:       libXfixes
Requires:       libX11
Requires:       libXext

Provides:       pkgconfig(xi)

%description
The X11 libXi runtime library.

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
%{_libdir}/*.so
%{_libdir}/pkgconfig
%{_libdir}/*.a
%{_datadir}/*

%changelog
* Tue May 19 2015 Alexey Makhalov <amakhalov@vmware.com> 1.7.4-1
- initial version
