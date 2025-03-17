Summary:        X11 Cursor management library.
Name:           libXcursor
Version:        1.2.1
Release:        3%{?dist}
URL:            http://www.x.org
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://ftp.x.org/pub/individual/lib/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  libXfixes-devel
BuildRequires:  libXrender-devel

Requires:       libX11
Requires:       libXfixes
Requires:       libXrender

%description
The X11 Cursor management library.

%package    devel
Summary:    Header and development files
Requires:   %{name} = %{version}-%{release}
Requires:   libXfixes-devel
Requires:   libXrender-devel

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
%{_libdir}/pkgconfig
%{_datadir}/*

%changelog
* Wed Dec 11 2024 Ajay Kaher <ajay.kaher@broadcom.com> 1.2.1-3
- Release bump for SRP compliance
* Wed Jun 14 2023 Shivani Agarwal <shivania2@vmware.com> 1.2.1-2
- Bump version as a part of libX11 upgrade
* Thu Aug 18 2022 Shivani Agarwal <shivania2@vmware.com> 1.2.1-1
- Upgrade to version 1.2.1
* Tue May 19 2015 Alexey Makhalov <amakhalov@vmware.com> 1.1.14-1
- initial version
