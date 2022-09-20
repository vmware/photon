Summary:        X11 Damage extension.
Name:           libXdamage
Version:        1.1.5
Release:        1%{?dist}
License:        MIT
URL:            http://www.x.org
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://ftp.x.org/pub/individual/lib/%{name}-%{version}.tar.bz2
%define sha512 %{name}=a3ca6cc33b1727f717a3e2aa5593f660508a81a47918a0aa949e9e8fba105e303fe5071983b48caac92feea0fe6e8e01620805e4d19b41f21f20d837b191c124

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
* Thu Aug 18 2022 Shivani Agarwal <shivania2@vmware.com> 1.1.5-1
- Upgrade to version 1.1.5
* Tue May 19 2015 Alexey Makhalov <amakhalov@vmware.com> 1.1.4-1
- initial version
