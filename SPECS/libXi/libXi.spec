Summary:        X11 libXi runtime library.
Name:           libXi
Version:        1.7.10
Release:        1%{?dist}
License:        MIT
URL:            http://www.x.org
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://ftp.x.org/pub/individual/lib/%{name}-%{version}.tar.bz2
%define sha512 %{name}=591f0860bf5904897587c4990d6c852f3729a212d1ef390362d41242440e078221877c31db2232d5cc81727fe97f4e194b077f7de917e251e60641bbd06ee218

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
* Wed Jun 21 2023 Kuntal Nayak <nkuntal@vmware.com> 1.7.10-1
- Version upgrade for CVE-2016-7945 fix
* Wed Jun 14 2023 Shivani Agarwal <shivania2@vmware.com> 1.7.4-2
- Bump version as a part of libX11 upgrade
* Tue May 19 2015 Alexey Makhalov <amakhalov@vmware.com> 1.7.4-1
- initial version
