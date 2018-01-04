%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           meson
Summary:        Extremely fast and user friendly build system
Version:        0.44.0
Release:        1%{?dist}
License:        ASL 2.0
URL:            https://mesonbuild.com/
Source0:        https://github.com/mesonbuild/meson/archive/%{version}/%{name}-%{version}.tar.gz
%define sha1    meson=4a5aa56f81fc1350a5c501ef6046eef8a13467c7
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

%description
Meson is an open source build system meant to be both extremely fast, 
and, even more importantly, as user friendly as possible.
The main design point of Meson is that every moment a developer spends 
writing or debugging build definitions is a second wasted. 
So is every second spent waiting for the build system to actually start compiling code.

%prep
%setup 

%build

%install
python3 setup.py install --root=%{buildroot}/
install -Dpm0644 data/macros.%{name} %{buildroot}%{_libdir}/rpm/macros.d/macros.%{name}

%check
export MESON_PRINT_TEST_OUTPUT=1
python3 ./run_tests.py

%files
%license COPYING
%{_bindir}/%{name}
%{_bindir}/%{name}conf
%{_bindir}/%{name}introspect
%{_bindir}/%{name}test
%{_bindir}/wraptool
%{python3_sitelib}/mesonbuild
%{python3_sitelib}/%{name}-*.egg-info
%{_mandir}/man1/%{name}.1*
%{_mandir}/man1/%{name}conf.1*
%{_mandir}/man1/%{name}introspect.1*
%{_mandir}/man1/%{name}test.1*
%{_mandir}/man1/wraptool.1*
%{_libdir}/rpm/macros.d/macros.%{name}

%changelog
*   Wed Dec 27 2017 Anish Swaminathan <anishs@vmware.com> 0.44.0-1
-   Initial packaging

