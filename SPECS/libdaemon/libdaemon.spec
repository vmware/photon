Summary:      Lightweight C library that eases the writing of UNIX daemons
Name:         libdaemon
Version:      0.14
Release:      4%{?dist}
URL:          http://0pointer.de/lennart/projects/libdaemon
Group:        System Environment/Libraries
Vendor:       VMware, Inc.
Distribution: Photon

Source0:      http://0pointer.de/lennart/projects/libdaemon/%{name}-%{version}.tar.gz
%define sha512  %{name}=a96b25c09bd63cc192c1c5f8b5bf34cc6ad0c32d42ac14b520add611423b6ad3d64091a47e0c7ab9a94476a5e645529abccea3ed6b23596567163fba88131ff2

Source1: license.txt
%include %{SOURCE1}

%description
The libdaemon package is a lightweight C library that eases the writing of UNIX daemons.

%package devel
Summary:    Development libraries and header files for libteam
Requires:   %{name} = %{version}-%{release}

%description devel
The package contains libraries and header files for
developing applications that use libdaemon.

%prep
%autosetup -p1

%build
%configure --disable-lynx
%make_build

%install
%make_install %{?_smp_mflags}

%ldconfig_scriptlets

%files
%defattr(-,root,root)
%doc LICENSE README
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_docdir}/%{name}/*
%{_libdir}/pkgconfig/*.pc
%dir %{_includedir}/libdaemon
%{_includedir}/libdaemon/*.h
%{_libdir}/*.a
%{_libdir}/*.so

%changelog
* Wed Dec 11 2024 Mukul Sikka <mukul.sikka@broadcom.com> 0.14-4
- Release bump for SRP compliance
* Sun Aug 07 2022 Shreenidhi Shedi <sshedi@vmware.com> 0.14-3
- Remove .la files
* Mon Aug 02 2021 Susant Sahani <ssahani@vmware.com> 0.14-2
- Use autosetup and ldconfig scriptlets
* Tue Dec 08 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 0.14-1
- Initial build.
