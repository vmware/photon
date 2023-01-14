Name:           meson
Summary:        Extremely fast and user friendly build system
Group:          Development/Tools
Version:        1.0.0
Release:        2%{?dist}
License:        ASL 2.0
URL:            https://mesonbuild.com
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/mesonbuild/meson/archive/%{version}/%{name}-%{version}.tar.gz
%define sha512 %{name}=9b1195cfe856c1aa51bc79f6eb4d0f94925bb02d0a9fbd68a6a6ced6e5c252b09b22d9aac812640687e49b8d64a313ce48d0a69a3bf83ea8ffb8c9dab559fc23

BuildArch:      noarch

BuildRequires:  gcc
BuildRequires:  python3-devel
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

install -Dpm0644 data/macros.%{name} %{buildroot}%{_rpmmacrodir}/macros.%{name}

%check
export MESON_PRINT_TEST_OUTPUT=1
python3 ./run_tests.py

%files
%defattr(-,root,root)
%license COPYING
%{_bindir}/%{name}
%{python3_sitelib}/mesonbuild/*
%{python3_sitelib}/%{name}-*.egg-info/
%{_mandir}/man1/%{name}.1*
%{_rpmmacrodir}/macros.%{name}
%dir %{_datadir}/polkit-1
%dir %{_datadir}/polkit-1/actions
%{_datadir}/polkit-1/actions/com.mesonbuild.install.policy

%changelog
* Sat Jan 14 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 1.0.0-2
- Bump version as a part of gettext upgrade
* Wed Jan 04 2023 Susant Sahani <ssahani@vmware.com> 1.0.0-1
- Update version
* Tue Dec 06 2022 Prashant S Chauhan <psinghchauha@vmware.com> 0.64.1-2
- Update release to compile with python 3.11
* Thu Nov 24 2022 Susant Sahani <ssahani@vmware.com> 0.64.1-1
- Update version
* Wed Aug 24 2022 Susant Sahani <ssahani@vmware.com> 0.63.1-1
- Update version
* Wed Dec 08 2021 Susant Sahani <ssahani@vmware.com> 0.60.2-1
- Update version
* Mon Jul 19 2021 Susant Sahani <ssahani@vmware.com> 0.59.0-1
- Update version
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
