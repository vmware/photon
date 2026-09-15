%global build_if %{photon_subrelease} >= 91

Summary:        Linux-native io_uring I/O access library
Name:           liburing
Version:        2.15
Release:        1%{?dist}
Group:          Development/System
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/axboe/liburing

Source0: https://github.com/axboe/liburing/archive/refs/tags/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

%description
Provides native async IO for the Linux kernel, in a fast and efficient
manner, for both buffered and O_DIRECT.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description    devel
The liburing-devel package contains libraries and header files for
developing applications that use liburing.

%package        doc
Summary:        Documentation and man pages for %{name}
Requires:       %{name} = %{version}-%{release}

%description    doc
The liburing-doc package contains man pages for liburing.

%prep
%autosetup -p1 -n %{name}-%{name}-%{version}

%build
# liburing ships its own hand-written ./configure, %%configure wont work
sh ./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --libdevdir=%{_libdir} \
    --mandir=%{_mandir} \
    --includedir=%{_includedir} \
    --use-libc
%make_build

%install
%make_install %{?_smp_mflags}

%if 0%{?with_check}
%check
%define _make_output_sync %{nil}
export TEST_EXCLUDE="io-wq-unused-exit.t"
%make_build runtests
%endif

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/%{name}.so.*
%{_libdir}/%{name}-ffi.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/%{name}.h
%{_includedir}/%{name}/*
%{_libdir}/%{name}.so
%{_libdir}/%{name}-ffi.so
%exclude %{_libdir}/%{name}.a
%exclude %{_libdir}/%{name}-ffi.a
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/pkgconfig/%{name}-ffi.pc

%files doc
%defattr(-,root,root)
%{_mandir}/*/*

%changelog
* Tue Sep 15 2026 Mukul Sikka <mukul.sikka@broadcom.com> 2.15-1
- Initial version
