Summary:       LTTng-UST is an Userspace Tracer library
Name:          lttng-ust
Version:       2.13.5
Release:       2%{?dist}
URL:           https://lttng.org/download/
Group:         Development/Libraries
Vendor:        VMware, Inc.
Distribution:  Photon

Source0:        https://lttng.org/files/lttng-ust/%{name}-%{version}.tar.bz2
%define sha512 %{name}=3bf969e9deb6ce05a1ae30ad48676ae8ff63a73198583e98ce083d52b78e9fc2d171a6e3890c201abfa364600d4471d1ee8b1ee23de3faeec1f0ca84e0f0acd4

Source1: license.txt
%include %{SOURCE1}

BuildRequires: userspace-rcu-devel

%if 0%{?with_check}
BuildRequires: perl
%endif

Requires:      userspace-rcu
Provides:      liblttng-ust.so.0()(64bit)

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

%make_build

%install
%make_install %{?_smp_mflags}

%check
make %{?_smp_mflags} check

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
* Thu Dec 12 2024 Ajay Kaher <ajay.kaher@broadcom.com> 2.13.5-2
- Release bump for SRP compliance
* Tue Jan 31 2023 Gerrit Photon <photon-checkins@vmware.com> 2.13.5-1
- Automatic Version Bump
* Thu Sep 29 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.13.4-2
- Add Provides: liblttng-ust.so.0()(64bit) to fix dotnet-runtime build
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 2.13.4-1
- Automatic Version Bump
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
