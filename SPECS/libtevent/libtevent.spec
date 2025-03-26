%global talloc_version 2.4.0

Name:           libtevent
Version:        0.14.1
Release:        2%{?dist}
Summary:        The tevent library
URL:            http://tevent.samba.org/
Vendor:         VMware, Inc.
Distribution:   Photon
Group:          Development/Libraries

Source0: http://samba.org/ftp/tevent/tevent-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires: docbook-xsl
BuildRequires: gcc
BuildRequires: libtalloc-devel >= %{talloc_version}
BuildRequires: libxslt-devel
BuildRequires: make
BuildRequires: which
BuildRequires: python3-devel
BuildRequires: python3-talloc-devel >= %{talloc_version}

Requires: glibc
Requires: libtalloc

Provides: bundled(libreplace)

%description
Tevent is an event system based on the talloc memory management library.
Tevent has support for many event types, including timers, signals, and
the classic file descriptor events.
Tevent also provide helpers to deal with asynchronous code providing the
tevent_req (Tevent Request) functions.

%package devel
Summary: Developer tools for the Tevent library
Requires: libtevent = %{version}-%{release}
Requires: libtalloc-devel >= %{talloc_version}

%description devel
Header files needed to develop programs that link against the Tevent library.

%package -n python3-tevent
Summary: Python 3 bindings for the Tevent library
Requires: libtevent = %{version}-%{release}
Requires: python3

%description -n python3-tevent
Python 3 bindings for libtevent

%prep
%autosetup -n tevent-%{version} -p1

%build
%configure --disable-rpath \
           --builtin-libraries=replace \
           --enable-debug

%make_build

%if 0%{?with_check}
%check
%make_build check
%endif

%install
%make_install %{?_smp_mflags}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/libtevent.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/tevent.h
%{_libdir}/libtevent.so
%{_libdir}/pkgconfig/tevent.pc
%{_libdir}/tevent/libcmocka-tevent.so

%files -n python3-tevent
%defattr(-,root,root)
%{python3_sitearch}/tevent.py
%{python3_sitearch}/_tevent.cpython*.so

%changelog
* Wed Dec 11 2024 Mukul Sikka <mukul.sikka@broadcom.com> 0.14.1-2
- Release bump for SRP compliance
* Tue Feb 14 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 0.14.1-1
- Initial addition to Photon. Needed for SSSD addition.
