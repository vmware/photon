Summary:        Library for low-level netlink programming interface to the in-kernel nf_tables subsystem
Name:           libnftnl
Version:        1.1.8
Release:        1%{?dist}
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
License:        GPLv2+
URL:            http://netfilter.org/projects/libnftnl/
Source0:        https://netfilter.org/projects/libnftnl/files/%{name}-%{version}.tar.bz2
%define sha1 %{name}-%{version}=a27cd5d53e2458fdcafbac81f71b90693d8c1aaf
Distribution:   Photon
BuildRequires:  libmnl-devel
BuildRequires:  jansson-devel

%description
libnftnl is a userspace library providing a low-level netlink programming interface (API) to the in-kernel nf_tables subsystem.

%package devel
Summary:    Development files for %{name}
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
%description    devel
Development files for %{name}

%prep
%autosetup

%build
%configure --disable-static \
        --disable-silent-rules \
        --with-json-parsing
make %{?_smp_mflags}

%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%install
make DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -delete

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc COPYING
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_libdir}/%{name}*.so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/%{name}

%changelog
* Mon Dec 14 2020 Gerrit Photon <photon-checkins@vmware.com> 1.1.8-1
- Automatic Version Bump
* Tue Oct 20 2020 Susant sahani <ssahani@vmware.com> 1.1.7-1
- Update to 1.1.7
* Mon Sep 10 2018 Ankit Jain <ankitja@vmware.com> 1.1.1-1
- Initial version
