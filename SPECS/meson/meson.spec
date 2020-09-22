%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           meson
Summary:        Extremely fast and user friendly build system
Group:          Development/Tools
Version:        0.55.3
Release:        1%{?dist}
License:        ASL 2.0
URL:            https://mesonbuild.com/
Vendor:         VMware, Inc.
Distribution:   Photon
Group:          Applications/System
Source0:        https://github.com/mesonbuild/meson/archive/%{version}/%{name}-%{version}.tar.gz
%define sha1    meson=6a6ca4d36eb8cdf954beff08c653fc72cf336527
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
python3 setup.py build

%install
python3 setup.py  install --root=%{buildroot}/

install -Dpm0644 data/macros.%{name} %{buildroot}%{_libdir}/rpm/macros.d/macros.%{name}

%check
export MESON_PRINT_TEST_OUTPUT=1
python3 ./run_tests.py

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
*   Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 0.55.3-1
-   Automatic Version Bump
*   Thu Sep 10 2020 Gerrit Photon <photon-checkins@vmware.com> 0.55.2-1
-   Automatic Version Bump
*   Wed Aug 26 2020 Keerthana K <keerthanak@vmware.com> 0.55.1-3
-   Remove python3-gobject-introspection as it creates a circular
-   dependency for glib build.
*   Sat Aug 22 2020 Ankit Jain <ankitja@vmware.com> 0.55.1-2
-   Added python3-gobject-introspection requires
*   Wed Aug 19 2020 Gerrit Photon <photon-checkins@vmware.com> 0.55.1-1
-   Automatic Version Bump
*   Wed Aug 12 2020 Susant Sahani <ssahani@vmware.com> 0.55.0-1
-   Update to version 0.55.0-1
*   Mon Sep 10 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 0.47.2-1
-   Update to version 0.47.2
*   Wed Dec 27 2017 Anish Swaminathan <anishs@vmware.com> 0.44.0-1
-   Initial packaging
