%global talloc_version 2.3.4

Name:           libtevent
Version:        0.13.0
Release:        1%{?dist}
Summary:        The tevent library
License:        LGPLv3+
URL:            http://tevent.samba.org/
Vendor:         VMware, Inc.
Distribution:   Photon
Group:          Development/Libraries

Source0: http://samba.org/ftp/tevent/tevent-%{version}.tar.gz
%define sha512 tevent=7aa05c09e3c708769e31cda88b319cee3629c88c51bda559193a85d4ab32204a8b4ba11f142861dbca06b578bf54953f2aca1ad847e99995a4fc40bf08618a93

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
* Thu Sep 22 2022 Brennan Lamoreaux <blamoreaux@vmware.com> 0.13.0-1
- Initial addition to Photon. Needed for SSSD addition.
