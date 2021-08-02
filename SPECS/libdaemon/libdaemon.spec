Summary:      Lightweight C library that eases the writing of UNIX daemons
Name:         libdaemon
Version:      0.14
Release:      2%{?dist}
License:      LGPL 2.1+
URL:          http://0pointer.de/lennart/projects/libdaemon
Source0:      http://0pointer.de/lennart/projects/libdaemon/%{name}-%{version}.tar.gz
%define sha1 libdaemon=78a4db58cf3a7a8906c35592434e37680ca83b8f
Group:        System Environment/Libraries
Vendor:       VMware, Inc.
Distribution: Photon
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
%configure  \
    --disable-lynx
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

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
%{_libdir}/*.la
%{_libdir}/*.a
%{_libdir}/*.so

%changelog
* Mon Aug 02 2021 Susant Sahani <ssahani@vmware.com> 0.14-2
- Use autosetup and ldconfig scriptlets
* Tue Dec 08 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 0.14-1
- Initial build.
