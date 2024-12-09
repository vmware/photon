%define network_required 1
%global debug_package %{nil}

Summary:        Build Tools
Name:           mm-common
Version:        1.0.5
Release:        3%{?dist}
URL:            https://gitlab.gnome.org/GNOME/mm-common
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://gitlab.gnome.org/GNOME/mm-common/-/archive/%{version}/%{name}-%{version}.tar.gz
%define sha512 %{name}=dc538fb134c5f385a7508bbe702c562a796f0fafd3e25b46c5eb652bf3df36c6a309d36e8b6c074234c4ad4be3a75dd68c47d9d2a807e9a87bd10a10d1a0743b

Source1: https://gcc.gnu.org/onlinedocs/libstdc++/latest-doxygen/libstdc++-%{version}.ph5.tar.xz
%define sha512 libstdc++=c5073c558252ef1238fd310d428033f58252649a3ae5ba5a780047fb62727cf3335b22742f363155957bc94dfba58727bdbecf13ac94fb124fed71512bd494b7

Source2: license.txt
%include %{SOURCE2}

BuildRequires:  ca-certificates

%description
This module is part of the GNOME C++ bindings effort <http://www.gtkmm.org/>.
The mm-common module provides the build infrastructure and utilities shared among the GNOME C++ binding libraries.
It is only a required dependency for building the C++ bindings from the gnome.org version make control repository.
An installation of mm-common is not required for building tarball releases, unless configured to use maintainer-mode.

%prep
%autosetup -a1 -p1

%build
sh ./autogen.sh --disable-network
cp libstdc++.tag doctags/

%configure --disable-network
%make_build

%install
%make_install %{?_smp_mflags}

%check
%make_build check

%files
%defattr(-,root,root)
%{_bindir}/%{name}-get
%{_bindir}/%{name}-prepare
%{_datadir}/aclocal/*.m4
%{_mandir}/man1/*.gz
%{_datadir}/doc/%{name}/*
%{_datadir}/pkgconfig/*.pc
%{_datadir}/%{name}/build/*.*
%{_datadir}/%{name}/doctags/*.tag
%{_datadir}/%{name}/doctool/*.*

%changelog
* Thu Dec 12 2024 Ajay Kaher <ajay.kaher@broadcom.com> 1.0.5-3
- Release bump for SRP compliance
* Thu Jul 18 2024 Harinadh D <Harinadh.Dommaraju@broadcom.com> 1.0.5-2
- Build the package in offline
* Tue Dec 13 2022 Gerrit Photon <photon-checkins@vmware.com> 1.0.5-1
- Automatic Version Bump
* Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 1.0.4-1
- Automatic Version Bump
* Mon Oct 5 2020 Michelle Wang <michellew@vmware.com> 1.0.2-1
- Initial build and add this for libsigc++ build requires
