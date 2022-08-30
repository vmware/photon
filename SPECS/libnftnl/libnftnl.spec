Summary:        Library for low-level netlink programming interface to the in-kernel nf_tables subsystem
Name:           libnftnl
Version:        1.2.3
Release:        1%{?dist}
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
License:        GPLv2+
URL:            http://netfilter.org/projects/libnftnl/
Source0:        https://netfilter.org/projects/libnftnl/files/%{name}-%{version}.tar.bz2
%define sha512 %{name}-%{version}=e2d16cbc062eb8900f0472abb8fe6b22910cc5a8efbb47445fe6ce6e2713a0637f74b46b2bf2031ba9ecb2e5eed932e3bbb49b015c7b7207591249de23d5149d
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
%autosetup -p1

%build
%configure  --disable-static --disable-silent-rules --with-json-parsing
%make_build %{?_smp_mflags}

%check
# make doesn't support _smp_mflags
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%install
%make_install
find %{buildroot} -name '*.la' -delete

%ldconfig_scriptlets

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
* Tue Aug 30 2022 Susant sahani <ssahani@vmware.com> 1.2.3-1
- Version bump
* Wed Dec 22 2021 Susant sahani <ssahani@vmware.com> 1.2.1-1
- Version bump
* Tue Jul 27 2021 Susant sahani <ssahani@vmware.com> 1.1.9-2
- Use ldconfig scriplets and switch autosetup
* Sun Jan 24 2021 Susant sahani <ssahani@vmware.com> 1.1.9-1
- Update to 1.1.9
* Fri Jul 10 2020 Susant sahani <ssahani@vmware.com> 1.1.7-1
- Update to 1.1.7
* Mon Sep 10 2018 Ankit Jain <ankitja@vmware.com> 1.1.1-1
- Initial version
