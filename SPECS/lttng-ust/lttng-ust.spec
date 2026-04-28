Summary:       LTTng-UST is an Userspace Tracer library
Name:          lttng-ust
Version:       2.13.5
Release:       1%{?dist}
License:       GPLv2, LGPLv2.1 and MIT
URL:           https://lttng.org/download/
Group:         Development/Libraries
Vendor:        VMware, Inc.
Distribution:  Photon

Source0: https://lttng.org/files/lttng-ust/%{name}-%{version}.tar.bz2
%define sha512 %{name}=3bf969e9deb6ce05a1ae30ad48676ae8ff63a73198583e98ce083d52b78e9fc2d171a6e3890c201abfa364600d4471d1ee8b1ee23de3faeec1f0ca84e0f0acd4

BuildRequires: userspace-rcu-devel

%if 0%{?with_check}
BuildRequires: perl
%endif

Requires:      userspace-rcu
Provides:      liblttng-ust.so.0()(64bit)

%description
This library may be used by user-space applications to generate
trace-points using LTTng.

%package devel
Summary:    The libraries and header files needed for LTTng-UST development.
Requires:   %{name} = %{version}-%{release}
Requires:   userspace-rcu-devel

%description devel
The libraries and header files needed for LTTng-UST development.

%prep
%autosetup -p1

%build
%configure \
    --docdir=%{_docdir}/%{name} \
    --disable-static \
    --disable-numa

%make_build

%install
%make_install %{?_smp_mflags}
rm -v %{buildroot}%{_libdir}/*.la

%if 0%{?with_check}
%check
%make_build check
%endif

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so.*
%{_datadir}/*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/lttng-ust*.pc

%changelog
* Thu Apr 23 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.13.5-1
- Upgrade to v2.13.5
* Tue Jun 30 2020 Gerrit Photon <photon-checkins@vmware.com> 2.12.0-1
- Automatic Version Bump
* Tue Mar 24 2020 Alexey Makhalov <amakhalov@vmware.com> 2.10.2-3
- Fix compilation issue with glibc >= 2.30.
* Wed Jan 02 2019 Keerthana K <keerthanak@vmware.com> 2.10.2-2
- Added make check.
* Wed Sep 05 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 2.10.2-1
- Update to version 2.10.2
* Mon Dec 19 2016 Dheeraj Shetty <dheerajs@vmware.com> 2.9.0-1
- Initial build. First version
