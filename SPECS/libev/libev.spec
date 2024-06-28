Summary:    A full-featured and high-performance event loop
Name:       libev
Version:    4.33
Release:    3%{?dist}
License:    BSD-2-Clause
URL:        http://software.schmorp.de/pkg/libev.html
Group:      System/Library
Vendor:     VMware, Inc.
Distribution:   Photon

Source0: http://dist.schmorp.de/libev/%{name}-%{version}.tar.gz
%define sha512 %{name}=c662a65360115e0b2598e3e8824cf7b33360c43a96ac9233f6b6ea2873a10102551773cad0e89e738541e75af9fd4f3e3c11cd2f251c5703aa24f193128b896b

BuildRequires:  pkg-config
#BuildRequires:  openssl-devel
#Requires:       openssl

%description
A full-featured and high-performance event loop that is loosely modelled after libevent, but without its limitations and bugs.

%package        devel
Summary:        Development files for libev
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The subpackage includes all development related headers and library for libev

%prep
%autosetup -p1

%build
%configure --disable-static
%make_build

%install
%make_install %{?_smp_mflags}

%check
make %{?_smp_mflags} check

%post -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/*.so.*
%{_mandir}/*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so

%changelog
* Sun Nov 19 2023 Shreenidhi Shedi <sshedi@vmware.com> 4.33-3
- Bump version as a part of openssl upgrade
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 4.33-2
- openssl 1.1.1
* Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 4.33-1
- Automatic Version Bump
* Mon Apr 03 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.24-1
- Initial Version.
