Summary:       LTTng-UST is an Userspace Tracer library
Name:          lttng-ust
Version:       2.13.3
Release:       1%{?dist}
License:       GPLv2, LGPLv2.1 and MIT
URL:           https://lttng.org/download/
Source:        https://lttng.org/files/lttng-ust/%{name}-%{version}.tar.bz2
%define sha512 lttng-ust=7d83c64a86698e85cf1133cd2551e4e5f9f2544175fb756f47ec821ece24995305dc892dd681ac24fdb58956ed2c1d982f60b108bc6fbbc17b9244cc4b82d876
Group:         Development/Libraries
Vendor:        VMware, Inc.
Distribution:  Photon
BuildRequires: userspace-rcu-devel
%if %{with_check}
BuildRequires: perl
%endif
Requires:      userspace-rcu

%description
This library may be used by user-space applications to generate
trace-points using LTTng.

%package       devel
Summary:       The libraries and header files needed for LTTng-UST development.
Requires:      %{name} = %{version}-%{release}

%description   devel
The libraries and header files needed for LTTng-UST development.

%prep
%autosetup

%build
%configure \
	--docdir=%{_docdir}/%{name} \
	--disable-static \
	--disable-numa

make %{?_smp_mflags}

%check
make %{?_smp_mflags} check

%install
make DESTDIR=%{buildroot} %{?_smp_mflags} install
rm -vf %{buildroot}%{_libdir}/*.la

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
* Thu May 26 2022 Gerrit Photon <photon-checkins@vmware.com> 2.13.3-1
- Automatic Version Bump
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 2.12.1-1
- Automatic Version Bump
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
