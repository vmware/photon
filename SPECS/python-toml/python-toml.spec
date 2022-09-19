Name:           python3-toml
Version:        0.10.2
Release:        1%{?dist}
Summary:        Python Library for Tom's Obvious, Minimal Language
Group:          Development/Libraries
License:        MIT
URL:            https://pypi.python.org/pypi/
Source0:        https://files.pythonhosted.org/packages/da/24/84d5c108e818ca294efe7c1ce237b42118643ce58a14d2462b3b2e3800d5/toml-%{version}.tar.gz
%define sha512  toml=ede2c8fed610a3827dba828f6e7ab7a8dbd5745e8ef7c0cd955219afdc83b9caea714deee09e853627f05ad1c525dc60426a6e9e16f58758aa028cb4d3db4b39
Vendor:         VMware, Inc.
Distribution:   Photon

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-packaging
BuildRequires:  python3-setuptools
BuildRequires:  python3-setuptools_scm

Requires:       python3

Provides:       python3dist(toml) = %{version}-%{release}
Provides:       python%{python3_version}dist(toml) = %{version}-%{release}

%description
Python Library for Tom's Obvious, Minimal Language

%prep
%autosetup -p1 -n toml-%{version}

%build
%py3_build

%install
%py3_install

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 0.10.2-1
- Automatic Version Bump
* Mon Sep 21 2020 Susant Sahani <ssahani@vmware.com> 0.10.1-1
- Initial rpm release
