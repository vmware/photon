Name:           meson
Summary:        Extremely fast and user friendly build system
Group:          Development/Tools
Version:        1.3.2
Release:        1%{?dist}
License:        ASL 2.0
URL:            https://mesonbuild.com/
Vendor:         VMware, Inc.
Distribution:   Photon
Group:          Applications/System
Source0:        https://github.com/mesonbuild/meson/archive/%{version}/%{name}-%{version}.tar.gz
%define sha512  meson=b44c28bb8d5ca955b74d64c13b845adfeed814afd92d15ecc8cedb0674932063972644b7fba3a1e60aa76ff2ecea8ab40108a8210ff3698900215342096f35d2
BuildArch:      noarch
BuildRequires:  gcc
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  ninja-build
BuildRequires:  gtest-devel
BuildRequires:  gmock-devel
BuildRequires:  gettext

Requires:       ninja-build
Requires:       python3
Requires:       python3-setuptools

%description
Meson is an open source build system meant to be both extremely fast,
and, even more importantly, as user friendly as possible. The main design
point of Meson is that every moment a developer spends writing or debugging
build definitions is a second wasted. So is every second spent waiting for
the build system to actually start compiling code.

%prep
%autosetup -p1

%build
%py3_build

%install
%py3_install

install -Dpm0644 data/macros.%{name} %{buildroot}%{_libdir}/rpm/macros.d/macros.%{name}

%check
export MESON_PRINT_TEST_OUTPUT=1

%files
%license COPYING
%{_bindir}/%{name}
%{python3_sitelib}/mesonbuild/*
%{python3_sitelib}/%{name}-*.egg-info/
%{_mandir}/man1/%{name}.1*
%{_libdir}/rpm/macros.d/macros.%{name}
%dir %{_datadir}/polkit-1
%dir %{_datadir}/polkit-1/actions
%{_datadir}/polkit-1/actions/com.mesonbuild.install.policy

%changelog
* Wed Jan 22 2025 Tapas Kundu <tapas.kundu@broadcom.com> 1.3.2-1
- Update to 1.3.2
* Mon Jan 16 2023 Shivani Agarwal <shivania2@vmware.com> 0.64.1-1
- Upgrade version
* Wed Oct 26 2022 Shivani Agarwal <shivania2@vmware.com> 0.60.2-1
- Update version
* Mon Dec 13 2021 Susant Sahani <ssahani@vmware.com> 0.56.2-3
- Use python macros
* Thu Dec 09 2021 Prashant S Chauhan <psinghchauha@vmware.com> 0.56.2-2
- Bump up to compile with python 3.10
* Sat Jan 23 2021 Susant Sahani <ssahani@vmware.com> 0.56.2-1
- Update to version 0.56.2-1
* Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 0.55.3-1
- Automatic Version Bump
* Thu Sep 10 2020 Gerrit Photon <photon-checkins@vmware.com> 0.55.2-1
- Automatic Version Bump
* Wed Aug 26 2020 Keerthana K <keerthanak@vmware.com> 0.55.1-3
- Remove python3-gobject-introspection as it creates a circular
- dependency for glib build.
* Sat Aug 22 2020 Ankit Jain <ankitja@vmware.com> 0.55.1-2
- Added python3-gobject-introspection requires
* Wed Aug 19 2020 Gerrit Photon <photon-checkins@vmware.com> 0.55.1-1
- Automatic Version Bump
* Wed Aug 12 2020 Susant Sahani <ssahani@vmware.com> 0.55.0-1
- Update to version 0.55.0-1
* Mon Sep 10 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 0.47.2-1
- Update to version 0.47.2
* Wed Dec 27 2017 Anish Swaminathan <anishs@vmware.com> 0.44.0-1
- Initial packaging
