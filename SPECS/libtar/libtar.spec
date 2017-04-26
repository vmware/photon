Summary:        C library for manipulating tar files
Name:           libtar
Version:        1.2.20
Release:        2%{?dist}
URL:            https://github.com/tklauser/libtar/archive/v1.2.20.tar.gz
License:        MIT
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        libtar-%{version}.tar.gz
%define         sha1 libtar=b3ec4058fa83448d6040ce9f9acf85eeec4530b1
Patch0:         libtar-gen-debuginfo.patch
Provides:       libtar.so.0()(64bit)

%description
libtar is a library for manipulating tar files from within C programs.

%package        devel
Summary:        Development files for libtar
Group:          Development/Libraries
Requires:       libtar = %{version}-%{release}

%description    devel
The litar-devel package contains libraries and header files for
developing applications that use libtar.

%prep
%setup
%patch0
autoreconf -iv

%build
%configure CFLAGS="%{optflags}" STRIP=/bin/true --disable-static
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
chmod +x %{buildroot}/%{_libdir}/libtar.so.*

%check
make %{?_smp_mflags} check

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/libtar
%{_libdir}/libtar.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_mandir}/man3/*
%{_libdir}/libtar.so
%{_libdir}/libtar.la

%changelog
*   Fri Mar 10 2017 Xiaolin Li <xiaolinl@vmware.com> 1.2.20-2
-   Provides libtar.so.0()(64bit).
*   Fri Mar 03 2017 Xiaolin Li <xiaolinl@vmware.com> 1.2.20-1
-   Initial packaging for Photon
