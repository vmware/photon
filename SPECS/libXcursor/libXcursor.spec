Summary:        X11 Cursor management library.
Name:           libXcursor
Version:        1.2.1
Release:        2%{?dist}
License:        MIT
URL:            http://www.x.org
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://ftp.x.org/pub/individual/lib/%{name}-%{version}.tar.gz
%define sha512 %{name}=381c8762b5aa0dedb610e563bc595f901ec06eac0da832be4829f413869ce5092b47b33c2059d816e29dc525e5615358add98c305b9bda63c5ffac8b52b2e287

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
* Wed Jun 14 2023 Shivani Agarwal <shivania2@vmware.com> 1.2.1-2
- Bump version as a part of libX11 upgrade
* Thu Aug 18 2022 Shivani Agarwal <shivania2@vmware.com> 1.2.1-1
- Upgrade to version 1.2.1
* Tue May 19 2015 Alexey Makhalov <amakhalov@vmware.com> 1.1.14-1
- initial version
