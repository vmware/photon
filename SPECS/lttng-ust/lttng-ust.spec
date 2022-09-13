Summary:       LTTng-UST is an Userspace Tracer library
Name:          lttng-ust
Version:       2.12.5
Release:       1%{?dist}
License:       GPLv2, LGPLv2.1 and MIT
URL:           https://lttng.org/download/
Source:        https://lttng.org/files/lttng-ust/%{name}-%{version}.tar.bz2
%define sha512 lttng-ust=7c1e39964f8eeb70c64ddb13e38de5dfff1abf6d133f9ee4b7e92545c93ea152ab75e1d63e15f3358d43fca98f109045f260095f84a4c1d53d0afdd59d239f7b
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
* Thu May 26 2022 Gerrit Photon <photon-checkins@vmware.com> 2.12.5-1
- Automatic Version Bump
- due to 2.13.* has issues with dotnet-runtime - https://github.com/dotnet/runtime/issues/57784
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
