Summary:        Library for low-level netlink programming interface to the in-kernel nf_tables subsystem
Name:           libnftnl
Version:        1.2.4
Release:        2%{?dist}
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
License:        GPLv2+
URL:            http://netfilter.org/projects/libnftnl
Distribution:   Photon

Source0: https://netfilter.org/projects/libnftnl/files/%{name}-%{version}.tar.bz2
%define sha512 %{name}-%{version}=5375d1d15627aabf25129433630395f53009b22a255fcd113b302af7f2f0a234fd54c827b0ef1c8fd3a13e272a1696f780560672d4af6abad0e19805f9d56326

BuildRequires:  libmnl-devel

Requires: libmnl

%description
libnftnl is a userspace library providing a low-level netlink programming interface (API) to the in-kernel nf_tables subsystem.

%package devel
Summary:    Development files for %{name}
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
Requires:   libmnl-devel

%description    devel
Development files for %{name}

%prep
%autosetup -p1

%build
%configure \
  --disable-static \
  --disable-silent-rules

%make_build

%install
%make_install %{?_smp_mflags}

%check
%make_build check

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
* Wed Sep 27 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.2.4-2
- Fix devel package requires
* Thu Jan 05 2023 Susant sahani <ssahani@vmware.com> 1.2.4-1
- Version bump
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
