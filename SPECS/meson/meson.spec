Name:           meson
Summary:        Extremely fast and user friendly build system
Group:          Development/Tools
Version:        0.56.2
Release:        1%{?dist}
License:        ASL 2.0
URL:            https://mesonbuild.com
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/mesonbuild/meson/archive/%{version}/%{name}-%{version}.tar.gz
%define sha512 %{name}=5304db3d1ed9ebccac67490ad112fc766a30d4bef64af79e655e2338d216fc67a66b35009d617d3045f43d21955ce7293c5457a5311efc664737190bffea9864

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

%check
python3 ./run_tests.py

%files
%license COPYING
%{_bindir}/%{name}
%{python3_sitelib}/mesonbuild/*
%{python3_sitelib}/%{name}-*.egg-info/
%{_mandir}/man1/%{name}.1*
%dir %{_datadir}/polkit-1
%dir %{_datadir}/polkit-1/actions
%{_datadir}/polkit-1/actions/com.mesonbuild.install.policy

%changelog
* Tue Aug 09 2022 Shreenidhi Shedi <sshedi@vmware.com> 0.56.2-1
- Upgrade to v0.56.2, needed for libslirp.
* Mon Sep 10 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 0.47.2-1
- Update to version 0.47.2
* Wed Dec 27 2017 Anish Swaminathan <anishs@vmware.com> 0.44.0-1
- Initial packaging
